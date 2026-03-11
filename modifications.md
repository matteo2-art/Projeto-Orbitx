# Documentação Global de Alterações — Website OrbitX

Registo unificado de todas as implementações, otimizações e ajustes realizados ao código original do website, listados por ordem cronológica de implementação.

---

1. **Barra de Progresso de Leitura** — Adicionada uma fina linha vermelha fixa no topo do ecrã (`#scroll-progress`, `z-index: 200`) que acompanha o *scroll* do utilizador em tempo real.

2. ***Starfield* Global (Fundo de Estrelas)** — O canvas de estrelas foi movido de `position: absolute` (confinado ao *Hero*) para `position: fixed`, cobrindo a totalidade da página. As 260 estrelas apresentam paralaxe 3D dinâmica ao movimento do rato (amplitude de 70px horizontal e 45px vertical) e cerca de 8% exibem um tom avermelhado subtil.

3. ***Ripple* no Clique** — Qualquer clique na página gera uma onda/argola vermelha expansiva (`.ripple-dot`) a partir do ponto exato do rato, que desaparece automaticamente após a animação.

4. **Motor de *Glitch* Textual** — Efeito que baralha rapidamente os carateres do título principal usando símbolos especiais (`GLITCH_CHARS`) antes de revelar o texto definitivo. Dispara no carregamento da página, no *hover* e aleatoriamente em *idle*. Aplica-se também em todos os cabeçalhos de secção (via `IntersectionObserver`) e gera aberração cromática no logótipo do rodapé ao *hover*.

5. **Máquina de Escrever (*Typewriter*)** — As *tags* temáticas das secções (`.s-tag`) surgem letra a letra, com um cursor piscante estilo terminal, quando entram no campo de visão do utilizador.

6. **Contadores de Estatísticas Animados** — Todos os números em destaque (métricas do satélite no *Hero* e dados da Equipa) contam fluidamente do zero até ao valor definido, ativados por `IntersectionObserver` ao entrar no ecrã.

7. **Botões Magnéticos** — Os botões principais (`.btn-p`, `.btn-g`, `.n-cta`) sofrem atração gravitacional em direção ao rato durante a passagem, recalculando a translação em cada `mousemove`.

8. ***Tilt* 3D nos Cartões** — Os blocos das secções "Valores" e "Serviços" (`.sc`, `.p-card`) inclinam-se nos eixos X e Y consoante a posição do ponteiro, criando uma ilusão de profundidade física.

9. **Timeline Reativa** — Passar o rato ou clicar nos nós do *roadmap* dispara a animação de um anel expansivo vermelho à volta do ponto selecionado.

10. ***Stagger* de Entrada em Cascata** — Elementos em lista (tags de serviços, especificações do CubeSat e colunas de links do rodapé) surgem sequencialmente com micro-atrasos, criando entradas orgânicas e fluidas.

11. **Grelha de Instituições com *Glow*** — Os blocos da grelha de parceiros emitem um brilho exterior ao *hover* e as respetivas siglas acendem a vermelho.

12. **Animação dos Ícones de Contacto** — Os ícones dos contactos diretos rodam ligeiramente sobre si próprios ao *hover*, emitindo uma sombra vermelha.

13. **Ícones Sociais com *Spin* 360°** — Os ícones das redes sociais no rodapé executam uma rotação completa de 360° com efeito de aceleração flexível ao *hover*.

14. ***Glow* Automático na *Sidebar* de CTA** — O botão principal da caixa de recrutamento lateral emite um *glow* pulsante no momento em que o utilizador chega à sua área de visualização.

15. **Cursor Adaptativo** — O cursor personalizado (ponto vermelho) aumenta de escala e transita suavemente para a cor branca sempre que passa sobre elementos clicáveis.

16. **Animação de Entrada no Gráfico** — O gráfico *Chart.js* renderiza com uma animação fluida de entrada (`duration: 1400ms`, `easing: easeOutQuart`).

17. **Nova Secção "CubeSat Showcase" (`#cubesat`)** — Adição de uma área de destaque com um diagrama SVG interativo do satélite OrbitX-1U e as respetivas especificações técnicas em grelha.

18. **Nova Secção "Ameaça Espacial" (`#ameaca`)** — Implementação de um bloco com gráfico interativo (*Chart.js*, tipo misto barra + linha) que ilustra a evolução temporal de ciberataques face ao número de satélites ativos desde 1957.

19. **Reorganização da Navegação** — A secção "Sobre Nós" foi movida para antes da secção "Missão", alinhando a ordem do conteúdo com o menu de navegação (Início → Sobre Nós → Missão → Ameaça → Contacto).

20. **Redesign do *Badge* de Status (*Hero*)** — O indicador informativo foi completamente redesenhado: inclui agora o título "Status da Missão", um separador visual, um indicador verde pulsante de "Recrutamento Aberto" e um mini-botão de candidatura com ligação direta ao formulário Google Forms.

21. **Remoção do Indicador de *Scroll*** — O texto "Scroll" e a linha vermelha animada foram removidos do *Hero*, simplificando o layout inferior da secção.

22. **Intensidade Numérica nos Cartões de Valores** — A opacidade dos grandes números de fundo nos cartões (`.p-num`) foi aumentada de 8% para 50%, com transição para vermelho sólido (`var(--red)`) ao *hover*.

23. **Responsividade Integral** — Expansão e refinamento das *media queries* (1024px, 870px, 768px, 480px e 360px) para garantir fluidez total em qualquer dispositivo, incluindo adaptação de grelhas para coluna única em mobile e menus compactados.

24. **Contador de Carateres no Formulário** — O campo de mensagem exibe um indicador em tempo real do número de carateres inseridos (ex: "X / 500").

25. **Remoção da Meta Description** — A tag `<meta name="description">` original foi removida do cabeçalho HTML.

26. **Correção do Email no Rodapé** — O endereço de email na coluna "Contactos" do rodapé foi atualizado para `orbitx.geral@gmail.com`, substituindo o endereço anterior ofuscado pelo Cloudflare. O link do ícone de email na secção de redes sociais foi igualmente atualizado.

27. ***Pipeline* de Dados Automatizado para o Gráfico** — Os dados do gráfico da secção `#ameaca` foram desacoplados do HTML. O `index.html` passa a carregar os dados de forma assíncrona via `fetch('chart_data.json')`. Um script Python independente (`generate_chart_data.py`) trata da extração, processamento e geração do ficheiro JSON, seguindo a arquitetura:

    - **Extração (*Fetch*):** Descarrega o ficheiro `stat001.txt` diretamente da fonte autoritativa *Jonathan's Space Report* (JSR / McDowell, `planet4589.org`), usando um `User-Agent` identificado.
    - **Processamento (*Parse*):** Analisa o ficheiro linha a linha, extrai a coluna `AC` (*active payloads*) e captura o valor de 31 de dezembro de cada ano da lista `CHART_YEARS` (último registo do ano = *snapshot* de fim de ano).
    - **Combinação:** Cruza os dados de satélites obtidos dinamicamente com o dicionário `CYBER_INCIDENTS` (curado manualmente a partir de relatórios de inteligência — *Space ISAC*, ETH Zürich CSS, Mayer Brown, Ear et al. arXiv:2309.04878, CSIS STA 2018–2025).
    - **Validação:** Verifica a integridade do *payload* antes de escrever (comprimento dos arrays, contagens negativas, anos sem dados).
    - **Exportação Atómica:** Escreve o `chart_data.json` via padrão *temp-then-rename*, evitando ficheiros corrompidos em caso de interrupção.
    - **Tratamento de Erros no Frontend:** Se o `chart_data.json` não for encontrado, o `index.html` exibe uma mensagem de erro não intrusiva dentro da área do gráfico, sem quebrar o resto da página.
    - **Automatização:** O script pode ser agendado com `cron` (ex: semanalmente) ou integrado numa *GitHub Action* para atualização automática sem intervenção manual.

28. **Atualização das Legendas e Fontes do Gráfico** — A barra superior do cartão do gráfico foi melhorada em legibilidade e rigor científico:

    - O tamanho do texto das legendas (`.chart-legend-item`) foi aumentado de `0.65rem` para `0.72rem` e a cor passou de muted para `rgba(255,255,255,.75)`, tornando-as claramente legíveis.
    - O indicador de estado foi atualizado de `"Fonte: UNOOSA / CSIS / ENISA"` (desatualizado) para `"Live · JSR / Space ISAC / CSIS STA"`, refletindo as fontes reais e o facto de os dados serem atualizados automaticamente.
    - Foi adicionada uma nova barra de fontes (`.chart-sources-bar`) sob a legenda, com referência explícita às quatro fontes autoritativas utilizadas: *Jonathan McDowell / JSR stat001.txt* (satélites), *Space ISAC & ETH Zürich CSS* (ciberataques 2020–2025), *Ear et al. arXiv:2309.04878* (baseline 1977–2022) e *CSIS Space Threat Assessment 2018–2025*.

29. **GitHub Action para Atualização Semanal Automática** — Criado o ficheiro `.github/workflows/update_chart_data.yml` que automatiza completamente o *pipeline* de dados sem necessidade de intervenção manual:

    - Corre **todos os domingos às 03:00 UTC** (via `cron`) e também pode ser acionado manualmente pelo separador *Actions* do GitHub.
    - Instala as dependências Python, executa `generate_chart_data.py`, e faz `commit` + `push` do `chart_data.json` atualizado caso os dados tenham mudado.
    - Se os dados forem idênticos aos da semana anterior, o workflow termina sem criar um commit vazio (comportamento idempotente).
    - O *GitHub Pages* serve automaticamente o ficheiro atualizado, tornando o gráfico do site *live* sem qualquer intervenção.