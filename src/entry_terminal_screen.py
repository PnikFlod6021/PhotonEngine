import tkinter as tk
from models.database import search

class PlayerEntryGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.player_id = None
        self.createGUI()



    def display_player_id_screen(self,event):
        player_id_string = tk.StringVar()

        #Create mini window the ask for player id input
        top = tk.Toplevel(self.root)
        top.geometry("200x200")
        top.title("Player ID")

        #Create Label and TextBox for Player to enter Player ID
        tk.Label(top, text="Enter Player ID").grid(row=0, column=0)
        e1 = tk.Entry(top, textvariable=player_id_string)
        e1.grid(row=0, column=1)

        def close_window():
            self.player_id = player_id_string.get()
            print(search(self.player_id))
            self.display_codename_screen(event)
            top.destroy()

        #Create button that when clicked, gets the Player ID input and then destroys window
        b1 = tk.Button(top, text="OK", command=close_window)
        b1.grid(row=1, column=0)


    def display_codename_screen(self,event):
        codename_string = tk.StringVar()

        # Create mini window the ask for player id input
        top = tk.Toplevel(self.root)
        top.geometry("200x200")
        top.title("Codename")

        # Create Label and TextBox for Player to enter Player ID
        tk.Label(top, text="Enter Codename").grid(row=0, column=0)
        e1 = tk.Entry(top, textvariable=codename_string)
        e1.grid(row=0, column=1)

        def close_window():
            print(codename_string.get())
            self.display_equipment_id_screen(event)
            top.destroy()

        # Create button that when clicked, gets the Player ID input and then destroys window
        b1 = tk.Button(top, text="OK", command=close_window)
        b1.grid(row=1, column=0)

    def display_equipment_id_screen(self,event):
        equipment_id = tk.StringVar()

        # Create mini window the ask for player id input
        top = tk.Toplevel(self.root)
        top.geometry("200x200")
        top.title("Equipment ID")

        # Create Label and TextBox for Player to enter Player ID
        tk.Label(top, text="Enter Equipment ID").grid(row=0, column=0)
        e1 = tk.Entry(top, textvariable=equipment_id)
        e1.grid(row=0, column=1)

        def close_window():
            print(equipment_id.get())
            top.destroy()

        # Create button that when clicked, gets the Player ID input and then destroys window
        b1 = tk.Button(top, text="OK", command=close_window)
        b1.grid(row=1, column=0)

    def createGUI(self):
        self.root.title("Entry Terminal")

        # Set background color
        self.root.configure(bg="#000000")

        # Constants for team colors
        RED_TEAM_BG = "#330000"
        GREEN_TEAM_BG = "#003300"
        LABEL_TEXT_COLOR="lightgray"

        # Title label
        title_label = tk.Label(self.root,
                           text="Edit Current Game",
                           bg="#000000",
                           fg="#7575fb",
                           font=("Helvetica", 16, "bold"))
        title_label.grid(row=0, column = 0, columnspan=5, pady=(5, 0), sticky="n")

        # Create team frames

        red_frame = tk.LabelFrame(self.root,
                          text="RED TEAM",
                          bg=RED_TEAM_BG,
                          fg=LABEL_TEXT_COLOR,
                          padx=10,
                          pady=0,
                          bd=0,
                          labelanchor="n")
        green_frame = tk.LabelFrame(self.root,
                            text="GREEN TEAM",
                            bg=GREEN_TEAM_BG,
                            fg=LABEL_TEXT_COLOR,
                            padx=10,
                            pady=0,
                            bd=0,
                            labelanchor="n")
        red_frame.grid(row=1, column=1)
        green_frame.grid(row=1, column=2)

        # spacers
        tk.Frame(self.root, bg="#000000", width=100).grid(row=1, column=0)
        tk.Frame(self.root, bg="#000000", width=100).grid(row=1,column=4)

        # Add player rows
        for i in range(19):
            tk.Checkbutton(red_frame, bg=RED_TEAM_BG, selectcolor=RED_TEAM_BG).grid(row=i, column=0, sticky="e")
            tk.Label(red_frame, text=f"{i+1}", bg=RED_TEAM_BG, fg=LABEL_TEXT_COLOR, padx=0).grid(row=i, column=1, sticky="w")

            entry = tk.Entry(red_frame)
            entry2 = tk.Entry(red_frame)
            entry.grid(row=i, column=2)
            entry2.grid(row=i, column=3)
            entry.bind("<Button>",self.display_player_id_screen)


            tk.Checkbutton(green_frame, bg=GREEN_TEAM_BG, selectcolor=GREEN_TEAM_BG).grid(row=i, column=0)
            tk.Label(green_frame, text=f"{i+1}", bg=GREEN_TEAM_BG, fg=LABEL_TEXT_COLOR, padx=0).grid(row=i, column=1, sticky="w")
            tk.Entry(green_frame).grid(row=i, column=2)
            tk.Entry(green_frame).grid(row=i, column=3)

        # Game mode text label
        game_mode_label = tk.Label(self.root, text="Game Mode: Standard public mode", bg="#2E2E2E", fg="white")
        game_mode_label.grid(row=2, column=0, columnspan=5, sticky="n")

        # Black spacer
        tk.Frame(self.root, bg="#000000", height=20).grid(row=3, column=0, columnspan=5)

        # Function key buttons
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=4, column=0, columnspan=5)
        for i, label in enumerate(["F1: New Game", "F2: Load Game", "F3: Save Game", "F4: Save As", "F5: Print", "F6: Print Setup", "F7: Exit"]):
            tk.Button(button_frame, text=label).grid(row=0, column=i, padx=2)

        # Status bar
        status = tk.Label(self.root, text="<Del> to Delete Player, <Ins> to Manually Insert, or edit codename", bd=1, relief=tk.SUNKEN, anchor=tk.CENTER)
        status.grid(row=5, column=0, columnspan=5, sticky="we")

        self.root.mainloop()

if __name__ == "__main__":
    PlayerEntryGUI()