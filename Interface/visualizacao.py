import pygame
from utils.Tile import Tile

class Visualizacao:
    def __init__(self,ambiente, largura=600, altura=600, titulo="Ambiente"):
        self.ambiente = ambiente
        self.largura = largura
        self.altura = altura
        self.titulo = titulo
        self.cor_fundo = (34, 139, 34)
        self.cor_borda = (0, 0, 0)
        self.largura_borda = 4
        self.running = False
        self.tela = None

    def iniciar(self):
        pygame.init()
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption(self.titulo)
        self.running = True

    def desenhar_cenario(self, ambiente):
        if self.tela is None:
            return

        self.tela.fill(self.cor_fundo)
        
        tam_celula_x = self.largura / ambiente.grid_size
        tam_celula_y = self.altura / ambiente.grid_size

        # Desenhar grid e eventos
        for x in range(ambiente.grid_size):
            for y in range(ambiente.grid_size):
                estado = ambiente.obter_estado(x, y)
                rect_celula = (x * tam_celula_x, y * tam_celula_y, tam_celula_x, tam_celula_y)
                
                # Preencher a célula se houver fogo ou vítima
                if estado == Tile.FOGO:
                    pygame.draw.rect(self.tela, (255, 69, 0), rect_celula) # Laranja Avermelhado (Fogo)
                elif estado == Tile.VITIMA:
                    pygame.draw.rect(self.tela, (30, 144, 255), rect_celula) # Azul (Vítima)

                # Desenhar as linhas da grade
                pygame.draw.rect(self.tela, (50, 180, 50), rect_celula, 1) # Verde claro

        # Desenhar borda
        pygame.draw.rect(self.tela, self.cor_borda, (0,0,self.largura, self.altura), self.largura_borda)

    def desenhar_agentes(self, ambiente, drone=None, bombeiro=None, socorrista_seq=None, socorrista_otm=None):
        if self.tela is None:
            return
            
        tam_celula_x = self.largura / ambiente.grid_size
        tam_celula_y = self.altura / ambiente.grid_size
        raio = int(min(tam_celula_x, tam_celula_y) / 3) # O raio deve ser um pouco menor que a metade da celula
        
        # Desenhar Drone
        if drone:
            centro_x = int(drone.x * tam_celula_x + tam_celula_x / 2)
            centro_y = int(drone.y * tam_celula_y + tam_celula_y / 2)
            # Círculo cinza claro para o drone
            pygame.draw.circle(self.tela, (169, 169, 169), (centro_x, centro_y), raio)
            pygame.draw.circle(self.tela, (0, 0, 0), (centro_x, centro_y), raio, 2)

        # Desenhar Bombeiro
        if bombeiro:
            centro_x = int(bombeiro.x * tam_celula_x + tam_celula_x / 2)
            centro_y = int(bombeiro.y * tam_celula_y + tam_celula_y / 2)
            # Círculo azul escuro para o bombeiro
            pygame.draw.circle(self.tela, (0, 0, 139), (centro_x, centro_y), raio)
            pygame.draw.circle(self.tela, (0, 0, 0), (centro_x, centro_y), raio, 2)

        # Desenhar Socorrista Sequencial
        if socorrista_seq:
            centro_x = int(socorrista_seq.x * tam_celula_x + tam_celula_x / 2)
            centro_y = int(socorrista_seq.y * tam_celula_y + tam_celula_y / 2)
            # Triângulo rosa
            pontos = [
                (centro_x, centro_y - raio),
                (centro_x - raio, centro_y + raio),
                (centro_x + raio, centro_y + raio)
            ]
            pygame.draw.polygon(self.tela, (255, 105, 180), pontos)
            pygame.draw.polygon(self.tela, (0, 0, 0), pontos, 2)

        # Desenhar Socorrista Otimizador
        if socorrista_otm:
            centro_x = int(socorrista_otm.x * tam_celula_x + tam_celula_x / 2)
            centro_y = int(socorrista_otm.y * tam_celula_y + tam_celula_y / 2)
            # Triângulo branco
            pontos = [
                (centro_x, centro_y - raio),
                (centro_x - raio, centro_y + raio),
                (centro_x + raio, centro_y + raio)
            ]
            pygame.draw.polygon(self.tela, (255, 255, 255), pontos)
            pygame.draw.polygon(self.tela, (0, 0, 0), pontos, 2)

    def atualizar(self, ambiente, drone=None, bombeiro=None, socorrista_seq=None, socorrista_otm=None):
        if not self.running:
            return False
            
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                return False

        self.desenhar_cenario(ambiente)
        self.desenhar_agentes(ambiente, drone, bombeiro, socorrista_seq, socorrista_otm)
        pygame.display.flip()
        
        return True
