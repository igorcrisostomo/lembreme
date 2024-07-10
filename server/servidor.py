from lxml import etree
from bs4 import BeautifulSoup
import requests
import io
import os
import json
# import webbrowser # importar apenas se quiser abrir o navegador com o URL
import difflib
import time

# Bliblioteca para envio de e-mail
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def main():

    # Carregar de urls.json os dados das páginas
    with open("./urls.json", encoding='utf-8') as myJson:
        pages = json.load(myJson)
    
    # Cria uma instância da classe Differ para comparar os arquivos
    differ = difflib.Differ()

    # Define cabeçalho das requisições a serem feitas para as páginas
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    # Percorre o JSON de páginas para verificar uma a uma se houve alteração
    for page in pages:
        try:
            # Faz a requisição HTTP e obtém o conteúdo HTML
            response = requests.get(page["url"], headers=headers)

            html = response.text

            # Cria um objeto BeautifulSoup a partir do conteúdo HTML
            soup = BeautifulSoup(html, "html.parser")
            pageContent = soup.select(page["selector"])[0]
            pageTitle = soup.select("title")[0]

            # Obtem o conteúdo antigo da página já salva
            pathFileName = './pages_saved/'+str(page["id"])+'.html'
            
            if os.path.exists(pathFileName):
                # Lê o conteúdo do arquivo salvo
                with open(pathFileName, 'r', encoding='utf-8') as file:
                    fileContent = file.read()
                file.close()

                if(pageContent.text != fileContent):
                    # print(page["id"],": Igual")
                # else:
                    print(page["id"],": Atualizada. Título: ", pageTitle.text)
                    # Compara as duas strings e retorna uma lista das diferenças
                    differences = list(differ.compare(pageContent.text, fileContent))
                    print("Detalhes da atualização:")
                    # Percorre a lista de diferenças e exibe as que começam com "+" (adicionadas) ou "-" (removidas)
                    textAdded = ""
                    for line in differences:
                        # pegar apenas o texto adicionado
                        if line.startswith("+"):
                            textAdded += line.strip()[2:]
                        
                    print("Texto adicionado: ", textAdded)
                    # Abre o navegador com a url que sofreu alterações
                    # webbrowser.open(page["url"])

                    body = f"""
                    <p>ID: {page["id"]}</p>\
                    <p>Título: {pageTitle.text}</p>\
                    <p>URL: {page["url"]}</p>\
                    <p>Texto adicionado/removido: {textAdded}</p>
                    """

                    sendMail(body)

                    # sobrescreve o arquivo com a atualização
                    writeFile(pathFileName, pageContent.text)
            
            # se o arquivo não existir, então grava
            else:
                print("Novo arquivo cadastrado: ", pathFileName)
                writeFile(pathFileName, pageContent.text)

        except TimeoutError:
            gravaLog("Ocorreu um erro de timeout ao tentar requisitar a página ", page['id'])

def writeFile(name, content):
    # Cria um objeto IO para escrever a resposta em um arquivo .html
    with io.open(name, 'w', encoding='utf-8') as file:
        file.write(content)
    file.close()

def sendMail(mensagem):
    try:
        # Criando mensagem de e-mail
        msg = MIMEMultipart()
        msg['From'] = 'igor.o.crisostomo@gmail.com'
        msg['To'] = 'igor.o.crisostomo@gmail.com'
        msg['Subject'] = 'Página atualizada'

        # Configuração do servidor SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(msg['From'], 'ltnrnhqeiqruynsg')

        # Adicionando conteúdo ao e-mail
        #mensagem = 'Olá, isso é um exemplo de e-mail enviado com Python.'
        msg.attach(MIMEText(mensagem, 'html'))

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