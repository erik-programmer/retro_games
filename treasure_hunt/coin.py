import pygame


class Coin:
    def __init__(self, x, y, images):
        self.x = x
        self.y = y
        self.start_time = pygame.time.get_ticks()
        self.image_number = 0
        self.images = images
        self.was_collected = False
        self.has_disappeared = False

    def update(self):
        if not self.was_collected:
            if self.start_time + 100 < pygame.time.get_ticks():
                self.image_number += 1
                self.start_time = pygame.time.get_ticks()
                if self.image_number == 8:
                    self.image_number = 0
        else:
            if self.start_time + 100 < pygame.time.get_ticks():
                self.image_number += 1
                self.start_time = pygame.time.get_ticks()
                if self.image_number == 14:
                    self.image_number = 0
                    self.has_disappeared = True

    def collected(self):
        if not self.was_collected:
            self.start_time = pygame.time.get_ticks()
            self.image_number = 8
        self.was_collected = True

    def get_rect(self):
        return self.images[self.image_number].get_rect(topleft=(self.x, self.y))

    def draw(self, screen: pygame.Surface):
        if not self.has_disappeared:
            screen.blit(self.images[self.image_number], (self.x, self.y))
