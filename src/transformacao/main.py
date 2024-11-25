# vamos importar o que precisamos
import pandas as pd
import sqlite3
from datetime import datetime

# Definir o caminho para o arquivo JSONL
file_path = r'C:\workspace-python\jornada-dados-py\projectwebscraping\data\data.jsonl'

try:
    # Ler o arquivo JSONL com pandas
    df = pd.read_json(file_path, lines=True)
    print(df)  # Exibe o conteúdo do DataFrame
except ValueError as e:
    print(f"Erro ao ler o arquivo JSONL: {e}")
except FileNotFoundError:
    print("Arquivo não encontrado. Verifique o caminho.")

# Setar o pandas para mostrar todas as colunas
pd.options.display.max_columns = None

# Adicionar a coluna_source com um valor fixo
df['_source'] = 'https://lista.mercadolivre.com.br/tenis-corrida?matt_tool=86626453&matt_word=Default_URL_MLB&matt_source=google&matt_campaign_id=11616247427&matt_ad_group_id=111803272303&matt_match_type=p&matt_network=g&matt_device=c&matt_creative=479753867413&matt_keyword=t%C3%AAnis%20de%20corrida%20mercado%20livre&matt_ad_position=&matt_ad_type=&matt_merchant_id=&matt_product_id=&matt_product_partition_id=&matt_target_id=aud-2009166904988:kwd-1018889522096&cq_src=google_ads&cq_cmp=11616247427&cq_net=g&cq_plt=gp&cq_med=&gad_source=1&gclid=CjwKCAiA9IC6BhA3EiwAsbltOEKI5CGsgACO8Kv4a4yQDmXyXixChQ3LicyO7eJKgiQLVLeTngSAuxoCubsQAvD_BwE'

# Adicionar a coluna_data_coleta com a data e hora atuais
df['_data_coleta'] = datetime.now()
print(df)

# Tratar os valores nulos para colunas numéricas e de texto
df['old_price_reais'] = df['old_price_reais'].fillna(0).astype(float)
df['old_price_centavos'] = df['old_price_centavos'].fillna(0).astype(float)
df['new_price_reais'] = df['new_price_reais'].fillna(0).astype(float)
df['new_price_centavos'] = df['new_price_centavos'].fillna(0).astype(float)
df['reviews_rating_number'] = df['reviews_rating_number'].fillna(0).astype(float)

# Remover os parênteses das colunas review_amount
df['reviews_amount'] = df['reviews_amount'].astype(str).str.replace(r'[\(\)]', '', regex=True)

# Remover caracteres indesejados e garantir que apenas números estejam na coluna
df['reviews_amount'] = df['reviews_amount'].str.extract(r'(\d+)', expand=False)

# Substituir valores nulos por zero
df['reviews_amount'] = df['reviews_amount'].fillna(0)

# Converter para inteiro
df['reviews_amount'] = df['reviews_amount'].astype(int)

# Tratar os preços como floats e calcular os valores totais
df['old_price'] = df['old_price_reais'] + df['old_price_centavos'] / 100
df['new_price'] = df['new_price_reais'] + df['new_price_centavos'] / 100

# Remover as colunas antigas de dados
df.drop(columns=['old_price_reais', 'old_price_centavos', 'new_price_reais', 'new_price_centavos'], inplace=True)

# Conectar ao banco de dados SQLite (ou criar um novo)
conn = sqlite3.connect('../data/quotes.db')

# Salvar o DataFrame no banco de dados SQLite3
df.to_sql('mercadolivre_itens', conn, if_exists='replace', index=False)

# Fechar a conexão com o BD
conn.close()
print(df.head())
