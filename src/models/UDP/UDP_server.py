import socket
import threading

from src.constants import UDPConstants
from src.models.player_event_handler import score_logic
from src.models.teams.green_team import GreenTeam
from src.models.teams.red_team import RedTeam


rx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rx_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
rx_sock.bind((UDPConstants.HOST, UDPConstants.RX_PORT))

def start_receiving():
    def listen():
        Score_logic = score_logic(RedTeam(), GreenTeam())
        while True:
            data, addr = rx_sock.recvfrom(UDPConstants.BUF_SIZE)
            message = data.decode('utf-8')
            Score_logic.handle_udp_message(message)
            
    threading.Thread(target=listen, daemon=True).start()
