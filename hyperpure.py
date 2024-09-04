

import requests
from selenium import webdriver
import json
import datetime
import os
import time
import utils

url = 'https://api.hyperpure.com/consumer/v2/search?outletId=0&pageNo={}&categoryIds=1&sourcePage=CATEGORY_PAGE&entity_id=&entity_type=&parent_reference_id=d23bcf4f-f2db-4996-bb1b-adad86e6df4b-1689773340493330045&parent_reference_type=&search_source=&source_page=&sub_reference_id=&sub_reference_type=&fetchThroughV2=true&onlyInStock=false'
file_name_counter = 1
name = list()
mrp = list()
sp = list()
qty = list()

all_products = {'data': []}
headers = {
    # 'Authority': 'api.hyperpure.com',
    # 'Path': '/consumer/v2/search?outletId=0&pageNo=1&categoryIds=1&sourcePage=CATEGORY_PAGE&entity_id=&entity_type=&parent_reference_id=f2c398d2-7f08-4c2f-9a36-2bc6eee81376-1689787508421918449&parent_reference_type=&search_source=&source_page=&sub_reference_id=&sub_reference_type=&fetchThroughV2=true&searchDebugFlag=false&onlyInStock=false',
    # 'Scheme': 'https',
    'Headerroute': 'v2',
    'Apiversion': '10.1',
}
r = requests.get(url.format(file_name_counter), headers=headers)
head_json_data = json.loads(r.text)

first_time = True

pageNo = 0
while first_time or head_json_data['response']['HasNextPage']:
    if first_time:
        first_time = False
    print('Fetching page no: {}'.format(pageNo))
    r = requests.get(url.format(file_name_counter), headers=headers)
    head_json_data = json.loads(r.text)
    products = head_json_data['response']['Products']

    all_products['data'].extend(products)

    for product in products:
        name.append(product['Name'])
        if product['unit_of_measure'] is None:
            qty.append('{}'.format(product['quantity']))
        else:
            qty.append('{} {}'.format(product['quantity'], product['unit_of_measure']))
        mrp.append(product['price']['mrp'])
        sp.append(product['price']['offer_price'])

    # file_name = 'swiggy_{}_{}.json'.format(datetime.datetime.today().date().isoformat(), file_name_counter)
    # with open(os.path.join('jsons', file_name), 'w') as f:
    #     json.dump(head_json_data, f)
    pageNo += 1
    file_name_counter += 1

file_name = 'swiggy_ALL_{}.json'.format(datetime.datetime.today().date().isoformat())
with open(os.path.join('jsons', file_name), 'w') as f:
    json.dump(all_products, f)

print("--------ITEM----------")
for n in name:
    print(n)
print("--------QTY----------")
for q in qty:
    print(q)
print("--------MRP----------")
for m in mrp:
    print(m)
print("----------SP-----------")
for s in sp:
    print(s)

utils.write_lists_to_excel('Swiggy', name, qty, mrp, sp)
