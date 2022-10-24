import json
import os
import sys
cur_dir = os.path.dirname(__file__)
helper_dir = os.path.join(cur_dir, 'db')
sys.path.append(helper_dir)
from config import (backup_ed_sites_board_id, ed_sites_board_id)
from tools import query_helper
site_ingest = query_helper(
    'query($board_id:Int!) {boards(ids:[$board_id]){items {name id}}}',
    {
        'board_id': ed_sites_board_id
    })
site_data = site_ingest['data']['boards'][0]['items']

backup_site_ingest = query_helper(
    'query($board_id:Int!) {boards(ids:[$board_id]){items {name id}}}',
    {
        'board_id': backup_ed_sites_board_id
    })
backup_site_data = backup_site_ingest['data']['boards'][0]['items']

col_id='connect_boards0'


for site_id in site_data:
    for backup_site_id in backup_site_data:
        if site_id['name'].casefold()==backup_site_id['name'].casefold():
            query_helper(
                'mutation ($board_id:Int!,$item_id:Int!,$site_val: JSON!) { change_multiple_column_values(item_id: $item_id, board_id: $board_id, column_values: $site_val){id}}',
                {
                    'board_id': ed_sites_board_id,
                    'item_id': int(site_id['id']),
                    'site_val': json.dumps({
                        col_id: {'item_ids': [int(backup_site_id['id'])]}
                    })
                })
