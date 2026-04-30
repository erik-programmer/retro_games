import pygame


class Path:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

    def get_rect(self):
        return self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, (self.x, self.y))
