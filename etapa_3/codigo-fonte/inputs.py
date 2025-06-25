from data_structure import Grafo
import re

"""
    Leitura e armazenamento dos dados de cada instância disponibilizada na pasta `MCGRP` de modo a armazená-las
    na estrutura de dados Grafo.
    Além disso, utiliza Regex para identificar os padrões nos arquivos .dat e possibilitar uma interpretação
    automatizada do conjunto de dados requisitados.
"""

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