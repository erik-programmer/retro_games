import pygame
from utils import *


class Fire:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start_time = pygame.time.get_ticks()
        self.image_number = 0
        self.images = load_images("/enemy/fire/fire", 6)
        self.life_time = self.start_time
        self.is_dead = False

    def update(self):
        if self.start_time + 50 < pygame.time.get_ticks():
            self.image_number += 1
            self.start_time = pygame.time.get_ticks()
            if self.image_number == 6:
                self.image_number = 0
        if self.life_time + 5000 < pygame.time.get_ticks():
            self.is_dead = True

    def get_rect(self):
        return self.images[self.image_number].get_rect(center=(self.x, self.y))

    def draw(self, screen: pygame.Surface):
        screen.blit(self.images[self.image_number], self.get_rect())
