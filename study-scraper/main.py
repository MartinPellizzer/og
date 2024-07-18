from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep

driver = webdriver.Firefox()
driver.maximize_window()

driver.get('https://scholar.google.com/')
sleep(5)
driver.get('https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=ozone&btnG=')
sleep(5)
# driver.find_element(By.XPATH, '//input[@name="q"]').send_keys('ozone')
# sleep(2)
latest_studies_url = driver.find_element(By.XPATH, '//a[contains(text(), "Ordina per data")]').get_attribute('href')
driver.get(latest_studies_url)
sleep(5)

with open('data.json') as f: data = json.load(f)
if 'studies' not in data: data['studies'] = []
with open('data.json', 'w') as f: json.dump(data, f)

for _ in range(99):
    elements = driver.find_elements(By.XPATH, '//h3/..')
    for e in elements:
        try: study_url = e.find_element(By.XPATH, './/h3/a').get_attribute('href')
        except: continue
        try: study_days = e.find_element(By.XPATH, './/div[2]').text
        except: continue
        
        if study_days.split(' ')[0].isdigit(): study_days = int(study_days.split(' ')[0])
        else: continue

        if study_days > 60: break

        found = False
        for obj in data['studies']:
            if obj['study_url'] == study_url:
                found = True

        if not found: 
            data['studies'].append({
                'study_url': study_url,
                'study_days': study_days,
            })
            with open('data.json', 'w') as f: json.dump(data, f)

        print(study_days, study_url)
        print()
        
    if study_days > 60: break

    sleep(5)

    next_page_url = driver.find_element(By.XPATH, '//*[contains(text(), "Avanti")]/..').get_attribute('href')
    driver.get(next_page_url)

