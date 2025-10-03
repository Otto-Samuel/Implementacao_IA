# %%
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

#%%
# ==========================
# 1. Grafo da cidade
# ==========================
G = nx.Graph()

# Adicionando nós (restaurante + clientes + ruas)
nodes = ["Restaurante", "A", "B", "C", "Cliente1", "Cliente2"]
G.add_nodes_from(nodes)

# Adicionando arestas com custos (distâncias em km)
edges = [
    ("Restaurante", "A", 4),
    ("Restaurante", "B", 2),
    ("A", "C", 5),
    ("B", "C", 8),
    ("A", "Cliente1", 7),
    ("C", "Cliente1", 2),
    ("C", "Cliente2", 3),
]
G.add_weighted_edges_from(edges)

# %%
def heuristic(u, v):
    # heurística simples: distância em linha reta (aqui só estimamos com grau dos nós)
    return abs(len(u) - len(v))

def melhor_rota(origem, destino):
    caminho = nx.astar_path(G, origem, destino, heuristic=heuristic, weight="weight")
    custo = nx.path_weight(G, caminho, weight="weight")
    return caminho, custo

rota, custo = melhor_rota("Restaurante", "Cliente2")
print("=== Roteamento (A*) ===")
print("Melhor rota:", " -> ".join(rota))
print("Custo total:", custo, "km")

#%%
urgencia = ctrl.Antecedent(np.arange(0, 11, 1), "urgencia")
vip = ctrl.Antecedent(np.arange(0, 2, 1), "vip")
prioridade = ctrl.Consequent(np.arange(0, 11, 1), "prioridade")

# Conjuntos fuzzy
urgencia["baixa"] = fuzz.trimf(urgencia.universe, [0, 0, 5])
urgencia["media"] = fuzz.trimf(urgencia.universe, [0, 5, 10])
urgencia["alta"] = fuzz.trimf(urgencia.universe, [5, 10, 10])

vip["nao"] = fuzz.trimf(vip.universe, [0, 0, 1])
vip["sim"] = fuzz.trimf(vip.universe, [0, 1, 1])

prioridade["baixa"] = fuzz.trimf(prioridade.universe, [0, 0, 5])
prioridade["media"] = fuzz.trimf(prioridade.universe, [0, 5, 10])
prioridade["alta"] = fuzz.trimf(prioridade.universe, [5, 10, 10])

# Regras
regra1 = ctrl.Rule(urgencia["baixa"] & vip["nao"], prioridade["baixa"])
regra2 = ctrl.Rule(urgencia["media"] & vip["nao"], prioridade["media"])
regra3 = ctrl.Rule(urgencia["alta"] & vip["nao"], prioridade["alta"])
regra4 = ctrl.Rule(urgencia["baixa"] & vip["sim"], prioridade["media"])
regra5 = ctrl.Rule(urgencia["media"] & vip["sim"], prioridade["alta"])
regra6 = ctrl.Rule(urgencia["alta"] & vip["sim"], prioridade["alta"])

# Sistema de controle fuzzy
prioridade_ctrl = ctrl.ControlSystem([regra1, regra2, regra3, regra4, regra5, regra6])
prioridade_sim = ctrl.ControlSystemSimulation(prioridade_ctrl)

# Exemplo de entrada
prioridade_sim.input["urgencia"] = 8   # urgência alta
prioridade_sim.input["vip"] = 1       # cliente VIP
prioridade_sim.compute()

print("\n=== Sistema Fuzzy ===")
print("Prioridade da entrega:", round(prioridade_sim.output["prioridade"], 2))

# %%
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue")
labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.show()
# %%
