import socket
import json
import time

# Ağ ayarları
UDP_PORT = 5008
NODE_ID = "A"  # Her Pi’de farklı olmalı (ör: "A", "B", "C", ...)
DESTINATION = "B"  # Hedef node (Task 1 için önemli değil)
BROADCAST_IP = "192.168.210.255"

seen_msgs = set()

# Yalnızca A node'u FLOOD mesajı gönderir
def send_flood():
    timestamp = time.time()
    msg = {
        "type": "FLOOD",
        "src": NODE_ID,
        "dst": DESTINATION,
        "payload": f"Hello from {NODE_ID}",
        "id": f"{NODE_ID}-{int(timestamp)}",
        "timestamp": timestamp
    }

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(json.dumps(msg).encode(), (BROADCAST_IP, UDP_PORT))
    print(f"[{NODE_ID}] Sent FLOOD at {timestamp:.5f}")

# FLOOD mesajı geldiğinde çalışır
def handle_flood(msg):
    msg_id = msg["id"]
    if msg_id in seen_msgs:
        return

    seen_msgs.add(msg_id)

    now = time.time()
    rtt = round((now - msg["timestamp"]) * 1000, 2)
    print(f"[{NODE_ID}] Received FLOOD from {msg['src']} – RTT: {rtt} ms")

    if NODE_ID == msg["dst"]:
        print(f"[{NODE_ID}] I am the destination. Not forwarding.")
        return

    msg["path"] = msg.get("path", []) + [NODE_ID]

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(json.dumps(msg).encode(), (BROADCAST_IP, UDP_PORT))
    print(f"[{NODE_ID}] Forwarded FLOOD")

# UDP mesajlarını dinler
def listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", UDP_PORT))
    print(f"[{NODE_ID}] Listening on port {UDP_PORT}...")

    while True:
        data, addr = sock.recvfrom(4096)
        try:
            msg = json.loads(data.decode())
        except json.JSONDecodeError:
            continue

        if msg.get("type") == "FLOOD":
            handle_flood(msg)

# Ana fonksiyon
if __name__ == "__main__":
    if NODE_ID == "A":
        time.sleep(2)
        send_flood()

    listen()
