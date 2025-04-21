import heapq, time

def busca_a_estrela(grafo, inicio, objetivo, heuristica):
    start = time.perf_counter()
    fila = [(heuristica.get(inicio, float('inf')), 0, [inicio])]
    visitados = set()
    expandidos = 0

    while fila:
        estimativa, custo_real, caminho = heapq.heappop(fila)
        atual = caminho[-1]
        expandidos += 1

        if atual == objetivo:
            elapsed = time.perf_counter() - start
            return caminho, custo_real, expandidos, elapsed

        if atual not in visitados:
            visitados.add(atual)
            for vizinho, custo in grafo.vizinhos(atual).items():
                g_novo = custo_real + custo
                f_novo = g_novo + heuristica.get(vizinho, float('inf'))
                heapq.heappush(fila, (f_novo, g_novo, caminho + [vizinho]))

    elapsed = time.perf_counter() - start
    return None, float('inf'), expandidos, elapsed
