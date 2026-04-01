# agentes/AgenteBaseadoEmObjetivo.py
class AgenteBaseadoEmObjetivo:
    def __init__(self, ambiente, bdi, x, y):
        self.ambiente = ambiente
        self.bdi = bdi
        self.x = x
        self.y = y
        self.lista_vitimas = []
        self.indice_atual = 0
        self.ocupado = False
        self.estado = 'ocioso'   # ocioso, movendo, no_alvo

    def receber_lista(self, lista):
        self.lista_vitimas = lista
        self.indice_atual = 0
        self.ocupado = True
        if lista:
            self.estado = 'movendo'
        else:
            self.estado = 'ocioso'

    def perceber(self):
        if not self.ocupado:
            self.estado = 'ocioso'
            return
        if self.indice_atual >= len(self.lista_vitimas):
            self.ocupado = False
            self.estado = 'ocioso'
            self.bdi.notificar_socorrista_concluiu(self)
            return
        alvo = self.lista_vitimas[self.indice_atual]
        if (self.x, self.y) == alvo:
            self.estado = 'no_alvo'
        else:
            self.estado = 'movendo'

    def agir(self):
        if self.estado == 'no_alvo':
            alvo = self.lista_vitimas[self.indice_atual]
            if self.ambiente.resgatar_vitima(alvo[0], alvo[1]):
                self.indice_atual += 1
                self.bdi.registrar_resgate(self, alvo)

    def mover(self):
        if self.estado != 'movendo':
            return
        alvo = self.lista_vitimas[self.indice_atual]
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
        if not self.ocupado:
            self.ocupado = True
            self.estado = 'movendo'