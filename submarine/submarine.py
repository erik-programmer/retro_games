import pygame, sys

# Constants
SCREEN_HEIGHT = 300
SCREEN_WIDTH = 400
MAX_SPEED = 0.055


def has_collided(obj1, obj2) -> bool:
    r1 = pygame.Rect(obj1.x, obj1.y, obj1.image.get_width(), obj1.image.get_height())
    r2 = pygame.Rect(obj2.x, obj2.y, obj2.image.get_width(), obj2.image.get_height())
    return r1.colliderect(r2)


class Ship:
    def __init__(self):
        self.image_moving = pygame.image.load("submarine/ship.png")
        self.image_exploding = pygame.image.load("submarine/ship_exploding.png")
        self.start()
        self.speed = 0.025

    def update(self):
        if self.was_hit == 0:
            self.x += self.speed
            if self.x > SCREEN_WIDTH:
                self.start()
        else:
            self.was_hit += 1
            if self.was_hit > 200:
                self.start()

    def start(self):
        self.x = 0
        self.y = 0
        self.was_hit = 0
        self.image = self.image_moving

    def got_hit(self):
        self.image = self.image_exploding
        self.was_hit = 1
        if self.speed < MAX_SPEED:
            self.speed += 0.005

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, (self.x, self.y))


class Rocket:
    def __init__(self):
        self.image = pygame.image.load("submarine/rocket.png")
        self.start()

    def update(self, keys):
        if keys[pygame.K_SPACE]:
            self.was_fired = True
        if self.was_fired:
            self.y -= 0.1
        if self.y < 0:
            self.start()

    def start(self):
        self.x = SCREEN_WIDTH / 2 - self.image.get_rect().width / 2
        self.y = SCREEN_HEIGHT - self.image.get_rect().height
        self.was_fired = False

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, (self.x, self.y))


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Submarine")

rocket = Rocket()
ship = Ship()
points = 0
font = pygame.font.Font(None, 25)
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((255, 255, 255))
    pygame.draw.rect(
        screen, (50, 50, 255), pygame.Rect(0, 25, SCREEN_WIDTH, SCREEN_HEIGHT)
    )
    rocket.update(pygame.key.get_pressed())
    rocket.draw(screen)
    ship.update()
    ship.draw(screen)
    if has_collided(rocket, ship):
        points += 1
        rocket.start()
        ship.got_hit()

    points_img = font.render(f"Points: {points}", True, (255, 255, 255))
    screen.blit(points_img, (0, SCREEN_HEIGHT - 25))
    speed_img = font.render(f"Speed: {ship.speed:.3f}", True, (255, 255, 255))
    screen.blit(speed_img, (SCREEN_WIDTH - 110, SCREEN_HEIGHT - 25))

    pygame.display.flip()
