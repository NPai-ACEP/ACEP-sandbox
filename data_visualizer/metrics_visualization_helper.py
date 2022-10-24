mport json
import os
import sys
cur_dir = os.path.dirname(__file__)
helper_dir = os.path.join(cur_dir, 'db')
sys.path.append(helper_dir)
from config import cedr_monthly_implementation_metrics_board_id
from tools import query_helper

cedr_monthly_implementation_metrics_board_id