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
           'любит китай',
           'великий китай',
           'Мао чжуси',
           'товарищ си'
           ]

answers = ['Ненавижу Китай!',
           'Обожаю Китай!',
           'Великий Китай!',
           'Пять тысяч лет истории!',
           'Восемь тысяч лет истории!',
           'Стопятьдесят тысяч лет истории!']

shenzhen_trigger = ['шеньжень',
           'шенчжен',
           'шэнчжэн',
           'шенжен',
           'шенджен',
           'шенчжен',
           'женьшень',
           'ШЖ',
           ]

shenzhen_answer = ['Шамбала?',
           'Каншифу?',
           'Жэньшень?',
           'Шаолинь?',
           'Шаисы?',]


@bot.message_handler(func=lambda message: True)
def butthurt(message: Message):
    reply = message.text.lower()
    counter = 0
    for i in trigger:
        if i in reply:
            counter = counter + 1
            break
    if counter > 0:
        bot.reply_to(message, random.choice(answers))
    counter_2 = 0
    for i in shenzhen_trigger:
        if i in reply:
            counter_2 = counter_2 + 1
            break
    if counter_2 > 0:
        bot.reply_to(message, random.choice(shenzhen_answer))


bot.polling()
