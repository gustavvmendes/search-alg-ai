class Grafo:
    def __init__(self):
        self.vertices = {}
    
    def adicionar_vertice(self, nome):
        if nome not in self.vertices:
            self.vertices[nome] = {}

    def adicionar_aresta(self, origem, destino, custo):
        self.adicionar_vertice(origem)
        self.adicionar_vertice(destino)
        self.vertices[origem][destino] = custo
        self.vertices[destino][origem] = custo  # Grafo não-direcionado

    def vizinhos(self, vertice):
        return self.vertices.get(vertice, {})
    
    def custo(self, origem, destino):
        return self.vertices[origem].get(destino, float('inf'))
