import telebot
import random
from telebot.types import Message

TOKEN = '794930488:AAEtpnGGR0NcidyV1JcA-tJOL0PjkI7DpiU'
bot = telebot.TeleBot(TOKEN)

trigger = ['обожаю китай', 'ненавижу китай', 'долбаный китай', 'сраный китай', 'китай...']
answers = ['Ненавижу Китай!', 'Обожаю Китай!']

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