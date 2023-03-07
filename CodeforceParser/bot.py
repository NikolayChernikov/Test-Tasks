import telebot
from telebot import types
from main import DataBase

bot = telebot.TeleBot('6042483401:AAGAPECY9w52vEZBH83Un5JI6JFUizwz7fE')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "👋 Привет! Я твой бот-помошник!", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == '👋 Поздороваться':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
        btn1 = types.KeyboardButton('Выбрать сложность и тему')
        btn2 = types.KeyboardButton('Выбрать по номеру задачи')
        markup.add(btn1, btn2)
        bot.send_message(message.from_user.id, 'Выбери что хочешь', reply_markup=markup)  # ответ бота

    elif message.text == 'Выбрать сложность и тему':
        bot.send_message(message.chat.id, "Введите сложность и тему через пробел: ")
        bot.register_next_step_handler(message, find_by_difficulty_theme)

    elif message.text == 'Выбрать по номеру задачи':
        bot.send_message(message.chat.id, "Введите номер задачи: ")
        bot.register_next_step_handler(message, find_by_id)


def find_by_id(message):
    db = DataBase()
    a = str(message.text)
    db.cur.execute('''SELECT * FROM codeforseparser WHERE id = %s;''', (a,))
    value = db.cur.fetchall()
    returned_string = ""
    for i in range(len(value)):
        returned_string += str(value[i])
    bot.send_message(message.from_user.id,
                     returned_string,
                     parse_mode='Markdown')


def find_by_difficulty_theme(message):
    db = DataBase()
    a = str(message.text)
    a = a.split(" ")
    dif = a[0]
    theme = a[1]
    db.cur.execute('''SELECT * FROM codeforseparser WHERE level = %s AND themes = %s LIMIT 10;''', (dif,theme))
    value = db.cur.fetchall()
    value = ' '.join(str(el) for el in value)

    bot.send_message(message.from_user.id,
                     value,
                     parse_mode='Markdown')


bot.polling(none_stop=True, interval=0)  # обязательная для работы бота часть
