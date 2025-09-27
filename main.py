import pygame


from src.views.loading_screen import LoadingScreen
from src.constants import ScreenConstants
from src.models.database import list_players, search, add_player



GAME_TITLE = "Photon"

def main():
    pygame.init()


    screen = pygame.display.set_mode((ScreenConstants.SCREEN_WIDTH, ScreenConstants.SCREEN_HEIGHT))

    pygame.display.set_caption(ScreenConstants.GAME_TITLE)

    #Display Splash Screen/Loading Screen
    loading_screen = LoadingScreen(screen)
    loading_screen.load_starting_screen()

    # Test adding players
    # add_player("Opus")
    # add_player("Scooby")
    # uncomment if needing to see database
    print("Players: ")
    for player in list_players():
        print(player)

    # test searching database by id
    #print(search(2))
    #print(search(7))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()