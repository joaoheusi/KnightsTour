import networkx as nx
import numpy as np
import string
import matplotlib.pyplot as plt

#Dicionário para interpretação das letras no tabuleiro
def letterpos(key):
    letter_pos = {
    'A':0,
    'B':1,
    'C':2,
    'D':3,
    'E':4,
    'F':5,
    'G':6,
    'H':7,
    0:'A',
    1:'B',
    2:'C',
    3:'D',
    4:'E',
    5:'F',
    6:'G',
    7:'H'
    }
    return(letter_pos.get(key,'Invalid'))


def initiateGraph(graph):
    #Gera cada vértice do grafo
    letters = list(string.ascii_uppercase)
    for position in np.arange(0,8,1):
        for letter in letters[0:8]:
            graph.add_node('{}{}'.format(letter,position),posx= letterpos(letter),posy=position, moveNumber =0)

    #Mapeamento dos movimentos possíveis do Cavalo
    vizinhanca_cavalo = [{'moveX':-1,'moveY':-2},
                        {'moveX':1,'moveY':-2},
                        {'moveX':-2,'moveY':-1},
                        {'moveX':2,'moveY':-1},
                        {'moveX':-2,'moveY':1},
                        {'moveX':2,'moveY':1},
                        {'moveX':-1,'moveY':2},
                        {'moveX':1,'moveY':2}]

    #Definição de movimentos possíveis no tabuleiro; Criação das arestas. utiliza o mapeamento acima para gerar as arestas entre os vértices do grafo.
    for node in graph.nodes:
        for vizinhanca in vizinhanca_cavalo:
            nextX =(graph.nodes[node]['posx'] + vizinhanca.get('moveX'))
            nextY =(graph.nodes[node]['posy'] + vizinhanca.get('moveY'))
            #Somente adicionar quando dentro do tabuleiro.
            if nextX in range(0,8) and nextY in range(0,8):
                neighbor = ('{}{}'.format(letterpos(nextX),nextY))
                graph.add_edge(node,neighbor)

#Função utilizada para encerrar a resolução do problema quando a busca chegar à um resultado não False 
def first_true(sequence):
    for item in sequence:
        if item:
            return item
    return None

#Codificação da heuristica de Warndorff. Utilizando a lista de vértices adjacentes,
# retorna a mesma, mas ordernada por ordem crescente de acessibilidade.  
def warndorffs_sorting(Graph,old_list):
    acessibility_List = list()
    for item in old_list:
        acessibility_List.append({'Node':item,
                                'Acessibility':checkAcessibility(Graph,item)})
    acessibility_List = sorted(acessibility_List, key= lambda i: (i['Acessibility'], i['Node']))
    chosen_list = list()
    for i in acessibility_List:
            chosen_list.append(i.get('Node'))
    return chosen_list

#Funcão que avalia qual a acessibilidade de um vértice do grafo. Acessibilidade = número de vértices adjacentes.
def checkAcessibility(Graph,Node):
    aux_list = list(Graph.neighbors(Node))
    return len(aux_list)

# Função principal para resolver o problema do passeio do cavalo.
def find_solution(graph, starting_node = 'A0'):
    #Tamanho do tabuleiro é utilizado para encerrar o programa.
    totalNodes = len(list(graph.nodes))
    
    #Recebe o caminho de vértices já visitados e o vértice atual.
    def traverse(path, currentNode):
        #Caso o tamanho da lista path percorrida pela recursividade seja o tamanho total do grafo, a função é encerrada com exito.
        if len(path) + 1 == totalNodes:
            path += [currentNode]
            return path

        #O vertor de próximos vértices a serem visitados é: vizinhos do vertice atual - itens já vizitados no caminho.
        yet_to_visit = [item for item in list(graph.neighbors(currentNode)) if item not in path]

        #Condição para verificar se existem vizinhos não visitados.
        #Caso não existam visinhos não vizitados significa que o caminho percorrido até aqui não é viável.
        if len(yet_to_visit) == 0:
            return False

        #É ordenado o vetor seguindo a função de ordenação selecionada. Cada função de ordenação explica como é seu funcionamento.
        neighbors = warndorffs_sorting(graph,yet_to_visit)

        # É passada a proxima iteração da busca, utilizando os vértices de yet_to_visit
        return first_true(traverse(path + [currentNode],node) for node in neighbors)
    
    return (traverse([], starting_node))

""" G = nx.Graph()
initiateGraph(G)

print(find_solution(G, 'A0'))
solution =  find_solution(G, 'A0')
 """
def convert_solution(sequence,graph):
    outermatrix = []
    newmatrix = []
    for i in range(8):
        newmatrix.append([0] * 8)
    for i in range(9):
        outermatrix.append([0] * 9)
    for i in sequence:
        graph.nodes[i]['moveNumber'] = sequence.index(i)
    
    for i in graph.nodes:
        posx = graph.nodes[i]['posx']
        posy = graph.nodes[i]['posy']
        mov = graph.nodes[i]['moveNumber']
        newmatrix[posy][posx]= mov

    outermatrix[0] = ['','','','','','','','','']
    outermatrix[1][0] = ' '
    outermatrix[2][0] = ' '
    outermatrix[3][0] = ' '
    outermatrix[4][0] = ' '
    outermatrix[5][0] = ' '
    outermatrix[6][0] = ' '
    outermatrix[7][0] = ' '   
    outermatrix[8][0] = ' '

    for i in range(len(newmatrix)):
        for j in range(len(newmatrix[i])):
            outermatrix[i+1][j+1] = newmatrix[i][j]

    return outermatrix
