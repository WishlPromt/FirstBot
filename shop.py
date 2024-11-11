import json
from social_credits import check_user, save_base


#DATABASES
with open('items.json', 'r', encoding='utf-8') as file:
    items = json.load(file)


def load_base(chat_id):

    with open('credits_base.json', 'r', encoding='utf-8') as file:
        credits = json.load(file)
        return credits[chat_id]


#Variables
max_pages = 3


def buy(item, buyer):

    check_user(buyer)

    base = load_base(buyer['chat_id'])
    print(base)

    inventory = base[buyer['id']]['inventory']
    username = base[buyer['id']]['username']


    price = items[item][0]


    if item not in inventory and item not in ['Пак карточек', 'Коробка карточек']:
        if price <= base[buyer['id']]['credits']:

            inventory.append(item)
            base[buyer['id']]['inventory'] = inventory
            base[buyer['id']]['credits'] = base[buyer['id']]['credits'] - price

            print(base)
            save_base(base, buyer['chat_id'])

            return f'<b>{username}</b>, вы купили <b>{item}</b>!\n{items[item][1]}'

        else:
            return f'<b>{username}</b>, у вас нет денег\n Используйте /balance, чтобы посмотреть баланс'

    elif item not in inventory and item in ['Пак карточек', 'Коробка карточек']:
        if price <= base[buyer['id']]['credits']:

            inventory.append(item)
            base[buyer['id']]['cards_packs'][item] = 1
            base[buyer['id']]['inventory'] = inventory
            base[buyer['id']]['credits'] = base[buyer['id']]['credits'] - price

            save_base(base, buyer['chat_id'])

            return f'<b>{username}</b>, вы купили <b>{item}</b>.\n{items[item][1]}'

        else:
            return f'<b>{username}</b>, у вас нет денег\n'

    elif item in inventory and item in ['Пак карточек', 'Коробка карточек']:
        if price <= base[buyer['id']]['credits']:

            base[buyer['id']]['cards_packs'][item] += 1
            base[buyer['id']]['credits'] = base[buyer['id']]['credits'] - price

            save_base(base, buyer['chat_id'])

            return f'<b>{username}</b>, вы купили <b>{item}</b>.\n Теперь их у вас <b>{base[buyer["id"]]["cards_packs"][item]}</b>\n{items[item][1]}'

        else:
            return f'<b>{username}</b>, у вас нет денег\n Используйте /balance, чтобы посмотреть баланс'

    return f'<b>{username}</b>, предмет уже есть в вашем инвенторе'


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
