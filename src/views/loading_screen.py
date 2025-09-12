import sys

import pygame.image
from pygame.time import Clock

from src.constants import ScreenConstants

LOADING_SCREEN_PATH = "images/logo.jpg"


class LoadingScreen:

    def __init__(self, screen):
        self.screen = screen


    def load_starting_screen(self):
        image = pygame.image.load(LOADING_SCREEN_PATH).convert()
        image = pygame.transform.scale(image, (ScreenConstants.SCREEN_WIDTH, ScreenConstants.SCREEN_HEIGHT))

        self.screen.blit(image, (0, 0))
        pygame.display.update()

        pygame.event.pump()
        pygame.time.delay(2500)

        fading_surface = pygame.Surface((ScreenConstants.SCREEN_WIDTH, ScreenConstants.SCREEN_HEIGHT))
        fading_surface.fill((0,0,0))


        for alpha_value in range(0, 45):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            fading_surface.set_alpha(alpha_value)
            self.screen.blit(fading_surface, (0, 0))
            pygame.display.update()
            pygame.time.Clock().tick(20)



