import time

def busca_profundidade(grafo, inicio, objetivo):
    start = time.perf_counter()
    pilha = [[inicio]]
    visitados = set()
    expandidos = 0

    while pilha:
        caminho = pilha.pop()
        atual = caminho[-1]
        expandidos += 1

        if atual == objetivo:
            elapsed = time.perf_counter() - start
            return caminho, None, expandidos, elapsed

        if atual not in visitados:
            visitados.add(atual)
            for vizinho in grafo.vizinhos(atual):
                pilha.append(caminho + [vizinho])

    elapsed = time.perf_counter() - start
    return None, None, expandidos, elapsed
