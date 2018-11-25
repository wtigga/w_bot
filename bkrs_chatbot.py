import telebot
import random
import os
from telebot.types import Message
import csv

# TOKEN = os.environ.get('TOKEN')
TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)


# reading the CSV file with triggers and answers
def read_csv(filename):
    with open(filename, 'r', encoding='utf-8') as file:  # read content from CSV
        reader = csv.reader(file, delimiter='\t')
        output_list = list(reader)
        return output_list


def clean_list(my_list):  # clean CSV list of empty cells
    for _ in my_list:
        try:
            my_list.pop(my_list.index(''))
        except:  # when we're run out of empty cells
            pass  # don't do anything
    return tuple(my_list)


def clean_upper_list(my_list):
    all_list = []
    for line in my_list:
        line = clean_list(line)
        all_list.append(line)
    return all_list


triggers_all = tuple(clean_upper_list(read_csv('triggers.csv')))  # use tuples to speed up search and iterations
answers_all = tuple(clean_upper_list(read_csv('answers.csv')))


@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    bot.reply_to(message, 'Привет, бро.')


@bot.message_handler(commands=['stop'])
def send_welcome(message: Message):
    bot.reply_to(message, 'Пока, бро.')


@bot.message_handler(func=lambda message: True)
def react_to_messages(message: Message):
    reply = message.text.lower()  # lowercase user's message to avoid case affect search
    count = 0  # count the line where the trigger happens
    for line in triggers_all:  # run through each list of trigger
        for each in line:  # run through each word in list
            if each in reply:  # if the trigger word is in the list
                bot.reply_to(message, random.choice(answers_all[count]))  # pick a random answer from the corresponding answer line
                break  # to prevent answering multiple times to several trigger word
        count = count + 1


bot.polling()  # this run bot messages handler
