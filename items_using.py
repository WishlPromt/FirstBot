from social_credits import check_user
from system import load_base
def get_master(user):
    check_user(user)
    base = load_base(user['chat_id'])

    if ('Dungeon master' or 'Full master') in base[user['id']]['inventory']:
        return True
