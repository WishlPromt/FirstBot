import json

with open('items.json', 'r', encoding='utf-8') as file:
    items = json.load(file)

with open('credits_base.json', 'r', encoding='utf-8') as file:
    credits = json.load(file)

def buy(item, buyer):
    if item in items:
        if items[item][0] <= credits[buyer]['credits']:
            pass
