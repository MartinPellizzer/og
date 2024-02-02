from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
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

search_text = 'salumificio treviso'




######################################################################################
# CSV
######################################################################################
def get_old_businesses(output_file):
	global sep
	if not os.path.isfile(output_file): 
		with open(output_file, 'w', encoding="utf-8") as f:
			return []
	else:
		with open(output_file, 'r', encoding="utf-8") as f:
			return [line.split(sep)[0] for line in f.readlines()]




######################################################################################
# STRINGS
######################################################################################
def sanitize(text):
	chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890,.-()\'&@ '
	encoded_string = text.encode('ascii', 'ignore')
	decoded_string = encoded_string.decode()
	text = ''
	for c in decoded_string:
		if c in chars:
			text += c
	return text


    



def open_browser():
	global driver
	driver = webdriver.Firefox()
	driver.maximize_window()
	driver.get('https://www.google.com')
	sleep(2)
	driver.find_element(By.XPATH, '//div[text()="Rifiuta tutto"]').click()
	sleep(2)


def search(search_text):
	driver.get(f'https://www.google.com/maps/search/{search_text}')


def find_new_business(old_businesses):
	global driver
	elements = driver.find_elements(By.XPATH, '//div[@role="article"]')
	for e in elements:
		label = e.get_attribute('aria-label')
		label = sanitize(label)
		if label not in old_businesses:
			return e, label
	return None, None





######################################################################################
# EMAILS
######################################################################################
def find_contact_url(url):
	contact_page = ''

	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'lxml')

	for link in soup.find_all('a'):
		if 'contatti' in str(link).lower():
			link = link.get('href')
			contact_page = link
	
	return contact_page


def scrape_emails(url):
	emails = set()

	regex_string = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'

	# homepage
	try: 
		# print('finding contact url...')
		response = requests.get(url)
		# print(response)
		matches = re.finditer(regex_string, response.text)
		for match in matches: emails.add(match.group())
	except: return emails

	# contact page 1
	try:
		# print('finding contact url...')
		contact_page = find_contact_url(url)
		response = requests.get(contact_page)
		# print(response)
		matches = re.finditer(regex_string, response.text)
		for match in matches: emails.add(match.group())
	except: return emails
	
	# print('done scraping website')
	return emails





######################################################################################
# SCRAPE
######################################################################################
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
	try: return e.find_element(By.XPATH, './/a[@data-item-id="authority"]').text
	except: return ''


def scrape_phone(e):
	try: return e.find_element(By.XPATH, './/button[contains(@data-item-id, "phone")]').text
	except: return ''



output_file = f'./exports/{search_text}.csv'.replace(' ', '_')

old_businesses = get_old_businesses(output_file)
business, label = find_new_business(old_businesses)



feed = driver.find_element(By.XPATH, '//div[@role="feed"]')
items = feed.find_elements(By.XPATH, './/a/..')
for item in items: 
    a = item.find_element(By.XPATH, './/a')
    a_href = a.get_attribute('href')
    a_aria_label = a.get_attribute('aria-label')
    text = item.text
    
    if 'support.' in a_href: continue

    lines = text.split('\n')
    business_name = lines[0].strip()
    business_category = lines[2].split('·')[0].strip()
    business_address = lines[2].split('·')[1].strip()

    # print(business_name)
    # print(business_category)
    # print(business_address)
    # print()
    # print()
    # print()

    item.click()

    sleep(3)

    
	card_element = get_card_element(item)

	name = scrape_name(card_element)
	address = scrape_address(card_element)
	district = scrape_district(card_element)
	website = scrape_website(card_element)
	phone = scrape_phone(card_element)
	emails = scrape_emails(website)
	s_emails = ' '.join(emails)
    
    print(name)
    print(address)
    print(district)
    print(website)
    print(phone)
    print(s_emails)

    break



open_browser()
search(search_text)