import sys
import os
import pygame
import random

def recurso_caminho(rel_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, rel_path)

def nova_posicao_maca():
    return random.randint(0, largura - largura_maca), random.randint(0, altura - altura_maca)

def tela_game_over(mensagem, pontos):
    while True:
        tela.fill(BRANCO)
        texto = fonte.render(mensagem, True, VERMELHO)
        pontos_txt = fonte.render(f"Pontos: {pontos}", True, (0, 0, 0))
        opcao = fonte.render("Pressione R para reiniciar ou ESC para sair", True, (0, 0, 0))
        tela.blit(texto, (largura//2 - texto.get_width()//2, altura//2 - 60))
        tela.blit(pontos_txt, (largura//2 - pontos_txt.get_width()//2, altura//2))
        tela.blit(opcao, (largura//2 - opcao.get_width()//2, altura//2 + 60))
        pygame.display.update()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    return True
                elif evento.key == pygame.K_ESCAPE:
                    return False

def tela_proximo_nivel(novo_nivel):
    while True:
        tela.fill(BRANCO)
        texto = fonte.render(f"Você chegou no nível {novo_nivel}!", True, (0, 0, 0))
        continuar = fonte.render("Pressione C para continuar ou ESC para sair", True, (0, 0, 0))
        tela.blit(texto, (largura // 2 - texto.get_width() // 2, altura // 2 - 60))
        tela.blit(continuar, (largura // 2 - continuar.get_width() // 2, altura // 2 + 20))
        pygame.display.update()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_c:
                    return True
                elif evento.key == pygame.K_ESCAPE:
                    return False

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load(recurso_caminho("Paparazzi.mp3"))
pygame.mixer.music.play(-1)

largura, altura = 1280, 768
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo do Nanato")

BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)

personagem = pygame.image.load(recurso_caminho("monkey.png")).convert_alpha()
personagem = pygame.transform.scale(personagem, (95, 95))
largura_perso, altura_perso = personagem.get_size()

maca = pygame.image.load(recurso_caminho("maca.png")).convert_alpha()
maca = pygame.transform.scale(maca, (32, 32))
largura_maca, altura_maca = maca.get_size()
maca_x, maca_y = nova_posicao_maca()

inimigo = pygame.image.load(recurso_caminho("inimigo.png")).convert_alpha()
inimigo = pygame.transform.scale(inimigo, (65, 65))
inimigo_x, inimigo_y = 700, 500
velocidade_inimigo = 2

x, y = 100, 100
velocidade = 5

fonte = pygame.font.SysFont(None, 48)

fundos = [
    pygame.transform.scale(pygame.image.load(recurso_caminho("fundo1.png")).convert(), (largura, altura)),
    pygame.transform.scale(pygame.image.load(recurso_caminho("fundo2.png")).convert(), (largura, altura)),
    pygame.transform.scale(pygame.image.load(recurso_caminho("fundo3.png")).convert(), (largura, altura))
]
#Dados do jogador: Inicio
nivel = 1
macas_coletadas = 0
pontuacao = 0
fundo_atual = fundos[nivel - 1] if nivel <= len(fundos) else fundos[-1]
tela.blit(fundo_atual, (0, 0))

clock = pygame.time.Clock()

while True:
    fundo_atual = fundos[nivel - 1] if nivel <= len(fundos) else fundos[-1]
    tela.blit(fundo_atual, (0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]: x -= velocidade
    if teclas[pygame.K_RIGHT]: x += velocidade
    if teclas[pygame.K_UP]: y -= velocidade
    if teclas[pygame.K_DOWN]: y += velocidade

    # Movimento inimigo
    if inimigo_x < x: inimigo_x += velocidade_inimigo
    elif inimigo_x > x: inimigo_x -= velocidade_inimigo
    if inimigo_y < y: inimigo_y += velocidade_inimigo
    elif inimigo_y > y: inimigo_y -= velocidade_inimigo

    # Colisão com maçã
    if pygame.Rect(x, y, largura_perso, altura_perso).colliderect((maca_x, maca_y, largura_maca, altura_maca)):
        maca_x, maca_y = nova_posicao_maca()
        pontuacao += 100
        macas_coletadas += 1

        if macas_coletadas >= 10:
            if tela_proximo_nivel(nivel + 1):
                nivel += 1
                velocidade_inimigo += 1
                macas_coletadas = 0
                x, y = 100, 100
                inimigo_x, inimigo_y = 700, 500
                maca_x, maca_y = nova_posicao_maca()
            else:
                pygame.quit()
                sys.exit()

    # Fora da tela
    if x <= 0 or x + largura_perso >= largura or y <= 0 or y + altura_perso >= altura:
        if tela_game_over("Faleceu", pontuacao):
            x, y = 100, 100
            inimigo_x, inimigo_y = 700, 500
            pontuacao = 0
            macas_coletadas = 0
            nivel = 1
            velocidade_inimigo = 1
            maca_x, maca_y = nova_posicao_maca()
        else:
            pygame.quit()
            sys.exit()

    # Pegou o macaco
    if pygame.Rect(x, y, largura_perso, altura_perso).colliderect((inimigo_x, inimigo_y, 65, 65)):
        if tela_game_over("Pegou o Macaco!", pontuacao):
            x, y = 100, 100
            inimigo_x, inimigo_y = 700, 500
            pontuacao = 0
            macas_coletadas = 0
            nivel = 1
            velocidade_inimigo = 1
            maca_x, maca_y = nova_posicao_maca()
        else:
            pygame.quit()
            sys.exit()

    # HUD
    texto_pontos = fonte.render(f"Pontos: {pontuacao}", True, (0, 0, 0))
    texto_nivel = fonte.render(f"Nível: {nivel}", True, (0, 0, 0))
    tela.blit(texto_pontos, (20, 20))
    tela.blit(texto_nivel, (20, 70))

    tela.blit(maca, (maca_x, maca_y))
    tela.blit(personagem, (x, y))
    tela.blit(inimigo, (inimigo_x, inimigo_y))

    pygame.display.update()
    clock.tick(60)
