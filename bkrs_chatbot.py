import telebot
import random
import os
from telebot.types import Message
import csv



TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)


def read_csv(filename):
    with open(filename, 'r', encoding='utf-8') as file:  # read content from CSV
        reader = csv.reader(file, delimiter='\t')
        output_list = list(reader)
        return output_list


def clean_list(my_list):  # clean CSV list of empty cells
    for i in my_list:
        try:
            my_list.pop(my_list.index(''))
        except:
            pass
    return my_list


def clean_upper_list(my_list):
    all_list = []
    for line in my_list:
        line = clean_list(line)
        all_list.append(line)
    return(all_list)


triggers_all = read_csv('triggers.csv')
answers_all = read_csv('answers.csv')
triggers_all = clean_upper_list(triggers_all)
answers_all = clean_upper_list(answers_all)



'''
#list comprehension
trigger_china = set([i for i in read_list[0] if len(i) > 0])
trigger_shenzhen = set([i for i in read_list[1] if len(i) > 0])
answers_china = set([i for i in read_list[2] if len(i) > 0])
answers_shenzhen = set([i for i in read_list[3] if len(i) > 0])


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
                
'''

@bot.message_handler(func=lambda message: True)
def butthurt2(message: Message, triggers, answers):
    message = message.text.lower()  # переводим сообщение юзера в нижний регистр
    count = 0  # считаем номер строки, по которой будет определён ответ
    for line in triggers:
        for each in line:  # для каждого слова из выбранного списка
            if each in message: # если слово из списка присутствует в сообщении
                bot.reply_to(message, random.choice(answers[count]))  # выбираем случайный ответ из строки
                break
        count = count + 1


bot.polling()
