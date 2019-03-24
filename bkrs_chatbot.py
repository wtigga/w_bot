import telebot
import random
import os
from telebot.types import Message
import csv
import urllib.request, json
import sqlite3

# TOKEN = os.environ.get('TOKEN')
TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)

with open('messages.txt', 'r') as f:
    feedbacks = f.readlines()

def func():
    for i in feedbacks[:]:
        lst = i.replace('\n','').replace('<br>','').replace('&quot;', '').split(' ')
        yield list(zip(lst, lst[1:]))

pairs = func()
corpora = dict()

for i in pairs:
    for ii in i:
        if ii[0] in corpora.keys():
            corpora[ii[0]].append(ii[1])
        else:
            corpora[ii[0]] = [ii[1]]


# reading the CSV file with triggers and answers
def read_csv(filename):
    with open(filename, 'r', encoding='utf-8') as file:  # read content from CSV
        reader = csv.reader(file, delimiter='\t')
        output_list = list(reader)
        return output_list

#added db support
def read_db(tablename):
    c = sqlite3.connect('texts.db')
    cur = c.execute('select * from %s;' % (tablename))
    res = cur.fetchall()
    output_list = [i[1] for i in res]
    c.close()
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


def currency(currency_pair):
    currencies_texts = {'CNY_RUB': 'рубля к юаню',
                        'USD_CNY': 'юаня к доллару',
                        'USD_RUB': 'рубля к доллару'}
    with urllib.request.urlopen(f"http://free.currencyconverterapi.com/api/v5/convert?q={currency_pair}&compact=y") as url:
        data = round((json.load(url)[currency_pair]["val"]), 3)  # get currency rate from VAL, round to 3 digits float
        output = (f'Курс {currencies_texts[currency_pair]}: ' + str(data))
        return output


triggers_all = tuple(clean_upper_list(read_csv('triggers.csv')))  # use tuples to speed up search and iterations
answers_all = tuple(clean_upper_list(read_csv('answers.csv')))


@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    bot.reply_to(message, 'Привет, бро. Я могу сказать курс валют по командам /cny, /rub и /usd')


@bot.message_handler(commands=['cny'])
def currency_cny(message: Message):
    bot.reply_to(message, currency('CNY_RUB'))


@bot.message_handler(commands=['usd'])
def currency_usd(message: Message):
    bot.reply_to(message, currency('USD_CNY'))


@bot.message_handler(commands=['rub'])
def currency_rub(message: Message):
    bot.reply_to(message, currency('USD_RUB'))

@bot.message_handler(content_types=['voice'])
def handle_docs_audio(message):
    bot.reply_to(message, 'Разговорчики!')


@bot.message_handler(func=lambda message: True)
def react_to_messages(message: Message):
    reply = message.text.lower()  # lowercase user's message to avoid case affect search
    count = 0  # count the line where the trigger happens
    for line in triggers_all:  # run through each list of trigger
        for each in line:  # run through each word in list
            for each in reply:  # if the trigger word is in the list
                # if "бот тупой" in reply or "тупой бот" in reply or "выключите бота" in reply or "надоел бот" in reply or "傻бкрс" in reply or "дебильный бот" in reply:
                #     first_word = np.random.choice(list(corpora.keys()))
                #     chain = [first_word]
                #     n_words = 30
                #     for i in range(n_words):
                #         try:
                #             chain.append(np.random.choice(corpora[chain[-1]]))
                #         except KeyError:
                #             break
                #     bot.reply_to(message, ' '.join(chain))
                #     break
                # else: 
                    bot.reply_to(message, random.choice(answers_all[count]))  # pick a random answer from the corresponding answer line
                    break  # to prevent answering multiple times to several trigger word
        count = count + 1

'''
bot.polling()  # this run bot messages handler
'''

if __name__ == '__main__':
    bot.polling(none_stop=True)

