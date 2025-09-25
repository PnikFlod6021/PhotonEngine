import socket

HOST = "127.0.0.1"   # IP address
TX_PORT = 7500       #  transmit on 7500

# Create UDP TX socket
tx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

RX_PORT = 7501
BUF_SIZE = 1024

# Create and bind the Receiver socket
rx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rx_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
rx_sock.bind(("0.0.0.0", RX_PORT))
### The code will stop here until something is sent to RX_PORT
# if data is 202 it means the game is about to start and start trabsmitting equipment codes
print("listening")
received_data = ' '
while received_data != '202':
	print("data was not 202")
	data, addr = rx_sock.recvfrom(BUF_SIZE) 
	received_data = data.decode('utf-8')
	print ("Received from game software: " + received_data)
print ('')



###### This is a while True Loop that keeps checking for your input
# take your input and send data to TX_PORT
while True:
    try:
        s = input("code> ").strip()
        if not s:
            continue
        if s.lower() in {"q", "quit", "exit"}:
            break
        # ensure it's an integer string (per spec transmissions are integers)
        int(s)  # will raise ValueError if not numeric
        tx_sock.sendto(s.encode("utf-8"), (HOST, TX_PORT))
        print(f"sent → {HOST}:{TX_PORT}  {s}")
    except ValueError:
        print("Please enter an integer (or 'quit' to exit).")
    except KeyboardInterrupt:
        print("\n^C - exiting.")
        break

tx_sock.close()
print("done.")
