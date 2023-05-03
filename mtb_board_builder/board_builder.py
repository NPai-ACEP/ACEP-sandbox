import time

start = time.time()
import os
import sys
import json


cur_dir = os.path.dirname(__file__)
helper_dir = os.path.join(cur_dir, "..", "tools")
sys.path.append(helper_dir)
from config import (
    ed_mgmt_board_id,
    sandbox_mtb_boards_folder_id,
    measure_tracking_board_id,
    sandbox_mtb_board_id,
)
from tools import query_helper


def columntype_helper(column_type, column_id, column_value, column_text):
    if column_value is not None or (column_text != "" and column_text is not None):
        match column_type:
            case "board-relation":
                column_data = json.dumps({column_id: {"item_ids": [column_value]}})
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
    "query($board_id:Int!, $col_id:String!, $col_val:String!) {items_by_column_values(board_id:$board_id, column_id:$col_id, column_value:$col_val){name id}}",
    {"board_id": ed_mgmt_board_id, "col_id": "text3", "col_val": "Neel Pai"},
)
status_list = status_ingest["data"]["items_by_column_values"]

# status_ingest = query_helper(
#     "query($board_id:Int!, $item_id:Int!) {boards(ids:[$board_id]){items(ids:[$item_id]) {name id}}}",
#     {
#         "board_id": status_board_id,
#         "item_id": 3372035514,
#     },
# )
# status_list = status_ingest["data"]["boards"][0]["items"]

for groups in status_list:
    if groups["name"] != "USACS Management Group, LTD.":
        new_mtb_ingest = query_helper(
            "mutation($board_name:String!, $folder_id:Int!){create_board(folder_id:$folder_id,board_name: $board_name,board_kind:public,template_id:3486332223){id}}",
            {
                "folder_id": sandbox_mtb_boards_folder_id,
                "board_name": groups["name"],
            },
        )
        new_mtb_board_id = int(new_mtb_ingest["data"]["create_board"]["id"])
        new_mtb_webhookup = query_helper(
            "mutation($board_id:Int!,$item_name:String!,$col_val:JSON!){create_item(board_id: $board_id, item_name:$item_name, column_values:$col_val){id}}",
            {
                "board_id": sandbox_mtb_board_id,
                "item_name": groups["name"],
                "col_val": json.dumps({"text": str(new_mtb_board_id)}),
            },
        )
        new_mtb_col_ingest = query_helper(
            "query($board_id:Int!) {boards(ids:[$board_id]){items(limit:1) {column_values{title id type}}}}",
            {"board_id": new_mtb_board_id},
        )
        time.sleep(15)
        new_mtb_col_list = new_mtb_col_ingest["data"]["boards"][0]["items"][0]
        new_mtb_ingest = query_helper(
            "query($board_id:Int!){boards(ids:[$board_id]){items{name id}}}",
            {"board_id": new_mtb_board_id},
        )
        new_mtb_list = new_mtb_ingest["data"]["boards"][0]["items"]
        mtb_ingest = query_helper(
            "query($board_id:Int!, $col_id:String!, $col_val:String!) {items_by_column_values (board_id: $board_id, column_id: $col_id , column_value: $col_val){name column_values{title type text value} updates{body created_at creator{name}}}}",
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
        if mtb_measure_list:
            for new_measure in new_mtb_list:
                for measure in mtb_measure_list:
                    if measure["name"].find(new_measure["name"].split(" - ")[0]) != -1:
                        for new_mtb_column in new_mtb_col_list["column_values"]:
                            if new_mtb_column["title"] != "Subitems":
                                for mtb_column in measure["column_values"]:
                                    if (
                                        mtb_column["title"] == new_mtb_column["title"]
                                        and new_mtb_column["id"] != "mirror"
                                        and mtb_column["title"] != "Subitems"
                                        and mtb_column["title"] != "MTB Helper"
                                    ):
                                        col_id = new_mtb_column["id"]
                                        col_type = mtb_column["type"]
                                        if col_type == "board-relation":
                                            col_val = int(groups["id"])
                                            col_txt = groups["name"]
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
                        if measure["updates"]:
                            for update in measure["updates"]:
                                date = update["created_at"].split("T")[0]
                                user = update["creator"]["name"]
                                body = update["body"]
                                new_body = f"{user} said {body} at {date}"
                                query_helper(
                                    "mutation($item_id:Int!,$body:String!){create_update(item_id: $item_id, body: $body){id}}",
                                    {
                                        "item_id": int(new_measure["id"]),
                                        "body": new_body,
                                    },
                                )

        else:
            for new_measure in new_mtb_list:
                for new_mtb_column in new_mtb_col_list["column_values"]:
                    if new_mtb_column["title"] != "Subitems":
                        col_id = new_mtb_column["id"]
                        col_type = new_mtb_column["type"]
                        if col_type == "board-relation":
                            col_val = int(groups["id"])
                            col_txt = groups["name"]
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


end = time.time()
print(end - start)
