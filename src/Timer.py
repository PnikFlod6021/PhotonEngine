# models/game_starter.py

from models.udp_handler import broadcast_message

class GameStarter:
    def __init__(self, root, timer_label, pre_game_seconds=30, game_seconds=6*60):
        """
        root: Tk root or Toplevel window
        timer_label: Label widget to show countdown text
        pre_game_seconds: how long before game starts
        game_seconds: total duration of the game
        """
        self.root = root
        self.timer_label = timer_label
        self.pre_game_seconds = pre_game_seconds
        self.game_seconds = game_seconds
        self.remaining_time = pre_game_seconds
        self.game_running = False

    def start(self):
        """Start pre-game countdown."""
        self.remaining_time = self.pre_game_seconds
        self.timer_label.config(text=f"Game starts in {self.remaining_time}s")
        self._pre_game_tick()

    def _pre_game_tick(self):
        """Run countdown using Tkinter's after() method."""
        if self.remaining_time > 0:
            self.timer_label.config(text=f"Game starts in {self.remaining_time}s")
            self.remaining_time -= 1
            # Schedule next tick in 1000 ms (1s)
            self.root.after(1000, self._pre_game_tick)
        else:
            # Countdown finished → broadcast code 202
            broadcast_message(202)
            self.start_game_timer()
