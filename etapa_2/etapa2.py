import re
from collections import deque
import time
import os

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

def ler_arquivo(path):
    grafo = None
    secao = None
    nome = ""
    capacidade = 0
    deposito = None
    num_vertices = None


    with open(path, 'r') as f:
        for linha in f:
            linha = linha.strip()
            if not linha or linha.startswith("the data"):
                continue

            
            match = re.match(r"(.*?):\s*(\S+)", linha)
            if match:
                chave = match.group(1).strip().upper().replace('#', '').replace(' ', '')
                valor = match.group(2).strip()


                if chave == "NAME":
                    nome = valor
                elif chave == "CAPACITY":
                    capacidade = int(valor)
                elif chave == "DEPOTNODE":
                    deposito = int(valor)
                elif chave == "NODES":
                    num_vertices = int(valor)
                    grafo = Grafo(num_vertices)
                elif chave == "EDGES" and grafo:
                    grafo.num_arestas = int(valor)
                elif chave == "ARCS" and grafo:
                    grafo.num_arcos = int(valor)
                elif chave == "REQUIREDE" and grafo:
                    grafo.num_arestas_req = int(valor)
                elif chave == "REQUIREDA" and grafo:
                    grafo.num_arcos_req = int(valor)

                
                if grafo:
                    grafo.nome = nome
                    grafo.capacidade = capacidade
                    grafo.deposito = deposito


                continue

            
            if linha.startswith("ReE."):
                secao = "ARESTA_REQ"
                continue
            if linha.startswith("ReA."):
                secao = "ARCO_REQ"
                continue
            if linha.startswith("ARC"):
                secao = "ARCO_NREQ"
                continue
            if linha.startswith("EDGE"):
                secao = "ARESTA_NREQ"
                continue

            
            if grafo:
                partes = linha.split()
                if secao == "ARESTA_REQ" and len(partes) >= 6:
                    _, u, v, custo, demanda, _ = partes
                    grafo.adicionar_aresta(int(u), int(v), int(custo), int(demanda))
                elif secao == "ARCO_REQ" and len(partes) >= 6:
                    _, u, v, custo, demanda, _ = partes
                    grafo.adicionar_arco(int(u), int(v), int(custo), int(demanda))
                elif secao == "ARESTA_NREQ" and len(partes) >= 4:
                    _, u, v, custo = partes
                    grafo.adicionar_aresta(int(u), int(v), int(custo), 0)
                elif secao == "ARCO_NREQ" and len(partes) >= 4:
                    if not linha.strip():
                        break 
                    if len(partes) >= 4 and partes[-3].isdigit() and partes[-2].isdigit() and partes[-1].isdigit():
                        _, u, v, custo = partes[-4:]
                        grafo.adicionar_arco(int(u), int(v), int(custo), 0)
                    else:
                        break


    return grafo
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

def construir_rotas_carp(grafo):
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

def imprimir_saida_formatada(grafo, rotas, clocks_execucao_ref, clocks_solucao_ref):
    custo_total_solucao = 0
    total_rotas = len(rotas)
    clocks_execucao_ref = clocks_execucao_ref
    clocks_solucao_ref = clocks_solucao_ref

    for rota in rotas:
        custo_rota = 0
        for i in range(len(rota) - 1):
            custo_rota += grafo.adj_matrix[rota[i]-1][rota[i+1]-1]
        custo_total_solucao += custo_rota

    vert_req_dict = {v[0]: idx+1 for idx, v in enumerate(grafo.vertices_req)}
    ar_req_dict = {}
    idx_base = len(grafo.vertices_req)
    for idx, (u,v,c,d) in enumerate(grafo.arestas_req):
        ar_req_dict[("aresta", u, v)] = idx_base + idx + 1
        ar_req_dict[("aresta", v, u)] = idx_base + idx + 1
    for idx, (u,v,c,d) in enumerate(grafo.arcos_req):
        ar_req_dict[("arco", u, v)] = idx_base + len(grafo.arestas_req) + idx + 1

    linhas_rotas = []

    for i, rota in enumerate(rotas):
        demanda_rota = 0
        custo_rota = 0
        total_visitas = len(rota)
        servicos_visitados = set()

        for j in range(len(rota) - 1):
            u = rota[j]
            v = rota[j+1]
            custo_rota += grafo.adj_matrix[u-1][v-1]
            for (au, av, ac, ad) in grafo.arestas_req:
                if (u == au and v == av) or (u == av and v == au):
                    demanda_rota += ad
                    servicos_visitados.add(ar_req_dict[("aresta", au, av)])
                    break
            for (au, av, ac, ad) in grafo.arcos_req:
                if u == au and v == av:
                    demanda_rota += ad
                    servicos_visitados.add(ar_req_dict[("arco", au, av)])
                    break
        for v in rota:
            if v in vert_req_dict:
                for (vn, vd) in grafo.vertices_req:
                    if vn == v:
                        demanda_rota += vd
                        servicos_visitados.add(vert_req_dict[v])
                        break

        linha = f" 0 1 {i+1} {demanda_rota} {custo_rota}  {total_visitas} "
        linha += "(D 0,1,1) "
        for j in range(len(rota)-1):
            u = rota[j]
            v = rota[j+1]
            serv_impresso = False
            for idx_arco, (au, av, ac, ad) in enumerate(grafo.arcos_req):
                id_serv = idx_base + len(grafo.arestas_req) + idx_arco + 1
                if u == au and v == av:
                    linha += f"(S {id_serv},{u},{v}) "
                    serv_impresso = True
                    break
            if serv_impresso:
                continue
            for idx_aresta, (au, av, ac, ad) in enumerate(grafo.arestas_req):
                id_serv = idx_base + idx_aresta + 1
                if (u == au and v == av) or (u == av and v == au):
                    linha += f"(S {id_serv},{u},{v}) "
                    serv_impresso = True
                    break
            if serv_impresso:
                continue
            if v in vert_req_dict:
                id_serv = vert_req_dict[v]
                linha += f"(S {id_serv},{v},{v}) "
        linha += "(D 0,1,1) "
        linhas_rotas.append(linha)

    with open(f"sol-{grafo.nome}.dat", "w") as f:
        f.write(f"{custo_total_solucao}\n")
        f.write(f"{total_rotas}\n")
        f.write(f"{clocks_execucao_ref}\n")
        f.write(f"{clocks_solucao_ref}\n")
        for linha in linhas_rotas:
            f.write(linha + "\n")

# função para pegar o tempo de clock
def pegar_tempo_clock():
    return time.monotonic_ns()

def ler_pasta(path):
    for nome_arquivo in os.listdir(path): 
        if nome_arquivo.endswith(".dat"):
            caminho_arquivo = os.path.join(path, nome_arquivo)
            clock_inicio = pegar_tempo_clock()
            grafo = ler_arquivo(caminho_arquivo)
            rotas = construir_rotas_carp(grafo)
            clock_fim = pegar_tempo_clock()
            clocks_execucao_ref = clock_fim - clock_inicio
            clocks_solucao_ref = clock_fim - clock_inicio
            imprimir_saida_em_pasta(grafo, rotas, clocks_execucao_ref, clocks_solucao_ref)

# imprime o arquivo gerado em "def saida_formatada" em uma pasta de saída
def imprimir_saida_em_pasta(grafo, rotas, clocks_execucao_ref, clocks_solucao_ref):
    pasta_saida = "./etapa_2/G14/"
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)
    # muda de diretório para a pasta de saída
    cwd = os.getcwd()
    os.chdir(pasta_saida)
    # Chama a função para criar o arquivo
    imprimir_saida_formatada(grafo, rotas, clocks_execucao_ref, clocks_solucao_ref)
    # Retorna ao diretório original
    os.chdir(cwd)

if __name__ == "__main__":
    ler_pasta("./MCGRP/")
    print("Execução concluída.")
    print("Arquivos de saída gerados na pasta ./etapa_2/G14/")
