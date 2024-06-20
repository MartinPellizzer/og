import os
import time
import json
import random
import requests

import lorem

import util
import util_ai
import layout

SLEEP_TIME = 30


def unsplash_image_get(tag):
    filepath = f'unsplash/{tag}.txt'
    if not os.path.exists(filepath):
        util.file_write(filepath, '')
    with open('C:/api-keys/unsplash-api-key.txt', 'r') as f:
        ACCESS_KEY = f.read().strip()
    url = f'https://api.unsplash.com/search/photos?page=1&query={tag}&client_id={ACCESS_KEY}'
    response = requests.get(url)
    data = response.json()['results']
    for i, image in enumerate(data):
        image_url = image['urls']['regular']
        util.file_append(filepath, f'{image_url}\n')
        print(image_url)


# unsplash_image_get('travel')
# unsplash_image_get('nature')


def ai_website_outline():
    content = ''
    filepath = 'content/outline.txt'

    if os.path.exists(filepath):
        with open(filepath) as f:
            content = f.read()

    if content.strip() == '':
        prompt = f'''
            I have a brand that sells ozone generation for sanitization purposes. Write me an outline for my website.
            '''
        reply = util_ai.gen_reply(prompt)

        with open(filepath, 'w') as f:
            f.write(reply)

        time.sleep(SLEEP_TIME)


def ai_page_home_outline():
    content = ''
    filepath = 'content/page_home.txt'

    if os.path.exists(filepath):
        with open(filepath) as f:
            content = f.read()

    if content.strip() == '':
        prompt = f'''
            I have a brand that sells ozone generation for sanitization purposes. Write me an outline for the homepage of my website.
            '''
        reply = util_ai.gen_reply(prompt)

        with open(filepath, 'w') as f:
            f.write(reply)

        time.sleep(SLEEP_TIME)


def ai_page_home_hero():
    content = ''
    filepath = 'content/page_home_hero.txt'

    if os.path.exists(filepath):
        with open(filepath) as f:
            content = f.read()

    if content.strip() == '':
        prompt = f'''
            Write the html and inline css for an hero section of a homepage about ozone sanitization.
            '''
        reply = util_ai.gen_reply(prompt)

        with open(filepath, 'w') as f:
            f.write(reply)

        time.sleep(SLEEP_TIME)



ai_website_outline()
ai_page_home_outline()
# ai_page_home_hero()



filepath = f'content/homepage/hero-title.txt'
util.file_append(filepath, '')
content = util.file_read(filepath)
if content.strip() == '':
    prompt = f'''
        Write me a numbered list of 10 titles for a homepage about ozone sanitization.
        The topic is: Engaging headline highlighting the benefits of ozone generation for sanitization.
        Write just the titles, don't add descriptions.
        Write the titles in 5 words or less.
    '''
    reply = util_ai.gen_reply(prompt)
    util.file_write(filepath, reply)

    
filepath = f'content/homepage/hero-desc.txt'
util.file_append(filepath, '')
content = util.file_read(filepath)
if content.strip() == '':
    prompt = f'''
        Write me a short descriptive paragraph for a homepage about ozone sanitization.
        The topic is: Brief overview of your brand and its mission
        Write just the description, don't add other content.
        Write the description in 32 words or less.
    '''
    reply = util_ai.gen_reply(prompt)
    util.file_write(filepath, reply)


random_theme = random.choice(['holy', 'dark'])
random_swap = random.choice([True, False])
menu = layout.menu_0001(random_theme, random_swap)

random_theme = random.choice(['holy', 'dark'])
random_swap = random.choice([True, False])
hero = layout.hero_0001(random_theme)

random_theme = random.choice(['holy', 'dark'])
cta = layout.cta_0001(random_theme)

random_theme = random.choice(['holy', 'dark'])
random_swap = random.choice([True, False])
content_1 = layout.content_0001(random_theme, random_swap)

random_theme = random.choice(['holy', 'dark'])
random_swap = random.choice([True, False])
content_2 = layout.content_0002(random_theme, random_swap)

# content_3 = layout.content_0003(theme='', swap=False)

features_1 = layout.features_0001(theme='holy', swap=False)

for i in range(3):
    random_theme = random.choice(['holy', 'dark'])
    random_swap = random.choice([True, False])
    random_func = random.choice(layout.functions)
    content_3 = random_func(random_theme, random_swap)

html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
        <link rel="stylesheet" href="style-auto.css">
        <link rel="stylesheet" href="tailwind.css">
    </head>
    <body>
        <header></header>
        
        <main>
            {menu}
            {hero}
            {cta}
            {content_1}
            {content_2}
            {content_3}
            {features_1}
        </main>
        <footer></footer>
    </body>
    </html>
'''

with open('index-auto.html', 'w') as f:
    f.write(html)