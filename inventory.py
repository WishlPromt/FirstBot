import json
from social_credits import check_user

def load_base():
    with open('credits_base.json', 'r', encoding='utf-8') as file:
        base = json.dump(file)


def show_inventory(user):
    check_user(user)
    load_base()

    id = user['id']
