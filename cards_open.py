import os
import random


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

    if item == 'Пак карточек':
        for card in range(random.randint(5, 7)):
            rare = get_rare()
            if rare == 'regular':
                cards.append(f'regular/{random.choice(regular_cards)}')
                print(cards)

            elif rare == 'rare':
                cards.append(f'rare/{random.choice(rare_cards)}')
                print(cards)

            elif rare == 'epic':
                cards.append(f'epic/{random.choice(epic_cards)}')
                print(cards)

            elif rare == 'legendary':
                cards.append(f'legendary/{random.choice(legendary_cards)}')
                print(cards)

    if cards != []:
        return cards

    else:
        return False




