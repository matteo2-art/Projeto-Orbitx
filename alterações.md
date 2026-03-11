# Documentação Global de Alterações — Website OrbitX

Abaixo encontra-se o registo unificado de todas as implementações, otimizações e ajustes realizados no código original do website, organizados por categorias funcionais e visuais.

## 1. Estrutura, Layout e Responsividade
* **Responsividade Integral:** Expansão e refinamento das *media queries* (1024px, 870px, 768px, 480px e 360px) para garantir fluidez perfeita em qualquer dispositivo, incluindo a adaptação de grelhas (passando a coluna única em mobile) e menus compactados.
* **Nova Secção "CubeSat Showcase" (`#cubesat`):** Adição de uma área de destaque contendo um diagrama SVG interativo do satélite OrbitX-1U e as respetivas especificações técnicas.
* **Nova Secção "Ameaça Espacial" (`#ameaca`):** Implementação de um bloco com um gráfico interativo (via *Chart.js*), que ilustra a evolução temporal de ciberataques face aos satélites lançados.
* **Reorganização da Navegação:** A secção "Sobre Nós" foi movida para antes da secção "Missão", garantindo alinhamento perfeito com a ordem cronológica do menu (Início → Sobre Nós → Missão → Ameaça → Contacto).
* **Remoção de Meta Description:** A tag `<meta name="description">` original foi limpa do cabeçalho HTML.

## 2. Experiência do Utilizador (UX) e Interface (UI)
* **Redesign do Pop-up de Status (Hero):** O *badge* informativo foi redesenhado e tornado totalmente responsivo. Inclui agora um separador visual, um indicador verde pulsante de "Recrutamento Aberto" e um mini-botão de candidatura. O emoji original (🛰️) foi removido a pedido do utilizador para um tom mais sóbrio.
* **Intensidade Numérica nos Cartões:** A opacidade dos grandes números de fundo nos cartões de Valores (`.p-num`) foi aumentada significativamente (de 8% para 50%), destacando-se a vermelho sólido (`var(--red)`) aquando da interação com o rato.
* **Barra de Progresso de Leitura:** Implementação de uma fina linha vermelha fixa no topo do ecrã que acompanha o *scroll* do utilizador.
* **Contador do Formulário:** O campo de texto da mensagem conta agora com um indicador em tempo real de carateres inseridos (ex: "X / 500").
* **Indicador de Scroll Minimalista:** O texto "Scroll" foi suprimido do *Hero*, deixando apenas a linha vertical animada, resultando numa estética mais *clean*.

## 3. Animações e Efeitos Dinâmicos
* **Starfield Global (Fundo de Estrelas):** O canvas de estrelas, antes confinado ao topo, ocupa agora toda a página (`position: fixed`). As estrelas apresentam paralaxe 3D dinâmica ao movimento do rato (com amplitude aumentada para maior imersão) e cerca de 8% exibem um tom avermelhado subtil.
* **Motor de *Glitch* Textual:** Foi criado um efeito que baralha rapidamente os carateres (usando símbolos especiais) antes de revelar o texto. Aplica-se no título inicial (no carregamento, *hover* e aleatoriamente em *idle*), em todos os cabeçalhos de secção e gera uma aberração cromática no logótipo do rodapé.
* **Máquina de Escrever (*Typewriter*):** As pequenas *tags* temáticas das secções (`.s-tag`) surgem letre a letra, com um cursor piscante estilo terminal, assim que entram no ecrã.
* **Contadores de Estatísticas:** Todos os números em destaque (métricas do satélite no *Hero* e dados da Equipa) contam fluidamente do zero até ao valor estipulado através da deteção de *scroll*.
* **Efeito *Stagger* (Entrada em Cascata):** Elementos em lista — como *tags* dos serviços, especificações do CubeSat e colunas de links do rodapé — surgem de forma sequencial com micro-atrasos, criando entradas orgânicas.
* **Animação do Gráfico:** O gráfico Chart.js renderiza agora com uma animação fluida de entrada com duração de 1400ms.

## 4. Interatividade e Micro-Interações
* **Cursor Adaptativo:** O ponto de cursor vermelho aumenta de escala e transita para a cor branca de forma suave sempre que passa sobre elementos clicáveis.
* **Ripple no Clique:** Qualquer clique feito na página gera uma onda/argola vermelha expansiva a partir do ponto central do rato.
* **Botões Magnéticos:** Os botões principais sofrem atração gravitacional em direção ao rato durante a passagem (efeito *magnetic*).
* **Cartões com Tilt 3D:** Os blocos das secções "Valores" e "Serviços" inclinam-se em eixo X e Y consoante a posição do ponteiro, dando a ilusão de profundidade física.
* **Timeline Reativa:** Passar o rato ou clicar nos pontos (nós) do *roadmap* dispara a animação de um anel expansivo vermelho.
* **Hovers e Realces Adicionais:**
    * **Grelha de Instituições:** Os blocos emitem um brilho exterior (*glow*) e as siglas acendem a vermelho.
    * **Contactos Diretos:** Os ícones rodam ligeiramente sobre si próprios, emitindo uma sombra vermelha.
    * **Ícones Sociais (Footer):** Fazem um *spin* completo de 360 graus com um efeito de aceleração flexível.
    * **Sidebar de CTA:** O botão principal da caixa de recrutamento lateral emite um *glow* automático no exato momento em que o utilizador rola até à sua visualização.