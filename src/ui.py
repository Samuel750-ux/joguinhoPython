import os
import pygame
from config import LARGURA, ALTURA, BRANCO, AMARELO_TIRO, CIANO, VERMELHO_CHEFAO

class Interface:
    def __init__(self):
        caminho_fonte = os.path.join("assets", "fonts", "pixel_font.ttf")
        if os.path.exists(caminho_fonte):
            self.fonte_pequena = pygame.font.Font(caminho_fonte, 18)
            self.fonte_grande = pygame.font.Font(caminho_fonte, 36)
        else:
            self.fonte_pequena = pygame.font.SysFont("consolas", 22, bold=True)
            self.fonte_grande = pygame.font.SysFont("consolas", 42, bold=True)

    def desenhar_hud(self, tela, pontos, vidas, fase):
        txt_pontos = self.fonte_pequena.render(f"PONTOS: {pontos}", True, BRANCO)
        txt_fase = self.fonte_pequena.render(f"FASE: {fase}", True, CIANO)
        txt_vidas = self.fonte_pequena.render(f"VIDAS: {vidas}", True, AMARELO_TIRO)

        tela.blit(txt_pontos, (15, 12))
        tela.blit(txt_fase, (LARGURA // 2 - txt_fase.get_width() // 2, 40))
        tela.blit(txt_vidas, (LARGURA - txt_vidas.get_width() - 15, 12))

    def desenhar_tela_inicial(self, tela):
        titulo = self.fonte_grande.render("BATALHA ESPACIAL CCM", True, AMARELO_TIRO)
        instrucao = self.fonte_pequena.render("Setas/A-D: Mover | Espaço: Atirar", True, BRANCO)
        iniciar = self.fonte_pequena.render("Pressione ENTER para jogar", True, CIANO)

        tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, ALTURA // 2 - 80))
        tela.blit(instrucao, (LARGURA // 2 - instrucao.get_width() // 2, ALTURA // 2))
        tela.blit(iniciar, (LARGURA // 2 - iniciar.get_width() // 2, ALTURA // 2 + 50))

    def desenhar_game_over(self, tela, pontos, vitoria=False):
        msg = "VOCÊ VENCEU!" if vitoria else "GAME OVER"
        cor = CIANO if vitoria else VERMELHO_CHEFAO
        txt_fim = self.fonte_grande.render(msg, True, cor)
        txt_pts = self.fonte_pequena.render(f"Pontuação Final: {pontos}", True, BRANCO)
        txt_reiniciar = self.fonte_pequena.render("Pressione R para jogar novamente", True, AMARELO_TIRO)

        tela.blit(txt_fim, (LARGURA // 2 - txt_fim.get_width() // 2, ALTURA // 2 - 70))
        tela.blit(txt_pts, (LARGURA // 2 - txt_pts.get_width() // 2, ALTURA // 2))
        tela.blit(txt_reiniciar, (LARGURA // 2 - txt_reiniciar.get_width() // 2, ALTURA // 2 + 50))