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

botao = drive.find_element(By.XPATH, '//*[@id="SubPageContainer"]/div[1]/nav/button[3]')
botao.click()

dict_uso_equipamentos = {
    'Id_equipamento': [],
    'Data': [],
    'Horas_uso': [],
    'Turno': []
}

elementos = drive.find_elements(By.TAG_NAME, 'tr')

for elemento in elementos:
    try:
        WebDriverWait(drive, 10).until(
            ec.presence_of_all_elements_located((By.TAG_NAME, 'tr'))
        )
        print('Elementos encontrados com sucesso!!!')

        id_equipamento = elemento.find_element(By.CLASS_NAME, 'td_id_equipamento').text.strip()
        data = elemento.find_element(By.CLASS_NAME, 'td_data').text.strip()
        horas_uso = elemento.find_element(By.CLASS_NAME, 'td_horas_uso').text.strip()
        turno = elemento.find_element(By.CLASS_NAME, 'td_turno').text.strip()

        dict_uso_equipamentos['Id_equipamento'].append(id_equipamento)
        dict_uso_equipamentos['Data'].append(data)
        dict_uso_equipamentos['Horas_uso'].append(horas_uso)
        dict_uso_equipamentos['Turno'].append(turno)

    except Exception as e:
        print('Elementos não encontrados!', e)
        continue

drive.quit()

df = pd.DataFrame(dict_uso_equipamentos)

df.to_excel('uso_equipamentos.xlsx', index=False)