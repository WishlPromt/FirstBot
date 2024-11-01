import json

with open('items.json', 'r', encoding='utf-8') as file:
    items = json.load(file)

with open('credits_base.json', 'r', encoding='utf-8') as file:
    credits = json.load(file)

def buy(item, buyer):
    if item in items:
        if items[item][0] <= credits[buyer]['credits']:
            credits[buyer]['inventory'][item] = [items[item][1], int(items[item][0] / 2)]


def get_items(page):
    items_on_page = []
    for item in items[page*3:(page+1*3)]:
        items_on_page.append(item)

    return items_on_page
