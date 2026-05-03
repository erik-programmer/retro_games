import pygame
from utils import *


class LevelMenu:
    def __init__(self, max_unlocked_level):
        self.max_unlocked_level = max_unlocked_level
        self.unlocked_level_imgs = load_images("level_menu/stone/level", 8)
        self.locked_level_imgs = load_images("level_menu/stone/level_grey", 8)
        self.selected_level = max_unlocked_level

    def is_level_selectable(self):
        return self.selected_level <= self.max_unlocked_level

    def process_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            self.selected_level -= 1
            if self.selected_level < 1:
                self.selected_level = 8
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            self.selected_level += 1
            if self.selected_level > 8:
                self.selected_level = 1

    def draw(self, screen: pygame.Surface):
        for l in range(0, self.max_unlocked_level):
            if l == self.selected_level - 1:
                screen.blit(
                    pygame.transform.scale(self.unlocked_level_imgs[l], (106, 103)),
                    (l * 120 + 20, 200),
                )
            else:
                screen.blit(self.unlocked_level_imgs[l], (l * 120 + 20, 200))
        for l in range(self.max_unlocked_level, 8):
            if l == self.selected_level - 1:
                screen.blit(
                    pygame.transform.scale(self.locked_level_imgs[l], (106, 103)),
                    (l * 120 + 20, 200),
                )
            else:
                screen.blit(self.locked_level_imgs[l], (l * 120 + 20, 200))
