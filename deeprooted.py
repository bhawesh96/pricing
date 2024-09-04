import requests
import json
import os
import datetime
import utils

name = list()
mrp = list()
sp = list()
qty = list()
ids = list()

veggies = requests.get('https://deeprooted.co/_next/data/PzFkUouklhyL42IpBmKuZ/bangalore.json?city=bangalore')

all = json.loads(veggies.text)

file_name = 'deeprooted_{}.json'.format(datetime.datetime.today().date().isoformat())
with open(os.path.join('jsons', file_name), 'w') as f:
    json.dump(all, f)

for category in all['pageProps']['catalog']['categoriesList']:
    for family in category['familiesList']:
        for product in family['productsList']:
            for variant in product['variantsList']:
                if variant['id'] not in ids:
                    ids.append(variant['id'])
                    name.append(product['name'])
                    qty.append(variant['weightdescription'])
                    mrp.append(variant['mrp'])
                    sp.append(variant['price'])

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

utils.write_lists_to_excel('Deeprooted', name, qty, mrp, sp)