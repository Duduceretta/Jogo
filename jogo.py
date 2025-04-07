import sys
import os
import pygame
import random

# Função que ajusta caminho para funcionar com PyInstaller
def recurso_caminho(rel_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, rel_path)

pygame.init()
pygame.mixer.init()

musica = recurso_caminho("Lady Gaga - Paparazzi (Audio).mp3")
pygame.mixer.music.load(Lady Gaga - Paparazzi (Audio).mp3)
pygame.mixer.music.play(-1)

largura, altura = 1024, 768
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo do Nanato")

# Cores
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)

# Imagens com caminho correto
personagem = pygame.image.load(recurso_caminho("monkey.png")).convert_alpha()
personagem = pygame.transform.scale(personagem, (95, 95))
largura_perso, altura_perso = personagem.get_size()

maca = pygame.image.load(recurso_caminho("maca.png")).convert_alpha()
maca = pygame.transform.scale(maca, (32, 32))
largura_maca, altura_maca = maca.get_size()

inimigo = pygame.image.load(recurso_caminho("inimigo.png")).convert_alpha()
inimigo = pygame.transform.scale(inimigo, (65, 65))
inimigo_x, inimigo_y = 700, 500
velocidade_inimigo = 2

x, y = 100, 100
velocidade = 5

def nova_posicao_maca():
    while True:
        x_m = random.randint(0, largura - largura_maca)
        y_m = random.randint(0, altura - altura_maca)
        if not pygame.Rect(x, y, largura_perso, altura_perso).colliderect((x_m, y_m, largura_maca, altura_maca)):
            return x_m, y_m

maca_x, maca_y = nova_posicao_maca()

fonte = pygame.font.SysFont(None, 48)

clock = pygame.time.Clock()
while True:
    tela.fill(BRANCO)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]: x -= velocidade
    if teclas[pygame.K_RIGHT]: x += velocidade
    if teclas[pygame.K_UP]: y -= velocidade
    if teclas[pygame.K_DOWN]: y += velocidade

    if inimigo_x < x: inimigo_x += velocidade_inimigo
    elif inimigo_x > x: inimigo_x -= velocidade_inimigo
    if inimigo_y < y: inimigo_y += velocidade_inimigo
    elif inimigo_y > y: inimigo_y -= velocidade_inimigo

    if pygame.Rect(x, y, largura_perso, altura_perso).colliderect((maca_x, maca_y, largura_maca, altura_maca)):
        maca_x, maca_y = nova_posicao_maca()

    if x <= 0 or x + largura_perso >= largura or y <= 0 or y + altura_perso >= altura:
        texto = fonte.render("Faleceu", True, VERMELHO)
        tela.blit(texto, (largura // 2 - 100, altura // 2))
        pygame.display.update()
        pygame.time.delay(2000)
        pygame.quit()
        sys.exit()

    if pygame.Rect(x, y, largura_perso, altura_perso).colliderect((inimigo_x, inimigo_y, 65, 65)):
        texto = fonte.render("Pegou o Macaco!", True, VERMELHO)
        tela.blit(texto, (largura // 2 - 150, altura // 2))
        pygame.display.update()
        pygame.time.delay(2000)
        pygame.quit()
        sys.exit()

    tela.blit(maca, (maca_x, maca_y))
    tela.blit(personagem, (x, y))
    tela.blit(inimigo, (inimigo_x, inimigo_y))

    pygame.display.update()
    clock.tick(60)
