import json
from social_credits import check_user
from telebot import types
from system import load_base, save_base


def load_items_base():
    with open('items.json', 'r', encoding='utf-8') as file:
        items_base = json.load(file)
        return items_base


def show_inventory(user):
    check_user(user)
    base = load_base(user['chat_id'])
    items_base = load_items_base()

    id = user['id']
    username = base[id]['username']
    inventory = get_inventory(user)
    cards_packs = base[id]['cards_packs']

    if inventory:
        text = f'<b>{username}</b>, вот ваш инвентарь: \n'

        for item in inventory:
            if item not in ['Пак карточек', 'Коробка карточек', 'Anime pack', 'Motivation pack']:
                text += f'<b>{item}</b>\n {items_base[item][2]}\n {items_base[item][1]}\n'

            else:
                text += f'<b>{item} - x{cards_packs[item]}</b>\n Предмет\n {items_base[item][1]}\n'

        return text

    else:
        return f'<b>{username}</b>, ваш инвентарь <b>пуст</b>\n /shop для покупки предметов и ролей'


def get_inventory(user):
    check_user(user)
    base = load_base(user['chat_id'])
    return base[user['id']]['inventory']


def create_cards_markup():

    markup = types.InlineKeyboardMarkup()

    next_btn = types.InlineKeyboardButton('>>', callback_data='next card')
    back_btn = types.InlineKeyboardButton('<<', callback_data='back card')

    equip_btn = types.InlineKeyboardButton('В профиль', callback_data='equip card')
    sell_btn = types.InlineKeyboardButton(f'Продать', callback_data='sell')

    markup.row(back_btn, next_btn)
    markup.add(equip_btn)
    markup.add(sell_btn)

    return markup


def get_cards(user):
    check_user(user)

    id = user['id']
    base = load_base(user['chat_id'])

    cards = base[id]['cards']

    for rare in cards:
        for card in cards[rare]:
            if rare == 'Обычные':
                base[id]['new_cards'].append('regular/'+card)

            elif rare == 'Редкие':
                base[id]['new_cards'].append('rare/'+card)

            elif rare == 'Эпические':
                base[id]['new_cards'].append('epic/'+card)

            elif rare == 'Легендарные':
                base[id]['new_cards'].append('legendary/'+card)

            elif rare == 'Секретные':
                base[id]['new_cards'].append('secret/' + card)


    save_base(base, user['chat_id'])


def show_card_inventory(card):

    if card[:2] == 're':
        image = f'cards/regular/{card}'

    elif card[:2] == 'ra':
        image = f'cards/rare/{card}'

    elif card[0] == 'e':
        image = f'cards/epic/{card}'

    else:
        image = f'cards/legendary/{card}'

    return image


def reset_cards(user):
    check_user(user)
    id = user['id']
    base = load_base(user['chat_id'])

    base[id]['new_cards'] = []
    base[id]['cur_card'] = 0

    save_base(base, user['chat_id'])
