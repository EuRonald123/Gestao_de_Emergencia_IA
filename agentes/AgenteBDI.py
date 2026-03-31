class AgenteBDI:
    def __init__(self, bombeiros, socorrista_sequencial, socorrista_otimizador):
        self.bombeiros = bombeiros                              #lista de bombeiros -> agentes reativos baseados em modelo
        self.socorrista_sequencial = socorrista_sequencial      #lista de socorristas sequenciais -> agente reativo baseado em objetivo
        self.socorrista_otimizador = socorrista_otimizador      #lista de socorristas otimizadores -> agente reativo baseado em utilidade


        #aqui vai armazenas as crencas relatadas pelos drones
        self.crencas = {
            "fogos": set(),  #conjunto de posições dos fogos
            "vitimas": set() #conjunto de posições das vítimas
        }

    '''
    Qual vai ser a lógica?
    1. Tem que separar o conjunto de vitimas em 2
        -> Lista = [] -> Todas as vítimas reportadas pelos drones
        -> ListaA -> vitimas para o socorrista sequencial
        -> ListaB -> vitimas para o socorrista otimizador

    2. Quem vai decicidir qual agente mandar será a propria classe responsável.
        -> exemplo: o agente BDI pega a lista de vitimas, manda uma lista para os socorristas sequenciais e outra para os otimizadores.
        -> A decisão de qual socorrista enviar, vai ficar para a propria classe do socorrista definir a estratégia



    3. Bombeiros
        -> Terei que implementar uma função para gerenciar os bombeiros de maneira mais agressiva
        -> Os bombeiros só irão se locomover para o foco de incêndia se o comandante BDI decidir que é necessário
    
    
    
    '''



    
