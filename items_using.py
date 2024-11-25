from social_credits import check_user
from system import load_base
def get_item(user, item):
    check_user(user)
    base = load_base(user['chat_id'])

    if item in base[user['id']]['inventory']:
        return True
