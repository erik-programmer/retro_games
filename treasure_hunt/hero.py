import pygame
from utils import *
from constants import *
from wall import Wall
from enemy import Enemy
from star import Star


class Hero:
    def __init__(self, x, y):

        self.images = {
            pygame.K_RIGHT: load_images("assassin/right", 20),
            pygame.K_LEFT: load_images("assassin/left", 20),
            pygame.K_UP: load_images("assassin/back", 20),
            pygame.K_DOWN: load_images("assassin/front", 20),
        }
        self.points = 0
        self.image = self.images[pygame.K_DOWN][0]
        self.image_number = 0
        self.x = x
        self.y = y
        self.movement_direction = pygame.K_DOWN
        self.stars: list[Star] = []
        self.star_image = pygame.image.load("treasure_hunt/images/star.png")
        self.stars_spend = 0
        self.lives = 3
        self.blink_counter = -1

    def start_new_level(self, x, y):
        self.image = self.images[pygame.K_DOWN][0]
        self.image_number = 0
        self.lives = 3
        self.x = x
        self.y = y
        self.stars_spend = 0
        self.points = 0
        self.movement_direction = pygame.K_DOWN
        self.stars: list[Star] = []

    def go_to_prev_position(self):
        self.x = self.prev_x
        self.y = self.prev_y
        self.image_number = 0
        self.image = self.images[self.movement_direction][0]

    def check_touched_wall(self, wall: Wall):
        if wall.get_rect().colliderect(self.get_rect()):
            self.go_to_prev_position()

        r = []
        for s in self.stars:
            if wall.get_rect().colliderect(s.get_rect()):
                r.append(s)
                wall.hit()

        self.stars = [s for s in self.stars if s not in r]

    def check_touched_enemy(self, enemy: Enemy):
        if enemy.get_rect().colliderect(self.get_rect()) and self.blink_counter == -1:
            self.lives -= 1
            self.blink_counter = 0
        for f in enemy.fires:
            if f.get_rect().colliderect(self.get_rect()) and self.blink_counter == -1:
                self.lives -= 1
                self.blink_counter = 0
            
        

        r = []
        for s in self.stars:
            if enemy.get_rect().colliderect(s.get_rect()):
                r.append(s)
                enemy.hit()
        self.stars = [s for s in self.stars if s not in r]

    def update(self, keys):
        self.prev_x = self.x
        self.prev_y = self.y
        was_moved = False

        if keys[pygame.K_LEFT]:
            self.image = self.images[pygame.K_LEFT][self.image_number]
            self.image_number += 1
            was_moved = True
            self.x -= HERO_SPEED
            self.movement_direction = pygame.K_LEFT
        elif keys[pygame.K_RIGHT]:
            self.image = self.images[pygame.K_RIGHT][self.image_number]
            self.image_number += 1
            was_moved = True
            self.x += HERO_SPEED
            self.movement_direction = pygame.K_RIGHT
        elif keys[pygame.K_UP]:
            self.image = self.images[pygame.K_UP][self.image_number]
            self.image_number += 1
            was_moved = True
            self.y -= HERO_SPEED
            self.movement_direction = pygame.K_UP
        elif keys[pygame.K_DOWN]:
            self.image = self.images[pygame.K_DOWN][self.image_number]
            self.image_number += 1
            was_moved = True
            self.y += HERO_SPEED
            self.movement_direction = pygame.K_DOWN
        if not was_moved:
            self.image_number = 0
            self.image = self.images[self.movement_direction][0]
        if self.image_number == 20:
            self.image_number = 0
        for s in self.stars:
            s.update()
        if self.blink_counter > -1:
            self.blink_counter += 1
        if self.blink_counter > 20:
            self.blink_counter = -1

    def process_event(self, event):
        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_SPACE
          #  and (self.points // 5 - self.stars_spend) > 0
        ):
            self.stars.append(
                Star(self.x, self.y, self.star_image, self.movement_direction)
            )
            self.stars_spend += 1

    def change_points(self):
        self.points += 1

    def change_lives(self):
        self.lives += 1

    def get_rect(self):
        collision_rect = self.image.get_rect(center=(self.x, self.y))
        collision_rect.x += 10
        collision_rect.width -= 20
        collision_rect.y += 1
        collision_rect.height -= 2

        return collision_rect

    def is_alive(self):
        return self.lives > 0

    def draw(self, screen: pygame.Surface, font):
        rect = self.image.get_rect(center=(self.x, self.y))
        if self.blink_counter % 2 == 1 or self.blink_counter == -1:
            screen.blit(self.image, rect)
        points_img = font.render(f"Coins: {self.points}", True, (255, 255, 255))
        screen.blit(points_img, (0, 0))
        stars_img = font.render(
            f"Stars: {self.points//5-self.stars_spend}", True, (255, 255, 255)
        )
        screen.blit(stars_img, (0, 25))
        lives_img = font.render(f"Lives: {self.lives}", True, (255, 255, 255))
        screen.blit(lives_img, (0, 50))
        for s in self.stars:
            s.draw(screen)
