import tkinter as tk
from tkinter import messagebox 
import socket

from src.models.database import search, add_player, delete_player
from src.constants import TerminalConstants, UDPConstants
from src.models.UDP.UDP_client import broadcast_equipment_id
from src.models.teams.player import Player
from src.models.teams.green_team import GreenTeam
from src.models.teams.red_team import RedTeam

GREEN_TEAM = GreenTeam()
RED_TEAM = RedTeam()
MAX_PLAYERS = TerminalConstants.PLAYER_MAX_COUNT

class EntryTerminalHandler():

    def __init__(self, root):
        self.root = root

        self.Player = Player(0,None)

        self.red_player_id_entries = []
        self.red_player_codename_entries = []
        self.green_player_id_entries = []
        self.green_player_codename_entries = []
        


    def get_player_input(self,event):
        self.create_input_window(title="Player ID", input_text="Enter Player ID", handler_fn=self.handle_player_id_input)


    def handle_player_id_input(self, player_id_entry, top):
        player_id = player_id_entry.get()
        self.Player = Player(player_id,None)

        if not self.Player.is_valid_player():
            (self.display_error_message(
                top,
                "Invalid Player ID", 
                "Must Enter Valid Player ID"
            ))
            return
        
        if GREEN_TEAM.has_duplicate_player(player_id) or RED_TEAM.has_duplicate_player(player_id):
            (self.display_error_message(
                top,
                "Player ID", 
                "Player ID Already Exists in Game"
            ))
            return
        
        player_codename = self.Player.search_database(int(player_id))
        self.Player.set_player_codename(player_codename)
        
    
        if self.Player.is_red() and RED_TEAM.is_full():
            (self.display_error_message(
                top,
                "Team Full", 
                "Red Team is Full. Delete player and try again"
            ))
            return
        
        if self.Player.is_green() and GREEN_TEAM.is_full():
            (self.display_error_message(
                top,
                "Team Full", 
                "Green Team is Full. Delete player and try again"
            ))
            return
        
        if not self.Player.has_codename():
            self.create_input_window(title="Player Codename", input_text="Enter Player Codename", handler_fn=self.handle_player_codename_input)
        else:
            self.create_input_window(title="Equipment ID", input_text="Enter Player Equipment ID", handler_fn=self.handle_player_equipment_id_input)

        top.destroy()

    def handle_player_codename_input(self, codename_entry, top):
        codename = codename_entry.get()

        if not codename:
            self.display_error_message(top,"Codename", "Must Enter Codename")
            return

        player_id = self.Player.get_player_id()
        self.Player.set_player_codename(codename)

        add_player(player_id,codename)

        self.create_input_window(title="Equipment ID", input_text="Enter Player Equipment ID", handler_fn=self.handle_player_equipment_id_input)

        top.destroy()

    def handle_player_equipment_id_input(self,equip_id_entry, top):

        equip_id = equip_id_entry.get()

        if not self.Player.has_valid_equipment_id(equip_id):
            (self.display_error_message
            (   
                top,
                "Equipment ID", 
                "Invalid Equipment ID. Please Try again"
            ))
            return
        
        if RED_TEAM.has_duplicate_equipment_id(equip_id) or GREEN_TEAM.has_duplicate_equipment_id(equip_id):
            (self.display_error_message
            (   
                top,
                "Equipment ID", 
                "Equipment ID already in use"
            ))
            return
            
        self.Player.set_equipment_id(equip_id)
        broadcast_equipment_id(int(equip_id))

        if self.Player.is_red():
            index = RED_TEAM.add_new_player(self.Player)
        else:
            index = GREEN_TEAM.add_new_player(self.Player)

        self.update_player_on_screen(self.Player, col=index)
        
        top.destroy()


    def delete_player_on_screen(self,event):
        self.create_input_window(title="Delete Player", input_text="Enter Player ID to Delete", handler_fn=self.handle_player_deletion)

    def handle_player_deletion(self,player_to_delete_entry,top):
        player_id_to_delete = player_to_delete_entry.get()
        temp_player = Player(player_id_to_delete,None)


        if not player_id_to_delete:
            self.display_error_message(top,"Delete Player", "Must Enter Valid Player ID to delete")
            return

        if temp_player.is_red():
            index_to_remove = RED_TEAM.remove_player(player_id_to_delete)

            if index_to_remove is None:
                self.display_error_message(top,"Delete Player", "Player ID not found on Red Team")
                return

            self.delete_player(temp_player,col=index_to_remove)

        else:
            index_to_remove = GREEN_TEAM.remove_player(player_id_to_delete)

            if index_to_remove is None:
                self.display_error_message(top,"Delete Player", "Player ID not found on Green Team")
                return

            self.delete_player(temp_player,index_to_remove)

        top.destroy()
    
    def change_ip_address(self, event):
        top = tk.Toplevel(self.root)
        top.geometry("400x200")
        top.title("Network Address")

        tk.Label(top, text="Enter Network Address").grid(row=0, column=0)
        e1 = tk.Entry(top)
        e1.grid(row=0, column=1)

        def close_window():
            if e1.get():
                UDPConstants.HOST = e1.get()
                top.destroy()
            else:
                messagebox.showwarning("Network","Must Enter Valid Network Address")
                top.destroy()
                return 

        tk.Button(top, text="OK", command=close_window).grid(row=1, column=0)
    
    def update_player_on_screen(self, Player, col, row=0):
        id_list = None
        codename_list = None

        if Player.is_red():
            id_list = self.red_player_id_entries
            codename_list = self.red_player_codename_entries
        else:
            id_list = self.green_player_id_entries
            codename_list = self.green_player_codename_entries

        id_list[row][col].config(state="normal")
        id_list[row][col].insert(0, str(self.Player.get_player_id()))
        id_list[row][col].config(state="readonly")

        codename_list[row][col].config(state="normal")
        codename_list[row][col].insert(0, str(self.Player.get_codename()))
        codename_list[row][col].config(state="readonly")
    
    def delete_player(self,Player, col, row=0):
        id_list = None
        codename_list = None

        if Player.is_red():
            id_list = self.red_player_id_entries
            codename_list = self.red_player_codename_entries
        else:
            id_list = self.green_player_id_entries
            codename_list = self.green_player_codename_entries

        id_list[row][col].config(state="normal")
        id_list[row][col].delete(0, tk.END)
        id_list[row][col].config(state="readonly")

        codename_list[row][col].config(state="normal")
        codename_list[row][col].delete(0, tk.END)
        codename_list[row][col].config(state="readonly")
    
    def delete_all_players(self,event):
        for i in range(MAX_PLAYERS):
            self.delete_player(Player(1,None), i)
            self.delete_player(Player(0,None), i)
        
        for player_index, player_id in GREEN_TEAM.player_index.items():
            if player_id: 
                GREEN_TEAM.remove_player(player_id)
        
        for player_index, player_id in RED_TEAM.player_index.items():
            if player_id:
                RED_TEAM.remove_player(player_id)


    def display_error_message(self,top,message_top_text=None,error_text=None):
        messagebox.showwarning(message_top_text,error_text)
        top.destroy()

    def create_input_window(self,size="200x200",title="Input Window",input_text="Enter Input",handler_fn=None):
        top = tk.Toplevel(self.root)
        top.geometry(size)
        top.title(title)

        tk.Label(top, text=input_text).grid(row=0, column=0)
        e1 = tk.Entry(top)
        e1.grid(row=0, column=1)

        tk.Button(top, text="OK", command=lambda: handler_fn(e1, top)).grid(row=1, column=0)