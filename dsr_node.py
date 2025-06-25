import socket
import json
import time

# Ad-hoc iletişim portu
UDP_PORT = 5008

# Her Raspberry Pi’de NODE_ID sabitini kendine göre ayarla: "A", "B", "C", ...
NODE_ID = "A"
DESTINATION = "B"  # Yalnızca kaynak düğüm için gerekli

# Broadcast adresi
BROADCAST_IP = "192.168.210.255"

# Node ID → IP eşlemesi (manuel tanımlı)
ip_map = {
    "A": "192.168.210.60",
    "B": "192.168.210.61",
    "C": "192.168.210.62",
    "D": "192.168.210.63",
}

# RREQ mesajı başlat: sadece kaynak düğüm çağırmalı
def send_rreq():
    msg = {
        "type": "RREQ",
        "src": NODE_ID,
        "dst": DESTINATION,
        "path": [NODE_ID],
        "timestamp": time.time()  # Gönderim zamanı (saniye cinsinden)
    }
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(json.dumps(msg).encode(), (BROADCAST_IP, UDP_PORT))
    print(f"[{NODE_ID}] Sent RREQ")

# Hedef node RREP üretip geri yollar
def send_rrep(path, timestamp):
    reversed_path = list(reversed(path))
    rrep_msg = {
        "type": "RREP",
        "path": reversed_path,
        "timestamp": timestamp  # RREQ'in gönderim zamanını taşı
    }
    next_hop = reversed_path[1]
    send_to_node(rrep_msg, next_hop)
    print(f"[{NODE_ID}] Sent RREP to {next_hop}: {reversed_path}")

# RREP mesajını işleyip bir sonraki node'a gönder
def handle_rrep(msg):
    path = msg["path"]
    idx = path.index(NODE_ID)

    if idx == len(path) - 1:
        # Son node: kaynak düğüm, süreyi yazdır
        duration = round((time.time() - msg["timestamp"]) * 1000, 2)
        print(f"[{NODE_ID}] Received final RREP: {path}")
        print(f"[{NODE_ID}] Route discovery duration: {duration} ms")
        return

    next_hop = path[idx + 1]
    send_to_node(msg, next_hop)
    print(f"[{NODE_ID}] Forwarded RREP to {next_hop}")

# Belirtilen node’a doğrudan UDP mesajı gönder
def send_to_node(msg, node_id):
    target_ip = ip_map[node_id]
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(json.dumps(msg).encode(), (target_ip, UDP_PORT))

# UDP mesajlarını dinle ve işleme al
def listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", UDP_PORT))
    print(f"[{NODE_ID}] Listening on port {UDP_PORT}")

    while True:
        data, addr = sock.recvfrom(4096)
        msg = json.loads(data.decode())

        if msg["type"] == "RREQ":
            handle_rreq(msg)
        elif msg["type"] == "RREP":
            handle_rrep(msg)

# Gelen RREQ mesajını işle
def handle_rreq(msg):
    if NODE_ID in msg["path"]:
        return  # Döngü önle

    msg["path"].append(NODE_ID)

    if msg["dst"] == NODE_ID:
        print(f"[{NODE_ID}] I am the destination. Full path: {msg['path']}")
        send_rrep(msg["path"], msg["timestamp"])
    else:
        print(f"[{NODE_ID}] Forwarding RREQ: {msg['path']}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(json.dumps(msg).encode(), (BROADCAST_IP, UDP_PORT))

# Program başlangıcı
if NODE_ID == "A":
    send_rreq()

listen()
