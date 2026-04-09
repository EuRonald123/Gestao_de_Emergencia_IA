from utils.Tile import Tile
import random

class AgenteReativoSimples:
    def __init__(self, ambiente, AgenteBDI, x=0, y=0):
        self.estado_atual = None
        self.x = x
        self.y = y
        self.ambiente = ambiente
        self.bdi = AgenteBDI

    def perceber(self):
        self.estado_atual = self.ambiente.obter_estado(self.x, self.y)

    
    def agir(self): 
        if self.estado_atual == Tile.FOGO:
            self.bdi.registrar_evento(Tile.FOGO, (self.x, self.y))
            return 'reportar fogo'
        elif self.estado_atual == Tile.VITIMA:
            self.bdi.registrar_evento(Tile.VITIMA, (self.x, self.y))
            return 'reportar vítima'
        else:
            return 'explorar'
        

    def mover(self):
        movimentos_possiveis = [
            (0, -1), (0, 1), (-1, 0), (1, 0),
            (-1, -1), (1, -1), (-1, 1), (1, 1)
        ]
        #Isso aqui é pra garantir que o drone ou outro agente qualquer nao fique bugado ou saia do ambiente
        movimentos_validos = []
        for dx, dy in movimentos_possiveis:
            novo_x = self.x + dx
            novo_y = self.y + dy

            if ((0 <= novo_x < self.ambiente.grid_size) and (0 <= novo_y < self.ambiente.grid_size)):
                movimentos_validos.append((dx, dy))

        if movimentos_validos:
            dx, dy = random.choice(movimentos_validos)
            self.x += dx
            self.y += dy