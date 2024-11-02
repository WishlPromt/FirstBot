import json
from social_credits import check_user, add_credits, save_base
from time import sleep

with open('items.json', 'r', encoding='utf-8') as file:
    items = json.load(file)

with open('credits_base.json', 'r', encoding='utf-8') as file:
    credits = json.load(file)

def save_inventory():
    file = open('credits_base.json', 'w', encoding='utf-8')
    json.dump(credits, file, indent=4, ensure_ascii=False)
    file.close()


def buy(item, buyer):

    check_user(buyer)

    price = items[item][0]
    inventory = credits[buyer['id']]['inventory']

    if item not in inventory:
        if price <= credits[buyer['id']]['credits']:

            inventory.append(item)
            credits[buyer['id']]['inventory'] = inventory
            credits[buyer['id']]['credits'] = credits[buyer['id']]['credits'] - price

            save_inventory()

            return True

    return False


def get_items(page):
    items_on_page = {}
    for item in items:
        if items[item][2] == page:
            items_on_page[item] = (items[item])

    return items_on_page
