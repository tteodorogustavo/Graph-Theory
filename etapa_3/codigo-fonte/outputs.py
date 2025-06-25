"""
    Padronização dos arquivos de saída de acordo com o arquivo "padrões de escrita" disponibilizado
    pelo professor. As saídas recebem as informações dos processamentos, como rotas e seus respectivos vértices,
    e as disponibilizam no formato .dat novamente.
"""

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