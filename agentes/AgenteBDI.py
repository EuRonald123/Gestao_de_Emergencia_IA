# agentes/AgenteBDI.py (implementação completa)
from utils.Tile import Tile

class AgenteBDI:
    def __init__(self, ambiente, bombeiros, socorrista_sequencial, socorrista_otimizador):
        self.ambiente = ambiente
        self.bombeiros = bombeiros
        self.socorrista_sequencial = socorrista_sequencial
        self.socorrista_otimizador = socorrista_otimizador

        # Crenças
        self.crencas = {
            "fogos": set(),
            "vitimas": set()
        }

        # Estado dos agentes
        self.bombeiro_ocupado = {b: False for b in bombeiros}
        self.socorrista_seq_ocupado = False
        self.socorrista_opt_ocupado = False

        # Planos em execução
        self.planos_incendio = {}          # o bombeiro é reponsavel apenaas por apagar o fogo, de acordocom o pdf,  bombeiro para cada quadrante
        #Vai pegar a lista de vitimas e alternar uma pra cada agente
        self.lista_resgate_sequencial = []
        self.lista_resgate_otimizador = []
        self.vitimas_designadas = set()
        self.fila_incendios = []
        self.contador_distribuicao_vitimas = 0


    #metodo pra receber as informações que o drone coletou
    def registrar_evento(self, tipo_evento, posicao):
        if tipo_evento == Tile.FOGO:
            self.crencas["fogos"].add(posicao)
            self._enfileirar_incendio(posicao)
        elif tipo_evento == Tile.VITIMA:
            self.crencas["vitimas"].add(posicao)
        self.processar_crencas()

    def processar_crencas(self):
        #atualiza os planos com base nas crenças
        self.processar_incendios()
        self.processar_resgates()

    def processar_incendios(self):
        if not self.fila_incendios:
            return

        pendentes_por_quadrante = {'Q1': [], 'Q2': [], 'Q3': [], 'Q4': []}
        for fogo in self.fila_incendios:
            q = self.ambiente.obter_quadrante(x=fogo[0], y=fogo[1])
            pendentes_por_quadrante[q].append(fogo)

        bombeiros_disponiveis = [b for b in self.bombeiros if not self.bombeiro_ocupado[b]]
        if not bombeiros_disponiveis:
            return

        # Prioriza incêndios do mesmo quadrante
        ainda_disponiveis = []
        for bombeiro in bombeiros_disponiveis:
            q = bombeiro.quadrante
            if pendentes_por_quadrante[q]:
                fogo = pendentes_por_quadrante[q].pop(0)
                self.atribuir_bombeiro(bombeiro, fogo)
            else:
                ainda_disponiveis.append(bombeiro)

        # Em seguida, distribui quaisquer incêndios restantes
        for bombeiro in ainda_disponiveis:
            for lista in pendentes_por_quadrante.values():
                if lista:
                    fogo = lista.pop(0)
                    self.atribuir_bombeiro(bombeiro, fogo)
                    break

    def atribuir_bombeiro(self, bombeiro, fogo):
        #Envia um bombeiro pra apagar o fogo da tua mae
        self.bombeiro_ocupado[bombeiro] = True
        self.planos_incendio[bombeiro] = fogo
        bombeiro.receber_ordem(fogo)
        self._remover_fogo_da_fila(fogo)

    def processar_resgates(self):
        vitimas = list(self.crencas["vitimas"])
        if not vitimas:
            return

        novas_vitimas = [v for v in vitimas if v not in self.vitimas_designadas]
        for vitima in novas_vitimas:
            destino = self._escolher_socorrista()
            if destino == 'seq':
                self._designar_para_sequencial(vitima)
            else:
                self._designar_para_otimizador(vitima)

    def notificar_bombeiro_concluiu(self, bombeiro):
        #Chama quando um bombeiro termina de apagar o fogo.
        self.bombeiro_ocupado[bombeiro] = False
        if bombeiro in self.planos_incendio:
            fogo = self.planos_incendio.pop(bombeiro)
            self.crencas["fogos"].discard(fogo)
            self._remover_fogo_da_fila(fogo)
        self.processar_crencas()

    def notificar_socorrista_concluiu(self, socorrista):
        #Chama quando um socorrista termina sua lista de resgates.
        if socorrista == self.socorrista_sequencial:
            self.socorrista_seq_ocupado = False
            self.lista_resgate_sequencial = []
        elif socorrista == self.socorrista_otimizador:
            self.socorrista_opt_ocupado = False
            self.lista_resgate_otimizador = []

        self.processar_crencas()

    def registrar_resgate(self, socorrista, vitima):
        self.crencas["vitimas"].discard(vitima)
        self.vitimas_designadas.discard(vitima)

        if socorrista == self.socorrista_sequencial:
            if vitima in self.lista_resgate_sequencial:
                self.lista_resgate_sequencial.remove(vitima)
            if not self.lista_resgate_sequencial:
                self.socorrista_seq_ocupado = False
        elif socorrista == self.socorrista_otimizador:
            if vitima in self.lista_resgate_otimizador:
                self.lista_resgate_otimizador.remove(vitima)
            if not self.lista_resgate_otimizador:
                self.socorrista_opt_ocupado = False

        self.processar_crencas()

    def _escolher_socorrista(self):
        # Para análise justa de desempenho (métricas), forçamos envio estrito 1 por 1 
        # (metade das vitimas para cada), ignorando quem está ocioso.

        if self.contador_distribuicao_vitimas % 2 == 0:
            escolha = 'seq'
        else:
            escolha = 'otm'
        self.contador_distribuicao_vitimas += 1
        return escolha

    def _designar_para_sequencial(self, vitima):
        self.lista_resgate_sequencial.append(vitima)
        self.vitimas_designadas.add(vitima)
        if self.socorrista_seq_ocupado:
            self.socorrista_sequencial.adicionar_vitima(vitima)
        else:
            self.socorrista_seq_ocupado = True
            self.socorrista_sequencial.receber_lista(list(self.lista_resgate_sequencial))

    def _designar_para_otimizador(self, vitima):
        self.lista_resgate_otimizador.append(vitima)
        self.vitimas_designadas.add(vitima)
        if self.socorrista_opt_ocupado:
            self.socorrista_otimizador.adicionar_vitima(vitima)
        else:
            self.socorrista_opt_ocupado = True
            self.socorrista_otimizador.receber_lista(list(self.lista_resgate_otimizador))

    def _enfileirar_incendio(self, fogo):
        if fogo not in self.fila_incendios and fogo not in self.planos_incendio.values():
            self.fila_incendios.append(fogo)

    def _remover_fogo_da_fila(self, fogo):
        if fogo in self.fila_incendios:
            self.fila_incendios.remove(fogo)