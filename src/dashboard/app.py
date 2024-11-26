import os
import sqlite3
import pandas as pd
import streamlit as st

# Função para obter o caminho absoluto do banco de dados
def get_database_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, '..', '..', 'data', 'quotes.db')

# Função para verificar se o banco de dados existe
def check_database_exists(db_path):
    if not os.path.exists(db_path):
        st.error(f"Banco de dados não encontrado no caminho: {db_path}")
        st.stop()

# Função principal
def main():
    # Obter o caminho do banco de dados
    db_path = get_database_path()

    # Verificar a existência do banco de dados
    check_database_exists(db_path)

    # Conectar ao banco de dados e carregar os dados
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT * FROM mercadolivre_itens", conn)
        conn.close()
    except sqlite3.OperationalError as e:
        st.error(f"Erro ao acessar o banco de dados: {e}")
        st.stop()

    # Aplicação Streamlit
    st.title('Pesquisa de mercado - Tênis Esportivos no Mercado Livre')

    # KPIs principais
    st.subheader('KPIs principais do sistema')
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Número total de itens", value=df.shape[0])
    col2.metric(label="Número de marcas únicas", value=df['brand'].nunique())
    col3.metric(label="Preço médio novo (R$)", value=f"{df['new_price'].mean():.2f}")

    # Marcas mais encontradas
    st.subheader('Marcas mais encontradas até a página 25°')
    col1, col2 = st.columns([4, 2])
    top_25_pages_brands = df['brand'].value_counts().sort_values(ascending=False)
    col1.bar_chart(top_25_pages_brands)
    col2.write(top_25_pages_brands)

    # Preço médio por marca
    st.subheader('Preço médio por marca')
    df_filtered = df[df['new_price'] > 0]  # Filtrar preços maiores que zero
    average_price_by_brand = (
        df_filtered.groupby('brand')['new_price']
        .mean()
        .sort_values(ascending=False)
        .round(2)
    )
    col1, col2 = st.columns([4, 2])
    col1.bar_chart(average_price_by_brand)
    col2.write(average_price_by_brand)

    # Satisfação por marca
    st.subheader('Satisfação por marca')
    col1, col2 = st.columns([4, 2])
    df_non_zero_reviews = df[df['reviews_rating_number'] > 0]
    satisfaction_by_brand = (
        df_non_zero_reviews.groupby('brand')['reviews_rating_number']
        .mean()
        .sort_values(ascending=False)
        .round(2)
    )
    col1.bar_chart(df_non_zero_reviews.groupby('brand')['reviews_rating_number'].mean())
    col2.write(satisfaction_by_brand)

# Garantir que a função main seja chamada apenas quando o script for executado diretamente
if __name__ == "__main__":
    main()
