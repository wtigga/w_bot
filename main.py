import telebot
import random
from telebot.types import Message

TOKEN = 'TOKEN'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    bot.reply_to(message, 'Привет, бро.')

@bot.message_handler(commands=['stop'])
def send_welcome(message: Message):
    bot.reply_to(message, 'Пока, бро.')

trigger = ['китай', 'китаи', 'китае', 'china']
answers = ['Ненавижу Китай!', 'Обожаю Китай!', 'Китай - это где?']

@bot.message_handler(func=lambda message: True)
def upper(message: Message):
    reply = message.text
    reply = reply.lower()
    counter = 0
    for i in trigger:
        if i in reply:
            counter = counter + 1
            break
        else:
            pass
    if counter > 0:
        bot.reply_to(message, random.choice(answers))
    else:
        pass

bot.polling()
