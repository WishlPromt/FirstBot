import json

from social_credits import check_user

def load_base():
    with open('credits_base.json', 'r', encoding='utf-8') as file:
        base = json.load(file)
        return base

def load_items():
    with open('items.json', 'r', encoding='utf-8') as file:
        items = json.load(file)
        return items

def save_base(base):
    file = open('credits_base.json', 'w', encoding='utf-8')
    json.dump(base, file, indent=4, ensure_ascii=False)
    file.close()


def show_profile(user):
    check_user(user)
    id = user['id']
    base = load_base()

    username = base[id]['username']
    credits = base[id]['credits']
    fav_item = base[id]['favorite_item']
    role = base[id]['role']
    fav_card = base[id]['favorite_card']

    profile = [f'<b>{username}</b> - <b>{role}</b>\n'
               f'<b>Кредиты</b>: <b>{credits}</b>\n'
               f'<b>Любимый предмет</b>: <b>{fav_item}</b>\n'
               f'<b>Любимая карта</b>: <b>{fav_card[fav_card.find("/")+1:fav_card.find(".")]}</b>',
               base[id]['favorite_card']]

    return profile

def equip(user, item):
    check_user(user)
    id = user['id']
    items = load_items()
    base = load_base()

    if item in base[id]['inventory']:

        if items[item][2] == 'Предмет':
            base[id]['favorite_item'] = item
            save_base(base)
            return f'Теперь предмет <b>{item}</b> отображается у вас в /profile'

        elif items[item][2] == 'Роль':
            base[id]['role'] = item
            save_base(base)
            return f'Теперь роль <b>{item}</b> отображается у вас в /profile'

        return 'Ошибка. Иди нахуй'

    else:
        return 'Это не твой предмет/роль. Иди нахуй'


def equip_card(user, card):
    check_user(user)
    id = user['id']
    base = load_base()

    base[id]['favorite_card'] = card

    save_base(base)


def show_items(user):
    check_user(user)
    id = user['id']
    base = load_base()

    return base[id]['inventory']
