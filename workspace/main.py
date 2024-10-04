import pygame
from controller import InputHandler
from model import Snake, Food, Game
from view import Renderer

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Snake Game")

    snake = Snake()
    food = Food()
    game = Game(snake, food)
    renderer = Renderer(screen)

    input_handler = InputHandler(snake)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            input_handler.handle_event(event)

        game.update()
        renderer.render(game)

        pygame.display.flip()
        clock.tick(5)

if __name__ == "__main__":
    main()
