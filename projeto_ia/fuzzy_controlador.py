import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from util import custo_terreno
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 


dificuldade = ctrl.Antecedent(np.arange(0, 11, 1), 'dificuldade')
distancia = ctrl.Antecedent(np.arange(0, 101, 1), 'distancia')

multiplicador_custo = ctrl.Consequent(np.arange(0.5, 3.1, 0.1), 'multiplicador_custo')
peso_heuristica = ctrl.Consequent(np.arange(0.1, 2.1, 0.1), 'peso_heuristica')


dificuldade['baixa'] = fuzz.trimf(dificuldade.universe, [0, 0, 4])
dificuldade['média'] = fuzz.trimf(dificuldade.universe, [2, 5, 8])
dificuldade['alta'] = fuzz.trimf(dificuldade.universe, [6, 10, 10])


distancia['perto'] = fuzz.trimf(distancia.universe, [0, 0, 30])
distancia['média'] = fuzz.trimf(distancia.universe, [15, 45, 75])
distancia['longe'] = fuzz.trimf(distancia.universe, [50, 100, 100])


multiplicador_custo['baixo'] = fuzz.trimf(multiplicador_custo.universe, [0.5, 0.5, 1.0])
multiplicador_custo['médio'] = fuzz.trimf(multiplicador_custo.universe, [0.9, 1.4, 1.9])
multiplicador_custo['alto'] = fuzz.trapmf(multiplicador_custo.universe, [1.6, 2.5, 3.0, 3.0])


peso_heuristica['baixo'] = fuzz.trimf(peso_heuristica.universe, [0.1, 0.1, 0.6])
peso_heuristica['médio'] = fuzz.trimf(peso_heuristica.universe, [0.4, 0.9, 1.4])
peso_heuristica['alto'] = fuzz.trapmf(peso_heuristica.universe, [1.0, 1.6, 2.0, 2.0])


regras = [
    ctrl.Rule(dificuldade['baixa'] & distancia['perto'], (multiplicador_custo['baixo'], peso_heuristica['médio'])),
    ctrl.Rule(dificuldade['baixa'] & distancia['média'], (multiplicador_custo['baixo'], peso_heuristica['alto'])),
    ctrl.Rule(dificuldade['baixa'] & distancia['longe'], (multiplicador_custo['médio'], peso_heuristica['alto'])),
    ctrl.Rule(dificuldade['média'] & distancia['perto'], (multiplicador_custo['médio'], peso_heuristica['baixo'])),
    ctrl.Rule(dificuldade['média'] & distancia['média'], (multiplicador_custo['médio'], peso_heuristica['médio'])),
    ctrl.Rule(dificuldade['média'] & distancia['longe'], (multiplicador_custo['alto'], peso_heuristica['médio'])),
    ctrl.Rule(dificuldade['alta'] & distancia['perto'], (multiplicador_custo['alto'], peso_heuristica['baixo'])),
    ctrl.Rule(dificuldade['alta'] & distancia['média'], (multiplicador_custo['alto'], peso_heuristica['baixo'])),
    ctrl.Rule(dificuldade['alta'] & distancia['longe'], (multiplicador_custo['alto'], peso_heuristica['baixo']))
]


sistema_fuzzy = ctrl.ControlSystem(regras)
simulador_fuzzy = ctrl.ControlSystemSimulation(sistema_fuzzy)


def avaliar_celula_fuzzy(celula, dist_objetivo):
    base = custo_terreno(celula)
    dificuldade_valor = (min(base, 5.0) - 0.5) / (5.0 - 0.5) * 10.0
    dist_norm = min(dist_objetivo, 100)
    simulador_fuzzy.input['dificuldade'] = dificuldade_valor
    simulador_fuzzy.input['distancia'] = dist_norm
    simulador_fuzzy.compute()
    return simulador_fuzzy.output['multiplicador_custo'], simulador_fuzzy.output['peso_heuristica']


def plot_membership_functions(output_path_prefix="docs/fuzzy"):
    """Salva os gráficos das funções de pertinência em arquivos PNG (sem .view())."""
    outdir = os.path.dirname(output_path_prefix) or "."
    os.makedirs(outdir, exist_ok=True)

    def _plot_var(var, title, path):
        plt.figure(figsize=(10, 6))
        for nome, termo in var.terms.items():
            plt.plot(var.universe, termo.mf, label=nome)
        plt.title(title)
        plt.xlabel(var.label)
        plt.ylabel('grau de pertinência')
        plt.ylim(-0.05, 1.05)
        plt.legend(loc='best')
        plt.grid(True, alpha=0.3)
        plt.savefig(path, bbox_inches='tight')
        plt.close()

    _plot_var(dificuldade, 'MF - dificuldade', f"{output_path_prefix}_mf_dificuldade.png")
    _plot_var(distancia, 'MF - distancia', f"{output_path_prefix}_mf_distancia.png")
    _plot_var(multiplicador_custo, 'MF - multiplicador_custo', f"{output_path_prefix}_mf_mult.png")
    _plot_var(peso_heuristica, 'MF - peso_heuristica', f"{output_path_prefix}_mf_peso.png")


def plot_surface_3d(output_path="docs/fuzzy_surface.png", resolution=41):
    """Gera superfície 3D da saída multiplicador_custo em função de dificuldade x distancia."""
    x = np.linspace(dificuldade.universe.min(), dificuldade.universe.max(), resolution)
    y = np.linspace(distancia.universe.min(), distancia.universe.max(), resolution)
    X, Y = np.meshgrid(x, y)

    Z = np.zeros_like(X)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            simulador_fuzzy.input['dificuldade'] = X[i, j]
            simulador_fuzzy.input['distancia'] = Y[i, j]
            simulador_fuzzy.compute()
            Z[i, j] = simulador_fuzzy.output['multiplicador_custo']

    outdir = os.path.dirname(output_path) or "."
    os.makedirs(outdir, exist_ok=True)
    fig = plt.figure(figsize=(10,7))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='viridis')
    ax.set_xlabel('dificuldade')
    ax.set_ylabel('distancia')
    ax.set_zlabel('multiplicador_custo')
    ax.set_title('Superfície Fuzzy')
    plt.savefig(output_path, bbox_inches='tight')
    plt.close(fig)