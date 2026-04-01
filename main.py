import random
from ambiente.Ambiente import Ambiente
from agentes.AgenteReativoSimples import AgenteReativoSimples
from agentes.AgenteBDI import AgenteBDI
from agentes.AgenteBaseadoEmObjetivo import AgenteBaseadoEmObjetivo
from agentes.AgenteBaseadoEmUtilidade import AgenteBaseadoEmUtilidade
from agentes.AgenteReativoBaseadoEmModelo import AgenteReativoBaseadoEmModelo
from time import sleep

def main():
    ambiente = Ambiente(grid_size = 5)

    #inicilizando os agentes
    bombeiro = AgenteReativoBaseadoEmModelo(ambiente, None, quadrante='Q1', x=0, y=0)
    socorrista_seq = AgenteBaseadoEmObjetivo(ambiente, None, x=0, y=4)
    socorrista_otm = AgenteBaseadoEmUtilidade(ambiente, None, x=4, y=0)

    bdi = AgenteBDI(ambiente, bombeiros=[bombeiro], socorrista_sequencial= socorrista_seq, socorrista_otimizador=socorrista_otm)

    bombeiro.bdi = bdi
    socorrista_seq.bdi = bdi
    socorrista_otm.bdi = bdi


    drone = AgenteReativoSimples(ambiente = ambiente, AgenteBDI = bdi)

    passos = 0
    intervalo_geracao_eventos = 5


    while True:
        if passos % intervalo_geracao_eventos == 0:
            #50% de chance de gerar fogo ou vitima
            if random.random() < 0.5:
                ambiente.gerar_fogos()
            else:
                ambiente.gerar_vitimas()

        
        #DRONE
        drone.perceber()
        print(f"Drone percebeu: {drone.estado_atual} na posição ({drone.x}, {drone.y})")
        acao = drone.agir()
        print(f"Drone decidiu: {acao}")
        drone.mover()

        #Bombeiro
        bombeiro.perceber()
        print(f"Bombeiro  percebeu: ({bombeiro.alvo}) na posicao: ({bombeiro.x}, {bombeiro.y})" )
        acao = bombeiro.agir()
        bombeiro.mover()

        #Socorrista Sequencial
        socorrista_seq.perceber()
        print(f"Socorrista Sequencial percebeu: ({socorrista_seq.lista_vitimas}) na posicao: ({socorrista_seq.x}, {socorrista_seq.y})" )
        acao = socorrista_seq.agir()
        socorrista_seq.mover()

        #Socorrista Otimizador
        socorrista_otm.perceber()
        print(f"Socorrista Otimizador percebeu: ({socorrista_otm.lista_vitimas}) na posicao: ({socorrista_otm.x}, {socorrista_otm.y})" )
        acao = socorrista_otm.agir()
        socorrista_otm.mover()


        sleep(2)
        passos += 1


if __name__ == "__main__":
    main()