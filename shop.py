import json
from social_credits import check_user, add_credits, save_base
from time import sleep

#DATABASES
with open('items.json', 'r', encoding='utf-8') as file:
    items = json.load(file)

with open('credits_base.json', 'r', encoding='utf-8') as file:
    credits = json.load(file)


def save_inventory():
    file = open('credits_base.json', 'w', encoding='utf-8')
    json.dump(credits, file, indent=4, ensure_ascii=False)
    file.close()


#Variables
max_pages = 2


def buy(item, buyer):

    check_user(buyer)

    price = items[item][0]
    inventory = credits[buyer['id']]['inventory']

    username = credits[buyer["id"]]["username"]

    if item not in inventory and item not in ['Пак карточек']:
        if price <= credits[buyer['id']]['credits']:

            inventory.append(item)
            credits[buyer['id']]['inventory'] = inventory
            credits[buyer['id']]['credits'] = credits[buyer['id']]['credits'] - price

            save_inventory()

            return 'buy'

        else:
            return f'{username}, у вас нет денег\n Используйте /balance, чтобы посмотреть баланс'

    elif item not in inventory and item in ['Пак карточек']:
        if price <= credits[buyer['id']]['credits']:

            inventory.append(item)
            credits[buyer['id']]['cards_packs']['item'] = 1
            credits[buyer['id']]['inventory'] = inventory
            credits[buyer['id']]['credits'] = credits[buyer['id']]['credits'] - price

            save_inventory()

            return f'{username}, вы купили {item}.\n Его можно будет открыть из инвенторя'

        else:
            return f'{username}, у вас нет денег\n Используйте /balance, чтобы посмотреть баланс'

    elif item in inventory and item in ['Пак карточек']:
        if price <= credits[buyer['id']]['credits']:

            credits[buyer['id']]['cards_packs'] += 1

            return f'{username}, вы купили {item}.\n Теперь их у вас {inventory['cards_packs'][item]}\n Их можно будет открыть из инвенторя'

        else:
            return f'{username}, у вас нет денег\n Используйте /balance, чтобы посмотреть баланс'

    return f'{username}, предмет уже есть в вашем инвенторе'


def next_page(cur_page):
    if cur_page < max_pages:
        return cur_page + 1
    else:
        return cur_page


def back_page(cur_page):
    if cur_page > 1:
        return cur_page - 1
    else:
        return cur_page


def get_items(page):
    items_on_page = {}
    for item in items:
        if items[item][2] == page:
            items_on_page[item] = (items[item])

    return items_on_page
