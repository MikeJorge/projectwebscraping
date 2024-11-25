import streamlit as st
import pandas as pd
import sqlite3

# Conectar ao banco de dados SQLite3
conn = sqlite3.connect('../data/quotes.db')

# Carregar os dados da tabela "mercadolivre_itens" em um DataFrame Pandas
df = pd.read_sql_query("SELECT * FROM mercadolivre_itens", conn)

# Fechar a conexão com o banco de dados
conn.close()

# Título da aplicação
st.title('Pesquisa de mercado - Tênis Esportivos no Mercado Livre')

# Melhorar o layout com colunas KPIs
st.subheader('KPIs principais do sistema')
col1, col2, col3 = st.columns(3)

# KPI 1: Número total de itens
total_itens = df.shape[0]
col1.metric(label="Número total de itens", value=total_itens)

# KPI 2: Número de marcas únicas
unique_brands = df['brand'].nunique()
col2.metric(label="Número de marcas únicas", value=unique_brands)

# KPI 3: Preço médio novo (em reais)
average_new_price = df['new_price'].mean()
col3.metric(label="Preço médio novo (R$)", value=f"{average_new_price:.2f}")

# Quais marcas são mais encontradas até a página 25° do website marketplace
st.subheader('Marcas mais encontradas até a página 25°')
col1, col2 = st.columns([4, 2])
top_25_pages_brands = df['brand'].value_counts().sort_values(ascending=False)
col1.bar_chart(top_25_pages_brands)
col2.write(top_25_pages_brands)

st.subheader('Preço médio por marca')

# Filtrar os dados para desconsiderar preços zero
df_filtered = df[df['new_price'] > 0]

# Calcular o preço médio por marca sem os valores zero e arredondar para 2 casas decimais
average_price_by_brand = (
    df_filtered.groupby('brand')['new_price']
    .mean()
    .sort_values(ascending=False)
    .round(2)  # Arredondar para duas casas decimais
)

# Configurar colunas para exibir os resultados
col1, col2 = st.columns([4, 2])

# Gráfico de barras com o preço médio por marca
col1.bar_chart(average_price_by_brand)

# Exibir a tabela com os preços médios arredondados
col2.write(average_price_by_brand)

# Qual a satisfação por produto
import pandas as pd

st.subheader('Satisfação por marca')

# Criar colunas para o layout
col1, col2 = st.columns([4, 2])

# Filtrar os dados para excluir valores zero
df_non_zero_reviews = df[df['reviews_rating_number'] > 0]

# Calcular a satisfação média por marca, arredondar e converter para string
satisfaction_by_brand = (
    df_non_zero_reviews.groupby('brand')['reviews_rating_number']
    .mean()
    .sort_values(ascending=False)
    .round(2)  # Arredondar para duas casas decimais
)

# Converter para string para alinhar os números à esquerda
satisfaction_by_brand = satisfaction_by_brand.apply(lambda x: f"{x:.2f}")

# Gráfico de barras com a satisfação por produto
col1.bar_chart(df_non_zero_reviews.groupby('brand')['reviews_rating_number'].mean())

# Exibir a tabela com números alinhados à esquerda
col2.write(satisfaction_by_brand)

