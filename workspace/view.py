import pygame

class Renderer:
    def __init__(self, screen):
        self.screen = screen

    def render(self, game):
        self.screen.fill((0, 0, 0))

        if game.game_over:
            self.render_game_over()
        else:
            self.render_snake(game.snake)
            self.render_food(game.food)

    def render_snake(self, snake):
        for i, segment in enumerate( snake.body):
            if i == 0:
                pygame.draw.rect(self.screen, (144, 255, 0), (segment.x, segment.y, 40, 40))
                continue
            pygame.draw.rect(self.screen, (0, 255, 0), (segment.x, segment.y, 40, 40))

    def render_food(self, food):
        pygame.draw.rect(self.screen, (255, 0, 0), (food.position.x, food.position.y, 40, 40))

    def render_game_over(self):
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over", True, (255, 255, 255))
        text_rect = text.get_rect(center=(400, 300))
        self.screen.blit(text, text_rect)
