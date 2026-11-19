from src.enemy import Inimigo
from src.boss import Chefao

def carregar_fase(numero_fase, grupo_inimigos, grupo_chefao):
    grupo_inimigos.empty()
    grupo_chefao.empty()

    if numero_fase == 1:
        for linha in range(3):
            for coluna in range(8):
                x = 90 + coluna * 75
                y = 60 + linha * 50
                tipo = 2 if linha == 0 else 1
                grupo_inimigos.add(Inimigo(x, y, tipo=tipo, velocidade=2))

    elif numero_fase == 2:
        for linha in range(4):
            for coluna in range(9):
                x = 65 + coluna * 75
                y = 55 + linha * 48
                tipo = 2 if linha < 2 else 1
                grupo_inimigos.add(Inimigo(x, y, tipo=tipo, velocidade=3))

    elif numero_fase >= 3:
        chefao = Chefao(vida_maxima=25 + (numero_fase - 3) * 10)
        grupo_chefao.add(chefao)
        for coluna in range(5):
            x = 150 + coluna * 115
            grupo_inimigos.add(Inimigo(x, 150, tipo=2, velocidade=3))