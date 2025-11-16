import pygame
import tkinter as tk

from src.views.loading_screen import LoadingScreen
from src.constants import ScreenConstants
from src.models.database import list_players, search, add_player
from src.views.countdown_screen import CountdownScreen
from src.views.entry_terminal_screen import PlayerEntryGUI
from src.models.teams.green_team import GreenTeam
from src.models.teams.red_team import RedTeam
from src.models.teams.player import Player
from src.views.play_action_screen import PlayActionScreen
from src.models.UDP.UDP_server import start_receiving
from src.models.UDP.UDP_client import broadcast_message 
from src.models.player_event_handler import score_logic



def main():
    pygame.init()
    screen = pygame.display.set_mode((ScreenConstants.SCREEN_WIDTH, ScreenConstants.SCREEN_HEIGHT))
    pygame.display.set_caption(ScreenConstants.GAME_TITLE)

    #Display Splash Screen/Loading Screen
    loading_screen = LoadingScreen(screen)
    loading_screen.load_starting_screen()

    pygame.quit()

    root = tk.Tk()

    player_entry_screen = PlayerEntryGUI(root)






if __name__ == "__main__":
    main()
