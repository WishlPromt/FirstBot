import time

def convert_time(datetime):
    return time.strftime('%H:%M:%S %d.%m.%Y', time.localtime(datetime))

def get_message_data(data):
    id = str(data.from_user.id)
    username = data.from_user.username
    name = data.from_user.first_name
    try:
        datetime = data.date
    except:
        datetime = 0

    return {'id': id,
            'username': username,
            'datetime': datetime,
            'name': name}