import pygame


class Gem:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

    def get_rect(self):
        return self.image.get_rect(center=(self.x, self.y))

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.get_rect())
