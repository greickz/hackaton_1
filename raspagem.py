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

dict_materiais = {
    'Id_material': [],
    'Nome': [],
    'Quantidade_uso': [],
    'Unidade': [],
    'Setor_uso': [],
    'Custo_unitario': [],
    'Fornecedor': [],
    'Filial': [],
    'Turno': []
}

dict_uso_equipamentos = {
    'Id_equipamento': [],
    'Data': [],
    'Horas_uso': [],
    'Turno': []
}

elementos = drive.find_element(By.XPATH, '//table/tbody//tr')


for elemento in elementos:
    try:
        WebDriverWait(drive, 10).until(
            ec.presence_of_all_elements_located((By.XPATH, '//table/tbody//tr'))
        )
        print('Elementos encontrados com sucesso!!!')

        id_equipamento = elemento.find_element(By.CLASS_NAME, 'td_id_equipamento')
        modelo = elemento.find_element(By.CLASS_NAME, 'td_modelo')
        setor = elemento.find_element(By.CLASS_NAME, 'td_setor')
        status_atual = elemento.find_element(By.CLASS_NAME, 'td_status_atual')
        tipo_manutencao = elemento.find_element(By.CLASS_NAME, 'td_tipo_manutencao')
        data_manutencao = elemento.find_element(By.CLASS_NAME, 'td_data_manutencao')
        

    except :
        