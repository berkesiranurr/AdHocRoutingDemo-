import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

# RTT ölçüm sonuçlarına göre bağlantılar (A = mcladhoc-01)
G.add_edge("mcladhoc-01", "mcladhoc-02", weight=41.63)
G.add_edge("mcladhoc-01", "mcladhoc-03", weight=41.58)
G.add_edge("mcladhoc-01", "mcladhoc-04", weight=41.35)

# Grafik çizimi
pos = nx.spring_layout(G, seed=42)  # sabit pozisyon için seed
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1500, font_size=10)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f"{d:.2f} ms" for (u, v), d in edge_labels.items()})
plt.title("Flooding-based Network Topology – Task 1")
plt.tight_layout()
plt.show()
