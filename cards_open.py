import json
import os
import random
from telebot import types
from social_credits import check_user


def load_base(chat_id):
    with open('credits_base.json', 'r', encoding='utf-8') as file:
        base = json.load(file)
        return base[chat_id]


def save_base(base):
    file = open('credits_base.json', 'w', encoding='utf-8')
    json.dump(base, file, indent=4, ensure_ascii=False)
    file.close()


regular_cards = os.listdir('cards/regular')
rare_cards = os.listdir('cards/rare')
epic_cards = os.listdir('cards/epic')
legendary_cards = os.listdir('cards/legendary')


def get_packs(user, pack):
    check_user(user)
    id = user['id']

    base = load_base(user['chat_id'])

    if base[id]['cards_packs'][pack] > 0:
        return True
    return False


def get_card_info(card):
    rare: str
    name: str

    name = '#' + card[card.find('/')+1:card.find('.')]

    if card[0:card.find('/')] == 'regular':
        rare = 'Обычная'

    elif card[0:card.find('/')] == 'rare':
        rare = 'Редкая'

    elif card[0:card.find('/')] == 'epic':
        rare = 'Эпическая'
        name = '#' + card[card.find('/'):]

    elif card[0:card.find('/')] == 'legendary':
        rare = 'Легендарная'

    else:
        rare = '???'

    return f'\n <i>{name}</i>\n\n <b>{rare}</b>'


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


def open_pack(user, item, message_id):
    check_user(user)

    id = user['id']
    cards = []

    base = load_base(user['chat_id'])

    base[id]['new_cards'] = []
    base[id]['cur_card'] = 0

    base[id]['iterator_of_message'] = message_id

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

    elif item == 'Коробка карточек' and base[id]['cards_packs'][item] > 0:
        for c in range(random.randint(150, 200)):
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
        return False


def show_cards(user):
    check_user(user)

    id = user['id']

    base = load_base(user['chat_id'])
    cur_card = base[id]['cur_card']

    if cur_card <= len(base[id]["new_cards"]) - 1:

        return base[id]["new_cards"][cur_card]

    return base[id]["new_cards"][0]


def next_back_card(user, action):
    check_user(user)

    id = user['id']
    base = load_base(user['chat_id'])

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
