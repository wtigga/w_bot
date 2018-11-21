import telebot
import random
import os
from telebot.types import Message
import csv

with open('triggers.csv', 'r', encoding='utf-8') as file:  # read content from CSV
  reader = csv.reader(file, delimiter='\t')
  read_list = list(reader)


def clean_list(my_list):  # clean CSV list of empty cells
    for i in my_list:
            try:
                my_list.pop(my_list.index(''))
            except:
                pass
    return my_list


TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)

trigger_china = clean_list(read_list[0])
trigger_shenzhen = clean_list(read_list[1])
answers_china = clean_list(read_list[2])
answers_shenzhen = clean_list(read_list[3])


@bot.message_handler(func=lambda message: True)
def butthurt(message: Message):
    reply = message.text.lower()
    for i in trigger_china:
        if i in reply:
            bot.reply_to(message, random.choice(answers_china))
            break
        else:
            for i in trigger_shenzhen:
                if i in reply:
                    bot.reply_to(message, random.choice(answers_shenzhen))
                    break


bot.polling()
