# Projeto: Webscraping para Análise de Mercado
Este projeto foi desenvolvido para realizar uma análise de mercado detalhada de tênis esportivos utilizando webscraping. Ele captura dados de um marketplace popular e apresenta os resultados em um dashboard interativo.

🛠 Funcionalidades
Coleta de Dados Automatizada:
Utiliza técnicas de webscraping para extrair informações de produtos, como:

Marca;
Preço;
Avaliações e outros dados relevantes.
Análise de Dados:
Geração de insights a partir dos dados coletados, como:

Número total de itens coletados;
Número de marcas únicas;
Preço médio dos produtos;
Satisfação por marca (baseada em avaliações).
Visualização Interativa:
Dashboard dinâmico desenvolvido com Streamlit, que apresenta:

KPIs principais;
Gráficos de barras;
Tabelas detalhadas.
Armazenamento Estruturado:
Os dados extraídos são armazenados em um banco de dados SQLite, garantindo persistência e fácil reuso.

🎯 Objetivo
Este projeto demonstra como técnicas de webscraping podem ser combinadas com ferramentas de análise de dados para fornecer insights estratégicos. Ele é útil para empresas e pesquisadores que desejam entender melhor o mercado de um produto específico.

🚀 Tecnologias Utilizadas
Python: Linguagem base do projeto;
Scrapy: Framework para web scraping;
SQLite: Banco de dados para armazenamento dos dados coletados;
pandas: Processamento e manipulação de dados;
Streamlit: Criação de dashboard interativo.

📂 Estrutura do Projeto

````pl
projectwebscraping/
├── src/
│   ├── dashboard/
│   │   └── app.py  # Aplicação Streamlit
│   └── transformacao/
│       └── main.py  # Scripts de manipulação dos dados
├── data/
│   └── quotes.db  # Banco de dados SQLite com os dados extraídos
└── README.md       # Documentação do projeto
````

📈 Como Executar
1. Rodar o Web Scraping
Para coletar os dados diretamente do marketplace, execute o comando abaixo na pasta onde o Scrapy está configurado:

````bash
scrapy crawl mercadolivre -o ../../data/data.jsonl
````
Os dados serão salvos no arquivo data.jsonl, localizado na pasta data/.

2. Processar os Dados com Pandas
Após a coleta, você pode processar os dados com Pandas. Execute este comando dentro da pasta src:

````bash
python transformacao/main.py
````
3. Executar o Dashboard Interativo
Para visualizar os insights, rode o Streamlit para carregar o dashboard:

````bash
streamlit run src/dashboard/app.py
````

📝 Licença
Este projeto é de código aberto e está licenciado sob os termos da MIT License.