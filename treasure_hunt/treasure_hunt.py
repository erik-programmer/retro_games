import pygame, sys
from constants import *
from utils import *
from maze import Maze
from hero import Hero
from level_menu import LevelMenu
import json

data = json.load(open(DATA_FILE))
level_menu = LevelMenu(data["level"])
background_img = pygame.image.load(f"treasure_hunt/images/background.png")

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Treasure hunt")

font = pygame.font.Font(None, 25)


is_game_started = False
selected_level = 0

maze = Maze(1)
r = maze.get_random_path().get_rect()
hero = Hero(r.centerx, r.centery)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not is_game_started:
            level_menu.process_event(event)
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_RETURN
                and level_menu.is_level_selectable()
            ):
                is_game_started = True
                selected_level = level_menu.selected_level
                maze = Maze(selected_level)
                r = maze.get_random_path().get_rect()
                hero.start_new_level(r.centerx, r.centery)
        else:
            if hero.is_alive():
                hero.process_event(event)

    if not is_game_started:
        screen.blit(background_img, (0, 0))
        level_menu.draw(screen)
    else:
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
            end_img = pygame.font.Font(None, 75).render(
                f"GAME OVER", True, (255, 50, 100)
            )
            screen.blit(end_img, (SCREEN_WIDTH / 2 - 135, SCREEN_HEIGHT / 2 - 20))

        if maze.is_completed():
            is_game_started = False
            if maze.level < 8 and maze.level == data["level"]:
                data["level"] += 1
            level_menu = LevelMenu(data["level"])
            json.dump(data, open(DATA_FILE, "w"))

    pygame.display.flip()
