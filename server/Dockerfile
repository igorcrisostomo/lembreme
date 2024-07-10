# Use a imagem base do Python
FROM python:3.8-slim-buster

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo servidor.py para o contêiner
COPY . .

# Instala as dependências (lxml, BeautifulSoup, requests, etc.)
RUN pip install lxml beautifulsoup4 requests

# Define o comando para executar o servidor.py
CMD ["python3", "servidor.py"]