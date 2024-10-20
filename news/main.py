import os
import requests
import base64
import time
import datetime
import shutil

from tkinter import *
from PIL import ImageTk, Image

from oliark_io import json_read, json_write
from oliark_llm import llm_reply

import torch
from diffusers import DiffusionPipeline, StableDiffusionXLPipeline
from diffusers import DPMSolverMultistepScheduler

checkpoint_filepath = '/home/ubuntu/vault/stable-diffusion/checkpoints/juggernautXL_juggXIByRundiffusion.safetensors'
pipe = StableDiffusionXLPipeline.from_single_file(
    checkpoint_filepath, 
    torch_dtype=torch.float16, 
    use_safetensors=True, 
    variant="fp16"
).to('cuda')
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

proj = 'ozonogroup'
query = f'ozone'.strip().lower()
query_slug = query.replace(' ', '-')

vault = '/home/ubuntu/vault'
proj_folderpath = '/home/ubuntu/proj'
vault_tmp = '/home/ubuntu/vault-tmp'
pubmed_folderpath = f'{vault}/{proj}/studies/pubmed'
query_folderpath = f'{pubmed_folderpath}/{query_slug}'
master_filepath = f'{query_folderpath}/master.csv'
json_folderpath = f'{query_folderpath}/json'
news_folderpath = f'{vault}/{proj}/news'
news_rejected_folderpath = f'{news_folderpath}/rejected'
news_done_folderpath = f'{news_folderpath}/done'
news_images_folderpath = f'{news_folderpath}/images'
news_tmp_folderpath = f'{news_folderpath}/tmp'

llms_path = f'{vault}/llms'
model_path = f'{vault_tmp}/llms/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf'

def get_studies_in_rows():
    todo_folderpath = f'{query_folderpath}/json'
    jsons_filenames_todo = [f for f in os.listdir(todo_folderpath)]
    done_folderpath = f'{news_folderpath}/done'
    jsons_filenames_done = [f for f in os.listdir(done_folderpath)]
    rejected_folderpath = f'{news_folderpath}/rejected'
    jsons_filenames_rejected = [f for f in os.listdir(rejected_folderpath)]
    rows = []
    for json_filename_todo in jsons_filenames_todo:
        if json_filename_todo in jsons_filenames_done: continue
        if json_filename_todo in jsons_filenames_rejected: continue
        json_filepath = f'{todo_folderpath}/{json_filename_todo}'
        data = json_read(json_filepath)
        try: citation = data['PubmedArticle'][0]['MedlineCitation']
        except: citation = ''
        try: pmid = citation['PMID']
        except: pmid = ''
        try: article = data['PubmedArticle'][0]['MedlineCitation']['Article']
        except: article = ''
        try: date = article['ArticleDate'][0]
        except: date = ''
        try: year = date['Year']
        except: year = ''
        try: month = date['Month']
        except: month = ''
        try: day = date['Day']
        except: day = ''
        if pmid == '': continue
        if year == '': continue
        if month == '': continue
        if day == '': continue
        rows.append([pmid, year, month, day])
    return rows

def get_pmid(rows):
    pmid_todo = ''
    for i in range(999):
        date_curr = datetime.datetime.now() - datetime.timedelta(i)
        year_curr = date_curr.year
        month_curr = date_curr.month
        day_curr = date_curr.day
        year_curr = str(year_curr)
        if month_curr < 10: month_curr = f'0{month_curr}'
        else: month_curr = str(month_curr)
        if day_curr < 10: day_curr = f'0{day_curr}'
        else: day_curr = str(day_curr)
        found = False
        for row in rows:
            if year_curr != row[1]: continue
            if month_curr != row[2]: continue
            if day_curr != row[3]: continue
            pmid_todo = row[0]
            print(f'{row[0]}: {row[1]}/{row[2]}/{row[3]}')
            found = True
            break
        if found:
            break
    return pmid_todo

def get_article_from_pmid(pmid):
    todo_folderpath = f'{query_folderpath}/json'
    json_filepath = f'{todo_folderpath}/{pmid}.json'
    data = json_read(json_filepath)
    try: citation = data['PubmedArticle'][0]['MedlineCitation']
    except: citation = ''
    try: pmid = citation['PMID']
    except: pmid = ''
    try: article = data['PubmedArticle'][0]['MedlineCitation']['Article']
    except: article = ''
    try: date = article['ArticleDate'][0]
    except: date = ''
    try: year = date['Year']
    except: year = ''
    try: month = date['Month']
    except: month = ''
    try: day = date['Day']
    except: day = ''
    try: title = article['ArticleTitle']
    except: title = ''
    try: abstract_text = article['Abstract']['AbstractText']
    except: abstract_text = ''
    try: journal_title = article['Journal']['Title']
    except: journal_title = ''
    try: journal_volume = article['Journal']['JournalIssue']['Volume']
    except: journal_volume = ''
    try: journal_issue = article['Journal']['JournalIssue']['Issue']
    except: journal_issue = ''
    abstract_text = ' '.join(abstract_text)
    pmid_entry.delete(0, END)
    pmid_entry.insert(0, pmid)
    date_entry.delete(0, END)
    date_entry.insert(0, f'{year}/{month}/{day}')
    journal_entry.delete(0, END)
    # journal_entry.insert(0, f'{journal_title}.{journal_volume}.{journal_issue}')
    journal_entry.insert(0, journal_title)
    study_title_entry.delete(0, END)
    study_title_entry.insert(0, title)
    abstract_text_widget.delete(1.0, END)
    abstract_text_widget.insert(END, abstract_text)
    return {
        'pmid': pmid,
        'year': year,
        'month': month,
        'day': day,
        'journal_title': journal_title,
        'journal_volume': journal_volume,
        'journal_issue': journal_issue,
        'study_title': title,
        'abstract_text': abstract_text,
    }

def get_pmid_old():
    todo_folderpath = f'{query_folderpath}/json'
    jsons_filenames_todo = [f for f in os.listdir(todo_folderpath)]
    json_filepath = f'{todo_folderpath}/{jsons_filenames_todo[0]}'
    data = json_read(json_filepath)
    try: citation = data['PubmedArticle'][0]['MedlineCitation']
    except: citation = ''
    try: pmid = citation['PMID']
    except: pmid = ''
    try: article = data['PubmedArticle'][0]['MedlineCitation']['Article']
    except: article = ''
    try: date = article['ArticleDate'][0]
    except: date = ''
    try: year = date['Year']
    except: year = ''
    try: month = date['Month']
    except: month = ''
    try: day = date['Day']
    except: day = ''
    try: title = article['ArticleTitle']
    except: title = ''
    try: abstract_text = article['Abstract']['AbstractText']
    except: abstract_text = ''
    try: journal_title = article['Journal']['Title']
    except: journal_title = ''
    try: journal_volume = article['Journal']['JournalIssue']['Volume']
    except: journal_volume = ''
    try: journal_issue = article['Journal']['JournalIssue']['Issue']
    except: journal_issue = ''
    abstract_text = ' '.join(abstract_text)
    pmid_entry.delete(0, END)
    pmid_entry.insert(0, pmid)
    date_entry.delete(0, END)
    date_entry.insert(0, f'{year}/{month}/{day}')
    journal_entry.delete(0, END)
    # journal_entry.insert(0, f'{journal_title}.{journal_volume}.{journal_issue}')
    journal_entry.insert(0, journal_title)
    study_title_entry.delete(0, END)
    study_title_entry.insert(0, title)
    abstract_text_widget.delete(1.0, END)
    abstract_text_widget.insert(END, abstract_text)
    print(pmid)
    return {
        'pmid': pmid,
        'year': year,
        'month': month,
        'day': day,
        'journal_title': journal_title,
        'journal_volume': journal_volume,
        'journal_issue': journal_issue,
        'study_title': title,
        'abstract_text': abstract_text,
    }

def summarize_translate(data):
    pmid = data['pmid']
    year = data['year']
    month = data['month']
    day = data['day']
    journal_title = data['journal_title']
    journal_volume = data['journal_volume']
    journal_issue = data['journal_issue']

root = Tk() 

def get_titles():
    pmid = pmid_entry.get()
    study_title = study_title_entry.get() 
    abstract_text = abstract_text_widget.get(1.0, END) 
    prompt = f'''
        write a numbered list of 10 titles for an article about the ABSTRACT below.
        use the following GUIDELINES to write the titles.
        ## GUIDELINES
        each headline must be unique, novel, and different for the others.
        each headline must be 3 to 16 words long.
        each headline must focus on ozone.
        write complete sentences.
        reply in italian.
        ## ABSTRACT
        {study_title}
        {abstract_text}
    '''
    reply = llm_reply(prompt, model_path)
    titles_textarea.delete(1.0, END)
    titles_textarea.insert(END, reply)

def get_slug():
    title = title_entry.get()
    prompt = f'''
        rewrite the following title by removing all stop words, determinative articles, and other unnecessary words.
        keep only the most important words.
        keep only the keywords.
        keep the spaces.
        don't write lists.
        write as few words as possible.
        the end result should look like a "slug" you find in a url.
        ## TITLE
        {title}
    '''
    reply = llm_reply(prompt, model_path)
    lines = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if line.endswith(':'): continue
        lines.append(line)
    if len(lines) == 1:
        reply = lines[0]
        reply = reply.replace(' ', '-').lower().strip()
        reply = reply.replace('"', '')
        slug_entry.delete(0, END)
        slug_entry.insert(0, reply)
    else:
        slug_entry.delete(0, END)
        slug_entry.insert(0, 'bad reply')

def get_body():
    title = title_entry.get()
    journal_title = journal_entry.get()
    abstract_text = abstract_text_widget.get(1.0, END) 
    prompt = f'''
        Write a detailed article discussing the scientific study in the ABSTRACT below and using the following GUIDELINES.
        ## GUIDELINES
        The article is 4 paragraphs.
        The paragraphs are very detailed and long.
        Write each paragraph in about 60-80 words.
        Title the paragraphs as following: Paragrafo 1, Paragrafo 2, Paragrafo 3, Paragrafo 4, Paragrafo 5.
        In paragraph 1, write the introduction and include the fact that the scientific study discussed was publisced by the following publication: "{journal_title}".
        In paragraph 2, write the methods.
        In paragraph 3, write the results.
        In paragraph 4, write the conclusions.
        Write the paragraphs in an easy and simple to understand way.
        Clarify and expand on concepts that are not easily understandable by most people.
        Include the name of the publication in the article: {journal_title}. 
        Include info about ozone from the abstract.
        Don't repeat yourself.
        Don't include the title of the study in the abstract.
        Don't include refereces to links, e.g. (1), etc...
        Don't include html tags.
        Reply in Italian.
        ## ABSTRACT
        {title}
        {abstract_text}
    '''
    reply = llm_reply(prompt, model_path)
    paragraphs = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if 'paragrafo' in line.lower(): continue
        if '**' in line.lower(): continue
        paragraphs.append(line)
    if len(paragraphs) == 5:
        print('***********************')
        for paragraph in paragraphs:
            print(paragraph)
            print()
        print('***********************')
        
    body_textarea.delete(1.0, END)
    body_textarea.insert(END, '\n\n'.join(paragraphs))

def get_image():
    global images
    for filename in os.listdir('tmp'):
        os.remove(f'tmp/{filename}')
    images = []
    prompt = image_entry.get()
    if prompt.strip() == '': return
    if image_var.get() == 1:
        export_filepath = f'tmp/final.jpg'
        '''
        payload = {
            "prompt": prompt,
            "width": 1024,
            "height": 1024,
            "steps": 25,
            "cfg_scale": 6,
            "denoising_strength": 0.7,
            "sampler_name": "DPM++ 2M",
            "scheduler": "Karras",
            "seed": -1,
            "batch_size": 1
        }
        response = requests.post(url='http://127.0.0.1:7860/sdapi/v1/txt2img', json=payload)
        r = response.json()
        with open(export_filepath, 'wb') as f:
            f.write(base64.b64decode(r['images'][0]))
        '''
        image = pipe(prompt=prompt, num_inference_steps=25).images[0]
        image.save(export_filepath)
    else:
        tags = prompt.split(', ')
        tag_curr = ''
        for i, tag in enumerate(tags):
            print(f'gen img: {i+1}/{len(tags)}')
            tag_curr += f'{tag}, '
            prompt = tag_curr[:-2]
            payload = {
                "prompt": prompt,
                "width": 1024,
                "height": 1024,
                "steps": 25,
                "cfg_scale": 6,
                "denoising_strength": 0.7,
                "sampler_name": "DPM++ 2M",
                "scheduler": "Karras",
                "seed": -1,
                "batch_size": 1
            }
            response = requests.post(url='http://127.0.0.1:7860/sdapi/v1/txt2img', json=payload)
            r = response.json()
            img_name = i
            if i < 10: img_name = f'0{i}'
            if i == len(tags) - 1: 
                img_name == 'final'
            else:
                print(f'{i}--{len(tags)-1}')
                print(type(i), type(len(tags)))
            export_filepath = f'tmp/{img_name}.jpg'
            with open(export_filepath, 'wb') as f:
                f.write(base64.b64decode(r['images'][0]))

    image = Image.open(export_filepath)
    image.thumbnail((600, 600))
    image = ImageTk.PhotoImage(image)
    images.append(image)
    image_label.config(image=images[0])

def tk_get_study():
    rows = get_studies_in_rows()
    pmid = get_pmid(rows)
    article = get_article_from_pmid(pmid)
    print(article)

def tk_reject_study():
    pmid = pmid_entry.get()
    todo_folderpath = f'{query_folderpath}/json'
    json_filepath = f'{todo_folderpath}/{pmid}.json'
    rejected_folderpath = f'{news_folderpath}/rejected'
    json_filepath_out = f'{rejected_folderpath}/{pmid}.json'
    shutil.copy(json_filepath, json_filepath_out)
    
def tk_summarize_study():
    pmid = pmid_entry.get()
    study_title = study_title_entry.get() 
    abstract_text = abstract_text_widget.get(1.0, END) 
    print(abstract_text)
    prompt = f'''
        write a short and easy to understand paragraph of about 60-80 words that summarize in italian of the following study:
        {study_title}
        {abstract_text}
    '''
    reply = llm_reply(prompt, model_path)
    summary_textarea.delete(1.0, END)
    summary_textarea.insert(END, reply)

def save_article():
    pmid = pmid_entry.get()
    date = date_entry.get()
    year = date.split('/')[0]
    month = date.split('/')[1]
    day = date.split('/')[2]
    title = title_entry.get()
    slug = slug_entry.get()
    category = category_entry.get()
    body = body_textarea.get(1.0, END) 
    body = body.strip().split('\n\n')

    date_curr = datetime.datetime.now()
    year_curr = date_curr.year
    month_curr = date_curr.month
    day_curr = date_curr.day
    year_curr = str(year_curr)
    if month_curr < 10: month_curr = f'0{month_curr}'
    else: month_curr = str(month_curr)
    if day_curr < 10: day_curr = f'0{day_curr}'
    else: day_curr = str(day_curr)
    date_final = f'{year_curr}/{month_curr}/{day_curr}'

    data = {
        'id': pmid,
        'year': year,
        'month': month,
        'day': day,
        'title': title,
        'slug': slug,
        'category': category,
        'body': body,
        'date_published': date_final,
    }
    json_write(f'{news_done_folderpath}/{pmid}.json', data)
    shutil.copy('tmp/final.jpg', f'{news_images_folderpath}/{pmid}.jpg')
    shutil.copy('tmp/final.jpg', f'{vault}/ozonogroup/website/immagini/news/{slug}.jpg')
    shutil.copy('tmp/final.jpg', f'{proj_folderpath}/og/website/public/immagini/news/{slug}.jpg')

# study
width = 100
study_frame = Frame(root)
study_frame.pack(side=LEFT)
pmid_label = Label(study_frame, text='pmid')
pmid_label.pack()
pmid_entry = Entry(study_frame)
pmid_entry.pack()
pmid_button = Button(study_frame, text='get pmid', command=tk_get_study)
pmid_button.pack()
date_label = Label(study_frame, text='date')
date_label.pack()
date_entry = Entry(study_frame)
date_entry.pack()
journal_label = Label(study_frame, text='journal')
journal_label.pack()
journal_entry = Entry(study_frame, width=width)
journal_entry.pack()
study_title_label = Label(study_frame, text='title')
study_title_label.pack()
study_title_entry = Entry(study_frame, width=width)
study_title_entry.pack()
abstract_label = Label(study_frame, text='abstract')
abstract_label.pack()
abstract_text_widget = Text(study_frame, width=width)
abstract_text_widget.pack()
summary_button = Button(study_frame, text='summarize', command=tk_summarize_study)
summary_button.pack()
summary_textarea = Text(study_frame, width=width)
summary_textarea.pack()
reject_button = Button(study_frame, text='reject', command=tk_reject_study)
reject_button.pack()

# article
article_frame = Frame(root)
article_frame.pack(side=LEFT)

titles_label = Label(article_frame, text='titles')
titles_label.pack()
titles_textarea = Text(article_frame, width=width)
titles_textarea.pack()
titles_button = Button(article_frame, text='get titles', command=get_titles)
titles_button.pack()

title_label = Label(article_frame, text='title')
title_label.pack()
title_entry = Entry(article_frame, width=width)
title_entry.pack()

slug_label = Label(article_frame, text='slug')
slug_label.pack()
slug_entry = Entry(article_frame, width=width)
slug_entry.pack()
slug_button = Button(article_frame, text='get slug', command=get_slug)
slug_button.pack()

categories = ['sanificazione', 'medicina', 'ambiente', 'lavorazione', 'tecnologia', 'chimica']
category_label = Label(article_frame, text=f'category: {", ".join(categories)}')
category_label.pack()
category_entry = Entry(article_frame, width=width)
category_entry.pack()

body_label = Label(article_frame, text='body')
body_label.pack()
body_textarea = Text(article_frame, width=width)
body_textarea.pack()
body_button = Button(article_frame, text='get body', command=get_body)
body_button.pack()

# image
image_frame = Frame(root)
image_frame.pack(side=LEFT)

image_var = IntVar()
image_var.set(1)
image_checkbutton = Checkbutton(image_frame, text='final only', variable=image_var)
image_checkbutton.pack()

image_label = Label(image_frame, text='image')
image_label.pack()
image_entry = Entry(image_frame, width=width)
image_entry.pack()
image_button = Button(image_frame, text='get image', command=get_image)
image_button.pack()

image = Image.open('img-test.png')
image.thumbnail((600, 600))
image = ImageTk.PhotoImage(image)
image_label = Label(image_frame, image=image)
image_label.pack()

save_button = Button(image_frame, text='save article', command=save_article)
save_button.pack()

images = []

root.mainloop()
