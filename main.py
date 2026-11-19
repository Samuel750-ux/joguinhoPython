import os
import random
import pygame
from config import LARGURA, ALTURA, FPS, TITULO, PRETO, BRANCO
from src.player import Jogador
from src.levels import carregar_fase
from src.ui import Interface

def carregar_som(nome_arquivo):
    caminho = os.path.join("assets", "sounds", nome_arquivo)
    if os.path.exists(caminho):
        return pygame.mixer.Sound(caminho)
    return None

def main():
    pygame.init()
    pygame.mixer.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption(TITULO)
    relogio = pygame.time.Clock()

    som_tiro = carregar_som("shoot.wav")
    som_explosao = carregar_som("explosion.wav")
    caminho_musica = os.path.join("assets", "sounds", "bg_music.ogg")
    if os.path.exists(caminho_musica):
        pygame.mixer.music.load(caminho_musica)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

    estrelas = [[random.randint(0, LARGURA), random.randint(0, ALTURA), random.randint(1, 3)] for _ in range(60)]

    ui = Interface()
    estado = "INICIO"
    pontos = 0
    fase = 1

    jogador = Jogador()
    grupo_jogador = pygame.sprite.GroupSingle(jogador)
    grupo_inimigos = pygame.sprite.Group()
    grupo_chefao = pygame.sprite.GroupSingle()
    tiros_jogador = pygame.sprite.Group()
    tiros_inimigos = pygame.sprite.Group()

    def reiniciar_jogo():
        nonlocal pontos, fase, estado
        pontos = 0
        fase = 1
        estado = "JOGANDO"
        jogador.vidas = 3
        jogador.rect.midbottom = (LARGURA // 2, ALTURA - 20)
        tiros_jogador.empty()
        tiros_inimigos.empty()
        carregar_fase(fase, grupo_inimigos, grupo_chefao)

    rodando = True
    while rodando:
        relogio.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if evento.type == pygame.KEYDOWN:
                if estado == "INICIO" and evento.key == pygame.K_RETURN:
                    reiniciar_jogo()
                elif estado in ("GAME_OVER", "VITORIA") and evento.key == pygame.K_r:
                    reiniciar_jogo()

        tela.fill(PRETO)
        for estrela in estrelas:
            estrela[1] += estrela[2]
            if estrela[1] > ALTURA:
                estrela[1] = 0
                estrela[0] = random.randint(0, LARGURA)
            pygame.draw.circle(tela, BRANCO, (estrela[0], estrela[1]), 1)

        if estado == "INICIO":
            ui.desenhar_tela_inicial(tela)

        elif estado == "JOGANDO":
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_SPACE]:
                jogador.atirar(tiros_jogador, som_tiro)

            grupo_jogador.update()
            grupo_inimigos.update()
            grupo_chefao.update()
            tiros_jogador.update()
            tiros_inimigos.update()

            for inimigo in grupo_inimigos:
                inimigo.tentar_atirar(tiros_inimigos)
                if inimigo.rect.bottom >= jogador.rect.top:
                    estado = "GAME_OVER"

            if grupo_chefao.sprite:
                grupo_chefao.sprite.tentar_atirar(tiros_inimigos)

            acertos = pygame.sprite.groupcollide(grupo_inimigos, tiros_jogador, True, True)
            for inimigo_atingido in acertos:
                pontos += inimigo_atingido.pontos
                if som_explosao:
                    som_explosao.play()

            if grupo_chefao.sprite:
                acertos_boss = pygame.sprite.spritecollide(grupo_chefao.sprite, tiros_jogador, True)
                for _ in acertos_boss:
                    grupo_chefao.sprite.vida -= 1
                    if grupo_chefao.sprite.vida <= 0:
                        pontos += grupo_chefao.sprite.pontos
                        if som_explosao:
                            som_explosao.play()
                        grupo_chefao.empty()

            if pygame.sprite.spritecollide(jogador, tiros_inimigos, True):
                jogador.vidas -= 1
                if som_explosao:
                    som_explosao.play()
                if jogador.vidas <= 0:
                    estado = "GAME_OVER"

            if len(grupo_inimigos) == 0 and len(grupo_chefao) == 0:
                if fase < 3:
                    fase += 1
                    tiros_jogador.empty()
                    tiros_inimigos.empty()
                    carregar_fase(fase, grupo_inimigos, grupo_chefao)
                else:
                    estado = "VITORIA"

            grupo_jogador.draw(tela)
            grupo_inimigos.draw(tela)
            grupo_chefao.draw(tela)
            tiros_jogador.draw(tela)
            tiros_inimigos.draw(tela)

            if grupo_chefao.sprite:
                grupo_chefao.sprite.desenhar_barra_vida(tela)

            ui.desenhar_hud(tela, pontos, jogador.vidas, fase)

        elif estado in ("GAME_OVER", "VITORIA"):
            ui.desenhar_game_over(tela, pontos, vitoria=(estado == "VITORIA"))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()