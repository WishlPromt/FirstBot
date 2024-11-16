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


def add_credits(user: dict, credits, base):
    check_user(user)

    id = user['id']
    base[id]['credits'] = base[id]['credits'] + credits
    save_base(base)


regular_cards = os.listdir('cards/regular')
rare_cards = os.listdir('cards/rare')
epic_cards = os.listdir('cards/epic')
legendary_cards = os.listdir('cards/legendary')
secret_cards = os.listdir('cards/secret')


def get_packs(user, pack):
    check_user(user)
    id = user['id']

    base = load_base()

    if base[id]['cards_packs'][pack] > 0:
        return base[id]['cards_packs'][pack]
    return False


def get_card_info(card, user):
    check_user(user)
    base = load_base()
    id = user['id']

    rare: str
    name: str
    count: str

    name = '#' + card[card.find('/')+1:card.find('.')]
    count = str(base[id]['cur_card']+1) + '/' + str(len(base[id]['new_cards']))

    if card[0:card.find('/')] == 'regular':
        rare = 'Обычная'

    elif card[0:card.find('/')] == 'rare':
        rare = 'Редкая'

    elif card[0:card.find('/')] == 'epic':
        rare = 'Эпическая'
        name = '#' + card[card.find('/'):]

    elif card[0:card.find('/')] == 'legendary':
        rare = 'Легендарная'

    elif card[0:card.find('/')] == 'secret':
        rare = 'Секретная'

    else:
        rare = '???'

    return f'{count}\n <i>{name}</i>.\n\n <b>{rare}</b>'


def create_markup():
    cards_markup = types.InlineKeyboardMarkup()
    btn_next = types.InlineKeyboardButton('>>', callback_data='new Следующая')
    btn_back = types.InlineKeyboardButton('<<', callback_data='new Предыдущая')
    btn_profile = types.InlineKeyboardButton('В профиль', callback_data='equip card')
    btn_sell = types.InlineKeyboardButton('Продать', callback_data='sell')

    cards_markup.row(btn_back, btn_next)
    cards_markup.add(btn_profile)
    cards_markup.add(btn_sell)

    return cards_markup


def create_simple_markup():
    cards_markup = types.InlineKeyboardMarkup()
    btn_next = types.InlineKeyboardButton('>>', callback_data='new Следующая')
    btn_back = types.InlineKeyboardButton('<<', callback_data='new Предыдущая')

    cards_markup.row(btn_back, btn_next)

    return cards_markup


def create_markup_photo():
    markup = types.InlineKeyboardMarkup()
    btn_regular = types.InlineKeyboardButton('Обычная', callback_data='regular')
    btn_rare = types.InlineKeyboardButton('Редкая', callback_data='rare')
    btn_epic = types.InlineKeyboardButton('Эпическая', callback_data='epic')
    btn_legendary = types.InlineKeyboardButton('Легендарная', callback_data='legendary')
    btn_secret = types.InlineKeyboardButton('Секретная', callback_data='secret')

    markup.add(btn_regular)
    markup.add(btn_rare)
    markup.add(btn_epic)
    markup.add(btn_legendary)
    markup.add(btn_secret)

    return markup


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


def get_special_rare():
    rare_n = random.randint(1, 100)
    if rare_n <= 70:
        return 'rare'

    elif rare_n <= 90:
        return 'epic'

    elif rare_n <= 99:
        return 'legendary'

    else:
        return 'secret'


def open_pack(user, item):
    check_user(user)

    id = user['id']
    cards = []

    base = load_base()

    base[id]['new_cards'] = []
    base[id]['cur_card'] = 0

    min_cards = [5, 150, 12]
    max_cards = [7, 200, 12]

    if ('Motivated' or 'Любитель аниме-тянок') in base[id]['inventory']:
        print('true')
        for min in range(len(min_cards)):
            min_cards[min] += int(min_cards[min] / 100 * 25)
        print(min_cards)
        for max in range(len(max_cards)):
            max_cards[max] += int(max_cards[max] / 100 * 25)
        print(max_cards)

    if item == 'Пак карточек' and base[id]['cards_packs'][item] > 0:
        for c in range(random.randint(min_cards[0], max_cards[0])):
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
        for c in range(random.randint(min_cards[1], max_cards[1])):
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

    elif item == 'Anime pack' or item == 'Motivation pack' and base[id]['cards_packs'][item] > 0:
        for c in range(random.randint(min_cards[2], max_cards[2])):
            rare = get_special_rare()
            if rare == 'rare':
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

            elif rare == 'secret':
                card = random.choice(secret_cards)
                cards.append(f'secret/{card}')
                base[id]['cards']['Секретные'].append(card)

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

    base = load_base()
    cur_card = base[id]['cur_card']

    if cur_card <= len(base[id]["new_cards"]) - 1:

        return base[id]["new_cards"][cur_card]

    return base[id]["new_cards"][0]


def get_cur_card(user):
    base = load_base()

    return base[user['id']]['new_cards'][base[user['id']]['cur_card']]


def sell_card(user):
    check_user(user)

    id = user['id']
    base = load_base()
    cur_card = base[id]['new_cards'][base[id]['cur_card']]
    rare = cur_card[0:cur_card.find('/')]
    name = cur_card[cur_card.find('/')+1:]

    if rare == 'regular':
        price = 3
        base[id]['cards']['Обычные'].remove(name)
        base[id]['new_cards'].remove(cur_card)
        add_credits(user, price, base)

    elif rare == 'rare':
        price = 7
        base[id]['cards']['Редкие'].remove(name)
        base[id]['new_cards'].remove(cur_card)
        add_credits(user, price, base)

    elif rare == 'epic':
        price = 15
        base[id]['cards']['Эпические'].remove(name)
        base[id]['new_cards'].remove(cur_card)
        add_credits(user, price, base)

    elif rare == 'legendary':
        price = 200
        base[id]['cards']['Легендарные'].remove(name)
        base[id]['new_cards'].remove(cur_card)
        add_credits(user, price, base)

    else:
        return False

    return [name, price]

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
