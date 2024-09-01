import os
import json
import shutil

import g

from lib import components

header_html = components.header()
footer_html = components.footer()

NEWS_LATEST_H3_LG = 'text-20'
NEWS_LATEST_P_MD = 'text-14'
NEWS_LATEST_P_SM = 'text-12'
NEWS_LATEST_H3_SM = 'text-14'
NEWS_LATEST_IMG_H = '80'

shutil.copy('style.css', 'public/style.css')

title = 'News Ozono | Ozonogroup'

vault = '/home/ubuntu/vault'
ozonogroup_folderpath = f'{vault}/ozonogroup'
news_folderpath = f'{ozonogroup_folderpath}/news'
images_folderpath = f'{news_folderpath}/images'

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

def get_month_name_from_val(num):
    month_name = ''
    if num == 1: month_name = 'Gen'
    elif num == 2: month_name = 'Feb'
    elif num == 3: month_name = 'Mar'
    elif num == 4: month_name = 'Apr'
    elif num == 5: month_name = 'Mag'
    elif num == 6: month_name = 'Giu'
    elif num == 7: month_name = 'Lug'
    elif num == 8: month_name = 'Ago'
    elif num == 9: month_name = 'Set'
    elif num == 10: month_name = 'Ott'
    elif num == 11: month_name = 'Nov'
    elif num == 12: month_name = 'Dic'
    return month_name

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
    folderpath_images = f'{vault}/ozonogroup/news/images'

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

        shutil.copy(f'{folderpath_images}/{article_id}.jpg', f'public/immagini/news/{article_slug}.jpg')

        article_title_html = f'<h1>{article_title}</h1>'
        image_src = f'/immagini/news/{article_slug}.jpg'
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

def section_2_html(news_latest):
    news = news_latest
    html = f'''
        <div class="container-xl mob-flex mb-48 gap-48">
            <div class="flex-2">
                <div class="border-0 border-b-4 border-solid border-black mb-24">
                    <h2 class="text-16 font-normal uppercase bg-black text-white pl-16 pr-16 pt-8 pb-4 inline-block">Ultime Notizie</h2>
                </div>
                <div class="flex gap-64">
                    <div class="flex-1">
                        <a href="/news/{news[0]['category']}/{news[0]['image']}.html" class="no-underline">
                            <div class="relative mb-16">
                                <img class="object-cover" height="240" src="/immagini/news/{news_latest[0]['image']}.jpg" alt="">
                                <p class="absolute bottom-0 text-12 bg-black text-white pl-8 pr-8 pt-2 pb-2">Sanificazione</p>
                            </div>
                            <h3 class="{NEWS_LATEST_H3_LG} font-normal mb-8">{news_latest[0]['title']}</h3>
                            <p class="{NEWS_LATEST_P_SM} mb-16"><span class="font-bold text-black">Ozonogroup</span> - {news_latest[0]['date']}</p>
                            <p class="{NEWS_LATEST_P_MD} mb-0">{news_latest[0]['desc_md']}</p>
                        </a>
                    </div>
                    <div class="flex-1 flex flex-col gap-24">
                        <a href="/news/{news[1]['category']}/{news[1]['image']}.html" class="no-underline">
                            <div class="flex gap-16">
                                <div class="flex-2">
                                    <img class="object-cover" height="{NEWS_LATEST_IMG_H}" src="/immagini/news/{news_latest[1]['image']}.jpg" alt="">
                                </div>
                                <div class="flex-5">
                                    <h3 class="{NEWS_LATEST_H3_SM} mb-8">{news_latest[1]['title']}</h3>
                                    <p class="text-12">{news_latest[1]['date']}</p>
                                </div>
                            </div>
                        </a>
                        <a href="/news/{news[2]['category']}/{news[2]['image']}.html" class="no-underline">
                            <div class="flex gap-16">
                                <div class="flex-2">
                                    <img class="object-cover" height="{NEWS_LATEST_IMG_H}" src="/immagini/news/{news_latest[2]['image']}.jpg" alt="">
                                </div>
                                <div class="flex-5">
                                    <h3 class="{NEWS_LATEST_H3_SM} mb-8">{news_latest[2]['title']}</h3>
                                    <p class="text-12">{news_latest[2]['date']}</p>
                                </div>
                            </div>
                        </a>
                        <a href="/news/{news[3]['category']}/{news[3]['image']}.html" class="no-underline">
                            <div class="flex gap-16">
                                <div class="flex-2">
                                    <img class="object-cover" height="{NEWS_LATEST_IMG_H}" src="/immagini/news/{news_latest[3]['image']}.jpg" alt="">
                                </div>
                                <div class="flex-5">
                                    <h3 class="{NEWS_LATEST_H3_SM} mb-8">{news_latest[3]['title']}</h3>
                                    <p class="text-12">{news_latest[3]['date']}</p>
                                </div>
                            </div>
                        </a>
                        <a href="/news/{news[4]['category']}/{news[4]['image']}.html" class="no-underline">
                            <div class="flex gap-16">
                                <div class="flex-2">
                                    <img class="object-cover" height="{NEWS_LATEST_IMG_H}" src="/immagini/news/{news_latest[4]['image']}.jpg" alt="">
                                </div>
                                <div class="flex-5">
                                    <h3 class="{NEWS_LATEST_H3_SM} mb-8">{news_latest[4]['title']}</h3>
                                    <p class="text-12">{news_latest[4]['date']}</p>
                                </div>
                            </div>
                        </a>
                    </div>
                </div>
            </div>
            <div class="flex-1">
                <div>
                    <div class="border-0 border-b-4 border-solid border-black mb-24">
                        <h2 class="text-16 font-normal uppercase bg-black text-white pl-16 pr-16 pt-8 pb-4 inline-block">Resta in Contatto</h2>
                    </div>
                    <div class="flex justify-between items-center">
                        <div class="flex items-center gap-16">
                            <div class="inline-block">
                                <img width=48 height=48 src="/immagini-statiche/linkedin.png" alt="logo linkedin">
                            </div>
                            <p class="text-12 font-bold text-black">1.000+ Followers</p>
                        </div>
                        <p class="text-12 font-bold text-black">Follow</p>
                    </div>
                </div>
            </div>
        </div>
    '''
    return html

def section_3_html(news_sanificazione, news_2):
    category_2 = 'lavorazione'
    news = news_2
    news_list = []
    for i in range(4):
        try: 
            news_list.append(f'''
                <a href="/news/{category_2}/{news[i]['image']}.html" class="no-underline flex-1 flex flex-col gap-24">
                    <div class="">
                        <div class="relative mb-16">
                            <img class="object-cover" height="180" src="/immagini/news/{news[i]['image']}.jpg" alt="">
                            <p class="absolute bottom-0 text-12 bg-black text-white pl-8 pr-8 pt-2 pb-2">{category_2.title()}</p>
                        </div>
                        <h3 class="{NEWS_LATEST_H3_SM} mb-8">{news[i]['title']}</h3>
                    </div>
                </a>
            ''')
        except:
            news_list.append(f'''
                <div class="flex-1 flex flex-col gap-24">
                </div>
            ''')

    medicina = f'''
        <div class="flex-1">
            <div>
                <div class="border-0 border-b-4 border-solid border-black mb-24">
                    <h2 class="text-16 font-normal uppercase bg-black text-white pl-16 pr-16 pt-8 pb-4 inline-block">{category_2}</h2>
                </div>
                <div class="flex flex-col gap-24">
                    <div class="flex gap-24">
                        {news_list[0]}
                        {news_list[1]}
                    </div>
                    <div class="flex gap-24">
                        {news_list[2]}
                        {news_list[3]}
                    </div>
                </div>
            </div>
        </div>
    '''

    news = news_sanificazione
    sanificazione_1 = f'''
        <div class="flex-1 flex flex-col gap-24">
            <div class="">
                <a href="/news/sanificazione/{news[0]['image']}.html" class="no-underline">
                    <div class="relative mb-16">
                        <img class="object-cover" height="240" src="/immagini/news/{news[0]['image']}.jpg" alt="">
                        <p class="absolute bottom-0 text-12 bg-black text-white pl-8 pr-8 pt-2 pb-2">Sanificazione</p>
                    </div>
                    <h3 class="{NEWS_LATEST_H3_LG} font-normal mb-8">{news[0]['title']}</h3>
                    <p class="{NEWS_LATEST_P_SM} mb-16"><span class="font-bold text-black">Ozonogroup</span> - {news[0]['date']}</p>
                    <p class="{NEWS_LATEST_P_MD} mb-0">{news[0]['desc_md']}</p>
                </a>
            </div>
            <div class="flex-1 flex flex-col gap-24">
                <a href="/news/sanificazione/{news[1]['image']}.html" class="no-underline">
                    <div class="flex gap-16">
                        <div class="flex-2">
                            <img class="object-cover" height="{NEWS_LATEST_IMG_H}" src="/immagini/news/{news[1]['image']}.jpg" alt="">
                        </div>
                        <div class="flex-5">
                            <h3 class="{NEWS_LATEST_H3_SM} mb-8">{news[1]['title']}</h3>
                            <p class="text-12">{news[1]['date']}</p>
                        </div>
                    </div>
                </a>
                <a href="/news/sanificazione/{news[2]['image']}.html" class="no-underline">
                    <div class="flex gap-16">
                        <div class="flex-2">
                            <img class="object-cover" height="{NEWS_LATEST_IMG_H}" src="/immagini/news/{news[2]['image']}.jpg" alt="">
                        </div>
                        <div class="flex-5">
                            <h3 class="{NEWS_LATEST_H3_SM} mb-8">{news[2]['title']}</h3>
                            <p class="text-12">{news[2]['date']}</p>
                        </div>
                    </div>
                </a>
            </div>
        </div>
    '''
    try:
        sanificazione_2_1 = f'''
            <div class="">
                <a href="/news/sanificazione/{news[3]['image']}.html" class="no-underline">
                    <div class="relative mb-16">
                        <img class="object-cover" height="240" src="/immagini/news/{news[3]['image']}.jpg" alt="">
                        <p class="absolute bottom-0 text-12 bg-black text-white pl-8 pr-8 pt-2 pb-2">Sanificazione</p>
                    </div>
                    <h3 class="{NEWS_LATEST_H3_LG} font-normal mb-8">{news[3]['title']}</h3>
                    <p class="{NEWS_LATEST_P_SM} mb-16"><span class="font-bold text-black">Ozonogroup</span> - {news[3]['date']}</p>
                    <p class="{NEWS_LATEST_P_MD} mb-0">{news[3]['desc_md']}</p>
                </a>
            </div>
        '''
    except:
        sanificazione_2_1 = '<div></div>'

    try:
        sanificazione_2_2 = f'''
            <a href="/news/sanificazione/{news[4]['image']}.html" class="no-underline">
                <div class="flex gap-16">
                    <div class="flex-2">
                        <img class="object-cover" height="{NEWS_LATEST_IMG_H}" src="/immagini/news/{news[4]['image']}.jpg" alt="">
                    </div>
                    <div class="flex-5">
                        <h3 class="{NEWS_LATEST_H3_SM} mb-8">{news[4]['title']}</h3>
                        <p class="text-12">{news[4]['date']}</p>
                    </div>
                </div>
            </a>
        '''
    except:
        sanificazione_2_2 = '<div></div>'

    try:
        sanificazione_2_3 = f'''
            <a href="/news/sanificazione/{news[5]['image']}.html" class="no-underline">
                <div class="flex gap-16">
                    <div class="flex-2">
                        <img class="object-cover" height="{NEWS_LATEST_IMG_H}" src="/immagini/news/{news[5]['image']}.jpg" alt="">
                    </div>
                    <div class="flex-5">
                        <h3 class="{NEWS_LATEST_H3_SM} mb-8">{news[5]['title']}</h3>
                        <p class="text-12">{news[5]['date']}</p>
                    </div>
                </div>
            </a>
        '''
    except:
        sanificazione_2_3 = '<div></div>'

    sanificazione_2 = f'''
        <div class="flex-1 flex flex-col gap-24">
            {sanificazione_2_1}
            <div class="flex-1 flex flex-col gap-24">
                {sanificazione_2_2}
                {sanificazione_2_3}
            </div>
        </div>
    '''

    html = f'''
        <section class="container-xl mob-flex mb-48 gap-48">
            <div class="flex-2">
                <div class="border-0 border-b-4 border-solid border-black mb-24">
                    <h2 class="text-16 font-normal uppercase bg-black text-white pl-16 pr-16 pt-8 pb-4 inline-block">Sanificazione</h2>
                </div>
                <div class="flex gap-48">
                    {sanificazione_1}
                    {sanificazione_2}
                </div>
            </div>
            {medicina}
        </section>
    '''

    return html

def section_4_html(news, category):
    html = f'''
        <section class="container-xl mob-flex mb-48 gap-48">
            <div class="flex-2">
                <div>
                    <div class="border-0 border-b-4 border-solid border-black mb-24">
                        <h2 class="text-16 font-normal uppercase bg-black text-white pl-16 pr-16 pt-8 pb-4 inline-block">{category}</h2>
                    </div>
                    <div class="flex gap-24">
                        <div class="flex-1 flex flex-col gap-24">
                            <div class="">
                                <div class="relative mb-16">
                                    <img class="object-cover" height="180" src="/immagini/news/{news[0]['image']}.jpg" alt="">
                                    <p class="absolute bottom-0 text-12 bg-black text-white pl-8 pr-8 pt-2 pb-2">{category}</p>
                                </div>
                                <h3 class="{NEWS_LATEST_H3_SM} mb-8">{news[0]['title']}</h3>
                            </div>
                        </div>

                        <div class="flex-1 flex flex-col gap-24">
                            <div class="">
                                <div class="relative mb-16">
                                    <img class="object-cover" height="180" src="/immagini/news/{news[1]['image']}.jpg" alt="">
                                    <p class="absolute bottom-0 text-12 bg-black text-white pl-8 pr-8 pt-2 pb-2">{category}</p>
                                </div>
                                <h3 class="{NEWS_LATEST_H3_SM} mb-8">{news[1]['title']}</h3>
                            </div>
                        </div>

                        <div class="flex-1 flex flex-col gap-24">
                            <div class="">
                                <div class="relative mb-16">
                                    <img class="object-cover" height="180" src="/immagini/news/{news[2]['image']}.jpg" alt="">
                                    <p class="absolute bottom-0 text-12 bg-black text-white pl-8 pr-8 pt-2 pb-2">{category}</p>
                                </div>
                                <h3 class="{NEWS_LATEST_H3_SM} mb-8">{news[2]['title']}</h3>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="flex-1">
            </div>
        </section>
    '''
    return html

def section_5_html(news, category):
    html = f'''
        <section class="container-xl mob-flex mb-48 gap-48">
            <div class="flex-2">
                <div>
                    <div class="border-0 border-b-4 border-solid border-black mb-24">
                        <h2 class="text-16 font-normal uppercase bg-black text-white pl-16 pr-16 pt-8 pb-4 inline-block">{category}</h2>
                    </div>
                    <div class="flex flex-col gap-32">
                        <div class="flex gap-24">
                            <div class="flex-1">
                                <img class="object-cover" height="180" src="/immagini/news/{news[0]['image']}.jpg" alt="">
                            </div>
                            <div class="flex-2">
                                <h3 class="{NEWS_LATEST_H3_LG} font-normal mb-8">{news[0]['title']}</h3>
                                <p class="{NEWS_LATEST_P_SM} mb-16"><span class="font-bold text-black">Ozonogroup</span> - {news[0]['date']}</p>
                                <p class="{NEWS_LATEST_P_MD} mb-0">{news[0]['desc_lg']}</p>
                            </div>
                        </div>
                        <div class="flex gap-24">
                            <div class="flex-1">
                                <img class="object-cover" height="180" src="/immagini/news/{news[1]['image']}.jpg" alt="">
                            </div>
                            <div class="flex-2">
                                <h3 class="{NEWS_LATEST_H3_LG} font-normal mb-8">{news[1]['title']}</h3>
                                <p class="{NEWS_LATEST_P_SM} mb-16"><span class="font-bold text-black">Ozonogroup</span> - {news[1]['date']}</p>
                                <p class="{NEWS_LATEST_P_MD} mb-0">{news[1]['desc_lg']}</p>
                            </div>
                        </div>
                        <div class="flex gap-24">
                            <div class="flex-1">
                                <img class="object-cover" height="180" src="/immagini/news/{news[2]['image']}.jpg" alt="">
                            </div>
                            <div class="flex-2">
                                <h3 class="{NEWS_LATEST_H3_LG} font-normal mb-8">{news[2]['title']}</h3>
                                <p class="{NEWS_LATEST_P_SM} mb-16"><span class="font-bold text-black">Ozonogroup</span> - {news[2]['date']}</p>
                                <p class="{NEWS_LATEST_P_MD} mb-0">{news[2]['desc_lg']}</p>
                            </div>
                        </div>
                        <div class="flex gap-24">
                            <div class="flex-1">
                                <img class="object-cover" height="180" src="/immagini/news/{news[3]['image']}.jpg" alt="">
                            </div>
                            <div class="flex-2">
                                <h3 class="{NEWS_LATEST_H3_LG} font-normal mb-8">{news[3]['title']}</h3>
                                <p class="{NEWS_LATEST_P_SM} mb-16"><span class="font-bold text-black">Ozonogroup</span> - {news[3]['date']}</p>
                                <p class="{NEWS_LATEST_P_MD} mb-0">{news[3]['desc_lg']}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="flex-1">
            </div>
        </section>
    '''
    return html

def page_news():
    folderpath_in = f'{vault}/ozonogroup/news/done'
    filenames_in = os.listdir(folderpath_in)
    objects = []
    for filename_in in filenames_in:
        filepath_in = f'{folderpath_in}/{filename_in}'
        with open(filepath_in) as f: data = json.load(f)
        date = data['year'] + '/' + data['month'] + '/' + data['day']
        obj = {
            'filename': filename_in,
            'date': date,
        }
        objects.append(obj)
    objects = sorted(objects, key=lambda x: x['date'], reverse=True)

    news_featured_list = []
    news_latest_html = ''
    news_sanificazione_html = ''
    news_lavorazione_html = ''
    news_ambiente_html = ''

    news_latest = []
    news_sanitization = []
    news_lavorazione = []
    news_medicina = []
    news_chemistry = []
    news_ambiente = []

    news_latest_list = []

    for obj_i, obj in enumerate(objects):
        filename_in = obj['filename']
        filepath_in = f'{folderpath_in}/{filename_in}'
        with open(filepath_in) as f: data = json.load(f)

        article_id = data['id']
        article_year = data['year']
        article_month = data['month']
        article_day = int(data['day'])
        article_month_name = get_month_name_from_val(int(article_month))
        article_date_str = f'{article_month_name} {article_day}, {article_year}'
        article_category = data['category'].lower().strip()
        article_slug = data['slug'].lower().strip()
        article_title = data['title']
        article_paragraphs = data['body']
        article_content = ' '.join(article_paragraphs)
        article_word_num = len(article_content.split(' '))
        article_time = article_word_num // 100
        article_desc = ' '.join(article_paragraphs[0].split(' ')[:16]) + '...'
        article_desc_md = ' '.join(article_paragraphs[0].split(' ')[:24]) + '...'
        article_desc_lg = ' '.join(article_paragraphs[0].split(' ')[:32]) + '...'

        news_latest_list.append({
            'title': article_title,
            'date': article_date_str,
            'image': article_slug,
            'desc': article_desc,
            'desc_md': article_desc_md,
            'desc_lg': article_desc_lg,
        })

        bottom_opacity = 0.5
        if obj_i == 0:
            news_featured_list.append(f'''
                <a href="/news/{article_category}/{article_slug}.html" class="no-underline bg-center bg-cover card-wide card-tall flex items-end pl-16 pb-16 pr-48" style="background-image: linear-gradient(rgba(0, 0, 0, 0.0), rgba(0, 0, 0, {bottom_opacity})), url(/immagini/news/{article_slug}.jpg)">
                    <div>
                        <span class="inline-block text-12 text-white bg-black uppercase mb-16 pl-8 pr-8 pt-4 pb-4">{article_category}</span>
                        <h2 class="text-white text-24 mb-16">{article_title}</h2>
                        <p class="text-white">Ozonogroup &middot; {article_date_str}</p>
                    </div>
                </a>
            '''
            )
        elif obj_i == 1:
            news_featured_list.append(f'''
                <a href="/news/{article_category}/{article_slug}.html" class="no-underline bg-center bg-cover card-wide flex items-end pl-16 pb-16 pr-48" style="background-image: linear-gradient(rgba(0, 0, 0, 0.0), rgba(0, 0, 0, {bottom_opacity})), url(/immagini/news/{article_slug}.jpg)">
                    <div>
                        <span class="inline-block text-12 text-white bg-black uppercase mb-16 pl-8 pr-8 pt-4 pb-4">{article_category}</span>
                        <h2 class="text-white text-24">{article_title}</h2>
                    </div>
                </a>
            '''
            )
        elif obj_i == 2:
            news_featured_list.append(f'''
                <a href="/news/{article_category}/{article_slug}.html" class="no-underline bg-center bg-cover flex items-end pl-16 pb-16 pr-48" style="background-image: linear-gradient(rgba(0, 0, 0, 0.0), rgba(0, 0, 0, {bottom_opacity})), url(/immagini/news/{article_slug}.jpg)">
                    <div>
                        <span class="inline-block text-12 text-white bg-black uppercase mb-16 pl-8 pr-8 pt-4 pb-4">{article_category}</span>
                        <h2 class="text-white text-16">{article_title}</h2>
                    </div>
                </a>
            '''
            )
        elif obj_i == 3:
            news_featured_list.append(f'''
                <a href="/news/{article_category}/{article_slug}.html" class="no-underline bg-center bg-cover flex items-end pl-16 pb-16 pr-48" style="background-image: linear-gradient(rgba(0, 0, 0, 0.0), rgba(0, 0, 0, {bottom_opacity})), url(/immagini/news/{article_slug}.jpg)">
                    <div>
                        <span class="inline-block text-12 text-white bg-black uppercase mb-16 pl-8 pr-8 pt-4 pb-4">{article_category}</span>
                        <h2 class="text-white text-16">{article_title}</h2>
                    </div>
                </a>
            '''
            )

        news_latest_html += f'''
            <a class="no-underline mb-48" href="/news/{article_category}/{article_slug}.html">
                <img class="object-cover mb-16" height=300 src="/immagini/news/{article_slug}.jpg">
                <p>Ozonogroup - {article_date_str}</p>
                <h3 class="text-24 mb-16">{article_title}</h3>
                <p>{article_desc}</p>
                <p><span class="text-blue-600">{article_category}</span> - lettura di {article_time} min</p>
            </a>
        '''
        if article_category == 'sanificazione':
            news_sanificazione_html += f'''
                <a class="no-underline mb-48" href="/news/{article_category}/{article_slug}.html">
                    <img class="object-cover mb-16" height=300 src="/immagini/news/{article_slug}.jpg">
                    <p>Ozonogroup - {article_date_str}</p>
                    <h3 class="text-32 mb-16">{article_title}</h3>
                    <p>{article_desc}</p>
                    <p><span class="text-blue-600">{article_category}</span> - lettura di 8 min</p>
                </a>
            '''
        if article_category == 'lavorazione':
            news_lavorazione_html += f'''
                <a class="no-underline mb-48" href="/news/{article_category}/{article_slug}.html">
                    <img class="object-cover mb-16" height=300 src="/immagini/news/{article_slug}.jpg">
                    <p>Ozonogroup - {article_date_str}</p>
                    <h3 class="text-32 mb-16">{article_title}</h3>
                    <p>{article_desc}</p>
                    <p><span class="text-blue-600">{article_category}</span> - lettura di 8 min</p>
                </a>
            '''

        if article_category == 'ambiente':
            news_ambiente_html += f'''
                <a class="no-underline mb-48" href="/news/{article_category}/{article_slug}.html">
                    <img class="object-cover mb-16" height=300 src="/immagini/news/{article_slug}.jpg">
                    <p>Ozonogroup - {article_date_str}</p>
                    <h3 class="text-32 mb-16">{article_title}</h3>
                    <p>{article_desc}</p>
                    <p><span class="text-blue-600">{article_category}</span> - lettura di 8 min</p>
                </a>
            '''

        if article_category == 'medicina':
            news_medicina.append({
                'category': article_category,
                'title': article_title,
                'date': article_date_str,
                'image': article_slug,
                'desc': article_desc,
                'desc_md': article_desc_md,
                'desc_lg': article_desc_lg,
            })

        if article_category == 'sanificazione':
            news_sanitization.append({
                'title': article_title,
                'date': article_date_str,
                'image': article_slug,
                'desc': article_desc,
                'desc_md': article_desc_md,
                'desc_lg': article_desc_lg,
            })

        if article_category == 'lavorazione':
            news_lavorazione.append({
                'title': article_title,
                'date': article_date_str,
                'image': article_slug,
                'desc': article_desc,
                'desc_md': article_desc_md,
                'desc_lg': article_desc_lg,
            })

        if article_category == 'chimica':
            news_chemistry.append({
                'title': article_title,
                'date': article_date_str,
                'image': article_slug,
                'desc': article_desc,
                'desc_md': article_desc_md,
                'desc_lg': article_desc_lg,
            })

        if article_category == 'ambiente':
            news_ambiente.append({
                'category': article_category,
                'title': article_title,
                'date': article_date_str,
                'image': article_slug,
                'desc': article_desc,
                'desc_md': article_desc_md,
                'desc_lg': article_desc_lg,
            })

        news_latest.append({
            'title': article_title,
            'date': article_date_str,
            'image': article_slug,
            'desc': article_desc,
            'desc_md': article_desc_md,
            'desc_lg': article_desc_lg,
            'category': article_category,
        })

    news_featured_html = '\n'.join(news_featured_list)
            
    category_text_size = f'text-32'
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

            <div class="container-xl grid-container mb-48">
                {news_featured_html}
            </div>

            {section_2_html(news_latest)}

            {section_3_html(news_sanitization, news_lavorazione)}

            {section_4_html(news_medicina, 'Medicina')}

            {section_5_html(news_ambiente, 'Ambiente')}


            {footer_html}
        </body>
    '''
    with open('public/news.html', 'w') as f: f.write(html)


gen_articles()
page_news()
