class MetricasSimulacao:
    AGENTE_SEQUENCIAL = "sequencial"
    AGENTE_OTIMIZADOR = "otimizador"

    def __init__(self):
        self._dados = {
            self.AGENTE_SEQUENCIAL: {
                "qtd_vitimas": 0,
                "qtd_passos": 0,
            },
            self.AGENTE_OTIMIZADOR: {
                "qtd_vitimas": 0,
                "qtd_passos": 0,
            },
        }

    def registrar_resgate(self, agente_nome):
        if agente_nome in self._dados:
            self._dados[agente_nome]["qtd_vitimas"] += 1

    def registrar_passo(self, agente_nome):
        if agente_nome in self._dados:
            self._dados[agente_nome]["qtd_passos"] += 1

    def obter_snapshot(self):
        return {
            agente: valores.copy()
            for agente, valores in self._dados.items()
        }
