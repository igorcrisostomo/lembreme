from lxml import etree
from bs4 import BeautifulSoup
import requests
import io

pages = [
    # {
    # "id": 1,
    # "url": 'https://www.in.gov.br/consulta/-/buscar/dou?q=%22+CLEBER+DE+MATTOS+CASALI%22&s=todos&exactDate=ano&sortType=0'
    # },
    {
    "id": 2,
    "url": 'https://www.in.gov.br/consulta/-/buscar/dou?q=%22IGOR+OLIVEIRA+CRISOSTOMO%22&s=todos&exactDate=ano&sortType=0'
    },
    # {
    # "id": 3,
    # "url": 'https://www.ifnmg.edu.br/mais-noticias-teofilo-otoni/653-teofilo-otoni-noticias-2023/31312-publicado-edital-do-pibed-para-selecao-de-projetos-de-extensao-com-bolsas-para-estudantes-do-ifnmg-12'
    # }
]

# Percorre o JSON de páginas para verificar uma a uma se houve alteração

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

for page in pages:
    # Faz a requisição HTTP e obtém o conteúdo HTML
    response = requests.get(page["url"], headers=headers)

    html = response.text

    # Cria um objeto BeautifulSoup a partir do conteúdo HTML
    soup = BeautifulSoup(html, "html.parser")
    pageContent = soup.select('.search-total-label.text-default strong')[0]

    # Obtem o conteúdo antigo da página já salva
    pathFileName = 'pages_saved/'+str(page["id"])+'.html'
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
