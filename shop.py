import json
from telebot import types
from social_credits import check_user
from system import load_base, save_base


#DATABASES
with open('items.json', 'r', encoding='utf-8') as file:
    items = json.load(file)


packs_items = ['Пак карточек', 'Коробка карточек', 'Anime pack', 'Motivation pack']


def get_max_pages(user):
    check_user(user)
    base = load_base(user['chat_id'])

    return base[user['id']]['max_pages']


def create_shop(page, user):
    base = load_base(user['chat_id'])
    get = get_items(page, user)
    items = get[0]
    base[user['id']]['max_pages'] = get[1]
    save_base(base, user['chat_id'])

    names = []
    for name in items:
        names.append(name)

    prices = []
    item_types = []

    for name in names:
        prices.append(items[name][0])
        item_types.append(items[name][2])

    markup = types.InlineKeyboardMarkup()

    try:
        but_item_0 = types.InlineKeyboardButton(f'{item_types[0]} {names[0]} - {str(prices[0])}', callback_data=names[0])
        markup.add(but_item_0)
    except:
        pass

    try:
        but_item_1 = types.InlineKeyboardButton(f'{item_types[1]} {names[1]} - {str(prices[1])}', callback_data=names[1])
        markup.add(but_item_1)
    except:
        pass


    try:
        but_item_2 = types.InlineKeyboardButton(f'{item_types[2]} {names[2]} - {str(prices[2])}', callback_data=names[2])
        markup.add(but_item_2)
    except:
        pass


    but_next = types.InlineKeyboardButton('>>', callback_data=f'>>{page}')
    but_back = types.InlineKeyboardButton('<<', callback_data=f'<<{page}')

    markup.row(but_back, but_next)

    return markup


def buy(item, buyer):

    check_user(buyer)

    base = load_base(buyer['chat_id'])

    inventory = base[buyer['id']]['inventory']
    username = base[buyer['id']]['username']

    if items[item][4] != 'standart' and items[item][4] not in inventory:
        return f'<b>{username}</b>, для покупки этого предмета нужна роль {items[item][4]}'

    price = items[item][0]


    if item not in inventory and item not in packs_items:
        if price <= base[buyer['id']]['credits']:

            inventory.append(item)
            base[buyer['id']]['inventory'] = inventory
            base[buyer['id']]['credits'] = base[buyer['id']]['credits'] - price

            save_base(base, buyer['chat_id'])

            return f'<b>{username}</b>, вы купили <b>{item}</b>!\n{items[item][1]}'

        else:
            return f'<b>{username}</b>, у вас нет денег\n Используйте /balance, чтобы посмотреть баланс'

    elif item not in inventory and item in packs_items:
        if price <= base[buyer['id']]['credits']:

            inventory.append(item)
            base[buyer['id']]['cards_packs'][item] = 1
            base[buyer['id']]['inventory'] = inventory
            base[buyer['id']]['credits'] = base[buyer['id']]['credits'] - price

            save_base(base, buyer['chat_id'])

            return f'<b>{username}</b>, вы купили <b>{item}</b>.\n{items[item][1]}'

        else:
            return f'<b>{username}</b>, у вас нет денег\n'

    elif item in inventory and item in packs_items:
        if price <= base[buyer['id']]['credits']:

            base[buyer['id']]['cards_packs'][item] += 1
            base[buyer['id']]['credits'] = base[buyer['id']]['credits'] - price

            save_base(base, buyer['chat_id'])

            return f'<b>{username}</b>, вы купили <b>{item}</b>.\n Теперь их у вас <b>{base[buyer["id"]]["cards_packs"][item]}</b>\n{items[item][1]}'

        else:
            return f'<b>{username}</b>, у вас нет денег\n Используйте /balance, чтобы посмотреть баланс'

    return f'<b>{username}</b>, предмет уже есть в вашем инвентаре'


def next_page(cur_page, max_pages):
    if cur_page < max_pages:
        return cur_page + 1
    else:
        return 1


def back_page(cur_page, max_pages):
    if cur_page > 1:
        return cur_page - 1
    else:
        return max_pages


def get_items(page, user):
    base = load_base(user['chat_id'])
    items_on_page = {}
    list_items = list(items.keys())
    id = user['id']

    for i in list_items:
        if items[i][4] != 'standart' and not items[i][4] in base[id]['inventory']:
            list_items.remove(i)

    for item in base[id]['inventory']:
        if item not in packs_items:
            list_items.remove(item)

    list_items = [list_items[i:i + 3] for i in range(0, len(list_items), 3)]

    for item in list_items[page-1]:
        items_on_page[item] = items[item]

    return [items_on_page, len(list_items)]
