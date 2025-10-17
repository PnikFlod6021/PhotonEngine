import pygame


from src.views.loading_screen import LoadingScreen
from src.constants import ScreenConstants
from src.models.database import list_players, search, add_player
from src.views.countdown_screen import CountdownScreen



GAME_TITLE = "Photon"

def main():
    pygame.init()


    screen = pygame.display.set_mode((ScreenConstants.SCREEN_WIDTH, ScreenConstants.SCREEN_HEIGHT))

    pygame.display.set_caption(ScreenConstants.GAME_TITLE)

    #Display Splash Screen/Loading Screen
    loading_screen = LoadingScreen(screen)
    loading_screen.load_starting_screen()

    # Game start countdown
    countdown = CountdownScreen(screen, duration=10)
    countdown.run()



if __name__ == "__main__":
    main()