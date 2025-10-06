from .mapa import mapa, posicoes
from .busca import busca_a_estrela, busca_gulosa
from .util import imprimir_mapa
from .fuzzy_controlador import plot_membership_functions, plot_surface_3d
import argparse
import os

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
    parser = argparse.ArgumentParser(description="Comparar algoritmos de busca no mapa")
    parser.add_argument("inicio", nargs='?', default='R1', help="Rótulo de início (ex.: R1)")
    parser.add_argument("objetivo", nargs='?', default='C2', help="Rótulo de objetivo (ex.: C1..C5)")
    parser.add_argument("--alg", choices=["astar","astar_fuzzy","gulosa","all"], default="all", help="Algoritmo a executar")
    parser.add_argument("--plot", action="store_true", help="Gerar gráficos das funções de pertinência e superfície 3D")
    parser.add_argument("--outdir", default=None, help="Diretório de saída para gráficos (padrão: pasta deste arquivo)")
    args = parser.parse_args()

    inicio_label = args.inicio
    objetivo_label = args.objetivo

    inicio = posicoes.get(inicio_label)
    objetivo = posicoes.get(objetivo_label)
    if inicio is None or objetivo is None:
        print(f"Posições inválidas: inicio={inicio_label}, objetivo={objetivo_label}. Disponíveis: {list(posicoes.keys())}")
    else:
        if args.alg == "all":
            comparar_buscas(inicio_label, objetivo_label)
        else:
            if args.alg == "astar":
                print("=== BUSCA A* SEM FUZZY ===")
                caminho, explorados, g = busca_a_estrela(inicio, objetivo, mapa, usar_fuzzy=False)
                custo = g.get(objetivo, float('inf'))
                print(f"Custo total: {custo:.2f}, Nós explorados: {len(explorados)}")
                imprimir_mapa(caminho, explorados, posicoes)
            elif args.alg == "astar_fuzzy":
                print("=== BUSCA A* COM FUZZY ===")
                caminho, explorados, g = busca_a_estrela(inicio, objetivo, mapa, usar_fuzzy=True)
                custo = g.get(objetivo, float('inf'))
                print(f"Custo total: {custo:.2f}, Nós explorados: {len(explorados)}")
                imprimir_mapa(caminho, explorados, posicoes)
            elif args.alg == "gulosa":
                print("=== BUSCA GULOSA ===")
                caminho, explorados = busca_gulosa(inicio, objetivo, mapa)
                print(f"Nós explorados: {len(explorados)}")
                imprimir_mapa(caminho, explorados, posicoes)

    if args.plot:
        base_outdir = args.outdir or os.path.dirname(__file__)
        os.makedirs(base_outdir, exist_ok=True)
        prefix = os.path.join(base_outdir, "fuzzy")
        plot_membership_functions(prefix)
        surface_path = os.path.join(base_outdir, "fuzzy_surface.png")
        plot_surface_3d(surface_path)