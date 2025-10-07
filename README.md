# 🚀 Sistema de Busca com Lógica Fuzzy — Inteligência Artificial
```
python -m projeto_ia.main R1 CC --alg all --plot
```
## 👥 Autores
<table>
  <tr>
     <td align="center">
       <br>
       <a href="https://github.com/Otto-Samuel">
         <img src="https://avatars.githubusercontent.com/u/162514493?v=4" style="border-radius: 50%" width="100px;" alt="Otto Samuel"/>
         <br />
         <sub><b>Otto Samuel 💻👑</b></sub>
       </a>
     </td>
    <td align="center">
       <a href="https://github.com/LucasAugustoSS">
         <img src="https://avatars.githubusercontent.com/u/126918429?v=4" style="border-radius: 50%" width="100px;" alt="Lucas augusto"/>
         <br />
         <sub><b>Lucas Augusto 💻</b></sub>
       </a>
     </td>
    <td align="center">
       <a href="https://github.com/FrrTiago">
         <img src="https://avatars.githubusercontent.com/u/132114628?v=4" style="border-radius: 50%" width="100px;" alt="ferreira"/>
         <br />
         <sub><b>Tiago Ferreira 💻</b></sub>
       </a>
     </td>
     <td align="center">
       <a href="https://github.com/JoaoDario632">
         <img src="https://avatars.githubusercontent.com/u/134674876?v=4" style="border-radius: 50%" width="100px;" alt="ferreira"/>
         <br />
         <sub><b>João Dário 💻</b></sub>
       </a>
     </td>
  </tr>
</table>

---

## 🧠 Descrição do Projeto
Este projeto implementa **buscas inteligentes** (A*, Gulosa e A* Fuzzy) aplicadas a um **sistema de delivery**.  
O agente deve encontrar a rota ideal levando em conta **distância**, **dificuldade do terreno** e **ajustes heurísticos fuzzy**, buscando equilibrar desempenho e custo total.

O diferencial é o uso de **lógica fuzzy** para adaptar dinamicamente o comportamento da busca, tornando-a mais próxima da **tomada de decisão humana**.

---

## ⚙️ Metodologia e Métricas

O sistema compara os seguintes algoritmos:
- **A\*** — heurístico admissível, garante caminho ótimo.
- **Busca Gulosa** — não ótima, prioriza nós mais promissores.
- **A\* com controle fuzzy** — ajusta custo e peso heurístico conforme regras fuzzy.

Para cada destino (C1..C5), são registrados:
- Custo total do caminho encontrado  
- Nós explorados  
- Ajustes fuzzy aplicados  
- Tempo de execução

Esses dados permitem avaliar o **trade-off entre custo e eficiência** conforme a intensidade do controle fuzzy.

---

## 📈 Resultados e Visualizações Fuzzy

O controlador fuzzy ajusta o comportamento do algoritmo de acordo com **distância** e **dificuldade**.  
Abaixo estão as funções de pertinência e superfícies de inferência utilizadas no sistema.

### 🔹 Função de Pertinência — Distância
<div align="center">
  <img src="https://github.com/Otto-Samuel/Implementacao_IA/blob/main/projeto_ia/fuzzy_mf_distancia.png" width="600px" alt="Função de pertinência - distância">
</div>

### 🔹 Função de Pertinência — Dificuldade
<div align="center">
  <img src="https://github.com/Otto-Samuel/Implementacao_IA/blob/main/projeto_ia/fuzzy_mf_dificuldade.png" width="600px" alt="Função de pertinência - dificuldade">
</div>

### 🔹 Função de Pertinência — Multiplicador de Custo
<div align="center">
  <img src="https://github.com/Otto-Samuel/Implementacao_IA/blob/main/projeto_ia/fuzzy_mf_mult.png" width="600px" alt="Função de pertinência - multiplicador de custo">
</div>

### 🔹 Função de Pertinência — Peso Heurístico
<div align="center">
  <img src="https://github.com/Otto-Samuel/Implementacao_IA/blob/main/projeto_ia/fuzzy_mf_peso.png" width="600px" alt="Função de pertinência - peso heurístico">
</div>

### 🔹 Superfície Fuzzy — Interação Distância x Dificuldade
<div align="center">
  <img src="https://github.com/Otto-Samuel/Implementacao_IA/blob/main/projeto_ia/fuzzy_surface.png" width="550px" alt="Superfície fuzzy 3D">
</div>

---

## 🗺️ Mapa de Simulação

O agente realiza entregas em um **mapa representativo** contendo caminhos com pesos variáveis.  
<div align="center">
  <img src="https://github.com/Otto-Samuel/Implementacao_IA/blob/main/mapadomundo.png" width="750px" alt="Mapa de simulação">
</div>

---

## 💻 Como Executar

### ✅ Requisitos
- **Python 3.8+**
- **Bibliotecas:** `numpy`, `matplotlib`, `networkx`, `scikit-fuzzy`

Instale todas com:
```bash
pip install -r requirements.txt
```
ou manualmente:
```bash
pip install numpy matplotlib networkx scikit-fuzzy
```

---

### ▶️ Execução via Terminal
1. Acesse a pasta do projeto:
   ```bash
   cd projeto_ia
   ```
2. Execute o programa principal:
   ```bash
   python main.py
   ```
3. O sistema exibirá opções de busca e permitirá observar os resultados fuzzy.

---

### 💡 Execução no VS Code (Passo a Passo)

1. Abra o **VS Code**.  
2. Vá em **File → Open Folder** e selecione a pasta `projeto_ia`.  
3. Abra o arquivo **main.py**.  
4. Configure o interpretador Python (Ctrl + Shift + P → “Python: Select Interpreter”).  
5. Instale as dependências com:
   ```bash
   pip install -r requirements.txt
   ```
6. Execute com **F5** ou clique em ▶️ “Run Python File”.

---

## 🧩 Estrutura do Projeto
```
📁 IMPLEMENTACAO_IA
|
📁 projeto_ia
├──┤
   │
   ├── busca.py                 # Implementação dos algoritmos A*, Gulosa e Fuzzy A*
   ├── fuzzy_controlador.py     # Controlador fuzzy e funções de pertinência
   |
   ├── fuzzy_mf_distancia.png   # Função de pertinência: distância
   ├── fuzzy_mf_dificuldade.png # Função de pertinência: dificuldade
   ├── fuzzy_mf_mult.png        # Função de pertinência: multiplicador de custo
   ├── fuzzy_mf_peso.png        # Função de pertinência: peso heurístico
   ├── fuzzy_surface.png        # Superfície fuzzy 3D
   |
   ├── main.py                  # Script principal de execução
   ├── mapa.py                  # Geração e manipulação de mapas
   ├── util.py                  # Funções auxiliares e métricas
   |
├──┤
│
├── desenhandomapa.py        # Funções para visualização gráfica do mapa e caminho
├── main.py                  # Script principal de execução
├── mapa.txt                 # Estrutura textual do grafo/matriz de mapa
├── mapadomundo.png          # Imagem ilustrativa do mapa de simulação
├── README.md                # Este arquivo
└── requirements.txt         # Dependências do projeto
```


---

## 🧭 Conclusão

A integração entre **buscas heurísticas clássicas** e **lógica fuzzy** demonstra um avanço significativo na adaptação de rotas e decisões.  
O sistema se mostra eficiente e flexível, ajustando o comportamento da busca conforme o contexto — o que o torna ideal para aplicações como **sistemas de delivery inteligentes**, **robótica móvel** e **planejamento de rotas**.
