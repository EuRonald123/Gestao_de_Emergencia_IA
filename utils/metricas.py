class MetricasSimulacao:
    AGENTE_SEQUENCIAL = "sequencial"
    AGENTE_OTIMIZADOR = "otimizador"

    def __init__(self):
        self.tempo_segundos = 0
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

    def registrar_tempo(self, segundos=1):
        self.tempo_segundos += max(0, int(segundos))

    def obter_snapshot(self):
        snapshot = {
            agente: valores.copy()
            for agente, valores in self._dados.items()
        }
        snapshot["tempo_segundos"] = self.tempo_segundos
        return snapshot
