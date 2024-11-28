from social_credits import check_user
from system import load_base, save_base, convert_time


def get_item(user, item):
    check_user(user)
    base = load_base(user['chat_id'])

    if item in base[user['id']]['inventory']:
        return True


def get_time(user, command):
    check_user(user)
    base = load_base(user['chat_id'])
    id = user['id']

    if command in base[id]['special_time']:
        if user['datetime'] >= base[id]['special_time'][command]:
            return False
        return convert_time(base[id]['special_time'][command])
    return 'error'


def set_time(user, command):
    check_user(user)
    base = load_base(user['chat_id'])
    id = user['id']

    if command in base[id]['special_time']:
        base[id]['special_time'][command] = user['datetime'] + 259200
        save_base(base, user['chat_id'])