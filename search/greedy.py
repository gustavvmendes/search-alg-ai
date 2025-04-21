import heapq, time

def busca_gulosa(grafo, inicio, objetivo, heuristica):
    start = time.perf_counter()
    fila = [(heuristica.get(inicio, float('inf')), [inicio])]
    visitados = set()
    expandidos = 0

    while fila:
        _, caminho = heapq.heappop(fila)
        atual = caminho[-1]
        expandidos += 1

        if atual == objetivo:
            elapsed = time.perf_counter() - start
            return caminho, None, expandidos, elapsed

        if atual not in visitados:
            visitados.add(atual)
            for vizinho in grafo.vizinhos(atual):
                heapq.heappush(fila, (heuristica.get(vizinho, float('inf')), caminho + [vizinho]))

    elapsed = time.perf_counter() - start
    return None, None, expandidos, elapsed
