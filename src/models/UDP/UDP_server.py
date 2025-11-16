import socket
import threading
import time

from src.constants import UDPConstants
from src.models.player_event_handler import score_logic
from src.models.teams.green_team import GreenTeam
from src.models.teams.red_team import RedTeam

STOP_RUNNING = threading.Event()

rx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rx_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
rx_sock.bind((UDPConstants.HOST, UDPConstants.RX_PORT))

def start_receiving(score_logic_instance):
    def listen():
        # Score_logic = score_logic(RedTeam(), GreenTeam())
        while not STOP_RUNNING.is_set():
            data, addr = rx_sock.recvfrom(UDPConstants.BUF_SIZE)
            message = data.decode('utf-8')
            score_logic_instance.handle_udp_message(message)
            
    threading.Thread(target=listen, daemon=True).start()

def stop_receiving():
    STOP_RUNNING.set()
    rx_sock.close()