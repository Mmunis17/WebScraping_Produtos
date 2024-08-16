import time
import math
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup


# Configuração inicial do WebDriver e URL base
url_base = 'https://www.oceanob2b.com/bebidas-e-alimentos'
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Executa o Chrome em modo headless (sem interface gráfica)
options.add_argument(f'user-agent={headers["User-Agent"]}')  # Define o User-Agent
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# Acessar a primeira página para obter o número total de itens
driver.get(url_base)
time.sleep(3)  # Aguarda o carregamento da página

# Faz o parsing da página inicial com BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Extrai a quantidade total de itens e calcula a última página
qtd_itens_text = soup.find('div', class_='resultados d-none d-md-block').get_text().strip()
qtd = int(re.search(r'\d+', qtd_itens_text).group())  # Extrai o número total de itens
itens_por_pagina = 96  # Número de itens por página
ultima_pagina = math.ceil(qtd / itens_por_pagina)

print(f"Número total de itens: {qtd}")
print(f"Número total de páginas: {ultima_pagina}")

# Função para extrair URLs de uma página
def extrair_urls_pagina(driver):
    produtos = driver.find_elements(By.CLASS_NAME, "product")  # Seletor do card do produto
    urls = []

    for produto in produtos:
        try:
            url_produto = produto.find_element(By.CLASS_NAME, "name").find_element(By.TAG_NAME, 'a').get_attribute('href')
            urls.append(url_produto)
            print(f"URL do Produto: {url_produto}")
        except Exception as e:
            print(f"Erro ao processar a URL de um produto: {e}")

    return urls

# Coletar URLs de todas as páginas com paginação
urls_todos_produtos = []

#for pagina_atual in range(1): ## -- para testar apenas 1 paginna -- ##
for pagina_atual in range(1, ultima_pagina + 1):
    print(f"Processando página {pagina_atual} de {ultima_pagina}...")
    driver.get(f"{url_base}?page={pagina_atual}")
    time.sleep(3)  # Aguarda o carregamento da página

    urls_pagina = extrair_urls_pagina(driver)
    urls_todos_produtos.extend(urls_pagina)

# Agora, acessar cada produto individualmente para extrair o código, descrição e valor do produto
dados_completos = []

for url_produto in urls_todos_produtos:
    driver.get(url_produto)
    time.sleep(3)  # Aguarda o carregamento da página do produto
    
    try:
        # Extrair o código do produto
        codigo_produto = driver.find_element(By.CLASS_NAME, "sku-produto").find_element(By.TAG_NAME, "span").text
        
        # Extrair a descrição do produto
        descricao = driver.find_element(By.CLASS_NAME, "detalhe-produto-nome").text
        
        # Extrair o valor do produto
        try:
            valor = driver.find_element(By.CLASS_NAME, "sales-price").text
        except:
            valor = "Indisponível"
      
        # Extraindo a categoria do breadcrumb
        breadcrumb = driver.find_element(By.CLASS_NAME, "detalhe-produto-breadcrumb")
        categorias = breadcrumb.find_elements(By.TAG_NAME, 'a')
        categoria_principal = categorias[0].text  # Pega o texto do primeiro <a>
        categoria_secundaria = categorias[-1].text  # Pega o texto do último <a>
        
        # Adicionar os dados coletados à lista
        dados_completos.append(["oceanob2b", codigo_produto, categoria_principal, categoria_secundaria, descricao, valor, url_produto])
        print(f"Descrição: {descricao}, Valor: {valor}, Código_Produto: {codigo_produto}, Categoria Principal: {categoria_principal}, Categoria Secundária: {categoria_secundaria}, URL_Produto: {url_produto}")
        
    except Exception as e:
        print(f"Erro ao processar os detalhes do produto: {e}")

# Fechar o navegador
driver.quit()

# Salvar os dados em um arquivo Excel com cabeçalhos
df = pd.DataFrame(dados_completos, columns=["Canal_Venda", "Código_Produto", "Categoria Principal", "Categoria Secundária", "Descrição", "Valor", "Url_Produto"])

# Adicionar data e hora ao nome do arquivo
data_hora_atual = pd.Timestamp.now().strftime("%d.%m.%Y_%H-%M")
nome_arquivo = f'C:\\Webscraping\\arquivos\\arquivos-oceanob2b\\oc_bebidas-e-alimentos_{data_hora_atual}.xlsx'

# Salvar no caminho especificado
df.to_excel(nome_arquivo, index=False)

print(f"Dados extraídos e salvos com sucesso em '{nome_arquivo}'")

### -- Script Criado em 15/08/2024 -- ### -->MaYaRa<--
### -- Script Atualizando em 16/08/2024 -- ### -->MaYaRa<--
