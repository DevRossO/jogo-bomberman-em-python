import pygame
import sys
import time

usuario = input("Digite seu nome: ")

pygame.init()  

vazio = 0
parede = 1
obstaculo = 2
jogador = "J"
inimigo = "I"
inimigo2 = "H"
bomba = "B"

tamanho = 11
celula = 45

largura = tamanho * celula
altura = tamanho * celula

CORES = {
    vazio: (30, 160, 30),
    parede: (130, 130, 130),
    obstaculo: (180, 180, 180),
}

player_img = pygame.transform.scale(pygame.image.load("sprites/player.png"), (celula, celula))
enemy_img = pygame.transform.scale(pygame.image.load("sprites/enemy.gif"), (celula, celula))
enemy2_img = pygame.transform.scale(pygame.image.load("sprites/enemy2.png"), (celula, celula))
bomb_img = pygame.transform.scale(pygame.image.load("sprites/bomb.png"), (celula, celula))

def organizar_ranking():
    try:
        with open("ranking.txt", "r") as arquivo:
            linhas = arquivo.readlines()

        dados = []
        for linha in linhas:
            nome, tempo = linha.strip().split(",")
            tempo = float(tempo.replace(" seg", ""))
            dados.append((nome, tempo))

        dados.sort(key=lambda x: x[1])

        with open("ranking.txt", "w") as arquivo:
            for nome, tempo in dados:
                arquivo.write(f"{nome},{tempo:.2f} seg\n")

    except:
        pass

def salvar_ranking(nome, tempo):
     with open("ranking.txt", "a") as arquivo:
        arquivo.write(f"{nome},{tempo:.2f} segundos\n")

def encontrar_jogador():
    for y in range(tamanho):
        for x in range(tamanho):
            if tabuleiro[y][x] == jogador:
                return x, y
    return None

def inimigos_restantes():
    for linha in tabuleiro:
        if inimigo in linha or inimigo2 in linha:
            return True
    return False

def mostrar_mensagem_final(texto):
    fonte = pygame.font.SysFont("Arial", 50, bold=True)
    superficie = fonte.render(texto, True, (255, 255, 0))

    rect = superficie.get_rect(center=(largura // 2, altura // 2))

    tela.blit(superficie, rect)
    pygame.display.update()

    esperando = True

    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                esperando = False
    return

tabuleiro = [
    [parede, parede, parede, parede, parede, parede, parede, parede, parede, parede, parede],
    [parede, jogador, vazio, vazio, obstaculo, vazio, inimigo2, obstaculo, vazio, inimigo, parede],
    [parede, vazio, parede, vazio, parede, vazio, parede, vazio, parede, vazio, parede],
    [parede, vazio, inimigo2, vazio, obstaculo, vazio, vazio, vazio, vazio, vazio, parede],
    [parede, obstaculo, parede, vazio, parede, vazio, parede, vazio, parede, inimigo, parede],
    [parede, vazio, vazio, vazio, vazio, vazio, vazio, vazio, vazio, vazio, parede],
    [parede, inimigo, parede, vazio, parede, vazio, parede, vazio, parede, vazio, parede],
    [parede, vazio, vazio, inimigo2, obstaculo, vazio, vazio, vazio, vazio, vazio, parede],
    [parede, vazio, parede, vazio, parede, vazio, parede, vazio, parede, vazio, parede],
    [parede, inimigo, vazio, vazio, obstaculo, vazio, inimigo2, obstaculo, vazio, vazio, parede],
    [parede, parede, parede, parede, parede, parede, parede, parede, parede, parede, parede],
]

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Bomberman Python MVP")

tempo_bomba = None
pos_bomba = None

inicio = time.time()
rodando = True
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        if event.type == pygame.KEYDOWN:

            pos = encontrar_jogador()
            if not pos:
                continue

            x, y = pos
            novo_x, novo_y = x, y

            if event.key == pygame.K_UP:
                novo_y -= 1
            elif event.key == pygame.K_DOWN:
                novo_y += 1
            elif event.key == pygame.K_LEFT:
                novo_x -= 1
            elif event.key == pygame.K_RIGHT:
                novo_x += 1

            if tabuleiro[novo_y][novo_x] == vazio:
                tabuleiro[y][x] = vazio
                tabuleiro[novo_y][novo_x] = jogador

            if event.key == pygame.K_SPACE and pos_bomba is None:
                bx, by = x, y
                tabuleiro[by][bx] = bomba
                pos_bomba = (bx, by)
                tempo_bomba = pygame.time.get_ticks()

                direcoes = [(1,0), (-1,0), (0,1), (0,-1)]
                for dx, dy in direcoes:
                    nx, ny = x + dx, y + dy
                    if tabuleiro[ny][nx] == vazio:
                        tabuleiro[ny][nx] = jogador
                        break

    if tempo_bomba and pos_bomba:
        agora = pygame.time.get_ticks()

        if agora - tempo_bomba >= 2000:
            bx, by = pos_bomba

            explosoes = [
                (bx, by),
                (bx+1, by), (bx-1, by),
                (bx, by+1), (bx, by-1),
                (bx+1, by+1), (bx-1, by-1),
                (bx+1, by-1), (bx-1, by+1),
            ]

            for ex, ey in explosoes:
                if 0 <= ex < tamanho and 0 <= ey < tamanho:

                    if tabuleiro[ey][ex] == inimigo or tabuleiro[ey][ex] == inimigo2:
                        tabuleiro[ey][ex] = vazio

                    if tabuleiro[ey][ex] == obstaculo:
                        tabuleiro[ey][ex] = vazio

                    if tabuleiro[ey][ex] == jogador:
                        tempo_total = time.time() - inicio
                        mostrar_mensagem_final("Você morreu!")
                        salvar_ranking(usuario, tempo_total)
                        pygame.quit()
                        sys.exit()

            tabuleiro[by][bx] = vazio
            pos_bomba = None
            tempo_bomba = None

            if not inimigos_restantes():
                tempo_total = time.time() - inicio
                mostrar_mensagem_final("Você passou de fase!")
                salvar_ranking(usuario, tempo_total)
                pygame.quit()
                sys.exit()

    tela.fill((0, 0, 0))

    for y in range(tamanho):
        for x in range(tamanho):
            valor = tabuleiro[y][x]

            pygame.draw.rect(tela, CORES.get(vazio), (x * celula, y * celula, celula, celula))

            if valor == parede:
                pygame.draw.rect(tela, CORES[parede], (x * celula, y * celula, celula, celula))

            elif valor == obstaculo:
                pygame.draw.rect(tela, CORES[obstaculo], (x * celula, y * celula, celula, celula))

            elif valor == jogador:
                tela.blit(player_img, (x * celula, y * celula))

            elif valor == inimigo:
                tela.blit(enemy_img, (x * celula, y * celula))
            
            elif valor == inimigo2:
                tela.blit(enemy2_img, (x * celula, y * celula))

            elif valor == bomba:
                tela.blit(bomb_img, (x * celula, y * celula))

            pygame.draw.rect(tela, (20, 20, 20), (x * celula, y * celula, celula, celula), 1)

    pygame.display.flip()
fim = time.time()
tempo_total = fim - inicio

print(f"Jogador: {usuario} - Tempo total de jogo: {tempo_total:.2f} segundos")

salvar_ranking(usuario, tempo_total)

pygame.quit()
sys.exit()