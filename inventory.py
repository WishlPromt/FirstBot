import json
from social_credits import check_user


def load_base():
    with open('credits_base.json', 'r', encoding='utf-8') as file:
        base = json.dump(file)
        return base


def show_inventory(user):
    check_user(user)
    base = load_base()

    id = user['id']
    username = base[id]['username']
    inventory = base[id]['inventory']
    cards_packs = base[id]['cards_packs']

    if inventory != []:
        text = f'<b>{username}</b>, вот ваш инвентарь: \n'

        for item in inventory:
            if item not in ['Пак карточек']:
                text += f'<b>{item}</b>\n'

            else:
                text += f'<b>{item}x{cards_packs['item']}</b>\n'

        return text

    else:
        return f'<b>{username}</b>, ваш инвентарь <b>пуст</b>\n /shop для покупки предметов и ролей'
