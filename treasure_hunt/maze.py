import random, pygame
from constants import *
from utils import *
from wall import Wall
from path import Path
from coin import Coin
from enemy import Enemy, EnemyType
from hero import Hero
from heart import Heart


class Maze:
    def __init__(self, level) -> None:
        self.coin_images = load_images("coin/coin", 8) + load_images(
            "coin/collected_coin", 6
        )
        self.heart_images = load_images("heart/heart", 25) + load_images(
            "heart/heart_frame", 25
        )

        self.path_image = pygame.image.load("treasure_hunt/images/path/stone/path.png")
        self.wall_images = load_images("wall/stone/wall_impact", 10)
        self.paths: list[Path] = []
        self.walls: list[Wall] = []
        self.enemies: list[Enemy] = []
        self.level = level
        self.level_enemies = {
            1: [EnemyType.MALE_GOBLIN, EnemyType.MALE_GOBLIN],
            2: [EnemyType.MALE_GOBLIN, EnemyType.MALE_GOBLIN, EnemyType.MALE_GOBLIN],
            3: [EnemyType.MALE_GOBLIN, EnemyType.MALE_GOBLIN, EnemyType.FEMALE_GOBLIN],
            4: [
                EnemyType.MALE_GOBLIN,
                EnemyType.FEMALE_GOBLIN,
                EnemyType.FEMALE_GOBLIN,
            ],
            5: [
                EnemyType.FEMALE_GOBLIN,
                EnemyType.FEMALE_GOBLIN,
                EnemyType.FEMALE_GOBLIN,
            ],
            6: [
                EnemyType.FEMALE_GOBLIN,
                EnemyType.FEMALE_GOBLIN,
                EnemyType.CHIEF_GOBLIN,
            ],
            7: [
                EnemyType.FEMALE_GOBLIN,
                EnemyType.CHIEF_GOBLIN,
                EnemyType.CHIEF_GOBLIN,
            ],
            8: [EnemyType.CHIEF_GOBLIN, EnemyType.CHIEF_GOBLIN, EnemyType.CHIEF_GOBLIN],
        }

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
        w = random.choice(self.walls)
        self.heart = Heart(w.x, w.y, self.heart_images)
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

        for et in self.level_enemies[self.level]:
            p = random.choice(self.paths)
            self.enemies.append(Enemy(p.get_rect().centerx, p.get_rect().centery, et))

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
        self.heart.update()

    def is_completed(self):
        return not self.enemies

    def check_touched_coin(self, hero: Hero):
        for c in self.coins:
            if c.get_rect().colliderect(hero.get_rect()):
                if not c.was_collected:
                    hero.change_points()
                c.collected()

    def check_touched_heart(self, hero: Hero):
        if self.heart.get_rect().colliderect(hero.get_rect()):
            if not self.heart.was_collected:
                hero.change_lives()
            self.heart.collected()

    def check_touched_wall(self, hero: Hero):
        for w in self.walls:
            hero.check_touched_wall(w)
            for e in self.enemies:
                e.check_touched_wall(w)

    def check_touched_enemy(self, hero: Hero):
        for e in self.enemies:
            hero.check_touched_enemy(e)

    def get_random_path(self):
        return random.choice(self.paths)

    def draw(self, screen, font):

        for p in self.paths:
            p.draw(screen)
        self.heart.draw(screen)
        for w in self.walls:
            w.draw(screen)
        for c in self.coins:
            c.draw(screen)
        for e in self.enemies:
            e.draw(screen)

        level_img = font.render(f"Level: {self.level}", True, (255, 255, 255))
        screen.blit(level_img, (0, 75))
