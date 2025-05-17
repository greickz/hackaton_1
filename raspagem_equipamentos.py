from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
import time

caminho = r"C:\Program Files\chromedriver-win64\chromedriver-win64\chromedriver.exe"
servico = Service(caminho)
opcoes = webdriver.ChromeOptions()
opcoes.add_argument('--disable-gpu')
opcoes.add_argument('--window-size=1920,1080')
drive = webdriver.Chrome(service= servico, options= opcoes)
url = 'https://masander.github.io/AlimenticiaLTDA/#/operational'
drive.get(url)
time.sleep(5)


dict_equipamentos = {
    'Id_equipamento': [],
    'Modelo': [],
    'Setor': [],
    'Status_atual': [],
    'Tipo_manutencao': [],
    'Data_manutencao': [],
    'Tempo_parado_dias': [],
    'Custo_manutencao': []
}


elementos = drive.find_elements(By.TAG_NAME, 'tr')

for elemento in elementos:
    try:
        WebDriverWait(drive, 10).until(
            ec.presence_of_all_elements_located((By.TAG_NAME, 'tr'))
        )
        print('Elementos encontrados com sucesso!!!')

        id_equipamento = elemento.find_element(By.CLASS_NAME, 'td_id_equipamento').text.strip()
        modelo = elemento.find_element(By.CLASS_NAME, 'td_modelo').text.strip()
        setor = elemento.find_element(By.CLASS_NAME, 'td_setor').text.strip()
        status_atual = elemento.find_element(By.CLASS_NAME, 'td_status_atual').text.strip()
        tipo_manutencao = elemento.find_element(By.CLASS_NAME, 'td_tipo_manutencao').text.strip()
        data_manutencao = elemento.find_element(By.CLASS_NAME, 'td_data_manutencao').text.strip()
        tempo_parado_dias = elemento.find_element(By.CLASS_NAME, 'td_tempo_parado_dias').text.strip()
        custo_manutencao = elemento.find_element(By.CLASS_NAME, 'td_custo_manutencao').text.strip()

        dict_equipamentos['Id_equipamento'].append(id_equipamento)
        dict_equipamentos['Modelo'].append(modelo)
        dict_equipamentos['Setor'].append(setor)
        dict_equipamentos['Status_atual'].append(status_atual)
        dict_equipamentos['Tipo_manutencao'].append(tipo_manutencao)
        dict_equipamentos['Data_manutencao'].append(data_manutencao)
        dict_equipamentos['Tempo_parado_dias'].append(tempo_parado_dias)
        dict_equipamentos['Custo_manutencao'].append(custo_manutencao)

    except:
        print('Elementos não encontrados!')
        continue

drive.quit()

df = pd.DataFrame(dict_equipamentos)

df.to_excel('equipamentos.xlsx', index=False)