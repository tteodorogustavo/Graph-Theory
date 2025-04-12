# GCC262 - Grafos e suas aplicações

## Trabalho Prático Final 


    Prof:   Mayron César O. Moreira
    
    Alunos:
            Thiago Lima Pereira - 202310057
            Gustavo de Jesus Teodoro - 202311146

*  Introdução

Estudar problemas de logística é crucial para otimizar o fluxo de bens e serviços, resultando em maior eficiência e redução de custos para empresas e consumidores. A análise detalhada de processos logísticos permite identificar gargalos, melhorar o planejamento de rotas, gerenciar estoques de forma mais eficaz e implementar tecnologias que aprimoram a tomada de decisões.
A logística desempenha um papel fundamental na competitividade das empresas, influenciando diretamente a satisfação do cliente e a sustentabilidade
ambiental. Ao compreender os desafios logísticos, é possível desenvolver soluções inovadoras que impulsionam o crescimento econômico e promovem um futuro mais eficiente e responsável.

### Estrutura do Código

```bash
+ etapa_1/
├── grafo.py
├── visualizacao_de_dados.ipynb
├── selected_instances/
└── README.md
```

#### Exercícios:

##### Etapa 1:

A primeira etapa solicitava que realizassemos a criação de uma estrutura de dados para receber grafos. Para testes, utilizamos arquivos da pasta `selected_instances`, mais especificamente os arquivos nomeados como `BHW*.bat`.
Sendo assim, realizamos a leitura dos dados juntamente com um ETL, utilizando python para que seja necessário somente modificar o nome do arquivo que descreve o grafo para que ele seja inserido na estrutura de dados e realize as devidas operações.

Logo após isso foram solicitadas respostas estatísticas relacionadas ao grafos em questão as quais se encontram a seguir:

1. Quantidade de vértices;
2. Quantidade de arestas;
3. Quantidade de arcos;
4. Quantidade de vértices requeridos;
5. Quantidade de arestas requeridas;
6. Quantidade de arcos requeridos;
7. Densidade do grafo (order strength);
8. Componentes conectados; (Havia uma observação de que essa resposta não era mais necessária para o desenvolvimento do trabalho)
9. Grau mínimo dos vértices;
10. Grau máximo dos vértices;
11. Intermediação;
12. Caminho médio;
13. Diâmetro.

---

## Pontos importantes do código:


### Algoritmo de Floyd-Warshall:

Algoritmo aprendido em sala de aula, usado para busca em largura.

```python
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
```

### Reconstruir caminho:

Usado na resposta da questão 11 para calcular a intermediação.

```python
   def reconstruir_caminho(pred, s, t):
    caminho = []
    if pred[s][t] is None:
        return caminho
    while t != s:
        caminho.insert(0, t)
        t = pred[s][t]
    caminho.insert(0, s)
    return caminho
```

### Cálculo da intermediação(usando a função acima de reconstruir caminho):

Usado para medir a frequência que um determinado nó aparece nos caminhos mais curtos entre outros nós.

```python
    def calcular_intermediacao_fw(grafo):
    n = grafo.num_vertices
    dist, pred = floyd_warshall(grafo)
    intermediacao = {v: 0 for v in range(1, n + 1)}


    for s in range(n):
        for t in range(n):
            if s != t:
                caminho = reconstruir_caminho(pred, s, t)
                for v in caminho[1:-1]:  
                    intermediacao[v + 1] += 1 


    return intermediacao
```

### Cálculo do caminho médio:

O uso dessa função é importante para encontrar o valor médio dos caminhos mínimos.

```python
   def calcular_caminho_medio(grafo):
    dist, _ = floyd_warshall(grafo)
    n = grafo.num_vertices
    soma = 0
    total_pares = 0


    for i in range(n):
        for j in range(n):
            if i != j and dist[i][j] != float('inf'):
                soma += dist[i][j]
                total_pares += 1


    caminho_medio = soma / total_pares if total_pares > 0 else 0
    return round(caminho_medio, 3)
```


### Cálculo do diametro do grafo:

Esse cálculo é importante para encontrar o menor dos caminhos mínimos.

```python
   def calcular_diametro(grafo):
    dist, _ = floyd_warshall(grafo)
    n = grafo.num_vertices
    diametro = 0


    for i in range(n):
        for j in range(n):
            if i != j and dist[i][j] != float('inf'):
                diametro = max(diametro, dist[i][j])


    return diametro
```