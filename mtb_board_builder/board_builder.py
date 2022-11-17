import json
import os
import sys
import time

cur_dir = os.path.dirname(__file__)
helper_dir = os.path.join(cur_dir, "..", "tools")
sys.path.append(helper_dir)
from config import (
    status_board_id,
    sandbox_mtb_boards_folder_id,
    measure_tracking_board_id,
)
from tools import query_helper

start = time.time()


def columntype_helper(column_type, column_id, column_value, column_text):
    if column_value is not None or (column_text != "" and column_text is not None):
        match column_type:
            case "board-relation":
                column_data = json.dumps(
                    {
                        column_id: {
                            "item_ids": [
                                json.loads(column_value)["linkedPulseIds"][0][
                                    "linkedPulseId"
                                ]
                            ]
                        }
                    }
                )
                return column_data
            case "color":
                column_data = json.dumps({column_id: {"label": column_text}})
                return column_data
            case "date":
                column_data = json.dumps({column_id: {"date": column_text}})
                return column_data
            case "dropdown":
                column_data = json.dumps(
                    {column_id: {"labels": column_text.split(", ")}}
                )
                return column_data
            case "multiple-person":
                column_data = json.dumps(
                    {
                        column_id: {
                            "personsAndTeams": json.loads(column_value)[
                                "personsAndTeams"
                            ]
                        }
                    }
                )
                return column_data
            case "timerange":
                column_value = json.loads(column_value)
                column_value.pop("changed_at")
                column_data = json.dumps({column_id: column_value})
                return column_data
            case "text":
                column_data = json.dumps({column_id: column_text})
                return column_data


status_ingest = query_helper(
    "query($board_id:Int!, $item_id:Int!) {boards(ids:[$board_id]){items(ids:[$item_id]) {name column_values(ids:[text3]){value text}}}}",
    {
        "board_id": status_board_id,
        "item_id": [
            ,
        ],
    },
)
status_list = status_ingest["data"]["boards"][0]["items"]

for groups in status_list:
    if groups["name"] != "USACS Management Group, LTD."
        new_mtb_ingest = query_helper(
            "mutation($board_name:String!, $folder_id:Int!){create_board(folder_id:$folder_id,board_name: $board_name,board_kind:public,template_id:3486332223){id}}",
            {
                "folder_id": sandbox_mtb_boards_folder_id,
                "board_name": groups["name"],
            },
        )
        new_mtb_board_id = int(new_mtb_ingest["data"]["create_board"]["id"])
        new_mtb_col_list = query_helper(
            "query($board_id:Int!) {boards(ids:[$board_id]){items(limit:1) {column_values{title id type}}}}",
            {"board_id": new_mtb_board_id},
        )["data"]["boards"][0]["items"][0]
        new_mtb_ingest = query_helper(
            "query($board_id:Int!){boards(ids:[$board_id]){items{name id}}}",
            {"board_id": new_mtb_board_id},
        )
        new_mtb_list = new_mtb_ingest["data"]["boards"][0]["items"]
        mtb_ingest = query_helper(
            "query($board_id:Int!, $col_id:String!, $col_val:String!) {items_by_column_values (board_id: $board_id, column_id: $col_id , column_value: $col_val){name column_values{title type text value} updates{body creator{name}}}}",
            {
                "board_id": measure_tracking_board_id,
                "col_id": "text4",
                "col_val": groups["name"],
            },
        )
        col_id = None
        col_type = None
        col_val = None
        col_txt = None
        mtb_measure_list = mtb_ingest["data"]["items_by_column_values"]
        for new_measure in new_mtb_list:
            for measure in mtb_measure_list:
                if measure["name"].find(new_measure["name"].split(" - ")[0]) != -1:
                    for new_mtb_column in new_mtb_col_list["column_values"]:
                        if new_mtb_column["title"] != "Subitems":
                            for mtb_column in measure["column_values"]:
                                if (
                                    mtb_column["title"] == new_mtb_column["title"]
                                    and mtb_column["title"] != "Subitems"
                                    and mtb_column["title"] != "MTB Helper"
                                ):
                                    col_id = new_mtb_column["id"]
                                    col_type = mtb_column["type"]
                                    if col_type == "multiple-person":
                                        col_val = groups["column_values"][0]["value"]
                                        col_txt = groups["column_values"][0]["text"]
                                    else:
                                        col_val = mtb_column["value"]
                                        col_txt = mtb_column["text"]
                                    query_helper(
                                        "mutation($board_id:Int!,$item_id:Int!,$col_val:JSON!){change_multiple_column_values(item_id: $item_id, board_id: $board_id, column_values: $col_val){id}}",
                                        {
                                            "board_id": new_mtb_board_id,
                                            "item_id": int(new_measure["id"]),
                                            "col_val": columntype_helper(
                                                col_type, col_id, col_val, col_txt
                                            ),
                                        },
                                    )
                    date = measure["updates"][0]["created_at"].split("T")[0]
                    user = measure["updates"][0]["creator"]["name"]
                    body = measure["updates"][0]["body"]
                    new_body = f"{user} said {body} at {date}"
                    query_helper(
                        "mutation($item_id:Int!,$body:String!){create_update(item_id: $item_id, body: $body){id}}",
                        {"item_id": int(measure["id"]), "body": new_body},
                    )

end = time.time()
print(end - start)
