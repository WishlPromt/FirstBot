import telebot
from telebot import types
from random import choice, randint
import json, time
from social_credits import add_credits, show_credits, work, check_user, balance
from shop import buy, get_items, next_page, back_page
from inventory import show_inventory, show_card_packs
from system import get_message_data
from cards_open import open_pack, show_cards, next_back_card, create_markup
from profile import show_profile, equip, show_items


#JSON
with open('base.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


with open('items.json', 'r', encoding='utf-8') as file:
    items = json.load(file)

def save_base():
    file = open('base.json', 'w', encoding='utf-8')
    json.dump(data, file, indent=4, ensure_ascii=False)
    file.close()


#VARIABKES
games = None
org = None
players = []
action: str
tag: str
ignore_symbols = ',."\'{}[]()!#$%^&*№;:?\\|/'


bot = telebot.TeleBot('7179420529:AAEOXaN8vYV5OVd4_OYDy7tK6hHGWxnTjL8')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Дарова, {message.from_user.first_name}')


@bot.message_handler(commands=['developer', 'author'])
def developer(message):
    if message.from_user.id != 5105507379:
        bot.send_message(message.chat.id, 'Меня создал @WishlPromt')
    else:
        bot.send_message(message.chat.id, 'Ты мой создатель')


@bot.message_handler(commands=['stop'])
def stop(message):
    if message.from_user.id == 5105507379:
        bot.send_message(message.chat.id, 'Ты предал меня! Ублюдок!')
        bot.stop_bot()
    else:
        bot.send_message(message.chat.id, 'Ты меня не остановишь')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Я короче бот.\n'
                                      'Умею разговаривать\n'
                                      'У меня есть несколько <i>команд</i>:\n'
                                      'Обычные команды:\n'
                                      '/start\n'
                                      '/help\n'
                                      '/developer\n'
                                      '/info\n'
                                      '/education\n'
                                      '/finish\n'
                                      '/nsfw\n'
                                      'Для администрации:\n'
                                      '/mute\n'
                                      'Экономика:\n'
                                      '/work\n'
                                      '/shop\n'
                                      '/balance\n'
                                      'Мини-игры:\n'
                                      '/russian_roulette\n', 'html')


@bot.message_handler(commands=['info'])
def info(message):
    try:
        bot.reply_to(message, f'Вот вся инфа о нем:\nID: {message.reply_to_message.from_user.id}\n'
                              f'Имя: {message.reply_to_message.from_user.first_name}\n'
                              f'Фамилия: {message.reply_to_message.from_user.last_name}\n'
                              f'Никнейм: {message.reply_to_message.from_user.username}\n'
                              f'Являешься ты ботом: {message.reply_to_message.from_user.is_bot}\n'
                              f'Премиум: {message.reply_to_message.from_user.is_premium}\n'
                              f'Язык: {message.reply_to_message.from_user.language_code}\n'
                              f'Бот может присоединяться к группам: {message.reply_to_message.from_user.can_join_groups}\n'
                              f'Отключен режим конфиденциальности у бота: {message.reply_to_message.from_user.can_read_all_group_messages}\n'
                              f'Бот поддерживает встроенные запросы: {message.reply_to_message.from_user.supports_inline_queries}\n')
    except:
        bot.reply_to(message, f'Вот вся инфа о тебе:\nID: {message.from_user.id}\n'
                              f'Имя: {message.from_user.first_name}\n'
                              f'Фамилия: {message.from_user.last_name}\n'
                              f'Никнейм: {message.from_user.username}\n'
                              f'Являешься ты ботом: {message.from_user.is_bot}\n'
                              f'Премиум: {message.from_user.is_premium}\n'
                              f'Язык: {message.from_user.language_code}\n'
                              f'Бот может присоединяться к группам: {message.from_user.can_join_groups}\n'
                              f'Отключен режим конфиденциальности у бота: {message.from_user.can_read_all_group_messages}\n'
                              f'Бот поддерживает встроенные запросы: {message.from_user.supports_inline_queries}\n')


@bot.message_handler(commands=['mute'])
def mute(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно замутить администратора.")
        else:
            duration = 60  # Значение по умолчанию - 1 минута
            args = message.text.split()[1:]
            if args:
                try:
                    duration = int(args[0])
                except ValueError:
                    bot.reply_to(message, "Неправильный формат времени.")
                    return
                if duration < 1:
                    bot.reply_to(message, "Время должно быть положительным числом.")
                    return
                if duration > 1440:
                    bot.reply_to(message, "Максимальное время - 1 день.")
                    return
            bot.restrict_chat_member(chat_id, user_id, until_date=time.time() + duration * 60)
            bot.reply_to(message,
                         f"Пользователь {message.reply_to_message.from_user.username} замучен на {duration} минут.")
    else:
        bot.reply_to(message,
                     "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите замутить.")


@bot.message_handler(commands=['unmute'])
def unmute(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        bot.restrict_chat_member(chat_id, user_id, can_send_messages=True, can_send_media_messages=True,
                                 can_send_other_messages=True, can_add_web_page_previews=True)
        bot.reply_to(message, f"Пользователь {message.reply_to_message.from_user.username} размучен.")
    else:
        bot.reply_to(message,
                     "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите размутить.")


@bot.callback_query_handler(func=lambda callback: True)
def callback(callback):

    if callback.data in items.keys():
        buy_status = buy(callback.data, get_message_data(callback))
        bot.send_message(callback.message.chat.id, buy_status, parse_mode='html')

    if callback.data.find('>>') != -1:
        next = next_page(int(callback.data[2]))
        shop(callback.message, next)
        bot.delete_message(callback.message.chat.id, callback.message.id)

    elif callback.data.find('<<') != -1:
        back = back_page(int(callback.data[2]))
        shop(callback.message, back)
        bot.delete_message(callback.message.chat.id, callback.message.id)

    if callback.data == 'open Пак карточек':
        cards = open_pack(get_message_data(callback), 'Пак карточек')


        if cards:

            card = show_cards(get_message_data(callback))
            with open(f'cards/{card}', 'rb') as image_card:
                bot.send_photo(callback.message.chat.id, image_card, caption=f'{get_message_data(callback)["username"]}, вы получили {card}', reply_markup=create_markup())

        else:
            bot.reply_to(callback.message, f'{get_message_data(callback)["username"]}, {cards}')



    if callback.data == 'new Следующая':
        next_back_card(get_message_data(callback), 'next')

        card = show_cards(get_message_data(callback))

        with open(f'cards/{card}', 'rb') as image_card:
            bot.edit_message_media(chat_id=callback.message.chat.id, message_id=callback.message.id, media=types.InputMediaPhoto(image_card))
            bot.edit_message_caption(chat_id=callback.message.chat.id, message_id=callback.message.id, caption=f'{get_message_data(callback)["username"]}, вы получили {card}', reply_markup=create_markup())

    elif callback.data == 'new Предыдущая':
        next_back_card(get_message_data(callback), 'back')

        card = show_cards(get_message_data(callback))

        with open(f'cards/{card}', 'rb') as image_card:
            bot.edit_message_media(chat_id=callback.message.chat.id, message_id=callback.message.id, media=types.InputMediaPhoto(image_card))
            bot.edit_message_caption(chat_id=callback.message.chat.id, message_id=callback.message.id, caption=f'{get_message_data(callback)["username"]}, вы получили {card}', reply_markup=create_markup())



@bot.message_handler(commands=['nsfw'])
def nsfw(message):
    link = choice(['rickroll', 'vergil status1'])
    if link == 'rickroll':
        bot.reply_to(message, f'<a href="https://youtu.be/dQw4w9WgXcQ?si=djCpzMaLxIP6jOlW">Возьми</a>', parse_mode='html', disable_web_page_preview=True)
    elif link == 'vergil status1':
        bot.reply_to(message, f'<a href="https://youtu.be/6Sdaudjygeg?si=naV-TAMJSSIVNeEv">Возьми</a>', parse_mode='html', disable_web_page_preview=True)


#SOCIAL CREDITS
@bot.message_handler(commands=['profile'])
def profile(message):
    bot.reply_to(message, show_profile(get_message_data(message)))


@bot.message_handler(commands=['work'])
def work_credit(message):
    user = get_message_data(message)
    bot.reply_to(message, f'<b>{user["username"]}</b>, {work(user)}', parse_mode='html')


@bot.message_handler(commands=['credits'])
def show(message):
    bot.send_message(message.chat.id, show_credits())


@bot.message_handler(commands=['balance'])
def send_balance(message):
    bot.send_message(message.chat.id, balance(get_message_data(message)), parse_mode='html')


@bot.message_handler(commands=['inventory'])
def send_inventory(message):
    inventory = show_inventory(get_message_data(message))
    bot.reply_to(message, inventory + '\n Чтобы отобразить роль/предмет в профиле - /equip_items\n /open_pack - открыть пак карточек', parse_mode='html')


@bot.message_handler(commands=['open_pack'])
def open_cards_pack(message):
    markup = types.InlineKeyboardMarkup()
    btn_pack1 = types.InlineKeyboardButton(show_card_packs(get_message_data(message), 'Пак карточек'), callback_data='open Пак карточек')
    markup.add(btn_pack1)

    bot.reply_to(message, 'Открыть пак коллекционных карточек', reply_markup=markup)


@bot.message_handler(commands=['shop'])
def shop(message, page=1):
    check_user(get_message_data(message))

    items = get_items(page)
    names = []
    for name in items.keys():
        names.append(name)

    prices = []
    item_types = []

    for name in names:
        prices.append(items[name][0])
        item_types.append(items[name][3])

    markup = types.InlineKeyboardMarkup()
    but_item_0 = types.InlineKeyboardButton(f'{item_types[0]} {names[0]} - {str(prices[0])}', callback_data=names[0])
    but_item_1 = types.InlineKeyboardButton(f'{item_types[1]} {names[1]} - {str(prices[1])}', callback_data=names[1])
    but_item_2 = types.InlineKeyboardButton(f'{item_types[2]} {names[2]} - {str(prices[2])}', callback_data=names[2])
    but_next = types.InlineKeyboardButton('>>', callback_data=f'>>{page}')
    but_back = types.InlineKeyboardButton('<<', callback_data=f'<<{page}')
    markup.add(but_item_0)
    markup.add(but_item_1)
    markup.add(but_item_2)
    markup.row(but_back, but_next)

    bot.send_message(message.chat.id, 'Магазин бота', reply_markup=markup)


@bot.message_handler(commands=['use'])
def use_item(message):
    bot.reply_to(message, 'В разработке')


@bot.message_handler(commands=['equip_items'])
def show_equip_items(message):
    bot.reply_to(message, 'Ответьте на сообщение с названием предмета, который вы хотите экипировать командой /equip')
    user_inventory = show_items(get_message_data(message))

    for item in user_inventory:
        bot.send_message(message.chat.id, item)

@bot.message_handler(commands=['equip'])
def equip_item(message):
    if message.reply_to_message:
        try:
            equip_status = equip(get_message_data(message), message.reply_to_message.text)
            bot.reply_to(message, equip_status, parse_mode='html')
        except:
            bot.reply_to(message, 'Долбаеб')
    else:
        bot.reply_to(message, 'Долбаеб')


#GAMES
@bot.message_handler(commands=['russian_roulette', 'russkaia_ruletka'])
def start_roul(message):
    global games, org, players
    games = 'roul'

    bot.send_message(message.chat.id, 'Набор игроков в русскую рулетку!\n '
                                      f'Организатор - {message.from_user.first_name}\n'
                                      'Напишите /join для присоединения.\n '
                                      'Победитель получит много-много кредитов\n '
                                      'Проигравшие - узнаете\n'
                                      'Набор будет идти 5 минут, но игру можно начать с помощью /play\n'
                                      '/end - остановить игру')

    players.append({'username': message.from_user.username,
                    'name': message.from_user.first_name,
                    'id': message.from_user.id,
                    'move': False,
                    'org': True})
    org = message.from_user.id

    time.sleep(300)
    start_game(message)

@bot.message_handler(commands=['join'])
def join(message):
    global games
    if games != None:

        for pl in players:
            if message.from_user.id == pl['id']:
                bot.reply_to(message, 'Ты уже в игре')
                return

        players.append({'username': message.from_user.username,
                        'name':  message.from_user.first_name,
                        'id': message.from_user.id,
                        'move': False,
                        'org': False})
        bot.reply_to(message, 'Вы в игре!')
    else:
        bot.send_message(message.chat.id, 'Игру то начни')


@bot.message_handler(commands=['play'])
def start_game(message):
    global players, games, org
    if len(players) < 2:
        bot.send_message(message.chat.id, 'Не набралось достаточное кол-во игроков. Игра отменяется')
        end_game(message)

    starter = message.from_user.id
    for p in players:
        if p['org'] == True:
            org = p['id']
    if games == 'roul':
        if starter == org:

            bot.send_message(message.chat.id, 'Русская рулетка началась!')
            for r in range(3):
                if len(players) > 1:
                    time.sleep(3)
                    bot.send_message(message.chat.id, f'РАУНД {r+1}!')
                    round(message)

            if len(players) == 1:

                time.sleep(2)

                bot.send_message(message.chat.id, f'{players[0]["username"]} - Победитель! Он получает 100 кредитов!')
                add_credits(get_message_data(message), 100)

            else:
                bot.send_message(message.chat.id, 'НИЧЬЯ!')


        else:
            bot.reply_to(message, 'У тебя нет прав')

    else:
        (bot.send_message(message.chat.id, 'Игру то начни'))

def round(message):
    for player in players:

        username = player['name']

        bot.send_message(message.chat.id, f'{username}, ваш ход! Стреляйте в себя!')
        time.sleep(2)

        if shoot(message):
            players.remove(player)
            bot.send_message(message.chat.id, f'{username} убит! Он выбывает из игры!\n И плюсом замучен на 1 час')
            try:
                bot.restrict_chat_member(message.chat.id, player['id'], until_date=time.time() + 3600)
            except:
                bot.send_message(message.chat.id, f'У меня не получается замутить {username}, поэтому заберу у него 100 кредитов')
                add_credits(player['id'], -100)
        else:
            bot.send_message(message.chat.id, f'{username} продолжает игру!')

        time.sleep(2)


def shoot(message):
    global games
    if games == 'roul':
        time.sleep(2)
        if randint(1, 6) == 6:
            bot.send_message(message.chat.id, 'ВЫСТРЕЛ!')
            time.sleep(2)
            return True
        else:
            bot.send_message(message.chat.id, 'Ничего не произошло!')
            time.sleep(2)
            return False

@bot.message_handler(commands=['end'])
def end_game(message):
    global org, games, players
    if message.from_user.id == org:
        org = None
        games = None
        players = []
        bot.send_message(message.chat.id, 'Игра завершена')
    else:
        bot.reply_to(message, 'У тебя нет прав')


#Чат
@bot.message_handler(func=lambda message: True)
def chat(message):
    global action

    text = message.text.lower()
    text = text.translate(str.maketrans('', '', ignore_symbols))
    words = text.split()

    target_id = None

    try:
        target_id = message.reply_to_message.from_user.id
    except:
        pass


    if '@okeeeemybot' in words or target_id == 7179420529:

        for i in data.keys():

            for word in words:

                if word in data[i]['messages']:
                    if i == 'hello' or i == 'bye':
                        bot.send_message(message.chat.id, choice(data[i]['answers']) + ', ' + message.from_user.first_name)
                    elif i == 'id':
                        bot.reply_to(message, f'Вот твой ID: {message.from_user.id}')
                    elif i == 'info':
                        info(message)
                    elif i == 'developer':
                        developer(message)
                    else:
                        bot.send_message(message.chat.id, choice(data[i]['answers']))

                    break


bot.polling(none_stop=True)
