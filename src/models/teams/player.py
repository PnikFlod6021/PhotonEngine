from src.models.database import search

class Player():
    def __init__(self,player_id, codename):
        self.player_id = player_id
        self.codename = codename
        self.equipment_id = 0
        self.is_on_team = False

    
    def is_valid_player(self):
        if not self.player_id or not self.player_id.isdigit():
            return False
        
        return True
    
    def has_valid_equipment_id(self, equipment_id):
        if not equipment_id or not equipment_id.isdigit():
            return False

        return True

    def is_red(self):
        return int(self.player_id) % 2 != 0
    
    def is_green(self):
        return int(self.player_id) % 2 == 0
    
    def get_player_id(self):
        return self.player_id
    
    def get_codename(self):
        return self.codename
    
    def set_player_codename(self,codename):
        self.codename = codename
    
    def search_database(self,player_id):
        player_data = search(player_id)

        if player_data:
            codename = player_data[1]
            return codename
        
        return None

    def has_codename(self):
        return self.codename is not None
    
    def set_equipment_id(self,equipment_id):
        self.equipment_id = equipment_id
    
    def get_equipment_id(self):
        return self.equipment_id

        
