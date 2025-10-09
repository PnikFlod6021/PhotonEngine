import tkinter as tk
from models.entry_terminal_handler import EntryTerminalHandler
from constants import TerminalConstants

class PlayerEntryGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.terminal_handler = EntryTerminalHandler(self.root)
        self.createGUI()


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

        red_id_entries = []
        red_codename_entries = []

        green_id_entries = []
        green_codename_entries = []
        # Add player rows
        for i in range(TerminalConstants.PLAYER_MAX_COUNT):
            #Creating headers for red and green team
            tk.Label(red_frame, text=f"{i+1}", bg=RED_TEAM_BG, fg=LABEL_TEXT_COLOR, padx=0).grid(row=i, column=1, sticky="w")
            tk.Label(green_frame, text=f"{i+1}", bg=GREEN_TEAM_BG, fg=LABEL_TEXT_COLOR, padx=0).grid(row=i, column=1, sticky="w")
            
            #This creates an entry field for the red and green side
            red_player_id_entry = tk.Entry(red_frame)
            red_player_codename_entry = tk.Entry(red_frame)
            green_player_id_entry = tk.Entry(green_frame)
            green_player_codename_entry = tk.Entry(green_frame)

            #Here, we create a grid of entries/input fields or a grid of 2x19 on each side that the user can give input
            red_player_id_entry.grid(row=i, column=2)
            red_player_codename_entry.grid(row=i, column=3)
            green_player_id_entry.grid(row=i, column=2)
            green_player_codename_entry.grid(row=i, column=3)

            #We want the user to only enter player_id and codename if a key is pressed
            #So, these entries are read only, so the user cannot directly enter into them
            red_player_id_entry.config(state="readonly")
            red_player_codename_entry.config(state="readonly")
            green_player_id_entry.config(state="readonly")
            green_player_codename_entry.config(state="readonly")


            #We are taking each of these input fields and storing them in a list, so we can manipulate them later
            red_id_entries.append(red_player_id_entry)
            red_codename_entries.append(red_player_codename_entry)
            green_id_entries.append(green_player_id_entry)
            green_codename_entries.append(green_player_codename_entry)


        #Storing the input fields in a list that is defined in the terminal handler model, where we can manipulate the data
        self.terminal_handler.red_player_id_entries.append(red_id_entries)
        self.terminal_handler.red_player_codename_entries.append(red_codename_entries)
        self.terminal_handler.green_player_id_entries.append(green_id_entries)
        self.terminal_handler.green_player_codename_entries.append(green_codename_entries)

        #Binding an event to the window, so if I or i is pressed, it will trigger the insert player logic
        self.root.bind(TerminalConstants.INSERT.upper(), self.terminal_handler.get_player_input)
        self.root.bind(TerminalConstants.INSERT, self.terminal_handler.get_player_input)

        self.root.bind(TerminalConstants.DELETE.upper(), self.terminal_handler.delete_player_on_screen)
        self.root.bind(TerminalConstants.DELETE, self.terminal_handler.delete_player_on_screen)

        self.root.bind(TerminalConstants.DELETE_ALL, self.terminal_handler.delete_all_players)

        self.root.bind(TerminalConstants.CHANGE_IP, self.terminal_handler.change_ip_address)

        self.root.bind(TerminalConstants.EXIT, lambda event: self.root.destroy())

        # Game mode text label
        game_mode_label = tk.Label(self.root, text="Game Mode: Standard public mode", bg="#2E2E2E", fg="white")
        game_mode_label.grid(row=2, column=0, columnspan=5, sticky="n")

        # Black spacer
        tk.Frame(self.root, bg="#000000", height=20).grid(row=3, column=0, columnspan=5)

        # Function key buttons
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=4, column=0, columnspan=5)
        for i, label in enumerate(["F1: New Game", "F2: Load Game", "F3: Save Game", "F4: Save As", "F5: Print", "F6: Change Network Address", "F7: Exit"]):
            tk.Button(button_frame, text=label).grid(row=0, column=i, padx=2)

        # Status bar
        status = tk.Label(self.root, text="<D or d> to Delete Player, <I or i> to Manually Insert, <F12> to delete all players", bd=1, relief=tk.SUNKEN, anchor=tk.CENTER)
        status.grid(row=5, column=0, columnspan=5, sticky="we")

        self.root.mainloop()

if __name__ == "__main__":
    PlayerEntryGUI()