import time
import os
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome(executable_path='C:\\drivers\\chromedriver_107')
# driver.maximize_window()

url_base = "https://www.informazione-aziende.it/10-71_PRODUZIONE-DI-PANE-PRODOTTI-DI-PASTICCERIA-FRESCHI/Regione_VENETO?qPg="
driver.get(url_base)
time.sleep(7)

try: driver.find_element(By.XPATH, '//button[@id="didomi-notice-agree-button"]').click()
except: pass 
time.sleep(3)

filename = 'export.txt'

try: os.remove(filename)
except: pass

for i in range(175):
    time.sleep(3)

    url = f'{url_base}{i+1}'
    driver.get(url)

    elements = driver.find_elements(By.XPATH, '//span[@itemprop="itemListElement"]')
    with open(filename, 'a') as f:
        for e in elements:
            url = e.find_element(By.XPATH, './/a').get_attribute('href')
            print(url)
            f.write(f'{url}\n')




with open('export.txt') as f:
    content = f.read().split('\n')
    print(content)

try: os.remove('export.csv')
except: pass

# for i in range(0, 100):
for i in range(201, 400):
    url = content[i]
    print(f'{i}/{len(content)} - {url}')
    driver.get(url)
    time.sleep(3)

    business_name = ''
    website = ''

    try: business_name = driver.find_element(By.XPATH, '//h1').text
    except: pass
    try: website = driver.find_element(By.XPATH, '//td[@data-title="Sito Web"]/a').get_attribute('href')
    except: pass

    with open('export.csv', 'a', newline='', encoding="utf-8", errors='ignore') as f:
        writer = csv.writer(f, delimiter='\\')
        writer.writerow([url, business_name, website])