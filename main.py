import random
import pygame
from ambiente.Ambiente import Ambiente
from agentes.AgenteReativoSimples import AgenteReativoSimples
from agentes.AgenteBDI import AgenteBDI
from agentes.AgenteBaseadoEmObjetivo import AgenteBaseadoEmObjetivo
from agentes.AgenteBaseadoEmUtilidade import AgenteBaseadoEmUtilidade
from agentes.AgenteReativoBaseadoEmModelo import AgenteReativoBaseadoEmModelo
from Interface.visualizacao import Visualizacao
from time import time

def main():
    ambiente = Ambiente(grid_size = 10)

    visualizacao = Visualizacao(ambiente=ambiente)
    visualizacao.iniciar()

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
    intervalo_geracao_eventos = 2

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


        # Atualiza a interface graficamente de forma contínua durante 1 segundo
        tempo_inicio = time()
        while time() - tempo_inicio < 1.0:
            if not visualizacao.atualizar(ambiente, drone=drone, bombeiro=bombeiro, socorrista_seq=socorrista_seq, socorrista_otm=socorrista_otm):
                return
            visualizacao.clock.tick(60) # Roda a interface a 60 FPS suavizando a animação

        passos += 1


if __name__ == "__main__":
    main()