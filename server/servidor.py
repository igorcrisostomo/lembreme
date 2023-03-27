from lxml import etree
from bs4 import BeautifulSoup
import requests
import io
import os

pages = [
    {
    "id": 1,
    "url": 'https://www.in.gov.br/consulta/-/buscar/dou?q=%22IGOR+OLIVEIRA+CRIS%C3%93STOMO%22&s=todos&exactDate=ano&sortType=0',
    "selector": '.search-total-label.text-default'
    },
    {
    "id": 2,
    "url": 'https://www.in.gov.br/consulta/-/buscar/dou?q=%22VITOR+VALSICHI+CUZIOL%22&s=todos&exactDate=all&sortType=0',
    "selector": '.search-total-label.text-default'
    },
]

# Percorre o JSON de páginas para verificar uma a uma se houve alteração

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

for page in pages:
    # Faz a requisição HTTP e obtém o conteúdo HTML
    response = requests.get(page["url"], headers=headers)

    html = response.text

    # Cria um objeto BeautifulSoup a partir do conteúdo HTML
    soup = BeautifulSoup(html, "html.parser")
    pageContent = soup.select(page["selector"])[0]

    # Obtem o conteúdo antigo da página já salva
    pathFileName = 'pages_saved/'+str(page["id"])+'.html'
    
    if os.path.exists(pathFileName):
        # Lê o conteúdo do arquivo salvo
        with open(pathFileName, 'r') as file:
            fileContent = file.read()
        file.close()

        if(pageContent.text == fileContent):
            print("igual")
        else:
            print("diferente")

    # Cria um objeto IO para escrever a resposta em um arquivo .html
    with io.open(pathFileName, 'w', encoding='utf-8') as file:
        file.write(pageContent.text)
    file.close()