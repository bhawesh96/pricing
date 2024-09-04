import requests
import json
import os
import datetime
import utils

name = list()
mrp = list()
sp = list()
qty = list()

resp = requests.get('https://madrasmandi.in/_next/data/7R29netEecJQ5Bo1G2gDB/products.json')
all = json.loads(resp.text)

file_name = 'madras_mandi_{}.json'.format(datetime.datetime.today().date().isoformat())
with open(os.path.join('jsons', file_name), 'w') as f:
    json.dump(all, f)

for product in all['pageProps']['products']:
    name.append(product['title'])
    _qty = product['rate'].split('/')[1].strip()
    if _qty == 'No':
        _qty = '1 pc'
    qty.append(_qty)
    mrp.append(product['rate'].split('/')[0].strip())
    sp.append(product['rate'].split('/')[0].strip())

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

utils.write_lists_to_excel('Madras Mandi', name, qty, mrp, sp)
