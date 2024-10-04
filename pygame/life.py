import pygame as pg
from random import choice
from copy import deepcopy
import field 
width = 900
height = 900
tile_size = 5
w = width//tile_size
h = height//tile_size

WHITE = (100, 100, 100)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

pg.init()
pg.mixer.init()
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Game Of Life")
clock = pg.time.Clock()

next_field = [[False for i in range(w)] for j in range(h)]
this_field = [[False  for i in range(w)] for j in range(h)]

#this_field = [[choice([True,False])  for i in range(w)] for j in range(h)]

# to_join = field.get1()
# for i in range(len(to_join)):
#     for j in range(len(to_join[i])):
#        this_field[i+4][j+4] = to_join [i][j]

# for i in range(w):
#     for j in range(h):
#         this_field[i][j] = True if i-j==0 or i+j == w    else False

for i in range(w):
    for j in range(h):
        this_field[i][j] = True if i-j==0 or i+j == w or i==w//2 or j==h//2   else False

# for i in range(w):
#     for j in range(h):
#         this_field[i][j] = True if i==w//2 or j==h//2 else False


running = True
while running:  
    #clock.tick(10)    
    screen.fill(BLACK)     
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    [pg.draw.line(screen,WHITE,(x,0),(x,height)) for x in range(0,width,tile_size)]
    [pg.draw.line(screen,WHITE,(0,y),(width,y)) for y in range(0,height,tile_size)]

    for i in range(1,len(this_field)-1):
            for j in range(1,len(this_field[i])-1):
                next_field [i][j] =  field.check_cell(this_field,i,j)
    
    this_field = deepcopy(next_field)
    for i in range(len(this_field)):
        for j in range(len(this_field[i])):
            if this_field[i][j]:
                pg.draw.rect(screen, GREEN, (j*tile_size,i*tile_size,tile_size,tile_size))
    
    

    pg.display.flip()

pg.quit()