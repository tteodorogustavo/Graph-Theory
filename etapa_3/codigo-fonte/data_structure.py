"""
    Estrutura de dados "Grafo" utilizada para armazenar as informações presentes no arquivo de cada
    instância, de modo a disponibilizar posteriormente para processamento cada um dos grafos interpretados.
"""

class Grafo:
    def __init__(self, num_vertices):
        self.nome = ""
        self.tipo = "CARP"
        self.num_vertices = num_vertices
        self.num_arestas = 0
        self.num_arcos = 0
        self.num_arestas_req = 0
        self.num_arcos_req = 0
        self.capacidade = 0
        self.custo_total = 0
        self.deposito = None
        self.arestas = []
        self.arcos = []
        self.arestas_req = []
        self.arcos_req = []
        self.vertices_req = []
        self.adj_matrix = [
            [float('inf')] * num_vertices for _ in range(num_vertices)
        ]
        for i in range(num_vertices):
            self.adj_matrix[i][i] = 0

    def adicionar_aresta(self, u, v, custo, demanda):
        self.arestas.append((u, v, custo, demanda))
        if demanda > 0:
            self.arestas_req.append((u, v, custo, demanda))
        self.adj_matrix[u-1][v-1] = custo
        self.adj_matrix[v-1][u-1] = custo

    def adicionar_arco(self, u, v, custo, demanda):
        self.arcos.append((u, v, custo, demanda))
        if demanda > 0:
            self.arcos_req.append((u, v, custo, demanda))
        self.adj_matrix[u-1][v-1] = custo