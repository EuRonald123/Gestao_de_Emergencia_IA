# agentes/SocorristaOtimizador.py
import math

class AgenteBaseadoEmUtilidade:
    def __init__(self, ambiente, bdi, x, y):
        self.ambiente = ambiente
        self.bdi = bdi
        self.x = x
        self.y = y
        self.lista_vitimas = []
        self.ocupado = False
        self.estado = 'ocioso'

    def receber_lista(self, lista):
        self.lista_vitimas = sorted(lista, key=lambda v: self.distancia(v))
        self.ocupado = True
        if self.lista_vitimas:
            self.estado = 'movendo'
        else:
            self.estado = 'ocioso'

    def distancia(self, pos):
        return math.hypot(self.x - pos[0], self.y - pos[1])

    def perceber(self):
        if not self.ocupado:
            self.estado = 'ocioso'
            return
        if not self.lista_vitimas:
            self.ocupado = False
            self.estado = 'ocioso'
            self.bdi.notificar_socorrista_concluiu(self)
            return
        alvo = self.lista_vitimas[0]
        if (self.x, self.y) == alvo:
            self.estado = 'no_alvo'
        else:
            self.estado = 'movendo'

    def agir(self):
        if self.estado == 'no_alvo':
            alvo = self.lista_vitimas[0]
            if self.ambiente.resgatar_vitima(alvo[0], alvo[1]):
                self.lista_vitimas.pop(0)
                self.bdi.registrar_resgate(self, alvo)
                self.lista_vitimas.sort(key=lambda v: self.distancia(v))

    def mover(self):
        if self.estado != 'movendo':
            return
        alvo = self.lista_vitimas[0]
        dx = 0
        dy = 0
        if self.x < alvo[0]:
            dx = 1
        elif self.x > alvo[0]:
            dx = -1
        if self.y < alvo[1]:
            dy = 1
        elif self.y > alvo[1]:
            dy = -1
        self.x += dx
        self.y += dy

    def adicionar_vitima(self, vitima):
        self.lista_vitimas.append(vitima)
        self.lista_vitimas.sort(key=lambda v: self.distancia(v))
        if not self.ocupado:
            self.ocupado = True
            self.estado = 'movendo'