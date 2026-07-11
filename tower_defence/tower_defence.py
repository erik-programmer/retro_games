import pygame, sys
import random
from enum import Enum

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1000


class ShopItemType(Enum):
    ASSASSIN_SIMPLE = 1
    ASSASSIN_ADVANDCED = 2
    ASSASSIN_EXPERT = 3
    CHEST = 4
    SELLING = 5


class AssassinType(Enum):
    SIMPLE = 1
    ADVANDCED = 2
    EXPERT = 3


class EnemyType(Enum):
    MALE_GOBLIN = 1
    FEMALE_GOBLIN = 2
    CHIEF_GOBLIN = 3


class Enemy:
    def __init__(self, y, type: EnemyType) -> None:
        self.x = SCREEN_WIDTH
        self.y = y
        if type == EnemyType.MALE_GOBLIN:
            self.images = list(
                pygame.image.load(
                    f"tower_defence/images/male_goblin/left_{i:02d}.png"
                ).convert_alpha()
                for i in range(0, 20)
            )
            self.lifes = 1
            self.speed = 2.5
        elif type == EnemyType.FEMALE_GOBLIN:
            self.images = list(
                pygame.image.load(
                    f"tower_defence/images/female_goblin/left_{i:02d}.png"
                ).convert_alpha()
                for i in range(0, 20)
            )
            self.lifes = 6
            self.speed = 5
        else:
            self.images = list(
                pygame.image.load(
                    f"tower_defence/images/chief_goblin/left_{i:02d}.png"
                ).convert_alpha()
                for i in range(0, 20)
            )
            self.speed = 5
            self.lifes = 9

        self.image_number = 0
        self.image_timer = pygame.time.get_ticks()
        self.type = type

    def update(self):
        if self.image_timer + 40 < pygame.time.get_ticks():
            self.x -= self.speed
            self.image_number += 1
            self.image_timer = pygame.time.get_ticks()
            if self.image_number > 19:
                self.image_number = 0

    def touched_left_border(self):
        return self.x < 0

    def got_hit(self, minus_lifes):
        self.lifes -= minus_lifes

    def got_killed(self):
        self.lifes = 0

    def get_rect(self):
        return self.images[self.image_number].get_rect(center=(self.x, self.y))

    def draw(self, screen):
        rect = self.get_rect()
        br = pygame.Rect(rect.x + 10, rect.y - 8, 30, 5)
        if self.type == EnemyType.MALE_GOBLIN:
            r = pygame.Rect(rect.x + 10, rect.y - 8, 30 * self.lifes / 1, 5)
        elif self.type == EnemyType.FEMALE_GOBLIN:
            r = pygame.Rect(rect.x + 10, rect.y - 8, 30 * self.lifes / 6, 5)
        else:
            r = pygame.Rect(rect.x + 10, rect.y - 8, 30 * self.lifes / 9, 5)
        pygame.draw.rect(screen, (0, 0, 0), br)
        pygame.draw.rect(screen, (0, 255, 0), r)
        screen.blit(self.images[self.image_number], rect)


class Star:
    def __init__(self, x, y, image) -> None:
        self.x = x
        self.y = y
        self.image = image
        self.angle = 0

    def update(self):
        self.x += 0.5
        self.angle -= 1

    def get_rect(self):
        rotated_img = pygame.transform.rotate(self.image, self.angle)
        return rotated_img.get_rect(center=(self.x, self.y))

    def draw(self, screen):
        rotated_img = pygame.transform.rotate(self.image, self.angle)
        rect = rotated_img.get_rect(center=(self.x, self.y))
        screen.blit(rotated_img, rect)


class Assassin:
    def __init__(self, x, y, image, type: AssassinType):
        self.x = x
        self.y = y
        self.image = image
        self.stars: list[Star] = []
        self.is_alive = True
        self.star_image = pygame.image.load(
            f"tower_defence/images/star.png"
        ).convert_alpha()
        self.star_timer = pygame.time.get_ticks()
        self.type = type

    def check_touched_enemy(self, enemy: Enemy):
        r = []
        for s in self.stars:
            if s.get_rect().colliderect(enemy.get_rect()):
                r.append(s)
                if self.type == AssassinType.SIMPLE:
                    enemy.got_hit(1)
                elif self.type == AssassinType.ADVANDCED:
                    enemy.got_hit(2)
                else:
                    enemy.got_hit(3)
        self.stars = list(s for s in self.stars if s not in r)
        if self.get_rect().colliderect(enemy.get_rect()):
            self.is_alive = False
            enemy.got_killed()

    def update(self):
        if self.star_timer + 5000 < pygame.time.get_ticks():
            self.stars.append(Star(self.x, self.y, self.star_image))
            self.star_timer = pygame.time.get_ticks()
        for s in self.stars:
            s.update()
        self.stars = list(s for s in self.stars if s.x < SCREEN_WIDTH)

    def get_rect(self):
        return self.image.get_rect(center=(self.x, self.y))

    def draw(self, screen):
        rect = self.get_rect()
        screen.blit(self.image, rect)
        for s in self.stars:
            s.draw(screen)


class Chest:
    def __init__(self, x, y, chest_full_callback):
        self.image = pygame.image.load(
            f"tower_defence/images/chest.png"
        ).convert_alpha()
        self.x = x
        self.y = y
        self.w = 1
        self.h = 1
        self.timer = pygame.time.get_ticks()
        self.chest_full_callback = chest_full_callback
        self.target = random.randint(45, 52)
        self.is_alive = True

    def update(self):
        if self.timer + 200 < pygame.time.get_ticks():
            self.w += 1
            self.h += 1
            self.timer = pygame.time.get_ticks()
        if self.w > self.target:
            self.w = 1
            self.h = 1
            self.target = random.randint(45, 52)
            self.chest_full_callback()

    def get_rect(self):
        scaled_img = pygame.transform.scale(self.image, (self.w, self.h))
        return scaled_img.get_rect(center=(self.x, self.y))

    def check_touched_enemy(self, enemy):
        if self.get_rect().colliderect(enemy.get_rect()):
            self.is_alive = False
            enemy.got_killed()

    def draw(self, screen):
        scaled_img = pygame.transform.scale(self.image, (self.w, self.h))
        rect = scaled_img.get_rect(center=(self.x, self.y))
        screen.blit(scaled_img, rect)


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tower defence")

font = pygame.font.Font(None, 25)
treasure_number = 100


def increase_treasure_number():
    global treasure_number
    treasure_number += 1


shop = {
    ShopItemType.ASSASSIN_SIMPLE: {
        "image": pygame.image.load(
            f"tower_defence/images/assassin.png"
        ).convert_alpha(),
        "price": 10,
        "type": AssassinType.SIMPLE,
    },
    ShopItemType.ASSASSIN_ADVANDCED: {
        "image": pygame.image.load(
            f"tower_defence/images/assassin_advanced.png"
        ).convert_alpha(),
        "price": 20,
        "type": AssassinType.ADVANDCED,
    },
    ShopItemType.ASSASSIN_EXPERT: {
        "image": pygame.image.load(
            f"tower_defence/images/assassin_expert.png"
        ).convert_alpha(),
        "price": 30,
        "type": AssassinType.EXPERT,
    },
    ShopItemType.CHEST: {
        "image": pygame.image.load("tower_defence/images/chest.png").convert_alpha(),
        "price": 5,
    },
    ShopItemType.SELLING: {
        "image": pygame.image.load("tower_defence/images/selling.png").convert_alpha(),
    },
}
shop[ShopItemType.ASSASSIN_SIMPLE]["rect"] = shop[ShopItemType.ASSASSIN_SIMPLE][
    "image"
].get_rect(topleft=(300, 5))
shop[ShopItemType.ASSASSIN_ADVANDCED]["rect"] = shop[ShopItemType.ASSASSIN_ADVANDCED][
    "image"
].get_rect(topleft=(350, 5))
shop[ShopItemType.ASSASSIN_EXPERT]["rect"] = shop[ShopItemType.ASSASSIN_EXPERT][
    "image"
].get_rect(topleft=(400, 5))
shop[ShopItemType.CHEST]["rect"] = shop[ShopItemType.CHEST]["image"].get_rect(
    topleft=(450, 5)
)
shop[ShopItemType.SELLING]["rect"] = shop[ShopItemType.SELLING]["image"].get_rect(
    topleft=(500, 5)
)

background_image = pygame.image.load(
    f"tower_defence/images/background.png"
).convert_alpha()
chests = [
    Chest(50, 100, increase_treasure_number),
    Chest(50, 200, increase_treasure_number),
    Chest(50, 300, increase_treasure_number),
    Chest(50, 400, increase_treasure_number),
    Chest(50, 500, increase_treasure_number),
]
assassins: list[Assassin] = []
enemies: list[Enemy] = []

game_finished = False
mouse_button_pressed = False
selected_shop_item_type = ShopItemType.ASSASSIN_SIMPLE
mouse_pos = (0, 0)
enemy_timer = pygame.time.get_ticks()
next_enemy_delay = random.randint(10000, 15000)
enemy_counter = 0
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_finished:
            for k, v in shop.items():
                if v["rect"].collidepoint(event.pos):
                    if "price" not in v or treasure_number >= v["price"]:
                        mouse_button_pressed = True
                        mouse_pos = event.pos
                        selected_shop_item_type = k
        if event.type == pygame.MOUSEMOTION and mouse_button_pressed:
            mouse_pos = event.pos
        if event.type == pygame.MOUSEBUTTONUP and mouse_button_pressed:
            mouse_button_pressed = False
            if selected_shop_item_type == ShopItemType.CHEST:
                chests.append(
                    Chest(
                        event.pos[0],
                        event.pos[1],
                        increase_treasure_number,
                    )
                )
                treasure_number -= shop[selected_shop_item_type]["price"]
            elif selected_shop_item_type == ShopItemType.SELLING:
                for a in assassins:
                    if a.get_rect().colliderect(
                        shop[selected_shop_item_type]["image"].get_rect(
                            center=mouse_pos
                        )
                    ):
                        if a.type == AssassinType.SIMPLE:
                            treasure_number += (
                                shop[ShopItemType.ASSASSIN_SIMPLE]["price"] // 2
                            )
                        elif a.type == AssassinType.ADVANDCED:
                            treasure_number += (
                                shop[ShopItemType.ASSASSIN_ADVANDCED]["price"] // 2
                            )
                        else:
                            treasure_number += (
                                shop[ShopItemType.ASSASSIN_EXPERT]["price"] // 2
                            )
                        assassins.remove(a)
                        break
            else:
                assassins.append(
                    Assassin(
                        event.pos[0],
                        event.pos[1],
                        shop[selected_shop_item_type]["image"],
                        shop[selected_shop_item_type]["type"],
                    )
                )
                treasure_number -= shop[selected_shop_item_type]["price"]

    if enemy_timer + next_enemy_delay < pygame.time.get_ticks() and not game_finished:
        if enemy_counter < 11:
            enemies.append(
                Enemy(random.choice([100, 200, 300, 400, 500]), EnemyType.CHIEF_GOBLIN)
            )
        elif 10 < enemy_counter < 20:
            enemies.append(
                Enemy(
                    random.choice([100, 200, 300, 400, 500]),
                    random.choice([EnemyType.CHIEF_GOBLIN, EnemyType.MALE_GOBLIN]),
                )
            )
        else:
            enemies.append(
                Enemy(
                    random.choice([100, 200, 300, 400, 500]),
                    random.choice([EnemyType.CHIEF_GOBLIN, EnemyType.FEMALE_GOBLIN]),
                )
            )
        enemy_timer = pygame.time.get_ticks()
        next_enemy_delay = random.randint(10000, 15000)
        enemy_counter += 1

    screen.blit(background_image, (0, 0))
    if not game_finished:
        for e in enemies:
            e.update()
            if e.touched_left_border():
                game_finished = True

        for c in chests:
            c.update()

        for a in assassins:
            a.update()

        for e in enemies:
            for a in assassins:
                a.check_touched_enemy(e)

        for c in chests:
            for e in enemies:
                c.check_touched_enemy(e)

    chests = list(c for c in chests if c.is_alive)
    assassins = list(a for a in assassins if a.is_alive)
    enemies = list(e for e in enemies if e.lifes > 0)

    for a in assassins:
        a.draw(screen)

    for e in enemies:
        e.draw(screen)

    for c in chests:
        c.draw(screen)

    if mouse_button_pressed:
        screen.blit(
            shop[selected_shop_item_type]["image"],
            shop[selected_shop_item_type]["image"].get_rect(center=mouse_pos),
        )

    for k, v in shop.items():
        screen.blit(v["image"], v["rect"])
        if "price" in v:
            if treasure_number >= v["price"]:
                assassin_price_image = pygame.font.Font(None, 25).render(
                    f"{v["price"]}", True, (0, 255, 0)
                )
            else:
                assassin_price_image = pygame.font.Font(None, 25).render(
                    f"{v["price"]}", True, (255, 0, 0)
                )
            screen.blit(
                assassin_price_image,
                (
                    v["rect"].x + v["image"].get_rect().width / 2 - 5,
                    v["image"].get_rect().height + 7,
                ),
            )

    treasure_number_image = pygame.font.Font(None, 25).render(
        f"Treasures: {treasure_number}", True, (255, 50, 100)
    )
    screen.blit(treasure_number_image, (10, 10))

    level_image = pygame.font.Font(None, 25).render(
        f"Enemies created: {enemy_counter}", True, (255, 50, 100)
    )
    screen.blit(level_image, (10, 30))

    if game_finished:
        end_img = pygame.font.Font(None, 75).render(f"GAME OVER", True, (255, 50, 100))
        screen.blit(end_img, (SCREEN_WIDTH / 2 - 135, SCREEN_HEIGHT / 2 - 20))

    pygame.display.flip()
