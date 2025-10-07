import math
import numpy as np
from .mapa import mapa

CUSTOS_TERRENO = {
    "🟩": 1.0, "🌲": 2.0, "🟧": 2.5, "🟫": 4.0, "🌋": 5.0,
    "⬜": 0.9, "🟨": 0.5, "🌊": math.inf, "🟦": math.inf, "🏝️ ": math.inf,
    "🏔️ ": 4.0, "🌵": 2.5, "🍟": 1.5, "🏠": 1.0, "🛥️ ": 1.0, 
}

def custo_terreno(celula: str) -> float:
    return CUSTOS_TERRENO.get(celula, 3.0)

INFLUENCIA_ADJACENTE = {
    "🟨": 0.3,
    "🌲": 0.2,
    "🟫": 0.5,
    "🌋": 1.0,
    "🏔️ ": 0.5,
    "🌵": 0.4,
    "🚥":0.3,
    "🚦":0.3,
    "🥚":0.2,
    "🧓":0.1,
}

def custo_efetivo(pos, mapa) -> float:
    """Retorna o custo da célula considerando influência dos vizinhos.

    A influência considera vizinhança 8-conexa (inclui diagonais) e soma
    pequenas penalidades por cada terreno "difícil" ao redor.
    """
    x, y = pos
    linhas, colunas = mapa.shape
    base = custo_terreno(mapa[x, y])

    # Se a própria célula é intransponível, preserve infinito
    if base == math.inf:
        return base

    penalidade = 0.0
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < linhas and 0 <= ny < colunas:
                cel = mapa[nx, ny]
                penalidade += INFLUENCIA_ADJACENTE.get(cel, 0.0)

    # Opcional: amortecer penalidade para não explodir
    penalidade *= 0.5

    return base + penalidade

def heuristica_manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def imprimir_mapa(caminho=None, explorados=None, posicoes=None):
    linhas, colunas = mapa.shape
    mapa_exibicao = mapa.copy()
    if explorados:
        for x, y in explorados:
            if posicoes and (x, y) not in posicoes.values():
                mapa_exibicao[x, y] = '⬛'
    if caminho:
        for x, y in caminho:
            if posicoes and (x, y) not in posicoes.values():
                mapa_exibicao[x, y] = '🟪'
    for linha in mapa_exibicao:
        print(''.join(linha))