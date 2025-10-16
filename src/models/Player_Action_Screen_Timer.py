# gui/game_screen.py
import tkinter as tk


class GameScreen:
    def __init__(self, root):
        self.root = root  
        self.remaining_time = 6 * 60
        self.timer_running = False

      
        # self.timer_label = tk.Label(
        #     self.root, text="Time left: 06:00", font=("Helvetica", 20, "bold"), fg="red"
        # )
        # self.timer_label.pack(pady=20)

      
        # start_button = tk.Button(self.root, text="Start Game Timer", command=self.start_timer)
        # start_button.pack(pady=10)

    def start_timer(self):
        
        if not self.timer_running:
            self.timer_running = True
            
            self._update_timer()

    def _update_timer(self):
        
        if self.remaining_time > 0 and self.timer_running:
            # mins, secs = divmod(self.remaining_time, 60)
            # self.timer_label.config(text=f"Time left: {mins:02d}:{secs:02d}")
            self.remaining_time -= 1
            self.root.after(1000, self._update_timer)
        else:
            # self.timer_label.config(text="Game Over!")
            self.timer_running = False

    def get_remaining_time(self):
        mins, secs = divmod(self.remaining_time, 60)
        return f"{mins}:{secs:02d}"


# def main():
#     root = tk.Tk()
#     app = GameScreen(root)
#     root.mainloop()

# if __name__ == "__main__":
    # main()