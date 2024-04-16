from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from time import sleep
import re
import os
import requests
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup
import pandas

import sys
import csv

driver = None

sep = '\\'

def sanitize(text):
	chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890,.-()\'&@ '
	encoded_string = text.encode('ascii', 'ignore')
	decoded_string = encoded_string.decode()
	text = ''
	for c in decoded_string:
		if c in chars:
			text += c
	return text
    
    
def click_on_listing(business):
	for _ in range(3):
		try: 
			business.click()
			return True
		except: 
			print('error click')
			continue
	return False

def get_card_element(e):
	try: return e.find_elements(By.XPATH, '//div[@role="main"]')[1]
	except: return None 

    
def scrape_name(e):
	try: return e.find_element(By.XPATH, './/h1').text
	except: return ''
	

def scrape_address(e):
	try: return e.find_element(By.XPATH, './/button[@data-item-id="address"]').text
	except: return ''


def scrape_district(e):
	try: return e.find_element(By.XPATH, './/button[@data-item-id="address"]').text.split(' ')[-1]
	except: return ''


def scrape_website(e):
	try: return e.find_element(By.XPATH, './/a[@data-item-id="authority"]').get_attribute("href")
	except: return ''


def scrape_phone(e):
	try: return e.find_element(By.XPATH, './/button[contains(@data-item-id, "phone")]').text
	except: return ''

binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')
# driver = webdriver.Firefox(firefox_binary=binary)
driver = webdriver.Firefox(firefox_binary=binary, executable_path=r'C:\drivers\geckodriver.exe')

driver.maximize_window()
driver.get('https://www.google.com')
sleep(2)
driver.find_element(By.XPATH, '//div[text()="Rifiuta tutto"]').click()
sleep(2)

feed = driver.find_element(By.XPATH, '//div[@role="feed"]')
items = feed.find_elements(By.XPATH, './/a/..')
for item in items:
    a = item.find_element(By.XPATH, './/a')
    a_href = a.get_attribute('href')
    if 'support.' in a_href: continue
    if 'google.' not in a_href: continue
    label = a.get_attribute('aria-label')
    label = sanitize(label)
    print(item)
    print(label)
    break

click_on_listing(item)

card_element = get_card_element(item)

name = scrape_name(card_element)
address = scrape_address(card_element)
district = scrape_district(card_element)
website = scrape_website(card_element)
phone = scrape_phone(card_element)
emails = scrape_emails(website)
s_emails = ' '.join(emails)

