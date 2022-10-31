import os.path

import config
import requests

api_url = "https://api.monday.com/v2"
headers = {"Authorization": config.api_key_monday}


def write_data(**all_data):
    for data_name, data_item in all_data.items():
        file_name = os.path.join(os.getcwd(), 'data')
        os.makedirs(file_name, exist_ok=True)
        with open(f'{file_name}/{data_name}.txt', 'w', encoding='utf8') as f:
            print(data_item, file=f)


def query_helper(query, variables, silent=1):
    data = {'query': query, 'variables': variables}
    r = requests.post(url=api_url, json=data, headers=headers)
    if silent is False:
        print(data)
        print(r.json())
    return r.json()


def titlecase_formater(item_list):
    new_item_list = []
    for item in item_list:
        new_item_name = item['name'].title()
        new_item_list.append([new_item_name, int(item['id'])])
    return new_item_list
