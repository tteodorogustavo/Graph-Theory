from collections import deque
from floyd_warshall import reconstruir_caminho, floyd_warshall

"""

    Neste arquivo encontram-se as linhas de código nececessárias para o algoritmo construtivo;
    A função executa o algoritmo de floyd-warshall possibilitando a criação das rotas CARP
    com base na matriz de distância e predecessores fornecida pelo algoritmo.
    Esse processo construtivo leva em consideração todas os vértices, arcos e arestas requeridos
    formando a rota através deles de maneira obrigatória.

    Retorna todas as rotas construídas.

"""

def construir_rotas_carp(grafo): # recebe um grafo para que crie as rotas
    dist, pred = floyd_warshall(grafo)
    deposito = grafo.deposito
    capacidade_max = grafo.capacidade
    rotas = []

    vertices_req = deque(grafo.vertices_req)
    arestas_req = deque(grafo.arestas_req)
    arcos_req = deque(grafo.arcos_req)

    while vertices_req or arestas_req or arcos_req:
        rota = [deposito]
        capacidade = capacidade_max
        current = deposito

        while capacidade > 0 and (vertices_req or arestas_req or arcos_req):
            melhor_custo = float('inf')
            proximo_elemento = None
            tipo_elemento = None
            demanda_elemento = None
            idx_elemento = None

            # Vertices requeridos
            for idx, (v, demanda) in enumerate(vertices_req):
                if demanda > capacidade:
                    continue
                custo = dist[current-1][v-1] + 1  # custo de trânsito + serviço
                if custo < melhor_custo:
                    melhor_custo = custo
                    proximo_elemento = v
                    tipo_elemento = 'vertice'
                    demanda_elemento = demanda
                    idx_elemento = idx

            # Arestas requeridas
            for idx, (u, v, t_cost, demanda) in enumerate(arestas_req):
                if demanda > capacidade:
                    continue
                custo1 = dist[current-1][u-1] + t_cost + 1
                custo2 = dist[current-1][v-1] + t_cost + 1
                custo = min(custo1, custo2)
                if custo < melhor_custo:
                    melhor_custo = custo
                    proximo_elemento = (u, v, t_cost, idx)
                    tipo_elemento = 'aresta'
                    demanda_elemento = demanda
                    idx_elemento = idx

            # Arcos requeridos
            for idx, (u, v, t_cost, demanda) in enumerate(arcos_req):
                if demanda > capacidade:
                    continue
                custo = dist[current-1][u-1] + t_cost + 1
                if custo < melhor_custo:
                    melhor_custo = custo
                    proximo_elemento = (u, v, t_cost, idx)
                    tipo_elemento = 'arco'
                    demanda_elemento = demanda
                    idx_elemento = idx

            if not proximo_elemento:
                break

            if tipo_elemento == 'vertice':
                caminho = reconstruir_caminho(pred, current-1, proximo_elemento-1)
                rota.extend([p+1 for p in caminho[1:] if (p+1) != rota[-1]])
                vertices_req.remove(vertices_req[idx_elemento])
                capacidade -= demanda_elemento
                current = proximo_elemento

            elif tipo_elemento == 'aresta':
                u, v, t_cost, idx = proximo_elemento
                if dist[current-1][u-1] <= dist[current-1][v-1]:
                    caminho = reconstruir_caminho(pred, current-1, u-1)
                    rota.extend([p+1 for p in caminho[1:] if (p+1) != rota[-1]])
                    if rota[-1] != v:
                        rota.append(v)
                    current = v
                else:
                    caminho = reconstruir_caminho(pred, current-1, v-1)
                    rota.extend([p+1 for p in caminho[1:] if (p+1) != rota[-1]])
                    if rota[-1] != u:
                        rota.append(u)
                    current = u
                del arestas_req[idx_elemento]
                capacidade -= demanda_elemento

            elif tipo_elemento == 'arco':
                u, v, t_cost, idx = proximo_elemento
                caminho = reconstruir_caminho(pred, current-1, u-1)
                rota.extend([p+1 for p in caminho[1:] if (p+1) != rota[-1]])
                if rota[-1] != v:
                    rota.append(v)
                current = v
                del arcos_req[idx_elemento]
                capacidade -= demanda_elemento

        caminho = reconstruir_caminho(pred, current-1, deposito-1)
        rota.extend([p+1 for p in caminho[1:] if (p+1) != rota[-1]])
        rotas.append(rota)

    return rotas