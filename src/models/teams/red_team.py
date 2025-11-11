from src.constants import TerminalConstants

MAX_PLAYER_COUNT = TerminalConstants.PLAYER_MAX_COUNT
PLAYERS = []
PLAYER_INDEX = {player_index:None for player_index in range(MAX_PLAYER_COUNT)}

class RedTeam():
    def __init__(self):
        pass

    
    def is_full(self):
        for index, player_id in PLAYER_INDEX.items():
            if not player_id:
                return False
        
        return True

    def add_new_player(self,Player):
        added_index = None
        for index, player_id in PLAYER_INDEX.items():
            if not player_id:
                PLAYER_INDEX[index] = Player.get_player_id()
                added_index = index
                break
        
        PLAYERS.append((Player.get_player_id(),Player.get_codename(), Player.get_equipment_id()))
        Player.is_on_team = True

        return added_index
    
    def remove_player(self,player_id_to_delete):
        remove_index = None
        for index,player_id in PLAYER_INDEX.items():
            if player_id == player_id_to_delete:
                remove_index = index
                PLAYER_INDEX[index] = None
                break
        
        i = 0
        for player_id, player_codename, equipment_id in PLAYERS:
            if player_id == player_id_to_delete:
                PLAYERS.pop(i)
                break
            i += 1
        
        return remove_index
    
    def has_duplicate_equipment_id(self,equipment_id):
        for player_id, player_data, player_equip_id in PLAYERS:
            if int(player_equip_id) == int(equipment_id):
                return True

        return False

    def has_duplicate_player(self,p_id):
        for player_id, player_data, player_equip_id in PLAYERS:
            if player_id == p_id:
                return True

        return False
    
    def get_indexes(self):
        return PLAYER_INDEX
    
    def get_players(self):
        return PLAYERS
    