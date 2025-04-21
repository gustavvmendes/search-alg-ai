import heapq, time

def busca_custo_uniforme(grafo, inicio, objetivo):
    start = time.perf_counter()
    fila = [(0, [inicio])]
    visitados = set()
    expandidos = 0

    while fila:
        custo_total, caminho = heapq.heappop(fila)
        atual = caminho[-1]
        expandidos += 1

        if atual == objetivo:
            elapsed = time.perf_counter() - start
            return caminho, custo_total, expandidos, elapsed

        if atual not in visitados:
            visitados.add(atual)
            for vizinho, custo in grafo.vizinhos(atual).items():
                heapq.heappush(fila, (custo_total + custo, caminho + [vizinho]))

    elapsed = time.perf_counter() - start
    return None, float('inf'), expandidos, elapsed
