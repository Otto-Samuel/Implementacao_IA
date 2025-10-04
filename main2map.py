import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.image as mpimg

# === 1. Carregar o mapa como fundo ===
mapa = mpimg.imread("mapa.png")

# === 2. Criar grafo ===
G = nx.DiGraph() 

# === 3. Definir nós (coordenadas x, y) ===

pos = {
    "N1": (100, 500),
    "N2": (300, 500),
    "N3": (500, 500),
    "N4": (700, 500),
    "N5": (300, 300),
    "N6": (500, 300),
    "N7": (700, 300),
    "N8": (500, 100)
}


edges = [
    ("N1", "N2"), ("N2", "N3"), ("N3", "N4"),
    ("N2", "N5"), ("N3", "N6"),
    ("N5", "N6"), ("N6", "N7"),
    ("N6", "N8")
]


for u, v in edges:
    x1, y1 = pos[u]
    x2, y2 = pos[v]
    dist = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    G.add_edge(u, v, weight=dist)
    G.add_edge(v, u, weight=dist) 

restaurante = "N1"
casa = "N7"


caminho = nx.dijkstra_path(G, source=restaurante, target=casa, weight="weight")
print("Caminho mais curto:", caminho)


fig, ax = plt.subplots(figsize=(10,6))
ax.imshow(mapa, extent=[0, 1000, 0, 600])  # ajusta fundo

# desenha grafo
nx.draw(G, pos, ax=ax, node_size=200, node_color="black", edge_color="white", with_labels=True, font_color="white")

# desenha caminho em vermelho
path_edges = list(zip(caminho, caminho[1:]))
nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="red", width=3, ax=ax)

plt.show()
