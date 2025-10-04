 
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


G = nx.Graph()

nodes = ["Restaurante", "A", "B", "C", "D", "E", "Cliente1", "Cliente2", "Cliente3", "Cliente4"]
G.add_nodes_from(nodes)

edges = [
    ("Restaurante", "A", 4),
    ("Restaurante", "B", 2),
    ("A", "C", 5),
    ("B", "C", 8),
    ("A", "Cliente1", 7),
    ("C", "Cliente1", 2),
    ("C", "Cliente2", 3),
    ("B", "D", 4),
    ("D", "E", 6),
    ("E", "Cliente3", 2),
    ("C", "Cliente4", 5),
]
G.add_weighted_edges_from(edges)


def heuristic(u, v):
    return abs(len(u) - len(v))

def melhor_rota(origem, destino):
    caminho = nx.astar_path(G, origem, destino, heuristic=heuristic, weight="weight")
    custo = nx.path_weight(G, caminho, weight="weight")
    return caminho, custo

rota, custo = melhor_rota("Restaurante", "Cliente3")
print("=== Roteamento (A*) ===")
print("Melhor rota:", " -> ".join(rota))
print("Custo total:", custo, "km")


urgencia = ctrl.Antecedent(np.arange(0, 11, 1), "urgencia")
vip = ctrl.Antecedent(np.arange(0, 2, 1), "vip")
prioridade = ctrl.Consequent(np.arange(0, 11, 1), "prioridade")

urgencia["baixa"] = fuzz.trimf(urgencia.universe, [0, 0, 5])
urgencia["media"] = fuzz.trimf(urgencia.universe, [0, 5, 10])
urgencia["alta"] = fuzz.trimf(urgencia.universe, [5, 10, 10])

vip["nao"] = fuzz.trimf(vip.universe, [0, 0, 1])
vip["sim"] = fuzz.trimf(vip.universe, [0, 1, 1])

prioridade["baixa"] = fuzz.trimf(prioridade.universe, [0, 0, 5])
prioridade["media"] = fuzz.trimf(prioridade.universe, [0, 5, 10])
prioridade["alta"] = fuzz.trimf(prioridade.universe, [5, 10, 10])

regra1 = ctrl.Rule(urgencia["baixa"] & vip["nao"], prioridade["baixa"])
regra2 = ctrl.Rule(urgencia["media"] & vip["nao"], prioridade["media"])
regra3 = ctrl.Rule(urgencia["alta"] & vip["nao"], prioridade["alta"])
regra4 = ctrl.Rule(urgencia["baixa"] & vip["sim"], prioridade["media"])
regra5 = ctrl.Rule(urgencia["media"] & vip["sim"], prioridade["alta"])
regra6 = ctrl.Rule(urgencia["alta"] & vip["sim"], prioridade["alta"])

prioridade_ctrl = ctrl.ControlSystem([regra1, regra2, regra3, regra4, regra5, regra6])
prioridade_sim = ctrl.ControlSystemSimulation(prioridade_ctrl)


prioridade_sim.input["urgencia"] = 9   
prioridade_sim.input["vip"] = 1      
prioridade_sim.compute()

print("\n=== Sistema Fuzzy ===")
print("Prioridade da entrega:", round(prioridade_sim.output["prioridade"], 2))

motoboys = {
    "João": {"disponivel": 1, "confiabilidade": 0.9},
    "Ana": {"disponivel": 0, "confiabilidade": 0.8},
    "Carlos": {"disponivel": 1, "confiabilidade": 0.6},
}

print("\n=== Escolha do Motoboy ===")
print("Motoboys disponíveis:")
for nome, dados in motoboys.items():
    print(f" - {nome}: disponível={dados['disponivel']}, confiabilidade={dados['confiabilidade']}")

escolha_manual = input("Digite o nome do motoboy (ou ENTER para escolha automática): ")

if escolha_manual and escolha_manual in motoboys:
    motoboy_escolhido = escolha_manual
else:
    disponiveis = {m: d for m, d in motoboys.items() if d["disponivel"] == 1}
    motoboy_escolhido = max(disponiveis, key=lambda x: disponiveis[x]["confiabilidade"])

print(f"Motoboy escolhido: {motoboy_escolhido}")

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue", edge_color="gray")

edge_colors = []
for u, v in G.edges():
    if (u, v) in zip(rota, rota[1:]) or (v, u) in zip(rota, rota[1:]):
        edge_colors.append("blue")
    else:
        edge_colors.append("gray")

nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color=edge_colors, width=2)
labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.show() 
