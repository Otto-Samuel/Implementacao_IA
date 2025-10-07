import math
import numpy as np
from .mapa import mapa

# Mapeamento de símbolos do mapa para custo base de entrada na célula.
# Valores maiores representam maior dificuldade/risco; infinito = intransponível.
CUSTOS_TERRENO = {
    "🟩": 1.0, "🌲": 2.0, "🟧": 2.5, "🟫": 4.0, "🌋": 5.0,
    "⬜": 0.9, "🟨": 0.5, "🌊": math.inf, "🟦": math.inf, "🏝️ ": math.inf,
    "🏔️ ": 4.0, "🌵": 2.5, "🍟": 1.5, "🏠": 1.0, "🛥️ ": 1.0, 
}

def custo_terreno(celula: str) -> float:
    """Retorna o custo base associado ao símbolo da célula.

    Caso o símbolo não esteja mapeado, assume custo intermediário (3.0)
    para manter o algoritmo robusto a novos ícones.
    """
    return CUSTOS_TERRENO.get(celula, 3.0)

# Penalidades de influência por terrenos adjacentes
# Penalidades adicionais aplicadas ao custo do quadrado branco (⬜)
# quando há vizinhos 8-conexos com esses símbolos. Representa o efeito
# de terrenos difíceis ao redor (areia, árvores, vulcão etc.) no trajeto.
INFLUENCIA_ADJACENTE = {
    "🟨": 0.3,   #? areia influencia equilíbrio
    "🌲": 0.2,   #? árvores, galhos atrapalham
    "🟫": 0.5,   #? rocha vulcânica irregular
    "🌋": 1.0,   #? vulcão muito arriscado
    "🏔️ ": 0.5, #? montanhoso próximo dificulta
    "🌵": 0.4,   #? cactos, terreno árido
    "🚥":0.3,    #? semaforos,
    "🚦":0.3,
    "🥚":0.2,
    "🧓":0.1,
    "🚔":0.8     # blitz 
}

def custo_efetivo(pos, mapa) -> float:
    """Custo efetivo da célula, somando custo base e influência de vizinhos.

    - Mantém infinito para células intransponíveis
    - Considera vizinhança 8-conexa (inclui diagonais)
    - Aplica amortecimento para evitar penalidades excessivas
    """
    x, y = pos
    linhas, colunas = mapa.shape
    base = custo_terreno(mapa[x, y])

    # Se a própria célula é intransponível, preserve infinito
    if base == math.inf:
        return base

    penalidade = 0.0
    # Percorre os 8 vizinhos (incluindo diagonais)
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0: # ignora a celula
                continue
            nx, ny = x + dx, y + dy
            # Verifica se o vizinho está dentro dos limites do mapa
            if 0 <= nx < linhas and 0 <= ny < colunas:
                cel = mapa[nx, ny]
                penalidade += INFLUENCIA_ADJACENTE.get(cel, 0.0)

    # Reduz metade da penalidade total para suavizar o efeito
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