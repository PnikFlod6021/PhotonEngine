import tkinter as tk
from src.models.Player_Action_Screen_Timer import GameScreen
from src.models.green_team import GreenTeam
from src.models.red_team import RedTeam

class PlayActionScreen:
    def __init__(self, root, red_team_data, green_team_data, game_log):
        self.root = root
        self.red_team_data = red_team_data
        self.green_team_data = green_team_data
        self.game_log = game_log

        self.radius = 30
        self.border_width = 4

        self.canvas = tk.Canvas(root, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.game_timer = GameScreen(root)
        self.game_timer.start_timer()

        self.time_text = None

        self.create_ui()
        self.update_scoreboard_timer()

    def draw_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1+radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1
        ]

        return self.canvas.create_polygon(points, smooth=True, **kwargs)
    
    def create_ui(self):
        # Create main scoreboard box
        self.draw_rounded_rect(50, 50, 750, 550, self.radius, fill="black", outline="yellow", width=self.border_width)

        # Create red team frame
        self.create_team_frame(self.red_team_data, "RED TEAM", "red", 56)

        # Create green team frame
        self.create_team_frame(self.green_team_data, "GREEN TEAM", "green", 400)

        # Game log box
        self.draw_rounded_rect(50, 200, 750, 500, self.radius, fill="#0a0d24", outline="yellow", width=self.border_width)

        # Time remaining label
        self.time_text = self.canvas.create_text(630, 525, text="", fill="white", font=("Helvetica", 16, "bold"))

    def create_team_frame(self, team_data, label, color, x):
        frame = tk.Frame(self.canvas, bg="black")
        self.canvas.create_window(x, 55, window=frame, width=344, height=140, anchor="nw")

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        tk.Label(frame, text=label, fg="white", bg="black", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, sticky="n", padx=0, pady=0)
        
        for i, player in enumerate(team_data):
            tk.Label(frame, text=player['name'], fg=color, bg="black", font=("Helvetica", 12, "bold")).grid(row=i+1, column=0, sticky="w", padx=5)
            tk.Label(frame, text=player['score'], fg=color, bg="black", font=("Helvetica", 12, "bold")).grid(row=i+1, column=1, sticky="e", padx=0)
        total_score = sum(player["score"] for player in team_data)
        total_label = tk.Label(frame, text=f"{total_score}", fg=color, bg="black", font=("Helvetica", 12, "bold"))
        total_label.place(relx=1.0, rely=1.0, anchor="se", x=0, y=0)

    def update_scoreboard_timer(self):
        current_time = self.game_timer.get_remaining_time()
        self.canvas.itemconfig(self.time_text, text=f"Time Remaining: {current_time}")
        self.root.after(1000, self.update_scoreboard_timer)

class TestPlayer:
    def __init__(self, pid, codename, equip):
        self._id = pid
        self._codename = codename
        self._equip = equip
        self.is_on_team = False

    def get_player_id(self): return self._id
    def get_codename(self): return self._codename
    def get_equipment_id(self): return self._equip

if __name__ == "__main__":
    green_team_model = GreenTeam()
    red_team_model = RedTeam()


    green_team_model = GreenTeam()
    red_team_model = RedTeam()

    # Data to test players -
    green_team_model.add_new_player(TestPlayer("G1", "Scooby Doo", "E1"))
    green_team_model.add_new_player(TestPlayer("G2", "Opus", "E2"))

    red_team_model.add_new_player(TestPlayer("R1", "Crimson", "E3"))
    red_team_model.add_new_player(TestPlayer("R2", "Opus", "E4"))


    red_team_data = red_team_model.get_display_data()
    green_team_data = green_team_model.get_display_data()

    # Game log - not used yet
    game_log = [
        "Scooby Doo hit Opus",
        "Scooby Doo hit Opus"
    ]

    root = tk.Tk()
    root.title("Play Action")
    root.geometry("800x600")
    root.configure(bg="black")

    PlayActionScreen(root, red_team_data, green_team_data, game_log)

    root.mainloop()