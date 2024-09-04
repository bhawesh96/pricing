import requests
import json
import os
import datetime
import utils

name = list()
mrp = list()
sp = list()
qty = list()

veggies = requests.get('https://www.chennaigrocers.com/collections/fruits-vegetables-1/products.json')
fruits = requests.get('https://www.chennaigrocers.com/collections/fresh-fruits/products.json')

all = json.loads(veggies.text)
all['products'].extend(json.loads(fruits.text)['products'])

file_name = 'chennai_grocers_{}.json'.format(datetime.datetime.today().date().isoformat())
with open(os.path.join('jsons', file_name), 'w') as f:
    json.dump(all, f)

for product in all['products']:
    for variant in product['variants']:
        name.append(product['title'])
        qty.append(str(variant['grams']) + ' g')
        mrp.append(variant['price'])
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

utils.write_lists_to_excel('Chennai Grocers', name, qty, mrp, sp)