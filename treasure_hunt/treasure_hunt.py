import pygame, sys
from constants import *
from utils import *
from maze import Maze
from hero import Hero

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
        maze.check_touched_heart(hero)

    maze.check_touched_wall(hero)

    maze.draw(screen, font)
    if hero.is_alive():
        hero.draw(screen, font)
    else:
        end_img = pygame.font.Font(None, 75).render(f"GAME OVER", True, (255, 50, 100))
        screen.blit(end_img, (SCREEN_WIDTH / 2 - 135, SCREEN_HEIGHT / 2 - 20))

    if maze.is_completed() and maze.level < 8:
        maze = Maze(maze.level + 1)
        r = maze.get_random_path().get_rect()
        hero.start_new_level(r.centerx, r.centery)

    pygame.display.flip()
