import pygame
from config import AMARELO_TIRO, VERMELHO_CHEFAO, ALTURA

class Projetil(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidade_y, eh_jogador=True):
        super().__init__()
        self.image = pygame.Surface((6, 16))
        self.image.fill(AMARELO_TIRO if eh_jogador else VERMELHO_CHEFAO)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidade_y = velocidade_y

    def update(self):
        self.rect.y += self.velocidade_y
        if self.rect.bottom < 0 or self.rect.top > ALTURA:
            self.kill()