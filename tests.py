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



def butthurt(message):
    reply = message.lower()
    for i in trigger_china:
        if i in reply:
            print(random.choice(answers_china))
            break
        else:
            for i in trigger_shenzhen:
                if i in reply:
                    print(random.choice(answers_shenzhen))
                    break
                else:
                    break

def butthurt2(message):
    for each in trigger_china:
        if each in message:
            print(random.choice(answers_china))
            break

def butthurt3(message):
    counter = 0
    for row in read_list:
        #print(read_list[counter])
        for element in read_list[counter]:
            if element in message:
                print(random.choice(read_list[counter + 1]))
                break
            else:
                pass
        counter = counter + 1



while True:
    message = input('Введите ваше сообщение: ')
    butthurt3(message)
