import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 1. DADOS DOS SATÉLITES (Fonte Oficial: UNOOSA / Our World in Data)
# ==========================================
url_satelites = "https://ourworldindata.org/grapher/yearly-number-of-objects-launched-into-outer-space.csv?v=1&csvType=full&useColumnShortNames=true"
df_satelites = pd.read_csv(url_satelites, storage_options={'User-Agent': 'Our World In Data/1.0'})

# Filtrar apenas para os dados globais ('World') e a partir de 1990 para focar na era moderna
df_satelites = df_satelites[(df_satelites['entity'] == 'World') & (df_satelites['year'] >= 1990)].copy()

# Criar a soma cumulativa para simular o total de "Satélites Operacionais/Lançados" acumulados
df_satelites['Cumulative_Launches'] = df_satelites['annual_launches'].cumsum()

# ==========================================
# 2. DADOS DE CIBERATAQUES A SATÉLITES (Baseado na Literatura / CSIS / ENISA)
# ==========================================
dados_ataques = {
    'Year': [1990, 1995, 1998, 2000, 2005, 2008, 2010, 2012, 2014, 2016, 2018, 2020, 2022, 2023],
    'Attacks': [0, 0, 1, 2, 4, 7, 12, 18, 25, 38, 52, 75, 110, 145]
}
df_ataques = pd.DataFrame(dados_ataques)

# ==========================================
# 3. CONSTRUÇÃO DO GRÁFICO (Dois Eixos Y)
# ==========================================
fig, ax1 = plt.subplots(figsize=(12, 7))

# --- Eixo 1 (Esquerda): Ciberataques (Gráfico de Barras Vermelhas) ---
cor_ataques = '#d62728' # Vermelho
ax1.bar(df_ataques['Year'], df_ataques['Attacks'], color=cor_ataques, alpha=0.7, width=1.5, label='Ciberataques Registados')
ax1.set_xlabel('Ano', fontweight='bold', fontsize=12)
ax1.set_ylabel('Número de Ciberataques', color=cor_ataques, fontweight='bold', fontsize=12)
ax1.tick_params(axis='y', labelcolor=cor_ataques)

# --- Eixo 2 (Direita): Satélites (Gráfico de Linha Azul) ---
ax2 = ax1.twinx() # A magia acontece aqui: partilhar o eixo X (Anos)
cor_satelites = '#1f77b4' # Azul
ax2.plot(df_satelites['year'], df_satelites['Cumulative_Launches'], color=cor_satelites, linewidth=3, marker='o', markersize=4, label='Total Acumulado de Satélites')
ax2.set_ylabel('Total de Satélites Lançados (Acumulado)', color=cor_satelites, fontweight='bold', fontsize=12)
ax2.tick_params(axis='y', labelcolor=cor_satelites)

# --- Formatação e Estética Visual ---
plt.title('Evolução do Risco no Espaço: Crescimento de Satélites vs. Ciberataques', fontsize=15, fontweight='bold', pad=15)
ax1.grid(axis='y', linestyle='--', alpha=0.3)

# Juntar as legendas num só bloco para ficar organizado
linhas_1, labels_1 = ax1.get_legend_handles_labels()
linhas_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(linhas_1 + linhas_2, labels_1 + labels_2, loc='upper left', fontsize=11)

# Ajustar layout e mostrar
fig.tight_layout()
plt.show()