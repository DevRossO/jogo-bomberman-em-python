import random

print("💣=======BOMBERMAN======💣")

vazio = 0
parede = 1
obstaculo = 2
jogador = "j"
inimigo = "I"
bomba = "B"
tamanho  = 9

tabuleiro = [[0] * tamanho for i in range(tamanho)]

obstaculos = "1"
jogador = "J"

alternar = random.randint(0, tamanho - 1)

for i in range (0, tamanho):
    print(tabuleiro[i])