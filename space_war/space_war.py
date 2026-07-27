import pygame, sys
import random
from enum import Enum

SCREEN_HEIGHT = 800
SCREEN_WIDTH = 1200


def load_images(thing, limit):
    return list(
        pygame.image.load(
            f"space_war/images/asteroid/{thing}_{i:02d}.png"
        ).convert_alpha()
        for i in range(0, limit)
    )


class Asteroid:
    def __init__(self) -> None:
        self.exploding_images = load_images("asteroid_exploding", 15)
        self.y = 0
        self.is_dead = False
        self.images = load_images("asteroid", 15)
        self.image_number = 0
        self.x = random.randint(0, SCREEN_WIDTH - self.images[0].get_width())
        self.timer = pygame.time.get_ticks()

    def get_rect(self):
        return pygame.Rect(
            self.x,
            self.y,
            self.images[self.image_number].get_width(),
            self.images[self.image_number].get_height(),
        )

    def got_hit(self):
        self.is_dead = True

    def update(self):
        if self.timer + 50 < pygame.time.get_ticks():
            self.image_number += 1
            self.timer = pygame.time.get_ticks()
        if self.image_number > 14:
            self.image_number = 0
        self.y += 0.3

    def draw(self, screen):
        screen.blit(self.images[self.image_number], (self.x, self.y))


class Bullet:

    image: pygame.Surface

    def __init__(self, x, y):
        self.x = x - Bullet.image.get_width() / 2
        self.y = y

    def update(self):
        self.y -= 0.8

    def get_rect(self):
        return pygame.Rect(
            self.x,
            self.y,
            Bullet.image.get_width(),
            Bullet.image.get_height(),
        )

    def draw(self, screen):
        screen.blit(Bullet.image, (self.x, self.y))


class Ship:
    def __init__(self) -> None:
        self.image = pygame.image.load("space_war/images/ship.png").convert_alpha()
        self.x = SCREEN_WIDTH / 2 - self.image.get_width() / 2
        self.y = SCREEN_HEIGHT - self.image.get_height()
        self.bullets = []

    def process_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.bullets.append(Bullet(self.x + self.image.get_width() / 2, self.y))

    def process_keys(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= 1
        if keys[pygame.K_RIGHT]:
            self.x += 1

    def check_touched_asteroid(self, asteroid):
        for b in self.bullets:
            if b.get_rect().colliderect(asteroid.get_rect()):
                b.y = -10
                asteroid.got_hit()

    def update(self):
        self.bullets = list(b for b in self.bullets if b.y > 0)
        for b in self.bullets:
            b.update()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        for b in self.bullets:
            b.draw(screen)


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space war")

Bullet.image = pygame.image.load("space_war/images/ship_shot.png").convert_alpha()

font = pygame.font.Font(None, 25)


ship = Ship()
asteroids = []
background_image = pygame.image.load("space_war/images/background.png").convert_alpha()
next_asteroid_time = random.randint(5000, 10000)
time = pygame.time.get_ticks()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        ship.process_event(event)

    ship.update()
    ship.process_keys(pygame.key.get_pressed())
    for a in asteroids:
        a.update()
        ship.check_touched_asteroid(a)

    asteroids = list(a for a in asteroids if not a.is_dead)

    if time + next_asteroid_time < pygame.time.get_ticks():
        time = pygame.time.get_ticks()
        next_asteroid_time = random.randint(5000, 10000)
        asteroids.append(Asteroid())

    screen.blit(background_image, (0, 0))
    for a in asteroids:
        a.draw(screen)
    ship.draw(screen)

    pygame.display.flip()
