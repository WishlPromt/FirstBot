import json
from telebot import types
from social_credits import check_user


#DATABASES
with open('items.json', 'r', encoding='utf-8') as file:
    items = json.load(file)


credits = {}

def load_base():
    global credits
    with open('credits_base.json', 'r', encoding='utf-8') as file:
        credits = json.load(file)


load_base()


def save_inventory():
    file = open('credits_base.json', 'w', encoding='utf-8')
    json.dump(credits, file, indent=4, ensure_ascii=False)
    file.close()


#Variables
max_pages = 4


def create_shop(page):
    items = get_items(page)
    names = []
    for name in items.keys():
        names.append(name)

    prices = []
    item_types = []

    for name in names:
        prices.append(items[name][0])
        item_types.append(items[name][3])

    markup = types.InlineKeyboardMarkup()
    but_item_0 = types.InlineKeyboardButton(f'{item_types[0]} {names[0]} - {str(prices[0])}', callback_data=names[0])
    but_item_1 = types.InlineKeyboardButton(f'{item_types[1]} {names[1]} - {str(prices[1])}', callback_data=names[1])
    but_item_2 = types.InlineKeyboardButton(f'{item_types[2]} {names[2]} - {str(prices[2])}', callback_data=names[2])
    but_next = types.InlineKeyboardButton('>>', callback_data=f'>>{page}')
    but_back = types.InlineKeyboardButton('<<', callback_data=f'<<{page}')
    markup.add(but_item_0)
    markup.add(but_item_1)
    markup.add(but_item_2)
    markup.row(but_back, but_next)

    return markup


def buy(item, buyer):

    check_user(buyer)

    load_base()

    inventory = credits[buyer['id']]['inventory']
    username = credits[buyer['id']]['username']


    price = items[item][0]


    if item not in inventory and item not in ['Пак карточек', 'Коробка карточек']:
        if price <= credits[buyer['id']]['credits']:

            inventory.append(item)
            credits[buyer['id']]['inventory'] = inventory
            credits[buyer['id']]['credits'] = credits[buyer['id']]['credits'] - price

            save_inventory()

            return f'<b>{username}</b>, вы купили <b>{item}</b>!\n{items[item][1]}'

        else:
            return f'<b>{username}</b>, у вас нет денег\n Используйте /balance, чтобы посмотреть баланс'

    elif item not in inventory and item in ['Пак карточек', 'Коробка карточек']:
        if price <= credits[buyer['id']]['credits']:

            inventory.append(item)
            credits[buyer['id']]['cards_packs'][item] = 1
            credits[buyer['id']]['inventory'] = inventory
            credits[buyer['id']]['credits'] = credits[buyer['id']]['credits'] - price

            save_inventory()

            return f'<b>{username}</b>, вы купили <b>{item}</b>.\n{items[item][1]}'

        else:
            return f'<b>{username}</b>, у вас нет денег\n'

    elif item in inventory and item in ['Пак карточек', 'Коробка карточек']:
        if price <= credits[buyer['id']]['credits']:

            credits[buyer['id']]['cards_packs'][item] += 1
            credits[buyer['id']]['credits'] = credits[buyer['id']]['credits'] - price

            save_inventory()

            return f'<b>{username}</b>, вы купили <b>{item}</b>.\n Теперь их у вас <b>{credits[buyer["id"]]["cards_packs"][item]}</b>\n{items[item][1]}'

        else:
            return f'<b>{username}</b>, у вас нет денег\n Используйте /balance, чтобы посмотреть баланс'

    return f'<b>{username}</b>, предмет уже есть в вашем инвенторе'


def next_page(cur_page):
    if cur_page < max_pages:
        return cur_page + 1
    else:
        return 1


def back_page(cur_page):
    if cur_page > 1:
        return cur_page - 1
    else:
        return max_pages


def get_items(page):
    items_on_page = {}
    for item in items:
        if items[item][2] == page:
            items_on_page[item] = (items[item])

    return items_on_page
