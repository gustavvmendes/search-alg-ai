from graph import Grafo
import csv
from search.bfs import busca_largura
from search.dfs import busca_profundidade
from search.uniform_cost import busca_custo_uniforme
from search.greedy import busca_gulosa
from search.a_star import busca_a_estrela

def carregar_distancias(arquivo):
    grafo = Grafo()
    with open(arquivo, newline='', encoding='utf-8') as f:
        leitor = csv.reader(f)
        next(leitor)
        for o, d, dist in leitor:
            grafo.adicionar_aresta(o, d, float(dist))
    return grafo

def carregar_heuristica(destino, arquivo, grafo):
    # heurística admissível: distância aérea até o destino (ou inf se faltar)
    heur = {v: float('inf') for v in grafo.vertices}
    with open(arquivo, newline='', encoding='utf-8') as f:
        leitor = csv.reader(f); next(leitor)
        for o, d, dist in leitor:
            if d == destino and o in heur:
                heur[o] = float(dist)
    heur[destino] = 0.0
    return heur

def calcular_custo(grafo, caminho):
    # soma peso de cada aresta no caminho
    if not caminho or len(caminho) < 2:
        return 0.0
    return sum(grafo.custo(caminho[i], caminho[i+1]) for i in range(len(caminho)-1))

def analisar_trajeto(inicio, destino,
                     arq_ter="data/distancias_terrestres.csv",
                     arq_aer="data/distancias_aereas.csv"):
    # carrega grafos
    g_ter = carregar_distancias(arq_ter)
    g_aer = carregar_distancias(arq_aer)
    # UCS em cada grafo para garantir menor custo
    _, custo_ter, _, _ = busca_custo_uniforme(g_ter, inicio, destino)
    _, custo_aer, _, _ = busca_custo_uniforme(g_aer, inicio, destino)
    # valida rota
    if custo_ter == float('inf') and custo_aer == float('inf'):
        return None
    # escolhe meio mais curto
    if custo_ter <= custo_aer:
        meio, custo, grafo = "Terrestre", custo_ter, g_ter
    else:
        meio, custo, grafo = "Aéreo", custo_aer, g_aer
    # recupera caminho no grafo escolhido
    caminho, _, _, _ = busca_custo_uniforme(grafo, inicio, destino)
    return {
        "dist_terrestre": custo_ter,
        "dist_aerea"   : custo_aer,
        "meio_mais_curto": meio,
        "caminho_escolhido": caminho,
        "grafo_ter": g_ter
    }

def comparar_algoritmos(inicio, destino, grafo, heur):
    # 1) custo ótimo via UCS
    _, custo_otimo, _, _ = busca_custo_uniforme(grafo, inicio, destino)
    resultados = {}
    # lista de tuplas: (função, precisa_heurística)
    mets = [
        ("BFS",    busca_largura,        False),
        ("DFS",    busca_profundidade,   False),
        ("UCS",    busca_custo_uniforme, False),
        ("Greedy", busca_gulosa,         True),
        ("A*",     busca_a_estrela,      True),
    ]
    for nome, fn, usa_h in mets:
        if usa_h:
            cam, custo_ret, exp, tempo = fn(grafo, inicio, destino, heur)
        else:
            cam, custo_ret, exp, tempo = fn(grafo, inicio, destino)
        # se fn não retorna custo, recalcula
        custo = custo_ret if custo_ret is not None and custo_ret != float('inf') \
                else calcular_custo(grafo, cam)
        otimo = (custo == custo_otimo)
        resultados[nome] = {
            "caminho": cam,
            "distância": custo,
            "nós_expandidos": exp,
            "ótimo": otimo,
            "tempo_s": tempo
        }
    return resultados

def main():
    cenarios = [
        ("Brasília","Goiânia"),
        ("Brasília","Belo Horizonte"),
        ("Brasília","Salvador"),
    ]
    for inicio, destino in cenarios:
        print(f"\n=== Cenário: {inicio} → {destino} ===")
        traj = analisar_trajeto(inicio, destino)
        if traj is None:
            print("Não há rota conectando essas cidades.\n")
            continue
        # 1) Bullet points iniciais
        print(f"• Distância terrestre : {traj['dist_terrestre']:.1f} km")
        print(f"• Distância aérea     : {traj['dist_aerea']:.1f} km")
        print(f"• Meio mais curto     : {traj['meio_mais_curto']}")
        print(f"• Caminho escolhido   : {traj['caminho_escolhido']}")
        # 2) Comparativo de eficiência (no grafo terrestre)
        print("\nComparativo de eficiência (grafo terrestre):")
        heur = carregar_heuristica(destino,
                                   "data/distancias_aereas.csv",
                                   traj["grafo_ter"])
        comp = comparar_algoritmos(inicio, destino,
                                   traj["grafo_ter"], heur)
        # cabeçalho
        print(f"{'Método':<8} {'Dist (km)':<9} {'Nós':<6} {'Ótimo':<6} {'Tempo(s)':<8} Caminho")
        print("-"*80)
        for m, info in comp.items():
            dist = f"{info['distância']:.1f}"
            nos  = info['nós_expandidos']
            opt  = "Sim" if info['ótimo'] else "Não"
            t    = f"{info['tempo_s']:.4f}"
            cam  = "→".join(info['caminho']) if info['caminho'] else "None"
            print(f"{m:<8} {dist:<9} {nos:<6} {opt:<6} {t:<8} {cam}")
    print()

if __name__ == "__main__":
    main()
