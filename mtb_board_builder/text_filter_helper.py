import json
import os
import sys

cur_dir = os.path.dirname(__file__)
helper_dir = os.path.join(cur_dir, "..", "tools")
sys.path.append(helper_dir)
from config import measure_tracking_board_id
from tools import query_helper
import time

start = time.time()

measure_tracking_board_ingest = query_helper(
    "query($board_id:Int!,$col_id:String!){boards(ids:[$board_id]){items{ id column_values(ids:[$col_id]){text}}}}",
    {"board_id": measure_tracking_board_id, "col_id": "connect_boards7"},
)
measure_tracking_board_list = measure_tracking_board_ingest["data"]["boards"][0][
    "items"
]
for item in measure_tracking_board_list:
    item_id = int(item["id"])
    group_name = item["column_values"][0]["text"]
    col_id = "text4"
    query_helper(
        "mutation($board_id:Int!,$item_id:Int!,$col_val:JSON!){change_multiple_column_values(item_id: $item_id, board_id: $board_id, column_values: $col_val){id}}",
        {
            "board_id": measure_tracking_board_id,
            "item_id": item_id,
            "col_val": json.dumps({col_id: group_name}),
        },
    )

end = time.time()
print(end - start)
