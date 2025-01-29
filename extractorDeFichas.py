from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup,Tag
import os
import time
import html2text
from selenium.common.exceptions import NoSuchElementException

        
def save_text(soup, filename, values):
    content_div = soup.find('div', class_='capa-contenido')
    if not content_div:
        return

    # Convertir el contenido HTML a texto con html2text
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    h.body_width = 0  # No limitar el ancho del texto
    text = h.handle(str(content_div))

    # Añadir los valores adicionales al principio del texto
    text = 'Número ONU: ' + values[0] + '\n' +'Nip: ' + values[1] + '\n'+'Etiqueta: ' + values[2] + '\n'  + 'Materia: ' + values[3] + '\n' + 'Número Ficha: ' + values[4] + '\n\n' + text

    # Validar si el archivo ya existe y agregar un sufijo numérico si es necesario
    base_filename, file_extension = os.path.splitext(filename)
    counter = 2
    new_filename = filename
    while os.path.exists(new_filename):
        new_filename = f"{base_filename}_variante{counter}{file_extension}"
        counter += 1

    with open(new_filename, 'w', encoding='utf-8') as file:
        file.write(text)

def main():
    # Variables de configuración
    empezar = False
    pagina_inicial =1
    pagina_final = 4
    sentido= "avanzando"
    pagina = pagina_inicial
    url = 'https://www.proteccioncivil.es/es/coordinacion/gestion-de-riesgos/tecnologicos/transporte-mercancias-peligrosas/fichas-de-primera-intervencion?p_p_id=com_grupoica_publicador_PublicadorPortlet_INSTANCE_DQLffHNH5vHb&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&_com_grupoica_publicador_PublicadorPortlet_INSTANCE_DQLffHNH5vHb_javax.portlet.action=buscarResultados&p_auth=50XDmnMp&_com_grupoica_publicador_PublicadorPortlet_INSTANCE_DQLffHNH5vHb_pagina=4'
    # Configurar el navegador Chrome
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    service = Service('drivers/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    # Cargar la página
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
    if sentido != "avanzando":
        # Desplázate hasta el enlace de la última página
        last_page_link = driver.find_element(By.CSS_SELECTOR, 'a.page-link.pag-fin')
        driver.execute_script("arguments[0].scrollIntoView();", last_page_link)
        time.sleep(1)  # Espera para que el desplazamiento se complete
        # Haz clic en el enlace de la siguiente página usando JavaScript
        driver.execute_script("arguments[0].click();", last_page_link)
        time.sleep(3)  # Espera para que la nueva página cargue
        url = driver.current_url
    # Crear carpeta "Fichas" si no existe
    
    if not os.path.exists('Fichas'):
        os.makedirs('Fichas')
    # Bucle principal para extraer las fichas retrocediendo página por página
    while True:
        # Verificar el span con clase page-num
        try:
            page_num_span = driver.find_element(By.CSS_SELECTOR, 'span.page-num')
            page_num_text = page_num_span.text.strip()

        except NoSuchElementException:
          pass
        # Se marca cuando comienza la extracción de las fichas
        if page_num_text.startswith(str(pagina_inicial)+' de'):
            empezar= True
        # Si estoy en la pagina adecuada empiezo a extraer las fichas   
        if empezar == True:
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
                
                # Se obtienen los valores del registro
                
                tr = link.find_parent('tr')
                tds = tr.find_all('td')
                if len(tds) >= 5:
                    values = [tds[0].get_text(strip=True), tds[1].get_text(strip=True),tds[2].get_text(strip=True), tds[3].get_text(strip=True),tds[4].get_text(strip=True)]
                    print(f'Pagina{pagina} Ficha {i+1}: {values}')
                
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
                filename = f'Fichas/{onu_number}_{str(values[1])}_{values[2].replace('.','-')}_{values[4].replace('.','-')}.txt'
                save_text(soup, filename,values)
                
                # Vuelve a la página anterior
                driver.back()
                time.sleep(3)  # Espera para cargar la página anterior
        # Se pasa a la página anterior/posterior
        try:
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
            if sentido == "avanzando": 
                if pagina < pagina_final:
                    next_page_link = driver.find_element(By.CSS_SELECTOR, 'a.page-link.pag-siguiente')
                    driver.execute_script("arguments[0].scrollIntoView();", next_page_link)
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", next_page_link)
                    time.sleep(3)
                    url = driver.current_url
                    pagina +=1
                    print(f'Pagina {pagina}')
                else:
                    print("Se ha alcanzado el final. Finalizando.")
                    break
            elif sentido != "avanzando":
                if pagina > pagina_final:
                    previous_page_link = driver.find_element(By.CSS_SELECTOR, 'li.page-item.pag-anterior > a.page-link')
                    driver.execute_script("arguments[0].scrollIntoView();", previous_page_link)
                    time.sleep(1)  # Espera para que el desplazamiento se complete
                    # Haz clic en el enlace de la siguiente página usando JavaScript
                    driver.execute_script("arguments[0].click();", previous_page_link)
                    time.sleep(3)  # Espera para que la nueva página cargue
                    url = driver.current_url
                    pagina -=1
                else:
                    print("Se ha alcanzado el final. Finalizando.")
                    break
            print(f'Pagina {pagina}')
        except NoSuchElementException:
            driver.quit()
            break
              
        

if __name__ == '__main__':
    main()