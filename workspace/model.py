from dataclasses import dataclass
from enum import Enum
import random

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

@dataclass
class Point:
    x: int
    y: int

class Snake:
    def __init__(self):
        self.head = Point(40, 40)
        self.body = [self.head]
        self.direction = Direction.RIGHT

    def move(self):
        if self.direction == Direction.UP:
            new_head = Point(self.head.x, self.head.y - 40)
        elif self.direction == Direction.DOWN:
            new_head = Point(self.head.x, self.head.y + 40)
        elif self.direction == Direction.LEFT:
            new_head = Point(self.head.x - 40, self.head.y)
        elif self.direction == Direction.RIGHT:
            new_head = Point(self.head.x + 40, self.head.y)

        self.body.insert(0, new_head)
        self.head = new_head
        self.body.pop()

    def change_direction(self, direction):
        if direction == Direction.UP and self.direction != Direction.DOWN:
            self.direction = direction
        elif direction == Direction.DOWN and self.direction != Direction.UP:
            self.direction = direction
        elif direction == Direction.LEFT and self.direction != Direction.RIGHT:
            self.direction = direction
        elif direction == Direction.RIGHT and self.direction != Direction.LEFT:
            self.direction = direction

    def grow(self):
        self.body.append(Point(self.head.x, self.head.y))

    def check_collision(self):
        if self.head.x < 0 or self.head.x >= 800 or self.head.y < 0 or self.head.y >= 600:
            return True

        for segment in self.body[1:]:
            if segment == self.head:
                return True

        return False

class Food:
    def __init__(self):
        self.position = self.generate_position()


    def generate_position(self):
        x = random.randint(0, 19) * 40
        y = random.randint(0, 14) * 40
        return Point(x, y)

    def check_collision(self, snake):
        if self.position == snake.head:
            return True
        return False

    def update(self):
        
        self.position = self.generate_position()

class Game:
    def __init__(self, snake, food):
        self.snake = snake
        self.food = food
        self.game_over = False

    def update(self):
        if not self.game_over:
            self.snake.move()
            if self.snake.check_collision():
                self.game_over = True
            if self.food.check_collision(self.snake):
                self.snake.grow()
                self.food.update()

    def reset(self):
        self.snake = Snake()
        self.food = Food()
        self.game_over = False
