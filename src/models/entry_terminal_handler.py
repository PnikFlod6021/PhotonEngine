import tkinter as tk
from tkinter import messagebox 
import socket

from models.database import search, add_player, delete_player
from constants import TerminalConstants, UDPConstants
from UDP_client import broadcast_equipment_id


class EntryTerminalHandler():
    def __init__(self, root):
        self.root = root
        self.red_player_id_entries = []
        self.red_player_codename_entries = []
        self.green_player_id_entries = []
        self.green_player_codename_entries = []
        self.red_players = {}   
        self.green_players = {} 
        self.red_spots_left = [i for i in range(TerminalConstants.PLAYER_MAX_COUNT)]
        self.green_spots_left = [i for i in range(TerminalConstants.PLAYER_MAX_COUNT)]

    def display_player_id_screen(self, event):
        player_id_string = tk.StringVar()
        top = tk.Toplevel(self.root)
        top.geometry("200x200")
        top.title("Player ID")

        tk.Label(top, text="Enter Player ID").grid(row=0, column=0)
        e1 = tk.Entry(top, textvariable=player_id_string)
        e1.grid(row=0, column=1)

        def close_window():
            player_id = player_id_string.get()

            if not player_id:
                messagebox.showwarning("Player ID", "Must Enter Player ID")
                top.destroy()
                return 
            
            try:
                player_id_temp = int(player_id)
            except:
                messagebox.showwarning("Player ID", "Must Enter Valid Player ID")
                top.destroy()
                return 

            player_data = search(player_id)

            if player_id in self.red_players or player_id in self.green_players:
                messagebox.showwarning("Player ID", "Entered Player ID already in game")
                top.destroy()
                return 

            if int(player_id) % 2 != 0:
                if len(self.red_players) >= TerminalConstants.PLAYER_MAX_COUNT:
                    messagebox.showwarning("Player Count", "You have exceeded max player count on RED Team")
                    top.destroy()
                    return 
                if player_data:
                    codename = player_data[1]
                    self.display_codename_screen(event,"red",player_id,codename=codename)
                else:
                    self.display_codename_screen(event, "red", player_id,codename=None)
                
            else:
                if len(self.green_players) >= TerminalConstants.PLAYER_MAX_COUNT:
                    messagebox.showwarning("Player Count", "You have exceeded max player count on GREEN Team")
                    top.destroy()
                    return 
                if player_data:
                    codename = player_data[1]
                    self.display_codename_screen(event,"green",player_id,codename=codename)
                else:
                    self.display_codename_screen(event, "green", player_id,codename=None)
                    

            top.destroy()

        tk.Button(top, text="OK", command=close_window).grid(row=1, column=0)

    def display_codename_screen(self, event, color, player_id, codename=None):

        if codename and color == "red":
            self.display_equipment_id_screen(event,codename,player_id,"red")
            return
        elif codename and color == "green":
            self.display_equipment_id_screen(event,codename,player_id,"green")
            return

        codename_string = tk.StringVar()
        top = tk.Toplevel(self.root)
        top.geometry("200x200")
        top.title("Codename")

        tk.Label(top, text="Enter Codename").grid(row=0, column=0)
        e1 = tk.Entry(top, textvariable=codename_string)
        e1.grid(row=0, column=1)

        def close_window():
            codename = codename_string.get()
            if not codename:
                messagebox.showwarning("Codename", "Must Enter Codename")
                top.destroy()
                return 

            if color == "red":
                add_player(player_id,codename)
                self.display_equipment_id_screen(event,codename,player_id,"red")
                
            else:
                add_player(player_id,codename)
                self.display_equipment_id_screen(event,codename,player_id,"green")

            top.destroy()

        tk.Button(top, text="OK", command=close_window).grid(row=1, column=0)

    def update_player_id(self, player_id, id_list, col, row=0):
        id_list[row][col].config(state="normal")
        id_list[row][col].insert(0, player_id)
        id_list[row][col].config(state="readonly")

    def update_player_codename(self, codename, codename_list, col, row=0):
        codename_list[row][col].config(state="normal")
        codename_list[row][col].insert(0, codename)
        codename_list[row][col].config(state="readonly")

    def delete_player(self, event):
        player_id_to_delete = tk.StringVar()
        top = tk.Toplevel(self.root)
        top.geometry("200x200")
        top.title("Delete Player")

        tk.Label(top, text="Enter Player ID").grid(row=0, column=0)
        e1 = tk.Entry(top, textvariable=player_id_to_delete)
        e1.grid(row=0, column=1)

        def close_window():
            player_to_delete = player_id_to_delete.get()

            try:
                if int(player_to_delete) % 2 == 0:
                    index = self.green_players.pop(player_to_delete)
                    self.green_player_id_entries[0][index].config(state="normal")
                    self.green_player_id_entries[0][index].delete(0, tk.END)
                    self.green_player_id_entries[0][index].config(state="readonly")

                    self.green_player_codename_entries[0][index].config(state="normal")
                    self.green_player_codename_entries[0][index].delete(0, tk.END)
                    self.green_player_codename_entries[0][index].config(state="readonly")

                    self.green_spots_left.insert(0, index)
                else:
                    index = self.red_players.pop(player_to_delete)
                    self.red_player_id_entries[0][index].config(state="normal")
                    self.red_player_id_entries[0][index].delete(0, tk.END)
                    self.red_player_id_entries[0][index].config(state="readonly")

                    self.red_player_codename_entries[0][index].config(state="normal")
                    self.red_player_codename_entries[0][index].delete(0, tk.END)
                    self.red_player_codename_entries[0][index].config(state="readonly")

                    self.red_spots_left.insert(0, index)
            except KeyError:
                messagebox.showwarning("Delete Player", "Player ID not found on Teams")
                top.destroy()
                return 

            top.destroy()

        tk.Button(top, text="OK", command=close_window).grid(row=1, column=0)
    
    def delete_all_players(self,event):
        for player_id, index in self.red_players.items():
            self.red_player_id_entries[0][index].config(state="normal")
            self.red_player_id_entries[0][index].delete(0, tk.END)
            self.red_player_id_entries[0][index].config(state="readonly")

            self.red_player_codename_entries[0][index].config(state="normal")
            self.red_player_codename_entries[0][index].delete(0, tk.END)
            self.red_player_codename_entries[0][index].config(state="readonly")

        for player_id, index in self.green_players.items():
            self.green_player_id_entries[0][index].config(state="normal")
            self.green_player_id_entries[0][index].delete(0, tk.END)
            self.green_player_id_entries[0][index].config(state="readonly")

            self.green_player_codename_entries[0][index].config(state="normal")
            self.green_player_codename_entries[0][index].delete(0, tk.END)
            self.green_player_codename_entries[0][index].config(state="readonly")

        self.red_players.clear()
        self.green_players.clear()
        self.red_spots_left = [i for i in range(TerminalConstants.PLAYER_MAX_COUNT)]
        self.green_spots_left = [i for i in range(TerminalConstants.PLAYER_MAX_COUNT)]


    def display_equipment_id_screen(self, event, codename, player_id, color):
        equipment_id = tk.StringVar()
        top = tk.Toplevel(self.root)
        top.geometry("200x200")
        top.title("Equipment ID")

        tk.Label(top, text="Enter Equipment ID").grid(row=0, column=0)
        e1 = tk.Entry(top, textvariable=equipment_id)
        e1.grid(row=0, column=1)

        def close_window():
            try:
                equip_id = int(equipment_id.get())
            except:
                messagebox.showwarning("Invalid Equipment ID. Please Try again")
                top.destroy()
                return 
            
            if equipment_id.get():
                broadcast_equipment_id((equipment_id.get()))
            else:
                messagebox.showwarning("Equipment ID","Must Enter Equipment ID")
                top.destroy()
                return 

           

            if color == "red":
                index = self.red_spots_left.pop(0)
                self.red_players[player_id] = index
                self.update_player_id(player_id, self.red_player_id_entries, col=index)
                self.update_player_codename(codename, self.red_player_codename_entries, col=index)
            else:
                index = self.green_spots_left.pop(0)
                self.green_players[player_id] = index
                self.update_player_id(player_id, self.green_player_id_entries, col=index)
                self.update_player_codename(codename, self.green_player_codename_entries, col=index)

            top.destroy()

        tk.Button(top, text="OK", command=close_window).grid(row=1, column=0)
    



    def change_ip_address(self, event):
        top = tk.Toplevel(self.root)
        top.geometry("200x200")
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
