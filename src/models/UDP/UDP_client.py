import socket

from src.constants import UDPConstants

def broadcast_equipment_id(equipment_id):
    tx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tx_sock.sendto(str(equipment_id).encode("utf-8"), (UDPConstants.HOST, UDPConstants.RX_PORT))
    print(f"Sent equipment id: {equipment_id} to {UDPConstants.HOST}:{UDPConstants.RX_PORT}")
    tx_sock.close()

def broadcast_message(message):
    tx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tx_sock.sendto(str(message).encode("utf-8"), (UDPConstants.HOST, UDPConstants.TX_PORT))
    print(f"Sent start message: {message} to {UDPConstants.HOST}:{UDPConstants.TX_PORT}")
    tx_sock.close()



