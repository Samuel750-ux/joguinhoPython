import os
import random
import pygame
from config import LARGURA, VERDE_ALIEN, ROXO_ALIEN, PRETO
from src.projectile import Projetil

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo=1, velocidade=2):
        super().__init__()
        self.tipo = tipo
        self.pontos = 100 if tipo == 1 else 200
        caminho_img = os.path.join("assets", "images", f"enemy_{tipo}.png")

        if os.path.exists(caminho_img):
            self.image = pygame.image.load(caminho_img).convert_alpha()
            self.image = pygame.transform.scale(self.image, (40, 32))
        else:
            cor = VERDE_ALIEN if tipo == 1 else ROXO_ALIEN
            self.image = pygame.Surface((36, 28), pygame.SRCALPHA)
            pygame.draw.rect(self.image, cor, (4, 4, 28, 18))
            pygame.draw.rect(self.image, cor, (0, 10, 36, 8))
            pygame.draw.rect(self.image, PRETO, (8, 8, 5, 5))
            pygame.draw.rect(self.image, PRETO, (23, 8, 5, 5))

        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocidade_x = velocidade

    def update(self):
        self.rect.x += self.velocidade_x
        if self.rect.right >= LARGURA - 10 or self.rect.left <= 10:
            self.velocidade_x *= -1
            self.rect.y += 25

    def tentar_atirar(self, grupo_tiros_inimigos):
        if random.random() < 0.003:
            tiro = Projetil(self.rect.centerx, self.rect.bottom, 5, eh_jogador=False)
            grupo_tiros_inimigos.add(tiro)