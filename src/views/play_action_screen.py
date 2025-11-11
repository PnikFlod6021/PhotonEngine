import tkinter as tk
from src.models.Timers.Player_Action_Screen_Timer import GameScreen
from src.models.teams.green_team import GreenTeam
from src.models.teams.red_team import RedTeam
from src.models.game_audio_handler import GameAudioHandler
from src.models.player_event_handler import score_logic

class PlayActionScreen:
    def __init__(self,red_team_data, green_team_data, game_log):
        game_audio_handler = GameAudioHandler()

        root = tk.Tk()
        root.title("Play Action")
        root.geometry("1200x800")
        root.configure(bg="black")

        self.root = root
        self.red_team_data = red_team_data
        self.green_team_data = green_team_data

        self.score_logic = score_logic(red_team_data, green_team_data)
        self.scores = self.score_logic.SCORES
        self.hit_messages = []
        self.current_hit_index = 0

        self.green_score_labels = {}
        self.red_score_labels = {}

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

        # self.entry_terminal = EntryTerminalHandler(self.root)
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
        # compute totals so we can determine which total is highest
        red_total = sum(player_data["score"] for equip_id, player_data in self.scores.items() if player_data["team"] == "red")
        green_total = sum(player_data["score"] for equip_id, player_data in self.scores.items() if player_data["team"] == "green")

        red_team_data = {equipment_id:player_data for equipment_id,player_data in self.scores.items() if player_data["team"] == "red"}
        green_team_data = {equipment_id:player_data for equipment_id,player_data in self.scores.items() if player_data["team"] == "green"}

        # Pass whether this team's total is the (co-)highest so it can flash
        self.create_team_frame(red_team_data, "RED TEAM", "red", 56, total_score=red_total, is_highest=(red_total >= green_total))

        # Create green team frame
        self.create_team_frame(green_team_data, "GREEN TEAM", "green", 325, total_score=green_total, is_highest=(green_total >= red_total))

        # Game log box
        self.draw_rounded_rect(620, 50, 1150, 650, self.radius,
                       fill="#0a0d24", outline="yellow", width=self.border_width)

        self.game_log_box = tk.Text(self.canvas, width=58, height=35,bg="#0a0d24", fg="white",font=("Helvetica", 12), wrap="word")

        self.canvas.create_window(620, 55, window=self.game_log_box,anchor="nw", width=530, height=595)

        self.game_log_box.config(state=tk.DISABLED)

        # Time remaining label
        self.time_text = self.canvas.create_text(900, 680, text="", fill="white", font=("Helvetica", 16, "bold"))

    def create_team_frame(self, team_data, label, color, x, total_score, is_highest):
        frame = tk.Frame(self.canvas, bg="black")
        self.canvas.create_window(x, 55, window=frame, width=269, height=594, anchor="nw")

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        tk.Label(frame, text=label, fg="white", bg="black", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, sticky="n", padx=0, pady=0)

        # Sort team data list from highest to lowest
        sorted_data = sorted(team_data.items(), key=lambda player_data: player_data[1]['score'], reverse=True)
        
        for i, (equip_id, player_data) in enumerate(sorted_data):
            tk.Label(frame, text=player_data['name'], fg=color, bg="black", font=("Helvetica", 14, "bold")).grid(row=i+1, column=0, sticky="w", padx=25)
            score_label = tk.Label(frame, text=player_data['score'], fg=color, bg="black", font=("Helvetica", 14, "bold"))
            score_label.grid(row=i+1, column=1, sticky="e", padx=0)
            if color == "red":
                self.red_score_labels[equip_id] = score_label
            elif color == "green":
                self.green_score_labels[equip_id] = score_label

        total_label = tk.Label(frame, text=f"{total_score}", fg=color, bg="black", font=("Helvetica", 14, "bold"))
        total_label.place(relx=1.0, rely=1.0, anchor="se", x=0, y=0)

        total_label.original_color = color

        if color == "red":
            self.red_total_label = total_label
        else:
            self.green_total_label = total_label

        if is_highest:
            self.flash_label(total_label, color, "white")

    def update_scoreboard_timer(self):
        current_time = self.game_timer.get_remaining_time()
        self.canvas.itemconfig(self.time_text, text=f"Time Remaining: {current_time}")
        
        self.scores = self.score_logic.SCORES

        if len(self.score_logic.MESSAGES) > self.current_hit_index:
            self.hit_messages = self.score_logic.MESSAGES[(self.current_hit_index + 1):]
            self.current_hit_index = len(self.hit_messages)
        else:
            self.hit_messages = []

        red_total = sum(player_data["score"] for equip_id, player_data in self.scores.items() if player_data["team"] == "red")
        green_total = sum(player_data["score"] for equip_id, player_data in self.scores.items() if player_data["team"] == "green")

        self.red_total_label.config(text=red_total)
        self.green_total_label.config(text=green_total)

        if red_total > green_total:
            self.stop_flashing(self.green_total_label)
            self.flash_label(self.red_total_label, "red", "white")
        elif green_total > red_total:
            self.stop_flashing(self.red_total_label)
            self.flash_label(self.green_total_label, "green", "white")
        else:
            self.flash_label(self.red_total_label, "red", "white")
            self.flash_label(self.green_total_label, "green", "white")

        for equipment_id,player_data in self.scores.items():
            for equip_id, label in self.red_score_labels.items():
                if int(equip_id) == int(equipment_id):
                    label.config(text=player_data["score"])

        for equipment_id,player_data in self.scores.items():
            for equip_id, label in self.green_score_labels.items():
                if int(equip_id) == int(equipment_id):
                    label.config(text=player_data["score"])
        

        for message in self.hit_messages:
            self.log_event(message)
        

        self.root.after(500, self.update_scoreboard_timer)


    def flash_label(self, label, color1, color2, interval=500):
        def toggle():
            current_color = label.cget("fg")
            new_color = color2 if current_color == color1 else color1
            label.config(fg=new_color)
            job_id = self.root.after(interval, toggle)
            self.flash_jobs[label] = job_id
        toggle()

    def stop_flashing(self, label):
        job_id = self.flash_jobs.pop(label, None)
        if job_id:
            self.root.after_cancel(job_id)
            label.config(fg=label.original_color)  # Reset to original

    def log_event(self, event_text):
        self.game_log_box.config(state=tk.NORMAL)
        self.game_log_box.insert(tk.END, event_text + "\n")
        self.game_log_box.yview(tk.END)  
        self.game_log_box.config(state=tk.DISABLED)
 

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


    