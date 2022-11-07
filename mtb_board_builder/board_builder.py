import json
import os
import sys
cur_dir = os.path.dirname(__file__)
helper_dir = os.path.join(cur_dir, '..', 'tools')
sys.path.append(helper_dir)
from config import group_accounts_board_id,sandbox_mtb_boards_folder_id
from tools import query_helper

group_acounts_ingest = query_helper(
    "query($board_id:Int!) {boards(ids:[$board_id]){items {name}}}",
    {"board_id": group_accounts_board_id}
    )
group_accounts_list = group_acounts_ingest['data']['boards'][0]['items']

for group_acounts in group_accounts_list:
    query_helper('mutation($board_name:String!, $folder_id:Int!){create_board(folder_id:$folder_id,board_name: $board_name,board_kind:public){id}}', {'folder_id': sandbox_mtb_boards_folder_id, 'board_name': group_acounts['name']}, True)
