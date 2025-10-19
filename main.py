import pygame


from src.views.loading_screen import LoadingScreen
from src.constants import ScreenConstants
from src.models.database import list_players, search, add_player
from src.views.countdown_screen import CountdownScreen
from src.views.entry_terminal_screen import PlayerEntryGUI
from src.models.teams.green_team import GreenTeam
from src.models.teams.red_team import RedTeam
from src.views.play_action_screen import PlayActionScreen



def main():
    pygame.init()
    screen = pygame.display.set_mode((ScreenConstants.SCREEN_WIDTH, ScreenConstants.SCREEN_HEIGHT))
    pygame.display.set_caption(ScreenConstants.GAME_TITLE)

    #Display Splash Screen/Loading Screen
    loading_screen = LoadingScreen(screen)
    loading_screen.load_starting_screen()

    pygame.quit()

    player_entry_screen = PlayerEntryGUI()


    # Game start countdown

    if player_entry_screen.has_finished:
        pygame.init()
        screen = pygame.display.set_mode((ScreenConstants.SCREEN_WIDTH, ScreenConstants.SCREEN_HEIGHT))
        pygame.display.set_caption(ScreenConstants.GAME_TITLE)

        countdown = CountdownScreen(screen, duration=30) #Remember to put this back to 30 after testing
        countdown_finished = countdown.run()

        pygame.quit()

        if countdown_finished:
            green_team_model = GreenTeam()
            red_team_model = RedTeam()

            red_team_data = red_team_model.get_display_data()
            green_team_data = green_team_model.get_display_data()

            game_log = [
                "Scooby Doo hit Opus",
                "Scooby Doo hit Opus"
            ]

            PlayActionScreen(red_team_data, green_team_data, game_log)






if __name__ == "__main__":
    main()
