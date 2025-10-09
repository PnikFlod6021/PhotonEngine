import socket

from constants import UDPConstants


# Create and bind the Receiver socket
rx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rx_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
rx_sock.bind((UDPConstants.HOST, UDPConstants.RX_PORT))
### The code will stop here until something is sent to RX_PORT
# if data is 202 it means the game is about to start and start trabsmitting equipment codes
received_data = ' '
while True:
	data, addr = rx_sock.recvfrom(1024) 
	received_data = data.decode('utf-8')
	print(f"Received equipment id: {data} from {addr}")


