import os
import json
import time
import shutil
import datetime
import csv

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import util_ai

vault = '/home/ubuntu/vault'
model_llama3_4 = f'{vault}/llms/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf'
model_mistral_4 = f'{vault}/llms/Mistral-Nemo-Instruct-2407.Q4_0.gguf'
model_mistral_8 = f'{vault}/llms/Mistral-Nemo-Instruct-2407.Q8_0.gguf'

campaign_name = '2024-07'
# campaign_name = 'ozone-bakery-products'
campaign_slug = campaign_name.lower().strip().replace(' ', '-')


try: os.makedirs(campaign_slug)
except: pass

def scrape_studies_latest():
    query = 'ozone'
    query_plus = query.replace(' ', '+')
    url = f'https://scholar.google.com/scholar?hl=it&as_sdt=0%2C5&q={query_plus}&btnG='
    query_slug = query.lower().strip().replace(' ', '-')
    driver = webdriver.Firefox()
    # driver.maximize_window()
    driver.get('https://scholar.google.com/')
    time.sleep(5)
    driver.get(url)
    time.sleep(5)
    # driver.find_element(By.XPATH, '//input[@name="q"]').send_keys('ozone')
    # time.sleep(2)
    recent_studies_url = driver.find_element(By.XPATH, '//a[contains(text(), "Ordina per data")]').get_attribute('href')
    driver.get(recent_studies_url)
    time.sleep(5)
    for _ in range(10):
        elements = driver.find_elements(By.XPATH, '//h3/..')
        for e in elements:
            try: study_title = e.find_element(By.XPATH, './/h3/a').text
            except: continue
            try: study_url = e.find_element(By.XPATH, './/h3/a').get_attribute('href')
            except: continue
            try: study_days = e.find_element(By.XPATH, './/div[2]').text
            except: continue
            if study_days.split(' ')[0].isdigit(): study_days = int(study_days.split(' ')[0])
            else: continue
            
            study_datetime = datetime.datetime.today() - datetime.timedelta(study_days)
            study_date = study_datetime.strftime('%Y-%m-%d')
            print(study_date)
            
            with open(f'{vault}/studies/master.csv', 'a', newline='') as f: pass
            
            # find last id
            last_id = 0
            found = False
            with open(f'{vault}/studies/master.csv', newline='') as f:
                reader = csv.reader(f, delimiter='\\')
                for row in reader:
                    csv_id = int(row[0])
                    if last_id < csv_id: last_id = csv_id
            
            # find if url already in "master"
            found = False
            with open(f'{vault}/studies/master.csv', newline='') as f:
                reader = csv.reader(f, delimiter='\\')
                for row in reader:
                    csv_url = row[3]
                    print(study_url)
                    print(csv_url)
                    print()
                    if study_url == csv_url:
                        found = True
                        break
            
            if not found:        
                with open(f'{vault}/studies/master.csv', 'a', newline='') as f:
                    writer = csv.writer(f, delimiter='\\')
                    writer.writerow([
                        last_id+1,
                        study_date,
                        study_title,
                        study_url,
                    ])
                
        time.sleep(5)
        next_page_url = driver.find_element(By.XPATH, '//*[contains(text(), "Avanti")]/..').get_attribute('href')
        driver.get(next_page_url)
    driver.close()


def scrape_studies_query():
    query = campaign_name
    query_plus = query.replace(' ', '+')
    url = f'https://scholar.google.com/scholar?hl=it&as_sdt=0%2C5&q={query_plus}&btnG='
    query_slug = query.lower().strip().replace(' ', '-')
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get('https://scholar.google.com/')
    time.sleep(5)
    driver.get(url)
    time.sleep(5)
    # driver.find_element(By.XPATH, '//input[@name="q"]').send_keys('ozone')
    # time.sleep(2)
    latest_studies_url = driver.find_element(By.XPATH, '//a[contains(text(), "Ordina per data")]').get_attribute('href')
    driver.get(latest_studies_url)
    time.sleep(5)
    data = {}
    data_filepath = f'{campaign_slug}/data.json'
    try: 
        with open(data_filepath) as f: data = json.load(f)
    except:
        with open(data_filepath, 'w') as f: json.dump(data, f)
    if 'studies' not in data: data['studies'] = []
    with open(data_filepath, 'w') as f: 
        json.dump(data, f)
    for i in range(10):
        elements = driver.find_elements(By.XPATH, '//h3/..')
        for e in elements:
            try: study_url = e.find_element(By.XPATH, './/h3/a').get_attribute('href')
            except: continue
            found = False
            for obj in data['studies']:
                if obj['study_url'] == study_url:
                    found = True
            if not found: 
                data['studies'].append({
                    'study_url': study_url,
                })
                with open(data_filepath, 'w') as f: json.dump(data, f)
        time.sleep(5)
        driver.get(f'https://scholar.google.com/scholar?start={i+1}0&q=ozone+bakery+products&hl=it&as_sdt=0,5')
        # next_page_url = driver.find_element(By.XPATH, '//*[contains(text(), "Avanti")]/..').get_attribute('href')
        # driver.get(next_page_url)

def filter_month(mm):
    with open('data.json') as f: data = json.load(f)
    studies = data['studies']
    data_filtered = {'studies': []}
    for obj in studies:
        study_url = obj['study_url']
        study_days = obj['study_days']
        study_days = int(study_days) + 5
        d = datetime.datetime.today() - datetime.timedelta(days=study_days)
        month = d.month
        if month == mm: 
            data_filtered['studies'].append(obj)
    with open('2024-06/data.json', 'w') as f: json.dump(data_filtered, f)

def scrape_content():
    with open(f'{campaign_slug}/data.json') as f: 
        data = json.load(f)
    if 'studies' not in data: 
        print('scrape studies urls first')
        return
    studies = data['studies']
    driver = webdriver.Firefox()
    driver.get('https://google.com/')
    for i, study in enumerate(studies[:999]):
        print(f'{i}/{len(studies)}')
        try: 
            os.makedirs(f'{campaign_slug}/studies_content/{i}')
        except: 
            print('failed creating folder')
            continue
        if os.path.exists(f'{campaign_slug}/studies_content/{i}/content.txt'): 
            continue
        study_url = study['study_url'] 
        try: 
            r = requests.get(study_url, timeout=10)
        except:
            print('cant request url')
            continue
        try: 
            content_type = r.headers.get('content-type')
        except:
            print('cant get header')
            continue
        if 'application/pdf' in content_type:
            print('skip pdf file')
            continue
        try: 
            driver.get(study_url)
        except: 
            print('cant open page')
            print(study_url)
            continue
        time.sleep(5)
        try:
            text = driver.find_element(By.XPATH, '//body').text
        except:
            print('cant get body')
            print(study_url)
            continue
        with open(f'{campaign_slug}/studies_content/{i}/content.txt', 'w') as f: f.write(text)


def scrape_content_new():
    studies_rows = []
    with open(f'{vault}/studies/master.csv', newline='') as f:
        reader = csv.reader(f, delimiter='\\')
        for row in reader:
            studies_rows.append(row)

    driver = webdriver.Firefox()
    driver.get('https://google.com/')
    for study_row in studies_rows:
        study_id = study_row[0]
        study_date = study_row[1]
        study_title = study_row[2]
        study_url = study_row[3]
    
        print(f'{study_id}/{len(studies_rows)}')
        raw_folderpath = f'{vault}/studies/raw'
        if os.path.exists(f'{raw_folderpath}/{study_id}.txt'): continue

        try: 
            r = requests.get(study_url, timeout=10)
        except:
            print('cant request url')
            continue
        try: 
            content_type = r.headers.get('content-type')
        except:
            print('cant get header')
            continue
        if 'application/pdf' in content_type:
            print('skip pdf file')
            continue
        try: 
            driver.get(study_url)
        except: 
            print('cant open page')
            print(study_url)
            continue
        time.sleep(5)
        try:
            text = driver.find_element(By.XPATH, '//body').text
        except:
            print('cant get body')
            print(study_url)
            continue
        with open(f'{raw_folderpath}/{study_id}.txt', 'w') as f: f.write(text)

def filter_chain(filter_strength, queries):
    studies_content_foldernames = f'{campaign_slug}/studies_content'
    queries_folderpaths = [f'{campaign_slug}/studies_filtered/{query}' for query in queries]
    folders_to_delete = os.listdir(f'{campaign_slug}/studies_filtered')
    for folder in folders_to_delete:
        try: shutil.rmtree(f'{campaign_slug}/studies_filtered/{folder}', ignore_errors=True)
        except: pass
    queries_folderpaths.insert(0, f'{campaign_slug}/studies_content')
    for query_index, query in enumerate(queries):
        try: os.makedirs(queries_folderpaths[query_index+1])
        except: pass
        studies_folderpaths_in = queries_folderpaths[query_index]
        studies_folderpaths_out = queries_folderpaths[query_index+1]
        studies_filenames_in = os.listdir(studies_folderpaths_in)
        for study_filename_in in studies_filenames_in[:]:
            study_filepath_in = f'{studies_folderpaths_in}/{study_filename_in}/content.txt'
            try: 
                with open(study_filepath_in) as f: content = f.read()
            except: pass
            content = ' '.join(content.split(' ')[:2000])
            if filter_strength == 0:
                filter_prompt = 'mention'
            elif filter_strength == 1:
                filter_prompt = 'mainly talks about'
            else:
                filter_prompt = 'talks about'
            prompt = f'''
                Tell me if this STUDY {filter_prompt} {query}.
                Follow the GUIDELINES below.
                GUIDELINES
                Reply with only "YES" or "NO"
                Reply with only 1 word
                STUDY:
                {content}
            '''
            reply = util_ai.gen_reply(prompt)
            if reply.strip().lower() == 'yes':
                try: os.makedirs(f'{studies_folderpaths_out}')
                except: pass
                try: os.makedirs(f'{studies_folderpaths_out}/{study_filename_in}')
                except: pass
                with open(f'{studies_folderpaths_out}/{study_filename_in}/content.txt', 'w') as f: f.write(content)
    try: shutil.rmtree(f'{campaign_slug}/studies_filtered/final', ignore_errors=True)
    except: pass
    shutil.copytree(queries_folderpaths[-1], f'{campaign_slug}/studies_filtered/final')
    

def summarize_paragraphs():
    folder = 'final'
    try: shutil.rmtree(f'{campaign_slug}/studies_summaries_paragraphs', ignore_errors=True)
    except: pass
    try: os.makedirs(f'{campaign_slug}/studies_summaries_paragraphs')
    except: pass
    studies_foldernames_in = os.listdir(f'{campaign_slug}/studies_filtered/{folder}')
    for study_foldername_in in studies_foldernames_in:
        study_folderpath_in = f'{campaign_slug}/studies_filtered/{folder}/{study_foldername_in}/content.txt'
        with open(study_folderpath_in) as f: content = f.read()
        content = ' '.join(content.split(' ')[:2000])
        prompt = f'''
            Summarize the following STUDY in 1 detailed paragraph.
            GUIDELINES
            Focus the summary on the info and data related to ozone.
            The 1 paragraph must be 60-80 words long.
            Pack as much info and data in as few words as possible.
            STUDY:
            {content}
        '''
        reply = util_ai.gen_reply(prompt)
        try: os.makedirs(f'{campaign_slug}/studies_summaries_paragraphs/{study_foldername_in}')
        except: pass
        with open(f'{campaign_slug}/studies_summaries_paragraphs/{study_foldername_in}/content.txt', 'w') as f: 
            f.write(reply)

def translate_paragraphs():
    try: shutil.rmtree(f'{campaign_slug}/studies_translations_paragraphs', ignore_errors=True)
    except: pass
    try: os.makedirs(f'{campaign_slug}/studies_translations_paragraphs')
    except: pass
    studies_foldernames_in = os.listdir(f'{campaign_slug}/studies_summaries_paragraphs')
    for study_foldername_in in studies_foldernames_in:
        study_folderpath_in = f'{campaign_slug}/studies_summaries_paragraphs/{study_foldername_in}/content.txt'
        with open(study_folderpath_in) as f: content = f.read()
        content = ' '.join(content.split(' ')[:2000])
        prompt = f'''
            Traduci in Italinao il seguente STUDIO.
            ## STUDIO
            {content}
        '''
        reply = util_ai.gen_reply(prompt)
        try: os.makedirs(f'{campaign_slug}/studies_translations_paragraphs/{study_foldername_in}')
        except: pass
        with open(f'{campaign_slug}/studies_translations_paragraphs/{study_foldername_in}/content.txt', 'w') as f: 
            f.write(reply)

def filter_studies_categories():
    foldername_in = f'{campaign_slug}/studies_content'
    studies_foldernames = os.listdir(foldername_in)
    try: shutil.rmtree(f'{campaign_slug}/studies_filtered', ignore_errors=True)
    except: pass
    try: os.makedirs(f'{campaign_slug}/studies_filtered')
    except: pass
    for i, study_foldername in enumerate(studies_foldernames[:]):
        study_filepath = f'{campaign_slug}/studies_content/{study_foldername}/content.txt'
        print(study_filepath)
        if not os.path.exists(study_filepath): continue
        with open(study_filepath) as f: content = f.read()
        content = ' '.join(content.split(' ')[:2000])
        # print(content)
        prompt = f'''
            Give me the category of the following STUDY.
            Follow the the GUIDELINES below.
            GUIDELINES:
            if the study is more about ozone sanitization, reply with the word "SANITIZATION".
            if the study is more about ozone therapy, reply with the word "THERAPY".
            if the study is more about environmental ozone, reply with the word "ENVIRONMENT".
            if the study is more about processing using ozone, reply with the word "PROCESSING".
            if the study is more about ozone technology, reply with the word "TECHNOLOGY".
            if none of the above, reply with the word "OTHER".
            reply with only 1 words.
            STUDY:
            {content}
        '''
        reply = util_ai.gen_reply(prompt)
        print('***********************')
        print('\n\n\n\n\n')
        category_slug = 'sanitization'
        if reply.strip().lower() == category_slug:
            if not os.path.exists(f'studies_sorted/{category_slug}'): os.makedirs(f'studies_sorted/{category_slug}')
            if not os.path.exists(f'studies_sorted/{category_slug}/{study_foldername}'): os.makedirs(f'studies_sorted/{category_slug}/{study_foldername}')
            with open(f'studies_sorted/{category_slug}/{study_foldername}/study-text.txt', 'w') as f:
                f.write(content)
        category_slug = 'therapy'
        if reply.strip().lower() == category_slug:
            if not os.path.exists(f'studies_sorted/{category_slug}'): os.makedirs(f'studies_sorted/{category_slug}')
            if not os.path.exists(f'studies_sorted/{category_slug}/{study_foldername}'): os.makedirs(f'studies_sorted/{category_slug}/{study_foldername}')
            with open(f'studies_sorted/{category_slug}/{study_foldername}/study-text.txt', 'w') as f:
                f.write(content)
        category_slug = 'environment'
        if reply.strip().lower() == category_slug:
            if not os.path.exists(f'studies_sorted/{category_slug}'): os.makedirs(f'studies_sorted/{category_slug}')
            if not os.path.exists(f'studies_sorted/{category_slug}/{study_foldername}'): os.makedirs(f'studies_sorted/{category_slug}/{study_foldername}')
            with open(f'studies_sorted/{category_slug}/{study_foldername}/study-text.txt', 'w') as f:
                f.write(content)
        category_slug = 'processing'
        if reply.strip().lower() == category_slug:
            if not os.path.exists(f'studies_sorted/{category_slug}'): os.makedirs(f'studies_sorted/{category_slug}')
            if not os.path.exists(f'studies_sorted/{category_slug}/{study_foldername}'): os.makedirs(f'studies_sorted/{category_slug}/{study_foldername}')
            with open(f'studies_sorted/{category_slug}/{study_foldername}/study-text.txt', 'w') as f:
                f.write(content)
        category_slug = 'technology'
        if reply.strip().lower() == category_slug:
            if not os.path.exists(f'studies_sorted/{category_slug}'): os.makedirs(f'studies_sorted/{category_slug}')
            if not os.path.exists(f'studies_sorted/{category_slug}/{study_foldername}'): os.makedirs(f'studies_sorted/{category_slug}/{study_foldername}')
            with open(f'studies_sorted/{category_slug}/{study_foldername}/study-text.txt', 'w') as f:
                f.write(content)


def cluster():
    foldername_in = f'{campaign_slug}/studies_filtered/final'
    foldername_out = f'{campaign_slug}/clusters'
    try: shutil.rmtree(foldername_out, ignore_errors=True)
    except: pass
    try: os.makedirs(foldername_out)
    except: pass
    categories_slugs = ['disinfection', 'therapy', 'environment', 'processing', 'technology', 'other']
    categories_prompt = '\n'.join([
        f'if the study focuses on ozone {category}, reply with the words "{category.upper()}"'
        for category in categories_slugs
    ])
    studies_foldernames = os.listdir(foldername_in)
    for i, study_foldername in enumerate(studies_foldernames[:]):
        study_filepath = f'{foldername_in}/{study_foldername}/content.txt'
        print(study_filepath)
        if not os.path.exists(study_filepath): continue
        with open(study_filepath) as f: content = f.read()
        content = ' '.join(content.split(' ')[:2000])
        prompt = f'''
            Give me the category of the following STUDY.
            Follow the the GUIDELINES below.
            GUIDELINES:
            {categories_prompt}
            reply with only 1 word.
            STUDY:
            {content}
        '''
        reply = util_ai.gen_reply(prompt)
        print('***********************')
        print('\n\n\n\n\n')
        for category_slug in categories_slugs:
            if reply.strip().lower() == category_slug:
                try: os.makedirs(f'{foldername_out}/{category_slug}')
                except: pass
                try: os.makedirs(f'{foldername_out}/{category_slug}/{study_foldername}')
                except: pass
                with open(f'{foldername_out}/{category_slug}/{study_foldername}/content.txt', 'w') as f:
                    f.write(content)

def filter_studies_ozone():
    try: shutil.rmtree(f'studies_ozone_yes', ignore_errors=True)
    except: pass
    try: shutil.rmtree(f'studies_ozone_no', ignore_errors=True)
    except: pass
    try: os.makedirs(f'studies_ozone_yes')
    except: pass
    try: os.makedirs(f'studies_ozone_no')
    except: pass
    studies_foldernames = os.listdir('studies')
    for study_foldername in studies_foldernames:
        if not os.path.exists(f'studies/{study_foldername}/study-text.txt'): continue
        with open(f'studies/{study_foldername}/study-text.txt') as f: content = f.read()
        content = ' '.join(content.split(' ')[:2000])
        prompt = f'''
            Tell me if this STUDY mainly talks about ozone.
            Follow the GUIDELINES below.
            GUIDELINES
            Reply with only "YES" or "NO"
            Reply with only 1 word
            STUDY:
            {content}
        '''
        reply = util_ai.gen_reply(prompt)
        if reply.strip().lower() == 'yes':
            try: os.makedirs(f'studies_ozone_yes/{study_foldername}')
            except: pass
            with open(f'studies_ozone_yes/{study_foldername}/study-text.txt', 'w') as f: f.write(content)
        elif reply.strip().lower() == 'no':
            try: os.makedirs(f'studies_ozone_no/{study_foldername}')
            except: pass
            with open(f'studies_ozone_no/{study_foldername}/study-text.txt', 'w') as f: f.write(content)

def gen_summaries_paragraphs():
    try: shutil.rmtree(f'studies_summaries_paragraphs', ignore_errors=True)
    except: pass
    try: os.makedirs(f'studies_summaries_paragraphs')
    except: pass
    studies_foldernames = os.listdir('studies_ozone_yes')
    for study_foldername in studies_foldernames:
        with open(f'studies_ozone_yes/{study_foldername}/study-text.txt') as f: content = f.read()
        content = ' '.join(content.split(' ')[:2000])
        prompt = f'''
            Summarize the following STUDY in 1 detailed paragraph.
            GUIDELINES
            Focus the summary on the info and data related to ozone.
            The 1 paragraph must be 60-80 words long.
            Pack as much info and data in as few words as possible.
            STUDY:
            {content}
        '''
        reply = util_ai.gen_reply(prompt)
        try: os.makedirs(f'studies_summaries_paragraphs/{study_foldername}')
        except: pass
        with open(f'studies_summaries_paragraphs/{study_foldername}/study-text.txt', 'w') as f: f.write(reply)

def gen_summaries_sentences():
    try: shutil.rmtree(f'studies_summaries_sentences', ignore_errors=True)
    except: pass
    try: os.makedirs(f'studies_summaries_sentences')
    except: pass
    studies_foldernames = os.listdir('studies_summaries_paragraphs')
    for study_foldername in studies_foldernames:
        with open(f'studies_summaries_paragraphs/{study_foldername}/study-text.txt') as f: content = f.read()
        content = ' '.join(content.split(' ')[:2000])
        prompt = f'''
            Summarize the following STUDY in 1 detailed sentence.
            GUIDELINES
            Pack as much info and data in as few words as possible.
            Focus on the info and data related to ozone.
            STUDY:
            {content}
        '''
        reply = util_ai.gen_reply(prompt)
        try: os.makedirs(f'studies_summaries_sentences/{study_foldername}')
        except: pass
        with open(f'studies_summaries_sentences/{study_foldername}/study-text.txt', 'w') as f: f.write(reply)

def write_articles():
    foldername_in = f'{campaign_slug}/clusters'
    foldername_out = f'{campaign_slug}/articles'
    studies_foldernames = os.listdir(foldername_in)
    try: shutil.rmtree(folderpath_out, ignore_errors=True)
    except: pass
    try: os.makedirs(folderpath_out)
    except: pass
    for i, study_foldername in enumerate(studies_foldernames[:]):
        studies_filenames = os.listdir(f'{foldername_in}/{study_foldername}')
        for study_filename in studies_filenames: 
            study_filepath = f'{foldername_in}/{study_foldername}/{study_filename}'
            study_filename_formatted = int(study_filename.strip().lower())
            # if int(study_filename_formatted) != 21: continue
            if not os.path.exists(f'{foldername_in}/{study_foldername}/{study_filename}/study-text.txt'): continue
            with open(f'{foldername_in}/{study_foldername}/{study_filename}/study-text.txt') as f: 
                study_text = f.read()
            prompt = f'''
                write 5 detailed paragraphs using the info and data from the following scientific STUDY. 
                also, folloq the GUIDELINES below.
                ## STUDY
                {study_text}
                ## GUIDELINES
                in paragraph 1, write the introduction in 100 words.
                in paragraph 2, write the methods in 100 words.
                in paragraph 3, write the results in 100 words.
                in paragraph 4, write the discussions in 100 words.
                in paragraph 5, write the conclusions in 100 words.
                use the following titles for the paragraphs: Paragraph 1, Paragraph 2, Paragraph 3, Paragraph 4, Paragraph 5.
            '''
            print(prompt)
            reply = util_ai.gen_reply(prompt).strip()
            lines = reply.split('\n')
            paragraphs = []
            paragraph_curr = ''
            paragraph_start = False
            for line in lines:
                line = line.strip()
                if line == '': continue
                line = line.replace('*', '')
                if line.lower().startswith('paragraph'):
                    paragraph_start = True
                    if paragraph_curr != '':
                        if paragraph_curr.endswith('.'):
                            paragraphs.append(paragraph_curr)
                            paragraph_curr = ''
                else:
                    if paragraph_start == True:
                        paragraph_curr += line
            if paragraph_curr != '':
                if paragraph_curr.endswith('.'):
                    paragraphs.append(paragraph_curr)
            print(paragraphs)
            if len(paragraphs) == 5:
                print('***********************')
                print(paragraphs)
                print('***********************')
                for paragraph_index, paragraph in enumerate(paragraphs):
                    try: os.makedirs(f'studies_articles/{study_foldername}')
                    except: pass
                    try: os.makedirs(f'studies_articles/{study_foldername}/{study_filename}')
                    except: pass
                    with open(f'studies_articles/{study_foldername}/{study_filename}/{paragraph_index}.txt', 'w') as f:
                        f.write(paragraph)

def write_magazine_articles_titles():
    clusters_folderpath = f'{vault}/studies/{campaign_slug}/clusters'
    clusters_foldernames = os.listdir(clusters_folderpath)
    for cluster_foldername in clusters_foldernames:
        cluster_folderpath = f'{clusters_folderpath}/{cluster_foldername}'
        studies_foldernames = os.listdir(cluster_folderpath)
        for study_foldername in studies_foldernames:
            study_filepath = f'{cluster_folderpath}/{study_foldername}/content.txt'
            with open(study_filepath) as f: study_content = f.read()
            prompt = f'''
                You are a world class direct response copywriter specializing in writing advertorials. 
                Today you are going to come up with 5 unique headlines for a news advertorial.
                Get the info for the advertorial from the following STUDY.
                Also, follow the GUIDELINES below.
                ## STUDY
                {study_content}
                ## GUIDELINES
                Write only the headlines
                The best headlines for news advertorials do the following: 
                They take a generic fact and turn it into a powerful benefit-based or pain-based statement that stimulates curiosity and intrigue.
                They build desire in the reader little by little by creating the urge to keep reading.
            '''
            print(prompt)
            reply = util_ai.gen_reply(prompt) 
            filepath_out = study_filepath.replace('/clusters', '/articles') 
            filepath_out = filepath_out.replace('content.txt', 'titles.txt') 
            create_folder(study_filepath)
            with open(filepath_out, 'w') as f: f.write(reply)

def create_folder(filepath):
    chunks = filepath.split('/')[:-1]
    folderpath_curr = ''
    for chunk in chunks:
        folderpath_curr += f'{chunk}/'
        try: os.makedirs(folderpath_curr)
        except: pass
        print(folderpath_curr)

def write_articles_clusters():
    folderpath_in = f'{campaign_slug}/clusters'
    folderpath_out = f'{campaign_slug}/articles'
    '''
    try: shutil.rmtree(folderpath_out, ignore_errors=True)
    except: pass
    '''
    try: os.makedirs(folderpath_out)
    except: pass
    clusters_foldernames_in = os.listdir(folderpath_in)
    for cluster_foldername in clusters_foldernames_in:
        cluster_folderpath = f'{folderpath_in}/{cluster_foldername}'
        try: os.makedirs(cluster_folderpath)
        except: pass
        studies_foldernames = os.listdir(cluster_folderpath)
        for study_foldername in studies_foldernames:
            study_folderpath = f'{cluster_folderpath}/{study_foldername}'
            study_filepath_in = f'{study_folderpath}/content.txt'
            study_filepath_out = study_filepath_in.replace('/clusters', '/articles')
            print(study_filepath_in)
            if not os.path.exists(study_filepath_in): continue
            if os.path.exists(study_filepath_out): continue
            with open(study_filepath_in) as f: study_text = f.read()
            prompt = f'''
                write 5 detailed paragraphs using the info and data from the following scientific STUDY. 
                also, folloq the GUIDELINES below.
                ## STUDY
                {study_text}
                ## GUIDELINES
                in paragraph 1, write the introduction in 100 words.
                in paragraph 2, write the methods in 100 words.
                in paragraph 3, write the results in 100 words.
                in paragraph 4, write the discussions in 100 words.
                in paragraph 5, write the conclusions in 100 words.
                use the following titles for the paragraphs: Paragraph 1, Paragraph 2, Paragraph 3, Paragraph 4, Paragraph 5.
            '''
            print(prompt)
            reply = util_ai.gen_reply(prompt).strip()
            create_folder(study_filepath_out)
            with open(study_filepath_out, 'w') as f: f.write(reply)


def gen_articles_big():
    foldername_in = 'studies_articles'
    studies_foldernames = os.listdir(foldername_in)
    try: shutil.rmtree(f'studies_articles_big', ignore_errors=True)
    except: pass
    try: os.makedirs(f'studies_articles_big')
    except: pass
    print(studies_foldernames)
    for i, study_foldername in enumerate(studies_foldernames[:]):
        studies_filenames = os.listdir(f'{foldername_in}/{study_foldername}')
        for study_filename in studies_filenames: 
            try: studies_paragraphs_filenames = os.listdir(f'{foldername_in}/{study_foldername}/{study_filename}')
            except: continue
            for study_paragraph_filename in studies_paragraphs_filenames:
                study_paragraph_filepath = f'{foldername_in}/{study_foldername}/{study_filename}/{study_paragraph_filename}'
                print(study_paragraph_filepath)
                with open(study_paragraph_filepath) as f: content = f.read()
                prompt = f'''
                    write 1 detailed paragraph using the following DATA.
                    Also, follow the GUIDELINES below.
                    ## DATA
                    {content}
                    ## GUIDELINES
                    reply in less than 160 words
                    reply in 1 paragraph
                    don't write lists
                '''
                reply = util_ai.gen_reply(prompt).strip()
            continue
    quit()
    for _ in range(1):
            study_filepath = f'{foldername_in}/{study_foldername}/{study_filename}'
            study_filename_formatted = int(study_filename.strip().lower())
            if int(study_filename_formatted) != 21: continue
            if not os.path.exists(f'{foldername_in}/{study_foldername}/{study_filename}/study-text.txt'): continue
            with open(f'{foldername_in}/{study_foldername}/{study_filename}/study-text.txt') as f: 
                study_text = f.read()
            prompt = f'''
                write 5 detailed paragraphs using the info and data from the following scientific STUDY. 
                also, folloq the GUIDELINES below.
                ## STUDY
                {study_text}
                ## GUIDELINES
                in paragraph 1, write the introduction in 100 words.
                in paragraph 2, write the methods in 100 words.
                in paragraph 3, write the results in 100 words.
                in paragraph 4, write the discussions in 100 words.
                in paragraph 5, write the conclusions in 100 words.
                use the following titles for the paragraphs: Paragraph 1, Paragraph 2, Paragraph 3, Paragraph 4, Paragraph 5.
            '''
            print(prompt)
            reply = util_ai.gen_reply(prompt).strip()
            lines = reply.split('\n')
            paragraphs = []
            paragraph_curr = ''
            paragraph_start = False
            for line in lines:
                line = line.strip()
                if line == '': continue
                line = line.replace('*', '')
                if line.lower().startswith('paragraph'):
                    paragraph_start = True
                    if paragraph_curr != '':
                        if paragraph_curr.endswith('.'):
                            paragraphs.append(paragraph_curr)
                            paragraph_curr = ''
                else:
                    if paragraph_start == True:
                        paragraph_curr += line
            if paragraph_curr != '':
                if paragraph_curr.endswith('.'):
                    paragraphs.append(paragraph_curr)
            print(paragraphs)
            if len(paragraphs) == 5:
                print('***********************')
                print(paragraphs)
                print('***********************')
                for paragraph_index, paragraph in enumerate(paragraphs):
                    try: os.makedirs(f'studies_articles/{study_foldername}')
                    except: pass
                    try: os.makedirs(f'studies_articles/{study_foldername}/{study_filename}')
                    except: pass
                    with open(f'studies_articles/{study_foldername}/{study_filename}/{paragraph_index}.txt', 'w') as f:
                        f.write(paragraph)

def posts_linkedin():
    vault = '/home/ubuntu/vault'
    studies_disinfection_folderpath = f'{vault}/studies/2024-07/articles/disinfection'
    studies_foldernames = os.listdir(studies_disinfection_folderpath)
    for study_foldername in studies_foldernames:
        filepath_in = f'{studies_disinfection_folderpath}/{study_foldername}/content.txt'
        filepath_out = filepath_in.replace('/articles', '/linkedin')
        folderpath_out = filepath_in.replace('/articles', '/linkedin').replace('/content.txt', '')
        with open(filepath_in) as f: study_content = f.read()
        create_folder(filepath_out)
        # hooks
        prompt = f'''
            write 5 different, unique, attention-grabbing, and novel "hooks" for the following STUDY.
            follow the GUIDELINES below.
            ## STUDY
            {study_content}
            ## GUIDELINES
            - a hook is like a movie trailer, you state the problem and the hint (tease) the solution
            - each hook should be 2 sentences long
            - in sentence 1 of each hook, state the problem and include data points, numbers, and statistics
            - in sentence 2 of each hook, tease the outcome and solution
            - each sentence must be less than 10 words
            - write only the hooks
            - make each sentence a complete sentence
            - write each hook in as few words as possible
            - write each sentence in a new line
            - use a scientific and professional tone of voice
            - avoid cliche words and expressions
        '''
        # reply = util_ai.gen_reply(prompt).strip()
        # with open(f'{folderpath_out}/hooks.txt', 'w') as f: f.write(reply)
        # intro
        prompt = f'''
            write an intro section for a post about the following STUDY.
            follow the GUIDELINES below.
            ## STUDY
            {study_content}
            ## GUIDELINES
            write less than 40 words
            write 3 short sentences
            focus the intro to what are the discoveries discussed in the study
            start the reply with the following words: "according to a study "
            end the reply with the following words: "here are the highlights."
        '''
        # reply = util_ai.gen_reply(prompt).strip()
        # with open(f'{folderpath_out}/intro.txt', 'w') as f: f.write(reply)
        # highlight
        prompt = f'''
            write a numbrered list of 3-5 highlights from the following STUDY.            
            follow the GUIDELINES below.
            ## STUDY
            {study_content}
            ## GUIDELINES
            write only the highlights
            write the highlights in 10 words or less
            don't include the character ":"
            don't include notes
        '''
        # reply = util_ai.gen_reply(prompt).strip()
        # with open(f'{folderpath_out}/highlights.txt', 'w') as f: f.write(reply)
        # body
        with open(f'{folderpath_out}/highlights.txt') as f: study_highlights = f.read()
        prompt = f'''
            write a short paragraph for each of the HIGHLIGHTS below using the info from the following STUDY.
            follow the GUIDELINES below.
            ## STUDY
            {study_content}
            ## HIGHLIGHTS
            {study_highlights}
            ## GUIDELINES
            write detailed but short paragraph in less than 40 words
            include detailed examples on why this is important
            reply only with the paragraphs
            don't repeat the same or similar info between paragraphs
        '''
        # reply = util_ai.gen_reply(prompt).strip()
        # with open(f'{folderpath_out}/body.txt', 'w') as f: f.write(reply)
        # merge
        with open(f'{folderpath_out}/hooks.txt') as f: study_hooks = f.read()
        with open(f'{folderpath_out}/intro.txt') as f: study_intro = f.read()
        with open(f'{folderpath_out}/highlights.txt') as f: study_highlights = f.read()
        with open(f'{folderpath_out}/body.txt') as f: study_body = f.read()
        with open(f'{folderpath_out}/0_full.txt', 'w') as f: pass
        with open(f'{folderpath_out}/0_full.txt', 'a') as f: f.write(f'{study_hooks}\n\n')
        with open(f'{folderpath_out}/0_full.txt', 'a') as f: f.write(f'{study_intro}\n\n')
        with open(f'{folderpath_out}/0_full.txt', 'a') as f: f.write(f'{study_highlights}\n\n')
        with open(f'{folderpath_out}/0_full.txt', 'a') as f: f.write(f'{study_body}\n\n')


def filter_ozone_yesterday():
    folderpath_in = f'{vault}/studies/yesterday'
    folderpath_out = f'{vault}/studies/ozone'
    try: shutil.rmtree(folderpath_out, ignore_errors=True)
    except: pass
    try: os.makedirs(folderpath_out)
    except: pass
    filenames_in = os.listdir(folderpath_in)
    for filename_in in filenames_in:
        filepath_in = f'{folderpath_in}/{filename_in}'
        filepath_out = f'{folderpath_out}/{filename_in}'
        with open(filepath_in) as f: content = f.read()
        content = ' '.join(content.split(' ')[:2000])
        prompt = f'''
            Tell me if this STUDY talks about ozone.
            Follow the GUIDELINES below.
            GUIDELINES
            Reply with only "YES" or "NO"
            Reply with only 1 word
            STUDY:
            {content}
        '''
        reply = util_ai.gen_reply(prompt)
        if reply.strip().lower() == 'yes':
            with open(filepath_out, 'w') as f: f.write(content)

def filter_studies_yesterday():
    rows_filtered = []
    with open(f'{vault}/studies/master.csv', newline='') as f:
        reader = csv.reader(f, delimiter='\\')
        for row in reader:
            csv_id = int(row[0])
            csv_date = row[1]
            csv_date = datetime.datetime.strptime(csv_date, '%Y-%m-%d')
            csv_date = datetime.datetime.today() - csv_date
            d = int(csv_date.days)
            if d < 3:
                print(row)
                rows_filtered.append(row)

    folderpath_in = f'{vault}/studies/raw'
    folderpath_out = f'{vault}/studies/yesterday'
    try: shutil.rmtree(folderpath_out, ignore_errors=True)
    except: pass
    try: os.makedirs(folderpath_out)
    except: pass
    filenames_in = os.listdir(folderpath_in)
    for filename_in in filenames_in:
        filepath_in = f'{folderpath_in}/{filename_in}'
        filepath_out = f'{folderpath_out}/{filename_in}'
        
        found = False
        for row_filtered in rows_filtered:
            row_id = str(row_filtered[0].strip())
            file_id = filename_in.split('.')[0].strip()
            if row_id == file_id:
                found = True
                break

        if found:
            with open(filepath_in) as f: content = f.read()
            with open(filepath_out, 'w') as f: f.write(content)


def summarize_ozone_yesterday():
    folderpath_in = f'{vault}/studies/ozone'
    folderpath_out = f'{vault}/studies/processed/summary'
    try: shutil.rmtree(folderpath_out, ignore_errors=True)
    except: pass
    try: os.makedirs(folderpath_out)
    except: pass
    filenames_in = os.listdir(folderpath_in)
    for filename_in in filenames_in:
        filepath_in = f'{folderpath_in}/{filename_in}'
        filepath_out = f'{folderpath_out}/{filename_in}'
        with open(filepath_in) as f: content = f.read()
        content = ' '.join(content.split(' ')[:2000])
        prompt = f'''
            Write a 100 word detailed summary of the following STUDY.
            Follow the GUIDELINES below.
            GUIDELINES
            Write only the summary
            Focus the summary on ozone
            STUDY:
            {content}
        '''
        reply = util_ai.gen_reply(prompt)
        with open(filepath_out, 'w') as f: f.write(reply)

def summarize_ozone_new():
    summary_folderpath = f'{vault}/studies/processed/summary'
    try: shutil.rmtree(summary_folderpath, ignore_errors=True)
    except: pass
    try: os.makedirs(summary_folderpath)
    except: pass
    ozone_folderpath = f'{vault}/studies/ozone'
    ozone_filenames = os.listdir(ozone_folderpath)
    for ozone_filename in ozone_filenames:
        ozone_filepath = f'{ozone_folderpath}/{ozone_filename}'
        with open(ozone_filepath) as f: content = f.read()
        content = ' '.join(content.split(' ')[:2000])
        prompt = f'''
            Write a 100 word detailed summary of the following STUDY.
            Follow the GUIDELINES below.
            GUIDELINES
            Write only the summary
            Focus the summary on ozone
            STUDY:
            {content}
        '''
        reply = util_ai.gen_reply(prompt)
        with open(f'{summary_folderpath}/{ozone_filename}', 'w') as f: f.write(reply)

def posts_linkedin_new():
    ozone_folderpath = f'{vault}/studies/ozone'
    linkedin_folderpath = f'{vault}/studies/processed/linkedin'
    try: shutil.rmtree(linkedin_folderpath, ignore_errors=True)
    except: pass
    try: os.makedirs(linkedin_folderpath)
    except: pass
    ozone_filenames = os.listdir(ozone_folderpath)
    for ozone_filename in ozone_filenames:
        if ozone_filename != '104.txt': continue
        ozone_filepath = f'{ozone_folderpath}/{ozone_filename}'
        with open(ozone_filepath) as f: study_content = f.read()
        content = ' '.join(study_content.split(' ')[:2000])

        # hooks
        prompt = f'''
            write 5 different, unique, attention-grabbing, and novel "hooks" for the following STUDY.
            follow the GUIDELINES below.
            ## STUDY
            {study_content}
            ## GUIDELINES
            - a hook is like a movie trailer, you state the problem and the hint (tease) the solution
            - each hook should be 2 sentences long
            - in sentence 1 of each hook, state the problem and include data points, numbers, and statistics
            - in sentence 2 of each hook, tease the outcome and solution
            - each sentence must be less than 10 words
            - write only the hooks
            - make each sentence a complete sentence
            - write each hook in as few words as possible
            - write each sentence in a new line
            - use a scientific and professional tone of voice
            - avoid cliche words and expressions
        '''
        reply = util_ai.gen_reply(prompt).strip()
        filepath_out = f'{linkedin_folderpath}/hooks/{ozone_filename}'
        create_folder(filepath_out) 
        with open(filepath_out, 'w') as f: f.write(reply)

        # intro
        prompt = f'''
            write an intro section for a post about the following STUDY.
            follow the GUIDELINES below.
            ## STUDY
            {study_content}
            ## GUIDELINES
            write less than 40 words
            write 3 short sentences
            focus the intro to what are the discoveries discussed in the study
            start the reply with the following words: "according to a study "
            end the reply with the following words: "here are the highlights."
        '''
        reply = util_ai.gen_reply(prompt).strip()
        filepath_out = f'{linkedin_folderpath}/intros/{ozone_filename}'
        create_folder(filepath_out) 
        with open(filepath_out, 'w') as f: f.write(reply)

        # highlight
        prompt = f'''
            write a numbrered list of 3-5 highlights from the following STUDY.            
            follow the GUIDELINES below.
            ## STUDY
            {study_content}
            ## GUIDELINES
            write only the highlights
            focus the highlights on ozone
            don't repeat yoursel
            don't repeat the same concept between highlights
            don't repeat similar concepts between highlights
            make each highlight novel and original
            write the highlights in 10 words or less
            don't include the character ":"
            don't include notes
        '''
        reply = util_ai.gen_reply(prompt).strip()
        filepath_out = f'{linkedin_folderpath}/highlights/{ozone_filename}'
        create_folder(filepath_out) 
        with open(filepath_out, 'w') as f: f.write(reply)

        # body
        with open(f'{linkedin_folderpath}/highlights/{ozone_filename}') as f: study_highlights = f.read()
        prompt = f'''
            write a short paragraph for each of the HIGHLIGHTS below using the info from the following STUDY.
            follow the GUIDELINES below.
            ## STUDY
            {study_content}
            ## HIGHLIGHTS
            {study_highlights}
            ## GUIDELINES
            write detailed but short paragraph in less than 40 words
            include detailed examples on why this is important
            reply only with the paragraphs
            don't repeat the same or similar info between paragraphs
        '''
        reply = util_ai.gen_reply(prompt).strip()
        filepath_out = f'{linkedin_folderpath}/bodies/{ozone_filename}'
        create_folder(filepath_out) 
        with open(filepath_out, 'w') as f: f.write(reply)

        # merge
        with open(f'{linkedin_folderpath}/hooks/{ozone_filename}') as f: study_hooks = f.read()
        with open(f'{linkedin_folderpath}/intros/{ozone_filename}') as f: study_intro = f.read()
        with open(f'{linkedin_folderpath}/highlights/{ozone_filename}') as f: study_highlights = f.read()
        with open(f'{linkedin_folderpath}/bodies/{ozone_filename}') as f: study_body = f.read()
        filepath_out = f'{linkedin_folderpath}/0_full/{ozone_filename}'
        create_folder(filepath_out) 
        with open(filepath_out, 'w') as f: pass
        with open(filepath_out, 'a') as f: f.write(f'{study_hooks}\n\n')
        with open(filepath_out, 'a') as f: f.write(f'{study_intro}\n\n')
        with open(filepath_out, 'a') as f: f.write(f'{study_highlights}\n\n')
        with open(filepath_out, 'a') as f: f.write(f'{study_body}\n\n')

def gen_website_news():
    model = model_llama3_4
    # model = model_mistral_4
    folderpath_in = f'{vault}/studies/ozone'
    folderpath_out = f'{vault}/studies/processed/articles'
    # try: shutil.rmtree(folderpath_out, ignore_errors=True)
    # except: pass
    # try: os.makedirs(folderpath_out)
    # except: pass
    filenames_in = os.listdir(folderpath_in)
    for filename_in in filenames_in:
        filepath_in = f'{folderpath_in}/{filename_in}'
        filepath_out = f'{folderpath_out}/{filename_in}'.replace('.txt', '.json')
        # if os.path.exists(filepath_out): continue
        with open(filepath_in) as f: study_content = f.read()
        study_content = ' '.join(study_content.split(' ')[:2000])

        # title
        prompt = f'''
            Scrivi in Italiano 10 titoli dettagliati per il seguente STUDIO. 
            Segui le LINEE GUIDA sotto.
            ## STUDIO
            {study_content}
            ## LINEE GUIDA
            - Rispondi con una lista numerata di titoli.
            - Scrivi solo i titoli.
            - Ogni titolo deve essere originale e diverso dagli altri titoli.
            - Scrivi titoli di lunghezza variabile, da 3 a 16 parole.
            - Scrivi titoli facili da capire.
            - Scrivi titoli centrati sull'argomento ozono.
        '''
        reply = util_ai.gen_reply(prompt, model).strip()
        titles = []
        for line in reply.split('\n'):
            line = line.strip()
            if line == '': continue
            if not line[0].isdigit(): continue
            if '. ' not in line: continue
            line = '. '.join(line.split('. ')[1:])
            line = line.strip()
            if line == '': continue
            titles.append(line)

        # body
        if False:
            prompt = f'''
                Scrivi in Italiano un articolo dettagliato di 800 parole per il seguente STUDIO.
                Segui le LINEE GUIDA sotto.
                ## STUDIO
                {study_content}
                ## LINEE GUIDA
                - L'articolo deve concentrarsi sull'ozono.
                - Scrivi solo l'articolo.
                - Non scrivere il titolo.
                - Non includere le "keywords".
                - Non includere le "references".
                - Non includere sottotitoli tra i paragrafi.
                - Scrivi un articolo facile da capire.
            '''
            reply = util_ai.gen_reply(prompt, model).strip()

        # body
        prompt = f'''
            Scrivi in Italiano 5 paragrafi usando i dati del seguente STUDIO.
            Segui le LINEE GUIDA sotto.
            ## STUDIO
            {study_content}
            ## LINEE GUIDA
            - nel paragrafo 1, scrivi l'introduzione in 100 parole
            - nel paragrafo 2, scrivi i metodi in 100 parole
            - nel paragrafo 3, scrivi i risultati in 100 parole
            - nel paragrafo 4, scrivi le discussioni in 100 parole
            - nel paragrafo 5, scrivi le conclusioni in 100 parole
            - per i paragrafi usa i seguenti titoli: Paragrafo 1, Paragrafo 2, Paragrafo 3, Paragrafo 4, Paragrafo 5
        '''
        reply = util_ai.gen_reply(prompt, model).strip()
        paragraphs = []
        paragraph_curr = ''
        for line in reply.split('\n'):
            line = line.strip()
            if line == '': continue
            line = line.replace('*', '')
            if line.lower().startswith('paragrafo'):
                if paragraph_curr != '':
                    if paragraph_curr.endswith('.'):
                        paragraphs.append(paragraph_curr)
                        paragraph_curr = ''
            else:
                paragraph_curr += line
        if paragraph_curr != '':
            if paragraph_curr.endswith('.'):
                paragraphs.append(paragraph_curr)

        data = {}
        data['id'] = filename_in.split('.')[0]
        data['slug'] = 'rivoluzione-produzione-ozono-nuovo-dispositivo-hdbd'
        data['category'] = 'tecnologia'
        data['title'] = 'La rivoluzione nella Produzione di Ozono: Il Nuovo Dispositivo HDBD'
        data['titles'] = titles
        data['body'] = paragraphs

        create_folder(filepath_out) 
        print(filepath_out)
        with open(filepath_out, 'w') as f: json.dump(data, f)


# scrape_studies_query()
# filter_month(6)
# scrape_content()
# gen_taxonomy()
# gen_summaries_paragraphs()
# gen_articles()
# gen_articles_big()

# filter_chain(filter_strength='1', queries=['ozone'])
# cluster()
# summarize_paragraphs()
# translate_paragraphs()
# write_articles_clusters()
# posts_linkedin()
# write_magazine_articles_titles()

# scrape_studies_latest()
# scrape_content_new()

# filter_ozone_yesterday()
# summarize_ozone_yesterday()

# posts_linkedin_new()

gen_website_news()


