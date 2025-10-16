import tkinter as tk
from src.models.Player_Action_Screen_Timer import GameScreen

radius = 30
border_width = 4

def draw_rounded_rect(canvas, x1, y1, x2, y2, radius, **kwargs):
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
    return canvas.create_polygon(points, smooth=True, **kwargs)

# Sample data to test
red_team = [
    {"name": "Opus", "score": 6025},
    {"name": "Crimson", "score": 3200},
    {"name": "Crimson", "score": 3200},
]
green_team = [{"name": "Scooby Doo", "score": 5000},
              {"name": "Opus", "score": 2500}]

# Game log - not used yet
game_log = [
    "Scooby Doo hit Opus",
    "Scooby Doo hit Opus"
]

time_remaining = "0:00"

# Create window
root = tk.Tk()
root.title("Play Action")
root.geometry("800x600")
root.configure(bg="black")

canvas = tk.Canvas(root, bg="black", highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)

game_timer = GameScreen(root)
game_timer.start_timer()

# Main scoreboard box
draw_rounded_rect(canvas, 50, 50, 750, 550, radius, fill="black", outline="yellow", width=border_width)

# Red Team Info
red_frame = tk.Frame(canvas, bg="black")
canvas.create_window(231, 55, window=red_frame, width=350, height=140, anchor="n")

red_frame.grid_columnconfigure(0, weight=1)
red_frame.grid_columnconfigure(1, weight=1)

tk.Label(red_frame, text="RED TEAM", fg="white", bg="black", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, sticky="n", padx=0, pady=0)

# Display labels for all players on red team
for i, player in enumerate(red_team):
    tk.Label(red_frame, text=player['name'], fg="red", bg="black", font=("Helvetica", 12, "bold")).grid(row=i+1, column=0, sticky="w", padx=5)
    tk.Label(red_frame, text=player['score'], fg="red", bg="black", font=("Helvetica", 12, "bold")).grid(row=i+1, column=1, sticky="e", padx=15)

# Total Red Score
total_row = len(red_team)
total_red = sum(player["score"] for player in red_team)
total_label = tk.Label(red_frame, text=f"{total_red}", fg="red", bg="black", font=("Helvetica", 12, "bold"))
total_label.place(relx=1.0, rely=1.0, anchor="se", x=-15, y=0)

# Green Team info
green_frame = tk.Frame(canvas, bg="black")
canvas.create_window(570, 55, window=green_frame, width=350, height=140, anchor="n")

green_frame.grid_columnconfigure(0, weight=1)
green_frame.grid_columnconfigure(1, weight=1)

tk.Label(green_frame, text="GREEN TEAM", fg="white", bg="black", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, sticky="n", padx=0, pady=0)

# Display labels for all players on green team
for i, player in enumerate(green_team):
    tk.Label(green_frame, text=player['name'], fg="green", bg="black", font=("Helvetica", 12, "bold")).grid(row=i+1, column=0, sticky="w", padx=5)
    tk.Label(green_frame, text=player['score'], fg="green", bg="black", font=("Helvetica", 12, "bold")).grid(row=i+1, column=1, sticky="e", padx=0)

# Total Green Score
# total_row = len(green_team)
total_green = sum(player["score"] for player in green_team)
total_label = tk.Label(green_frame, text=f"{total_green}", fg="green", bg="black", font=("Helvetica", 12, "bold"))
total_label.place(relx=1.0, rely=1.0, anchor="se", x=0, y=0)

# Game Action Log
draw_rounded_rect(canvas, 50, 200, 750, 500, radius, fill="#0a0d24", outline="yellow", width=border_width)
# canvas.create_text(400, 190, text="Current Game Action", fill="white", font=("Helvetica", 16, "bold"))

# Display game log - not used yet
# y_offset = 220
# for action in game_log:
#     canvas.create_text(60, y_offset, text=action, fill="white", font=("Helvetica", 14, "bold italic"), anchor="w")
#     y_offset += 25

# Time Remaining text
time_text = canvas.create_text(630, 525, text="", fill="white", font=("Helvetica", 16, "bold"))

def update_scoreboard_timer():
    current_time = game_timer.get_remaining_time()
    canvas.itemconfig(time_text, text=f"Time Remaining: {current_time}")
    root.after(1000, update_scoreboard_timer)

update_scoreboard_timer()

root.mainloop()