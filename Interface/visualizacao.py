import pygame
from utils.Tile import Tile

class Visualizacao:
    def __init__(self,ambiente, metricas=None, largura=600, altura=600, titulo="IA"):
        self.ambiente = ambiente
        self.metricas = metricas
        self.largura = largura
        self.altura = altura
        self.titulo = titulo
        self.cor_fundo = (34, 139, 34)
        self.cor_borda = (0, 0, 0)
        self.largura_borda = 4
        self.largura_menu = 0
        self.largura_cenario = self.largura
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
        self.carregar_assets()

    def carregar_assets(self):
        tam_celula_x = self.largura_cenario / self.ambiente.grid_size
        tam_celula_y = self.altura / self.ambiente.grid_size

        self.img_obstaculo = pygame.transform.scale(pygame.image.load("Interface/assets/obstaculo_2.png").convert_alpha(), (int(tam_celula_x), int(tam_celula_y)))
        self.img_fogo = pygame.transform.scale(pygame.image.load("Interface/assets/fogo2.png").convert_alpha(), (int(tam_celula_x), int(tam_celula_y)))
        self.img_vitima = pygame.transform.scale(pygame.image.load("Interface/assets/vitima.png").convert_alpha(), (int(tam_celula_x), int(tam_celula_y)))

        escala_agente = 0.7
        tam_agente_x = tam_celula_x * escala_agente
        tam_agente_y = tam_celula_y * escala_agente

        self.img_bombeiro = pygame.transform.scale(pygame.image.load("Interface/assets/bombeiro.png").convert_alpha(), (int(tam_agente_x), int(tam_agente_y)))
        self.img_socorrista_seq = pygame.transform.scale(pygame.image.load("Interface/assets/socorrista_seq.png").convert_alpha(), (int(tam_agente_x), int(tam_agente_y)))
        self.img_socorrista_otm = pygame.transform.scale(pygame.image.load("Interface/assets/socorrista_otm.png").convert_alpha(), (int(tam_agente_x), int(tam_agente_y)))
        self.img_drone = pygame.transform.scale(pygame.image.load("Interface/assets/drone.png").convert_alpha(), (int(tam_agente_x), int(tam_agente_y)))



    def desenhar_cenario(self, ambiente, bdi=None):
        if self.tela is None:
            return

        self.tela.fill(self.cor_fundo)
        
        tam_celula_x = self.largura_cenario / ambiente.grid_size
        tam_celula_y = self.altura / ambiente.grid_size

        # Desenhar grid e eventos
        for x in range(ambiente.grid_size):
            for y in range(ambiente.grid_size):
                estado = ambiente.obter_estado(x, y)
                rect_celula = (x * tam_celula_x, y * tam_celula_y, tam_celula_x, tam_celula_y)
                
                # Desenho fogo, vimita, obstaculo
                if estado == Tile.FOGO:
                    self.tela.blit(self.img_fogo, rect_celula) # Desenha a imagem do fogo
                    
                elif estado == Tile.VITIMA:
                    self.tela.blit(self.img_vitima, rect_celula) # Desenha a imagem da vítima
                    
                elif estado == Tile.OBSTACULO:
                    self.tela.blit(self.img_obstaculo, rect_celula) # Desenha a imagem do obstáculo   

                # linhas da grade
                pygame.draw.rect(self.tela, (50, 180, 50), rect_celula, 1) # Verde claro

        self._desenhar_indicadores_vitimas_designadas(ambiente, bdi, tam_celula_x, tam_celula_y)

        pygame.draw.rect(self.tela, self.cor_borda, (0,0,self.largura_cenario, self.altura), self.largura_borda)
        pygame.draw.line(self.tela, (0, 0, 0), (self.largura_cenario / 2, 0), (self.largura_cenario / 2, self.altura), 4) # Linha vertical grossa
        pygame.draw.line(self.tela, (0, 0, 0), (0, self.altura / 2), (self.largura_cenario, self.altura / 2), 4) # Linha horizontal grossa

        # Desenhar Hospital centralizado
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
            
            # cruz vermelha do hospital
            cx = h_rect[0] + h_rect[2] / 2
            cy = h_rect[1] + h_rect[3] / 2
            pygame.draw.rect(self.tela, (255, 0, 0), (cx - 4, cy - h_altura/4, 8, h_altura/2))
            pygame.draw.rect(self.tela, (255, 0, 0), (cx - h_largura/4, cy - 4, h_largura/2, 8))


    #essa funcao aqui é apenas para desenhar um pequeno circulo da cor do socorrista em cima da vitima.
    def _desenhar_indicadores_vitimas_designadas(self, ambiente, bdi, tam_celula_x, tam_celula_y):
        if not bdi:
            return

        vitimas_seq = set(getattr(bdi, "lista_resgate_sequencial", []))
        vitimas_otm = set(getattr(bdi, "lista_resgate_otimizador", []))
        vitimas_otm -= vitimas_seq
        raio = max(4, int(min(tam_celula_x, tam_celula_y) * 0.12))

        def desenhar_marcadores(vitimas, cor):
            for pos in vitimas:
                if not isinstance(pos, tuple) or len(pos) != 2:
                    continue

                x, y = pos
                if not (0 <= x < ambiente.grid_size and 0 <= y < ambiente.grid_size):
                    continue

                if ambiente.obter_estado(x, y) != Tile.VITIMA:
                    continue

                centro_x = int(x * tam_celula_x + tam_celula_x / 2)
                centro_y = int(y * tam_celula_y + tam_celula_y / 2)
                pygame.draw.circle(self.tela, cor, (centro_x, centro_y), raio)
                pygame.draw.circle(self.tela, (0, 0, 0), (centro_x, centro_y), raio, 1)

        desenhar_marcadores(vitimas_seq, (255, 255, 255))
        desenhar_marcadores(vitimas_otm, (255, 235, 59))

    def desenhar_agentes(self, ambiente, drones=None, bombeiros=None, socorrista_seq=None, socorrista_otm=None):
        if self.tela is None:
            return
            
        tam_celula_x = self.largura_cenario / ambiente.grid_size
        tam_celula_y = self.altura / ambiente.grid_size
        raio = int(min(tam_celula_x, tam_celula_y) / 3)

        escala_agente = 0.7
        tam_agente_x = tam_celula_x * escala_agente
        tam_agente_y = tam_celula_y * escala_agente
        fonte_bombeiro = pygame.font.SysFont("arial", max(12, int(tam_celula_y * 0.22)), bold=True)

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
                rect_x = centro_x - tam_celula_x / 2
                rect_y = centro_y - tam_celula_y / 2

                drone_x = rect_x + (tam_celula_x - tam_agente_x) / 2
                drone_y = rect_y + (tam_celula_y - tam_agente_y) / 2

                self.tela.blit(self.img_drone, (drone_x, drone_y))

        # Desenha os bombeiros
        if bombeiros:
            for bombeiro in bombeiros:
                centro_x, centro_y = interpolar(bombeiro)
                # Calculando o canto superior esquerdo da célula a partir do centro interpolado
                rect_x = centro_x - tam_celula_x / 2
                rect_y = centro_y - tam_celula_y / 2

                #centralizar a imagem do bombeiro no centro da célula
                bombeiro_x = rect_x + (tam_celula_x - tam_agente_x) / 2
                bombeiro_y = rect_y + (tam_celula_y - tam_agente_y) / 2
                
                # Desenha a imagem do bombeiro acompanhando o movimento
                self.tela.blit(self.img_bombeiro, (bombeiro_x, bombeiro_y))
                
                #Desenha o identificador do quadrante do bombeiroo
                texto_quadrante = fonte_bombeiro.render(bombeiro.quadrante.lower(), True, (255, 255, 255))
                texto_sombra = fonte_bombeiro.render(bombeiro.quadrante.lower(), True, (0, 0, 0))
                texto_x = int(centro_x - texto_quadrante.get_width() / 2)
                texto_y = int(bombeiro_y + tam_agente_y - texto_quadrante.get_height() / 2)
                self.tela.blit(texto_sombra, (texto_x + 1, texto_y + 1))
                self.tela.blit(texto_quadrante, (texto_x, texto_y))

        # Desenhar Socorrista Sequencial
        if socorrista_seq:
            centro_x, centro_y = interpolar(socorrista_seq)

            rect_x = centro_x - tam_celula_x / 2
            rect_y = centro_y - tam_celula_y / 2

            socorrista_seq_x = rect_x + (tam_celula_x - tam_agente_x) / 2
            socorrista_seq_y = rect_y + (tam_celula_y - tam_agente_y) / 2
            
            
            self.tela.blit(self.img_socorrista_seq, (socorrista_seq_x, socorrista_seq_y))
            

        # Desenhar Socorrista Otimizador
        if socorrista_otm:
            centro_x, centro_y = interpolar(socorrista_otm)
            # triangulo branco socorrista otimizador

            rect_x = centro_x - tam_celula_x / 2
            rect_y = centro_y - tam_celula_y / 2

            socorrista_otm_x = rect_x + (tam_celula_x - tam_agente_x) / 2
            socorrista_otm_y = rect_y + (tam_celula_y - tam_agente_y) / 2
            self.tela.blit(self.img_socorrista_otm, (socorrista_otm_x, socorrista_otm_y))

    def atualizar(self, ambiente, drones=None, bombeiros=None, socorrista_seq=None, socorrista_otm=None):
        if not self.running:
            return False
            
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                return False

        bdi = None
        if socorrista_seq and hasattr(socorrista_seq, "bdi"):
            bdi = socorrista_seq.bdi
        elif socorrista_otm and hasattr(socorrista_otm, "bdi"):
            bdi = socorrista_otm.bdi

        self.desenhar_cenario(ambiente, bdi=bdi)
        self.desenhar_agentes(ambiente, drones, bombeiros, socorrista_seq, socorrista_otm)
        pygame.display.flip()
        
        return True
