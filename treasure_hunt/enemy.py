from enum import Enum

import pygame, random
from utils import *
from constants import *
from wall import Wall
from fire import Fire


class EnemyType(Enum):
    MALE_GOBLIN = 1
    FEMALE_GOBLIN = 2
    CHIEF_GOBLIN = 3
    CAVEMAN = 4


class Enemy:
    def __init__(self, x, y, type: EnemyType):
        self.type = type
        image_dir = ""

        image_dir = self.type.name.lower()
        if self.type == EnemyType.CHIEF_GOBLIN:
            self.lives = 3
        else:
            self.lives = 1

        self.images = {
            pygame.K_RIGHT: load_images(f"enemy/{image_dir}/right", 20)
            + load_images(f"enemy/{image_dir}/right_hurt", 5),
            pygame.K_LEFT: load_images(f"enemy/{image_dir}/left", 20)
            + load_images(f"enemy/{image_dir}/left_hurt", 5),
            pygame.K_UP: load_images(f"enemy/{image_dir}/back", 20)
            + load_images(f"enemy/{image_dir}/back_hurt", 5),
            pygame.K_DOWN: load_images(f"enemy/{image_dir}/front", 20)
            + load_images(f"enemy/{image_dir}/front_hurt", 5),
        }
        self.fires: list[Fire] = []
        self.movement_direction_change_time = 0
        self.image = self.images[pygame.K_DOWN][0]
        self.image_number = 0
        self.x = x
        self.y = y
        self.movement_direction = random.choice([pygame.K_LEFT, pygame.K_UP])
        self.hit_time = 0
        self.is_dead = False
        self.update_counter = 0

    def update(self, directions):
        fs = []
        for f in self.fires:
            if not f.is_dead:
                fs.append(f)
        self.fires = fs

        self.update_counter += 1
        for f in self.fires:
            f.update()
        if self.hit_time == 0:
            if self.movement_direction_change_time + 1000 < pygame.time.get_ticks():
                if (
                    self.type == EnemyType.FEMALE_GOBLIN
                    or self.type == EnemyType.CHIEF_GOBLIN
                    or self.type == EnemyType.CAVEMAN
                ):
                    if directions:
                        self.movement_direction = random.choice(directions)
                        self.movement_direction_change_time = pygame.time.get_ticks()

            if self.movement_direction == pygame.K_LEFT:
                self.image = self.images[pygame.K_LEFT][self.image_number]
                self.image_number += 1
                self.x -= ENEMY_SPEED
            elif self.movement_direction == pygame.K_RIGHT:
                self.image = self.images[pygame.K_RIGHT][self.image_number]
                self.image_number += 1
                self.x += ENEMY_SPEED
            elif self.movement_direction == pygame.K_UP:
                self.image = self.images[pygame.K_UP][self.image_number]
                self.image_number += 1
                self.y -= ENEMY_SPEED
            elif self.movement_direction == pygame.K_DOWN:
                self.image = self.images[pygame.K_DOWN][self.image_number]
                self.image_number += 1
                self.y += ENEMY_SPEED

            if self.image_number == 20:
                self.image_number = 0
            if self.update_counter > 200 and self.type == EnemyType.CAVEMAN:
                self.update_counter = 0
                self.fires.append(Fire(self.x, self.y))
        else:
            if self.hit_time + 100 > pygame.time.get_ticks():
                self.hit_time = pygame.time.get_ticks()
                self.image_number += 1
                self.image = self.images[self.movement_direction][self.image_number]
            if self.image_number > 23:
                if self.lives < 1:
                    self.is_dead = True
                else:
                    self.image_number = 0
                    self.image = self.images[self.movement_direction][self.image_number]
                    self.hit_time = 0

    def hit(self):
        self.hit_time = pygame.time.get_ticks()
        self.image_number = 19
        self.lives -= 1

    def check_touched_wall(self, wall: Wall):
        if wall.get_rect().colliderect(self.get_rect()):
            if self.movement_direction == pygame.K_LEFT:
                self.movement_direction = pygame.K_RIGHT
            elif self.movement_direction == pygame.K_RIGHT:
                self.movement_direction = pygame.K_LEFT
            elif self.movement_direction == pygame.K_UP:
                self.movement_direction = pygame.K_DOWN
            elif self.movement_direction == pygame.K_DOWN:
                self.movement_direction = pygame.K_UP

    def get_rect(self):
        collision_rect = self.image.get_rect(center=(self.x, self.y))
        collision_rect.x += 10
        collision_rect.width -= 20

        return collision_rect

    def draw(self, screen: pygame.Surface):
        # pygame.draw.rect(screen, (255, 50, 50), collision_rect)
        for f in self.fires:
            f.draw(screen)
        rect = self.image.get_rect(center=(self.x, self.y))
        screen.blit(self.image, rect)
