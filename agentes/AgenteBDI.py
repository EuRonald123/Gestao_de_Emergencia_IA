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
        #Vai pegar a lista de vitimas e dividir em duas parte, uma pra cada agente
        self.lista_resgate_sequencial = []
        self.lista_resgate_otimizador = []


    #metodo pra receber as informações que o drone coletou
    def registrar_evento(self, tipo_evento, posicao):
        if tipo_evento == Tile.FOGO:
            self.crencas["fogos"].add(posicao)
        elif tipo_evento == Tile.VITIMA:
            self.crencas["vitimas"].add(posicao)
        self.processar_crencas()

    def processar_crencas(self):
        #atualiza os planos com base nas crenças
        self.processar_incendios()
        self.processar_resgates()

    def processar_incendios(self):
        #Aqui é para atribuir os bombeiros para os incendios de acordo com o quadrante
        fogos = list(self.crencas["fogos"])
        if not fogos:
            return

        # Agrupar fogos por quadrante
        fogos_por_quadrante = {'Q1': [], 'Q2': [], 'Q3': [], 'Q4': []}
        for fogo in fogos:
            q = self.ambiente.obter_quadrante(x = fogo[0], y = fogo[1])
            fogos_por_quadrante[q].append(fogo)

        # Primeiro, atribui bombeiros aos fogos do seu próprio quadrante
        bombeiros_disponiveis = []
        #pega todos os bombeiros disponiveis
        for b in self.bombeiros:
            if not self.bombeiro_ocupado[b]:
                bombeiros_disponiveis.append(b)
            
        for bombeiro in bombeiros_disponiveis:
            #ainda tenho que implementar essa funcao de obter quadrante do bombeiro, mas isso é coisa simples
            q = bombeiro.quadrante
            if fogos_por_quadrante[q]:
                fogo = fogos_por_quadrante[q].pop(0)
                self.atribuir_bombeiro(bombeiro, fogo)

        # Depois, se ainda há fogos e bombeiros disponíveis, realocar
        bombeiros_disponiveis = []
        for b in self.bombeiros:
            if not self.bombeiro_ocupado[b]:
                bombeiros_disponiveis.append(b)

        for bombeiro in bombeiros_disponiveis:
            for q, lista in fogos_por_quadrante.items():
                if lista:
                    fogo = lista.pop(0)
                    self.atribuir_bombeiro(bombeiro, fogo)
                    break

    def atribuir_bombeiro(self, bombeiro, fogo):
        #Envia um bombeiro pra apagar o fogo da tua mae
        self.bombeiro_ocupado[bombeiro] = True
        self.planos_incendio[bombeiro] = fogo
        bombeiro.receber_ordem(fogo)

    def processar_resgates(self):
        #Plano de Resgate é dividir vítimas entre socorristas.
        vitimas = list(self.crencas["vitimas"])
        if not vitimas:
            return

        if not self.socorrista_seq_ocupado and not self.socorrista_opt_ocupado:
            #metade para cada mas pode ser numeros impares etc
            meio = len(vitimas) // 2
            lista_seq = vitimas[:meio]
            lista_opt = vitimas[meio:]
            self.lista_resgate_sequencial = lista_seq
            self.lista_resgate_otimizador = lista_opt
            self.socorrista_seq_ocupado = True
            self.socorrista_opt_ocupado = True
            self.socorrista_sequencial.receber_lista(lista_seq)
            self.socorrista_otimizador.receber_lista(lista_opt)

    def notificar_bombeiro_concluiu(self, bombeiro):
        #Chama quando um bombeiro termina de apagar o fogo.
        self.bombeiro_ocupado[bombeiro] = False
        if bombeiro in self.planos_incendio:
            fogo = self.planos_incendio.pop(bombeiro)
            self.crencas["fogos"].discard(fogo)
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