import random
from ambiente.Ambiente import Ambiente
from agentes.AgenteReativoSimples import AgenteReativoSimples
from time import sleep

def main():
    ambiente = Ambiente(grid_size = 10)
    drone = AgenteReativoSimples(ambiente = ambiente)

    passos = 0
    intervalo_geracao_eventos = 5


    while True:
        if passos % intervalo_geracao_eventos == 0:
            #50% de chance de gerar fogo ou vitima
            if random.random() < 0.5:
                ambiente.gerar_fogos()
            else:
                ambiente.gerar_vitimas()

        

        drone.perceber()
        print(f"Drone percebeu: {drone.estado_atual} na posição ({drone.x}, {drone.y})")
        acao = drone.agir()
        print(f"Drone decidiu: {acao}")

        #ambiente.atualizar_estado(acao=acao, x=drone.x, y=drone.y)
        #print(f"Ambiente atualizado: {acao} na posição ({drone.x}, {drone.y}), estado atual: {ambiente.obter_estado(drone.x, drone.y)}")

        drone.movimentar()

        sleep(0.5)
        passos += 1


if __name__ == "__main__":
    main()

