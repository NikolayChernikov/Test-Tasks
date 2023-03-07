import telebot
from telebot import types
from main import DataBase

bot = telebot.TeleBot('token')


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

    elif message.text == 'Выбрать сложность и задачу':
        bot.send_message(message.from_user.id,
                         'ВЫБРАННО',
                         parse_mode='Markdown')

    elif message.text == 'Выбрать по номеру задачи':
        bot.send_message(message.chat.id, "Введите номер задачи: ")
        bot.register_next_step_handler(message, add_user)


def add_user(message):
    db = DataBase()
    a = str(message.text)
    db.cur.execute('''SELECT * FROM codeforseparser WHERE id = %s;''', (a,))
    hui = db.cur.fetchall()
    returned_string = ""
    for i in range(len(hui)):
        returned_string += str(hui[i])
    bot.send_message(message.from_user.id,
                     returned_string,
                     parse_mode='Markdown')


bot.polling(none_stop=True, interval=0)  # обязательная для работы бота часть
