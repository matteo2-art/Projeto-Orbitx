# Desafio Técnico - OrbitX: Evolução de Satélites vs. Ciberataques

Este repositório contém o código desenvolvido para o desafio técnico da OrbitX. O objetivo é analisar e visualizar a correlação entre o crescimento exponencial de satélites no espaço e o aumento dos ciberataques ao longo dos anos.

## 🚀 Sobre o Projeto
O script Python (`analise_satelites_ataques.py`) recolhe dados de lançamentos espaciais e cruza-os com o histórico de incidentes de cibersegurança, gerando um gráfico de dois eixos.

* **Linha Azul (Satélites):** Representa o número cumulativo de satélites globais lançados, utilizando dados públicos (ex: UNOOSA / Our World in Data).
* **Barras Vermelhas (Ataques):** Representa incidentes de cibersegurança em infraestruturas espaciais, baseados na literatura e em relatórios de ameaças (ex: CSIS, ENISA).

## 📊 Análise de Dados e Visão de Negócio
Ao analisar o gráfico gerado, torna-se evidente que a transição para o "New Space" trouxe uma superfície de ataque sem precedentes. No entanto, os dados públicos sobre ciberataques a satélites são fragmentados e sub-reportados.

**Conclusão para a OrbitX:** Esta lacuna de dados limpos no setor valida perfeitamente a missão da OrbitX. Ao lançar um satélite para atuar como um *honeypot* (isca), a equipa conseguirá gerar uma base de dados proprietária de ataques reais. Estes dados serão fundamentais para treinar modelos preditivos de *Machine Learning*, criando uma solução de defesa comercialmente viável e inovadora para o mercado espacial.

## 🛠️ Tecnologias Utilizadas
* Python 3
* Pandas (Manipulação de dados e leitura de CSV)
* Matplotlib (Visualização de dados)
* Requests (Acesso a dados web)
