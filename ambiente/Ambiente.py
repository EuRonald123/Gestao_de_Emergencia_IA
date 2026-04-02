import random
from utils.Tile import Tile

class Ambiente:
    def __init__(self, grid_size = 10):
        self.grid_size = grid_size

        self.fogos_ativos = 0
        self.vitimas_ativas = 0

        #criando a matriz para o ambiente
        self.matriz = []
        for i in range(grid_size):
            linha = []
            for j in range(grid_size):
                linha.append(Tile.VAZIO)
            self.matriz.append(linha)

        # Hospital no centro
        meio = grid_size // 2
        self.hospital_posicoes = [(meio-1, meio-1), (meio-1, meio), (meio, meio-1), (meio, meio)]
        for (hx, hy) in self.hospital_posicoes:
            self.matriz[hx][hy] = Tile.HOSPITAL


    #Funcao que retorna todas posições das casinhas vazias da matriz
    def calc_celulas_vazias(self):
        vazias = []
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if (self.matriz[i][j]==Tile.VAZIO):
                    vazias.append((i, j))

        if (not vazias):
            return None
        #se tiver celulas vazias, retorna a lista de celulas vazias
        return vazias


    '''nas funcoes de gerar fogoe  gerar vitima eu coloquei um teto maximo,
    porem, acredito que seja melhor deixar sem esse teto, vai ser configurável de qualquer maneira.'''
    def gerar_fogos(self, max_fogos = None):
        celulas_vazias = self.calc_celulas_vazias()
        if celulas_vazias == None:
            #print("Não há mais espaço para gerar fogos ou vitimas.") #remover depois ;-;
            return False

        if max_fogos is not None and self.fogos_ativos >= max_fogos:
            return False
        
        x,y = random.choice(celulas_vazias)
        self.matriz[x][y] = Tile.FOGO
        self.fogos_ativos += 1

        #print("__Fogo gerado na posição ({}, {})".format(x, y)) #remover depois
        return True

    def gerar_vitimas(self, max_vitimas = None):
        celulas_vazias = self.calc_celulas_vazias()
        if celulas_vazias == None:
            #print("Não há mais espaço para gerar fogos ou vitimas.") #esse printe é para debug e testes ininciais, vou remover depois kk
            return False

        if max_vitimas is not None and self.vitimas_ativas >= max_vitimas:
            return False
        
        x,y = random.choice(celulas_vazias)
        self.matriz[x][y] = Tile.VITIMA
        self.vitimas_ativas += 1

        #print("__Vitima gerada na posição ({}, {})".format(x, y)) #remover depois
        return True


    def apagar_fogo(self, x, y):
        if self.matriz[x][y] == Tile.FOGO:
            self.matriz[x][y] = Tile.VAZIO
            self.fogos_ativos -= 1
            #print("__Fogo apagado na posição ({}, {})".format(x, y)) #remover depois
            return True
        
        return False
    
    def resgatar_vitima(self, x, y):
        if self.matriz[x][y] == Tile.VITIMA:
            self.matriz[x][y] = Tile.VAZIO
            self.vitimas_ativas -= 1
            #print("__Vitima resgatada na posição ({}, {})".format(x, y)) #remover depois
            return True
        
        return False


    def obter_estado(self, x, y):
        #retorna o estado do ambiente na posição x, y
        return self.matriz[x][y]


    def obter_quadrante(self, x, y):
        meio = self.grid_size // 2
        if x < meio and y < meio:
            return 'Q1'   # Q1 
        elif x < meio and y >= meio:
            return 'Q2'   # Q2 
        elif x >= meio and y < meio:
            return 'Q3'   # Q3 
        else:
            return 'Q4'   # Q4 
        

    def gerar_obstaculos(self, quantidade):
        celulas_vazias = self.calc_celulas_vazias()
        if celulas_vazias is None:
            return False

        for _ in range(quantidade):
            if not celulas_vazias:
                break
            x, y = random.choice(celulas_vazias)
            self.matriz[x][y] = Tile.OBSTACULO
            celulas_vazias.remove((x, y))
        
        return True