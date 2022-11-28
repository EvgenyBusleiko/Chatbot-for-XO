import telebot
import json
import random, os


API_TOKEN='5910633103:AAFVnDNyWS3klWIB4OLCjWY-t8soT1qJ2jU'

field = []
field_count=[]
global m

def win_check():
    winner=''
    sum=[]
    for i in range (8): sum.append(0)
    tmp=0
    tmp1=0
    for i in range (3):
        for j in range(3):
            tmp=tmp+field_count[i][j]
            tmp1 = tmp1 + field_count[j][i]
            if (i==j):
                sum[6]=sum[6]+ field_count[j][i]

            if ((i==j==1)) or ((i==0) and (j==2)) or ((i==2) and (j==0)):
                sum[7]=sum[7]+ field_count[j][i]

        sum[i] = tmp
        sum[i + 3] = tmp1
        tmp =tmp1=0

    for i in sum:
        if i==3 :winner="Я победил!"
        elif i==12:winner="Ты победил!"

    return winner;



bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    global m
    global win
    win=''
    bot.send_message(message.chat.id,"Бот для игры в крестики / нолики")
    bot.send_message(message.chat.id, "Первый ход определяется случайным образом")
    bot.send_message(message.chat.id, "Компьютер всегда играет ноликами")

    bot.send_message(message.chat.id, 'Начало игры')
    for i in range(3):
        fieldrow = []
        field_drow_count = []
        for j in range(3):
            fieldrow.append('_')
            field_drow_count.append(0)
        field.append(fieldrow)
        field_count.append(field_drow_count)
    for i in range(3):
        s=''
        for i in range(3):
           s=("  ".join(field[i]))
        bot.send_message(message.chat.id, s)
    m = random.randint(1, 2)
    print(m)
    if (m % 2 != 0):
        bot.send_message(message.chat.id, 'Мой ход')
        x = random.randint(0, 2)
        y = random.randint(0, 2)
        while field[x][y] != '_':
            x = random.randint(0, 2)
            y = random.randint(0, 2)
        field[x][y]='0'
        field_count[x][y] = 1
        m = m + 1
        print(x,y)
        print(field[x][y])
        for i in range(3):
            s = ("  ".join(field[i]))
            bot.send_message(message.chat.id, s)
        bot.send_message(message.chat.id, 'Твой ход. Вводи координаты поля через пробел')

    else: bot.send_message(message.chat.id, 'Твой ход. Вводи координаты поля через пробел')


@bot.message_handler(content_types='text')
def check_message(message):
    global m, win

    if (win == ''):
        move_coord=message.text.split(' ')
        x=int (move_coord[0])
        y=int (move_coord[1])

        if field[x][y] != '_':bot.send_message(message.chat.id,'Поле занято. Попробуй другое')
        else:
            field[x][y] = 'X'
            field_count[x][y] = 4
            for i in range(3):
                s = ("  ".join(field[i]))
                bot.send_message(message.chat.id, s)
            m = m + 1
            win = win_check()
    if (m % 2 != 0) and (win == ''):
        bot.send_message(message.chat.id, 'Мой ход')
        x = random.randint(0, 2)
        y = random.randint(0, 2)
        while field[x][y] != '_':
            x = random.randint(0, 2)
            y = random.randint(0, 2)
        field[x][y] = '0'
        field_count[x][y] = 1
        m = m + 1
        print(x, y)
        print(field[x][y])
        for i in range(3):
            s = ("  ".join(field[i]))
            bot.send_message(message.chat.id, s)
        win = win_check()
        if win=='':bot.send_message(message.chat.id, 'Твой ход. Вводи координаты поля через пробел')
    if win != '':
        field.clear()
        field_count.clear()
        bot.send_message(message.chat.id,win)
        bot.send_message(message.chat.id, 'Играем еще? /start')
        win=''
    elif (m>10):
        win='Ничья'
        field.clear()
        field_count.clear()
        bot.send_message(message.chat.id,win)
        bot.send_message(message.chat.id, 'Играем еще? /start')
        win = ''



bot.polling()