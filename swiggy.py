import requests
from selenium import webdriver
import json
import datetime
import os
import time
import utils

def start_driver(headless=True):
    if not headless:
        return webdriver.Chrome()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    return webdriver.Chrome(options=chrome_options)

# 'https://www.swiggy.com/mapi/misc_new/location-features?lat=13.0826802&lng=80.2707184&features=SWIGGY_DASH%2CCITY_INFO'


driver = start_driver()
# driver.set_window_size(20, 100)
driver.get('https://www.swiggy.com/instamart')
but = driver.find_element('xpath', "//*[contains(text(), 'SETUP YOUR LOCATION')]")
but.click()
time.sleep(2)
but = driver.find_element('xpath', "//*[contains(text(), 'Use Current Location')]")
but.click()
time.sleep(2)

header = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': 'Android'
}

s = requests.session()

# set cookies
# f***ed Swiggy on this
for cookie in driver.get_cookies():
    s.cookies.set(cookie['name'], cookie['value'])
s.cookies.set('userLocation', '{%22lat%22:13.0826802%2C%22lng%22:80.2707184%2C%22address%22:%22Chennai%2C%20Tamil%20Nadu%2C%20India%22%2C%22area%22:%22%22%2C%22id%22:%22%22}')

# r = s.get('https://www.swiggy.com/api/instamart/category-listing?categoryName=Fruits%20and%20Vegetables&filterName=&taxonomyType=All%20Listing', headers=header)
# products = json.loads(r.text)

driver.close()

sections = ['5f2c18a68ac42c7d7c3efee5',  # fresh vegetables
            '5f2c18a68ac42c7d7c3efee4',  # fresh fruits
            '5f2c18a68ac42c7d7c3efee9',  # leafy and seasonings
            '5f2c18a68ac42c7d7c3efeea',  # exotic vegetables
            '60d2cbaa8ac42c7f24024829',  # certified organics
            '5f2c18a68ac42c7d7c3efee6',  # fresh cuts
            '610d303f79e93b52b84739a6',  # speciality
            '610bd61a8ac42c7f240251a6'  # hydrophonics
            ]

url = 'https://www.swiggy.com/api/instamart/category-listing/filter?filterId={}&type=All%20Listing&pageNo={}&limit=20'
file_name_counter = 1
name = list()
mrp = list()
sp = list()
qty = list()

all_products = {'data': []}

for section in sections:
    _url = url.format(section, 0)
    r = s.get(_url, headers=header)
    head_json_data = json.loads(r.text)

    first_time = True

    pageNo = 0
    while first_time or head_json_data['data']['hasMore']:
        if first_time:
            first_time = False
        print('Fetching for {} - page no: {}'.format(section, pageNo))
        _url = url.format(section, pageNo)
        r = s.get(_url, headers=header)
        head_json_data = json.loads(r.text)
        products = head_json_data['data']['items']

        all_products['data'].extend(products)

        for product in products:
            for variant in product['variations']:
                name.append(variant['display_name'])
                if variant['unit_of_measure'] is None:
                    qty.append('{}'.format(variant['quantity']))
                else:
                    qty.append('{} {}'.format(variant['quantity'], variant['unit_of_measure']))
                mrp.append(variant['price']['mrp'])
                sp.append(variant['price']['offer_price'])

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
