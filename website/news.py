import os
import shutil

from oliark_io import file_write
from oliark_io import json_read

vault = f'/home/ubuntu/vault'
public_folderpath = f'public'
output_path = f'{vault}/ozonogroup/website/ozonogroup'

shutil.copy2('style.css', f'{output_path}/style.css')

news_folderpath = f'{vault}/ozonogroup/news/done'
jsons_filepaths = [f'{news_folderpath}/{filename}' for filename in os.listdir(news_folderpath)]
news = []
for json_filepath in jsons_filepaths:
    json_data = json_read(json_filepath)
    news_id = json_data['id']
    news_year = json_data['year']
    news_month = json_data['month']
    news_day = json_data['day']
    news_title = json_data['title']
    news_slug = json_data['slug']
    news_category = json_data['category']
    news_body = json_data['body']
    if 'date_published' in json_data:
        news_date_published = json_data['date_published']
    else:
        news_date_published = '0000/00/00'
    news_dict = {
        'id': news_id,
        'year': news_year,
        'month': news_month,
        'day': news_day,
        'date_study': f'{news_year}/{news_month}/{news_day}',
        'title': news_title,
        'slug': news_slug,
        'category': news_category,
        'body': news_body,
        'date_published': news_date_published,
    }
    news.append(news_dict)
news_latest = sorted(news, key=lambda d: d['date_study'], reverse=True)
news_latest_published = sorted(news, key=lambda d: d['date_published'], reverse=True)

def section_1(news_latest):
    html = ''
    html += '<div class="container-xl grid-container mb-48">'
    html += f'''
        <a href="/news/{news_latest[0]['category']}/{news_latest[0]['slug']}.html" class="no-underline bg-center bg-cover card-wide card-tall flex items-end pl-16 pb-16 pr-48" style="background-image: linear-gradient(rgba(0, 0, 0, 0.0), rgba(0, 0, 0, 0.5)), url(/immagini/news/{news_latest[0]['slug']}.jpg)">
            <div>
                <span class="inline-block text-12 text-white bg-black uppercase mb-16 pl-8 pr-8 pt-4 pb-4">{news_latest[0]['category']}</span>
                <h2 class="text-white text-24 mb-16">{news_latest[0]['title']}</h2>
                <p class="text-white">Ozonogroup &middot; {news_latest[0]['date_study']}</p>
            </div>
        </a>
    '''
    html += f'''
        <a href="/news/{news_latest[1]['category']}/{news_latest[1]['slug']}.html" class="no-underline bg-center bg-cover card-wide flex items-end pl-16 pb-16 pr-48" style="background-image: linear-gradient(rgba(0, 0, 0, 0.0), rgba(0, 0, 0, 0.5)), url(/immagini/news/{news_latest[1]['slug']}.jpg)">
            <div>
                <span class="inline-block text-12 text-white bg-black uppercase mb-16 pl-8 pr-8 pt-4 pb-4">{news_latest[1]['category']}</span>
                <h2 class="text-white text-24">{news_latest[1]['title']}</h2>
            </div>
        </a>
    '''
    html += f'''
        <a href="/news/{news_latest[2]['category']}/{news_latest[2]['slug']}.html" class="no-underline bg-center bg-cover flex items-end pl-16 pb-16 pr-48" style="background-image: linear-gradient(rgba(0, 0, 0, 0.0), rgba(0, 0, 0, 0.5)), url(/immagini/news/{news_latest[2]['slug']}.jpg)">
            <div>
                <span class="inline-block text-12 text-white bg-black uppercase mb-16 pl-8 pr-8 pt-4 pb-4">{news_latest[2]['category']}</span>
                <h2 class="text-white text-16">{news_latest[2]['title']}</h2>
            </div>
        </a>
    '''
    html += f'''
        <a href="/news/{news_latest[3]['category']}/{news_latest[3]['slug']}.html" class="no-underline bg-center bg-cover flex items-end pl-16 pb-16 pr-48" style="background-image: linear-gradient(rgba(0, 0, 0, 0.0), rgba(0, 0, 0, 0.5)), url(/immagini/news/{news_latest[3]['slug']}.jpg)">
            <div>
                <span class="inline-block text-12 text-white bg-black uppercase mb-16 pl-8 pr-8 pt-4 pb-4">{news_latest[3]['category']}</span>
                <h2 class="text-white text-16">{news_latest[3]['title']}</h2>
            </div>
        </a>
    '''
    html += '</div>'
    return html

def section_2(news):
    news_1_html = f'''
        <div class="flex-1">
            <a href="/news/{news[0]['category']}/{news[0]['slug']}.html" class="no-underline">
                <div class="relative mb-16">
                    <img class="object-cover" height="240" src="/immagini/news/{news[0]['slug']}.jpg" alt="">
                    <p class="absolute bottom-0 text-12 bg-black text-white pl-8 pr-8 pt-2 pb-2">{news[0]['category']}</p>
                </div>
                <h3 class="text-20 font-normal mb-8">{news[0]['title']}</h3>
                <p class="text-12 mb-16"><span class="font-bold text-black">Ozonogroup</span> - {news[0]['date_study']}</p>
                <p class="text-14 mb-0">{' '.join(news[0]['body'][0].split(' ')[:32])}</p>
            </a>
        </div>
    '''
    news_list_1_html = ''
    for i in range(1, 5):
        news_list_1_html += f'''
            <a href="/news/{news[i]['category']}/{news[i]['slug']}.html" class="no-underline">
                <div class="flex gap-16">
                    <div class="flex-2">
                        <img class="object-cover" height="80" src="/immagini/news/{news[i]['slug']}.jpg" alt="">
                    </div>
                    <div class="flex-5">
                        <h3 class="text-14 mb-8">{news[i]['title']}</h3>
                        <p class="text-12">{news[i]['date_study']}</p>
                    </div>
                </div>
            </a>
        '''
    html = f'''
        <div class="container-xl mob-flex mb-48 gap-48">
            <div class="flex-2">
                <div class="border-0 border-b-4 border-solid border-black mb-24">
                    <h2 class="text-16 font-normal uppercase bg-black text-white pl-16 pr-16 pt-8 pb-4 inline-block">Ultime Notizie</h2>
                </div>
                <div class="flex gap-64">
                    {news_1_html}
                    <div class="flex-1 flex flex-col gap-24">
                        {news_list_1_html}
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

def section_3(news_latest):
    category = 'sanificazione'
    news = [obj for obj in news_latest if obj['category'] == category]
    sanificazione_title_html = f'''
        <div class="border-0 border-b-4 border-solid border-black mb-24">
            <h2 class="text-16 font-normal uppercase bg-black text-white pl-16 pr-16 pt-8 pb-4 inline-block">Sanificazione</h2>
        </div>
    '''
    sanificazione_col_1_html = f'''
        <div class="flex-1 flex flex-col gap-24">
            <div class="">
                <a href="/news/{news[0]['category']}/{news[0]['slug']}.html" class="no-underline">
                    <div class="relative mb-16">
                        <img class="object-cover" height="240" src="/immagini/news/{news[0]['slug']}.jpg" alt="">
                        <p class="absolute bottom-0 text-12 bg-black text-white pl-8 pr-8 pt-2 pb-2">{news[0]['category']}</p>
                    </div>
                    <h3 class="text-20 font-normal mb-8">{news[0]['title']}</h3>
                    <p class="text-12 mb-16"><span class="font-bold text-black">Ozonogroup</span> - {news[0]['date_study']}</p>
                    <p class="text-14 mb-0">{' '.join(news[0]['body'][0].split(' ')[:32])}</p>
                </a>
            </div>
            <div class="flex-1 flex flex-col gap-24">
                <a href="/news/{news[2]['category']}/{news[2]['slug']}.html" class="no-underline">
                    <div class="flex gap-16">
                        <div class="flex-2">
                            <img class="object-cover" height="80" src="/immagini/news/{news[2]['slug']}.jpg" alt="">
                        </div>
                        <div class="flex-5">
                            <h3 class="text-14 mb-8">{news[2]['title']}</h3>
                            <p class="text-12">{news[2]['date_study']}</p>
                        </div>
                    </div>
                </a>
                <a href="/news/{news[3]['category']}/{news[3]['slug']}.html" class="no-underline">
                    <div class="flex gap-16">
                        <div class="flex-2">
                            <img class="object-cover" height="80" src="/immagini/news/{news[3]['slug']}.jpg" alt="">
                        </div>
                        <div class="flex-5">
                            <h3 class="text-14 mb-8">{news[3]['title']}</h3>
                            <p class="text-12">{news[3]['date_study']}</p>
                        </div>
                    </div>
                </a>
            </div>
        </div>
    '''
    sanificazione_col_2_html = f'''
        <div class="flex-1 flex flex-col gap-24">
            
            <div class="">
                <a href="/news/{news[1]['category']}/{news[1]['slug']}.html" class="no-underline">
                    <div class="relative mb-16">
                        <img class="object-cover" height="240" src="/immagini/news/{news[1]['slug']}.jpg" alt="">
                        <p class="absolute bottom-0 text-12 bg-black text-white pl-8 pr-8 pt-2 pb-2">{news[1]['category']}</p>
                    </div>
                    <h3 class="text-20 font-normal mb-8">{news[1]['title']}</h3>
                    <p class="text-12 mb-16"><span class="font-bold text-black">Ozonogroup</span> - {news[1]['date_study']}</p>
                    <p class="text-14 mb-0">{' '.join(news[1]['body'][0].split(' ')[:32])}</p>
                </a>
            </div>
        
            <div class="flex-1 flex flex-col gap-24">
                <a href="/news/{news[4]['category']}/{news[4]['slug']}.html" class="no-underline">
                    <div class="flex gap-16">
                        <div class="flex-2">
                            <img class="object-cover" height="80" src="/immagini/news/{news[4]['slug']}.jpg" alt="">
                        </div>
                        <div class="flex-5">
                            <h3 class="text-14 mb-8">{news[4]['title']}</h3>
                            <p class="text-12">{news[4]['date_study']}</p>
                        </div>
                    </div>
                </a>
                <a href="/news/{news[5]['category']}/{news[5]['slug']}.html" class="no-underline">
                    <div class="flex gap-16">
                        <div class="flex-2">
                            <img class="object-cover" height="80" src="/immagini/news/{news[5]['slug']}.jpg" alt="">
                        </div>
                        <div class="flex-5">
                            <h3 class="text-14 mb-8">{news[5]['title']}</h3>
                            <p class="text-12">{news[5]['date_study']}</p>
                        </div>
                    </div>
                </a>
            </div>
        </div>
    
    '''

    category = 'lavorazione'
    news = [obj for obj in news_latest if obj['category'] == category]
    lavorazione_title_html = f'''
        <div class="border-0 border-b-4 border-solid border-black mb-24">
            <h2 class="text-16 font-normal uppercase bg-black text-white pl-16 pr-16 pt-8 pb-4 inline-block">lavorazione</h2>
        </div>
    '''
    lavorazione_grid_html = f'''
        <div class="flex gap-24">
            <a href="/news/{news[0]['category']}/{news[0]['slug']}.html" class="no-underline flex-1 flex flex-col gap-24">
                <div class="">
                    <div class="relative mb-16">
                        <img class="object-cover" height="180" src="/immagini/news/{news[0]['slug']}.jpg" alt="">
                        <p class="absolute bottom-0 text-12 bg-black text-white pl-8 pr-8 pt-2 pb-2">{news[0]['category']}</p>
                    </div>
                    <h3 class="text-14 mb-8">{news[0]['title']}</h3>
                </div>
            </a>
            <a href="/news/{news[1]['category']}/{news[1]['slug']}.html" class="no-underline flex-1 flex flex-col gap-24">
                <div class="">
                    <div class="relative mb-16">
                        <img class="object-cover" height="180" src="/immagini/news/{news[1]['slug']}.jpg" alt="">
                        <p class="absolute bottom-0 text-12 bg-black text-white pl-8 pr-8 pt-2 pb-2">{news[1]['category']}</p>
                    </div>
                    <h3 class="text-14 mb-8">{news[1]['title']}</h3>
                </div>
            </a>
        </div>
        <div class="flex gap-24">
            <a href="/news/{news[2]['category']}/{news[2]['slug']}.html" class="no-underline flex-1 flex flex-col gap-24">
                <div class="">
                    <div class="relative mb-16">
                        <img class="object-cover" height="180" src="/immagini/news/{news[2]['slug']}.jpg" alt="">
                        <p class="absolute bottom-0 text-12 bg-black text-white pl-8 pr-8 pt-2 pb-2">{news[2]['category']}</p>
                    </div>
                    <h3 class="text-14 mb-8">{news[2]['title']}</h3>
                </div>
            </a>
            <a href="/news/{news[3]['category']}/{news[3]['slug']}.html" class="no-underline flex-1 flex flex-col gap-24">
                <div class="">
                    <div class="relative mb-16">
                        <img class="object-cover" height="180" src="/immagini/news/{news[3]['slug']}.jpg" alt="">
                        <p class="absolute bottom-0 text-12 bg-black text-white pl-8 pr-8 pt-2 pb-2">{news[3]['category']}</p>
                    </div>
                    <h3 class="text-14 mb-8">{news[3]['title']}</h3>
                </div>
            </a>
        </div>
    '''

    html = f'''
        <section class="container-xl mob-flex mb-48 gap-48">
            <div class="flex-2">
                {sanificazione_title_html}
                <div class="flex gap-48">
                    {sanificazione_col_1_html}
                    {sanificazione_col_2_html}
                </div>
            </div>
            
        <div class="flex-1">
            <div>
                {lavorazione_title_html}
                <div class="flex flex-col gap-24">
                    {lavorazione_grid_html}                    
                </div>
            </div>
        </div>
    
        </section>
    

    '''
    return html

def section_4(news):
    category = 'medicina'
    news = [obj for obj in news_latest if obj['category'] == category]
    html = f'''
        <section class="container-xl mob-flex mb-48 gap-48">
            <div class="flex-2">
                <div>
                    <div class="border-0 border-b-4 border-solid border-black mb-24">
                        <h2 class="text-16 font-normal uppercase bg-black text-white pl-16 pr-16 pt-8 pb-4 inline-block">Medicina</h2>
                    </div>
                    <div class="flex gap-24">
                        <div class="flex-1 flex flex-col gap-24">
                            <a href="/news/{news[0]['category']}/{news[0]['slug']}.html" class="no-underline">
                                <div class="">
                                    <div class="relative mb-16">
                                        <img class="object-cover" height="180" src="/immagini/news/{news[0]['slug']}.jpg" alt="">
                                        <p class="absolute bottom-0 text-12 bg-black text-white pl-8 pr-8 pt-2 pb-2">{news[0]['category']}</p>
                                    </div>
                                    <h3 class="text-14 mb-8">{news[0]['title']}</h3>
                                </div>
                            </a>
                        </div>

                        <div class="flex-1 flex flex-col gap-24">
                            <a href="/news/{news[1]['category']}/{news[1]['slug']}.html" class="no-underline">
                                <div class="">
                                    <div class="relative mb-16">
                                        <img class="object-cover" height="180" src="/immagini/news/{news[1]['slug']}.jpg" alt="">
                                        <p class="absolute bottom-0 text-12 bg-black text-white pl-8 pr-8 pt-2 pb-2">{news[0]['category']}</p>
                                    </div>
                                    <h3 class="text-14 mb-8">{news[1]['title']}</h3>
                                </div>
                            </a>
                        </div>

                        <div class="flex-1 flex flex-col gap-24">
                            <a href="/news/{news[2]['category']}/{news[2]['slug']}.html" class="no-underline">
                                <div class="">
                                    <div class="relative mb-16">
                                        <img class="object-cover" height="180" src="/immagini/news/{news[2]['slug']}.jpg" alt="">
                                        <p class="absolute bottom-0 text-12 bg-black text-white pl-8 pr-8 pt-2 pb-2">{news[2]['category']}</p>
                                    </div>
                                    <h3 class="text-14 mb-8">{news[2]['title']}</h3>
                                </div>
                            </a>
                        </div>

                    </div>
                </div>
            </div>
            <div class="flex-1">
            </div>
        </section>
    '''
    return html
    

gtag = ''' 
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-TV11JVJVKC"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-TV11JVJVKC');
    </script>
'''

html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="/style.css">
        <title>News Ozono | Ozonogroup</title>
        {gtag}
    </head>
    <body>
        <header class="container-xl flex justify-between py-24">
          <a class="text-16 uppercase text-black no-underline" href="/">Ozonogroup</a>
          <nav class="flex gap-16">
              <a class="text-16 uppercase text-black no-underline" href="/news.html">News</a>
          </nav>
        </header>
        
        {section_1(news_latest)}
        {section_2(news_latest_published)}
        {section_3(news_latest)}
        {section_4(news_latest)}

        <section class="footer-section">
            <div class="container-xl h-full">
                <footer class="flex items-center justify-center">
                    <span class="text-white">Ozonogroup s.r.l. | Tutti i diritti riservati</span>
                </footer>
            </div>
        </section>
    </body>
    </html>
'''

file_write(f'{output_path}/news.html', html)

def news_articles():
    for article in news:
        article_slug = article['slug']
        article_title = article['title']
        article_category = article['category']
        article_body = article['body']
        article_body_formatted = ''
        article_body_formatted += f'<p>{article_body[0]}</p>'
        article_body_formatted += f'<h2 class="mb-16 mt-48">Metodi</h2><p>{article_body[1]}</p>'
        article_body_formatted += f'<h2 class="mb-16 mt-48">Risultati</h2><p>{article_body[2]}</p>'
        article_body_formatted += f'<h2 class="mb-16 mt-48">Conclusioni</h2><p>{article_body[3]}</p>'
        html = f'''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link rel="stylesheet" href="/style.css">
                <title>News Ozono | Ozonogroup</title>
                {gtag}
            </head>
            <body>
                <header class="container-xl flex justify-between py-24">
                  <a class="text-16 uppercase text-black no-underline" href="/">Ozonogroup</a>
                  <nav class="flex gap-16">
                      <a class="text-16 uppercase text-black no-underline" href="/news.html">News</a>
                  </nav>
                </header>
                
                <section class="container-md py-96">
                    <h1 class="mb-16">{article_title}</h1>
                    <img class="mb-16" src="/immagini/news/{article_slug}.jpg">
                    {article_body_formatted}
                </section>
                <section class="footer-section">
                    <div class="container-xl h-full">
                        <footer class="flex items-center justify-center">
                            <span class="text-white">Ozonogroup s.r.l. | Tutti i diritti riservati</span>
                        </footer>
                    </div>
                </section>
            </body>
            </html>
        '''

        file_write(f'{output_path}/news/{article_category}/{article_slug}.html', html)

news_articles()
