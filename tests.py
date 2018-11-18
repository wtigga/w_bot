trigger = ['китай', 'китаи', 'китае']


while True:
    word = input('Введите фразу: ')
    word = str(word)
    word = word.lower()
    counter = 0
    answer = ''
    for i in trigger:
        if i in word:
            counter = counter + 1
            break
        else:
            pass
    if counter > 0:
        answer = "Ненавижу Китай!"
    else:
        answer = 'нипонял'
    print(answer)
