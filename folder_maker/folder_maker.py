import os
import sys
cur_dir=os.path.dirname(__file__)
helper_dir=os.path.join(cur_dir, '..','tools')
sys.path.append(helper_dir)
import config
from tools import query_helper


group_ingest = query_helper('query($board_id:Int!) {boards(ids:[$board_id]){items {name column_values(ids:["text8"]){text}}}}',{'board_id': config.group_accounts_board_id})
group_data=group_ingest["data"]['boards'][0]["items"]

for group_vals in group_data:
    acep_id = group_vals["column_values"][0]["text"]
    group_name = group_vals["name"]
    directory = f'{acep_id} - {group_name}'
    path = os.path.join(cur_dir, directory)
    os.makedirs(path)
    





