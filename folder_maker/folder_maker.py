import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..','tools'))
from tools import query_helper

group_board_id = 3000198537

group_ingest = query_helper('query($board_id:Int!) {boards(ids:[$board_id]){items {name column_values(ids:["text8"]){text}}}}',{'board_id': group_board_id})
group_data=group_ingest["data"]['boards'][0]["items"]

for group_vals in group_data:
    acep_id = group_vals["column_values"][0]["text"]
    group_name = group_vals["name"]
    directory = f'{acep_id} - {group_name}'
    path = os.path.join(os.getcwd, directory)
    os.makedirs(path)
    





