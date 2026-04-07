import random
from ambiente.Ambiente import Ambiente
from agentes.AgenteReativoSimples import AgenteReativoSimples
from agentes.AgenteBDI import AgenteBDI
from agentes.AgenteBaseadoEmObjetivo import AgenteBaseadoEmObjetivo
from agentes.AgenteBaseadoEmUtilidade import AgenteBaseadoEmUtilidade
from agentes.AgenteReativoBaseadoEmModelo import AgenteReativoBaseadoEmModelo
from Interface.visualizacao import Visualizacao
from utils.metricas import MetricasSimulacao
from time import time
from rich.live import Live

def main():
    ambiente = Ambiente(grid_size = 10)
    metricas = MetricasSimulacao()

    #cria a janela pygame para a visualizacao
    visualizacao = Visualizacao(ambiente=ambiente, metricas=metricas)
    visualizacao.iniciar()

    #Auxiliar para pegar posiçoes
    meio = ambiente.grid_size // 2
    final = ambiente.grid_size - 1


    #inicilizando os agentes

    #DRONES:
    drones = []
    pos_drones = [(0,meio), (final, meio)]
    qtd_drones = 4
    for d in range(qtd_drones):
        if d%2 == 0:
            pos = 0
        else:
            pos = 1
        drone = AgenteReativoSimples(ambiente = ambiente, AgenteBDI=None, x=pos_drones[pos][0], y=pos_drones[pos][1])
        drones.append(drone)


    #BOMBEIROS:
    bombeiros = []
    qtd_bombeiros = 4
    pos_bombeiros = [(0, 0), (0, ambiente.grid_size - 1), (ambiente.grid_size - 1, 0), (ambiente.grid_size - 1, ambiente.grid_size - 1)]

    for b in range(qtd_bombeiros):
        bombeiro = AgenteReativoBaseadoEmModelo(ambiente, None, quadrante=f'Q{b+1}', x=pos_bombeiros[b][0], y=pos_bombeiros[b][1])
        bombeiros.append(bombeiro)

    #SOCORRISTAS:
    socorrista_seq = AgenteBaseadoEmObjetivo(ambiente, None, x=meio-1, y=meio)
    socorrista_otm = AgenteBaseadoEmUtilidade(ambiente, None, x=meio, y=meio)

    #Agente BDI:
    bdi = AgenteBDI(
        ambiente,
        bombeiros=bombeiros,
        socorrista_sequencial=socorrista_seq,
        socorrista_otimizador=socorrista_otm,
        metricas=metricas,
    )


    #Atribuicao do BDI para os agentes
    for drone in drones:
        drone.bdi = bdi

    for bombeiro in bombeiros:
        bombeiro.bdi = bdi
    
    socorrista_seq.bdi = bdi
    socorrista_otm.bdi = bdi


    passos = 0
    intervalo_geracao_eventos = 1

    ambiente.gerar_obstaculos(quantidade=15) 

    with Live(metricas.gerar_dashboard(), refresh_per_second=4, screen=False) as live:
        while True:
            if passos >0 and passos % intervalo_geracao_eventos == 0:
                #50% de chance de gerar fogo ou vitima
                if random.random() < 0.5:
                    ambiente.gerar_fogos()
                else:
                    ambiente.gerar_vitimas()

            
            #DRONE
            for drone in drones:
                drone.perceber()
                acao = drone.agir()
                drone.mover()

            #Bombeiro
            for bombeiro in bombeiros:
                bombeiro.perceber()
                acao = bombeiro.agir()
                bombeiro.mover()

            #Socorrista Sequencial
            pos_seq_antes = (socorrista_seq.x, socorrista_seq.y)
            socorrista_seq.perceber()
            acao = socorrista_seq.agir()
            socorrista_seq.mover()
            if (socorrista_seq.x, socorrista_seq.y) != pos_seq_antes:
                metricas.registrar_passo(MetricasSimulacao.AGENTE_SEQUENCIAL)

            #Socorrista Otimizador
            pos_otm_antes = (socorrista_otm.x, socorrista_otm.y)
            socorrista_otm.perceber()
            acao = socorrista_otm.agir()
            socorrista_otm.mover()
            if (socorrista_otm.x, socorrista_otm.y) != pos_otm_antes:
                metricas.registrar_passo(MetricasSimulacao.AGENTE_OTIMIZADOR)


            # interface att
            tempo_inicio = time()
            while time() - tempo_inicio < 1.0:
                if not visualizacao.atualizar(ambiente, drones=drones, bombeiros=bombeiros, socorrista_seq=socorrista_seq, socorrista_otm=socorrista_otm):
                    return
                visualizacao.clock.tick(60)
                live.update(metricas.gerar_dashboard(bdi.historico_mensagens))

            metricas.registrar_tempo(segundos=1)
            passos += 1
            


if __name__ == "__main__":
    main()
    