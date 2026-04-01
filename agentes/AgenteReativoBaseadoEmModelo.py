# agentes/Bombeiro.py (novo)
class AgenteReativoBaseadoEmModelo:
    def __init__(self, ambiente, bdi, quadrante, x, y):
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

    #movimento manhattan
    def mover(self):
        if self.estado != 'movendo':
            return
        dx = 0
        dy = 0
        if self.x < self.alvo[0]:
            dx = 1
        elif self.x > self.alvo[0]:
            dx = -1
        if self.y < self.alvo[1]:
            dy = 1
        elif self.y > self.alvo[1]:
            dy = -1
        self.x += dx
        self.y += dy


    


