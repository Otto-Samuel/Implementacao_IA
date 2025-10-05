from mapa import mapa, posicoes
from busca import busca_a_estrela, busca_gulosa
from util import imprimir_mapa

def comparar_buscas(inicio_label='R1', objetivo_label='C2'):
    inicio = posicoes[inicio_label]
    objetivo = posicoes[objetivo_label]

    print("=== BUSCA A* SEM FUZZY ===")
    caminho_a, explorados_a, g_a = busca_a_estrela(inicio, objetivo, mapa, usar_fuzzy=False)
    custo_a = g_a.get(objetivo, float('inf'))
    print(f"Custo total: {custo_a:.2f}, Nós explorados: {len(explorados_a)}")
    imprimir_mapa(caminho_a, explorados_a, posicoes)
    print("\n")

    print("=== BUSCA A* COM FUZZY ===")
    caminho_f, explorados_f, g_f = busca_a_estrela(inicio, objetivo, mapa, usar_fuzzy=True)
    custo_f = g_f.get(objetivo, float('inf'))
    print(f"Custo total: {custo_f:.2f}, Nós explorados: {len(explorados_f)}")
    imprimir_mapa(caminho_f, explorados_f, posicoes)
    print("\n")

    print("=== BUSCA GULOSA ===")
    caminho_g, explorados_g = busca_gulosa(inicio, objetivo, mapa)
    print(f"Nós explorados: {len(explorados_g)}")
    imprimir_mapa(caminho_g, explorados_g, posicoes)
    print("\n")

if __name__ == "__main__":
    comparar_buscas('R1', 'C7')


