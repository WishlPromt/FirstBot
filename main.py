import telebot
import requests
from telebot import types
from random import choice, randint
import json, time, os
from social_credits import add_credits, dashboard, work, check_user, balance, collect
from shop import buy, next_page, back_page, create_shop, get_max_pages
from inventory import show_inventory, create_cards_markup, get_cards, reset_cards, get_inventory
from system import get_message_data, generate_id
from cards_open import open_pack, show_cards, next_back_card, create_markup, get_packs, get_card_info, sell_card, create_simple_markup, get_cur_card, create_markup_photo
from profile import show_profile, equip, equip_card
import items_using


#JSON
with open('base.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


with open('items.json', 'r', encoding='utf-8') as file:
    items = json.load(file)


def load_chats_base():
    with open('chats_base.json', 'r', encoding='utf-8') as file:
        base = json.load(file)
        return base


#VARIABLES
games = None
org = None
players = []
action: str
tag: str
ignore_symbols = ',."\'{}[]()!#$%^&*№;:?\\|/'


bot = telebot.TeleBot('7179420529:AAEOXaN8vYV5OVd4_OYDy7tK6hHGWxnTjL8')

@bot.message_handler(commands=['start', 'hello'])
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
                          '/collect\n'
                          '/shop\n'
                          '/balance\n'
                          '/profile'
                          '/equip\n'
                          '/show_cards'
                          '/show_card'
                          'Мини-игры:\n'
                          '/russian_roulette\n', parse_mode='html')


@bot.message_handler(commands=['economy_help'])
def economy_help(message):
    bot.reply_to(message, 'Экономика:\n'
                          'Вы можете зарабатывать валюту(<b>кредиты</b>) с помощью команд бота:\n'
                          '/work - <b>работать</b>, зарабатывается от <i>30 до 45</i> кредитов, можно использовать раз в <i>2 часа</i>\n'
                          '/collect - <b>собрать кредиты</b> с инвенторя, почти каждый ваш предмет в инвенторе приносит прибыль, можно использовать раз в <i>4 часа</i>(о кредитах с каждого предмета-/help_collect)\n'
                          'Вы можете тратить кредиты на покупку <i>предметов и ролей</i> в <b>магазине</b>(/shop). Просмотреть <b>инвентарь</b> можно через /inventory\n'
                          'Все купленные предметы отображаются у вас в <b>профиле</b> - /profile'
                          'После покупки предмета/роли можно <b>экипировать</b> его/ее с помощью /equip\n'
                          'Также есть <b>коллекционные карточки</b> - <i>обычные</i>, <i>редкие</i>, <i>эпические</i> и <i>легендарные</i>, получить их можно открывая <b>паки</b> и <b>коробки карточек</b>(приобретаются в магазине)\n'
                          'Их можно <b>просмотреть</b> с помощью /show_cards'
                          'Их можно также <b>экипировать в профиль</b> и <b>продать</b>(кнопки есть при просмотре)', parse_mode='html')


@bot.message_handler(commands=['help_collect'])
def collect_help(message):
    bot.reply_to(message, 'Сбор кредитов с инвентаря:\n'
                          '<b>Вилка</b> - <b>1</b>\n'
                          '<b>Костюм горничной</b> - <b>3</b>\n'
                          '<b>Шампунь Жумайсынба</b> - <b>5</b>\n'
                          '<b>Клоун</b> - <b>10</b>\n'
                          '<b>Сборник анекдотов</b> - <b>5</b> - <i>Генерирует анекдоты - /rofl</i>\n'
                          '<b>Dungeon master</b> - <b>30</b> - <i>Позволяет делать /fisting пользователям</i>\n'
                          '<b>Лудоман</b> - от <b>-25</b> до <b>60</b>\n'
                          '<b>Любитель аниме-тянок</b> - <b>10</b> - <i>Добавляет 25% карточек в паки</i>\n'
                          '<b>Motivated</b> - <b>10</b> - <i>Увеличивает стоимость продажи карт на 50%</i>\n'
                          '<b>Палка-уебалка</b> - <b>45</b>\n'
                          '<b>Липовый модератор</b> - <b>100</b> - <i>Уменьшает время между использованием /work и /collect на 25%</i>\n'
                          '<b>Boss of the gym</b> - <b>150</b> - <i>/work дает на 50% кредитов больше</i>\n', parse_mode='html')


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
                cause = ''
                args = message.text.split()[1:]
                if args:
                    try:
                        duration = int(args[0])
                        for arg in args[1:]:
                            cause += arg + ' '
                    except ValueError:
                        bot.reply_to(message, "Неправильный формат времени.")
                        return
                    if duration < 1:
                        bot.reply_to(message, "Время должно быть положительным числом.")
                        return
                    if duration > 604800:
                        bot.reply_to(message, "Максимальное время - 1 неделя.")
                        return
                if cause:
                    bot.restrict_chat_member(chat_id, user_id, until_date=time.time() + duration * 60)
                    bot.reply_to(message.reply_to_message,
                                 f"Пользователь {message.reply_to_message.from_user.username} замучен на {duration} минут.\n"
                                 f"Причина: {cause}")
                else:
                    bot.reply_to(message, 'Без причины мут не дам')
        else:
            bot.reply_to(message,
                         "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите замутить.")

    else:
        bot.reply_to(message, 'У тебя нет прав')


@bot.message_handler(commands=['unmute'])
def unmute(message):
    if message.reply_to_message:
        iterator_status = bot.get_chat_member(message.chat.id, message.from_user.id).status
        if iterator_status == 'administrator' or iterator_status == 'creator':
            chat_id = message.chat.id
            user_id = message.reply_to_message.from_user.id
            bot.restrict_chat_member(chat_id, user_id, can_send_messages=True, can_send_media_messages=True,
                                     can_send_other_messages=True, can_add_web_page_previews=True)
            bot.reply_to(message, f"Пользователь {message.reply_to_message.from_user.username} размучен.")
        else:
            bot.send_message(message, 'У тебя нет прав')
    else:
        bot.reply_to(message,
                     "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите размутить.")


@bot.message_handler(commands=['ban'])
def ban(message):
    base = load_chats_base()

    if message.reply_to_message:
        iterator_status = bot.get_chat_member(message.chat.id, message.from_user.id).status
        if iterator_status == 'administrator' or iterator_status == 'creator':
            message = message.reply_to_message
            id = str(message.from_user.id)
            username = message.from_user.username
            chat_id = str(message.chat.id)
            if id not in base[chat_id]['ban_blacklist']:
                bot.ban_chat_member(chat_id, int(id))
                base[chat_id]['banned_users'][username] = id
                bot.send_message(chat_id, f'Пользователь {username} забанен')
            else:
                bot.send_message(chat_id, f'Пользователя нельзя забанить')
        else:
            bot.send_message(message, 'У тебя нет прав')


@bot.message_handler(commands=['nsfw'])
def nsfw(message):
    link = choice(['rickroll', 'vergil status1'])
    if link == 'rickroll':
        bot.reply_to(message, f'<a href="https://youtu.be/dQw4w9WgXcQ?si=djCpzMaLxIP6jOlW">Возьми</a>', parse_mode='html', disable_web_page_preview=True)
    elif link == 'vergil status1':
        bot.reply_to(message, f'<a href="https://youtu.be/6Sdaudjygeg?si=naV-TAMJSSIVNeEv">Возьми</a>', parse_mode='html', disable_web_page_preview=True)


@bot.message_handler(commands=['get_chat'])
def get_chat(message):
    bot.reply_to(message, message.chat.id)


#CALLBACK
@bot.callback_query_handler(func=lambda callback: True)
def callback(callback):

    if callback.data in items.keys():
        buy_status = buy(callback.data, get_message_data(callback, callback.message.chat.id))
        bot.send_message(callback.message.chat.id, buy_status, parse_mode='html')

    if callback.data.find('>>') != -1:
        next = next_page(int(callback.data[2]), get_max_pages(get_message_data(callback, callback.message.chat.id)))

        markup = create_shop(next, get_message_data(callback, callback.message.chat.id))

        bot.edit_message_text(chat_id=callback.message.chat.id,
                              message_id=callback.message.id,
                              text='Магазин бота',
                              reply_markup=markup)

    elif callback.data.find('<<') != -1:
        back = back_page(int(callback.data[2]), get_max_pages(get_message_data(callback, callback.message.chat.id)))

        markup = create_shop(back, get_message_data(callback, callback.message.chat.id))

        bot.edit_message_text(chat_id=callback.message.chat.id,
                              message_id=callback.message.id,
                              text='Магазин бота',
                              reply_markup=markup)

    if callback.data.find('equip.') != -1:
        item = callback.data[callback.data.find('.')+1:]
        user = get_message_data(callback, callback.message.chat.id)

        equip_status = equip(user, item)
        print(equip_status)

        bot.send_message(callback.message.chat.id, equip_status, parse_mode='html')

    if callback.data in ['regular', 'rare', 'epic', 'legendary']:
        from cards_open import add_new_card
        ids = os.listdir(f'cards/{callback.data}')
        id = ids[0]
        id = generate_id(ids, id, callback.data)

        photo = callback.message.photo[-1]
        file_info = bot.get_file(photo.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        save_path = f'cards/{callback.data}/{id}.jpg'
        with open(save_path, 'wb') as new_file:
            new_file.write(downloaded_file)
            add_new_card(id+'.jpg', callback.data)
        bot.reply_to(callback.message.reply_to_message, f'Карточка добавлена под id {id}.')

    if callback.data in ['open Пак карточек', 'open Коробка карточек', 'open Anime pack', 'open Motivation pack', 'open Dungeon pack']:
        message = callback.message.reply_to_message
        user = get_message_data(message, callback.message.chat.id)
        item = callback.data[callback.data.find(' ')+1:]

        if str(callback.from_user.id) == user['id']:
            if get_packs(user, item):
                bot.reply_to(message, f'{user["username"]} открывает {item}')
                cards = open_pack(user, item)

                if cards:

                    card = show_cards(user)

                    with open(f'cards/{card}', 'rb') as image_card:
                        if card[card.find('.')+1:] != 'gif':
                            bot.send_photo(message.chat.id,
                                           image_card,
                                           reply_to_message_id=message.id,
                                           caption=f'{user["username"]}, вы получили {get_card_info(card, user)}',
                                           reply_markup=create_markup(),
                                           parse_mode='html')
                        else:
                            bot.send_animation(message.chat.id,
                                               image_card,
                                               reply_to_message_id=message.id,
                                               caption=f'{user["username"]}, вы получили {get_card_info(card, user)}',
                                               reply_markup=create_markup(),
                                               parse_mode='html')

                else:
                    bot.reply_to(message, f'{get_message_data(message, callback.message.chat.id)["username"]}, вы не получили ни одной карточки')

            else:
                bot.reply_to(message, f'{get_message_data(message, callback.message.chat.id)["username"]}, у тебя нет паков, купи в /shop')

    if callback.data == 'next card':
        opener = get_message_data(callback.message.reply_to_message, callback.message.chat.id)

        next_back_card(opener, 'next')

        card = show_cards(opener)

        markup = create_cards_markup()
        with open(f'cards/{card}', 'rb') as image_card:
            if card[card.find('.')+1:] != 'gif':
                bot.edit_message_media(chat_id=callback.message.chat.id,
                                       message_id=callback.message.id,
                                       media=types.InputMediaPhoto(image_card))
            else:
                bot.edit_message_media(chat_id=callback.message.chat.id,
                                       message_id=callback.message.id,
                                       media=types.InputMediaAnimation(image_card))

            bot.edit_message_caption(chat_id=callback.message.chat.id,
                                     message_id=callback.message.id,
                                     caption=f'Карточка {opener["username"]}\n'
                                             f'{get_card_info(card, opener)}',
                                     reply_markup=markup,
                                     parse_mode='html')

    elif callback.data == 'back card':
        opener = get_message_data(callback.message.reply_to_message, callback.message.chat.id)

        next_back_card(opener, 'back')

        card = show_cards(opener)

        markup = create_cards_markup()
        with open(f'cards/{card}', 'rb') as image_card:
            if card[card.find('.')+1:] != 'gif':
                bot.edit_message_media(chat_id=callback.message.chat.id,
                                       message_id=callback.message.id,
                                       media=types.InputMediaPhoto(image_card))
            else:
                bot.edit_message_media(chat_id=callback.message.chat.id,
                                       message_id=callback.message.id,
                                       media=types.InputMediaAnimation(image_card))

            bot.edit_message_caption(chat_id=callback.message.chat.id,
                                     message_id=callback.message.id,
                                     caption=f'Карточка {opener["username"]}\n'
                                             f'{get_card_info(card, opener)}',
                                     reply_markup=markup,
                                     parse_mode='html')

    elif callback.data == 'equip card':
        opener = callback.message.reply_to_message.from_user.id
        text = callback.message.caption
        user = get_message_data(callback, callback.message.chat.id)

        if callback.from_user.id == opener:

            equip_card(get_message_data(callback.message.reply_to_message, callback.message.chat.id), get_cur_card(user))
            bot.send_message(callback.message.chat.id, f'{user["username"]}, теперь карточка {text[text.find("#")+1:text.find(".")]} отбражается у вас в /profile')

    elif callback.data == 'sell':
        opener = callback.message.reply_to_message.from_user.id
        user = get_message_data(callback, callback.message.chat.id)

        if callback.from_user.id == opener:

            sell = sell_card(get_message_data(callback.message.reply_to_message, callback.message.chat.id))

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

            next_back_card(get_message_data(callback, callback.message.chat.id), 'next')

            card = show_cards(get_message_data(callback, callback.message.chat.id))

            with open(f'cards/{card}', 'rb') as image_card:
                if card[card.find('.')+1:] != 'gif':
                    bot.edit_message_media(chat_id=callback.message.chat.id,
                                           message_id=callback.message.id,
                                           media=types.InputMediaPhoto(image_card))
                else:
                    bot.edit_message_media(chat_id=callback.message.chat.id,
                                           message_id=callback.message.id,
                                           media=types.InputMediaAnimation(image_card))

                bot.edit_message_caption(chat_id=callback.message.chat.id,
                                         message_id=callback.message.id,
                                         caption=f'Карточка {get_message_data(callback, callback.message.chat.id)["username"]}\n{get_card_info(card, get_message_data(callback, callback.message.chat.id))}',
                                         reply_markup=create_markup(),
                                         parse_mode='html')

    elif callback.data == 'new Предыдущая':

        opener = callback.message.reply_to_message.from_user.id

        if callback.from_user.id == opener:

            next_back_card(get_message_data(callback, callback.message.chat.id), 'back')

            card = show_cards(get_message_data(callback, callback.message.chat.id))

            with open(f'cards/{card}', 'rb') as image_card:
                if card[card.find('.')+1:] != 'gif':
                    bot.edit_message_media(chat_id=callback.message.chat.id,
                                           message_id=callback.message.id,
                                           media=types.InputMediaPhoto(image_card))
                else:
                    bot.edit_message_media(chat_id=callback.message.chat.id,
                                           message_id=callback.message.id,
                                           media=types.InputMediaAnimation(image_card))

                bot.edit_message_caption(chat_id=callback.message.chat.id,
                                         message_id=callback.message.id,
                                         caption=f'{get_message_data(callback, callback.message.chat.id)["username"]}, вы получили {get_card_info(card, get_message_data(callback, callback.message.chat.id))}',
                                         reply_markup=create_markup(),
                                         parse_mode='html')


#SOCIAL CREDITS
@bot.message_handler(commands=['profile'])
def profile(message):

    if not message.reply_to_message:
        profile = show_profile(get_message_data(message, message.chat.id))
        message_id = message.id

    else:
        profile = show_profile(get_message_data(message.reply_to_message, message.chat.id))
        message_id = message.reply_to_message.message_id

    try:
        with open(f'cards/{profile[1]}', 'rb') as image:
            if profile[1][profile[1].find('.')+1:] != 'gif':
                bot.send_photo(chat_id=message.chat.id,
                               photo=image,
                               caption=profile[0],
                               reply_to_message_id=message_id,
                               parse_mode='html')
            else:
                bot.send_animation(chat_id=message.chat.id,
                                   animation=image,
                                   caption=profile[0],
                                   reply_to_message_id=message_id,
                                   parse_mode='html')

    except:
        bot.reply_to(message, profile[0], parse_mode='html')


@bot.message_handler(commands=['work'])
def work_credit(message):
    user = get_message_data(message, message.chat.id)
    bot.reply_to(message, f'<b>{user["username"]}</b>, {work(user)}', parse_mode='html')


@bot.message_handler(commands=['collect'])
def command_collect(message):
    user = get_message_data(message, message.chat.id)

    collects = collect(user)

    bot.reply_to(message, f'{user["username"]}, со своего инвентаря вы собираете:\n {collects}', parse_mode='html')


@bot.message_handler(commands=['dashboard'])
def show_dashboard(message):
    bot.send_message(message.chat.id, dashboard(message.chat.id), parse_mode='html')


@bot.message_handler(commands=['balance'])
def send_balance(message):
    bot.reply_to(message, balance(get_message_data(message, message.chat.id)), parse_mode='html')


@bot.message_handler(commands=['inventory'])
def send_inventory(message):
    inventory = show_inventory(get_message_data(message, message.chat.id))
    bot.reply_to(message, inventory + '\n Чтобы отобразить роль/предмет в профиле - /equip\n /open_pack - открыть пак карточек\n /show_cards - коллекционные карточки', parse_mode='html')


@bot.message_handler(commands=['open_pack'])
def open_cards_pack(message):
    user = get_message_data(message, message.chat.id)

    packs = []
    for i in ['Пак карточек', 'Коробка карточек', 'Anime pack', 'Motivation pack', 'Dungeon pack']:
        packs.append(get_packs(user, i))

    markup = types.InlineKeyboardMarkup()

    btn_pack = types.InlineKeyboardButton(f'Пак карточек - {packs[0]}', callback_data='open Пак карточек')
    btn_box = types.InlineKeyboardButton(f'Коробка карточек - {packs[1]}', callback_data='open Коробка карточек')
    btn_anime_pack = types.InlineKeyboardButton(f'Anime pack - {packs[2]}', callback_data='open Anime pack')
    btn_motivation_pack = types.InlineKeyboardButton(f'Motivation pack - {packs[3]}', callback_data='open Motivation pack')
    btn_dungeon_pack = types.InlineKeyboardButton(f'Dungeon pack - {packs[4]}',
                                                     callback_data='open Dungeon pack')

    if packs[0]:
        markup.add(btn_pack)
    if packs[1]:
        markup.add(btn_box)
    if packs[2]:
        markup.add(btn_anime_pack)
    if packs[3]:
        markup.add(btn_motivation_pack)
    if packs[4]:
        markup.add(btn_dungeon_pack)

    if packs == [False, False, False, False]:
        bot.reply_to(message, 'У тебя нет паков, купи их в /shop')

    else:
        bot.reply_to(message, 'Открыть паки', reply_markup=markup)


@bot.message_handler(commands=['shop'])
def shop(message, page=1):
    check_user(get_message_data(message, message.chat.id))

    markup = create_shop(page, get_message_data(message, message.chat.id))

    bot.reply_to(message, 'Магазин бота', reply_markup=markup)


@bot.message_handler(commands=['show_cards'])
def show_cards_user(message):
    user = get_message_data(message, message.chat.id)

    reset_cards(user)

    get_cards(user)
    card = show_cards(user)
    markup = create_cards_markup()
    with open(f'cards/{card}', 'rb') as image_card:
        if card[card.find('.')+1:] != 'gif':
            bot.send_photo(chat_id=message.chat.id,
                           reply_to_message_id=message.id,
                           photo=image_card,
                           caption=f'Карточка {user["username"]}\n'
                                   f'{get_card_info(card, user)}',
                           reply_markup=markup,
                           parse_mode='html')
        else:
            bot.send_animation(chat_id=message.chat.id,
                               reply_to_message_id=message.id,
                               animation=image_card,
                               caption=f'Карточка {user["username"]}\n'
                                       f'{get_card_info(card, user)}',
                               reply_markup=markup,
                               parse_mode='html')


from cards_open import card_names
@bot.message_handler(commands=card_names)
def show_card(message):

    card = ''
    for dir in os.listdir('cards'):
        for c in os.listdir(f'cards/{dir}'):
            if message.text.find('@') != -1:
                if message.text[1:message.text.find('@')] == c[0:c.find('.')]:
                    card = f'{dir}/{c}'
            else:
                if message.text[1:] == c[0:c.find('.')]:
                    card = f'{dir}/{c}'

    if not card:
        bot.reply_to(message, 'Карта не найдена')
        return

    with open(f'cards/{card}', 'rb') as image_card:
        if card[card.find('.') + 1:] != 'gif':
            bot.send_photo(chat_id=message.chat.id,
                           reply_to_message_id=message.id,
                           photo=image_card,
                           caption=f'Карточка {card}',
                           parse_mode='html')
        else:
            bot.send_animation(chat_id=message.chat.id,
                               reply_to_message_id=message.id,
                               animation=image_card,
                               caption=f'Карточка {card}',
                               parse_mode='html')


@bot.message_handler(commands=['add_card'])
def preposition(message):
    bot.reply_to(message, 'Ответьте на мое сообщение карточкой, которую хотите добавить, я отправлю ее разработчику')


@bot.message_handler(content_types=['photo'])
def preposition_card(message):
    if message.reply_to_message:

        if message.reply_to_message.text == 'Ответьте на мое сообщение карточкой, которую хотите добавить, я отправлю ее разработчику' and message.reply_to_message.from_user.id == 7179420529:

            photo = message.photo[-1]
            file_info = bot.get_file(photo.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            name = str(message.from_user.username) + str(randint(-1000, 1000)) + str(randint(-1000, 1000)) + str(randint(-1000, 1000))

            with open(f'cards/preposition/{name}.jpg', 'wb') as new_file:
                print(new_file)
                new_file.write(downloaded_file)


@bot.message_handler(commands=['show_prep'])
def show_prep(message):
    if message.from_user.id == 5105507379:
        for image in os.listdir('cards/preposition/'):
            with open(f'cards/preposition/{image}', 'rb') as card:
                bot.send_photo(chat_id=message.chat.id,
                               photo=card,
                               reply_to_message_id=message.id,
                               caption=f'Выберите редкость для карты - {image}',
                               reply_markup=create_markup_photo())


@bot.message_handler(commands=['use'])
def use_item(message):
    bot.reply_to(message, 'В разработке')

@bot.message_handler(commands=['equip'])
def equip_item(message):
    user = get_message_data(message, message.chat.id)
    inventory = get_inventory(user)

    markup = types.InlineKeyboardMarkup()

    for item in inventory:
        button = types.InlineKeyboardButton(item, callback_data=f'equip.{item}')
        markup.add(button)

    bot.reply_to(message, 'Экипировка предметов и ролей', reply_markup=markup)


@bot.message_handler(commands=['fisting'])
def fisting(message):
    get_master = False
    for role in ['Dungeon master', 'Full master']:
        if items_using.get_item(get_message_data(message, message.chat.id), role):
            get_master = True

    if get_master:
        master = get_message_data(message, message.chat.id)['username']
        if message.reply_to_message:
            slave = get_message_data(message.reply_to_message, message.chat.id)['username']
        else:
            slave = 'Воздух'
        text = choice([f'{master} сделал фистинг {slave}',
                      f'{slave} был пронзен мечом {master}',
                      f'{master} посвятил {slave} в Dungeon Master\'ы'])
        bot.send_message(message.chat.id, text)
    else:
        bot.reply_to(message, 'Ты не master, поэтому недостоин это делать')


@bot.message_handler(commands=['rofl'])
def rofl(message):
    if items_using.get_item(get_message_data(message, message.chat.id), 'Сборник анекдотов'):
        with open('rofls.json', 'r', encoding='utf-8') as file:
            base = json.load(file)['rofls']
        bot.reply_to(message, choice(base))
    else:
        bot.reply_to(message, 'У тебя нет сборника анекдотов')


#GAMES
@bot.message_handler(commands=[])
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
        bot.reply_to(message, 'Игру то начни')


@bot.message_handler(commands=[])
def start_game(message):
    global players, games, org
    if len(players) < 2:
        bot.reply_to(message, 'Не набралось достаточное кол-во игроков. Игра отменяется')
        end_game(message)

    starter = message.from_user.id
    for p in players:
        if p['org'] == True:
            org = p['id']
    if games == 'roul':
        if starter == org:

            bot.reply_to(message, 'Русская рулетка началась!')
            for r in range(3):
                if len(players) > 1:
                    time.sleep(3)
                    bot.send_message(message.chat.id, f'РАУНД {r+1}!')
                    round(message)

            if len(players) == 1:

                time.sleep(2)

                bot.send_message(message.chat.id, f'{players[0]["username"]} - Победитель! Он получает 100 кредитов!')
                add_credits(get_message_data(message, message.chat.id), 100)

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
        bot.reply_to(message, 'Игра завершена')
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


@bot.message_handler(content_types=['new_chat_members'])
def new_member(message):
    greetings = [f'Welcome to the club, buddy!',
                 f'Приветствуем в этом чате! Мы тебя забулим, не против?',
                 f'Дарова!']
    bot.reply_to(message, choice(greetings))


if __name__ == '__main__':
    bot.infinity_polling(timeout=90, long_polling_timeout=5, interval=5)
