from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import pandas as pd
import time
from selenium.common.exceptions import TimeoutException


chrome_driver_path = "C:\Program Files\chromedriver-win64\chromedriver.exe"
service= Service(chrome_driver_path) 
options = webdriver.ChromeOptions() 
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')
driver= webdriver.Chrome(service=service, options=options)
url_base= 'https://www.kabum.com.br/audio/fone-de-ouvido/bluetooth'
driver.get(url_base)
time.sleep(5)


fones_sem_fio =  {'Descrição do Produto': [], 'Preço': [] }
pagina = 1

while True:
    print(f'\n Coletando dados da página {pagina} ...')

    try:
        WebDriverWait(driver, 10).until(
            ec.presence_of_all_elements_located((By.CLASS_NAME, 'productCard'))
        )
        print("Elementos encontrados com sucesso")
    except TimeoutException:
        print("Tempo de espera excedido!")

    produtos = driver.find_elements(By.CLASS_NAME, 'productCard')

    for produto in produtos:
        try:
            marca= produto.find_element(By.CLASS_NAME, 'nameCard').text.strip()
            preco= produto.find_element(By.CLASS_NAME, 'priceCard').text.strip()
            print(f'{marca} - {preco}')
            fones_sem_fio['Descrição do Produto'].append(marca)
            fones_sem_fio['Preço'].append(preco)
        except Exception:
            print("Erro ao coletar dados:", Exception)

    try:
        botao_proximo = WebDriverWait(driver, 5).until(
            ec.element_to_be_clickable((By.CLASS_NAME, 'nextLink'))
        )
        if botao_proximo:
            driver.execute_script('arguments[0].scrollIntoView();', botao_proximo)
            time.sleep(1)

            driver.execute_script('arguments[0].click();', botao_proximo)
            print(f'Indo para a página {pagina}')
            pagina += 1
            time.sleep(5)

        else:
            print("Você chegou na ultima página!")
            break

    except Exception as e:
        print("Erro ao tentar avançar para a próxima página.", e)
        break

driver.quit()
df = pd.DataFrame(fones_sem_fio)
df.to_excel("Fones sem Fio.xlsx", index=False)
print(f"Arquivo 'Fones sem Fio' salvo com sucesso! ({len(df)} produtos capturados.)")
