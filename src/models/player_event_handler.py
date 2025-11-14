from src.models.UDP.UDP_client import broadcast_equipment_id, broadcast_message

class score_logic:
    

    FRIENDLY_FIRE_PENALTY = -10
    ENEMY_HIT_REWARD = 10
    BASE_REWARD = 100

    SCORES = {}

    MESSAGES = []

    def __init__(self, red_team, green_team, ui_callback=None):

        self.red_team = red_team
        self.green_team = green_team
        self.red_base_available = True
        self.green_base_available = True
        self.ui_callback = ui_callback 
        self._init_scores()

    # ----------------------------------------------------------
    def _init_scores(self):
		# create a dictionary for each member with a score of 0
		# {equip_id: {"team": str, "name": str, "score": int, "has_base" : bool}}
        
        for pid, name, equip, in self.red_team.get_players():
            self.SCORES[int(equip)] = {"team": "red", "name": name, "score": 0, "has_base": False}
        for pid, name, equip in self.green_team.get_players():
            self.SCORES[int(equip)] = {"team": "green", "name": name, "score": 0, "has_base": False}

    # ----------------------------------------------------------
    def handle_udp_message(self, msg: str):
        
        msg = msg.strip() # get rid of space in message just in case
        if not msg:
            return
        if ":" in msg:               # hit message
            self._process_hit(msg)

        else:
            print(f"[WARN] Unknown message: {msg}")

    # ----------------------------------------------------------
    def _process_hit(self, msg):
        try:
            attacker, target = map(int, msg.split(":")) #Take the message="attacker":"target" return int
        except ValueError:
            print(f"[WARN] Invalid hit: {msg}")
            return
        
        # base hit
        if target == 53:
            self._process_base_hit(attacker, "red")
            return
        
        if target == 43:
            self._process_base_hit(attacker, "green")
            return
       
        atk = self.SCORES.get(attacker) # attacker  {team ,name, score}
        tgt = self.SCORES.get(target)  # target {team ,name ,score}
        if not atk or not tgt:
            print(f"[WARN] Unknown IDs in message {msg}")
            return

        # friendly fire
        if atk["team"] == tgt["team"]:
            self.MESSAGES.append(f"{atk['name']} hit {tgt['name']}")
            print(f"[FRIENDLY-FIRE] {atk['name']} → {tgt['name']}")
            atk["score"] += self.FRIENDLY_FIRE_PENALTY
            tgt["score"] += self.FRIENDLY_FIRE_PENALTY
            broadcast_message(target)
        ## Enemy fire
        ## Don't know if I need to add this tho :)
        else:
            self.MESSAGES.append(f"{atk['name']} hit {tgt['name']}")
            print(f"[HIT] {atk['name']} ({atk['team']}) → {tgt['name']} ({tgt['team']})")
            atk["score"] += self.ENEMY_HIT_REWARD
            broadcast_message(attacker)
            broadcast_message(target)

    def _process_base_hit(self, attacker_id, base):
        atk = self.SCORES.get(attacker_id)
        if not atk:
            return

        # if red base hit (code 53 received)
        if base == "red" and self.red_base_available == True:
            if atk["team"] == "green":
                atk["score"] += self.BASE_REWARD
                atk["has_base"] = True
                self.red_base_available = False
                self.MESSAGES.append(f"[BASE HIT] {atk['name']} → Red Base")
                print(f"[BASE HIT] {atk['name'] } → Red Base")
                self._notify_ui(attacker_id)
        # if green base hit (code 43 received)
        elif base == "green" and self.green_base_available == True:
            if atk["team"] == "red":
                atk["score"] += self.BASE_REWARD
                atk["has_base"] = True
                self.green_base_available = False
                self.MESSAGES.append(f"[BASE HIT] {atk['name']} → Green Base")
                print(f"[BASE HIT] {atk['name']} → Green Base")
                self._notify_ui(attacker_id)

    def _notify_ui(self, attacker_id = None):
        if self.ui_callback:
            self.ui_callback(self.get_team_data(), attacker_id)

    def get_team_data(self):
        """Return current scoreboard for both teams."""
        red = []
        green = []
        for equip, data in self.SCORES.items():
            entry = {"name": data["name"], "score": data["score"], "equip": equip, "has_base": bool(data.get("has_base", False))}
            (red if data["team"] == "red" else green).append(entry)
        red.sort(key=lambda x: x["score"], reverse=True)
        green.sort(key=lambda x: x["score"], reverse=True)
        return red, green
