import os
import random
import pygame
from config import LARGURA, VERMELHO_CHEFAO, AMARELO_TIRO, BRANCO
from src.projectile import Projetil

class Chefao(pygame.sprite.Sprite):
    def __init__(self, vida_maxima=30):
        super().__init__()
        caminho_img = os.path.join("assets", "images", "boss.png")

        if os.path.exists(caminho_img):
            self.image = pygame.image.load(caminho_img).convert_alpha()
            self.image = pygame.transform.scale(self.image, (140, 90))
        else:
            self.image = pygame.Surface((130, 80), pygame.SRCALPHA)
            pygame.draw.rect(self.image, VERMELHO_CHEFAO, (15, 10, 100, 50))
            pygame.draw.rect(self.image, AMARELO_TIRO, (0, 25, 130, 20))
            pygame.draw.rect(self.image, BRANCO, (45, 20, 40, 15))

        self.rect = self.image.get_rect(midtop=(LARGURA // 2, 50))
        self.vida_maxima = vida_maxima
        self.vida = vida_maxima
        self.velocidade_x = 3
        self.pontos = 2000

    def update(self):
        self.rect.x += self.velocidade_x
        if self.rect.right >= LARGURA - 20 or self.rect.left <= 20:
            self.velocidade_x *= -1

    def tentar_atirar(self, grupo_tiros_inimigos):
        if random.random() < 0.03:
            for offset in (-40, 0, 40):
                tiro = Projetil(self.rect.centerx + offset, self.rect.bottom, 6, eh_jogador=False)
                grupo_tiros_inimigos.add(tiro)

    def desenhar_barra_vida(self, tela):
        largura_barra = 200
        altura_barra = 14
        x = (LARGURA - largura_barra) // 2
        y = 15
        proporcao = max(0, self.vida / self.vida_maxima)
        pygame.draw.rect(tela, (80, 80, 80), (x, y, largura_barra, altura_barra))
        pygame.draw.rect(tela, VERMELHO_CHEFAO, (x, y, int(largura_barra * proporcao), altura_barra))
        pygame.draw.rect(tela, BRANCO, (x, y, largura_barra, altura_barra), 2)