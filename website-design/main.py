import os
import time
import json
import random
import requests

import lorem

import util
import util_ai

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
    filepath = 'content/outline.html'

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
    filepath = 'content/page_home.html'

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


def block_sentence():
    s = lorem.sentence()
    return f'<p>{s}</p>'


def block_paragraph():
    p = lorem.paragraph()
    return f'<p>{p}</p>'


def block_text():
    t = lorem.text()
    return f'<p>{t}</p>'


def block_image():
    filepath = f'unsplash/nature.txt'
    content = util.file_read(filepath)
    urls = content.strip().split('\n')
    url = random.choice(urls)
    return f'<img src="{url}" alt="">'


# def ai_page_home_hero():
#     content = ''
#     filepath = 'content/page_home_hero.html'

#     if os.path.exists(filepath):
#         with open(filepath) as f:
#             content = f.read()

#     if content.strip() == '':
#         prompt = f'''
#             Write the html and inline css for an hero section of a homepage about ozone sanitization.
#             '''
#         reply = util_ai.gen_reply(prompt)

#         with open(filepath, 'w') as f:
#             f.write(reply)

#         time.sleep(SLEEP_TIME)



ai_website_outline()
ai_page_home_outline()
# ai_page_home_hero()



html_h1 = f'<h1>Sanificazione Ozono</h1>' 
html_p = block_text()
html_img = block_image()

html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
        <link rel="stylesheet" href="style-auto.css">
    </head>
    <body>
        <header></header>
        
        <main>
            <section id="hero">
                <div class="container-lg">
                    {html_h1}
                    {html_p}
                    {html_img}
                </div>
            </section>
        </main>
        <footer></footer>
    </body>
    </html>
'''

with open('index-auto.html', 'w') as f:
    f.write(html)