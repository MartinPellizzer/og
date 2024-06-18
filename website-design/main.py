import os
import time

import util_ai

SLEEP_TIME = 30


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
                </div>
            </section>
        </main>
        <footer></footer>
    </body>
    </html>
'''

with open('index-auto.html', 'w') as f:
    f.write(html)