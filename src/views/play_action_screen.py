import tkinter as tk
from src.models.Timers.Player_Action_Screen_Timer import GameScreen
from src.models.teams.green_team import GreenTeam
from src.models.teams.red_team import RedTeam
from src.models.game_audio_handler import GameAudioHandler
from friendly_fire import score_logic
from src.models.UDP.UDP_client import broadcast_message
from PIL import Image, ImageTk


class PlayActionScreen:
    def __init__(self,red_team_data, green_team_data, game_log, attacker_id = None):
        game_audio_handler = GameAudioHandler()

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

        self.player_widgets = {}

        # load base icon
        try:
            img =  Image.open("images/baseicon.jpg")
            img = img.resize((20,20))
            self.base_icon = ImageTk.PhotoImage(img)
        except Exception as e:
            print("Could not load baseicon.jpg: ", e)
            self.base_icon = None

        self.canvas = tk.Canvas(root, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.game_timer = GameScreen(root)
        self.game_timer.start_timer()

        self.logic = score_logic(red_team_data, green_team_data, ui_callback = self.update_player_info)

        self.time_text = None

        self.create_ui()
        self.update_scoreboard_timer()

        game_audio_handler.play_random_audio() 

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
        self.create_team_frame(self.red_team_data, "RED TEAM", "red", 56)

        # Create green team frame
        self.create_team_frame(self.green_team_data, "GREEN TEAM", "green", 325)

        # Game log box
        self.draw_rounded_rect(620, 50, 1150, 650, self.radius, fill="#0a0d24", outline="yellow", width=self.border_width)

        # Time remaining label
        self.time_text = self.canvas.create_text(900, 670, text="", fill="white", font=("Helvetica", 16, "bold"))

    def create_team_frame(self, team_data, label, color, x):
        frame = tk.Frame(self.canvas, bg="black")
        self.canvas.create_window(x, 55, window=frame, width=269, height=594, anchor="nw")

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        tk.Label(frame, text=label, fg="white", bg="black", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, sticky="n", padx=0, pady=0)
        
        for i, player in enumerate(team_data):
            name_label = tk.Label(frame, text=player['name'], fg=color, bg="black", font=("Helvetica", 14, "bold"))
            name_label.grid(row=i+1, column=0, sticky="w", padx=5)

            score_label = tk.Label(frame, text=player['score'], fg=color, bg="black", font=("Helvetica", 14, "bold"))
            score_label.grid(row=i+1, column=1, sticky="e", padx=0)

            equip_id = player.get("equip", None)

            # store widgets so they can be updated
            if equip_id is not None:
                self.player_widgets[equip_id] = {
                    "name_label": name_label,
                    "score_label": score_label
                }

        total_score = sum(player["score"] for player in team_data)
        total_label = tk.Label(frame, text=f"{total_score}", fg=color, bg="black", font=("Helvetica", 14, "bold"))
        total_label.place(relx=1.0, rely=1.0, anchor="se", x=0, y=0)

    def update_scoreboard_timer(self):
        current_time = self.game_timer.get_remaining_time()
        min, sec = map(int, current_time.split(":"))
        total_seconds = min * 60 + sec

        self.canvas.itemconfig(self.time_text, text=f"Time Remaining: {current_time}")
        if total_seconds <= 0:
            self.game_over()
            return
        self.root.after(1000, self.update_scoreboard_timer)
    
    def update_player_info(self, team_data, attacker_id = None):
        red_team_data, green_team_data = team_data
        for player in red_team_data + green_team_data:
            equip = player.get("equip")
            score = player.get("score")
            if equip in self.player_widgets:
                self.player_widgets[equip]["score_label"].config(text=score)
        
        if attacker_id and attacker_id in self.player_widgets and self.base_icon:
            label = self.player_widgets[attacker_id]["name_label"]
            label.config(image = self.base_icon, compound = "right")
            label.image = self.base_icon

    def game_over(self):
        for _ in range(3):
            broadcast_message(221)
        print("Game over broadcast sent")
        
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


    