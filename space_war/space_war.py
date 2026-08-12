import pygame, sys
import random
from enum import Enum

SCREEN_HEIGHT = 800
SCREEN_WIDTH = 1200


def load_images(image_folder, obj, limit):
    return list(
        pygame.image.load(
            f"space_war/images/{image_folder}/{obj}_{i:02d}.png"
        ).convert_alpha()
        for i in range(0, limit)
    )


class Asteroid:

    exploding_images: list[pygame.Surface]
    images: list[pygame.Surface]

    def __init__(self, points) -> None:
        self.y = 0
        self.speed = 0.3 if points < 10 else 0.4
        self.is_dead = False
        self.showed_exploding_images = False
        self.image_number = 0
        self.x = random.randint(0, SCREEN_WIDTH - Asteroid.images[0].get_width())
        self.timer = pygame.time.get_ticks()
        self.max_image_number = 15

    def get_rect(self):
        return pygame.Rect(
            self.x,
            self.y,
            Asteroid.images[self.image_number].get_width(),
            Asteroid.images[self.image_number].get_height(),
        )

    def got_hit(self, change_points_fn):
        if not self.is_dead:
            self.is_dead = True
            self.image_number = 0
            self.max_image_number = 9
            change_points_fn()

    def update(self):
        if self.timer + 50 < pygame.time.get_ticks():
            self.image_number += 1
            self.timer = pygame.time.get_ticks()
        if self.image_number > self.max_image_number:
            self.image_number = 0
            if self.is_dead:
                self.showed_exploding_images = True
        self.y += self.speed

    def check_touched_border(self):
        if self.y + Asteroid.images[0].get_height() > SCREEN_HEIGHT:
            self.showed_exploding_images = True
            ship.change_lives(-1)

    def draw(self, screen):
        if not self.is_dead:
            screen.blit(Asteroid.images[self.image_number], (self.x, self.y))
        else:
            screen.blit(Asteroid.exploding_images[self.image_number], (self.x, self.y))


class Phantom:

    image: pygame.Surface
    exploding_images: list[pygame.Surface]

    def __init__(self, points) -> None:
        self.showed_exploding_images = False
        self.y = 0
        self.speed = 0.3 if points < 40 else 0.4
        self.is_dead = False
        self.x = random.randint(0, SCREEN_WIDTH - Phantom.image.get_width())
        self.timer = pygame.time.get_ticks()
        self.is_visible = True

    def get_rect(self):
        return pygame.Rect(
            self.x,
            self.y,
            Phantom.image.get_width(),
            Phantom.image.get_height(),
        )

    def got_hit(self, change_points_fn):
        if not self.is_dead:
            self.is_visible = True
            self.is_dead = True
            self.exploding_timer = pygame.time.get_ticks()
            self.exploding_image_number = 0
            change_points_fn()

    def update(self):
        if self.is_dead:
            if self.exploding_timer + 50 < pygame.time.get_ticks():
                if 8 > self.exploding_image_number:
                    self.exploding_image_number += 1
                    self.exploding_timer = pygame.time.get_ticks()
                else:
                    self.showed_exploding_images = True
        else:
            self.y += self.speed
            if self.timer + 1000 < pygame.time.get_ticks():
                self.timer = pygame.time.get_ticks()
                self.is_visible = not self.is_visible

    def check_touched_border(self):
        if self.y + Phantom.image.get_height() > SCREEN_HEIGHT and not self.is_dead:
            self.got_hit(lambda: None)
            ship.change_lives(-1)

    def draw(self, screen):
        if self.is_visible:
            if not self.is_dead:
                screen.blit(Phantom.image, (self.x, self.y))
            else:
                screen.blit(
                    Phantom.exploding_images[self.exploding_image_number],
                    (self.x, self.y),
                )


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


class Bomb:
    def __init__(self) -> None:
        self.image = pygame.image.load("space_war/images/bomb.png").convert_alpha()
        self.x = random.randint(0, SCREEN_WIDTH - self.image.get_width())
        self.y = 0
        self.is_caught = False

    def get_rect(self):
        return pygame.Rect(
            self.x,
            self.y,
            self.image.get_width(),
            self.image.get_height(),
        )

    def check_touched_border(self):
        return self.y + self.image.get_height() > SCREEN_HEIGHT

    def update(self):
        self.y += 0.3

    def caught(self, fn):
        self.is_caught = True
        fn()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class Heart:
    def __init__(self) -> None:
        self.image = pygame.image.load("space_war/images/heart.png").convert_alpha()
        self.x = random.randint(0, SCREEN_WIDTH - self.image.get_width())
        self.y = 0
        self.is_caught = False

    def get_rect(self):
        return pygame.Rect(
            self.x,
            self.y,
            self.image.get_width(),
            self.image.get_height(),
        )

    def update(self):
        self.y += 0.3

    def check_touched_border(self):
        return self.y + self.image.get_height() > SCREEN_HEIGHT

    def caught(self, fn):
        self.is_caught = True
        fn()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class Ship:
    def __init__(self) -> None:
        self.points = 0
        self.lives = 3
        self.image = pygame.image.load("space_war/images/ship.png").convert_alpha()
        self.x = SCREEN_WIDTH / 2 - self.image.get_width() / 2
        self.y = SCREEN_HEIGHT - self.image.get_height()
        heart_image = pygame.image.load("space_war/images/heart.png").convert_alpha()
        self.scaled_heart_image = pygame.transform.scale(heart_image, (30, 30))
        self.bullets = []
        self.bomb_image = pygame.image.load("space_war/images/bomb.png").convert_alpha()
        self.scaled_bomb_image = pygame.transform.scale(self.bomb_image, (30, 30))
        self.bombs = 0

    def process_event(self, event, delete_all_enemies):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.bullets.append(Bullet(self.x + self.image.get_width() / 2, self.y))
        if event.type == pygame.KEYDOWN and event.key == pygame.K_x and self.bombs > 0:
            self.bombs -= 1
            delete_all_enemies()

    def process_keys(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= 1
        if keys[pygame.K_RIGHT]:
            self.x += 1

    def change_points(self):
        self.points += 1

    def change_lives(self, lives):
        self.lives += lives

    def change_bombs(self):
        self.bombs += 1

    def get_rect(self):
        return pygame.Rect(
            self.x,
            self.y,
            self.image.get_width(),
            self.image.get_height(),
        )

    def check_bullet_touched_asteroid(self, asteroid):
        for b in self.bullets:
            if b.get_rect().colliderect(asteroid.get_rect()):
                b.y = -10
                asteroid.got_hit(self.change_points)

    def check_bullet_touched_phantom(self, phantom):
        if phantom.is_visible:
            for b in self.bullets:
                if b.get_rect().colliderect(phantom.get_rect()):
                    b.y = -10
                    phantom.got_hit(self.change_points)

    def check_touched_heart(self, heart):
        if heart.get_rect().colliderect(self.get_rect()):
            heart.caught(lambda: self.change_lives(1))

    def check_touched_bomb(self, bomb):
        if bomb.get_rect().colliderect(self.get_rect()):
            bomb.caught(lambda: self.change_bombs())

    def check_touched_asteroid(self, asteroid):
        if not asteroid.is_dead:
            if self.get_rect().colliderect(asteroid.get_rect()):
                self.change_lives(-1)
                asteroid.got_hit(lambda: None)

    def check_touched_phantom(self, phantom):
        if not phantom.is_dead:
            if self.get_rect().colliderect(phantom.get_rect()):
                self.change_lives(-1)
                phantom.got_hit(lambda: None)

    def update(self):
        self.bullets = list(b for b in self.bullets if b.y > 0)
        for b in self.bullets:
            b.update()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        for b in self.bullets:
            b.draw(screen)
        for i in range(1, self.lives + 1):
            screen.blit(self.scaled_heart_image, (i * 25, 25))
        for i in range(1, self.bombs + 1):
            screen.blit(self.scaled_bomb_image, (i * 25, 60))

        level = self.points // 10
        for i in range(1, level + 1):
            pygame.draw.rect(
                screen,
                (255, 0, 0),
                (i * 28, 10, 20, 12),
                0,  # Border thickness
            )
        for i in range(level + 1, 11):
            pygame.draw.rect(
                screen,
                (255, 0, 0),
                (i * 28, 10, 20, 12),
                2,  # Border thickness
            )


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space war")

Bullet.image = pygame.image.load("space_war/images/ship_shot.png").convert_alpha()
Asteroid.exploding_images = load_images("asteroid", "asteroid_exploding", 10)
Asteroid.images = load_images("asteroid", "asteroid", 16)
Phantom.image = pygame.image.load("space_war/images/phantom/phantom.png")
Phantom.exploding_images = load_images("phantom", "phantom_exploding", 9)

font = pygame.font.Font(None, 25)
asteroids = []
phantoms = []


def delete_all_enemies():
    for a in asteroids:
        a.got_hit(ship.change_points)
    for p in phantoms:
        p.got_hit(ship.change_points)


ship = Ship()
heart = None
bomb = None
background_image = pygame.image.load("space_war/images/background.png").convert_alpha()
next_asteroid_time = random.randint(5000, 10000)
time = pygame.time.get_ticks()
next_phantom_time = random.randint(5000, 10000)
phantom_time = pygame.time.get_ticks()
heart_time = pygame.time.get_ticks()
win_img_height = 17
win_img_width = 90
loose_img_height = 17
loose_img_width = 90
next_heart_time = random.randint(30000, 60000)
bomb_time = pygame.time.get_ticks()
next_bomb_time = random.randint(70000, 110000)
is_game_finshed = False
angle = 0
while True:
    points = ship.points
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        ship.process_event(event, delete_all_enemies)
    if ship.lives < 1:
        is_game_finshed = True
    if points >= 100:
        is_game_finshed = True
    if not is_game_finshed:
        ship.update()
        if heart != None:
            if heart.check_touched_border():
                heart = None
        if bomb != None:
            if bomb.check_touched_border():
                bomb = None
        if heart != None:
            heart.update()
        if bomb != None:
            bomb.update()
        ship.process_keys(pygame.key.get_pressed())
        for a in asteroids:
            a.update()
            a.check_touched_border()
            ship.check_bullet_touched_asteroid(a)
            ship.check_touched_asteroid(a)
        for p in phantoms:
            p.update()
            p.check_touched_border()
            ship.check_bullet_touched_phantom(p)
            ship.check_touched_phantom(p)

        asteroids = list(a for a in asteroids if not a.showed_exploding_images)
        phantoms = list(p for p in phantoms if not p.showed_exploding_images)
        if heart != None:
            ship.check_touched_heart(heart)
            if heart.is_caught:
                heart = None
        if bomb != None:
            ship.check_touched_bomb(bomb)
            if bomb.is_caught:
                bomb = None

        if time + next_asteroid_time < pygame.time.get_ticks():
            time = pygame.time.get_ticks()
            if points < 10:
                next_asteroid_time = random.randint(5000, 10000)
                asteroids.append(Asteroid(points))
            if points >= 10 and points < 20:
                next_asteroid_time = random.randint(5000, 10000)
                asteroids.append(Asteroid(points))
            if points > 19:
                next_asteroid_time = random.randint(3000, 5000)
                asteroids.append(Asteroid(points))

        if points >= 40 and phantom_time + next_phantom_time < pygame.time.get_ticks():
            phantom_time = pygame.time.get_ticks()
            if points >= 40 and points < 50:
                next_phantom_time = random.randint(5000, 10000)
                phantoms.append(Phantom(points))
            if points >= 50 and points < 60:
                next_phantom_time = random.randint(5000, 10000)
                phantoms.append(Phantom(points))
            if points > 60:
                next_phantom_time = random.randint(3000, 5000)
                phantoms.append(Phantom(points))

        if heart_time + next_heart_time < pygame.time.get_ticks():
            heart_time = pygame.time.get_ticks()
            next_heart_time = random.randint(30000, 60000)
            heart = Heart()

        if bomb_time + next_bomb_time < pygame.time.get_ticks():
            bomb_time = pygame.time.get_ticks()
            next_bomb_time = random.randint(70000, 110000)
            bomb = Bomb()

    screen.blit(background_image, (0, 0))
    for a in asteroids:
        a.draw(screen)
    for p in phantoms:
        p.draw(screen)
    ship.draw(screen)
    if heart != None:
        heart.draw(screen)
    if bomb != None:
        bomb.draw(screen)
    if points >= 100:
        if angle < 361:
            win_img_height += 1
            win_img_width += 1
            angle += 1
        win_img = font.render(f"YOU WON!", True, (0, 255, 0))
        scaled_win_image = pygame.transform.scale(
            win_img, (win_img_width, win_img_height)
        )
        rotated_img = pygame.transform.rotate(scaled_win_image, angle)
        rect = rotated_img.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(rotated_img, rect)
    if ship.lives < 1:
        if angle < 361:
            loose_img_height += 1
            loose_img_width += 1
            angle += 1
        loose_img = font.render(f"GAME OVER :-(", True, (255, 0, 0))
        scaled_loose_image = pygame.transform.scale(
            loose_img, (loose_img_width, loose_img_height)
        )
        rotated_img = pygame.transform.rotate(scaled_loose_image, angle)
        rect = rotated_img.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(rotated_img, rect)

    pygame.display.flip()
