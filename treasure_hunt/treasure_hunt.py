import random, pygame, sys
from enum import Enum

TILE_SIZE = 64
SCREEN_HEIGHT = TILE_SIZE * 12
SCREEN_WIDTH = TILE_SIZE * 15
HERO_SPEED = TILE_SIZE // 8
ENEMY_SPEED = TILE_SIZE // 16


class EnemyType(Enum):
    MALE_GOBLIN = 1
    FEMALE_GOBLIN = 2
    CHIEF_GOBLIN = 3


def load_images(path, limit):
    return list(
        pygame.image.load(f"treasure_hunt/images/{path}_{i:02d}.png")
        for i in range(0, limit)
    )


class Path:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

    def get_rect(self):
        return self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, (self.x, self.y))


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
        self.movement_direction_change_time = 0
        self.image = self.images[pygame.K_DOWN][0]
        self.image_number = 0
        self.x = x
        self.y = y
        self.movement_direction = random.choice([pygame.K_LEFT, pygame.K_UP])
        self.hit_time = 0
        self.is_dead = False

    def update(self, directions):
        if self.hit_time == 0:
            if self.movement_direction_change_time + 1000 < pygame.time.get_ticks():
                if (
                    self.type == EnemyType.FEMALE_GOBLIN
                    or self.type == EnemyType.CHIEF_GOBLIN
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
        else:
            if self.hit_time + 100 > pygame.time.get_ticks():
                self.hit_time = pygame.time.get_ticks()
                self.image_number += 1
                self.image = self.images[self.movement_direction][self.image_number]
            if self.image_number > 23:
                if self.lives == 0:
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
        collision_rect = self.image.get_rect(center=(self.x, self.y))
        collision_rect.x += 10
        collision_rect.width -= 20
        # pygame.draw.rect(screen, (255, 50, 50), collision_rect)
        rect = self.image.get_rect(center=(self.x, self.y))
        screen.blit(self.image, rect)


class Maze:
    def __init__(self, level) -> None:
        self.coin_images = load_images("coin/coin", 8) + load_images(
            "coin/collected_coin", 6
        )

        self.path_image = pygame.image.load("treasure_hunt/images/path.png")
        self.wall_images = load_images("wall/wall_impact", 10)
        self.paths: list[Path] = []
        self.walls: list[Wall] = []
        self.enemies: list[Enemy] = []
        self.level = level

        for x in range(1, SCREEN_WIDTH // TILE_SIZE - 1):
            for y in range(1, SCREEN_HEIGHT // TILE_SIZE - 1):
                if random.randint(0, 4) == 4:
                    self.walls.append(
                        Wall(
                            x * TILE_SIZE,
                            y * TILE_SIZE,
                            self.wall_images,
                            False,
                            self.path_image,
                        )
                    )
                else:
                    self.paths.append(
                        Path(x * TILE_SIZE, y * TILE_SIZE, self.path_image)
                    )
        for x in range(0, SCREEN_WIDTH // TILE_SIZE):
            self.walls.append(
                Wall(x * TILE_SIZE, 0, self.wall_images, True, self.path_image)
            )
            self.walls.append(
                Wall(
                    x * TILE_SIZE,
                    SCREEN_HEIGHT - TILE_SIZE,
                    self.wall_images,
                    True,
                    self.path_image,
                )
            )
        for y in range(1, SCREEN_HEIGHT // TILE_SIZE - 1):
            self.walls.append(
                Wall(0, y * TILE_SIZE, self.wall_images, True, self.path_image)
            )
            self.walls.append(
                Wall(
                    SCREEN_WIDTH - TILE_SIZE,
                    y * TILE_SIZE,
                    self.wall_images,
                    True,
                    self.path_image,
                )
            )
        ps = random.sample(self.paths, random.choice(range(1, 11)))
        self.coins = list(Coin(p.x, p.y, self.coin_images) for p in ps)
        ps = random.sample(self.paths, 2)
        self.enemies = list(
            Enemy(p.get_rect().centerx, p.get_rect().centery, EnemyType.MALE_GOBLIN)
            for p in ps
        )
        p = random.choice(self.paths)
        self.enemies.append(
            Enemy(p.get_rect().centerx, p.get_rect().centery, EnemyType.FEMALE_GOBLIN)
        )
        p = random.choice(self.paths)
        self.enemies.append(
            Enemy(p.get_rect().centerx, p.get_rect().centery, EnemyType.CHIEF_GOBLIN)
        )

    def get_possible_directions(self, enemy: Enemy):
        r = []
        ep = next(
            (
                p
                for p in self.paths
                if p.get_rect().centerx == enemy.get_rect().centerx
                and p.get_rect().centery == enemy.get_rect().centery
            ),
            None,
        )
        if not ep:
            return r
        if any(
            p.get_rect().centerx - TILE_SIZE == ep.get_rect().centerx
            and p.get_rect().centery == ep.get_rect().centery
            for p in self.paths
        ):
            r.append(pygame.K_RIGHT)
        if any(
            p.get_rect().centerx + TILE_SIZE == ep.get_rect().centerx
            and p.get_rect().centery == ep.get_rect().centery
            for p in self.paths
        ):
            r.append(pygame.K_LEFT)
        if any(
            p.get_rect().centerx == ep.get_rect().centerx
            and p.get_rect().centery - TILE_SIZE == ep.get_rect().centery
            for p in self.paths
        ):
            r.append(pygame.K_DOWN)
        if any(
            p.get_rect().centerx == ep.get_rect().centerx
            and p.get_rect().centery + TILE_SIZE == ep.get_rect().centery
            for p in self.paths
        ):
            r.append(pygame.K_UP)
        return r

    def update(self):
        for c in self.coins:
            c.update()
        self.coins = [c for c in self.coins if not c.has_disappeared]
        if not self.coins:
            ps = random.sample(self.paths, random.choice(range(1, 11)))
            self.coins = list(Coin(p.x, p.y, self.coin_images) for p in ps)

        for w in self.walls:
            w.update()
            if w.is_destroyed:
                self.paths.append(Path(w.x, w.y, self.path_image))
        self.walls = [w for w in self.walls if not w.is_destroyed]

        for e in self.enemies:
            e.update(self.get_possible_directions(e))
        self.enemies = [e for e in self.enemies if not e.is_dead]

    def is_completed(self):
        return not self.enemies

    def check_touched_coin(self, hero):
        for c in self.coins:
            if c.get_rect().colliderect(hero.get_rect()):
                if not c.was_collected:
                    hero.change_points()
                c.collected()

    def check_touched_wall(self, hero):
        for w in self.walls:
            hero.check_touched_wall(w)
            for e in self.enemies:
                e.check_touched_wall(w)

    def check_touched_enemy(self, hero):
        for e in self.enemies:
            hero.check_touched_enemy(e)

    def get_random_path(self):
        return random.choice(self.paths)

    def draw(self, screen, font):
        for p in self.paths:
            p.draw(screen)
        for w in self.walls:
            w.draw(screen)
        for c in self.coins:
            c.draw(screen)
        for e in self.enemies:
            e.draw(screen)
        level_img = font.render(f"Level: {self.level}", True, (255, 255, 255))
        screen.blit(level_img, (0, 75))


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

    def go_to_position(self, x, y):
        self.image = self.images[pygame.K_DOWN][0]
        self.image_number = 0
        self.x = x
        self.y = y
        self.movement_direction = pygame.K_DOWN
        self.stars: list[Star] = []

    def go_to_prev_position(self):
        self.x = self.prev_x
        self.y = self.prev_y
        self.image_number = 0
        self.movement_direction = self.prev_movement_direction
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

        r = []
        for s in self.stars:
            if enemy.get_rect().colliderect(s.get_rect()):
                r.append(s)
                enemy.hit()
        self.stars = [s for s in self.stars if s not in r]

    def update(self, keys):
        self.prev_x = self.x
        self.prev_y = self.y
        self.prev_movement_direction = self.movement_direction
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
            and (self.points // 5 - self.stars_spend) > 0
        ):
            self.stars.append(
                Star(self.x, self.y, self.star_image, self.movement_direction)
            )
            self.stars_spend += 1

    def change_points(self):
        self.points += 1

    def get_rect(self):
        collision_rect = self.image.get_rect(center=(self.x, self.y))
        collision_rect.x += 10
        collision_rect.width -= 20

        return collision_rect

    def is_alive(self):
        return self.lives > 0

    def draw(self, screen: pygame.Surface, font):
        collision_rect = self.image.get_rect(center=(self.x, self.y))
        collision_rect.x += 10
        collision_rect.width -= 20
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


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Treasure hunt")

font = pygame.font.Font(None, 25)


maze = Maze(1)
r = maze.get_random_path().get_rect()
hero = Hero(r.centerx, r.centery)


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if hero.is_alive():
            hero.process_event(event)

    screen.fill((0, 0, 0))

    if hero.is_alive():
        hero.update(pygame.key.get_pressed())
    maze.update()

    if hero.is_alive():
        maze.check_touched_coin(hero)
        maze.check_touched_enemy(hero)

    maze.check_touched_wall(hero)

    maze.draw(screen, font)
    if hero.is_alive():
        hero.draw(screen, font)
    else:
        end_img = pygame.font.Font(None, 75).render(f"GAME OVER", True, (255, 50, 100))
        screen.blit(end_img, (SCREEN_WIDTH / 2 - 135, SCREEN_HEIGHT / 2 - 20))
    if maze.is_completed():
        maze = Maze(maze.level + 1)
        r = maze.get_random_path().get_rect()
        hero.go_to_position(r.centerx, r.centery)

    pygame.display.flip()
