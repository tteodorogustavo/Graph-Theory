"""
Algoritmo de Floyd-Warshall que busca de maneira iterativa os caminhos mais curtos entre dois vértices, 
nesse caso, retornando a matriz de predecessores e as distâncias de cada vértice.
"""

def floyd_warshall(grafo):
    n = grafo.num_vertices
    dist = [[float('inf')] * n for _ in range(n)]
    pred = [[None] * n for _ in range(n)]

    for i in range(n):
        dist[i][i] = 0

    for u in range(n):
        for v in range(n):
            if grafo.adj_matrix[u][v] != float('inf'):
                dist[u][v] = grafo.adj_matrix[u][v]
                pred[u][v] = u

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    pred[i][j] = pred[k][j]
    return dist, pred

def reconstruir_caminho(pred, s, t):
    caminho = []
    if pred[s][t] is None:
        return caminho
    while t != s:
        caminho.insert(0, t)
        t = pred[s][t]
    caminho.insert(0, s)
    return caminho
