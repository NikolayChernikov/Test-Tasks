import telebot
import configparser
from telebot import types
from database import DataBase

config = configparser.ConfigParser()
config.read("../deployment/config/config.conf")
bot = telebot.TeleBot(str(config["BOT"]["token"]))


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Выбрать сложность и тему')
    btn2 = types.KeyboardButton('Выбрать по номеру задачи')
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, 'Выбери что хочешь', reply_markup=markup)

    if message.text == 'Выбрать сложность и тему':
        bot.send_message(message.chat.id, "Введите сложность и тему через пробел: ")
        bot.register_next_step_handler(message, find_by_difficulty_theme)

    elif message.text == 'Выбрать по номеру задачи':
        bot.send_message(message.chat.id, "Введите номер задачи: ")
        bot.register_next_step_handler(message, find_by_id)


def find_by_id(message):
    db = DataBase()
    a = str(message.text)
    value = db.find_by_id(a)
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
    value = db.find_by_difficulty_theme(dif, theme)
    value = ' '.join(str(el) for el in value)

    bot.send_message(message.from_user.id,
                     value,
                     parse_mode='Markdown')


bot.polling(none_stop=True, interval=0)
