import tkinter as tk
import threading as thr
import time
import random

color_bg = "#115249"
color_food = "#4EFCE5"
color_snake = "#FCD335"

HEIGHT = 1500
WIDTH = 1200

size = 50
rate = 5
snake_x = 15
snake_y = 15
direction = "w"
food_x = 0
food_y = 0
score = 0
tail = []

root = tk.Tk()
root.title("Змеюка")
root.geometry(f"{HEIGHT}x{WIDTH}")
root.resizable(False, False)
root['bg'] = color_bg
canvas = tk.Canvas(root)

def create_food():
    global food_x, food_y, snake_x, snake_y
    x = random.randint(0, int(WIDTH/size)-1)
    y = random.randint(0, int(HEIGHT/size)-1)
    if x == snake_x and y == snake_y:
        create_food()
    food_x = x
    food_y = y

def death():
    global root
    root.quit()

def update():
    global canvas, snake_x, snake_y, direction, food_x, food_y , tail
    canvas_new = tk.Canvas()
    canvas_new.create_rectangle(0, 0, HEIGHT, WIDTH, outline=color_bg, fill=color_bg)

    if len(tail)>0:        
        tail[len(tail)-1][0] = snake_x
        tail[len(tail)-1][1] = snake_y
        tail.insert(0,tail.pop(len(tail)-1))

    if direction == "w":
        snake_y -= 1
    if direction == "s":
        snake_y += 1
    if direction == "a":
        snake_x -= 1
    if direction == "d":
        snake_x += 1

    if snake_y>=HEIGHT/size or snake_y<0 or snake_x>=WIDTH/size or snake_x<0:
        death()
    
    for piece in tail:
        canvas_new.create_rectangle(
        piece[0] * size,
        piece[1] * size,
        piece[0] * size + size,
        piece[1] * size + size,
        outline=color_snake,
        fill=color_snake,
        )    

    canvas_new.create_rectangle(
        snake_x * size,
        snake_y * size,
        snake_x * size + size,
        snake_y * size + size,
        outline=color_snake,
        fill=color_snake,
    )

    if snake_y == food_y and snake_x == food_x:
        create_food()
        tail.append([snake_x,snake_y])

    canvas_new.create_rectangle(
        food_x * size,
        food_y * size,
        food_x * size + size,
        food_y * size + size,
        outline=color_food,
        fill=color_food,
    )
    canvas.destroy()
    canvas_new.pack(fill=tk.BOTH, expand=1)
    canvas = canvas_new

def loop():
    while True:
        update()
        time.sleep(1 / rate)

def change_direction_w(self):
    global direction
    direction = "w"

def change_direction_a(self):
    global direction
    direction = "a"

def change_direction_s(self):
    global direction
    direction = "s"

def change_direction_d(self):
    global direction
    direction = "d"

create_food()
t = thr.Thread(target=loop, daemon=True)
t.start()

root.bind("w", change_direction_w)
root.bind("a", change_direction_a)
root.bind("s", change_direction_s)
root.bind("d", change_direction_d)
root.mainloop()
