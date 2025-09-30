from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import re

#Variáveis globais
dados_globais = {}
escala_global = 1
largura_window, altura_window = 1280, 720


def data_load(arquivo, largura, altura):
    #vai ler os dados do Paths_D.txt linha por linha
    pontos_por_pessoa = {}
    pixels_por_metro = {}

    try:
        with open(arquivo, 'r') as f:
            linhas = f.readlines() #linhas é uma lista onde cada linha é um elemento na lista, sendo uma lista de strings

            #a primeira linha é processada para escala
            escala = re.search(r'\[(\d+)\]', linhas[0])
            if escala:
                pixels_por_metro = int(escala.group(1))

            #processa as linhas de coordenadas dos pontos do dataset
            #A PARTIR DA SEGUNDA LINHA
            id_pessoa_atual = 1
            for i in range (1, len(linhas)):
                linha = linhas[i].strip()
                if not linha: continue # serve para ignorar linhas vazias

                #da esquerda para a direita, separa a string no primeiro espaço em branco que encontrar
                partes = linha.split(maxsplit=1)

                if len(partes) == 2: #verifica se dividiu em 2
                    contagem_str, string_coordenadas = partes #divide as partes em duas diferentes variáveis
                    contagem_declarada = int(contagem_str) # converte a contagem de string pra INT
                    #re.findall encontra todas as ocorrencias de (x,y,f) na string e
                    #retorna uma lista de tuplas
                    coordenadas_encontradas = re.findall(r'\((\d+),(\d+),(\d+)\)', string_coordenadas)

                    #cria uma lista para guardar o caminho final dessa pessoa
                    caminho = []
                    #itera sobre cada dupla de cordenada encontrada
                    for coord in coordenadas_encontradas:
                         #converter para int
                         x = int(coord[0])
                         y = int(coord[1])

                         x_normalizado = (x / largura) * 2 - 1
                         y_normalizado = 1 - (y / altura) * 2

                         caminho.append((x_normalizado,y_normalizado)) #bota a tupla x,y na lista caminho

                    if len(caminho) != contagem_declarada:
                         print (f"ERRO: Número diferente de pessoas declaradas e encontradas: "
                                f"Encontradas: {len(caminho)}"
                                f"Declarada: {contagem_declarada}"
                                f"Pessoa(s): {id_pessoa_atual} ")

                    if caminho:
                         pontos_por_pessoa[id_pessoa_atual] = caminho
                         id_pessoa_atual += 1

    except FileNotFoundError:
            print(f"Erro: Erro ao encontrar o arquivo: {arquivo}.")
            return None, None
    #retorna os dados lidos e processados se tudo occorreu bem
    return pontos_por_pessoa, pixels_por_metro

def desenhar ():
    #função de callback - sera chamada toda vez que o frame for redesenhado
        glClearColor(0.1, 0.1, 0.1, 1)
        glClear(GL_COLOR_BUFFER_BIT) #mesmo sendo 2d, é boa prática limpar o buffer 3d
        glPointSize(11)

        glBegin(GL_POINTS)
        for trajetoria in dados_globais.values():
            if trajetoria:
                pos_inicial = trajetoria[0]
                glColor3f(0.1, 1, 0.1)
                glVertex2f(pos_inicial[0], pos_inicial[1])
        glEnd()

        #futuramente encaixar o codigo das coordenadas
        glutSwapBuffers()

def main():

    global dados_globais, escala_global

    glutInit() #Inicializa o glut
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE) # sis. de cores RGBA / buffer duplo

    glutInitWindowSize(largura_window, altura_window) # tamanho inicial da janela
    glutInitWindowPosition(100, 100) # onde a janela vai aparece na tela

    window_id = glutCreateWindow("Trabalho de CG - Vicente Hofmeister")

    #CARREGMENTO DOS DADOS
    dados_globais, escala_global = data_load('Paths_D.txt', largura_window, altura_window)

    if dados_globais is None:
        return #encerra o programa se der problema
    
    #----------------area de debug no terminal-----------------

    print("-----------Dados do Paths_D.txt")
    print(f"Escala: {escala_global} p por metro")
    print(f"Caminhos encontrados: {len(dados_globais)}")
    for id_pessoa, trajetoria in dados_globais.items():
         print(f" Pessoa {id_pessoa}: {len(trajetoria)} pontos encontrados.")
    print("--------------------------")

    glutDisplayFunc(desenhar)
    print("Janela glut criada")

    glutMainLoop()


if __name__ == "__main__":
    main()
