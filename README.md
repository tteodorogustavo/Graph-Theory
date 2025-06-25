# GCC262 - Grafos e suas aplicações

## Trabalho Prático Final 


    Prof:   Mayron César O. Moreira
    
    Alunos:
            Thiago Lima Pereira - 202310057
            Gustavo de Jesus Teodoro - 202311146

### Introdução

Estudar problemas de logística é crucial para otimizar o fluxo de bens e serviços, resultando em maior eficiência e redução de custos para empresas e consumidores. A análise detalhada de processos logísticos permite identificar gargalos, melhorar o planejamento de rotas, gerenciar estoques de forma mais eficaz e implementar tecnologias que aprimoram a tomada de decisões.
A logística desempenha um papel fundamental na competitividade das empresas, influenciando diretamente a satisfação do cliente e a sustentabilidade
ambiental. Ao compreender os desafios logísticos, é possível desenvolver soluções inovadoras que impulsionam o crescimento econômico e promovem um futuro mais eficiente e responsável.

### Estrutura do Projeto

```bash
+ etapa_1/
├── grafo.py
├── visualizacao_de_dados.ipynb
├── selected_instances/
├── README.md

+ etapa_2/
├── etapa2.py
├── G14/ ← pasta onde as soluções são armazenadas automaticamente
```

---

## Etapa 1

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

---

## Etapa 2: Construção de Solução Inicial

Nesta segunda etapa, foi implementado um algoritmo **construtivo** para gerar uma solução inicial viável ao problema do CARP (Capacitated Arc Routing Problem). O objetivo foi gerar rotas que:

- Não ultrapassem a **capacidade dos veículos**;
- Atendam **cada serviço exatamente uma vez**;
- Evitem **duplicidade no cálculo de custo ou demanda**, mesmo que um arco ou vértice seja visitado mais de uma vez.

### Funcionamento do Código

A execução começa pela função `ler_pasta(...)`, que percorre automaticamente os arquivos da pasta `etapa_1/selected_instances/`. Para cada arquivo:

1. É feita a **leitura do grafo** com `ler_arquivo(...)`;
2. O **clock** é iniciado (`clock_inicio`) com `pegar_tempo_clock()` para medir o tempo de execução;
3. O algoritmo construtivo `construir_rotas_carp(grafo)` é chamado;
4. O clock é finalizado (`clock_fim`) e o tempo é armazenado;
5. A função `imprimir_saida_em_pasta(...)` salva o arquivo de saída no formato padronizado na pasta `etapa_2/G14/`.

---

### Estratégia do Algoritmo Construtivo

A solução é construída gradualmente da seguinte forma:

- Inicia-se no **depósito** com capacidade máxima.
- Iterativamente, seleciona-se o **elemento mais próximo** (vértice, aresta ou arco ainda requerido) que caiba na capacidade restante.
- O caminho é calculado com **Floyd-Warshall** (algoritmo desenvolvido na etapa 1) e adicionado à rota.
- A demanda do serviço é descontada da capacidade.
- Após atender a demanda máxima possível, o veículo retorna ao depósito e uma nova rota se inicia.

Este processo garante que:

- Cada serviço é contado **uma única vez**;
- As restrições de **capacidade** são respeitadas;
- O caminho entre pontos é sempre o **mais curto** disponível.

---

### Geração de Saída

A saída para cada instância é salva no formato:

```
sol-NOMEINSTANCIA.dat
```

Com o conteúdo no seguinte padrão:

```
<custo_total_da_solucao>
<total_de_rotas>
<total_de_clocks_para_a_execucao_do_algoritmo_referencia>
<otal_de_clocks_para_encontrar_a_solucao_referencia>
<linha_descrevendo_cada_rota>
```

Cada linha de rota segue o formato exigido pela especificação do problema, incluindo todos os serviços realizados na ordem correta e suas respectivas identificações.

---

### Execução

Para rodar o projeto da Etapa 2, basta executar o script `etapa2.py`:

```bash
python etapa2.py
```

O script irá automaticamente:

- Ler todas as instâncias da pasta `etapa_1/selected_instances/`;
- Processá-las com o algoritmo construtivo;
- Salvar as soluções na pasta `etapa_2/G14/`.

---

## Etapa 3: Métodos de Melhoria e Modularização

Nesta etapa, o foco foi aprimorar a solução inicial gerada na Etapa 2 através da implementação de um método de melhoria e, crucialmente, a modularização do código para uma melhor organização e manutenção do projeto.

### Modularização do Código

Para atender ao feedback de modularização e melhorar a estrutura do projeto, o código foi dividido em módulos com responsabilidades bem definidas. A estrutura de diretórios da `etapa_3` agora se apresenta da seguinte forma:

```bash
+ etapa_3/
├── codigo-fonte/
│   ├── construcao_rotas.py
│   ├── data_structure.py
│   ├── floyd_warshall.py
│   ├── inputs.py
│   ├── main.py
│   ├── optimization.py
│   └── outputs.py
├── G14/ <- pasta onde as soluções são armazenadas automaticamente
├── MCGRP/ <- pasta com todas as soluções a serem executadas
├── G14.zip
└── README.md
```

Cada arquivo dentro de `codigo-fonte/` tem um propósito específico:

*   `construcao_rotas.py`: Contém a lógica para a construção das rotas iniciais (algoritmo construtivo).
*   `data_structure.py`: Define a estrutura de dados do grafo que será processada pelos demais algoritmos.
*   `floyd_warshall.py`: Implementa o algoritmo de Floyd-Warshall para cálculo de caminhos mais curtos.
*   `inputs.py`: Responsável pela leitura e parsing dos arquivos de entrada (`.dat`).
*   `main.py`: O arquivo principal que orquestra a execução, chamando as funções dos outros módulos.
*   `optimization.py`: Contém os algoritmos de otimização, como o 2-opt.
*   `outputs.py`: Lida com a formatação e gravação dos arquivos de saída.

Esta abordagem visa tornar o código mais limpo, coeso e fácil de entender, facilitando futuras modificações e extensões.

### Algoritmo 2-opt

Para aprimorar as rotas geradas pelo algoritmo construtivo, foi implementado o algoritmo de otimização **2-opt**. Este é um dos métodos de busca local comumente utilizado para resolver o Problema do Caixeiro Viajante (TSP) e problemas de roteamento de veículos, como o CARP, que encontramos na literatura e resolvemos implementar.

#### Como funciona o 2-opt:

O algoritmo 2-opt opera iterativamente em uma rota existente, buscando melhorias. Ele funciona da seguinte maneira:

1.  **Seleção de Segmentos:** Escolhe dois segmentos não adjacentes da rota.
2.  **Inversão:** Inverte a ordem dos nós em um dos segmentos selecionados.
3.  **Avaliação:** Calcula o custo da nova rota resultante.
4.  **Troca:** Se a nova rota tiver um custo total menor que a rota original e ainda respeitar as restrições de capacidade e demanda, a troca é aceita e a nova rota se torna a rota atual.
5.  **Iteração:** O processo se repete até que nenhuma melhoria significativa possa ser encontrada, ou seja, até que nenhuma troca de 2-opt resulte em uma rota de menor custo.

No contexto deste trabalho, a implementação do 2-opt foi adaptada para garantir que as restrições do CARP (capacidade do veículo e atendimento único de serviços) sejam mantidas durante as operações de troca.

### Execução da Etapa 3

Para executar a solução da Etapa 3, você deve rodar o arquivo `main.py` localizado dentro da pasta `codigo-fonte/`:

```bash
python etapa_3/codigo-fonte/main.py
```

Este script irá:

- Ler as instâncias de teste.
- Gerar uma solução inicial usando o algoritmo construtivo.
- Aplicar o algoritmo 2-opt para otimizar as rotas.
- Salvar os resultados otimizados na pasta `etapa_3/G14/` no formato `sol-NOMEINSTANCIA.dat`.
