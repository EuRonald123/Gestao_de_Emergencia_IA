# agentes/Bombeiro.py (novo)
from utils.Tile import Tile
from collections import deque

class AgenteReativoBaseadoEmModelo:
    def __init__(self, ambiente, bdi, quadrante, x , y):
        self.ambiente = ambiente
        self.bdi = bdi
        self.quadrante = quadrante
        self.x = x
        self.y = y
        self.alvo = None
        self.ocupado = False
        self.estado = 'ocioso' #ocioso, movendo, no_alvo

    def receber_ordem(self, alvo):
        self.alvo = alvo
        self.ocupado = True
        self.estado = 'movendo'

    def perceber(self):
        if self.alvo:
            if (self.x, self.y) == self.alvo:
                self.estado = 'no_alvo'
            else:
                self.estado = 'movendo'
        else:
            self.estado = 'ocioso'

    def agir(self):
        if self.estado == 'no_alvo':
            if self.ambiente.apagar_fogo(self.x, self.y):
                self.ocupado = False
                self.alvo = None
                self.estado = 'ocioso'
                self.bdi.notificar_bombeiro_concluiu(self)

    # Função interna para gerar uma rota driblando obstáculos com base no seu modelo de mundo
    def _planejar_caminho(self, inicio, fim):
        if inicio == fim:
            return []
        
        fila = deque([(inicio[0], inicio[1], [])])
        visitados = set()
        visitados.add(inicio)
        
        direcoes = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (-1,-1), (1,-1), (-1,1)]
        
        while fila:
            x, y, caminho = fila.popleft()
            for dx, dy in direcoes:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.ambiente.grid_size and 0 <= ny < self.ambiente.grid_size:
                    if (nx, ny) == fim:
                        return caminho + [(nx, ny)]
                    if (nx, ny) not in visitados and self.ambiente.matriz[nx][ny] != Tile.OBSTACULO:
                        visitados.add((nx, ny))
                        fila.append((nx, ny, caminho + [(nx, ny)]))
        return []

    #movimento 
    def mover(self):
        if self.estado != 'movendo':
            return
            
        caminho = self._planejar_caminho((self.x, self.y), self.alvo)
        if caminho:
            self.x, self.y = caminho[0]


    


