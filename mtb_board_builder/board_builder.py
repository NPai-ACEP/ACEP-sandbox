import json
import os
import sys
import time
cur_dir = os.path.dirname(__file__)
helper_dir = os.path.join(cur_dir, '..', 'tools')
sys.path.append(helper_dir)
from config import group_accounts_board_id,sandbox_mtb_boards_folder_id, measure_tracking_board_id
from tools import query_helper

start = time.time()

group_acounts_ingest = query_helper(
    "query($board_id:Int!) {boards(ids:[$board_id]){items {name id}}}",
    {"board_id": group_accounts_board_id}
    )
group_accounts_list = group_acounts_ingest['data']['boards'][0]['items']

for group_acounts in group_accounts_list:
    # new_mtb_ingest = query_helper('mutation($board_name:String!, $folder_id:Int!){create_board(folder_id:$folder_id,board_name: $board_name,board_kind:public,template_id:3486332223){id}}', {'folder_id': sandbox_mtb_boards_folder_id, 'board_name': group_acounts['name']})
    # new_mtb_board_id = int(new_mtb_injest['data']['create_board']['id'])
    # new_mtb_col_ingest = query_helper(
    # "query($board_id:Int!) {boards(ids:[$board_id]){items(limit:1) {column_values{title id}}}}",
    # {"board_id": new_mtb_board_id}
    # )
    mtb_ingest = query_helper("query($board_id:Int!, $col_id:String!, $col_val:String!) {items_by_column_values (board_id: $board_id, column_id: $col_id , column_value: $col_val){name id column_values{title id text value} updates{id}}}",{'board_id':measure_tracking_board_id, 'col_id': 'text4', 'col_val':group_acounts['name']})
    mtb_measure_list = mtb_ingest["data"]["items_by_column_values"]
    for measure in mtb_measure_list:
        temp = measure["name"].split(' - ')[0]
    breakpoint()
    
end = time.time()
print(end - start)  
