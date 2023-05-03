import json
import os
import sys
import datetime


cur_dir = os.path.dirname(__file__)
helper_dir = os.path.join(cur_dir, "..", "tools")
sys.path.append(helper_dir)
from config import mips_tracker_board_id, emdi_data_acquisition_spreadsheet
from tools import query_helper

mips_tracker_dict = query_helper(
    "query ($board_id: Int!,$col_id:String!) {boards(ids: [$board_id]) {items {name id column_values(ids:[$col_id]){value}}}}",
    {"board_id": mips_tracker_board_id, "col_id": "max_enctr_date"},
)["data"]["boards"][0]["items"]
emdi_date = emdi_data_acquisition_spreadsheet.active

emdi_date_db = []
emdi_date_db_value = []
for row in range(1, emdi_date.max_row):
    for col in emdi_date.iter_cols(1, 2):
        emdi_date_db_value.append(col[row].value)
    emdi_date_db.append(emdi_date_db_value)
    emdi_date_db_value = []

for emdi_date_db_row in emdi_date_db:
    for mips_tracker_list in mips_tracker_dict:
        if str(emdi_date_db_row[0]).casefold() == mips_tracker_list["name"].casefold():
            last_acquisition_date = json.loads(
                mips_tracker_list["column_values"][0]["value"]
            )["date"]
            if last_acquisition_date != "2022-12-31":
                new_acquisition_date = emdi_date_db_row[1].strftime("%Y-%m-%d")
                col_id = "max_enctr_date"
                query_helper(
                    "mutation ($board_id:Int!,$item_id:Int!,$col_val: JSON!) { change_multiple_column_values(item_id: $item_id, board_id: $board_id, column_values: $col_val){id}}",
                    {
                        "board_id": mips_tracker_board_id,
                        "item_id": int(mips_tracker_list["id"]),
                        "col_val": json.dumps({col_id: {"date": new_acquisition_date}}),
                    },
                    True,
                )
                # delivery_date = "2023-03-04"
                # col_id = "date"
                # query_helper(
                #     "mutation ($board_id:Int!,$item_id:Int!,$col_val: JSON!) { change_multiple_column_values(item_id: $item_id, board_id: $board_id, column_values: $col_val){id}}",
                #     {
                #         "board_id": mips_tracker_board_id,
                #         "item_id": int(mips_tracker_list["id"]),
                #         "col_val": json.dumps({col_id: {"date": delivery_date}}),
                #     },
                #     True,
                # )
