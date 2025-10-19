import pygame
import time
from src.constants import ScreenConstants
from src.models.UDP.UDP_client import broadcast_message

class CountdownScreen:
    def __init__ (self, screen, duration=30):
        self.screen = screen
        self.duration = duration
        self.font = pygame.font.Font(None, 200)
        self.start_time = time.time()
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
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

            if remaining == 0:
                self.screen.fill((0,0,0))
                go_txt = self.font.render("GO!", True, (221, 191, 218))
                go_rect = go_txt.get_rect(center = (ScreenConstants.SCREEN_WIDTH/2, ScreenConstants.SCREEN_HEIGHT/2))
                self.screen.blit(go_txt, go_rect)
                pygame.display.flip()

                pygame.time.wait(1500)
                broadcast_message(202)
                running = False

        return True
   