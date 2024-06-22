import os
import time
import json
import random
import requests

import lorem

import util
import util_ai
import layout
import components

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



# ai_website_outline()
# ai_page_home_outline()



# filepath = f'content/homepage/hero-title.txt'
# util.file_append(filepath, '')
# content = util.file_read(filepath)
# if content.strip() == '':
#     prompt = f'''
#         Write me a numbered list of 10 titles for a homepage about ozone sanitization.
#         The topic is: Engaging headline highlighting the benefits of ozone generation for sanitization.
#         Write just the titles, don't add descriptions.
#         Write the titles in 5 words or less.
#     '''
#     reply = util_ai.gen_reply(prompt)
#     util.file_write(filepath, reply)

    
# filepath = f'content/homepage/hero-desc.txt'
# util.file_append(filepath, '')
# content = util.file_read(filepath)
# if content.strip() == '':
#     prompt = f'''
#         Write me a short descriptive paragraph for a homepage about ozone sanitization.
#         The topic is: Brief overview of your brand and its mission
#         Write just the description, don't add other content.
#         Write the description in 32 words or less.
#     '''
#     reply = util_ai.gen_reply(prompt)
#     util.file_write(filepath, reply)




# random_theme = random.choice(['holy', 'dark'])
# random_swap = random.choice([True, False])
# menu = layout.menu_0001(random_theme, random_swap)


# hero = layout.hero_extra_0001(title='', desc='', cta='', img='', theme='holy', swap=False)

# random_theme = random.choice(['holy', 'dark'])
# cta = layout.cta_0001(random_theme)

# contents_html = []
# for i in range(3):
#     random_theme = random.choice(['holy', 'dark'])
#     random_swap = random.choice([True, False])
#     random_func = random.choice(layout.contents)
#     contents_html.append(random_func(random_theme, random_swap))

# features_html = []
# for i in range(2):
#     random_theme = random.choice(['holy', 'dark'])
#     random_swap = random.choice([True, False])
#     # random_func = random.choice(layout.features)
#     func = layout.features[i]
#     features_html.append(func(random_theme, random_swap))

# features_html = ''.join(features_html)

# block_curr = layout.footer_0001(theme='holy', swap=False)


# html = f'''
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>Document</title>
#         <link rel="stylesheet" href="style-auto.css">
#         <link rel="stylesheet" href="tailwind.css">
#     </head>
#     <body>
#         <header></header>
        
#         <main>
#             {menu}
#             {hero}
#             {cta}

#             {contents_html[0]}
#             {contents_html[1]}
#             {contents_html[2]}

#             {features_html}

#             {block_curr}
#         </main>
#         <footer></footer>
#     </body>
#     </html>
# '''

# with open('index-auto.html', 'w') as f:
#     f.write(html)



def preview_atoms():
    atoms = []

    atoms.append(components.atom_title_primary())
    atoms.append(components.atom_title_secondary())
    atoms.append(components.atom_title_tertiary())
    atoms.append(components.atom_paragraph_primary())
    atoms.append(components.atom_link_primary())
    atoms.append(f'<div>{components.atom_button_primary()}</div>')
    atoms.append(components.atom_image())

    atoms = '<div class="py-8"></div>'.join(atoms)

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
                <section>
                    <div class="container-lg">
                        {atoms}
                    </div>
                </section>
            </main>
            <footer></footer>
        </body>
        </html>
    '''

    with open('preview-atoms.html', 'w') as f:
        f.write(html)

preview_atoms()