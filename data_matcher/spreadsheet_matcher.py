import json
import os
import sys
cur_dir = os.path.dirname(__file__)
helper_dir = os.path.join(cur_dir, '..', 'tools')
sys.path.append(helper_dir)
from config import status_board_id,reporting_plan_2022_spreadsheet
from tools import query_helper,write_data

status_ingest = query_helper('query ($board_id: Int!) {boards(ids: [$board_id]) {items {name id}}}', {'board_id': status_board_id})
status_dict = status_ingest['data']['boards'][0]['items']
reporting_plan_2022 = reporting_plan_2022_spreadsheet.active
mips_db = []
mips_db_value = []
for row in range(1, reporting_plan_2022.max_row):
    for col in reporting_plan_2022.iter_cols(1, reporting_plan_2022.max_column):
        mips_db_value.append(col[row].value)
    mips_db.append(mips_db_value)
    mips_db_value = []

for mips_db_row in mips_db:
    for status_list in status_dict:
        if mips_db_row[0].casefold() == status_list['name'].casefold():
            mips_status = mips_db_row[4]
            col_id = "status"
            query_helper('mutation ($board_id:Int!,$item_id:Int!,$col_val: JSON!) { change_multiple_column_values(item_id: $item_id, board_id: $board_id, column_values: $col_val){id}}', {
                "board_id": status_board_id,
                "item_id": int(status_list['id']),
                "col_val": json.dumps(
                    {col_id: {"label": mips_status}}
                ),
            })
            print(mips_db_row[0])
            break

write_data(status_ingest=status_ingest,
           status_dict=status_dict,
           mips_db=mips_db)
