import pygame
import random

# Inicializando o Pygame
pygame.init()

# Dimensões da tela
largura = 1280
altura = 720

# Configurando a tela
screen = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Meu jogo em Python')

# Carregando e ajustando o fundo
bg_original = pygame.image.load('image/cenario.jpg').convert_alpha()
bg = pygame.transform.scale(bg_original, (largura * 2, altura))

# Carregando e ajustando as imagens dos personagens
alien = pygame.image.load('image/nave.png').convert_alpha()
alien = pygame.transform.scale(alien, (100, 100))
alien = pygame.transform.rotate(alien, -90)  # Gira a nave para o lado

playerImg = pygame.image.load('image/inimigo.png').convert_alpha()
playerImg = pygame.transform.scale(playerImg, (50, 50))
playerImg = pygame.transform.rotate(playerImg, -90)  # Ajusta a orientação do inimigo

# Carregando e ajustando a imagem do míssil
missil = pygame.image.load('image/missil.png').convert_alpha()
missil = pygame.transform.scale(missil, (20, 10))  # Ajuste o tamanho do míssil para ser menor
missil = pygame.transform.rotate(missil, -45)

# Inicializando variáveis do míssil
pos_x_missil = -50  # Começa fora da tela
pos_y_missil = -25
vel_x_missil = 10  # Velocidade do míssil
disparado = False  # Flag para controlar o disparo do míssil

# Inicializando a variável 'rodando'
rodando = True
jogo_ativo = True  # Flag para controlar o estado do jogo

# Posições iniciais dos personagens
x_pos = 0
pos_player_x = 100  # Posição inicial do jogador no eixo X
pos_player_y = 100  # Posição inicial do jogador no eixo Y

# Lista de inimigos
num_inimigos = 3
inimigos = []
for _ in range(num_inimigos):
    inimigo_x = largura + random.randint(0, 200)
    inimigo_y = random.randint(0, altura - playerImg.get_height())
    inimigos.append([inimigo_x, inimigo_y, 4, 2])  # x, y, velocidade_x, velocidade_y

# Lista de obstáculos
num_obstaculos = 5
obstaculos = []
for _ in range(num_obstaculos):
    obstaculo_x = largura + random.randint(0, 300)
    obstaculo_y = random.randint(0, altura - 50)
    obstaculos.append([obstaculo_x, obstaculo_y])

# Inicializando o placar
pontos = 0
font = pygame.font.SysFont(None, 36)

# Inicializando o temporizador
tempo_inicio = pygame.time.get_ticks()
tempo_limite = 60 * 1000  # 1 minuto em milissegundos

# Controlando a taxa de atualização
clock = pygame.time.Clock()

# Velocidade do movimento do fundo (pixels por frame)
velocidade_fundo = 4

# Velocidade do movimento do jogador (pixels por frame)
velocidade_jogador = 4

# Função para verificar colisão
def verificar_colisao(rect1, rect2):
    return rect1.colliderect(rect2)

# Função para respawn do inimigo
def respawn():
    x = largura  # Começa fora da tela à direita
    y = random.randint(0, altura - playerImg.get_height())  # Posição aleatória dentro da tela
    return [x, y]

# Função para verificar colisão com obstáculos
def verificar_colisao_obstaculo(rect1, obstaculos):
    for obstaculo in obstaculos:
        obstaculo_rect = pygame.Rect(obstaculo[0], obstaculo[1], 50, 50)  # Tamanho do obstáculo
        if rect1.colliderect(obstaculo_rect):
            return True
    return False

# Função para mostrar a tela de Game Over
def tela_game_over():
    screen.fill((0, 0, 0))  # Tela preta
    texto_game_over = font.render('Game Over! Pressione R para Reiniciar ou Q para Sair', True, (255, 0, 0))
    screen.blit(texto_game_over, (largura // 4, altura // 2))
    pygame.display.update()

# Função para mostrar a tela de Vitória
def tela_vitoria():
    screen.fill((0, 0, 0))  # Tela preta
    texto_vitoria = font.render(f'Parabéns! Sua Pontuação Final: {pontos}', True, (0, 255, 0))
    screen.blit(texto_vitoria, (largura // 4, altura // 2))
    pygame.display.update()

# Função para desenhar os obstáculos
def desenhar_obstaculos():
    for obstaculo in obstaculos:
        pygame.draw.rect(screen, (255, 0, 0), (obstaculo[0], obstaculo[1], 50, 50))  # Desenha obstáculos em vermelho

# Função para resetar o jogo
def resetar_jogo():
    global pos_player_x, pos_player_y, pos_x_missil, pos_y_missil, disparado, pontos
    global inimigos, obstaculos, tempo_inicio, jogo_ativo
    pos_player_x = 100
    pos_player_y = 100
    pos_x_missil = -50
    pos_y_missil = -25
    disparado = False
    pontos = 0
    inimigos = []
    for _ in range(num_inimigos):
        inimigo_x = largura + random.randint(0, 200)
        inimigo_y = random.randint(0, altura - playerImg.get_height())
        inimigos.append([inimigo_x, inimigo_y, 4, 2])  # x, y, velocidade_x, velocidade_y
    obstaculos = []
    for _ in range(num_obstaculos):
        obstaculo_x = largura + random.randint(0, 300)
        obstaculo_y = random.randint(0, altura - 50)
        obstaculos.append([obstaculo_x, obstaculo_y])
    tempo_inicio = pygame.time.get_ticks()
    jogo_ativo = True

while rodando:
    if jogo_ativo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    resetar_jogo()
                if event.key == pygame.K_q:
                    rodando = False

        # Movendo o fundo
        x_pos -= velocidade_fundo
        if x_pos <= -largura:
            x_pos = 0

        # Controle do movimento do jogador
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP] and pos_player_y > 0:
            pos_player_y -= velocidade_jogador
        if teclas[pygame.K_DOWN] and pos_player_y < altura - alien.get_height():
            pos_player_y += velocidade_jogador

        # Controle do movimento do míssil
        if teclas[pygame.K_SPACE] and not disparado:
            pos_x_missil = pos_player_x + alien.get_width()  # Ajuste para disparar a partir da frente da nave
            pos_y_missil = pos_player_y + (alien.get_height() / 2) - (missil.get_height() / 2)
            disparado = True
        
        if disparado:
            pos_x_missil += vel_x_missil
            if pos_x_missil > largura:
                disparado = False
                pos_x_missil = -50  # Posiciona o míssil fora da tela

        # Movimentação dos inimigos e verificar limites
        for inimigo in inimigos:
            inimigo[0] -= inimigo[2]  # Atualiza a posição X
            inimigo[1] += inimigo[3]  # Atualiza a posição Y

            if inimigo[0] < -playerImg.get_width():
                inimigo[0], inimigo[1] = respawn()
            
            if inimigo[1] <= 0 or inimigo[1] >= altura - playerImg.get_height():
                inimigo[3] *= -1  # Muda a direção vertical

        # Verificar colisão entre o míssil e os inimigos
        for inimigo in inimigos:
            retangulo_inimigo = pygame.Rect(inimigo[0], inimigo[1], playerImg.get_width(), playerImg.get_height())
            retangulo_missil = pygame.Rect(pos_x_missil, pos_y_missil, missil.get_width(), missil.get_height())
            
            if verificar_colisao(retangulo_missil, retangulo_inimigo):
                print("Colisão detectada com o inimigo!")
                pontos += 10
                inimigo[0], inimigo[1] = respawn()
                disparado = False
                pos_x_missil = -50  # Posiciona o míssil fora da tela

        # Verificar colisão entre a nave e os inimigos
        retangulo_nave = pygame.Rect(pos_player_x, pos_player_y, alien.get_width(), alien.get_height())
        for inimigo in inimigos:
            retangulo_inimigo = pygame.Rect(inimigo[0], inimigo[1], playerImg.get_width(), playerImg.get_height())
            if verificar_colisao(retangulo_nave, retangulo_inimigo):
                jogo_ativo = False
                break

        # Verificar colisão entre a nave e os obstáculos
        if verificar_colisao_obstaculo(retangulo_nave, obstaculos):
            jogo_ativo = False

        # Verificar o tempo
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - tempo_inicio >= tempo_limite:
            if jogo_ativo:  # Se o tempo acabar e o jogador não morreu
                tela_vitoria()
                pygame.display.update()
                pygame.time.wait(3000)  # Espera 3 segundos antes de permitir a reinicialização
                resetar_jogo()
            else:
                tela_game_over()
                pygame.display.update()
                pygame.time.wait(3000)  # Espera 3 segundos antes de permitir a reinicialização
                resetar_jogo()

        # Atualizando a tela
        screen.blit(bg, (x_pos, 0))
        screen.blit(bg, (x_pos + largura, 0))
        screen.blit(alien, (pos_player_x, pos_player_y))
        for inimigo in inimigos:
            screen.blit(playerImg, (inimigo[0], inimigo[1]))
        desenhar_obstaculos()
        if disparado:
            screen.blit(missil, (pos_x_missil, pos_y_missil))

        # Atualiza o placar
        texto_pontos = font.render(f'Pontuação: {pontos}', True, (255, 255, 255))
        screen.blit(texto_pontos, (10, 10))

        tempo_restante = max(0, tempo_limite - (tempo_atual - tempo_inicio)) // 1000
        texto_tempo = font.render(f'Tempo Restante: {tempo_restante} s', True, (255, 255, 255))
        screen.blit(texto_tempo, (10, 50))

        pygame.display.update()

    else:
        tela_game_over()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    resetar_jogo()
                if event.key == pygame.K_q:
                    rodando = False

    clock.tick(60)  # 60 FPS

pygame.quit()
