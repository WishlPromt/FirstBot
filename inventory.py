import json
from social_credits import check_user
from telebot import types


def load_base():
    with open('credits_base.json', 'r', encoding='utf-8') as file:
        base = json.load(file)
        return base


def load_items_base():
    with open('items.json', 'r', encoding='utf-8') as file:
        items_base = json.load(file)
        return items_base


def show_inventory(user):
    check_user(user)
    base = load_base()
    items_base = load_items_base()

    id = user['id']
    username = base[id]['username']
    inventory = base[id]['inventory']
    cards_packs = base[id]['cards_packs']

    if inventory != []:
        text = f'<b>{username}</b>, вот ваш инвентарь: \n'

        for item in inventory:
            if item not in ['Пак карточек']:
                text += f'<b>{item}</b>\n {items_base[item][3]}\n {items_base[item][1]}\n'

            else:
                text += f'<b>{item} - x{cards_packs[item]}</b>\n Предмет\n {items_base[item][1]}\n'

        return text

    else:
        return f'<b>{username}</b>, ваш инвентарь <b>пуст</b>\n /shop для покупки предметов и ролей'


def create_cards_markup(prev_rare, next_rare):
    markup = types.InlineKeyboardMarkup()

    prev_rare_btn = types.InlineKeyboardButton(prev_rare, callback_data=f'go {prev_rare}')
    next_rare_btn = types.InlineKeyboardButton(next_rare, callback_data=f'go {next_rare}')

    next_btn = types.InlineKeyboardButton('>>', callback_data='next card')
    back_btn = types.InlineKeyboardButton('>>', callback_data='back card')


    equip_btn = types.InlineKeyboardButton('В профиль', callback_data='equip card')
    sell_btn = types.InlineKeyboardButton('Продать', callback_data='sell')


    markup.row(next_btn, back_btn)
    markup.row(prev_rare_btn, next_rare_btn)
    markup.add(equip_btn)
    markup.add(sell_btn)

    return markup


def show_card_inventory(user):
    check_user(user)
    base = load_base()

    id = user['id']
    cards = base[id]['cards']

    image = cards['Обычные'][0]

    return image

