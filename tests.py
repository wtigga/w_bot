import random
import csv
import urllib.request, json
from pprint import pprint
'''

def clean_list(my_list):  # clean CSV list of empty cells
    for i in my_list:
        try:
            my_list.pop(my_list.index(''))
        except:
            pass
    return my_list


def read_csv(filename):
    with open(filename, 'r', encoding='utf-8') as file:  # read content from CSV
        reader = csv.reader(file, delimiter='\t')
        output_list = tuple(list(reader))
        return output_list


triggers_all = read_csv('triggers.csv')
answers_all = read_csv('answers.csv')

def clean_upper_list(my_list):
    all_list = []
    for line in my_list:
        line = clean_list(line)
        all_list.append(line)
    return tuple(all_list)

triggers_all = clean_upper_list(triggers_all)
answers_all = clean_upper_list(answers_all)

triggers_all = tuple(triggers_all)
answers_all = tuple(answers_all)

'''
'''
TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)

trigger_china = clean_list(triggers_all[0])
trigger_shenzhen = clean_list(triggers_all[1])
answers_china = clean_list(answers_all[0])
answers_shenzhen = clean_list(answers_all[1])
'''


'''

def butthurt2(message, triggers, answers):
    message = message.lower()  # переводим сообщение юзера в нижний регистр
    count = 0  # считаем номер строки, по которой будет определён ответ
    for line in triggers:
        for each in line:  # для каждого слова из выбранного списка
            if each in message: # если слово из списка присутствует в сообщении
                print(random.choice(answers[count]))  # выбираем случайный ответ из строки
                break
        count = count + 1


while True:
    message_user = input('Введите ваше сообщение: ')
    butthurt2(message_user, triggers_all, answers_all)
'''
def currency_cny_rub():
    with urllib.request.urlopen("http://free.currencyconverterapi.com/api/v5/convert?q=CNY_RUB&compact=y") as url:
        data = json.load(url)
        data = data["CNY_RUB"]["val"]
        output = str('Курс юаня к рублю: ' + str(data))
        return output

print(currency_cny_rub())