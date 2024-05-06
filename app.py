import pygame
import random

# Definindo algumas constantes
DIMENSAO = 10
NUM_MINAS = 10
LARGURA_JANELA = 400
ALTURA_JANELA = 450

# Cores personalizadas
VERDE_CLARO = (45, 180, 105)
VERDE_ESCURO = (30, 130, 76)
VERDE_MUITO_ESCURO = (10, 60, 35)
CINZA_CLARO = (192, 192, 192)
CINZA_ESCURO = (211, 211, 211)
VERMELHO = (255, 0, 0)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Variáveis globais
tabuleiro_real = None
tabuleiro_visivel = None
game_over = False
tempo_inicio = 0
tempo_pausado = True
tempo_atual = 0 

def criar_tabuleiro():
    # Cria um tabuleiro vazio
    tabuleiro = [[0 for _ in range(DIMENSAO)] for _ in range(DIMENSAO)]

    # Distribui as minas aleatoriamente
    minas_colocadas = 0
    while minas_colocadas < NUM_MINAS:
        row = random.randint(0, DIMENSAO - 1)
        col = random.randint(0, DIMENSAO - 1)
        if tabuleiro[row][col] != '*':
            tabuleiro[row][col] = '*'
            minas_colocadas += 1

    # Calcula os números de minas ao redor de cada célula
    for r in range(DIMENSAO):
        for c in range(DIMENSAO):
            if tabuleiro[r][c] == '*':
                continue
            count = 0
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < DIMENSAO and 0 <= nc < DIMENSAO and tabuleiro[nr][nc] == '*':
                        count += 1
            tabuleiro[r][c] = count

    return tabuleiro

def revelar_celula(tabuleiro_visivel, tabuleiro_real, row, col):
    global game_over, tempo_pausado
    if tabuleiro_visivel[row][col] != '-':
        return True

    # Revela a célula
    tabuleiro_visivel[row][col] = tabuleiro_real[row][col]
    if tabuleiro_real[row][col] == '*':
        # Se uma mina foi revelada, jogo termina e pausa o tempo
        game_over = True
        tempo_pausado = True
    elif tabuleiro_real[row][col] == 0:
        # Se a célula revelada for 0, revela recursivamente suas adjacências
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < DIMENSAO and 0 <= nc < DIMENSAO:
                    revelar_celula(tabuleiro_visivel, tabuleiro_real, nr, nc)

def verificar_vitoria(tabuleiro_visivel, tabuleiro_real):
    for r in range(DIMENSAO):
        for c in range(DIMENSAO):
            if tabuleiro_real[r][c] == '*':
                if tabuleiro_visivel[r][c] != 'X':
                    return False 
            elif tabuleiro_real[r][c] != '*':
                if tabuleiro_visivel[r][c] == '-':
                    return False  
    return True

def reiniciar_jogo():
    global tabuleiro_real, tabuleiro_visivel, game_over, tempo_inicio, tempo_pausado, tempo_atual
    tabuleiro_real = criar_tabuleiro()
    tabuleiro_visivel = [['-' for _ in range(DIMENSAO)] for _ in range(DIMENSAO)]
    game_over = False
    tempo_pausado = True
    tempo_atual = 0

def desenhar_texto_centralizado(tela, texto, fonte, cor, x, y):
    texto_surface = fonte.render(texto, True, cor)
    texto_rect = texto_surface.get_rect(center=(x, y))
    tela.blit(texto_surface, texto_rect)

def main():
    global game_over, tempo_inicio, tempo_pausado, tempo_atual
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
    pygame.display.set_caption('Campo Minado')

    fonte = pygame.font.SysFont('comicsansms', 24)

    reiniciar_jogo()  # Reinicia o jogo

    # Define o tamanho do layout do jogo
    tamanho_layout = min(LARGURA_JANELA, ALTURA_JANELA - 50)
    margem = 20

    # Define o tamanho e posição do tabuleiro dentro do layout
    tamanho_tabuleiro = tamanho_layout - 2 * margem
    pos_tabuleiro_x = (LARGURA_JANELA - tamanho_tabuleiro) // 2
    pos_tabuleiro_y = margem + 50

    rodando = True
    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if pos_tabuleiro_x <= mouse_x < pos_tabuleiro_x + tamanho_tabuleiro and pos_tabuleiro_y <= mouse_y < pos_tabuleiro_y + tamanho_tabuleiro:
                    # Cálculo das coordenadas no tabuleiro
                    col = (mouse_x - pos_tabuleiro_x) // (tamanho_tabuleiro // DIMENSAO)
                    row = (mouse_y - pos_tabuleiro_y) // (tamanho_tabuleiro // DIMENSAO)

                    if 0 <= row < DIMENSAO and 0 <= col < DIMENSAO and not game_over:
                        if tempo_pausado:
                            tempo_inicio = pygame.time.get_ticks()
                            tempo_pausado = False
                        
                        if event.button == 1:  # Botão esquerdo do mouse (revelar célula)
                            revelar_celula(tabuleiro_visivel, tabuleiro_real, row, col)

                        elif event.button == 3:  # Botão direito do mouse (marcar com X)
                            if tabuleiro_visivel[row][col] == '-':
                                tabuleiro_visivel[row][col] = 'X'
                            elif tabuleiro_visivel[row][col] == 'X':
                                tabuleiro_visivel[row][col] = '-'

                        if verificar_vitoria(tabuleiro_visivel, tabuleiro_real):
                            game_over = True
                            tempo_pausado = True  # Pausa o tempo ao final do jogo

                # Verifica se o botão de reiniciar foi clicado
                if LARGURA_JANELA // 2 - 50 <= mouse_x <= LARGURA_JANELA // 2 + 50 and 10 <= mouse_y <= 40:
                    reiniciar_jogo()

        # Desenha o tabuleiro na tela
        tela.fill(VERDE_MUITO_ESCURO)

        tamanho_celula = tamanho_tabuleiro // DIMENSAO
        for r in range(DIMENSAO):
            for c in range(DIMENSAO):
                if (r + c) % 2 == 0:
                    cor_celula = VERDE_CLARO if tabuleiro_visivel[r][c] == '-' else CINZA_CLARO
                else:
                    cor_celula = VERDE_ESCURO if tabuleiro_visivel[r][c] == '-' else CINZA_ESCURO

                pygame.draw.rect(tela, cor_celula, (pos_tabuleiro_x + c * tamanho_celula, pos_tabuleiro_y + r * tamanho_celula, tamanho_celula, tamanho_celula))

                if tabuleiro_visivel[r][c] != '-' and tabuleiro_visivel[r][c] != ' ' and tabuleiro_visivel[r][c] != 0:
                    texto = str(tabuleiro_visivel[r][c])
                    texto_renderizado = fonte.render(texto, True, (0, 0, 0))
                    texto_rect = texto_renderizado.get_rect(center=(pos_tabuleiro_x + c * tamanho_celula + tamanho_celula // 2, pos_tabuleiro_y + r * tamanho_celula + tamanho_celula // 2))
                    tela.blit(texto_renderizado, texto_rect)

                if tabuleiro_visivel[r][c] == 'X':
                    texto_x = fonte.render("X", True, VERMELHO)
                    texto_rect_x = texto_x.get_rect(center=(pos_tabuleiro_x + c * tamanho_celula + tamanho_celula // 2, pos_tabuleiro_y + r * tamanho_celula + tamanho_celula // 2))
                    tela.blit(texto_x, texto_rect_x)

        # Desenha a barra superior, com o botão de reiniciar, temporizador e quantidade de minas no jogo
        pygame.draw.rect(tela, VERDE_ESCURO, (0, 0, LARGURA_JANELA, 50))
        texto_minas = fonte.render(f'Minas: {NUM_MINAS}', True, BRANCO)
        if not tempo_pausado and not game_over:
            tempo_atual = (pygame.time.get_ticks() - tempo_inicio) // 1000
        texto_tempo = fonte.render(f'Tempo: {tempo_atual}s', True, BRANCO)
        texto_reiniciar = fonte.render('Reiniciar', True, BRANCO)
        tela.blit(texto_minas, (10, 10))
        tela.blit(texto_tempo, (LARGURA_JANELA - 10 - texto_tempo.get_width(), 10))
        pygame.draw.rect(tela, VERDE_MUITO_ESCURO, (LARGURA_JANELA // 2 - 60, 10, 120, 30))
        texto_reiniciar_rect = texto_reiniciar.get_rect(center=(LARGURA_JANELA // 2, 25))
        tela.blit(texto_reiniciar, texto_reiniciar_rect)

        # Verifica condição de vitória
        if game_over:
            if verificar_vitoria(tabuleiro_visivel, tabuleiro_real):
                texto_vitoria = 'Você Ganhou!'
            else:
                texto_vitoria = 'Fim de Jogo'

            # Desenha retângulo preto em torno do texto de fim de jogo
            pygame.draw.rect(tela, PRETO, (100, 200, 200, 50))
            desenhar_texto_centralizado(tela, texto_vitoria, fonte, BRANCO, LARGURA_JANELA // 2, ALTURA_JANELA // 2)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()