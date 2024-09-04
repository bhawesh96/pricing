import requests
from selenium import webdriver
import json
import re
import datetime
import os
import utils


def _print(name, qty, mrp, sp):
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


def start_driver(headless=True):
    if not headless:
        return webdriver.Chrome()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    return webdriver.Chrome(options=chrome_options)


driver = start_driver()

driver.get('https://www.dunzo.com')
# todo: get csrf token from page source and pass it in header. (Almost got me killed)
csrfToken = re.search("<script>window\.csrfToken.*?</script>", driver.page_source).group()
csrfToken = csrfToken.split('"')[1]

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'x-csrf-token': str(csrfToken)
}

s = requests.session()
for cookie in driver.get_cookies():
    s.cookies.set(cookie['name'], cookie['value'])

# json_data = {"location": {"lat": 13.0826802, "lng": 80.2707184}, "userId": "2c36b74b-f212-4eb2-800c-f660c5864ec7",
#              "is_guest_user": True}

# r = s.post('https://www.dunzo.com/api/v0/order/fruit-and-vegetable-stores?page=1&size=200',
#            json=json_data,
#            headers=header)
# products = json.loads(r.text)

# url = 'https://www.dunzo.com/api/v1/order/store/kovai-pazhamudir-nilayam-6th-avenue-anna-nagar?subTag=fnv'
# dadf8010-1800-4142-8769-11c5758709fc this is the dzid from above URL's response

# url = 'https://www.dunzo.com/api/v1/order/store/jk-cheese-n-more-egmore-12418744?subTag=fnv'
# 34a2edea-45a0-4daa-9424-f50d9517067c this is the dzid from above URL's response

stores = {
    'dadf8010-1800-4142-8769-11c5758709fc': {
        'name': 'kovai',
        'sections': ['FRUITS', 'VEGETABLES']
    },
    '34a2edea-45a0-4daa-9424-f50d9517067c': {
        'name': 'jkcheese',
        'sections': ['FRUITS', 'VEGETABLES', 'HERBS AND SEASONING']
    },
}

url = 'https://www.dunzo.com/v1/web/sku/listing/{}/tab/FRESH {}?subTag=FnV&page={}&size=200'
file_name_counter = 1

name = list()
mrp = list()
sp = list()
qty = list()

for store in stores:
    name = list()
    mrp = list()
    sp = list()
    qty = list()
    for section in stores[store]['sections']:
        _url = url.format(store, section, 1)
        r = s.post(_url, headers=header)
        head_json_data = json.loads(r.text)
        first_time = True
        pageNo = 1
        while first_time or head_json_data['data']['skuList']['nextPageAvailable']:
            if first_time:
                first_time = False
            print('Fetching for {} - page no: {}'.format(section, pageNo))
            _url = url.format(store, section, pageNo)
            r = s.post(_url, headers=header)
            head_json_data = json.loads(r.text)
            subcats = head_json_data['data']['skuList']['subCategories']
            for subcat in subcats:
                products = subcat['products']
                for product in products:
                    for var in product['customizationData']['variantTypes']:
                        for variant in var['variants']:
                            name.append(product['title'])
                            qty.append(variant['title'])
                            mrp.append(variant['price'])
                            sp.append(variant['price'])
            file_name = 'dunzo_{}_{}_{}.json'.format(stores[store]['name'], datetime.datetime.today().date().isoformat(), file_name_counter)
            with open(os.path.join('jsons', file_name), 'w') as f:
                json.dump(head_json_data, f)
            pageNo += 1
            file_name_counter += 1
    print('----- Store: {} -----'.format(stores[store]['name']))
    _print(name, qty, mrp, sp)
    utils.write_lists_to_excel('Dunzo - {}'.format(stores[store]['name']), name, qty, mrp, sp)

driver.close()