import json

from social_credits import check_user

def load_base():
    with open('credits_base.json', 'r', encoding='utf-8') as file:
        base = json.load(file)
        return base


def show_profile(user):
    check_user(user)
    id = user['id']
    base = load_base()

    username = base[id]['username']
    credits = base[id]['credits']
    fav_item = base[id]['favorite_item']
    role = base[id]['role']
    fav_card = base[id]['favorite_card']

    profile = (f'{username} - {role}\n'
               f'Кредиты: {credits}\n'
               f'Любимый предмет: {fav_item}\n'
               f'Любимая карта: {fav_card}')

    return profile
