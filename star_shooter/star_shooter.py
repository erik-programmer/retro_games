import random, pygame, sys
from enum import Enum

# Constants
SCREEN_HEIGHT = 300
SCREEN_WIDTH = 400


class Star:
    def __init__(self):
        self.images = [
            pygame.image.load("star_shooter/star1.png"),
            pygame.image.load("star_shooter/star2.png"),
            pygame.image.load("star_shooter/star3.png"),
            pygame.image.load("star_shooter/star4.png"),
            pygame.image.load("star_shooter/star5.png"),
            pygame.image.load("star_shooter/star6.png"),
            pygame.image.load("star_shooter/star7.png"),
            pygame.image.load("star_shooter/star8.png"),
        ]
        self.x = random.randint(0, SCREEN_WIDTH)
        self.image_number = 0
        self.y = 0
        self.hit_time = 0

    def update(self):
        self.y += 0.1
        if self.hit_time > 0:
            if self.hit_time + 100 < pygame.time.get_ticks():
                self.image_number += 1
                self.hit_time = pygame.time.get_ticks()
            if self.image_number == 8:
                self.x = random.randint(0, SCREEN_WIDTH)
                self.image_number = 0
                self.y = 0
                self.hit_time = 0

    def got_hit(self):
        self.hit_time = pygame.time.get_ticks()
        self.image_number += 1

    def get_rect(self):
        return self.images[self.image_number].get_rect(center=(self.x, self.y))

    def draw(self, screen: pygame.Surface):
        rect = self.images[self.image_number].get_rect(center=(self.x, self.y))
        screen.blit(self.images[self.image_number], rect)


class Crosshair:
    def __init__(self):
        self.image = pygame.image.load("star_shooter/crosshair.png")
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2
        self.points = 0

    def process_event(self, event, star):
        if event.type == pygame.MOUSEMOTION:
            self.x, self.y = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.x, self.y = event.pos
            if star.get_rect().collidepoint((self.x, self.y)):
                self.points += 1
                star.got_hit()

    def draw(self, screen: pygame.Surface):
        rect = self.image.get_rect(center=(self.x, self.y))
        screen.blit(self.image, rect)


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Star shooter")

font = pygame.font.Font(None, 25)

crosshair = Crosshair()

star = Star()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        crosshair.process_event(event, star)

    screen.fill((255, 255, 255))

    star.update()
    star.draw(screen)

    crosshair.draw(screen)

    points_img = font.render(f"Points: {crosshair.points}", True, (0, 0, 0))
    screen.blit(points_img, (10, 10))

    pygame.display.flip()
