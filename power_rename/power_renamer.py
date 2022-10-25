import json
import os
import sys
cur_dir = os.path.dirname(__file__)
helper_dir = os.path.join(cur_dir, '..', 'tools')
sys.path.append(helper_dir)
from config import ed_data_feed_board_id
from tools import query_helper, write_data

ed_data_feed_ingest = query_helper('query($board_id:Int!){boards(ids:[$board_id]){items{name id}}}',{'board_id':ed_data_feed_board_id})
ed_data_feed_data = ed_data_feed_ingest['data']['boards'][0]['items']

ed_site_list = []

for ed_site in ed_data_feed_data:
    new_ed_site_name = ed_site['name'].title()
    ed_site_list.append([new_ed_site_name, ed_site['name'], ed_site['id']])    
write_data(ed_site_list=ed_site_list)
