import time

def convert_time(datetime):
    return time.strftime('%H:%M:%S %d.%m.%Y', time.localtime(datetime))