from tkinter import *


HEIGHT = 500
WIDTH = 800
window = Tk()
window.title('Bubble Blaster')#название игры
c = Canvas(window,width = WIDTH, height = HEIGHT, bg = 'darkblue') #создает холст делает цвет
c.pack()
#2>>>
ship_id = c.create_polygon( 5,5,5,25,30,15, fill = 'red', outline = 'black')
ship_id2 = c.create_oval( 0,0,30,30,outline = 'red')
SHIP_R=15 # Размер(радиус) лодки
MID_X = WIDTH/2 # Координаты середины экрана
MID_Y = HEIGHT/2 
c.move (ship_id, MID_X, MID_Y) #перемешает в центр экрана
c.move (ship_id2, MID_X, MID_Y)
#3>>
SHIP_SPD = 10

def move_ship(event):
    if event.keysym == 'Up':
        c.move(ship_id, 0, -SHIP_SPD) #двигает лодку принажатие вверх
        c.move(ship_id2, 0, -SHIP_SPD)
    elif event.keysym == 'Down' :
        c.move(ship_id, 0, SHIP_SPD) #двигает лодку принажатие вниз
        c.move(ship_id2, 0, SHIP_SPD)
    elif event.keysym == 'Left' :
        c.move(ship_id, -SHIP_SPD, 0) #двигает лодку принажатие влево
        c.move(ship_id2, -SHIP_SPD, 0)
    elif event.keysym == 'Right' :
        c.move(ship_id, SHIP_SPD, 0) #двигает лодку принажатие вправо
        c.move(ship_id2, SHIP_SPD, 0)
c.bind_all('<Key>', move_ship) #указывает что нужно вызвать функцию при нажатии       
#4>>>
from random import randint


bub_id = list() #
bub_r = list() # создает пустые списки для хранения данных
bub_speed = list() #
MIN_BUB_R = 10
MAX_BUB_R = 30
MAX_BUB_SPD = 10
GAP = 100

def create_bubble():
    x = WIDTH + GAP
    y = randint(0, HEIGHT)
    r = randint(MIN_BUB_R, MAX_BUB_R)#выбирает случайный размер
    idl = c.create_oval(x - r, y - r, x + r, y + r, outline = 'white') #рисует пузыри
    bub_id.append(idl)#
    bub_r.append(r)# Добавляет имя,радиус,скорость в списки 
    bub_speed.append(randint(1, MAX_BUB_SPD))#
#5>>>
def move_bubbles():
    for i in range(len(bub_id)):#по очереди берет каждый пвзырь из списка
        c.move(bub_id[i], -bub_speed[i], 0)
#7>>>
def get_coords(id_num):
    pos = c.coords(id_num)
    x = (pos[0] + pos[2])/2 #вычисляет Х-координаты пузыря
    y = (pos[1] + pos[3])/2 #вычисляет У-координаты пузыря
    return x, y
#8>>>
def del_bubble(i):
    del bub_r[i]
    del bub_speed[i] #удаляет пузырт из списков радиусов и скоростей
    c.delete(bub_id[i]) #удаляет пузырь с холста
    del bub_id[i] # удаляет пузырь из списка имен
#9>>>
def clean_up_bubs():
    for i in range(len(bub_id)-1, -1, -1):
        x, y = get_coords(bub_id[i])
        if x < - GAP:
            del_bubble(i)
#11>>>
from math import sqrt #загружает функцию sqrt из модуля math

def distance ( id1, id2):
    x1, y1 = get_coords(id1)
    x2, y2 = get_coords(id2)
    return sqrt((x2 - x1)**2 + (y2 - y1)**2) #Возращает расстояние между объектами
#12>>>
def collision():
    points = 0
    for bub in range(len(bub_id)-1, -1, -1):
        if distance(ship_id2, bub_id[bub]) < (SHIP_R + bub_r[bub]): #проверяет не столкнулась ли лотка с пузырем
            points += (bub_r[bub] + bub_speed[bub]) # вычисляет сколько очков за этот пузырь и прибавляет к points
            del_bubble(bub) #удаляет пузырь
    return points #возращает колво набраных очков       
#14>>>
c.create_text(50, 30, text = 'TIME', fill = 'white')
c.create_text(150,30, text = 'SCORE', fill = 'white')
time_text = c.create_text(50, 50, fill = 'white')
score_text = c.create_text(150, 50, fill = 'white')

def show_score(score):
    c.itemconfig(score_text, text = str(score)) # отображает счет
def show_time(time_left):
    c.itemconfig(time_text, text = str(time_left))
    
#6>>>
from time import sleep, time #загружает нужные функции из модуля time

BUB_CHANCE = 10
TIME_LIMIT = 30
BONUS_SCORE = 100
score = 0
bonus = 0
end = time() + TIME_LIMIT
#MAIN GAME LOOP
while time() < end:
    if randint(1, BUB_CHANCE) == 1 : #выбирает случ. число от 1 до 10
        #если число равно 1 создается новый пузырь
        create_bubble()
    move_bubbles() # обновляет позицию всех пузырей
    clean_up_bubs() #удаляет пузыри уплывшие за экран
    score += collision() # прибавляет очки к общему счету
    if (int(score / BONUS_SCORE)) > bonus:
        bonus += 1
        end+= TIME_LIMIT
    show_score(score)
    show_time(int(end - time())) # показывает ост время
    window.update() #обновляет окно чтоб отоброзить все изменения
    sleep(0.01) #замедляет игру

#17>>>
c.create_text(MID_X, MID_Y, \
              text = ' GAME OVER',  fill = ' white', font = ('Helvetica',30)) #задает шрифт
c.create_text(MID_X, MID_Y + 30, \
              text = ' Score: ' + str(score), fill = 'white')#показывает очки
c.create_text(MID_X, MID_Y + 45, \
              text = 'Bonus time: ' + str(bonus*TIME_LIMIT), fill = 'white')#показывает призовое время