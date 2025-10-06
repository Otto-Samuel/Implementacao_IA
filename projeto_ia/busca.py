import heapq
from .util import custo_terreno, heuristica_manhattan, custo_efetivo
from .fuzzy_controlador import avaliar_celula_fuzzy

def vizinhos(pos, mapa, objetivo=None):
    linhas, colunas = mapa.shape
    x, y = pos
    direcoes = [(0,1),(1,0),(0,-1),(-1,0)]
    candidatos = []
    for dx, dy in direcoes:
        nx, ny = x+dx, y+dy
        if 0 <= nx < linhas and 0 <= ny < colunas:
            # Restrito a caminhar apenas em quadrados brancos; objetivo é exceção
            if mapa[nx, ny] == '⬜' or (objetivo is not None and (nx, ny) == objetivo):
                candidatos.append((nx, ny))
    return candidatos

def busca_a_estrela(inicio, objetivo, mapa, usar_fuzzy=True):
    def f_score(g, h, peso_h): return g + peso_h * h
    abertos = [(0, inicio)]
    veio_de = {}
    gscore = {inicio: 0}
    explorados = set()
    while abertos:
        _, atual = heapq.heappop(abertos)
        if atual == objetivo:
            caminho = []
            while atual in veio_de:
                caminho.append(atual)
                atual = veio_de[atual]
            caminho.append(inicio)
            return list(reversed(caminho)), explorados, gscore
        explorados.add(atual)
        for nb in vizinhos(atual, mapa, objetivo):
            custo_base = custo_efetivo(nb, mapa)
            dist = heuristica_manhattan(nb, objetivo)
            mult, peso_h = (1.0, 1.0)
            if usar_fuzzy:
                mult, peso_h = avaliar_celula_fuzzy(mapa[nb], dist, pos=nb, mapa=mapa)
            novo_g = gscore[atual] + custo_base * mult
            if nb not in gscore or novo_g < gscore[nb]:
                veio_de[nb] = atual
                gscore[nb] = novo_g
                fval = f_score(novo_g, heuristica_manhattan(nb, objetivo), peso_h)
                heapq.heappush(abertos, (fval, nb))
    return None, explorados, gscore

def busca_gulosa(inicio, objetivo, mapa):
    # Heurística principal ainda é a distância; adiciona-se uma leve penalização pelo custo efetivo
    def prioridade(pos):
        h = heuristica_manhattan(pos, objetivo)
        c = custo_efetivo(pos, mapa)
        return h + 0.6 * c  # aumenta a influência do custo efetivo

    abertos = [(prioridade(inicio), custo_efetivo(inicio, mapa), inicio)]
    veio_de = {}
    explorados = set()
    visitados = set([inicio])
    while abertos:
        _, _, atual = heapq.heappop(abertos)
        if atual == objetivo:
            caminho = []
            while atual in veio_de:
                caminho.append(atual)
                atual = veio_de[atual]
            caminho.append(inicio)
            return list(reversed(caminho)), explorados
        explorados.add(atual)
        for nb in vizinhos(atual, mapa, objetivo):
            if nb in visitados: continue
            visitados.add(nb)
            # Usa tupla (prioridade, custo, pos) para desempate a favor de menor custo
            heapq.heappush(abertos, (prioridade(nb), custo_efetivo(nb, mapa), nb))
            veio_de[nb] = atual
    return None, explorados