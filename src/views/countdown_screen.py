import pygame
import time
from src.constants import ScreenConstants, GameAudioConstants
from src.models.UDP.UDP_client import broadcast_message
from src.models.game_audio_handler import GameAudioHandler

class CountdownScreen:
    def __init__ (self, screen, duration=30):
        self.screen = screen
        self.duration = duration
        self.font = pygame.font.Font(None, 200)
        self.start_time = time.time()

        self.game_audio_handler = GameAudioHandler()
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        audio_played = False
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return False
            
            spent = int(time.time() - self.start_time)
            remaining = max(0, self.duration - spent)

            self.screen.fill((0,0,0))

            text_surface = self.font.render(str(remaining), True, (221, 191, 218))
            text_rect = text_surface.get_rect(center=(ScreenConstants.SCREEN_WIDTH/2, ScreenConstants.SCREEN_HEIGHT/2))

            self.screen.blit(text_surface, text_rect)

            pygame.display.flip()
            clock.tick(30)

            if remaining == GameAudioConstants.COUNTDOWN_GAME_AUDIO_LENGTH and not audio_played:
                self.game_audio_handler.play_countdown_audio()
                audio_played = True

            if remaining == 1:
                # self.screen.fill((0,0,0))
                # go_txt = self.font.render("GO!", True, (221, 191, 218))
                # go_rect = go_txt.get_rect(center = (ScreenConstants.SCREEN_WIDTH/2, ScreenConstants.SCREEN_HEIGHT/2))
                # self.screen.blit(go_txt, go_rect)
                # pygame.display.flip()

                # pygame.time.wait(1500)
                broadcast_message(202)
                running = False

        return True
   