import socket
import time

team_number = 8
UDP_PORT = 5000 + team_number
MESSAGE = "DISCOVER"
BROADCAST_IP = "192.168.210.255"

# UDP broadcast socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.settimeout(2.0)  # Timeout 2 saniye beklesin

print(f"[Sender] Sending DISCOVER broadcast on port {UDP_PORT}...")

start_time = time.time()
sock.sendto(MESSAGE.encode(), (BROADCAST_IP, UDP_PORT))

# Cevapları topla
try:
    while True:
        data, addr = sock.recvfrom(1024)
        rtt = round((time.time() - start_time) * 1000, 2)
        print(f"[Sender] Got reply from {addr[0]}: {data.decode()} (RTT: {rtt} ms)")
except socket.timeout:
    print("[Sender] Discovery finished.")

sock.close()
