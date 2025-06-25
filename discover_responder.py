import socket

team_number = 8
UDP_PORT = 5000 + team_number

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", UDP_PORT))

print(f"[Responder] Listening for DISCOVER messages on port {UDP_PORT}...")

while True:
    data, addr = sock.recvfrom(1024)
    msg = data.decode()
    print(f"[Responder] Received '{msg}' from {addr[0]}")
    if msg == "DISCOVER":
        response = f"HELLO from {socket.gethostname()}"
        sock.sendto(response.encode(), addr)
