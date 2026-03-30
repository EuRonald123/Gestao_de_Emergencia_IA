from ambiente.Ambiente import Ambiente
from agentes.AgenteReativoSimples import AgenteReativoSimples
from time import sleep

def main():
    ambiente = Ambiente(grid_size = 10)
    drone = AgenteReativoSimples(ambiente = ambiente)

    while True:
        print(f"Posição atual do drone: ({drone.x}, {drone.y})")
        drone.perceber()
        print(f"Drone percebeu: {drone.estado_atual}")
        acao = drone.agir()
        print(f"Drone decidiu: {acao}")
        drone.ambiente.atualizar_estado(acao, drone.x, drone.y)
        print(f"Ambiente atualizado: {drone.ambiente.obter_estado(drone.x, drone.y)}")
        drone.movimentar()

        sleep(1)


if __name__ == "__main__":
    main()

