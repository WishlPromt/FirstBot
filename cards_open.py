import random

regular_cards = []
rare_cards = []
epic_cards = []
legendary_cards = []

for image in open('cards/regular', 'r'):
    regular_cards.append(image)


def get_rare():
    rare_n = random.randint(1, 100)
    if rare_n < 65:
        return 'regular'

    elif rare_n < 85:
        return 'rare'

    elif rare_n < 95:
        return 'epic'

    else:
        return 'legendary'


def open_pack(user, item):
    id = user[id]
    if item == 'Пак карточек':
        rare = get_rare()
        if rare == 'regular':
            return f'cards/regular/{random.choice(regular_cards)}'

        elif rare == 'rare':
            return f'cards/rare/{random.choice(rare_cards)}'

        elif rare == 'epic':
            return f'cards/rare/{random.choice(epic_cards)}'

        elif rare == 'legendary':
            return f'cards/rare/{random.choice(legendary_cards)}'

    return f'{user["username"]}, произошла ошибка, иди нахуй'


print(regular_cards)
