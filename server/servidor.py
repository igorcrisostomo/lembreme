# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By

from lxml import etree
from bs4 import BeautifulSoup
import requests
import io
import os
import json

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def main():
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

    sendMail()

def sendMail():
    try:
        # Criando mensagem de e-mail
        msg = MIMEMultipart()
        msg['From'] = 'igor.o.crisostomo@gmail.com'
        msg['To'] = 'igor.oliveira@ufvjm.edu.br'
        msg['Subject'] = 'Assunto do E-mail'

        # Configuração do servidor SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(msg['From'], 'gmksbiwlicyvhdgi')

        # Adicionando conteúdo ao e-mail
        mensagem = 'Olá, isso é um exemplo de e-mail enviado com Python.'
        msg.attach(MIMEText(mensagem, 'plain'))

        # Enviando e-mail
        texto = msg.as_string()
        server.sendmail(msg['From'], msg['To'], texto)
        server.quit()
    except TimeoutError:
        gravaLog("Ocorreu um erro de timeout ao tentar conectar com o servidor SMTP para enviar o e-mail de notificação.\nEste pode ser:\na) Um problema de comunicação com servidor; ou\nb)Regra de firewall da rede que este APP está conectado.")

def gravaLog(msg):
    print(msg)

if __name__ == '__main__':
    # servico = Service(ChromeDriverManager().install())
    # navegador = webdriver.Chrome(service=servico)

    # navegador.get("https://web.whatsapp.com/")
    # input_box = navegador.find_element(By.XPATH, '//div[@class="_2_1wd copyable-text selectable-text"][@dir="ltr"][@data-tab="3"]')
    # input_box.send_keys("Lembrete" + Keys.ENTER)

    #exit('FIM')
    main()