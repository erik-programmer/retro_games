import pygame


def load_images(path, limit):
    return list(
        pygame.image.load(f"treasure_hunt/images/{path}_{i:02d}.png").convert_alpha()
        for i in range(0, limit)
    )
