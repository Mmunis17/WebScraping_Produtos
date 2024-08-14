import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime

# Configuração do WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Acessar a página desejada
driver.get("https://www.edona.com.br/alimentos-e-bebidas")

# Função para rolar a página até o final
def rolar_pagina(driver):
    altura_inicial = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  # Aguarda o carregamento de novos itens
        altura_final = driver.execute_script("return document.body.scrollHeight")
        
        if altura_final == altura_inicial:
            print("Nenhum novo conteúdo foi carregado.")
            break
        else:
            print("Novos conteúdos foram carregados.")
            altura_inicial = altura_final

# Rolar a página para carregar todos os produtos
rolar_pagina(driver)

# Extrair URLs dos produtos
produtos = driver.find_elements(By.CLASS_NAME, "product__inner")

urls = []
dados = []

# Coletar todas as URLs dos produtos
for produto in produtos:
    try:
        descricao_element = produto.find_element(By.CLASS_NAME, "product__name")
        url = descricao_element.find_element(By.TAG_NAME, 'a').get_attribute('href')
        urls.append(url)
        print(f"URL coletada: {url}")
    except Exception as e:
        print(f"Erro ao processar um produto: {e}")

# Navegar por cada URL para extrair informações detalhadas
for url in urls:
    driver.get(url)
    time.sleep(3)  # Aguarda o carregamento da página do produto
    
    try:
        # Coletar informações da página do produto
        descricao = driver.find_element(By.CLASS_NAME, "product__name").text
        try:
            valor = driver.find_element(By.ID, "normal-price-text").text
            if not valor.strip():  # Verifica se o valor está vazio ou apenas com espaços
                valor = "Indisponível"
        except:
            valor = "Indisponível"  # Define caso o elemento não seja encontrado

        codigo = driver.find_element(By.CLASS_NAME, "skuReference").text

        # Extraindo a categoria do breadcrumb
        breadcrumb = driver.find_element(By.CLASS_NAME, "bread-crumb")
        categoria = breadcrumb.find_elements(By.TAG_NAME, 'a')[-1].text  # Pega o texto do último <a>

        # Adicionar os dados coletados à lista
        dados.append([codigo, categoria, descricao, valor, url])
        print(f"Descrição: {descricao}, Valor: {valor}, Código_Produto: {codigo}, Categoria: {categoria}, URL_Produto: {url}")

    except Exception as e:
        print(f"Erro ao acessar a página do produto: {e}")

# Fechar o navegador
driver.quit()

# Criar DataFrame e salvar os dados em um arquivo xlsx com cabeçalho
df = pd.DataFrame(dados, columns=["Código_Produto", "Categoria", "Descrição", "Valor", "URL_Produto"])

# Obter a data e a hora atual e Gerar o nome do arquivo com data e hora e salvar arquivo Excel
data_hora_atual = datetime.datetime.now().strftime("%d.%m.%Y_%H-%M")
nome_arquivo = f'C:\\Webscraping\\Arquivos\\alimentos-e-bebidas_{data_hora_atual}.xlsx'
df.to_excel(nome_arquivo, index=False)

print(f"Dados salvos com sucesso em '{nome_arquivo}'")
