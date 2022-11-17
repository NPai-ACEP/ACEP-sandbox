import json
import os
import sys

cur_dir = os.path.dirname(__file__)
helper_dir = os.path.join(cur_dir, "..", "tools")
sys.path.append(helper_dir)
from config import _2022_mips_messaging_board_id, emdi_tiers_spreadsheet
from tools import query_helper, write_data

_2022_mips_messaging_ingest = query_helper(
    "query ($board_id: Int!) {boards(ids: [$board_id]) {items {name id}}}",
    {"board_id": _2022_mips_messaging_board_id},
)
_2022_mips_messaging_dict = _2022_mips_messaging_ingest["data"]["boards"][0]["items"]
emdi_tiers = emdi_tiers_spreadsheet.active

emdi_tiers_db = []
emdi_tiers_db_value = []
for row in range(1, emdi_tiers.max_row):
    for col in emdi_tiers.iter_cols(1, emdi_tiers.max_column):
        emdi_tiers_db_value.append(col[row].value)
    emdi_tiers_db.append(emdi_tiers_db_value)
    emdi_tiers_db_value = []

for emdi_tiers_db_row in emdi_tiers_db:
    for _2022_mips_messaging_list in _2022_mips_messaging_dict:
        if (
            emdi_tiers_db_row[0].casefold()
            == _2022_mips_messaging_list["name"].casefold()
        ):
            messaging = emdi_tiers_db_row[1]
            if isinstance(messaging, int):
                query_helper(
                    "mutation ($board_id:Int!,$item_id:Int!,$col_val: JSON!) { change_multiple_column_values(item_id: $item_id, board_id: $board_id, column_values: $col_val){id}}",
                    {
                        "board_id": _2022_mips_messaging_board_id,
                        "item_id": int(_2022_mips_messaging_list["id"]),
                        "col_val": json.dumps({"numbers": messaging}),
                    },
                )
            break

write_data(
    _2022_mips_messaging_ingest=_2022_mips_messaging_ingest,
    _2022_mips_messaging_dict=_2022_mips_messaging_dict,
    emdi_tiers_db=emdi_tiers_db,
)
