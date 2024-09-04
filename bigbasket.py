# !/usr/bin/env python
# coding: utf-8

import requests
from selenium import webdriver
import json
import datetime
import os
import utils

def start_driver(headless=True):
    if not headless:
        return webdriver.Chrome()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    return webdriver.Chrome(options=chrome_options)


header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
}

driver = start_driver()

# 1000045 is the city code for Chennai. Make this get request to set the cookies for Chennai (huh, smarties)
# To get all cities list, make GET to: https://www.bigbasket.com/mapi/v3.5.2/cities/
driver.get('https://www.bigbasket.com/skip_explore/?c=1000045&l=0&s=0&n=/')

s = requests.session()
for cookie in driver.get_cookies():
  s.cookies.set(cookie['name'], cookie['value'])

driver.close()

r = s.get('https://www.bigbasket.com/mapi/v4.1.0/product/list/?page=1&slug=fruits-vegetables&tab_type=%5B%22all%22%5D&type=pc', headers=header)

products = json.loads(r.text)

total_pages = products['response']['tab_info'][0]['product_info']['tot_pages']

name = list()
mrp = list()
sp = list()
qty = list()

all_products = {'data': []}

for i in range(1, total_pages+1):
    print('Fetching for page no.: {}'.format(i))
    r = s.get('https://www.bigbasket.com/mapi/v4.1.0/product/list/?page={}&slug=fruits-vegetables&tab_type=%5B%22all%22%5D&type=pc'.format(i),
              headers=header)

    products_json = json.loads(r.text)
    # file_name = 'bigbasket_{}_{}.json'.format(datetime.datetime.today().date().isoformat(), i)
    # with open(os.path.join('jsons', file_name), 'w') as f:
    #     json.dump(products_json, f)
    products = products_json['response']['tab_info'][0]['product_info']['products']

    all_products['data'].extend(products)

    for product in products:
        name.append(product['p_desc'])
        qty.append(product['w'])
        mrp.append(product['mrp'])
        sp.append(product['sp'])

r.close()
s.close()

file_name = 'bigbasket_ALL_{}.json'.format(datetime.datetime.today().date().isoformat())
with open(os.path.join('jsons', file_name), 'w') as f:
    json.dump(all_products, f)

# df = pd.DataFrame(list(zip(name, qty, mrp, sp)), columns=['Item', 'Quantity', 'MRP', 'Selling Price'])
# excel_file_name = '{}.xlsx'.format(datetime.datetime.today().date().isoformat())
# try:
#     book = openpyxl.load_workbook(excel_file_name)
# except IOError:
#     book = openpyxl.Workbook()
# writer = pd.ExcelWriter(excel_file_name, engine='openpyxl')
# writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
# df.to_excel(writer, sheet_name='BigBasket', index=False)
# writer.save()
# writer.close()

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

utils.write_lists_to_excel('Bigbasket', name, qty, mrp, sp)
