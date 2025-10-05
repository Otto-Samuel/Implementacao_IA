import math
import numpy as np
from .mapa import mapa

CUSTOS_TERRENO = {
    "🟩": 1.0, "🌲": 2.0, "🟧": 2.5, "🟫": 4.0, "🌋": 5.0,
    "⬜": 0.9, "🟨": 0.5, "🌊": math.inf, "🟦": math.inf, "🏝️ ": math.inf,
    "🏔️ ": 4.0, "🌵": 2.5, "🍟": 1.5, "🏠": 1.0, "🛥️ ": 1.0
}

def custo_terreno(celula: str) -> float:
    return CUSTOS_TERRENO.get(celula, 3.0)

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
