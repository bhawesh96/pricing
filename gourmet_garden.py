import requests
import json
import os
import datetime
import utils

name = list()
mrp = list()
sp = list()
qty = list()

veggies = requests.get('https://chennai.gourmetgarden.in/collections/fresh-vegetables/products.json')
fruits = requests.get('https://chennai.gourmetgarden.in/collections/fresh-fruits/products.json')
greens = requests.get('https://chennai.gourmetgarden.in/collections/leafy-greens/products.json')

all = json.loads(veggies.text)
all['products'].extend(json.loads(fruits.text)['products'])
all['products'].extend(json.loads(greens.text)['products'])

file_name = 'gourmet_garden_{}.json'.format(datetime.datetime.today().date().isoformat())
with open(os.path.join('jsons', file_name), 'w') as f:
    json.dump(all, f)

for product in all['products']:
    for variant in product['variants']:
        name.append(product['title'])
        qty.append(variant['title'])
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

utils.write_lists_to_excel('Gourmet Garden', name, qty, mrp, sp)
