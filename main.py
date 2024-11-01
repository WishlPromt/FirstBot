import telebot
from telebot import types
from random import choice, randint
import json, time
from social_credits import add_credits, show_credits, work, check_user


#JSON
with open('base.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


def save_base():
    file = open('base.json', 'w', encoding='utf-8')
    json.dump(data, file, indent=4, ensure_ascii=False)
    file.close()



education_mode = False
math_mode = False
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
        bot.send_message(message.chat.id, 'Меня создал @AppleBox01')
    else:
        bot.send_message(message.chat.id, 'Ты мой создатель')


@bot.message_handler(commands=['stop'])
def developer(message):
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
                                      '/start\n'
                                      '/help\n'
                                      '/developer\n'
                                      '/info\n'
                                      '/education\n'
                                      '/finish\n'
                                      '/nsfw\n'
                                      '/work\n'
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


@bot.message_handler(commands=['math'])
def math(message):
    global math_mode
    if not education_mode:
        if not math_mode:
            math_mode = True
            bot.send_message(message.chat.id, 'Отправьте мне математическое выражение, я решу его... Наверное')
        else:
            bot.send_message(message.chat.id, 'Вы уже в режиме математики')
    else:
        bot.send_message(message.chat.id, 'Вы в режиме обучения')


@bot.message_handler(commands=['education'])
def education(message):
    global education_mode
    if not math_mode:
        if not education_mode:
            education_mode = True
            bot.send_message(message.chat.id, 'Обучение начато')
            bot.send_message(message.chat.id, 'Напишите "/choose"')
        else:
            bot.send_message(message.chat.id, 'Обучение уже начато')
    else:
        bot.send_message(message.chat.id, 'Вы в режиме математики')


@bot.message_handler(commands=['finish'])
def finish(message):
    global education_mode, action, math_mode
    if education_mode:
        education_mode = False
        action = ''
        bot.send_message(message.chat.id, 'Обучение завершено\nЕсли вы хотите продолжить обучение, напишите /education')

    elif math_mode:
        math_mode = False
        bot.send_message(message.chat.id, 'Вы вышли из режима математики')

    else:
        if message.from_user.id != 5105507379:
            bot.send_message(message.chat.id, 'Вы не вошли ни в один из режимов')
        else:
            bot.send_message(message.chat.id, 'Сначала войди в какой-нибудь режим, идиот!')


@bot.message_handler(commands=['choose'])
def choose(message):
    if education_mode:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Новый тег', callback_data='new_tag'))
        markup.add(types.InlineKeyboardButton('Редактировать тег', callback_data='edit_tag'))
        markup.add(types.InlineKeyboardButton('Закончить обучение', callback_data='finish'))
        bot.send_message(message.chat.id, 'Что вы хотите сделать?', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Режим обучения не включен')


@bot.callback_query_handler(func=lambda callback: True)
def callback(callback):

    if callback.data == 'new_tag':
        new_tag(callback.message)

    elif callback.data == 'edit_tag':
        edit_tag(callback.message)

    elif callback.data == 'rename_tag':
        rename(callback.message)

    elif callback.data == 'edit_messages':
        add_message(callback.message)

    elif callback.data == 'edit_answers':
        add_answers(callback.message)

    elif callback.data == 'finish':
        finish(callback.message)

    else:
        bot.send_message(callback.message.chat.id, 'Произошла ошибка')


#Режим обучения
@bot.message_handler(commands=['new tag'])
def new_tag(message):
    global action
    if education_mode:
        action = 'new tag'
        bot.send_message(message.chat.id, 'Напишите мне новый тег')
    else:
        bot.send_message(message.chat.id, 'Режим обучения не включен')


@bot.message_handler(commands=['edit tag'])
def edit_tag(message):
    global action
    if education_mode:
        action = 'edit tag'
        bot.send_message(message.chat.id,'Напишите тег, который хотите редактировать')
    else:
        bot.send_message(message.chat.id, 'Режим обучения не включен')


def rename(message):
    global action
    action = 'rename tag'
    bot.send_message(message.chat.id, 'Напишите новое название тега')


def add_message(message):
    global action
    action = 'add messages'
    bot.send_message(message.chat.id, 'Напишите сообщение или сообщения(через точку с запятой), на которые я должен буду давать ответ')


def add_answers(message):
    global action
    action = 'add answers'
    bot.send_message(message.chat.id, 'Напишите сообщение или сообщения(через точку с запятой), которые я должен буду писать в ответ')



@bot.message_handler(commands=['nsfw'])
def nsfw(message):
    bot.send_message(message.chat.id, "https://youtu.be/dQw4w9WgXcQ?si=djCpzMaLxIP6jOlW")


#SOCIAL CREDITS
@bot.message_handler(commands=['work'])
def work_credit(message):
    user = {'id': str(message.from_user.id),
            'username': message.from_user.username}
    bot.reply_to(message, f'{user["username"]}, {work(user)}')


@bot.message_handler(commands=['credits'])
def show(message):
    bot.send_message(message.chat.id, show_credits())


@bot.message_handler(commands=['shop'])
def shop(message):
    check_user({'id': str(message.from_user.id), 'username': message.from_user.username})

    markup = types.InlineKeyboardMarkup


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
                add_credits({'id':str(players[0]['id']), 'username': players[0]['username']}, 100)

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
    if not education_mode and not math_mode:

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


    elif education_mode:
        global tag
        if action == 'new tag' and message.text != '':
            tag = message.text
            data[tag] = {'messages': [], 'answers': []}
            add_message(message)

        elif action == 'edit tag' and message.text != '':
            tag = message.text.lower()
            if tag in data.keys():
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton('Изменить название', callback_data='rename_tag'))
                markup.add(types.InlineKeyboardButton('Изменить содержимое', callback_data='edit_messages'))
                markup.add(types.InlineKeyboardButton('Закончить обучение', callback_data='finish'))
                bot.send_message(message.chat.id, 'Что вы хотите сделать?', reply_markup=markup)

            else:
                bot.send_message(message.chat.id, 'Такого тега не существует')

        elif action == 'rename tag' and message.text != '':
            new_tag = message.text.lower()
            data[new_tag] = data.pop(tag)
            tag = ''
            save_base()
            finish(message)

        elif action == 'add messages' and message.text != '':
            messages = message.text.lower()
            messages = messages.split(';')
            for i in range(len(messages)):
                if messages[i][0] == ' ':
                    messages[i] = messages[i][1:]
            data[tag]['messages'] = messages
            add_answers(message)

        elif action == 'add answers' and message.text != '':
            answers = message.text
            answers = answers.split(';')
            for i in range(len(answers)):
                if answers[i][0] == ' ':
                    answers[i] = answers[i][1:]
            data[tag]['answers'] = answers
            tag = ''
            save_base()
            finish(message)

        else:
            if message.from_user.id != 5105507379:
                bot.send_message(message.chat.id, 'Ошибка')
            else:
                bot.send_message(message.chat.id, 'Ошибка. Чини меня, дебил')


    elif math_mode:
        if message.text != '/finish':
            try:
                math_exp = eval(message.text)
                bot.send_message(message.chat.id, math_exp)
                finish(message)
            except:
                bot.send_message(message.chat.id, 'непонятно')


bot.polling(none_stop=True)
