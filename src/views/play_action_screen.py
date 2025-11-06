import tkinter as tk
from src.models.Timers.Player_Action_Screen_Timer import GameScreen
from src.models.teams.green_team import GreenTeam
from src.models.teams.red_team import RedTeam

class PlayActionScreen:
    def __init__(self,red_team_data, green_team_data, game_log):
        root = tk.Tk()
        root.title("Play Action")
        root.geometry("1200x800")
        root.configure(bg="black")

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
        # store flashing job ids so we can cancel them when needed
        self.flash_jobs = {}

        # references to the total labels so we can toggle flashing dynamically
        self.red_total_label = None
        self.green_total_label = None

        self.create_ui()
        self.update_scoreboard_timer()

        self.root.mainloop()

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
        self.draw_rounded_rect(50, 50, 600, 650, self.radius, fill="black", outline="yellow", width=self.border_width)

        # Create red team frame
        # compute totals so we can determine which total is highest
        red_total = sum(player["score"] for player in self.red_team_data)
        green_total = sum(player["score"] for player in self.green_team_data)

        # Pass whether this team's total is the (co-)highest so it can flash
        self.create_team_frame(self.red_team_data, "RED TEAM", "red", 56, total_score=red_total, is_highest=(red_total >= green_total))

        # Create green team frame
        self.create_team_frame(self.green_team_data, "GREEN TEAM", "green", 325, total_score=green_total, is_highest=(green_total >= red_total))

        # Game log box
        self.draw_rounded_rect(620, 50, 1150, 650, self.radius, fill="#0a0d24", outline="yellow", width=self.border_width)

        # Time remaining label
        self.time_text = self.canvas.create_text(900, 670, text="", fill="white", font=("Helvetica", 16, "bold"))

    def create_team_frame(self, team_data, label, color, x, total_score, is_highest):
        frame = tk.Frame(self.canvas, bg="black")
        self.canvas.create_window(x, 55, window=frame, width=269, height=594, anchor="nw")

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        tk.Label(frame, text=label, fg="white", bg="black", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, sticky="n", padx=0, pady=0)

        # Sort team data list from highest to lowest
        sorted_data = sorted(team_data, key=lambda player: player['score'], reverse=True)
        
        for i, player in enumerate(sorted_data):
            tk.Label(frame, text=player['name'], fg=color, bg="black", font=("Helvetica", 14, "bold")).grid(row=i+1, column=0, sticky="w", padx=25)
            tk.Label(frame, text=player['score'], fg=color, bg="black", font=("Helvetica", 14, "bold")).grid(row=i+1, column=1, sticky="e", padx=0)
        total_score = sum(player["score"] for player in team_data)
        total_label = tk.Label(frame, text=f"{total_score}", fg=color, bg="black", font=("Helvetica", 14, "bold"))
        total_label.place(relx=1.0, rely=1.0, anchor="se", x=0, y=0)

    def update_scoreboard_timer(self):
        current_time = self.game_timer.get_remaining_time()
        self.canvas.itemconfig(self.time_text, text=f"Time Remaining: {current_time}")
        self.root.after(1000, self.update_scoreboard_timer)

# Class to test data
class TestPlayer:
    def __init__(self, pid, codename, equip):
        self._id = pid
        self._codename = codename
        self._equip = equip
        self.is_on_team = False

    def get_player_id(self): return self._id
    def get_codename(self): return self._codename
    def get_equipment_id(self): return self._equip


    