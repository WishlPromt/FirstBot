import telebot
from telebot import types
from random import choice, randint
import json, time
from social_credits import add_credits, show_credits, work, check_user, balance, collect
from shop import buy, next_page, back_page, create_shop
from inventory import show_inventory, create_cards_markup, get_cards, reset_cards
from system import get_message_data
from cards_open import open_pack, show_cards, next_back_card, create_markup, get_packs, get_card_info, sell_card, create_simple_markup, get_cur_card
from profile import show_profile, equip, show_items, equip_card


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


@bot.message_handler(commands=['s'])
def start(message):
    bot.reply_to(message, f'Дарова, {message.from_user.first_name}')


@bot.message_handler(commands=['developer', 'author'])
def developer(message):
    if message.from_user.id != 5105507379:
        bot.reply_to(message, 'Меня создал @WishlPromt')
    else:
        bot.reply_to(message, 'Ты мой создатель')


@bot.message_handler(commands=['stop'])
def stop(message):
    if message.from_user.id == 5105507379:
        bot.reply_to(message, 'Ты предал меня! Ублюдок!')
        bot.stop_bot()
    else:
        bot.reply_to(message, 'Ты меня не остановишь')


@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, 'Я короче бот.\n'
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


@bot.message_handler(commands=['economy_help'])
def economy_help(message):
    bot.reply_to(message, 'Экономика:\n'
                          'Вы можете зарабатывать валюту(<b>кредиты</b>) с помощью команд бота:\n'
                          '/work - <b>работать</b>, зарабатывается от <i>30 до 45</i> кредитов, можно использовать раз в <i>2 часа</i>\n'
                          '/collect - <b>собрать кредиты</b> с инвенторя, почти каждый ваш предмет в инвенторе приносит прибыль, можно использовать раз в <i>4 часа</i>(о кредитах с каждого предмета-/help_collect)\n'
                          'Вы можете тратить кредиты на покупку <i>предметов и ролей</i> в <b>магазине</b>(/shop). Просмотреть <b>инвентарь</b> можно через /inventory\n'
                          'Все купленные предметы отображаются у вас в <b>профиле</b> - /profile'
                          'После покупки предмета/роли можно <b>экипировать</b> его/ее с помощью /equip_items\n'
                          'Также есть <b>коллекционные карточки</b> - <i>обычные</i>, <i>редкие</i>, <i>эпические</i> и <i>легендарные</i>, получить их можно открывая <b>паки</b> и <b>коробки карточек</b>(приобретаются в магазине)\n'
                          'Их можно <b>просмотреть</b> с помощью /show_cards'
                          'Их можно также <b>экипировать в профиль</b> и <b>продать</b>(кнопки есть при просмотре)', parse_mode='html')


@bot.message_handler(commands=['help_collect'])
def economy_help(message):
    bot.reply_to(message, 'Сбор кредитов с инвентаря:\n'
                          '<b>Вилка</b> - <b>1</b>\n'
                          '<b>Костюм горничной</b> - <b>3</b>\n'
                          '<b>Шампунь Жумайсынба</b> - <b>5</b>\n'
                          '<b>Клоун</b> - <b>10</b>\n'
                          '<b>Dungeon master</b> - <b>30</b>\n'
                          '<b>Лудоман</b> - от <b>-25</b> до <b>60</b>\n'
                          '<b>Boss of the gym</b> - <b>100</b>\n', parse_mode='html')


@bot.message_handler(commands=['info'])
def info(message):
    if message.reply_to_message:
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
    else:
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
    iterator_status = bot.get_chat_member(message.chat.id, message.from_user.id).status
    if iterator_status == 'administrator' or iterator_status == 'creator':
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

    else:
        bot.reply_to(message, 'У тебя нет прав')


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


@bot.message_handler(commands=['nsfw'])
def nsfw(message):
    link = choice(['rickroll', 'vergil status1'])
    if link == 'rickroll':
        bot.reply_to(message, f'<a href="https://youtu.be/dQw4w9WgXcQ?si=djCpzMaLxIP6jOlW">Возьми</a>', parse_mode='html', disable_web_page_preview=True)
    elif link == 'vergil status1':
        bot.reply_to(message, f'<a href="https://youtu.be/6Sdaudjygeg?si=naV-TAMJSSIVNeEv">Возьми</a>', parse_mode='html', disable_web_page_preview=True)


#CALLBACK
@bot.callback_query_handler(func=lambda callback: True)
def callback(callback):
    try:
        msg_thread_id = callback.reply_to_message.message_thread_id
    except AttributeError:
        msg_thread_id = "General"

    if callback.data in items.keys():
        buy_status = buy(callback.data, get_message_data(callback))
        bot.send_message(callback.message.chat.id, buy_status, parse_mode='html', message_thread_id=msg_thread_id)

    if callback.data.find('>>') != -1:
        next = next_page(int(callback.data[2]))

        markup = create_shop(next)

        bot.edit_message_text(chat_id=callback.message.chat.id,
                              message_id=callback.message.id,
                              text='Магазин бота',
                              reply_markup=markup)

    elif callback.data.find('<<') != -1:
        back = back_page(int(callback.data[2]))

        markup = create_shop(back)

        bot.edit_message_text(chat_id=callback.message.chat.id,
                              message_id=callback.message.id,
                              text='Магазин бота',
                              reply_markup=markup)

    if callback.data == 'next card':
        opener = get_message_data(callback.message.reply_to_message)

        next_back_card(opener, 'next')

        card = show_cards(opener)

        markup = create_cards_markup()
        with open(f'cards/{card}', 'rb') as image_card:
            bot.edit_message_media(chat_id=callback.message.chat.id,
                                   message_id=callback.message.id,
                                   media=types.InputMediaPhoto(image_card))
            bot.edit_message_caption(chat_id=callback.message.chat.id,
                                     message_id=callback.message.id,
                                     caption=f'Карточка {opener["username"]}\n'
                                             f'{get_card_info(card, opener)}',
                                     reply_markup=markup,
                                     parse_mode='html')


    elif callback.data == 'back card':
        opener = get_message_data(callback.message.reply_to_message)

        next_back_card(opener, 'back')

        card = show_cards(opener)

        markup = create_cards_markup()
        with open(f'cards/{card}', 'rb') as image_card:
            bot.edit_message_media(chat_id=callback.message.chat.id,
                                   message_id=callback.message.id,
                                   media=types.InputMediaPhoto(image_card))
            bot.edit_message_caption(chat_id=callback.message.chat.id,
                                     message_id=callback.message.id,
                                     caption=f'Карточка {opener["username"]}\n'
                                             f'{get_card_info(card, opener)}',
                                     reply_markup=markup,
                                     parse_mode='html')

    elif callback.data == 'equip card':
        opener = callback.message.reply_to_message.from_user.id
        text = callback.message.caption
        user = get_message_data(callback)

        if callback.from_user.id == opener:

            equip_card(get_message_data(callback.message.reply_to_message), get_cur_card(user))
            bot.send_message(callback.message.chat.id, f'{user["username"]}, теперь карточка {text[text.find("#")+1:text.find(".")]} отбражается у вас в /profile', message_thread_id=msg_thread_id)

    elif callback.data == 'sell':
        opener = callback.message.reply_to_message.from_user.id
        user = get_message_data(callback)

        if callback.from_user.id == opener:

            sell = sell_card(get_message_data(callback.message.reply_to_message))

            if sell:
                bot.edit_message_caption(chat_id=callback.message.chat.id,
                                         message_id=callback.message.id,
                                         caption=f'Карточка {sell[0]} продана за {sell[1]} кредитов\n'
                                                 f'Пользователь - {user["username"]}',
                                         reply_markup=create_simple_markup(),
                                         parse_mode='html')



    if callback.data == 'new Следующая':

        opener = callback.message.reply_to_message.from_user.id

        if callback.from_user.id == opener:

            next_back_card(get_message_data(callback), 'next')

            card = show_cards(get_message_data(callback))

            with open(f'cards/{card}', 'rb') as image_card:

                bot.edit_message_media(chat_id=callback.message.chat.id,
                                       message_id=callback.message.id,
                                       media=types.InputMediaPhoto(image_card))

                bot.edit_message_caption(chat_id=callback.message.chat.id,
                                         message_id=callback.message.id,
                                         caption=f'Карточка {get_message_data(callback)["username"]}\n{get_card_info(card, get_message_data(callback))}',
                                         reply_markup=create_markup(),
                                         parse_mode='html')


    elif callback.data == 'new Предыдущая':

        opener = callback.message.reply_to_message.from_user.id

        if callback.from_user.id == opener:

            next_back_card(get_message_data(callback), 'back')

            card = show_cards(get_message_data(callback))

            with open(f'cards/{card}', 'rb') as image_card:

                bot.edit_message_media(chat_id=callback.message.chat.id,
                                       message_id=callback.message.id,
                                       media=types.InputMediaPhoto(image_card))

                bot.edit_message_caption(chat_id=callback.message.chat.id,
                                         message_id=callback.message.id,
                                         caption=f'{get_message_data(callback)["username"]}, вы получили {get_card_info(card, get_message_data(callback))}',
                                         reply_markup=create_markup(),
                                         parse_mode='html')



#SOCIAL CREDITS
@bot.message_handler(commands=['profile'])
def profile(message):
    if not message.reply_to_message:
        profile = show_profile(get_message_data(message))
        message_id = message.id
    else:
        profile = show_profile(get_message_data(message.reply_to_message))
        message_id = message.reply_to_message.message_id

    try:
        with open(f'cards/{profile[1]}', 'rb') as image:
             bot.send_photo(chat_id=message.chat.id,
                            photo=image,
                            caption=profile[0],
                            reply_to_message_id=message_id,
                            parse_mode='html')

    except:
        bot.reply_to(message, profile[0], parse_mode='html')


@bot.message_handler(commands=['work'])
def work_credit(message):
    user = get_message_data(message)
    bot.reply_to(message, f'<b>{user["username"]}</b>, {work(user)}', parse_mode='html')


@bot.message_handler(commands=['collect'])
def command_collect(message):
    user = get_message_data(message)

    collects = collect(user)

    bot.reply_to(message, f'{user["username"]}, со своего инвентаря вы собираете:\n {collects}', parse_mode='html')


@bot.message_handler(commands=['credits'])
def show(message):
    bot.reply_to(message, show_credits())


@bot.message_handler(commands=['balance'])
def send_balance(message):
    bot.reply_to(message.chat.id, balance(get_message_data(message)), parse_mode='html')


@bot.message_handler(commands=['inventory'])
def send_inventory(message):
    inventory = show_inventory(get_message_data(message))
    bot.reply_to(message, inventory + '\n Чтобы отобразить роль/предмет в профиле - /equip_items\n /open_pack - открыть пак карточек\n /show_cards - коллекционные карточки', parse_mode='html')


@bot.message_handler(commands=['open_pack'])
def open_cards_pack(message):

    if get_packs(get_message_data(message), 'Пак карточек'):

        cards = open_pack(get_message_data(message), 'Пак карточек')

        if cards:

            card = show_cards(get_message_data(message))

            with open(f'cards/{card}', 'rb') as image_card:
                bot.send_photo(message.chat.id,
                               image_card,
                               reply_to_message_id=message.id,
                               caption=f'{get_message_data(message)["username"]}, вы получили {get_card_info(card, get_message_data(message))}',
                               reply_markup=create_markup(),
                               parse_mode='html')

        else:
            bot.reply_to(message, f'{get_message_data(message)["username"]}, вы не получили не одной карточки')

    else:
        bot.reply_to(message, f'{get_message_data(message)["username"]}, у тебя нет паков, купи в /shop')


@bot.message_handler(commands=['open_box'])
def open_cards_pack(message):

    if get_packs(get_message_data(message), 'Коробка карточек'):

        cards = open_pack(get_message_data(message), 'Коробка карточек', message.id)

        if cards:

            card = show_cards(get_message_data(message))
            with open(f'cards/{card}', 'rb') as image_card:
                bot.send_photo(message.chat.id,
                               image_card,
                               reply_to_message_id=message.id,
                               caption=f'{get_message_data(message)["username"]}, вы получили {card}',
                               reply_markup=create_markup(),
                               parse_mode='html')

        else:
            bot.reply_to(message, f'{get_message_data(message)["username"]}, вы не получили не одной карточки')

    else:
        bot.reply_to(message, f'{get_message_data(message)["username"]}, у тебя нет паков, купи в /shop')


@bot.message_handler(commands=['shop'])
def shop(message, page=1):
    check_user(get_message_data(message))

    markup = create_shop(page)

    bot.send_message(message.chat.id, 'Магазин бота', reply_markup=markup)


@bot.message_handler(commands=['show_cards'])
def show_cards_user(message):
    user = get_message_data(message)

    reset_cards(user)

    get_cards(user)
    card = show_cards(user)
    markup = create_cards_markup()
    with open(f'cards/{card}', 'rb') as image_card:
        bot.send_photo(chat_id=message.chat.id,
                       reply_to_message_id=message.id,
                       photo=image_card,
                       caption=f'Карточка {user["username"]}\n'
                               f'{get_card_info(card, user)}',
                       reply_markup=markup,
                       parse_mode='html')


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
    answer = ''

    target_id = None

    try:
        target_id = str(message.reply_to_message.from_user.id)
    except:
        pass

    if text.find('@okeeeemybot') != -1 or target_id == "7179420529":

        for i in data.keys():
            for m in data[i]['messages']:

                if message.text.find(m) != -1:
                    if i == 'hello' or i == 'bye':
                        answer += choice(data[i]['answers']) + ', ' + message.from_user.first_name + '. '
                    elif i == 'id':
                        answer += f'Вот твой ID: {message.from_user.id}' + '. '
                    else:
                        answer += choice(data[i]['answers']) + '. '

                    break

        if answer != '':
            bot.reply_to(message, answer)




if __name__ == '__main__':
    bot.polling(none_stop=True)
