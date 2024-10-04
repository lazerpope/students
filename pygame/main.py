import pygame as pg
import random

WIDTH = 360
HEIGHT = 480
FPS = 60


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My Game")
clock = pg.time.Clock()

rect = {'x':10,'y':10}
speed = 0
gravity = 0.1
running = True
while running:
    clock.tick(FPS)  
    screen.fill(WHITE)     
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    pg.draw.rect(screen, RED, (int(rect['x'] ),rect['y'],50,100),4)
    
    speed +=gravity
    rect['x'] +=speed
    
    if rect['x']>= 400:
        rect['x']=0

    pg.display.flip()

pg.quit()