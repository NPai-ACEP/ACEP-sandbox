import json
import os
import sys

cur_dir = os.path.dirname(__file__)
helper_dir = os.path.join(cur_dir, "..", "tools")
sys.path.append(helper_dir)
from config import (
    status_board_id,
    mips_scores_board_id,
)
from tools import query_helper


status_board_data = query_helper(
    "query($board_id:Int!, $col_id:String!) {boards(ids:[$board_id]){items {id column_values(ids:[$col_id]){text} }}}",
    {"board_id": status_board_id, "col_id": "lookup7"},
)["data"]["boards"][0]["items"]


mips_score_data = query_helper(
    "query($board_id:Int!,$group_id:String!) {boards(ids:[$board_id]){groups(ids:[$group_id]){id items{name id}}}}",
    {"board_id": mips_scores_board_id, "group_id": "1681932491_mips_tracker_168193"},
    True,
)["data"]["boards"][0]["groups"][0]["items"]

col_id0 = "board_relation7"
col_id1 = "connect_boards"
col_id2 = "connect_boards"


for group_accounts in status_board_data:
    for acep_id_account in acep_id_info_data:
        if str(acep_id_account["column_values"][0]["value"]) == str(
            group_accounts["column_values"][0]["value"]
        ):
            query_helper(
                "mutation ($board_id:Int!,$item_id:Int!,$col_val: JSON!) { change_multiple_column_values(item_id: $item_id, board_id: $board_id, column_values: $col_val){id}}",
                {
                    "board_id": acep_id_info_board_id,
                    "item_id": int(acep_id_account["id"]),
                    "col_val": json.dumps(
                        {col_id0: {"item_ids": [int(group_accounts["id"])]}}
                    ),
                },
                True,
            )
        # for ed_site in ed_mgmt_data:
        #     if str(acep_id_account["column_values"][1]["value"]) == str(
        #         ed_site["column_values"][0]["value"]
        #     ):
        #         query_helper(
        #             "mutation ($board_id:Int!,$item_id:Int!,$col_val: JSON!) { change_multiple_column_values(item_id: $item_id, board_id: $board_id, column_values: $col_val){id}}",
        #             {
        #                 "board_id": acep_id_info_board_id,
        #                 "item_id": int(acep_id_account["id"]),
        #                 "col_val": json.dumps(
        #                     {col_id1: {"item_ids": [int(ed_site["id"])]}}
        #                 ),
        #             },
        #             True,
        #         )
    for group_mips_tracker in mips_tracker_data:
        if (
            group_mips_tracker["column_values"][0]["value"]
            == group_accounts["column_values"][1]["value"]
        ):
            query_helper(
                "mutation ($board_id:Int!,$item_id:Int!,$col_val: JSON!) { change_multiple_column_values(item_id: $item_id, board_id: $board_id, column_values: $col_val){id}}",
                {
                    "board_id": mips_tracker_board_id,
                    "item_id": int(group_mips_tracker["id"]),
                    "col_val": json.dumps(
                        {col_id2: {"item_ids": [int(group_accounts["id"])]}}
                    ),
                },
                True,
            )
# ed_mgmt_ingest = query_helper(
#     "query($board_id:Int!,$col_id:String!){boards(ids:[$board_id]){items{id column_values(ids:[$col_id]){value}}}}",
#     {
#         "board_id": ed_mgmt_board_id,
#         "col_id": "link_to_group_accounts",
#     },
# )
# ed_mgmt_list = ed_mgmt_ingest["data"]["boards"][0]["items"]

# ed_data_ingest = query_helper(
#     "query($board_id:Int!,$col_id:String!){boards(ids:[$board_id]){items{id column_values(ids:[$col_id]){value}}}}",
#     {
#         "board_id": ed_data_feed_board_id,
#         "col_id": "board_relation",
#     },
# )
# ed_data_list = ed_data_ingest["data"]["boards"][0]["items"]

# for ed_group_data in ed_mgmt_list:
#     for ed_data_data in ed_data_list:
#         linked_group_id = int(
#             json.loads(ed_group_data["column_values"][0]["value"])["linkedPulseIds"][0][
#                 "linkedPulseId"
#             ]
#         )
#         linked_ed_id = int(
#             json.loads(ed_data_data["column_values"][0]["value"])["linkedPulseIds"][0][
#                 "linkedPulseId"
#             ]
#         )

#         if linked_ed_id == int(ed_group_data["id"]):

#             col_id = "connect_boards92"
#             query_helper(
#                 "mutation ($board_id:Int!,$item_id:Int!,$col_val: JSON!) { change_multiple_column_values(item_id: $item_id, board_id: $board_id, column_values: $col_val){id}}",
#                 {
#                     "board_id": ed_data_feed_board_id,
#                     "item_id": int(ed_data_data["id"]),
#                     "col_val": json.dumps({col_id: {"item_ids": [linked_group_id]}}),
#                 },
#             )
