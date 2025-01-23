from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os
import time
from selenium.common.exceptions import NoSuchElementException

def save_text(soup, filename):
    content_div = soup.find('div', class_='capa-contenido')
    if not content_div:
        return

    text = ''
    for element in content_div.descendants:
        if element.name == 'h1':
            text += element.get_text(strip=True) + '\n' + '.' * 80 + '\n'
        elif element.name == 'h2':
            text += element.get_text(strip=True) + '\n' + '-' * 80 + '\n'
        elif element.string:
            text += element.get_text(strip=True) + '\n'

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)

def main():
    url = 'https://www.proteccioncivil.es/coordinacion/gestion-de-riesgos/tecnologicos/transporte-mercancias-peligrosas/fichas-de-primera-intervencion?p_p_id=com_grupoica_publicador_PublicadorPortlet_INSTANCE_DQLffHNH5vHb&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&_com_grupoica_publicador_PublicadorPortlet_INSTANCE_DQLffHNH5vHb_javax.portlet.action=buscarResultados&p_auth=QH1iD5fE&_com_grupoica_publicador_PublicadorPortlet_INSTANCE_DQLffHNH5vHb_pagina=15'
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    service = Service('drivers/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.get(url)
    time.sleep(3)  # Espera para cargar la página
    
    # Intentar cerrar el banner de cookies si existe
    try:
        cookie_banner = driver.find_element(By.CLASS_NAME, 'COMUN-Cookie-containe-txt')
        close_button = cookie_banner.find_element(By.TAG_NAME, 'button')
        close_button.click()
        time.sleep(1)  # Espera para que el banner se cierre
    except:
        pass  # Si no se encuentra el banner, continuar
    
    # Crear carpeta "Fichas" si no existe
    if not os.path.exists('Fichas'):
        os.makedirs('Fichas')
    
    while True:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        links = soup.find_all('a', string="Ver ficha")    
    
        links_elements = driver.find_elements(By.LINK_TEXT, "Ver ficha")

        for i, link in enumerate(links):
            # Intentar cerrar el banner de cookies si existe
            try:
                cookie_banner = driver.find_element(By.CLASS_NAME, 'COMUN-Cookie-containe-txt')
                close_button = cookie_banner.find_element(By.TAG_NAME, 'button')
                close_button.click()
                time.sleep(1)  # Espera para que el banner se cierre
            except:
                pass  # Si no se encuentra el banner, continuar
            # Encuentra el enlace de nuevo y desplázate hasta él

            driver.get(url)
            time.sleep(3)  # Espera para cargar la página
            links_elements = driver.find_elements(By.LINK_TEXT, "Ver ficha")
            driver.execute_script("arguments[0].scrollIntoView();", links_elements[i])
            time.sleep(3)  # Espera para que el desplazamiento se complete
            
            # Haz clic en el enlace usando JavaScript
            driver.execute_script("arguments[0].click();", links_elements[i])
            time.sleep(3)
            # Espera a que la nueva página cargue
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            time.sleep(3)
            # Extrae el contenido de la página
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            time.sleep(3)  # Espera para que el contenido se cargue
            # Extrae el valor del elemento que contiene PC_fichaintervencion_ONU
            onu_element = soup.find('span', {'class': 'PC_fichaintervencion_ONU'})
            if onu_element:
                onu_number = onu_element.text.strip()
            else:
                onu_number = f'desconocido_{i+1}'
            
            # Guarda el contenido en un archivo de texto
            filename = f'Fichas/ficha_{onu_number}.txt'
            save_text(soup, filename)
            
            # Vuelve a la página anterior
            driver.back()
            time.sleep(3)  # Espera para cargar la página anterior
        
        # Se pasa a la siguiente página
        try:
            next_page_link = driver.find_element(By.CLASS_NAME, 'page-link pag-siguiente')
            driver.execute_script("arguments[0].scrollIntoView();", next_page_link)
            time.sleep(1)  # Espera para que el desplazamiento se complete
            # Haz clic en el enlace de la siguiente página usando JavaScript
            driver.execute_script("arguments[0].click();", next_page_link)
            time.sleep(3)  # Espera para que la nueva página cargue
            url = driver.current_url
        except NoSuchElementException:
        # Si no se encuentra el enlace a la siguiente página, salir del bucle
            break
        driver.quit()
        

if __name__ == '__main__':
    main()