import pygame, random, sys

# Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800


class EnemyTank:
    def __init__(self):

        self.images = [
            pygame.image.load("tanks/enemy_tank.png"),
            pygame.image.load("tanks/explosion1.png"),
            pygame.image.load("tanks/explosion2.png"),
            pygame.image.load("tanks/explosion3.png"),
            pygame.image.load("tanks/explosion4.png"),
            pygame.image.load("tanks/explosion5.png"),
        ]
        self.start()

    def got_hit(self):
        self.image_number += 1
        self.hit_time = pygame.time.get_ticks()

    def was_already_hit(self):
        return self.hit_time != 0

    def update(self):
        if self.hit_time != 0:
            if self.hit_time + 100 < pygame.time.get_ticks():
                self.image_number += 1
                self.hit_time = pygame.time.get_ticks()
            if self.image_number == 6:
                self.start()

    def start(self):
        self.image_number = 0
        self.hit_time = 0
        self.x = random.randint(
            0, SCREEN_WIDTH - self.images[self.image_number].get_rect().width
        )
        self.y = random.randint(
            0, SCREEN_HEIGHT - self.images[self.image_number].get_rect().height
        )

    def get_rect(self):
        return pygame.Rect(
            self.x,
            self.y,
            self.images[self.image_number].get_width(),
            self.images[self.image_number].get_height(),
        )

    def draw(self, screen: pygame.Surface):
        screen.blit(self.images[self.image_number], (self.x, self.y))


class Tank:
    def __init__(self):
        self.image = pygame.image.load("tanks/tank.png")
        self.start()
        self.bullets = []

    def process_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.bullets.append(Bullet(self.x, self.y, self.angle))

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= 2
            self.angle = 90
        if keys[pygame.K_RIGHT]:
            self.x += 2
            self.angle = 270
        if keys[pygame.K_UP]:
            self.y -= 2
            self.angle = 0
        if keys[pygame.K_DOWN]:
            self.y += 2
            self.angle = 180
        for b in self.bullets:
            b.update()
            if b.is_gone():
                self.bullets.remove(b)

    def check_hit(self, enemy_tank: EnemyTank):
        ret = False
        for b in self.bullets:
            if b.check_hit(enemy_tank):
                self.bullets.remove(b)
                if not enemy_tank.was_already_hit():
                    enemy_tank.got_hit()
                    ret = True
        return ret

    def start(self):
        self.x = SCREEN_WIDTH // 2  # center x
        self.y = SCREEN_HEIGHT // 2  # center y
        self.angle = 0

    def draw(self, screen: pygame.Surface):
        rotated_img = pygame.transform.rotate(self.image, self.angle)
        rect = rotated_img.get_rect(center=(self.x, self.y))
        screen.blit(rotated_img, rect)
        for b in self.bullets:
            b.draw(screen)


class Bullet:
    def __init__(self, x, y, angle):
        self.image = pygame.image.load("tanks/bullet.png")
        self.x = x
        self.y = y
        self.angle = angle

    def update(self):
        if self.angle == 90:
            self.x -= 5
        if self.angle == 270:
            self.x += 5
        if self.angle == 0:
            self.y -= 5
        if self.angle == 180:
            self.y += 5

    def is_gone(self) -> bool:
        return (
            self.x < 0 or self.x > SCREEN_WIDTH or self.y < 0 or self.y > SCREEN_HEIGHT
        )

    def check_hit(self, enemy_tank: EnemyTank) -> bool:
        rotated_img = pygame.transform.rotate(self.image, self.angle)
        rect = rotated_img.get_rect(center=(self.x, self.y))
        return rect.colliderect(enemy_tank.get_rect())

    def draw(self, screen: pygame.Surface):
        rotated_img = pygame.transform.rotate(self.image, self.angle)
        rect = rotated_img.get_rect(center=(self.x, self.y))
        screen.blit(rotated_img, rect)


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tanks")

font = pygame.font.Font(None, 25)
points = 0
background = pygame.image.load("tanks/background.png")
tank = Tank()
enemy_tank = EnemyTank()

while True:
    if pygame.time.get_ticks() < 20 * 1000:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            tank.process_events(event)

        screen.blit(background, (0, 0))
        tank.update(pygame.key.get_pressed())
        if tank.check_hit(enemy_tank):
            points += 1
        enemy_tank.update()
        enemy_tank.draw(screen)
        tank.draw(screen)
        points_img = font.render(f"Points: {points}", True, (255, 255, 255))
        screen.blit(points_img, (10, 10))
        time_img = font.render(
            f"Time: {pygame.time.get_ticks()//1000}", True, (255, 255, 255)
        )
        screen.blit(time_img, (10, 30))

        pygame.display.flip()
