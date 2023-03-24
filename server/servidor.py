import requests


# URL da página que você deseja obter a resposta HTML
url = 'https://www.in.gov.br/consulta/-/buscar/dou?q=%22+CLEBER+DE+MATTOS+CASALI%22&s=todos&exactDate=ano&sortType=0'
r = requests.get(url)
print(r.content)
print(url)


###

import requests
import io

response = requests.get(url).text

# Cria um objeto IO para escrever a resposta em um arquivo .txt
with io.open('resposta.html', 'w', encoding='utf-8') as file:
    file.write(response)