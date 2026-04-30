import pygame


class Wall:
    def __init__(self, x, y, images, is_border_wall, path_image):
        self.x = x
        self.y = y
        self.images = images
        self.image_number = 0
        self.hit_time = 0
        self.is_destroyed = False
        self.is_border_wall = is_border_wall
        self.path_image = path_image

    def update(self):
        if self.hit_time > 0:
            if self.hit_time + 100 < pygame.time.get_ticks():
                self.image_number += 1
                self.hit_time = pygame.time.get_ticks()
            if self.image_number == 10:
                self.image_number = 0
                self.hit_time = 0
                self.is_destroyed = True

    def hit(self):
        if not self.is_border_wall and self.hit_time == 0:
            self.hit_time = pygame.time.get_ticks()
            self.image_number += 1

    def get_rect(self):
        return self.images[self.image_number].get_rect(topleft=(self.x, self.y))

    def draw(self, screen: pygame.Surface):
        if self.hit_time > 0:
            screen.blit(self.path_image, (self.x, self.y))
        screen.blit(self.images[self.image_number], (self.x, self.y))
