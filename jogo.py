import random
import pygame
import sys

pygame.init()

vazio = 0
parede = 1
obstaculo = 2
jogador = "J"
inimigo = "I"
bomba = "B"
tamanho = 11
celula = 45

largura = tamanho * celula
altura = tamanho * celula

CORES = {
    vazio: (200, 200, 200),    
    parede: (100, 100, 100),   
    obstaculo: (150, 75, 0),   
    jogador: (0, 0, 255),      
    inimigo: (255, 0, 0),      
    bomba: (0, 0, 0),          
}

tabuleiro = [[vazio] * tamanho for _ in range(tamanho)]
tabuleiro[1][7] = jogador
tabuleiro[2][2] = obstaculo
tabuleiro[6][2] = parede
tabuleiro[4][7] = inimigo
tabuleiro[6][6] = bomba

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("💣 Bomberman")

rodando = True
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    for y in range(tamanho):
        for x in range(tamanho):
            valor = tabuleiro[y][x]
            cor = CORES.get(valor, (255, 255, 255))
            pygame.draw.rect(tela, cor, (x * celula, y * celula, celula, celula))
            pygame.draw.rect(tela, (0, 0, 0), (x * celula, y * celula, celula, celula), 1)

    pygame.display.flip()

pygame.quit()
sys.exit()