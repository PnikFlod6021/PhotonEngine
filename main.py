import pygame


from src.views.loading_screen import LoadingScreen
from src.constants import ScreenConstants
from database import connect_data, init_db, list_players, clear_players, search, wipe_data


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
    
    # when we are through testing, uncomment below to clear the database and add legit players
    wipe_data


    # Test adding players
    add_player("Opus")
    add_player("Scooby")
    # uncomment if needing to see database
    # print("Players: ")
    # for player in list_players():
    #     print(player)

    # test searching database by id
    print(search(2))
    print(search(7))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    init_db()
    # uncomment when debugging to reset database to add 'real' players/create legit database, remove before final
    # wipe_data()
    main()