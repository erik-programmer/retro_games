import pygame, sys
import random
from enum import Enum

TILE_SIZE = 32
SCREEN_HEIGHT = TILE_SIZE * 20
SCREEN_WIDTH = TILE_SIZE * 40


class MazeCellType(Enum):
    WALL = 1
    FRUIT = 2
    EMPTY = 3
    POINT = 4


class Enemy:
    def __init__(self, x, color) -> None:
        self.x = x
        self.y = SCREEN_HEIGHT // 2
        self.timer = pygame.time.get_ticks()
        self.image_number = 0
        self.direction = pygame.K_RIGHT
        self.images = {
            pygame.K_DOWN: [
                pygame.image.load(f"pacman/images/monster/{color}_down_0.png"),
                pygame.image.load(f"pacman/images/monster/{color}_down_1.png"),
            ],
            pygame.K_UP: [
                pygame.image.load(f"pacman/images/monster/{color}_up_0.png"),
                pygame.image.load(f"pacman/images/monster/{color}_up_1.png"),
            ],
            pygame.K_LEFT: [
                pygame.image.load(f"pacman/images/monster/{color}_left_0.png"),
                pygame.image.load(f"pacman/images/monster/{color}_left_1.png"),
            ],
            pygame.K_RIGHT: [
                pygame.image.load(f"pacman/images/monster/{color}_right_0.png"),
                pygame.image.load(f"pacman/images/monster/{color}_right_1.png"),
            ],
        }

    def get_rect(self):
        return pygame.Rect(
            self.x,
            self.y,
            self.images[self.direction][self.image_number].get_width(),
            self.images[self.direction][self.image_number].get_height(),
        )

    def animate(self):
        if self.timer + 300 < pygame.time.get_ticks():
            if self.image_number == 0:
                self.image_number = 1
            else:
                self.image_number = 0
            self.timer = pygame.time.get_ticks()

    def get_possible_directions(self, has_wall, direction_to_check):
        directions = []
        if not has_wall:
            if self.direction == direction_to_check:
                directions.append(direction_to_check)
                directions.append(direction_to_check)
            directions.append(direction_to_check)
        return directions

    def update(self, fn):
        if self.x % TILE_SIZE == 0 and self.y % TILE_SIZE == 0:
            directions = []
            directions += self.get_possible_directions(
                fn(int(self.y // TILE_SIZE), int(self.x // TILE_SIZE - 1)),
                pygame.K_LEFT,
            )
            directions += self.get_possible_directions(
                fn(int(self.y // TILE_SIZE), int(self.x // TILE_SIZE + 1)),
                pygame.K_RIGHT,
            )
            directions += self.get_possible_directions(
                fn(int(self.y // TILE_SIZE + 1), int(self.x // TILE_SIZE)),
                pygame.K_DOWN,
            )
            directions += self.get_possible_directions(
                fn(int(self.y // TILE_SIZE - 1), int(self.x // TILE_SIZE)),
                pygame.K_UP,
            )
            self.direction = random.choice(directions)
        if self.direction == pygame.K_RIGHT:
            self.x += 1
            self.animate()
        elif self.direction == pygame.K_LEFT:
            self.x -= 1
            self.animate()
        elif self.direction == pygame.K_DOWN:
            self.y += 1
            self.animate()
        elif self.direction == pygame.K_UP:
            self.y -= 1
            self.animate()

    def draw(self, screen):
        screen.blit(self.images[self.direction][self.image_number], (self.x, self.y))


class Maze:
    def __init__(self) -> None:
        self.timer = pygame.time.get_ticks()
        self.color = 0
        self.fruit_image = pygame.image.load("pacman/images/fruit.png")
        self.cells: list[list[MazeCellType]] = [
            [
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
            ],
            [
                MazeCellType.WALL,
                MazeCellType.FRUIT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.FRUIT,
                MazeCellType.WALL,
            ],
            [
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
            ],
            [
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
            ],
            [
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
            ],
            [
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
            ],
            [
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
            ],
            [
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
            ],
            [
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
            ],
            [
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
            ],
            [
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
            ],
            [
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
            ],
            [
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
            ],
            [
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
            ],
            [
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
            ],
            [
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
            ],
            [
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
            ],
            [
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
            ],
            [
                MazeCellType.WALL,
                MazeCellType.FRUIT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.WALL,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.POINT,
                MazeCellType.FRUIT,
                MazeCellType.WALL,
            ],
            [
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
                MazeCellType.WALL,
            ],
        ]

    def on_pacman_changed_cell(self, row, column, fn):
        if self.cells[row][column] == MazeCellType.POINT:
            self.cells[row][column] = MazeCellType.EMPTY
            fn()

    def check_is_wall(self, row, culuomn):
        return self.cells[row][culuomn] == MazeCellType.WALL

    def is_empty(self):
        for r in self.cells:
            for c in r:
                if c == MazeCellType.POINT:
                    return False
        return True

    def draw(self, screen):
        for ic, row in enumerate(self.cells):
            for ir, c in enumerate(row):
                if c == MazeCellType.POINT:
                    if self.color == 0:
                        pygame.draw.circle(
                            screen,
                            (109, 165, 25),
                            (
                                ir * TILE_SIZE + TILE_SIZE / 2,
                                ic * TILE_SIZE + TILE_SIZE / 2,
                            ),
                            5,
                        )
                        if self.timer + 1000 < pygame.time.get_ticks():
                            self.color = 1
                            self.timer = pygame.time.get_ticks()
                    elif self.color == 1:
                        pygame.draw.circle(
                            screen,
                            (255, 165, 0),
                            (
                                ir * TILE_SIZE + TILE_SIZE / 2,
                                ic * TILE_SIZE + TILE_SIZE / 2,
                            ),
                            5,
                        )
                        if self.timer + 1000 < pygame.time.get_ticks():
                            self.color = 2
                            self.timer = pygame.time.get_ticks()
                    elif self.color == 2:
                        pygame.draw.circle(
                            screen,
                            (255, 255, 255),
                            (
                                ir * TILE_SIZE + TILE_SIZE / 2,
                                ic * TILE_SIZE + TILE_SIZE / 2,
                            ),
                            5,
                        )
                        if self.timer + 1000 < pygame.time.get_ticks():
                            self.color = 0
                            self.timer = pygame.time.get_ticks()

                if c == MazeCellType.WALL:
                    pygame.draw.rect(
                        screen,
                        (255, 0, 255),
                        (ir * TILE_SIZE, ic * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                        5,
                    )
                if c == MazeCellType.FRUIT:
                    screen.blit(self.fruit_image, (ir * TILE_SIZE, ic * TILE_SIZE))


class Pacman:
    def __init__(self) -> None:
        self.is_dead = False
        self.points = 0
        self.lives = 3
        self.images = {
            pygame.K_RIGHT: [
                pygame.image.load("pacman/images/pacman/pacman_right_0.png"),
                pygame.image.load("pacman/images/pacman/pacman_right_1.png"),
            ],
            pygame.K_LEFT: [
                pygame.image.load("pacman/images/pacman/pacman_left_0.png"),
                pygame.image.load("pacman/images/pacman/pacman_left_1.png"),
            ],
            pygame.K_DOWN: [
                pygame.image.load("pacman/images/pacman/pacman_down_0.png"),
                pygame.image.load("pacman/images/pacman/pacman_down_1.png"),
            ],
            pygame.K_UP: [
                pygame.image.load("pacman/images/pacman/pacman_up_0.png"),
                pygame.image.load("pacman/images/pacman/pacman_up_1.png"),
            ],
            "dead_images": [
                pygame.image.load("pacman/images/pacman/pacman_dead_0.png"),
                pygame.image.load("pacman/images/pacman/pacman_dead_1.png"),
                pygame.image.load("pacman/images/pacman/pacman_dead_2.png"),
                pygame.image.load("pacman/images/pacman/pacman_dead_3.png"),
                pygame.image.load("pacman/images/pacman/pacman_dead_4.png"),
                pygame.image.load("pacman/images/pacman/pacman_dead_5.png"),
                pygame.image.load("pacman/images/pacman/pacman_dead_6.png"),
                pygame.image.load("pacman/images/pacman/pacman_dead_7.png"),
                pygame.image.load("pacman/images/pacman/pacman_dead_8.png"),
                pygame.image.load("pacman/images/pacman/pacman_dead_9.png"),
                pygame.image.load("pacman/images/pacman/pacman_dead_10.png"),
            ],
        }
        self.x = 64
        self.y = 64
        self.image_number = 1
        self.showed_dead_images = False
        self.timer = pygame.time.get_ticks()
        self.direction = None

    def change_points(self):
        self.points += 1

    def restart(self):
        self.image_number = 1
        self.direction = None
        self.is_dead = False
        self.showed_dead_images = False
        self.x = 64
        self.y = 64

    def get_rect(self):
        if self.direction != None:
            return pygame.Rect(
                self.x,
                self.y,
                self.images[self.direction][self.image_number].get_width(),
                self.images[self.direction][self.image_number].get_height(),
            )
        else:
            return pygame.Rect(
                self.x,
                self.y,
                self.images[pygame.K_RIGHT][1].get_width(),
                self.images[pygame.K_RIGHT][self.image_number].get_height(),
            )

    def update(self):
        if self.is_dead:
            if self.timer + 300 < pygame.time.get_ticks():
                self.image_number += 1
                self.timer = pygame.time.get_ticks()
            if self.image_number == 10:
                self.showed_dead_images = True

    def set_dead(self):
        self.lives -= 1
        self.direction = "dead_images"
        self.image_number = 0
        self.is_dead = True

    def checked_touched_enemy(self, enemy):
        return self.get_rect().colliderect(enemy.get_rect())

    def process_keys(self, keys, points_callbsck_fn, check_touched_wall_fn):
        if self.is_dead:
            return

        touched_wall = False
        if self.direction == pygame.K_LEFT or keys[pygame.K_LEFT]:
            if (
                self.x % TILE_SIZE == 0 and self.y % TILE_SIZE == 0
            ) or self.direction == pygame.K_LEFT:
                if self.x % TILE_SIZE == 0 and self.y % TILE_SIZE == 0:
                    points_callbsck_fn(
                        int(self.y // TILE_SIZE),
                        int(self.x // TILE_SIZE),
                        self.change_points,
                    )
                    if check_touched_wall_fn(
                        int(self.y // TILE_SIZE), int(self.x // TILE_SIZE - 1)
                    ):
                        touched_wall = True
                if not touched_wall:
                    self.x -= 1
                    if self.timer + 200 < pygame.time.get_ticks():
                        self.image_number = 1 if self.image_number == 0 else 0
                        self.timer = pygame.time.get_ticks()
                else:
                    self.image_number = 1
                self.direction = pygame.K_LEFT

        if self.direction == pygame.K_RIGHT or keys[pygame.K_RIGHT]:
            if (
                self.x % TILE_SIZE == 0 and self.y % TILE_SIZE == 0
            ) or self.direction == pygame.K_RIGHT:
                if self.x % TILE_SIZE == 0 and self.y % TILE_SIZE == 0:
                    points_callbsck_fn(
                        int(self.y // TILE_SIZE),
                        int(self.x // TILE_SIZE),
                        self.change_points,
                    )
                    if check_touched_wall_fn(
                        int(self.y // TILE_SIZE), int(self.x // TILE_SIZE + 1)
                    ):
                        touched_wall = True
                if not touched_wall:
                    self.x += 1
                    if self.timer + 200 < pygame.time.get_ticks():
                        self.image_number = 1 if self.image_number == 0 else 0
                        self.timer = pygame.time.get_ticks()
                else:
                    self.image_number = 1
                self.direction = pygame.K_RIGHT
        if self.direction == pygame.K_UP or keys[pygame.K_UP]:
            if (
                self.x % TILE_SIZE == 0 and self.y % TILE_SIZE == 0
            ) or self.direction == pygame.K_UP:
                if self.x % TILE_SIZE == 0 and self.y % TILE_SIZE == 0:
                    points_callbsck_fn(
                        int(self.y // TILE_SIZE),
                        int(self.x // TILE_SIZE),
                        self.change_points,
                    )
                    if check_touched_wall_fn(
                        int(self.y // TILE_SIZE - 1), int(self.x // TILE_SIZE)
                    ):
                        touched_wall = True
                if not touched_wall:
                    self.y -= 1
                    if self.timer + 200 < pygame.time.get_ticks():
                        self.image_number = 1 if self.image_number == 0 else 0
                        self.timer = pygame.time.get_ticks()
                else:
                    self.image_number = 1
                self.direction = pygame.K_UP
        if self.direction == pygame.K_DOWN or keys[pygame.K_DOWN]:
            if (
                self.x % TILE_SIZE == 0 and self.y % TILE_SIZE == 0
            ) or self.direction == pygame.K_DOWN:
                if self.x % TILE_SIZE == 0 and self.y % TILE_SIZE == 0:
                    points_callbsck_fn(
                        int(self.y // TILE_SIZE),
                        int(self.x // TILE_SIZE),
                        self.change_points,
                    )
                    if check_touched_wall_fn(
                        int(self.y // TILE_SIZE + 1), int(self.x // TILE_SIZE)
                    ):
                        touched_wall = True
                if not touched_wall:
                    self.y += 1
                    if self.timer + 200 < pygame.time.get_ticks():
                        self.image_number = 1 if self.image_number == 0 else 0
                        self.timer = pygame.time.get_ticks()
                else:
                    self.image_number = 1
                self.direction = pygame.K_DOWN

    def draw(self, screen):
        info_image = pygame.font.Font(None, 25).render(
            f"Points: {self.points}, Lives: {self.lives}", True, (255, 255, 255)
        )

        screen.blit(info_image, (5, 10))
        if self.direction != None:
            screen.blit(
                self.images[self.direction][self.image_number], (self.x, self.y)
            )
        else:
            screen.blit(self.images[pygame.K_RIGHT][1], (self.x, self.y))


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pacman")


def create_new_enemies():
    return [
        Enemy(20 * TILE_SIZE, "blue"),
        Enemy(25 * TILE_SIZE, "red"),
        Enemy(15 * TILE_SIZE, "rosa"),
    ]


pacman = Pacman()
enemies = create_new_enemies()
maze = Maze()
should_enemies_move = True
is_game_finished = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((0, 0, 0))

    if pacman.lives == 0:
        is_game_finished = True

    if not is_game_finished:

        if should_enemies_move:
            for enemy in enemies:
                enemy.update(maze.check_is_wall)

            for enemy in enemies:
                if pacman.checked_touched_enemy(enemy) and should_enemies_move:
                    pacman.set_dead()
                    should_enemies_move = False

        pacman.update()

        if pacman.showed_dead_images:
            should_enemies_move = True
            pacman.restart()
            enemies = create_new_enemies()

        pacman.process_keys(
            pygame.key.get_pressed(),
            maze.on_pacman_changed_cell,
            maze.check_is_wall,
        )
    for enemy in enemies:
        enemy.draw(screen)
    maze.draw(screen)
    pacman.draw(screen)
    if is_game_finished and not maze.is_empty():
        game_over_image = pygame.font.Font(None, 50).render(
            f"Game over", True, (144, 238, 144)
        )
        screen.blit(game_over_image, (SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT // 2 - 40))
    if maze.is_empty():
        is_game_finished = True
        win_image = pygame.font.Font(None, 50).render(f"You Won", True, (144, 238, 144))
        screen.blit(win_image, (SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT // 2 - 40))
    pygame.display.flip()
