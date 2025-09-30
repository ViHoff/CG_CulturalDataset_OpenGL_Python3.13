from OpenGL.GL import *
from OpenGL.GLUT import *
import re
import math

#----------------------------------------------variaveis globais--------------------------------------
dados_globais = []
escala_global = 1
largura_window, altura_window = 1280, 720
proximidade = 0.05 # distancia para ser considerado proximo, e assim mudar de cor

#------------variaveis globais de animação
frame_atual = 0
#1000ms / 30fps = 33ms
velocidade_animacao = 33 #em ms
max_frames = 0
#------------variaveis do jogador "personagem"
pos_jogador = [0.0, 0.0]
velocidade_personagem = 0.02
teclas_ativadas = set()


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
                         #converter para float
                         x = float(coord[0])
                         y = float(coord[1])

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

def testar_proximidade():

    #restarta todos os pontos para false
    for ponto in dados_globais:
        ponto['esta_perto'] = False

    #testa proximidade
    for i in range(len(dados_globais)):
        for j in range(i+1, len(dados_globais)):
            ponto_1 = dados_globais[i]
            ponto_2 = dados_globais[j]

            dist = math.hypot(ponto_1['pos_atual'][0] - ponto_2['pos_atual'][0],
                              ponto_1['pos_atual'][1] - ponto_2['pos_atual'][1])

            if dist < proximidade:
                ponto_1['esta_perto'] = True
                ponto_2['esta_perto'] = True

    #calcula a distancia com o usuário
    for ponto in dados_globais:
        dist = math.hypot(ponto['pos_atual'][0] - pos_jogador[0],
                          ponto ['pos_atual'][1] - pos_jogador[1])
        if dist < proximidade:
            ponto['esta_perto'] = True

def desenhar ():
    #função de callback - sera chamada toda vez que o frame for redesenhado

        testar_proximidade()
        glClearColor(0.1, 0.1, 0.1, 1)
        glClear(GL_COLOR_BUFFER_BIT)
        glPointSize(11)
        glBegin(GL_POINTS)

        for ponto in dados_globais:
            if ponto['esta_perto']:
                glColor3f(1, 0.1, 0.1)
            else:
                glColor3f(0.1, 1, 0.1)

            glVertex2f(ponto['pos_atual'][0], ponto['pos_atual'][1])

        #desenha jogador
        glColor3f(0.1, 0.1, 1)
        glVertex2f(pos_jogador[0], pos_jogador[1])

        glEnd()
        glutSwapBuffers()

def atualizar(valor):
    global frame_atual, pos_jogador

    #----------------------movimentacao do usuario "personagem"-----------------

    if b'w' in teclas_ativadas:
        pos_jogador[1] += velocidade_personagem

    if b's' in teclas_ativadas:
        pos_jogador[1] -= velocidade_personagem

    if b'a' in teclas_ativadas:
        pos_jogador[0] -= velocidade_personagem

    if b'd' in teclas_ativadas:
        pos_jogador[0] += velocidade_personagem

    #--------------------------movimentacao dataset------------------------------------

    frame_atual += 1
    #reinicia o contador global quando atinge max_frames
    if max_frames > 0:
        frame_atual = frame_atual % max_frames

    for ponto in dados_globais:
        if ponto['trajetoria']:
            indice = frame_atual % len(ponto['trajetoria'])
            ponto['pos_atual'] = ponto['trajetoria'][indice]

    glutPostRedisplay() #??
    #essa e a funcao responsavel pelo loop, daqui a X milissegundos usa a mesma funcao denovo
    glutTimerFunc(velocidade_animacao, atualizar, 0)

#funcao chamada quando uma tecla eh pressionada
def pressed_key(key, x, y):
    teclas_ativadas.add(key)

#funcao chamada quando uma tecla eh solta
def unpressed_key(key, x, y):
    teclas_ativadas.discard(key)

def main():

    global dados_globais, escala_global, max_frames

    glutInit() #Inicializa o glut
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE) # sis. de cores RGBA / buffer duplo
    glutInitWindowSize(largura_window, altura_window) # tamanho inicial da janela
    glutInitWindowPosition(100, 100) # onde a janela vai aparece na tela
    window_id = glutCreateWindow("Visualizador 2D - Animação Completa".encode('utf-8'))

    #CARREGMENTO DOS DADOS
    dados_carregados, escala_global = data_load('Paths_D.txt', largura_window, altura_window)

    if dados_carregados is None:
        return #encerra o programa se der problema

    for trajetoria in dados_carregados.values():
        #cria um dic pra cada ponto
        novo_ponto = {
            'trajetoria': trajetoria,
            'pos_atual': trajetoria[0],
            'esta_perto': False
        }
        dados_globais.append(novo_ponto)

    if dados_globais:
        max_frames = max(len(p['trajetoria']) for p in dados_globais)
    
    #----------------area de debug no terminal-----------------

    print("-----------Dados do Paths_D.txt")
    print(f"Escala: {escala_global} p por metro")
    print(f"Caminhos encontrados: {len(dados_globais)}")
    print("--------------------------")

    #loop
    glutDisplayFunc(desenhar)
    glutTimerFunc(velocidade_animacao, atualizar, 0)

    #inputs do telcado
    glutKeyboardFunc(pressed_key)
    glutKeyboardUpFunc(unpressed_key)

    print("Janela glut criada")

    glutMainLoop()

if __name__ == "__main__":
    main()
