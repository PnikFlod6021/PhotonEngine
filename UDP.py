import socket

HOST = "127.0.0.1"   # IP address
TX_PORT = 7500       #  transmit on 7501

# Create UDP TX socket
tx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

RX_PORT = 7501
BUF_SIZE = 1024

# Create and bind the Receiver socket
rx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rx_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
rx_sock.bind(("0.0.0.0", RX_PORT))
### The code will stop here until something is sent to RX_PORT
print("listening")
data, addr = rx_sock.recvfrom(BUF_SIZE)  # blocks until something arrives
text = data.decode("utf-8").strip()
print(f"Received from {addr}: {text}") ### Prints the Received Data

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
