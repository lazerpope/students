import pygame
from model import Direction

class InputHandler:
    def __init__(self, snake):
        self.snake = snake

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.snake.change_direction(Direction.UP)
            elif event.key == pygame.K_DOWN:
                self.snake.change_direction(Direction.DOWN)
            elif event.key == pygame.K_LEFT:
                self.snake.change_direction(Direction.LEFT)
            elif event.key == pygame.K_RIGHT:
                self.snake.change_direction(Direction.RIGHT)
