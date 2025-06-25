# AdHocRoutingDemo

This repository contains three main components from the Mobile Computing Lab at Universität Stuttgart:

## Task 0 – Network Discovery
- `discover_sender.py`: Sends a DISCOVER message to discover other nodes
- `discover_responder.py`: Listens and responds to discovery messages

## Task 1 – Flooding Protocol
- `flood_node.py`: Implements basic flooding and logs RTT for each node
- `graph.py`: Draws network topology using measured RTTs

## Task 2 – Dynamic Source Routing (DSR)
- `dsr_node.py`: Implements RREQ/RREP based dynamic source routing, logs route discovery time

## Nodes
- `mcladhoc-01` → A  
- `mcladhoc-02` → B  
- `mcladhoc-03` → C  
- `mcladhoc-04` → D  

Each script must be executed on the correct node with appropriate NODE_ID configuration.

---

**Author:** Berke Şiranur  
**Course:** Mobile Computing Lab (2025)
