import time, os
from data_structure import Grafo
from inputs import ler_arquivo
from construcao_rotas import construir_rotas_carp
from optimization import melhorar_rotas_2opt
from outputs import imprimir_saida_formatada

"""
    Função main, reponsável por pegar o tempo de clock, ler as pastas fornecidas e agrupar todos os resultados
    em outra pasta específica.
"""



# função para pegar o tempo de clock
def pegar_tempo_clock():
    return time.monotonic_ns()

def ler_pasta(path):
    for nome_arquivo in os.listdir(path): 
        if nome_arquivo.endswith(".dat"):
            caminho_arquivo = os.path.join(path, nome_arquivo)
            clock_inicio = pegar_tempo_clock()
            grafo = ler_arquivo(caminho_arquivo)
            
            # 1. Solução inicial
            clock_inicio = pegar_tempo_clock()
            rotas_iniciais = construir_rotas_carp(grafo)
            clock_meio = pegar_tempo_clock()

            # 2. Aplicar 2-opt
            rotas = melhorar_rotas_2opt(grafo, rotas_iniciais)
            clock_fim = pegar_tempo_clock()

            # Clocks
            clocks_execucao_ref = clock_meio - clock_inicio         # tempo até a solução inicial
            clocks_solucao_ref = clock_fim - clock_inicio           # tempo total até a solução final
            imprimir_saida_em_pasta(grafo, rotas, clocks_execucao_ref, clocks_solucao_ref)

# imprime o arquivo gerado em "def saida_formatada" em uma pasta de saída
def imprimir_saida_em_pasta(grafo, rotas, clocks_execucao_ref, clocks_solucao_ref):
    pasta_saida = "./G14/"
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
    ler_pasta("../MCGRP/")
    print("Execução concluída.")
    print("Arquivos de saída gerados na pasta ./G14/")