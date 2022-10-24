import json
import os
import sys
cur_dir = os.path.dirname(__file__)
helper_dir = os.path.join(cur_dir, 'db')
sys.path.append(helper_dir)
from config import (group_accounts_board_id, backup_ed_sites_board_id, ed_sites_board_id)
from tools import query_helper, write_data

group_ingest = query_helper(
    "query($board_id:Int!) {boards(ids:[$board_id]){items {name id}}}",
    {"board_id": group_accounts_board_id},
)
group_data = group_ingest["data"]["boards"][0]["items"]

backup_group_ingest = query_helper(
    'query($board_id:Int!) {boards(ids:[$board_id]){items {name column_values(ids: "connect_boards") {text}}}}',
    {"board_id": backup_ed_sites_board_id},
)
backup_group_data = backup_group_ingest["data"]["boards"][0]["items"]

sites_ingest = query_helper(
    "query($board_id:Int!) {boards(ids:[$board_id]){items {name id}}}",
    {"board_id": ed_sites_board_id},
)
sites_data = sites_ingest["data"]["boards"][0]

sites_col_id = "link_to_group_accounts"

backup_group_sites = {
    backup_group_vals["name"]: backup_group_vals["column_values"][0]["text"]
    for backup_group_vals in backup_group_data
}

backup_group = list(enumerate(backup_group_sites.keys()))
backup_sites = list(enumerate(backup_group_sites.values()))

all_site_ids = set(
    (site_val["name"].casefold(), site_val["id"]) for site_val in sites_data["items"]
)
groups_ids = {
    name: set(
        int(site_val_id)
        for site_val_name, site_val_id in all_site_ids
        if site_val_name.casefold()
        in set(site_name.casefold() for site_name in sites.split(", "))
    )
    for name, sites in backup_group_sites.items()
}

col_id = "connect_boards44"
connect_new_id = [
    [
        query_helper(
            "mutation ($board_id:Int!,$item_id:Int!,$group_val: JSON!) { change_multiple_column_values(item_id: $item_id, board_id: $board_id, column_values: $group_val){id}}",
            {
                "board_id": group_accounts_board_id,
                "item_id": int(group_id["id"]),
                "group_val": json.dumps(
                    {col_id: {"item_ids": list(groups_ids[group_name])}}
                ),
            },
            0
        )
        for group_name in groups_ids
        if group_id["name"].casefold() in group_name.casefold()
    ]
    for group_id in group_data
]

write_data(
    backup_group_ingest=backup_group_ingest,
    backup_group_data=backup_group_data,
    sites_ingest=sites_ingest,
    sites_data=sites_data,
    group_ingest=group_ingest,
    group_data=group_data,
    backup_group=backup_group,
    backup_sites=backup_sites,
    groups_ids=groups_ids,
)
