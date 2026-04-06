# agentes/SocorristaOtimizador.py
import math
from utils.Tile import Tile
from collections import deque

class AgenteBaseadoEmUtilidade:
    def __init__(self, ambiente, bdi, x, y):
        self.ambiente = ambiente
        self.bdi = bdi
        self.x = x
        self.y = y
        self.lista_vitimas = []
        self.ocupado = False
        self.carregando_vitima = False
        self.estado = 'ocioso'

    def _hospital_mais_proximo(self):
        return min(self.ambiente.hospital_posicoes, key=lambda pos: self.distancia(pos))

    def receber_lista(self, lista):
        self.lista_vitimas = sorted(lista, key=lambda v: self.distancia(v))
        self.ocupado = True
        self.carregando_vitima = False
        if self.lista_vitimas:
            self.estado = 'movendo_vitima'
        else:
            self.estado = 'ocioso'

    def distancia(self, pos):
        return math.hypot(self.x - pos[0], self.y - pos[1])

    def perceber(self):
        if not self.ocupado:
            self.estado = 'ocioso'
            return
        if not self.lista_vitimas and not self.carregando_vitima:
            self.ocupado = False
            self.estado = 'ocioso'
            self.bdi.notificar_socorrista_concluiu(self)
            return

        if self.carregando_vitima:
            alvo = self._hospital_mais_proximo()
            if (self.x, self.y) == alvo:
                self.estado = 'no_hospital'
            else:
                self.estado = 'movendo_hospital'
        else:
            alvo = self.lista_vitimas[0]
            if (self.x, self.y) == alvo:
                self.estado = 'resgatando'
            else:
                self.estado = 'movendo_vitima'

    def agir(self):
        if self.estado == 'resgatando':
            alvo = self.lista_vitimas[0]
            if self.ambiente.resgatar_vitima(alvo[0], alvo[1]):
                self.carregando_vitima = True
                self.vitima_carregada = self.lista_vitimas.pop(0) # Remove da fila de pendentes logo no resgate

        elif self.estado == 'no_hospital':
            self.carregando_vitima = False
            self.bdi.registrar_resgate(self, self.vitima_carregada)
            #(f"[{self.__class__.__name__}] Deixou a vítima no hospital.")
            if self.lista_vitimas:
                self.lista_vitimas.sort(key=lambda v: self.distancia(v))


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

    def mover(self):
        alvo = None
        if self.estado == 'movendo_vitima':
            alvo = self.lista_vitimas[0] # Lista já vem ordenada via heurística local de distancias
        elif self.estado == 'movendo_hospital':
            alvo = self._hospital_mais_proximo()
        
        if alvo is None:
            return
            
        caminho = self._planejar_caminho((self.x, self.y), alvo)
        if caminho:
            self.x, self.y = caminho[0]

    def adicionar_vitima(self, vitima):
        self.lista_vitimas.append(vitima)
        self.lista_vitimas.sort(key=lambda v: self.distancia(v))
        if not self.ocupado:
            self.ocupado = True
            self.estado = 'movendo_vitima'