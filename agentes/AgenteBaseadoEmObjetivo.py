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
        self.carregando_vitima = False
        self.estado = 'ocioso'   # ocioso, movendo_vitima, resgatando, movendo_hospital, no_hospital

    def _hospital_mais_proximo(self):
        # Acha o bloco do hospital mais perto da posição atual
        return min(self.ambiente.hospital_posicoes, key=lambda pos: abs(self.x - pos[0]) + abs(self.y - pos[1]))

    def receber_lista(self, lista):
        self.lista_vitimas = lista
        self.indice_atual = 0
        self.ocupado = True
        self.carregando_vitima = False
        if lista:
            self.estado = 'movendo_vitima'
        else:
            self.estado = 'ocioso'

    def perceber(self):
        if not self.ocupado:
            self.estado = 'ocioso'
            return
        if self.indice_atual >= len(self.lista_vitimas) and not self.carregando_vitima:
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
            alvo = self.lista_vitimas[self.indice_atual]
            if (self.x, self.y) == alvo:
                self.estado = 'resgatando'
            else:
                self.estado = 'movendo_vitima'

    def agir(self):
        if self.estado == 'resgatando':
            alvo = self.lista_vitimas[self.indice_atual]
            if self.ambiente.resgatar_vitima(alvo[0], alvo[1]):
                self.carregando_vitima = True
                self.vitima_carregada = self.lista_vitimas.pop(self.indice_atual)

        elif self.estado == 'no_hospital':
            self.carregando_vitima = False
            self.bdi.registrar_resgate(self, self.vitima_carregada)
            print(f"[{self.__class__.__name__}] Deixou a vítima no hospital.")
            
            if self.indice_atual >= len(self.lista_vitimas):
                self.indice_atual = 0

    def mover(self):
        alvo = None
        if self.estado == 'movendo_vitima':
            alvo = self.lista_vitimas[self.indice_atual]
        elif self.estado == 'movendo_hospital':
            alvo = self._hospital_mais_proximo()
        
        if alvo is None:
            return
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
            self.estado = 'movendo_vitima'