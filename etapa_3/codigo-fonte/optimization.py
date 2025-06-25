"""
    Algoritmo referente a otimização das soluções encontradas nas etapas 1 e 2.
        O algoritmo 2-opt é uma heurística de busca local comumente utilizada para resolver
        problemas de roteamento de veículos.
        Ele opera melhorando iterativamente uma solução existente (uma rota) através da troca de duas arestas não adjacentes.
        Dessa forma ele rebece um grafo e as suas rotas correspondentes e utilizando substituições de arestas tenta encontrar,
        dentro de cada uma dessas rotas um novo caminho possívelmente melhor que o atual.
"""

def melhorar_rotas_2opt(grafo, rotas):
    def calcular_custo(rota):
        return sum(grafo.adj_matrix[rota[i]-1][rota[i+1]-1] for i in range(len(rota)-1))

    def demanda_rota(rota):
        visitados = set()
        demanda_total = 0
        for i in range(len(rota) - 1):
            u, v = rota[i], rota[i + 1]
            for (a, b, c, d) in grafo.arestas_req:
                if (u == a and v == b) or (u == b and v == a):
                    if (min(a,b), max(a,b)) not in visitados:
                        demanda_total += d
                        visitados.add((min(a,b), max(a,b)))
            for (a, b, c, d) in grafo.arcos_req:
                if u == a and v == b and (a,b) not in visitados:
                    demanda_total += d
                    visitados.add((a,b))
            for (v_req, d) in grafo.vertices_req:
                if v == v_req and v not in visitados:
                    demanda_total += d
                    visitados.add(v)
        return demanda_total

    novas_rotas = []
    for rota in rotas:
        melhor_rota = rota[:]
        melhor_custo = calcular_custo(melhor_rota)
        melhorou = True

        while melhorou:
            melhorou = False
            for i in range(1, len(melhor_rota) - 2):
                for j in range(i + 1, len(melhor_rota) - 1):
                    if j - i == 1:
                        continue
                    nova_rota = melhor_rota[:i] + melhor_rota[i:j][::-1] + melhor_rota[j:]
                    if nova_rota[0] != grafo.deposito or nova_rota[-1] != grafo.deposito:
                        continue
                    nova_demanda = demanda_rota(nova_rota)
                    if nova_demanda > grafo.capacidade:
                        continue
                    novo_custo = calcular_custo(nova_rota)
                    if novo_custo < melhor_custo:
                        melhor_rota = nova_rota
                        melhor_custo = novo_custo
                        melhorou = True
        novas_rotas.append(melhor_rota)
    return novas_rotas