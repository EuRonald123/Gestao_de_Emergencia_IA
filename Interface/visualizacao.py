import pygame
from utils.Tile import Tile

class Visualizacao:
    def __init__(self,ambiente, largura=600, altura=600, titulo="IA"):
        self.ambiente = ambiente
        self.largura = largura
        self.altura = altura
        self.titulo = titulo
        self.cor_fundo = (34, 139, 34)
        self.cor_borda = (0, 0, 0)
        self.largura_borda = 4
        self.running = False
        self.tela = None
        self.posicoes_agentes = {} # Guarda as posições x,y de animação de cada agente ativo
        self.velocidade_animacao = 0.1 # Controle de velocidade (0.1 a 1.0)
        self.clock = pygame.time.Clock()

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

        # Carrega a imagem e já transforma para o tamanho de uma única célula
        img_obstaculo = pygame.image.load("Interface/assets/obstaculo_2.png")
        img_obstaculo = pygame.transform.scale(img_obstaculo, (int(tam_celula_x), int(tam_celula_y)))

        img_fogo = pygame.image.load("Interface/assets/fogo2.png")
        img_fogo = pygame.transform.scale(img_fogo, (int(tam_celula_x), int(tam_celula_y)))

        

        # Desenhar grid e eventos
        for x in range(ambiente.grid_size):
            for y in range(ambiente.grid_size):
                estado = ambiente.obter_estado(x, y)
                rect_celula = (x * tam_celula_x, y * tam_celula_y, tam_celula_x, tam_celula_y)
                
                # Preencher a célula se houver fogo ou vítima
                if estado == Tile.FOGO:
                    self.tela.blit(img_fogo, rect_celula) # Desenha a imagem do fogo
                    #pygame.draw.rect(self.tela, (255, 69, 0), rect_celula) # Laranja Avermelhado (Fogo)
                elif estado == Tile.VITIMA:
                    pygame.draw.rect(self.tela, (30, 144, 255), rect_celula) # Azul (Vítima)
                elif estado == Tile.OBSTACULO:
                    self.tela.blit(img_obstaculo, rect_celula) # Desenha a imagem do obstáculo
                    #pygame.draw.rect(self.tela, (139, 69, 19), rect_celula) # Marrom (Obstáculo)

                # linhas da grade
                pygame.draw.rect(self.tela, (50, 180, 50), rect_celula, 1) # Verde claro
        pygame.draw.rect(self.tela, self.cor_borda, (0,0,self.largura, self.altura), self.largura_borda)
        pygame.draw.line(self.tela, (0, 0, 0), (self.largura / 2, 0), (self.largura / 2, self.altura), 4) # Linha vertical grossa
        pygame.draw.line(self.tela, (0, 0, 0), (0, self.altura / 2), (self.largura, self.altura / 2), 4) # Linha horizontal grossa

        # Desenhar Hospital centralizado (um único grande bloco com 1 cruz)
        if hasattr(ambiente, 'hospital_posicoes') and ambiente.hospital_posicoes:
            h_min_x = min([p[0] for p in ambiente.hospital_posicoes])
            h_min_y = min([p[1] for p in ambiente.hospital_posicoes])
            h_max_x = max([p[0] for p in ambiente.hospital_posicoes])
            h_max_y = max([p[1] for p in ambiente.hospital_posicoes])
            
            h_largura = (h_max_x - h_min_x + 1) * tam_celula_x
            h_altura = (h_max_y - h_min_y + 1) * tam_celula_y
            h_rect = (h_min_x * tam_celula_x, h_min_y * tam_celula_y, h_largura, h_altura)
            
            # Fundo branco do bloco único
            pygame.draw.rect(self.tela, (200, 200, 200), h_rect)
            
            # Uma única cruz vermelha grande no centro
            cx = h_rect[0] + h_rect[2] / 2
            cy = h_rect[1] + h_rect[3] / 2
            pygame.draw.rect(self.tela, (255, 0, 0), (cx - 4, cy - h_altura/4, 8, h_altura/2))
            pygame.draw.rect(self.tela, (255, 0, 0), (cx - h_largura/4, cy - 4, h_largura/2, 8))

    def desenhar_agentes(self, ambiente, drones=None, bombeiros=None, socorrista_seq=None, socorrista_otm=None):
        if self.tela is None:
            return
            
        tam_celula_x = self.largura / ambiente.grid_size
        tam_celula_y = self.altura / ambiente.grid_size
        raio = int(min(tam_celula_x, tam_celula_y) / 3)

        # Fator de tamanho (0.8 = 80% do tamanho da célula)
        escala_bombeiro = 0.7
        tam_bombeiro_x = tam_celula_x * escala_bombeiro
        tam_bombeiro_y = tam_celula_y * escala_bombeiro

        img_bombeiro = pygame.image.load("Interface/assets/bombeiro.png")
        img_bombeiro = pygame.transform.scale(img_bombeiro, (int(tam_bombeiro_x), int(tam_bombeiro_y)))

        # Função auxiliar de interpolação visual ("Tweening") -> efeito de movimento suave
        def interpolar(agente):
            alvo_x, alvo_y = agente.x, agente.y
            if id(agente) not in self.posicoes_agentes:
                self.posicoes_agentes[id(agente)] = [alvo_x, alvo_y]
            
            curr_x, curr_y = self.posicoes_agentes[id(agente)]
            novo_x = curr_x + (alvo_x - curr_x) * self.velocidade_animacao
            novo_y = curr_y + (alvo_y - curr_y) * self.velocidade_animacao
            
            if abs(alvo_x - novo_x) < 0.05: novo_x = alvo_x
            if abs(alvo_y - novo_y) < 0.05: novo_y = alvo_y
            
            self.posicoes_agentes[id(agente)] = [novo_x, novo_y]
            
            # Retorna as coordenadas para atualizar o desenho
            return int(novo_x * tam_celula_x + tam_celula_x / 2), int(novo_y * tam_celula_y + tam_celula_y / 2)

        # Desenha o drone
        if drones:
            for drone in drones:
                centro_x, centro_y = interpolar(drone)
                # Círculo cinza claro para o drone
                pygame.draw.circle(self.tela, (169, 169, 169), (centro_x, centro_y), raio)
                pygame.draw.circle(self.tela, (0, 0, 0), (centro_x, centro_y), raio, 2)

        # Desenha os bombeiros
        if bombeiros:
            for bombeiro in bombeiros:
                centro_x, centro_y = interpolar(bombeiro)
                # Calculando o canto superior esquerdo da célula a partir do centro interpolado
                rect_x = centro_x - tam_celula_x / 2
                rect_y = centro_y - tam_celula_y / 2

                #centralizar a imagem do bombeiro no centro da célula
                bombeiro_x = rect_x + (tam_celula_x - tam_bombeiro_x) / 2
                bombeiro_y = rect_y + (tam_celula_y - tam_bombeiro_y) / 2
                
                # Desenha a imagem do bombeiro acompanhando o movimento
                self.tela.blit(img_bombeiro, (bombeiro_x, bombeiro_y))

                # Círculo azul escuro para o bombeiro
                #pygame.draw.circle(self.tela, (0, 0, 139), (centro_x, centro_y), raio)
                #pygame.draw.circle(self.tela, (0, 0, 0), (centro_x, centro_y), raio, 2)

        # Desenhar Socorrista Sequencial
        if socorrista_seq:
            centro_x, centro_y = interpolar(socorrista_seq)
            # usei um tringulo de cor rosa 
            pontos = [
                (centro_x, centro_y - raio),
                (centro_x - raio, centro_y + raio),
                (centro_x + raio, centro_y + raio)
            ]
            pygame.draw.polygon(self.tela, (255, 105, 180), pontos)
            pygame.draw.polygon(self.tela, (0, 0, 0), pontos, 2)

        # Desenhar Socorrista Otimizador
        if socorrista_otm:
            centro_x, centro_y = interpolar(socorrista_otm)
            # triangulo branco socorrista otimizador
            pontos = [
                (centro_x, centro_y - raio),
                (centro_x - raio, centro_y + raio),
                (centro_x + raio, centro_y + raio)
            ]
            pygame.draw.polygon(self.tela, (255, 255, 255), pontos)
            pygame.draw.polygon(self.tela, (0, 0, 0), pontos, 2)

    def atualizar(self, ambiente, drones=None, bombeiros=None, socorrista_seq=None, socorrista_otm=None):
        if not self.running:
            return False
            
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                return False

        self.desenhar_cenario(ambiente)
        self.desenhar_agentes(ambiente, drones, bombeiros, socorrista_seq, socorrista_otm)
        pygame.display.flip()
        
        return True
