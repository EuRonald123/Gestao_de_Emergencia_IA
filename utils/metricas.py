from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich import box

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

    def gerar_dashboard(self, mensagens_bdi=[]):
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=10),
        )

        # Header
        layout["header"].update(
            Panel(
                f"[bold cyan]SIMULAÇÃO DE GESTÃO DE EMERGÊNCIAS - SMART CITY[/bold cyan] | [bold yellow]Tempo: {self.tempo_segundos}s[/bold yellow]",
                box=box.DOUBLE_EDGE,
            )
        )

        # Main metrics comparison
        tabela = Table(title="Comparativo de Desempenho (Objetivo vs. Utilidade)", expand=True)
        tabela.add_column("Métrica", style="cyan", no_wrap=True)
        tabela.add_column("Socorrista Sequencial (Objetivo)", style="magenta", justify="center")
        tabela.add_column("Socorrista Otimizador (Utilidade)", style="green", justify="center")

        tabela.add_row(
            "Vítimas Resgatadas",
            str(self._dados[self.AGENTE_SEQUENCIAL]["qtd_vitimas"]),
            str(self._dados[self.AGENTE_OTIMIZADOR]["qtd_vitimas"]),
        )
        tabela.add_row(
            "Passos Percorridos",
            str(self._dados[self.AGENTE_SEQUENCIAL]["qtd_passos"]),
            str(self._dados[self.AGENTE_OTIMIZADOR]["qtd_passos"]),
        )
        
        # Eficiência (Passos por vítima)
        def calc_eficiencia(ag):
            vitimas = self._dados[ag]["qtd_vitimas"]
            passos = self._dados[ag]["qtd_passos"]
            return f"{passos/vitimas:.2f}" if vitimas > 0 else "N/A"

        tabela.add_row(
            "Eficiência (Passos/Vítima)",
            calc_eficiencia(self.AGENTE_SEQUENCIAL),
            calc_eficiencia(self.AGENTE_OTIMIZADOR),
        )

        layout["main"].update(Panel(tabela))

        # Footer with BDI logs
        logs_text = "\n".join(mensagens_bdi[-8:]) if mensagens_bdi else "Sem mensagens do BDI..."
        layout["footer"].update(Panel(logs_text, title="[bold white]Logs do Comandante Central (BDI)[/bold white]", border_style="blue"))

        return layout
