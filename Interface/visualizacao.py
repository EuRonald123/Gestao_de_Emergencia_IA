import pygame
from utils.Tile import Tile

class Visualizacao:
    def __init__(self,ambiente, metricas=None, largura=900, altura=600, titulo="IA"):
        self.ambiente = ambiente
        self.metricas = metricas
        self.largura = largura
        self.altura = altura
        self.titulo = titulo
        self.cor_fundo = (34, 139, 34)
        self.cor_borda = (0, 0, 0)
        self.largura_borda = 4
        self.largura_menu = 280
        self.largura_cenario = self.largura - self.largura_menu
        self.running = False
        self.tela = None
        self.posicoes_agentes = {} # Guarda as posições x,y de animação de cada agente ativo
        self.velocidade_animacao = 0.1 # Controle de velocidade (0.1 a 1.0)
        self.clock = pygame.time.Clock()
        self.modo_painel = "metricas"
        self.opcoes_painel = ["metricas", "mensagens"]
        self.indice_opcao = 0

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



    def desenhar_cenario(self, ambiente):
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
                
                # Preencher a célula se houver fogo ou vítima
                if estado == Tile.FOGO:
                    self.tela.blit(self.img_fogo, rect_celula) # Desenha a imagem do fogo
                    
                elif estado == Tile.VITIMA:
                    self.tela.blit(self.img_vitima, rect_celula) # Desenha a imagem da vítima
                    
                elif estado == Tile.OBSTACULO:
                    self.tela.blit(self.img_obstaculo, rect_celula) # Desenha a imagem do obstáculo
                    

                # linhas da grade
                pygame.draw.rect(self.tela, (50, 180, 50), rect_celula, 1) # Verde claro
        pygame.draw.rect(self.tela, self.cor_borda, (0,0,self.largura_cenario, self.altura), self.largura_borda)
        pygame.draw.line(self.tela, (0, 0, 0), (self.largura_cenario / 2, 0), (self.largura_cenario / 2, self.altura), 4) # Linha vertical grossa
        pygame.draw.line(self.tela, (0, 0, 0), (0, self.altura / 2), (self.largura_cenario, self.altura / 2), 4) # Linha horizontal grossa

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
            
        tam_celula_x = self.largura_cenario / ambiente.grid_size
        tam_celula_y = self.altura / ambiente.grid_size
        raio = int(min(tam_celula_x, tam_celula_y) / 3)

        escala_agente = 0.7
        tam_agente_x = tam_celula_x * escala_agente
        tam_agente_y = tam_celula_y * escala_agente

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
                #pygame.draw.circle(self.tela, (169, 169, 169), (centro_x, centro_y), raio)
                #pygame.draw.circle(self.tela, (0, 0, 0), (centro_x, centro_y), raio, 2)

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

                # Círculo azul escuro para o bombeiro
                #pygame.draw.circle(self.tela, (0, 0, 139), (centro_x, centro_y), raio)
                #pygame.draw.circle(self.tela, (0, 0, 0), (centro_x, centro_y), raio, 2)

        # Desenhar Socorrista Sequencial
        if socorrista_seq:
            centro_x, centro_y = interpolar(socorrista_seq)

            rect_x = centro_x - tam_celula_x / 2
            rect_y = centro_y - tam_celula_y / 2

            socorrista_seq_x = rect_x + (tam_celula_x - tam_agente_x) / 2
            socorrista_seq_y = rect_y + (tam_celula_y - tam_agente_y) / 2
            
            
            '''# usei um tringulo de cor rosa 

            pontos = [
                (centro_x, centro_y - raio),
                (centro_x - raio, centro_y + raio),
                (centro_x + raio, centro_y + raio)
            ]
            '''
            self.tela.blit(self.img_socorrista_seq, (socorrista_seq_x, socorrista_seq_y))
            
            #pygame.draw.polygon(self.tela, (255, 105, 180), pontos)
            #pygame.draw.polygon(self.tela, (0, 0, 0), pontos, 2)

        # Desenhar Socorrista Otimizador
        if socorrista_otm:
            centro_x, centro_y = interpolar(socorrista_otm)
            # triangulo branco socorrista otimizador
            '''
             pontos = [
                (centro_x, centro_y - raio),
                (centro_x - raio, centro_y + raio),
                (centro_x + raio, centro_y + raio)
            ]
            pygame.draw.polygon(self.tela, (255, 255, 255), pontos)
            pygame.draw.polygon(self.tela, (0, 0, 0), pontos, 2)
            '''
            rect_x = centro_x - tam_celula_x / 2
            rect_y = centro_y - tam_celula_y / 2

            socorrista_otm_x = rect_x + (tam_celula_x - tam_agente_x) / 2
            socorrista_otm_y = rect_y + (tam_celula_y - tam_agente_y) / 2
            self.tela.blit(self.img_socorrista_otm, (socorrista_otm_x, socorrista_otm_y))

    def desenhar_menu_lateral(self):
        area_x = self.largura_cenario
        area_largura = self.largura_menu
        pygame.draw.rect(self.tela, (20, 20, 20), (area_x, 0, area_largura, self.altura))

        fonte_titulo = pygame.font.SysFont("arial", 28, bold=True)
        fonte_item = pygame.font.SysFont("arial", 22, bold=False)
        fonte_texto = pygame.font.SysFont("arial", 20, bold=False)

        #define o titulo da janela da met e mens
        titulo = fonte_titulo.render("Painel", True, (255, 255, 255))
        
        
        self.tela.blit(titulo, (area_x + 20, 20))

        for i, opcao in enumerate(self.opcoes_painel):
            selecionado = i == self.indice_opcao
            cor_fundo = (70, 70, 70) if selecionado else (40, 40, 40)
            cor_texto = (255, 255, 255) if selecionado else (180, 180, 180)
            caixa_y = 70 + i * 44
            pygame.draw.rect(self.tela, cor_fundo, (area_x + 20, caixa_y, area_largura - 40, 34), border_radius=6)
            texto = fonte_item.render(opcao.capitalize(), True, cor_texto)
            self.tela.blit(texto, (area_x + 30, caixa_y + 6))

        pygame.draw.line(self.tela, (90, 90, 90), (area_x + 20, 170), (area_x + area_largura - 20, 170), 1)

        if self.modo_painel == "metricas":
            self._desenhar_metricas(area_x, fonte_texto, fonte_item)
        else:
            placeholder = fonte_texto.render("Mensagens: em breve", True, (230, 230, 230))
            self.tela.blit(placeholder, (area_x + 20, 190))

    def _desenhar_metricas(self, area_x, fonte_texto, fonte_item):
        if not self.metricas:
            sem_dados = fonte_texto.render("Sem metricas", True, (230, 230, 230))
            self.tela.blit(sem_dados, (area_x + 20, 190))
            return

        snapshot = self.metricas.obter_snapshot()
        seq = snapshot.get("sequencial", {"qtd_vitimas": 0, "qtd_passos": 0})
        otm = snapshot.get("otimizador", {"qtd_vitimas": 0, "qtd_passos": 0})

        titulo_seq = fonte_item.render("Sequencial", True, (255, 255, 255))
        self.tela.blit(titulo_seq, (area_x + 20, 190))
        self.tela.blit(fonte_texto.render(f"qtd_vitimas: {seq['qtd_vitimas']}", True, (210, 210, 210)), (area_x + 20, 220))
        self.tela.blit(fonte_texto.render(f"qtd_passos: {seq['qtd_passos']}", True, (210, 210, 210)), (area_x + 20, 248))

        titulo_otm = fonte_item.render("Otimizador", True, (255, 255, 255))
        self.tela.blit(titulo_otm, (area_x + 20, 300))
        self.tela.blit(fonte_texto.render(f"qtd_vitimas: {otm['qtd_vitimas']}", True, (210, 210, 210)), (area_x + 20, 330))
        self.tela.blit(fonte_texto.render(f"qtd_passos: {otm['qtd_passos']}", True, (210, 210, 210)), (area_x + 20, 358))
        

    def atualizar(self, ambiente, drones=None, bombeiros=None, socorrista_seq=None, socorrista_otm=None):
        if not self.running:
            return False
            
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    self.indice_opcao = (self.indice_opcao - 1) % len(self.opcoes_painel)
                elif evento.key == pygame.K_DOWN:
                    self.indice_opcao = (self.indice_opcao + 1) % len(self.opcoes_painel)
                elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    self.modo_painel = self.opcoes_painel[self.indice_opcao]

        self.desenhar_cenario(ambiente)
        self.desenhar_agentes(ambiente, drones, bombeiros, socorrista_seq, socorrista_otm)
        self.desenhar_menu_lateral()
        pygame.display.flip()
        
        return True
