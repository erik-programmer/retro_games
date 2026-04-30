import pygame
from constants import *


class Star:
    def __init__(self, x, y, image, direction):
        self.x = x
        self.y = y
        self.image = image
        self.direction = direction
        self.angle = 0

    def update(self):
        self.angle += 10
        if self.direction == pygame.K_RIGHT:
            self.x += HERO_SPEED * 1.1
        if self.direction == pygame.K_LEFT:
            self.x -= HERO_SPEED * 1.1
        if self.direction == pygame.K_UP:
            self.y -= HERO_SPEED * 1.1
        if self.direction == pygame.K_DOWN:
            self.y += HERO_SPEED * 1.1

    def get_rect(self):
        return pygame.transform.rotate(self.image, self.angle).get_rect(
            center=(self.x, self.y)
        )

    def draw(self, screen: pygame.Surface):
        rotated_img = pygame.transform.rotate(self.image, self.angle)
        rect = rotated_img.get_rect(center=(self.x, self.y))
        #  pygame.draw.rect(screen, (255, 50, 50), self.get_rect())
        screen.blit(rotated_img, rect)
