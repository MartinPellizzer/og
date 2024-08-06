import os
import json
import shutil

import g

shutil.copy('style.css', 'public/style.css')

title = 'News Ozono | Ozonogroup'

vault = '/home/ubuntu/vault'

header_html = f'''
    <header class="container-xl flex justify-between py-24">
        <a class="text-16 uppercase text-black no-underline" href="/">Ozonogroup</a>
        <nav class="flex gap-16">
            <a class="text-16 uppercase text-black no-underline" href="/news.html">News</a>
            <a class="text-16 uppercase text-black no-underline" href="/risorse.html">Risorse</a>
            <a class="text-16 uppercase text-black no-underline" href="/servizi.html">Servizi</a>
        </nav>
    </header>
'''

footer_html = f'''
    <section class="footer-section">
        <div class="container-xl h-full">
            <footer class="flex items-center justify-center">
                <span class="text-white">Ozonogroup s.r.l. | Tutti i diritti riservati</span>
            </footer>
        </div>
    </section>
'''

def get_articles_category(category_slug):
    folderpath_in = f'public/news/{category_slug}'
    filenames_in = os.listdir(folderpath_in)
    articles_filepaths_web = []
    for filename_in in filenames_in:
        filepath_in = f'{folderpath_in}/{filename_in}'
        articles_filepaths_web.append(f'news/{category_slug}/{filename_in}')
    return articles_filepaths_web

sanificazione_articles_filepaths = get_articles_category('sanificazione')
sanificazione_articles_html = '' 
for article_filepath in sanificazione_articles_filepaths:
    sanificazione_articles_html += f'''
        <div>
            <a href="{article_filepath}">
                <img class="object-cover mb-16" height=300 src="/immagini/test-img-2.png">
                <p>Ozonogroup - 2024/07/29</p>
                <h3 class="text-24 text-black mb-16">Oceani in pericolo: ozono per bonifica?</h3>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean molestie luctus massa sollicitudin eleifend. In hac habitasse platea dictumst. Curabitur luctus auctor auctor.</p>
                <p><span class="text-blue-600">Sanificazione</span> - lettura di 8 min</p>
            </a>
        </div>
    '''

def page_news():
    folderpath_in = f'{vault}/ozonogroup/news/done'
    filenames_in = os.listdir(folderpath_in)
    news_latest_html = ''
    news_sanificazione_html = ''
    news_ambiente_html = ''
    for filename_in in filenames_in:
        filepath_in = f'{folderpath_in}/{filename_in}'
        with open(filepath_in) as f: data = json.load(f)
        article_id = data['id']
        article_category = data['category'].lower().strip()
        article_slug = data['slug'].lower().strip()
        article_title = data['title']
        article_paragraphs = data['body']
        article_content = ' '.join(article_paragraphs)
        article_word_num = len(article_content.split(' '))
        article_time = article_word_num // 100
        article_desc = ' '.join(article_paragraphs[0].split(' ')[:16]) + '...'
        news_latest_html += f'''
            <a class="no-underline mb-48" href="/news/{article_category}/{article_slug}.html">
                <img class="object-cover mb-16" height=300 src="/immagini/news/{article_slug}.png">
                <p>Ozonogroup - 2024/07/29</p>
                <h3 class="text-24 mb-16">{article_title}</h3>
                <p>{article_desc}</p>
                <p><span class="text-blue-600">{article_category}</span> - lettura di {article_time} min</p>
            </a>
        '''
        if article_category == 'sanificazione':
            news_sanificazione_html += f'''
                <a class="no-underline mb-48" href="/news/{article_category}/{article_slug}.html">
                    <img class="object-cover mb-16" height=300 src="/immagini/news/{article_slug}.png">
                    <p>Ozonogroup - 2024/07/29</p>
                    <h3 class="text-32 mb-16">{article_title}</h3>
                    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean molestie luctus massa sollicitudin eleifend. In hac habitasse platea dictumst. Curabitur luctus auctor auctor.</p>
                    <p><span class="text-blue-600">{article_category}</span> - lettura di 8 min</p>
                </a>
            '''
        if article_category == 'ambiente':
            news_ambiente_html += f'''
                <a class="no-underline mb-48" href="/news/{article_category}/{article_slug}.html">
                    <img class="object-cover mb-16" height=300 src="/immagini/news/{article_slug}.png">
                    <p>Ozonogroup - 2024/07/29</p>
                    <h3 class="text-32 mb-16">{article_title}</h3>
                    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean molestie luctus massa sollicitudin eleifend. In hac habitasse platea dictumst. Curabitur luctus auctor auctor.</p>
                    <p><span class="text-blue-600">{article_category}</span> - lettura di 8 min</p>
                </a>
            '''
            
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="/style.css">
            <title>{title}</title>
            {g.GOOGLE_TAG}
        </head>
        <body>
            {header_html}
            <section class="py-96">
                <div class="container-xl">
                    <h1>Novita sul Mondo dell'Ozono</h1>
                </div>
            </section>
            <section class="mb-96">
                <div class="container-xl grid grid-2 items-center">
                    <img class="object-cover" height=500 src="/immagini/test-img-1.png">
                    <div>
                        <p>Ozonogroup - 2024/07/29</p>
                        <h2 class="text-48 mb-16">Oceani in pericolo: ozono per bonifica?</h2>
                        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean molestie luctus massa sollicitudin eleifend. In hac habitasse platea dictumst. Curabitur luctus auctor auctor. Suspendisse ultricies tellus ac mollis mattis. Donec bibendum lobortis diam. Integer auctor eget ligula vitae vulputate. Etiam massa sapien, volutpat et ultricies sed, auctor et tellus. Phasellus molestie vitae nulla non eleifend. Sed ultrices massa quis ex congue elementum. Donec dignissim tempus commodo.</p>
                        <p><span class="text-blue-600">Sanificazione</span> - lettura di 8 min</p>
                    </div>
                </div>
            </section>
            <section class="mb-96">
                <div class="container-xl">
                    <h2 class="text-48 mb-32">Ultime Notizie</h2>
                    <div class="grid grid-4 gap-16">
                        {news_latest_html}
                    </div>
                </div>
            </section>
            <section class="mb-96">
                <div class="container-xl">
                    <h2 class="text-48 mb-32">Sanificazione</h2>
                    <div class="grid grid-4 gap-16">
                        {news_sanificazione_html}
                    </div>
                </div>
            </section>
            <section class="mb-96">
                <div class="container-xl">
                    <h2 class="text-48 mb-32">Ambiente</h2>
                    <div class="grid grid-4 gap-16">
                        {news_ambiente_html}
                    </div>
                </div>
            </section>
            {footer_html}
        </body>
    '''
    with open('public/news.html', 'w') as f: f.write(html)


def create_folder(filepath):
    chunks = filepath.split('/')[:-1]
    folderpath_curr = ''
    for chunk in chunks:
        folderpath_curr += f'{chunk}/'
        try: os.makedirs(folderpath_curr)
        except: pass
        print(folderpath_curr)

def gen_articles():
    folderpath_in = f'{vault}/ozonogroup/news/done'

    filenames_in = os.listdir(folderpath_in)
    for filename_in in filenames_in:
        filepath_in = f'{folderpath_in}/{filename_in}'
        with open(filepath_in) as f: data = json.load(f)
        article_id = data['id']
        article_category = data['category'].lower().strip()
        article_slug = data['slug'].lower().strip()
        article_title = data['title']
        article_paragraphs = data['body']

        article_paragraphs_html = '' 
        for article_paragraph in article_paragraphs:
            article_paragraphs_html += f'<p>{article_paragraph}</p>'

        article_title_html = f'<h1>{article_title}</h1>'
        image_src = f'/immagini/news/{article_slug}.png'
        article_image_html = f'<img src="{image_src}" alt="">'
        html = f'''
            <!DOCTYPE html>
            <html lang="en">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link rel="stylesheet" href="/style.css">
                <title>{title}</title>
                {g.GOOGLE_TAG}
            </head>

            <body>
                {header_html}

                <main class="container-md py-96">
                    {article_title_html}
                    {article_image_html}
                    {article_paragraphs_html}
                </main>

                {footer_html}
            </body>
        '''

        folderpath_out = f'public/news/{article_category}'
        filepath_out = f'{folderpath_out}/{article_slug}.html'
        print(filepath_out)
        create_folder(filepath_out)
        with open(filepath_out, 'w') as f: f.write(html)

gen_articles()
page_news()
