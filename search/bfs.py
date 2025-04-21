from collections import deque
import time

def busca_largura(grafo, inicio, objetivo):
    start = time.perf_counter()
    fila = deque([[inicio]])
    visitados = set()
    expandidos = 0

    while fila:
        caminho = fila.popleft()
        atual = caminho[-1]
        expandidos += 1

        if atual == objetivo:
            elapsed = time.perf_counter() - start
            return caminho, None, expandidos, elapsed

        if atual not in visitados:
            visitados.add(atual)
            for vizinho in grafo.vizinhos(atual):
                fila.append(caminho + [vizinho])

    elapsed = time.perf_counter() - start
    return None, None, expandidos, elapsed
