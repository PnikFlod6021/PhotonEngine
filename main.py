import pygame


from src.views.loading_screen import LoadingScreen
from src.constants import ScreenConstants
from database import connect_data, init_db, list_players, clear_players, search


GAME_TITLE = "Photon"

def main():
    pygame.init()


    screen = pygame.display.set_mode((ScreenConstants.SCREEN_WIDTH, ScreenConstants.SCREEN_HEIGHT))

    pygame.display.set_caption(ScreenConstants.GAME_TITLE)

    #Display Splash Screen/Loading Screen
    loading_screen = LoadingScreen(screen)
    loading_screen.load_starting_screen()

    # add players
    def add_player(codename):
        con = connect_data()
        cursor = con.cursor()
        cursor.execute("INSERT INTO players (name) VALUES (?)",(codename, ))
        con.commit()
        con.close()
    
    # Test adding players
    # clear_players()
    add_player("Opus")
    add_player("Scooby")
    print("Players: ")
    for player in list_players():
        print(player)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    init_db()
    main()