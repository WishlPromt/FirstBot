import json
import os
import random
from telebot import types
from social_credits import check_user


def load_base():
    with open('credits_base.json', 'r', encoding='utf-8') as file:
        base = json.load(file)
        return base


def save_base(base):
    file = open('credits_base.json', 'w', encoding='utf-8')
    json.dump(base, file, indent=4, ensure_ascii=False)
    file.close()


regular_cards = os.listdir('cards/regular')
rare_cards = os.listdir('cards/rare')
epic_cards = os.listdir('cards/epic')
legendary_cards = os.listdir('cards/legendary')


def create_markup():
    cards_markup = types.InlineKeyboardMarkup()
    btn_next = types.InlineKeyboardButton('>>', callback_data='new Следующая')
    btn_back = types.InlineKeyboardButton('<<', callback_data='new Предыдущая')
    cards_markup.row(btn_back, btn_next)

    return cards_markup

def get_rare():
    rare_n = random.randint(1, 100)
    if rare_n < 70:
        return 'regular'

    elif rare_n <= 90:
        return 'rare'

    elif rare_n <= 99:
        return 'epic'

    else:
        return 'legendary'


def open_pack(user, item):
    check_user(user)

    id = user['id']
    cards = []

    base = load_base()

    base[id]['new_cards'] = []
    base[id]['cur_card'] = 0

    if item == 'Пак карточек' and base[id]['cards_packs'][item] > 0:
        for c in range(random.randint(5, 7)):
            rare = get_rare()
            if rare == 'regular':
                card = random.choice(regular_cards)

                cards.append(f'regular/{card}')
                base[id]['cards']['Обычные'].append(card)


            elif rare == 'rare':
                card = random.choice(rare_cards)
                cards.append(f'rare/{card}')
                base[id]['cards']['Редкие'].append(card)

            elif rare == 'epic':
                card = random.choice(epic_cards)
                cards.append(f'epic/{card}')
                base[id]['cards']['Эпические'].append(card)

            elif rare == 'legendary':
                card = random.choice(legendary_cards)
                cards.append(f'legendary/{card}')
                base[id]['cards']['Легендарные'].append(card)


        base[id]['new_cards'] = cards
        save_base(base)

    if cards != []:
        base[id]['cards_packs'][item] -= 1
        save_base(base)
        return True

    else:
        return 'Вы не получили не одной карточки'


def show_cards(user):
    check_user(user)

    id = user['id']

    base = load_base()
    cur_card = base[id]['cur_card']

    return f'{base[id]["new_cards"][cur_card]}'


def next_back_card(user, action):
    check_user(user)

    id = user['id']
    base = load_base()

    cur_card = base[id]['cur_card']

    if action == 'next':
        if cur_card < len(base[id]['new_cards']) - 1:
            base[id]['cur_card'] += 1
            save_base(base)

            return base[id]['cur_card']

        else:
            base[id]['cur_card'] = 0
            save_base(base)

            return base[id]['cur_card']

    if action == 'back':
        if cur_card > 0:
            base[id]['cur_card'] -= 1
            save_base(base)

            return base[id]['cur_card']

        else:
            base[id]['cur_card'] = len(base[id]['new_cards']) - 1
            save_base(base)

            return base[id]['cur_card']
