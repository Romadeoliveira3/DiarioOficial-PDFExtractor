import os
import re
import time
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import fitz  # PyMuPDF

def access_site(driver):
    driver.get("http://diariooficial.imprensaoficial.com.br/nav_v6/index.asp?c=34031&e=20231030&p=1")
    time.sleep(5)
    driver.switch_to.default_content()
    driver.switch_to.frame(0)
    select_element = driver.find_element(By.ID, 'pg')
    options = select_element.find_elements(By.TAG_NAME, 'option')
    for option in options:
        if option.text.strip() == '____Educação .... 137':
            option.click()
            break
    time.sleep(5)

def get_pdf_url(driver):
    pdf_url = None
    scripts = driver.find_elements(By.TAG_NAME, 'script')
    for script in scripts:
        if '.pdf' in script.get_attribute('innerHTML'):
            match = re.search(r"src\s*=\s*'(.+\.pdf)'", script.get_attribute('innerHTML'))
            if match:
                pdf_url = match.group(1)
                break
    return pdf_url

def download_pdf(pdf_url):
    if pdf_url:
        response = requests.get(pdf_url)
        file_name = pdf_url.split('/')[-1]
        if not os.path.exists(file_name):
            with open(file_name, 'wb') as file:
                file.write(response.content)
            print(f"PDF baixado com sucesso: {file_name}")
        else:
            print(f"Arquivo já existe: {file_name}")
        return file_name
    else:
        print("Nenhum arquivo PDF encontrado.")
        return None

def extract_pdf_text(file_name, pattern):
    doc = fitz.open(file_name)
    matches = []
    for page in doc:
        text = page.get_text()
        matches.extend(re.findall(pattern, text))
    return matches

# Configuração do Selenium com o WebDriver
driver = webdriver.Chrome()

# Acessar site e selecionar opção
access_site(driver)

# Obter URL do PDF
pdf_url = get_pdf_url(driver)

# Fecha o navegador
driver.quit()

# Baixar PDF
file_name = download_pdf(pdf_url)

# Extrair texto do PDF
if file_name:
    pattern = r"TOMADA DE PREÇOS Nº:\s*\d+/\d+/\d+/\d+"
    matches = extract_pdf_text(file_name, pattern)
    for match in matches:
        print(match)
