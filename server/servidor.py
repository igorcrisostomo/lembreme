from lxml import etree
from bs4 import BeautifulSoup
import requests
import io
import os
import csv
import json

currentPath = os.getcwd()

# Navega para o diretório raiz do projeto
while not os.path.exists(os.path.join(currentPath, 'README.md')):
    currentPath = os.path.dirname(currentPath)

serverPath = os.path.abspath(currentPath) + '/server'

# Abrir o arquivo JSON
with open(serverPath+"/urls.json", encoding='utf-8') as myJson:
    pages = json.load(myJson)


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

# Percorre o JSON de páginas para verificar uma a uma se houve alteração
for page in pages:
    # Faz a requisição HTTP e obtém o conteúdo HTML
    response = requests.get(page["url"], headers=headers)

    html = response.text

    # Cria um objeto BeautifulSoup a partir do conteúdo HTML
    soup = BeautifulSoup(html, "html.parser")
    pageContent = soup.select(page["selector"])[0]

    # Obtem o conteúdo antigo da página já salva
    pathFileName = serverPath+'/pages_saved/'+str(page["id"])+'.html'
    
    if os.path.exists(pathFileName):
        # Lê o conteúdo do arquivo salvo
        with open(pathFileName, 'r', encoding='utf-8') as file:
            fileContent = file.read()
        file.close()

        if(pageContent.text == fileContent):
            print(page["id"],": igual")
        else:
            print(page["id"],": diferente")

    # Cria um objeto IO para escrever a resposta em um arquivo .html
    with io.open(pathFileName, 'w', encoding='utf-8') as file:
        file.write(pageContent.text)
    file.close()