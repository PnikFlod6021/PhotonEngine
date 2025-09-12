import pygame


from src.views.loading_screen import LoadingScreen
from src.constants import ScreenConstants


GAME_TITLE = "Photon"

def main():
    pygame.init()


    screen = pygame.display.set_mode((ScreenConstants.SCREEN_WIDTH, ScreenConstants.SCREEN_HEIGHT))

    pygame.display.set_caption(ScreenConstants.GAME_TITLE)

    #Display Splash Screen/Loading Screen
    loading_screen = LoadingScreen(screen)
    loading_screen.load_starting_screen()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()