import pygame                #importa a biblioteca pygame
import sys                   #importa a biblioteca system 
import math                  #importa biblioteca matematica

pygame.init()                #inicia a pygame

width = 960     #Define a largura da tela
height = 540    #Define a altura da tela

CorFundo = 75,0,130 #Cor de fundo em RGB

font = pygame.font.SysFont(None, 24) #inicaliza a fonte

black = 0, 0, 0         #cor preta
white = 255, 255, 255   #cor branca

tela = pygame.display.set_mode([width,height],0,32) #Define o modo da tela

centro = [(width-30)/2+15,(height-80)/2+15] #centro da messa

posicao = [(width-30)/2+15,(height-80)/2+15] #Posicao da bolinha

estado = 0 #variavel do estado do sistema
velocidade = 0.5 #velocidade
variacaodavelocidade = 0.0015 #variacao da velocidade para o estado 0

angulo = 0 #angulo
variacaodoangulo = 0.001    #Variacao do angulo

velocidademaxima = 3 #velocidade maxima da bola
posicaoinical, posicaofinal = [0,0],[0,0] #variavel pra desenhar a mira
desaceleracao = 1 #dessaceleracao da boa
variacaodadesaceleracao = 0.001 #velocidade com que a bola dessacelera
while 1: #enquanto infinito
    for event in pygame.event.get(): #para cada evento do pygame
        if event.type == pygame.QUIT: sys.exit() #se o evento for de fechar o programa sai do programa
        if event.type == pygame.KEYDOWN and estado < 2: #se o evento for de tecla apertada muda o estado do sistema se possivel
            estado=(estado+1)%4 #acumulador de zero a dois
    #====================================================================
    #mecanica
    #====================================================================
        #================================================================================
        #Estado 0: escolhe a força
        #================================================================================
    if estado == 0: #estado 0 (velocidade inicial da bola)
        velocidade = velocidade + variacaodavelocidade #acumulador para a velocidade inicial
        if velocidade >= 1: #se a velocidade for maior que 1
            velocidade = 1 #define a velocidade em 1
            variacaodavelocidade = -variacaodavelocidade #inverte a variação do acumulador
        elif velocidade <= 0: #se velocidade for menor que 0
            velocidade = 0 #define a velocidade em 0
            variacaodavelocidade = -variacaodavelocidade #inverte o aumulador
        tela.fill(CorFundo)#define o plano de fundo
        #================================================================================
        #Estado 1: escolhe o ângulo
        #================================================================================
    elif estado == 1: #estado 1 (angulo da tacada)
        angulo = angulo + variacaodoangulo #acumulador para a velocidade inicial
        if angulo >= 1: #se o angulo for maior que 1
            angulo = 0 #vira zero
        tela.fill(CorFundo) #limpa a tela
        posicaoinical = [15*math.sin(angulo*2*math.pi)+posicao[0],15*math.cos(angulo*2*math.pi)+posicao[1]] #posicao inicial da mira
        posicaofinal = [30*math.sin(angulo*2*math.pi)+posicao[0],30*math.cos(angulo*2*math.pi)+posicao[1]] #posicao final da mira
        #================================================================================
        #Estado 2: Define o vetor movimento
        #================================================================================
    elif estado == 2: #configura o vetor movimento
        tela.fill(CorFundo) #limpa a tela
        vetormovimento = [math.sin(angulo*2*math.pi),math.cos(angulo*2*math.pi)] #calcula o vetor movimeto a partir do angulo
        estado=(estado+1)%4 #muda o estado
        #================================================================================
        #Estado 3: Movimenta a bola
        #================================================================================
    elif estado == 3: #estado de movimento da bola
        tela.fill(CorFundo) #limpa a tela
        if desaceleracao > 0: #se a desaceleracao for maior que zero
            desaceleracao = desaceleracao - variacaodadesaceleracao #diminui a desaceleração em variacaodeaceleracao
        else: #se não 
            desaceleracao = 1 #reinicia a aceleracao
            estado=(estado+1)%4 #muda o estado
        #================================================================================
        #colisao
        #================================================================================
        pontocolisao = [posicao[0]+vetormovimento[0]*10,posicao[1]+vetormovimento[1]*10] #calcula o ponto de colisao da bola
        if pontocolisao[0] <= 15 or pontocolisao[0] >= 2*(width-30)/2+15: #se a bola bate no lado esquerdo ou direito 
            vetormovimento[0] = -vetormovimento[0] #o sentido do vetor movimento no eixo x muda o sinal 
        if pontocolisao[1] <= 15 or pontocolisao[1] >= 2*(height-80)/2+15: #se a bola bate no lado de cima ou de baixo
            vetormovimento[1] = -vetormovimento[1] #o sentido do vetor movimento no eixo y muda o sinal 
        posicao[0] = posicao[0] + velocidademaxima*velocidade*vetormovimento[0]*desaceleracao #a nova posicao é igual a antiga mais velocidademaxima*velocidade*desaceleracao* vetormovimento no eixo x
        posicao[1] = posicao[1] + velocidademaxima*velocidade*vetormovimento[1]*desaceleracao #a nova posicao é igual a antiga mais velocidademaxima*velocidade*desaceleracao* vetormovimento no eixo y
    #================================================================================
    #tela
    #================================================================================
        #================================================================================
        #Imprime a mesa
        #================================================================================
    pygame.draw.rect(tela,pygame.Color(139,69,19),(5,5,width-10,height-60)) #desenha a borda da mesa
    pygame.draw.rect(tela,pygame.Color(34,139,34),(15,15,(width-30),(height-80))) #desenha a borda da mesa
        #================================================================================
        #Se no estado 2 imprime a mira
        #================================================================================
    if estado == 1: #se esta no estado 1
        pygame.draw.line(tela,white,posicaoinical,posicaofinal,width=3) #desenha a linha da mira
        #================================================================================
        #imprime a barra de forca da tacada
        #================================================================================
    texto = font.render("Força da tacada: "+str(int(velocidade*100))+"%",True, black) #renderiza o texto
    cordabarra = int(velocidade*255),int((1-velocidade)*255),0 #calcula a cor da barra
    pygame.draw.rect(tela,white,(100-5,height-35-5,(width-400)*velocidade+200+10,25+10))#desenha o contorno branco da barra
    pygame.draw.rect(tela,cordabarra,(100,height-35,(width-400)*velocidade+200,25)) #desenha a barra
    tela.blit(texto, (120,height-30)) #escreve o texto da barra
        #================================================================================
        #imprime a bola
        #================================================================================
    pygame.draw.circle(tela,white,posicao,10) #desenha a bola

    pygame.display.flip() #atualiza a tela