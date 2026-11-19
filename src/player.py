import os
import pygame
from config import LARGURA, ALTURA, VELOCIDADE_JOGADOR, VIDAS_INICIAIS, COOLDOWN_TIRO, AZUL_NAVE, BRANCO
from src.projectile import Projetil

class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        caminho_img = os.path.join("assets", "images", "player.png")
        
        if os.path.exists(caminho_img):
            self.image = pygame.image.load(caminho_img).convert_alpha()
            self.image = pygame.transform.scale(self.image, (48, 48))
        else:
            self.image = pygame.Surface((44, 44), pygame.SRCALPHA)
            pygame.draw.polygon(self.image, AZUL_NAVE, [(22, 0), (44, 44), (22, 34), (0, 44)])
            pygame.draw.rect(self.image, BRANCO, (19, 14, 6, 14))

        self.rect = self.image.get_rect(midbottom=(LARGURA // 2, ALTURA - 20))
        self.vidas = VIDAS_INICIAIS
        self.ultimo_tiro = 0

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.rect.x -= VELOCIDADE_JOGADOR
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.rect.x += VELOCIDADE_JOGADOR

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > LARGURA:
            self.rect.right = LARGURA

    def atirar(self, grupo_tiros, som_tiro=None):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro >= COOLDOWN_TIRO:
            self.ultimo_tiro = agora
            tiro = Projetil(self.rect.centerx, self.rect.top, -10, eh_jogador=True)
            grupo_tiros.add(tiro)
            if som_tiro:
                som_tiro.play()