
import numpy as np
import heapq
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import pygame
import itertools

mapa = np.array([
    ["🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","⬜","🟨","🌊","🟦","🟦","🟦"],
    ["🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","C2","⬜","🟨","🌊","🟦","🛥️ ","🟦"],
    ["🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","C1","🟩","⬜","⬜","⬜","⬜","⬜","⬜","⬜","⬜","⬜","⬜","⬜","⬜","🟨","🌊","🟦","🟦","🟦"],
    ["🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","⬜","⬜","⬜","⬜","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","⬜","🟨","🌊","🟦","🟦","🟦"],
    ["🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","⬜","🟩","🟩","🟩","⬜","C3","🟩","🟩","🟩","🟩","🟩","⬜","⬜","🟨","🌊","🏝️ ","🟦"],
    ["🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","⬜","⬜","⬜","⬜","⬜","🟩","🟩","🟩","🟩","🟩","🟩","🟩","⬜","🟨","🌊","🟦","🟦"],
    ["🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","⬜","⬜","⬜","⬜","🟩","⬜","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","⬜","🟨","🌊","🟦","🟦"],
    ["🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","⬜","🟩","⬜","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","⬜","🟩","🟨","🌊","🌊"],
    ["🟧","🟧","🟧","🟧","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","⬜","🟩","⬜","🟩","🟩","🟩","🟫","🟫","🟫","🟩","🟩","🟩","⬜","🟩","🟩","🟨","🟨"],
    ["🟧","🟧","🟧","🟧","🟧","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","⬜","🟩","⬜","🟩","🟩","🟩","🟫","🌋","🟫","🟩","🟩","🟩","⬜","🟩","🟩","🟩","🟩"],
    ["🟧","🟧","🟧","🟧","🟧","🟧","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","⬜","🟩","⬜","🟩","🟩","🟩","🟫","🟫","🟫","🟩","🟩","🟩","⬜","🟩","🟩","🟩","🟩"],
    ["🟧","🌵","🟧","🟧","🟧","🟧","🟧","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","⬜","⬜","⬜","⬜","⬜","⬜","⬜","⬜","⬜","⬜","⬜","⬜","⬜","R1","🟩","🟩","🟩"],
    ["🟧","🟧","🟧","🟧","🟧","🟧","🟧","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","⬜","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","⬜","🟩","⬜","🟩","🟩","🟩","🟩"],
    ["🟧","🟧","🟧","🟧","🟧","🟧","🟧","🟩","🟩","🟩","🟩","🟩","🟩","🟩","C5","🏔️ ","🟩","🟩","🟩","🟩","🟩","🟩","🟩","⬜","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","C4","⬜","🟩","⬜","🟩","🟩","🟩","🟩"],
    ["🟧","🟧","🟧","🟧","🟧","🟧","🟧","🟩","🟩","🟩","⬜","⬜","⬜","⬜","⬜","⬜","⬜","⬜","⬜","⬜","⬜","⬜","⬜","⬜","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","⬜","⬜","⬜","🌴","🌴","🌴","🌴"],
    ["🟧","🟧","🌵","🟧","🟧","🟧","🟧","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","⬜","🌴","🌴","🌴","🌴","🌴"],
    ["🟧","🟧","🟧","🟧","🟧","🟧","🟧","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🟩","⬜","🌴","🌴","🌴","🌴","🌴"],
])

positions = {'R1': (11, 36), 'C2': (1, 33)} # aqui sao as posicoes no mapa, depois vcs colocam mais
rows, cols = mapa.shape

# Busca A*
def a_star(start, goal, mapa):
    def manhattan(p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
    def get_vizinhos(pos):
        x, y = pos
        vizinhos = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and (mapa[nx, ny] == '⬜' or mapa[nx, ny] in positions):
                vizinhos.append((nx, ny))
        return vizinhos
    
    def reconstruir_caminho(came_from, current):
        caminho = [current]
        while current in came_from:
            current = came_from[current]
            caminho.append(current)
        return caminho[::-1]
    
    open_set = [(0, start)]  
    came_from = {}
    g_score = {start: 0}
    f_score = {start: manhattan(start, goal)}
    explored = set()
    
    while open_set:
        current_f, current = heapq.heappop(open_set)
        if current == goal:
            return reconstruir_caminho(came_from, current), explored, g_score
        
        explored.add(current)
        for vizinho in get_vizinhos(current):
            tentative_g = g_score[current] + 1 
            if vizinho not in g_score or tentative_g < g_score[vizinho]:
                came_from[vizinho] = current
                g_score[vizinho] = tentative_g
                f_score[vizinho] = tentative_g + manhattan(vizinho, goal)
                heapq.heappush(open_set, (f_score[vizinho], vizinho))
    return None, explored, g_score

def print_map(mapa, caminho=None, explored=None):
    mapa_display = mapa.copy()
    if explored:
        for x, y in explored:
            if mapa_display[x, y] not in positions and (caminho is None or (x, y) not in caminho):
                mapa_display[x, y] = '⬛'  
    if caminho:
        for x, y in caminho:
            if mapa_display[x, y] not in positions:  
                mapa_display[x, y] = '🟪' 
    
    for i in range(rows):
        print(''.join(mapa_display[i]))

caminho, explored, g_score = a_star(positions['R1'], positions['C2'], mapa)
if caminho:
    print(f"\nCaminho de R1 para C2: {caminho}")
    print(f"Custo total: {g_score[positions['C2']]:.2f}")
    print(f"Nós explorados: {len(explored)}")
    print("\nMapa com caminho (🟪) e nós explorados (⬛):")
    print_map(mapa, caminho, explored)
else:
    print("Nenhum caminho encontrado!")