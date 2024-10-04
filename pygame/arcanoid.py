from asyncio.windows_events import NULL
from platform import java_ver
from turtle import speed
import pygame as pg
import random
from random import randrange as rnd

width = 1600
height = 900
FPS = 60


ball_color = (255, 255, 255)
bg_color = (0, 0, 0)
paddle_color = (200, 100, 0)

paddle_w = 300
paddle_h = 30
paddle_speed = 20
paddle = pg.Rect(width // 2 - paddle_w // 2, height - paddle_h - 10, paddle_w, paddle_h)

ball_radius = 25
ball_speed = 6
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pg.Rect(width // 2, height - paddle_h - 2 * paddle_h, ball_rect, ball_rect)
dx, dy = random.choice([1, -1]), -1

block_num_x = 10
block_num_y = 4

block_list = [
    [pg.Rect(20 + 160 * i, 10 + 60 * j, 150, 50) for i in range(block_num_x)]
    for j in range(block_num_y)
]
max_color = 255
min_color = 0
block_color = []
for i in range(block_num_y):
    color_row = []
    for j in range(block_num_x):
        r = sorted((min_color, 80 + (i+1) * (j+1) * 3, max_color))[1] 
        g = sorted((min_color, 130 - (i+1) * (j+1) * 3, max_color))[1] 
        b = 150
        color_row.append((r,g,b))
    block_color.append(color_row)

def detect_collision(dx,dy,ball,rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx,dy = -dx,-dy
    elif delta_x>delta_y:
        dy*=-1
    elif delta_y > delta_x:
        dy*=-1
    return dx,dy

def update_fps():
	fps = str(int(clock.get_fps()))
	fps_text = font.render(fps, 1, pg.Color("coral"))
	return fps_text
 

pg.init()
pg.mixer.init()
screen = pg.display.set_mode((width, height))
pg.display.set_caption("My Game")
clock = pg.time.Clock()
font = pg.font.SysFont("Arial", 30)

running = True
while running:
    clock.tick(FPS)
    screen.fill(bg_color)
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    key = pg.key.get_pressed()

    if key[pg.K_LEFT] and paddle.left > 0:
        paddle.left -= paddle_speed
    if key[pg.K_RIGHT] and paddle.right < width:
        paddle.right += paddle_speed

    if ball.centerx < ball_radius + 8 or ball.centerx + 5 > width - ball_radius:
        dx *= -1
    if ball.centery < ball_radius:
        dy *= -1

    if ball.colliderect(paddle) and dy > 0:
        dy *= -1

    for i in range(block_num_y):        
        for j in range(block_num_x):
                if block_list[i][j]!=NULL and ball.colliderect(block_list[i][j]):
                    dx,dy = detect_collision(dx,dy,ball,block_list[i][j])
                    block_list[i][j] = NULL   
                    block_color[i][j] = NULL  
                    
    for i in range(block_num_y):        
        for j in range(block_num_x):
            if block_list[i][j]!=NULL:
                pg.draw.rect(screen, block_color[i][j], block_list[i][j])
       
    pg.draw.rect(screen, paddle_color, paddle)
    pg.draw.circle(screen, ball_color, ball.center, ball_radius)
    ball.x += ball_speed * dx
    ball.y += ball_speed * dy
    screen.blit(update_fps(), (10,0))
    pg.display.flip()

pg.quit()
