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

'''
#list comprehension
trigger_china = set([i for i in read_list[0] if len(i) > 0])
trigger_shenzhen = set([i for i in read_list[1] if len(i) > 0])
answers_china = set([i for i in read_list[2] if len(i) > 0])
answers_shenzhen = set([i for i in read_list[3] if len(i) > 0])
'''


@bot.message_handler(func=lambda message: True)
def butthurt(message: Message):
    reply = set(message.text.lower().split(' '))
    _trigger = reply.intersection(trigger_shenzhen.union(trigger_china))
    if len(_trigger) > 0:
        _trigger_shenzhen = reply.intersection(trigger_shenzhen)
        if len(_trigger_shenzhen) > 0:
            bot.reply_to(message, random.choice(answers_shenzhen))
        else:
            _trigger_china = reply.intersection(trigger_china)
            if len(_trigger_china) > 0:
                bot.reply_to(message, random.choice(answers_china))

    # for i in trigger_china:
    #     if i in reply:
    #         bot.reply_to(message, random.choice(answers_china))
    #         break
    #     else:
    #         for i in trigger_shenzhen:
    #             if i in reply:
    #                 bot.reply_to(message, random.choice(answers_shenzhen))
    #                 break
    #             else:
    #                 break

bot.polling()
