from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import re

def data_load(arquivo):
    #vai ler os dados do Paths_D.txt linha por linha
    pontos_por_pessoa = {}
    pixels_por_metro = {}

    try:
        with open(arquivo, 'r') as f:
            linhas = f.readlines()

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

                coordenadas_pessoas = re.findall(r'\((\d+), (\d+), (\d+)\)', linha)

                caminho = []
                for coord in coordenadas_pessoas:
                    x = int (coord[0])
                    y = int (coord[1])
                    caminho.append ((x, y))

                if caminho: #Só incrmenta se achou alguma coordenada
                    pontos_por_pessoa[id_pessoa_atual] = caminho
                    id_pessoa_atual += 1

    except FileNotFoundError:
            print(f"Erro: O arquivo: '{arquivo}' não encontrado.")
            return None, None

def desenhar ():
    #função de callback - sera chamada toda vez que o frame for redesenhado
        glClear(GL_COLOR_BUFFER_BIT) #mesmo sendo 2d, é boa prática limpar o buffer 3d
        #futuramente encaixar o codigo das coordenadas
        glutSwapBuffers()

def main():
    glutInit() #Inicializa o glut
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE) # sis. de cores RGBA / buffer duplo

    glutInitWindowSize(800, 600) # tamanho inicial da janela
    glutInitWindowPosition(100, 100) # onde a janela vai aparece na tela

    window_id = glutCreateWindow("Trabalho CG")

    glutDisplayFunc(desenhar) # regisrta a função de callback de desenho

    print("Janela GLUT criada.")
    glutMainLoop()


if __name__ == "__main__":
    main()
