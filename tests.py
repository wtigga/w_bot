import csv

with open('triggers.csv', 'r', encoding='utf-8') as file:
  reader = csv.reader(file, delimiter='\t')
  read_list = list(reader)


def clean_list(my_list):  # clean CSV list of empty cells
    for i in my_list:
            try:
                my_list.pop(my_list.index(''))
            except:
                pass
    return my_list


trigger_china = clean_list(read_list[0])
trigger_shenzhen = clean_list(read_list[1])
answers_china = clean_list(read_list[2])
answers_shenzhen = clean_list(read_list[3])





trigger_china = ['обожаю китай',
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

answers_china = ['Ненавижу Китай!',
           'Обожаю Китай!',
           'Великий Китай!',
           'Пять тысяч лет истории!',
           'Восемь тысяч лет истории!',
           'Стопятьдесят тысяч лет истории!']

trigger_shenzhen = ['шеньжень',
           'шенчжен',
           'шэнчжэн',
           'шенжен',
           'шенджен',
           'шенчжен',
           'женьшень',
           'ШЖ']

answers_shenzhen = ['Шамбала?',
           'Каншифу?',
           'Жэньшень?',
           'Шаолинь?',
           'Шаисы?',]