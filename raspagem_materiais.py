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

botao = drive.find_elements(By.XPATH, "//div[@class='App']//button[text()='Materiais']")

try:
    WebDriverWait(drive, 10).until(
        ec.presence_of_all_elements_located((By.TAG_NAME, 'tr'))
        )
    print('Elementos encontrados com sucesso!!')
    
except TimeoutException:
    print('Tempo de espera excedido')

botao[0].click()

elementos = drive.find_elements(By.TAG_NAME, 'tr')

for elemento in elementos:
    try:
        id_material = elemento.find_element(By.CLASS_NAME, 'td_id_material').text.strip()
        nome = elemento.find_element(By.CLASS_NAME, 'td_nome').text.strip()
        quantidade_uso = elemento.find_element(By.CLASS_NAME, 'td_quantidade_uso').text.strip()
        unidade = elemento.find_element(By.CLASS_NAME, 'td_unidade').text.strip()
        setor_uso = elemento.find_element(By.CLASS_NAME, 'td_setor_uso').text.strip()
        custo_unitario = elemento.find_element(By.CLASS_NAME, 'td_custo_unitario').text.strip()
        fornecedor = elemento.find_element(By.CLASS_NAME, 'td_fornecedor').text.strip()
        filial = elemento.find_element(By.CLASS_NAME, 'td_Filial').text.strip()
        turno = elemento.find_element(By.CLASS_NAME, 'td_turno').text.strip()
        
        dict_materiais['Id_material'].append(id_material)
        dict_materiais['Nome'].append(nome)
        dict_materiais['Quantidade_uso'].append(quantidade_uso)
        dict_materiais['Unidade'].append(unidade)
        dict_materiais['Setor_uso'].append(setor_uso)
        dict_materiais['Custo_unitario'].append(custo_unitario)
        dict_materiais['Fornecedor'].append(fornecedor)
        dict_materiais['Filial'].append(filial)
        dict_materiais['Turno'].append(turno)

    except Exception as e:
        print('Elementos não encontrados!', e)
        continue
        
drive.quit()

df = pd.DataFrame(dict_materiais)

df.to_excel('materiais.xlsx', index=False)