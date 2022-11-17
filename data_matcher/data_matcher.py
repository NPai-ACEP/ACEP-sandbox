import json
import os
import sys

cur_dir = os.path.dirname(__file__)
helper_dir = os.path.join(cur_dir, "..", "tools")
sys.path.append(helper_dir)
from config import status_board_id, group_accounts_board_id
from tools import query_helper

col_id = "status"
status_ingest = query_helper(
    "query($board_id:Int!) {boards(ids:[$board_id]){items {name id}}}",
    {"board_id": status_board_id},
)
status_list = status_ingest["data"]["boards"][0]["items"]

group_accounts_ingest = query_helper(
    "query($board_id:Int!) {boards(ids:[$board_id]){items {name id}}}",
    {"board_id": group_accounts_board_id},
)
group_accounts_list = group_accounts_ingest["data"]["boards"][0]["items"]


for group in status_list:
    for group_dupe1 in group_accounts_list:
        if group["name"].casefold() == group_dupe1["name"].casefold():
            col_id = "connect_boards06"
            query_helper(
                "mutation ($board_id:Int!,$item_id:Int!,$site_val: JSON!) { change_multiple_column_values(item_id: $item_id, board_id: $board_id, column_values: $site_val){id}}",
                {
                    "board_id": group_accounts_board_id,
                    "item_id": int(group_dupe1["id"]),
                    "site_val": json.dumps({col_id: {"item_ids": [int(group["id"])]}}),
                },
            )
