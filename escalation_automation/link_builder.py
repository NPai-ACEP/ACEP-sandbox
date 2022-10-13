import json
import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..','tools'))
from tools import query_helper

board_id = 3212680769

items_ingest=query_helper('query ($board_id:Int!) {boards(ids:[$board_id]){items{id name}}}',{'board_id': board_id})
items_val=items_ingest['data']['boards']
board_id=str(board_id)
items_url=sum(([
    [
        int(items_ids['id']),
        items_ids['name'],
        f'https://acep-space.monday.com/boards/{board_id}/pulses/{items_ids["id"]}'
    ]
    for items_ids in items['items']] for items in items_val),[])

board_id = int(board_id)

col_ingest = query_helper('query ($board_id:Int!) {boards(ids:[$board_id]){items(limit:1){column_values{id title type}}}}',{'board_id': board_id})
col_data=col_ingest['data']['boards'][0]['items'][0]['column_values']
col_id = [col_val['id'] for col_val in col_data if col_val['type'] == 'link' and col_val['title'] == 'Email Link'][0]


for item_id,item_name,item_url in items_url:
    query_helper('mutation ($board_id:Int!,$item_id:Int!,$link_val: JSON!) { change_multiple_column_values(item_id: $item_id, board_id: $board_id, column_values: $link_val){id}}',{'board_id':board_id,'item_id':item_id,'link_val':json.dumps({col_id: {'url': item_url, 'text': item_name}})})
