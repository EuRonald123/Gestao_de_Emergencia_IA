# Simulação de Agentes Inteligentes em Ambiente de Emergência

Este projeto implementa uma simulação de **Sistemas Multiagentes** focada no gerenciamento e resposta a emergências usando uma arquitetura em grid (matriz). O ambiente simula a ocorrência dinâmica de focos de incêndio e vítimas, utilizando diferentes tipos de agentes inteligentes, cada um projetado com arquiteturas específicas para resolver partes do problema.

## Objetivo
O principal objetivo do projeto é demonstrar, de forma prática, os diferentes tipos e arquiteturas de agentes inteligentes em Inteligência Artificial, mostrando como esses agentes podem colaborar (através de uma central inteligente / Agente BDI) para mitigar desastres, apagar incêndios e resgatar vítimas, tudo operando dentro de um ambiente com restrições e obstáculos.

---

## Estrutura do Projeto

* `main.py`: Ponto de entrada do sistema. Gerencia o loop da simulação, instancia o ambiente, os agentes, os componentes visuais, e controla as passagens de "tempo" e geração de eventos (fogo e  vítimas).
* `ambiente/`
    * `Ambiente.py`: Modela o grid do mundo. Controla onde cada entidade (Obstáculos, Hospital, Fogo, Vítimas, etc.) está posicionada, e calcula posições vazias, gerência quadrantes e serve como o sensor primário para o módulo de percepção dos agentes.
* `agentes/`
    * `AgenteBDI.py` (Crença, Desejo e Intenção): Atua como a "Central de Comando". Recebe percepções/alertas dos drones e delega as tarefas (apagar fogo ou resgatar vítima) para os bombeiros e socorristas baseados em suas localizações e status.
    * `AgenteReativoSimples.py` (Drones): Agentes simples que patrulham o grid. Caso identifiquem fogo ou vítimas, comunicam imediatamente ao agente BDI. Não possuem memória extensa.
    * `AgenteReativoBaseadoEmModelo.py` (Bombeiros): Contém um modelo de mundo e patrulham zonas específicas (quadrantes). Quando recebem uma tarefa do BDI, navegam de modo a apagar o incêndio.
    * `AgenteBaseadoEmObjetivo.py` (Socorrista Sequencial): Tem o objetivo claro de resgatar vítimas e deixá-las no hospital, atuando de maneira estrita à realização da meta.
    * `AgenteBaseadoEmUtilidade.py` (Socorrista Otimizador): Parecido com o baseado em objetivo, porém com uma função de utilidade para tomar a rota mais otimizada/menos custosa para o salvamento ou priorizar de forma mais inteligente.
* `Interface/`
    * `visualizacao.py`: Lida com a renderização gráfica do grid e dos agentes usando o PyGame, permitindo ver em tempo real o que está acontecendo (movimentação, incêndios instanciados e sendo apagados).
    * `assets/`: Imagens e sprites usados na renderização visual.
* `utils/`
    * `metricas.py`: Faz o rastreamento das ocorrências (quantos incêndios foram apagados, vítimas salvas, uso da CPU, tempo de execução, etc) gerando um dashboard no terminal durante ou pós simulação usando a biblioteca Rich.
    * `Tile.py`: Mapeamento de tipos/constantes (VAZIO, FOGO, VITIMA, HOSPITAL, OBSTACULO).
    * `requeriments.txt`: Dependências necessárias do projeto (Ex: `pygame==2.6.1`, `rich==13.9.4`).
* `docs/`: Outras documentações técnicas do sistema.

---

## Dinâmica da Simulação

1. **Inicialização das Entidades:** O grid é criado (ex: 10x10) contendo um "Hospital" no centro. Obstáculos são gerados de forma aleatória nas células vazias. Em seguida, as instâncias dos Drones, Bombeiros e Socorristas são posicionadas no mundo e ligadas ao BDI.
2. **Ciclo Aleatório de Eventos:** Após um certo número de passos (turnos), novas situações de emergência (50% fogo, 50% vítima) são dinamicamente injetadas no ambiente pela classe `Ambiente.py`.
3. **Percepção e Ação:** 
   - Os **Drones** patrulham o mapa. Ao baterem os "olhos" em fogo ou vítima, reportam as as coordenadas para o **Agente BDI**.
   - O **Agente BDI** processa essas crenças, gera a intenção de socorro/mitigação, e notifica o Bombeiro mais adequado (baseado no quadrante, por exemplo) para apagar o incêndio, ou os Socorristas para buscarem as vítimas e deixarem no Hospital.
   - **Bombeiros e Socorristas** calculam suas rotas e movem-se pelo grid desviando dos obstáculos e cumprindo suas funções estabelecidas.
4. **Métricas Visuais:** Você vai acompanhar com visualizações ricas a movimentação em 2D na tela via **PyGame** enquanto observa, direto pelo terminal com `rich`, os cálculos estatísticos através de uma interface interativa via CLI.

---

## Como Executar

### Pré-requisitos
Ter o Python instalado (Versão recomendada: >= 3.8).

**1. Clone o repositório ou navegue para o diretório raiz do projeto.**
```bash
cd Trabalho_1_IA
```

**2. Crie e ative um ambiente virtual**
*(Opcional mas recomendado)*
No Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```
No Linux/Mac:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**3. Instale as dependências**
```bash
pip install -r utils/requeriments.txt
```

**4. Rode a Simulação**
```bash
python main.py
```
*A janela do PyGame abrirá mostrando a simulação no ambiente 2D enquanto o terminal mostrará o dashboard dinâmico das métricas (passos, status do BDI, total de resgates, etc).*

---

## Arquitetura dos Agentes (Detalhado)

- **Agente BDI:** Funciona baseado na literatura de Crenças (o que ele sabe do mundo pelas mensagens dos Drones), Desejos (apagar fogos e salvar vítimas) e Intenções (enviar Bombeiro X ou Socorrista Y).
- **Agentes Reativos Simples:** Mapeado na abstração apenas na regra Condição-Ação sem se importar com um histórico complexo ou planejamento. 
- **Agentes Baseados em Modelo:** Mantém rastro sobre a situação global, permitindo agir quando não possuem a visualização exata do local (pois eles atualizam seu estado mental onde fica o fogo que ele deve apagar).
- **Agentes de Objetivo/Utilidade:** Avaliam os diferentes estados futuros. Um "caminha" simplesmente para sua premissa meta sem otimizar, o outro calcula caminhos mais curtos, avaliando custos ou desvios de obstáculos.

## Tecnologias Utilizadas
- **Python**: Linguagem de programação base.
- **Pygame**: Para visualização 2D espacial de sprites.
- **Rich**: Para manipulação robusta de textos e dashboards estáticos/animados no console.
