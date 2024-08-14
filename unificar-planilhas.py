import os
import pandas as pd
import datetime

# Definir o diretório onde os arquivos .xlsx estão localizados
diretorio = "C:\Webscraping\Webscraping_Produtos_Python_e_Selenium"  # Substitua pelo caminho do seu diretório

# Gerar a data e a hora atual para usar no nome do arquivo
data_hora_atual = datetime.datetime.now().strftime("%d.%m.%Y_%H-%M")

# Definir o caminho onde o arquivo unificado será salvo, incluindo a data e a hora no nome do arquivo
caminho_para_salvar = f"C:\\Webscraping\\Webscraping_Produtos_Python_e_Selenium\\Arquivos\\{data_hora_atual}_produtos-edona.xlsx"

# Inicializar uma lista para armazenar os DataFrames
lista_dfs = []

# Iterar sobre todos os arquivos .xlsx no diretório
for arquivo in os.listdir(diretorio):
    if arquivo.endswith(".xlsx"):
        caminho_arquivo = os.path.join(diretorio, arquivo)
        # Ler o arquivo Excel, forçando a coluna 'codigo' a ser tratada como string
        df = pd.read_excel(caminho_arquivo, dtype={'Código_Produto': str})
        lista_dfs.append(df)

# Concatenar todos os DataFrames em um único DataFrame
df_unificado = pd.concat(lista_dfs, ignore_index=True)

# Salvar o DataFrame unificado em um novo arquivo Excel no caminho especificado
df_unificado.to_excel(caminho_para_salvar, index=False)

print(f"Todos os arquivos foram unificados com sucesso em '{caminho_para_salvar}'")
