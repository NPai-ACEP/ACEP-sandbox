import json
import os
import sys

cur_dir = os.path.dirname(__file__)
helper_dir = os.path.join(cur_dir, "..", "tools")
sys.path.append(helper_dir)
from config import group_accounts_board_id, measure_tracking_board_id, mtb_board_id
from tools import query_helper, write_data

group_list = query_helper(
    "query($board_id:Int!, $column_id:String!, $group_name: String!) {boards(ids:[$board_id]){groups(ids:[$group_name]){items{id column_values(ids:[$column_id]){text}}}}}",
    {
        "board_id": group_accounts_board_id,
        "column_id": "text9",
        "group_name": "1660067352_group_names",
    },
)["data"]["boards"][0]["groups"][0]["items"]

template_measure_data = query_helper(
    "query($board_id:Int!) {boards(ids:[$board_id]){items{name}}}",
    {"board_id": mtb_board_id},
)["data"]["boards"][0]["items"]


for group_accounts in group_list:
    group_name = group_accounts["column_values"][0]["text"]
    measure_data = query_helper(
        "query($board_id:Int!, $column_id:String!, $column_val:String!) {items_by_column_values (board_id: $board_id, column_id: $column_id, column_value: $column_val){name id}}",
        {
            "board_id": measure_tracking_board_id,
            "column_id": "dup__of_group_name4",
            "column_val": group_name,
        },
    )["data"]["items_by_column_values"]

    for template_measure in template_measure_data:
        for measure in measure_data:
            if (
                template_measure["name"].split(" - ")[0]
                == measure["name"].split(" - ")[0]
            ):
                col_id = ""
                query_helper(
                    "mutation ($board_id:Int!,$item_id:Int!, $col_val: JSON!) {change_multiple_column_values(item_id: $item_id, board_id: $board_id, column_values: $col_val){id}}",
                    {
                        "board_id": measure_tracking_board_id,
                        "item_id": measure["id"],
                        "col_val": json.dumps({"name": template_measure["name"]}),
                    },
                    True,
                )
