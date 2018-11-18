import telebot
import random
import os
from telebot.types import Message

TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)

trigger = ['обожаю китай',
           'ненавижу китай',
           'долбаный китай',
           'сраный китай',
           'китай...',
           'любишь китай',
           'хочешь в китай',
           'любит китай']

answers = ['Ненавижу Китай!',
           'Обожаю Китай!',
           'Великий Китай!',
           'Пять тысяч лет истории!',
           'Восемь тысяч лет истории!'
           'Стопятьдесят тысяч лет истории!']


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