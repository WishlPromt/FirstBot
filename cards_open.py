import json
import os
import random


def load_base():
    with open('credits_base.json', 'r', encoding='utf-8') as file:
        base = json.load(file)
        return base


def save_base(base):
    file = open('credits_base.json', 'w', encoding='utf-8')
    json.dump(base, file, indent=4, ensure_ascii='utf-8')
    file.close()


regular_cards = os.listdir('cards/regular')
rare_cards = os.listdir('cards/rare')
epic_cards = os.listdir('cards/epic')
legendary_cards = os.listdir('cards/legendary')


def get_rare():
    rare_n = random.randint(1, 100)
    if rare_n < 65:
        return 'regular'

    elif rare_n <= 85:
        return 'rare'

    elif rare_n <= 95:
        return 'epic'

    else:
        return 'legendary'


def open_pack(user, item):
    id = user['id']
    cards = []

    base = load_base()

    if item == 'Пак карточек':
        for c in range(random.randint(5, 7)):
            rare = get_rare()
            if rare == 'regular':
                card = random.choice(regular_cards)
                cards.append(f'regular/{card}')
                base[id]['cards']['Обычные'] = card
                save_base(base)

            elif rare == 'rare':
                card = random.choice(rare_cards)
                cards.append(f'rare/{card}')
                base[id]['cards']['Редкие'] = card
                save_base(base)

            elif rare == 'epic':
                card = random.choice(epic_cards)
                cards.append(f'epic/{card}')
                base[id]['cards']['Эпические'] = card
                save_base(base)

            elif rare == 'legendary':
                card = random.choice(legendary_cards)
                cards.append(f'legendary/{card}')
                base[id]['cards']['Легендарные'] = card
                save_base(base)

    if cards != []:
        return cards

    else:
        return False




