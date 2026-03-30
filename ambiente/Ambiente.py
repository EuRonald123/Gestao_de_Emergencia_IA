from utils.Tile import Tile

class Ambiente:
    def __init__(self, grid_size = 10):
        self.grid_size = grid_size


        #criando a matriz para o ambiente
        self.matriz = []
        for i in range(grid_size):
            linha = []
            for j in range(grid_size):
                linha.append(Tile.VAZIO)
            self.matriz.append(linha)

        self.matriz[2][3] = Tile.FOGO
        self.matriz[5][5] = Tile.VITIMA
        self.matriz[9][9] = Tile.FOGO


    def obter_estado(self, x, y):
        #retorna o estado do ambiente na posição x, y
        return self.matriz[x][y]
    
    def atualizar_estado(self, acao, x, y):
        if acao == 'Apagar Fogo':
            self.matriz[x][y] = Tile.VAZIO
        elif acao == 'Proximo local':
            self.matriz[x][y] = Tile.VAZIO
        elif acao == 'Resgatar Vitima':
            self.matriz[x][y] = Tile.VAZIO
        else:
            pass