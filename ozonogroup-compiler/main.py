import json
import os
import random
import re
import markdown
import math
import shutil
import csv
import pathlib
import util

from PIL import Image, ImageFont, ImageDraw, ImageColor



GOOGLE_TAG = '''
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-TV11JVJVKC"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', 'G-TV11JVJVKC');
    </script>
'''


def lst_to_blt(lst):
    txt = ''
    for item in lst:
        txt += f'- {item}\n'
    return txt.strip()


def lst_to_txt(lst):
    txt = ''
    if len(lst) == 0: txt = ''
    elif len(lst) == 1: txt = lst[0]
    elif len(lst) == 2: txt = f'{lst[0]} e {lst[1]}'
    else: txt = f'{", ".join(lst[:-1])} e {lst[-1]}'
    return txt


def bold_blt(lst):
    bld_lst = []
    for item in lst:
        if ':' in item:
            item_parts = item.split(":")
            bld_lst.append(f'**{item_parts[0]}**: {item_parts[1]}')
        else:
            bld_lst.append(f'{item}')
    return bld_lst


def generate_toc(content_html):
    table_of_contents_html = ''

    # get list of headers and generate IDs
    headers = []
    content_html_with_ids = ''
    current_id = 0
    for line in content_html.split('\n'):
        if '<h2>' in line:
            headers.append(line)
            content_html_with_ids += (line.replace('<h2>', f'<h2 id="{current_id}">'))
            current_id +=1
        elif '<h3>' in line:
            headers.append(line)
            content_html_with_ids += (line.replace('<h3>', f'<h3 id="{current_id}">'))
            current_id +=1
        elif '<h4>' in line:
            headers.append(line)
            content_html_with_ids += (line.replace('<h4>', f'<h4 id="{current_id}">'))
            current_id +=1
        elif '<h5>' in line:
            headers.append(line)
            content_html_with_ids += (line.replace('<h5>', f'<h5 id="{current_id}">'))
            current_id +=1
        elif '<h6>' in line:
            headers.append(line)
            content_html_with_ids += (line.replace('<h6>', f'<h6 id="{current_id}">'))
            current_id +=1
        else:
            content_html_with_ids += (line)
        content_html_with_ids += '\n'

    # generate table
    toc_li = []

    table_of_contents_html += '<div class="toc">'
    table_of_contents_html += '<span class="toc-title">Tabella dei Contenuti</span>'
    table_of_contents_html += '<ul>'
    
    last_header = '<h2>'
    for i, line in enumerate(headers):
        insert_open_ul = False
        insert_close_ul = False

        if '<h2>' in line: 
            if last_header != '<h2>': 
                if int('<h2>'[2]) > int(last_header[2]): insert_open_ul = True
                else: insert_close_ul = True
            last_header = '<h2>'
            line = line.replace('<h2>', '').replace('</h2>', '')

        elif '<h3>' in line:
            if last_header != '<h3>':
                if int('<h3>'[2]) > int(last_header[2]): insert_open_ul = True
                else: insert_close_ul = True

            last_header = '<h3>'
            line = line.replace('<h3>', '').replace('</h3>', '')

        if insert_open_ul: table_of_contents_html += f'<ul>'
        if insert_close_ul: table_of_contents_html += f'</ul>'
        table_of_contents_html += f'<li><a href="#{i}">{line}</a></li>'

    table_of_contents_html += '</ul>'
    table_of_contents_html += '</div>'

    # insert table in article
    content_html_formatted = ''

    toc_inserted = False
    for line in content_html_with_ids.split('\n'):
        if not toc_inserted:
            if '<h2' in line:
                # print(line)
                toc_inserted = True
                content_html_formatted += table_of_contents_html
                content_html_formatted += line
                continue
        content_html_formatted += line

    return content_html_formatted


def generate_breadcrumbs(filepath_in):
    filepath_chunks = filepath_in.split('/')
    breadcrumbs = [f.replace('.json', '').title() for f in filepath_chunks[2:-1]]
    article_name = filepath_chunks[-1].replace('.json', '').replace('-', ' ').title()
    
    breadcrumbs_hrefs = []
    total_path = ''
    for b in breadcrumbs:
        total_path += b + '/'
        breadcrumbs_hrefs.append('/' + total_path[:-1].lower() + '.html')
    
    breadcrumbs_text = total_path.split('/')

    breadcrumbs_html = []
    for i in range(len(breadcrumbs_hrefs)):
        html = f'<a href="{breadcrumbs_hrefs[i]}">{breadcrumbs_text[i]}</a>'
        breadcrumbs_html.append(html)

    breadcrumbs_html_formatted = [f' > {f}' for f in breadcrumbs_html]
    breadcrumbs_html_formatted.append(f' > {article_name}')

    breadcrumbs_html_formatted = ''.join(breadcrumbs_html_formatted)

    return breadcrumbs_html_formatted


def generate_table_problems():
    pass
    # article_html += f'<p>La seguente tabella elenca i nomi di alcuni problemi di contaminazione che l\'ozono elimina {application_a_1}{application}, divisi per categoria.</p>'
        # batteri = ', '.join(data['problemi_batteri'][:5])
        # virus = ', '.join(data['problemi_virus'][:5])
        # muffe = ', '.join(data['problemi_muffe'][:5])
        # insetti = ', '.join(data['problemi_insetti'][:5])
        # odori = ', '.join(data['problemi_odori'][:5])
        # article_html += f'''
        #     <table>
        #         <tr>
        #             <th>Categoria</th>
        #             <th>Nomi</th>
        #         </tr>
        #         <tr>
        #             <td>Batteri</td>
        #             <td>{batteri}</td>
        #         </tr>
        #         <tr>
        #             <td>Virus</td>
        #             <td>{virus}</td>
        #         </tr>
        #         <tr>
        #             <td>Muffe</td>
        #             <td>{muffe}</td>
        #         </tr>
        #         <tr>
        #             <td>Insetti</td>
        #             <td>{insetti}</td>
        #         </tr>
        #         <tr>
        #             <td>Odori</td>
        #             <td>{odori}</td>
        #         </tr>
        #     </table>
        # '''


###################################################################################################################
# images
###################################################################################################################

def img_resize(image_path):
    w, h = 768, 512

    img = Image.open(image_path)

    start_size = img.size
    end_size = (w, h)

    if start_size[0] / end_size [0] < start_size[1] / end_size [1]:
        ratio = start_size[0] / end_size[0]
        new_end_size = (end_size[0], int(start_size[1] / ratio))
    else:
        ratio = start_size[1] / end_size[1]
        new_end_size = (int(start_size[0] / ratio), end_size[1])

    img = img.resize(new_end_size)

    w_crop = new_end_size[0] - end_size[0]
    h_crop = new_end_size[1] - end_size[1]
    
    area = (
        w_crop // 2, 
        h_crop // 2,
        new_end_size[0] - w_crop // 2,
        new_end_size[1] - h_crop // 2
    )
    img = img.crop(area)

    output_path = image_path.replace('articles', 'articles-images')
    output_path = f'public/assets/images/{"-".join(image_path.split("/")[2:])}'
    img.save(f'{output_path}')

    return output_path


def img_resize_2(image_path_in, image_path_out):
    w, h = 768, 576

    img = Image.open(image_path_in)

    start_size = img.size
    end_size = (w, h)

    if start_size[0] / end_size [0] < start_size[1] / end_size [1]:
        ratio = start_size[0] / end_size[0]
        new_end_size = (end_size[0], int(start_size[1] / ratio))
    else:
        ratio = start_size[1] / end_size[1]
        new_end_size = (int(start_size[0] / ratio), end_size[1])

    img = img.resize(new_end_size, Image.Resampling.LANCZOS)

    w_crop = new_end_size[0] - end_size[0]
    h_crop = new_end_size[1] - end_size[1]
    
    area = (
        w_crop // 2, 
        h_crop // 2,
        new_end_size[0] - w_crop // 2,
        new_end_size[1] - h_crop // 2
    )
    img = img.crop(area)

    output_path = image_path_out
    img.save(output_path, quality=100)

    return output_path


def generate_featured_image(attribute, attr_2):
    industry_formatted = industry.replace(' ', '-')
    image_path_in = f'articles-images/public/ozono/sanificazione/{attribute}/{industry_formatted}/featured.jpg'
    image_filename_out = f'{attribute.replace("/", "-")}-{industry_formatted}-featured.jpg'
    image_filepath_out = f'/assets/images/{image_filename_out}'
    image_path_out = f'public/assets/images/{image_filename_out}'
    img_resize_2(image_path_in, image_path_out)

    return image_filepath_out


def generate_image_plain(image_path, w, h, image_path_out):
    img = Image.open(image_path)

    start_size = img.size
    end_size = (w, h)

    if start_size[0] / end_size [0] < start_size[1] / end_size [1]:
        ratio = start_size[0] / end_size[0]
        new_end_size = (end_size[0], int(start_size[1] / ratio))
    else:
        ratio = start_size[1] / end_size[1]
        new_end_size = (int(start_size[0] / ratio), end_size[1])

    img = img.resize(new_end_size)

    w_crop = new_end_size[0] - end_size[0]
    h_crop = new_end_size[1] - end_size[1]
    
    area = (
        w_crop // 2, 
        h_crop // 2,
        new_end_size[0] - w_crop // 2,
        new_end_size[1] - h_crop // 2
    )
    img = img.crop(area)

    name = image_path.split('/')[-1]
    path = image_path.split('/')[:-1]
        
    img.save(f'{image_path_out}')



###################################################################################################################
# articles html
###################################################################################################################

def generate_article_html(date, attribute, article, title):
    with open(f'articles/public/ozono/sanificazione/{attribute}.md', 'w', encoding='utf-8') as f:
        f.write(article)

    with open(f'articles/public/ozono/sanificazione/{attribute}.md', encoding='utf-8') as f:
        article_md = f.read()

    word_count = len(article_md.split(' '))
    reading_time = str(word_count // 200) + ' minuti'
    # word_count_html = str(word_count) + ' words'

    # article_html = markdown.markdown(article_md)
    article_html = markdown.markdown(article_md, extensions=['markdown.extensions.tables'])


    # GENERATE TABLE OF CONTENTS ----------------------------------------
    article_html = generate_toc(article_html)

    with open('components/header.html', encoding='utf-8') as f:
            header_html = f.read()

    author = 'Ozonogroup'

    html = f'''
        <!DOCTYPE html>
        <html lang="en">

        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="/style-blog.css">
            <title>{title}</title>
            {GOOGLE_TAG}
        </head>

        <body>
            <section class="header-section">
                <div class="container-xl">
                    {header_html}
                </div>
            </section>

            <section class="meta-section mt-48">
                <div class="container-md px-16">
                    <div class="flex justify-between mb-8">
                        <span>by {author} • {date}</span>
                        <span>Tempo Lettura: {reading_time}</span>
                    </div>
                </div>
            </section>

            <section class="mb-96">
                <div class="container-md px-16">
                    {article_html}
                </div>
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

    with open(f'public/ozono/sanificazione/{attribute}.html', 'w', encoding='utf-8') as f:
        f.write(html)


def get_csv_table(filepath):
    lines = []
    with open(filepath, encoding='utf-8') as f:
        reader = csv.reader(f, delimiter="|")
        for i, line in enumerate(reader):
            lines.append([line[0].strip(), line[1].strip()])
    return lines


def generate_table(lines):
    text = ''
    for i, line in enumerate(lines):
        if i == 0: 
            text += f'| {line[0].title()} | Problemi | \n'
            text += f'| --- | --- |\n'
        else:
            text += f'| {line[0].capitalize()} | {line[1].capitalize()} |\n'
    text += f'\n'
    return text


def generate_manual_article_html():
    folder = pathlib.Path("articles")

    w, h = 768, 432
    generate_image_plain(
        'assets/images/featured/ozono-chimica.jpg', 
        w, h,
        'public/assets/images/ozono-chimica.jpg',
    )
    generate_image_plain(
        'assets/images/featured/ozono-stratosferico.jpg', 
        w, h, 
        'public/assets/images/ozono-stratosferico.jpg', 
    )
    generate_image_plain(
        'assets/images/featured/ozono-troposferico.jpg', 
        w, h, 
        'public/assets/images/ozono-troposferico.jpg', 
    )
    generate_image_plain(
        'assets/images/featured/ozono-effetti.jpg', 
        w, h, 
        'public/assets/images/ozono-effetti.jpg', 
    )
    generate_image_plain(
        'assets/images/featured/ozono-benefici.jpg', 
        w, h, 
        'public/assets/images/ozono-benefici.jpg', 
    )
    generate_image_plain(
        'assets/images/featured/ozono-sanificazione.jpg', 
        w, h, 
        'public/assets/images/ozono-sanificazione.jpg', 
    )
    generate_image_plain(
        'assets/images/featured/ozono-sanificazione-benefici.jpg', 
        w, h, 
        'public/assets/images/ozono-sanificazione-benefici.jpg', 
    )

    for filepath in folder.rglob("*.md"):
        filepath = str(filepath)
        
        with open(filepath, encoding='utf-8') as f:
            content = f.read()

        content_html = markdown.markdown(content, extensions=['markdown.extensions.tables', 'meta'])

        md = markdown.Markdown(extensions=['meta'])
        md.convert(content)

        title = ''
        try: title = md.Meta['title'][0]
        except: pass
        print(title)

        lines = '\n'.join(md.lines)

        content_html = markdown.markdown(lines, extensions=['markdown.extensions.tables'])

        # BREADCRUMBS  ---------------------------------------------
        breadcrumbs = generate_breadcrumbs(filepath)

        # READING TIME  --------------------------------------------
        reading_time = len(content.split(' ')) // 200

        # PUBLICATION DATE  ----------------------------------------
        publishing_date = ''
        try: publishing_date = md.Meta['publishing_date'][0]
        except: pass

        # AUTHOR ----------------------------------------
        author = 'Ozonogroup Staff'
        try: author = md.Meta['author'][0]
        except: pass

        last_update_date = ''
        try: last_update_date = md.Meta['last_update_date'][0]
        except: pass

        # GENERATE TABLE OF CONTENTS ----------------------------------------
        toc_html = generate_toc(content_html)
        
        
        with open('components/header.html', encoding='utf-8') as f:
            header_html = f.read()
                

                
        html = f'''
            <!DOCTYPE html>
            <html lang="en">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link rel="stylesheet" href="/style-blog.css">
                <link rel="stylesheet" href="/util.css">
                <title>{title}</title>
                {GOOGLE_TAG}
            </head>

            <body>
                <section class="header-section">
                    <div class="container-xl h-full">
                        {header_html}
                    </div>
                </section>

                <section class="breadcrumbs-section">
                    <div class="container-xl h-full">
                        <a href="/index.html">Home</a>{''.join(breadcrumbs)}
                    </div>
                </section>

                <section class="meta-section mt-48">
                    <div class="container-md h-full">
                        <div class="flex justify-between mb-8">
                            <span>by {author} • {publishing_date}</span>
                            <span>Tempo Lettura: {reading_time} min</span>
                        </div>
                    </div>
                </section>

                <section class="container-md">
                    {toc_html}
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

        filepath_out_dir = '/'.join(filepath_chunks[1:-1])
        filepath_out = '/'.join(filepath_chunks[1:]).replace('.md', '.html')
        # print(filepath_out)

        if not os.path.exists(filepath_out_dir):
            os.makedirs(filepath_out_dir)

        util.file_write(filepath_out, html)

    
    # IMAGES
    industries = [
        'lattiero-casearia',
        'salumiera',
        'ittica',
        'cerealicola',
        'ortofrutticola',
        'vinicola',
        'acqua-minerale',
        'birraria',
        'lavorazione-carni',
        'automobili',
        'ospedali',
        'ambulanze',
        'case-di-riposo',
        'cliniche-dentistiche',
        'cliniche-veterinarie',
        'scuole',
        'asili',
        'bagni-pubblici',
        'cinema',
        'teatri',
        'alberghi',
        'bed-and-breakfast',
    ]
    articles_folder = 'articles/public/ozono/sanificazione/applicazioni'
    for article_filename in os.listdir(articles_folder):
        article_filename_no_ext = article_filename.replace('.md', '')
        print(article_filename)
        if article_filename_no_ext in industries:
            print('ok')
            article_filepath = f'{article_filename}/{article_filename}'
            images_articles_folder = f'C:/og-assets/images/articles'
            images_article_folder = f'{images_articles_folder}/{article_filename_no_ext}'
            images_filepath = [f'{images_article_folder}/{filepath}' for filepath in os.listdir(images_article_folder)]

            image_filepath = images_filepath.pop(0)
            img_resize_2(
                image_filepath, 
                f'public/assets/images/ozono-sanificazione-{article_filename_no_ext}.jpg'
            )

            image_filepath = images_filepath.pop(0)
            img_resize_2(
                image_filepath, 
                f'public/assets/images/ozono-sanificazione-{article_filename_no_ext}-definizione.jpg'
            )

            image_filepath = images_filepath.pop(0)
            img_resize_2(
                image_filepath, 
                f'public/assets/images/ozono-sanificazione-{article_filename_no_ext}-problemi.jpg'
            )

            image_filepath = images_filepath.pop(0)
            img_resize_2(
                image_filepath, 
                f'public/assets/images/ozono-sanificazione-{article_filename_no_ext}-benefici.jpg'
            )

            image_filepath = images_filepath.pop(0)
            img_resize_2(
                image_filepath, 
                f'public/assets/images/ozono-sanificazione-{article_filename_no_ext}-applicazioni.jpg'
            )
            

def copy_images():
    # articles_images_path = 'assets/images/articles/'
    # for f in os.listdir(articles_images_path):
    #     shutil.copy2(f'{articles_images_path}{f}', f'public/assets/images/{f}')
        
    articles_images_path = 'assets/images/home/'
    for f in os.listdir(articles_images_path):
        shutil.copy2(f'{articles_images_path}{f}', f'public/assets/images/{f}')
        
    articles_images_path = 'assets/images/static/'
    for f in os.listdir(articles_images_path):
        shutil.copy2(f'{articles_images_path}{f}', f'public/assets/images/{f}')





###################################################################################################################
# ARTICLES
###################################################################################################################

def gen_articles_html(regen=False):
    if regen:
        folderpath = 'public/ozono/sanificazione/applicazioni'
        for filename in os.listdir(folderpath):
            filepath = f'{folderpath}/{filename}'
            os.remove(filepath)

    folderpath = 'articles/public/ozono/sanificazione/applicazioni'
    rows = util.csv_get_rows('database/tables/applications.csv')

    cols = {}
    for i, item in enumerate(rows[0]): cols[item] = i

    # for filename in os.listdir(folderpath):
    for row in rows[1:]:
        filename = row[cols['slug']] + '.json'
        # filename = row[0].lower().strip().replace(' ', '-').replace("'", '-') + '.json'
        application_name_dash = filename.split('.')[0]
        application_a_1 = util.csv_get_rows_by_entity('database/tables/applications.csv', application_name_dash, col_num=cols['slug'])

        filepath_in = f'{folderpath}/{filename}'
        filepath_out = filepath_in.replace('articles/', '').replace('.json', '.html')
        data = util.json_read(filepath_in)

        keyword = filename.replace('.json', '')
        application = keyword.lower().replace('-', ' ')
        title = f'Sanificazione {application} con ozono'

        article_html = ''

        intro = ''
        try: intro = data['intro_desc']
        except: print(f'MISSING: INTRO >>> {filename}')
        if intro != '':
            article_html += f'<h1>{title}</h1>' + '\n'
            image_path = f'/assets/images/ozono-sanificazione-{keyword}-introduzione.jpg'
            article_html += f'<p><img src="{image_path}" alt=""></p>' + '\n'
            try: article_html += util.text_format_1N1_html(intro) + '\n'
            except: print(f'MISSING: INTRO >>> {filename}')

        definition = ''
        try: definition = data['definition_desc']
        except: print(f'MISSING: DEFINITION >>> {filename}')
        if definition != '':
            article_html += f'<h2>Cos\'è la sanificazione ad ozono per {application}?</h2>' + '\n'
            article_html += f'<p><img src="/assets/images/ozono-sanificazione-{keyword}-definizione.jpg" alt=""></p>' + '\n'
            article_html += util.text_format_1N1_html(definition) + '\n'

        problems_text = ''
        try: problems_text = data['problems_desc']
        except: print(f'MISSING: PROBLEMS_TEXT >>> {filename}')
        if problems_text != '':
            article_html += f'<h2>Quali problemi risolve la sanificazione ad ozono per {application}?</h2>' + '\n'
            article_html += f'<p><img src="/assets/images/ozono-sanificazione-{keyword}-problemi.jpg" alt=""></p>' + '\n'
            article_html += util.text_format_1N1_html(problems_text) + '\n'

        benefits_text = ''
        try: benefits_text = data['benefits_desc']
        except: print(f'MISSING: BENEFITS_TEXT >>> {filename}')
        if benefits_text != '':
            article_html += f'<h2>Quali sono i benefici della sanificazione ad ozono per {application}?</h2>' + '\n'
            image_path = f'/assets/images/ozono-sanificazione-{keyword}-benefici.jpg'
            # if os.path.exists(image_path):
            article_html += f'<p><img src="{image_path}" alt=""></p>' + '\n'
            article_html += util.text_format_1N1_html(benefits_text) + '\n'

        applications_text = ''
        try: applications_text = data['applications_desc']
        except: print(f'MISSING: BENEFITS_TEXT >>> {filename}')
        if applications_text != '':
            article_html += f'<h2>Quali sono le applicazioni della sanificazione ad ozono per {application}?</h2>' + '\n'
            article_html += f'<p><img src="/assets/images/ozono-sanificazione-{keyword}-applicazioni.jpg" alt=""></p>' + '\n'
            article_html += util.text_format_1N1_html(applications_text) + '\n'
            # article_html += util.list_bold_to_html(data['applications_list']) + '\n'

        # META
        breadcrumbs = generate_breadcrumbs(filepath_in)
        reading_time = len(article_html.split(' ')) // 200

        publishing_date = ''
        try: publishing_date = md.Meta['publishing_date'][0]
        except: pass

        author = 'Ozonogroup Staff'
        try: author = md.Meta['author'][0]
        except: pass

        last_update_date = ''
        try: last_update_date = md.Meta['last_update_date'][0]
        except: pass

        article_html = generate_toc(article_html)

        # COMPONENTS
        with open('components/header.html', encoding='utf-8') as f:
            header_html = f.read()

        # HTML
        html = f'''
            <!DOCTYPE html>
            <html lang="en">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link rel="stylesheet" href="/style-blog.css">
                <link rel="stylesheet" href="/util.css">
                <title>{title}</title>
                {GOOGLE_TAG}
            </head>

            <body>
                <section class="header-section">
                    <div class="container-xl h-full">
                        {header_html}
                    </div>
                </section>

                <section class="breadcrumbs-section">
                    <div class="container-xl h-full">
                        <a href="/index.html">Home</a>{breadcrumbs}
                    </div>
                </section>

                <section class="meta-section mt-48">
                    <div class="container-md h-full">
                        <div class="flex justify-between mb-8">
                            <span>by {author} • {publishing_date}</span>
                            <span>Tempo Lettura: {reading_time} min</span>
                        </div>
                    </div>
                </section>

                <section class="container-md">
                    {article_html}
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

        util.file_write(filepath_out, html)


    # IMAGES
    # articles_folder = 'articles/public/ozono/sanificazione/applicazioni'
    # for article_filename in os.listdir(articles_folder):
    #     article_filename_no_ext = article_filename.replace('.json', '')

    #     article_filepath = f'{article_filename}/{article_filename}'
    #     images_articles_folder = f'C:/og-assets/images/articles'
    #     images_article_folder = f'{images_articles_folder}/{article_filename_no_ext}'
    #     try: images_filepath = [f'{images_article_folder}/{filepath}' for filepath in os.listdir(images_article_folder)]
    #     except: 
    #         print(f'MISSING: IMAGE FOLDER >>> {article_filename}')
    #         continue

    #     images_filpaths_out = [
    #         f'public/assets/images/ozono-sanificazione-{article_filename_no_ext}-introduzione.jpg',
    #         f'public/assets/images/ozono-sanificazione-{article_filename_no_ext}-definizione.jpg',
    #         f'public/assets/images/ozono-sanificazione-{article_filename_no_ext}-problemi.jpg',
    #         f'public/assets/images/ozono-sanificazione-{article_filename_no_ext}-benefici.jpg',
    #         f'public/assets/images/ozono-sanificazione-{article_filename_no_ext}-applicazioni.jpg',
    #     ]
    #     for image_filepath_out in images_filpaths_out:
    #         image_filepath = images_filepath.pop(0)
    #         if not os.path.exists(image_filepath_out):
    #             img_resize_2(
    #                 image_filepath, 
    #                 image_filepath_out
    #             )


def gen_article_applications():
    filepath_in = 'articles/public/ozono/sanificazione/applicazioni.json'
    filepath_out = 'public/ozono/sanificazione/applicazioni.html'

    article_html = ''
    
    title = 'Quali sono le applicazioni della sanificazione ad ozono?'
    article_html += f'<h1>{title}</h1>' + '\n'
    article_html += f'<p><img src="/assets/images/ozono-sanificazione-applicazioni-introduzione.jpg" alt=""><p>' + '\n'

    data = util.json_read(filepath_in)
    for application in data['applications']:
        application_name = application['application_name']
        application_a_1 = util.csv_get_rows_by_entity('database/tables/applications.csv', application_name)[0][1]
        application_desc = application['application_desc']
        application_dash = application_name.strip().lower().replace(' ', '-').replace("'", '-')
        application_desc_with_link = application_desc.replace(
            f'La sanificazione ad ozono {application_a_1}{application_name}',
            f'<a href="/ozono/sanificazione/applicazioni/{application_dash}.html">La sanificazione ad ozono {application_a_1}{application_name}</a>',
        )
        article_html += f'<h2>{application_name.title()}</h2>' + '\n'
        article_html += f'<p><img src="/assets/images/ozono-sanificazione-{application_dash}-introduzione.jpg" alt=""><p>' + '\n'
        article_html += util.text_format_1N1_html(application_desc_with_link) + '\n'

    # META
    breadcrumbs = generate_breadcrumbs(filepath_in)
    reading_time = len(article_html.split(' ')) // 200

    publishing_date = ''
    try: publishing_date = md.Meta['publishing_date'][0]
    except: pass

    author = 'Ozonogroup Staff'
    try: author = md.Meta['author'][0]
    except: pass

    last_update_date = ''
    try: last_update_date = md.Meta['last_update_date'][0]
    except: pass

    article_html = generate_toc(article_html)

    # COMPONENTS
    with open('components/header.html', encoding='utf-8') as f:
        header_html = f.read()

    # HTML
    html = f'''
        <!DOCTYPE html>
        <html lang="en">

        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="/style-blog.css">
            <link rel="stylesheet" href="/util.css">
            <title>{title}</title>
            {GOOGLE_TAG}
        </head>

        <body>
            <section class="header-section">
                <div class="container-xl h-full">
                    {header_html}
                </div>
            </section>

            <section class="breadcrumbs-section">
                <div class="container-xl h-full">
                    <a href="/index.html">Home</a>{breadcrumbs}
                </div>
            </section>

            <section class="meta-section mt-48">
                <div class="container-md h-full">
                    <div class="flex justify-between mb-8">
                        <span>by {author} • {publishing_date}</span>
                        <span>Tempo Lettura: {reading_time} min</span>
                    </div>
                </div>
            </section>

            <section class="container-md">
                {article_html}
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

    util.file_write(filepath_out, html)





###################################################################################################################
# PAGINE
###################################################################################################################

def gen_pagina_guide():
    content = util.file_read('guide.html')
    rows = util.csv_get_rows('database/tables/applications.csv')[1:]

    articles_dict = {}
    for row in rows:
        print(row)
        try: articles_dict[row[2]].append([row[0], row[1], row[3]])
        except: articles_dict[row[2]] = [[row[0], row[1], row[3]]]


    articles = ''
    for key, values in articles_dict.items():
        articles_curr = ''
        for value in values:
            application_name = value[0].strip()
            application_slug = value[2]
            articles_curr += f'''
            <a class="decoration-none" href="/ozono/sanificazione/applicazioni/{application_slug}.html">
                <img src="/assets/images/ozono-sanificazione-{application_slug}-introduzione.jpg" alt="">
                <h3>Sanificazione ad ozono per {application_name.lower()}</h3>
            </a>
        '''

        articles += f'''
            <section id="articoli-1" class="pb-96">
                <div class="container h-full">
                    <h2 class="text-center mb-16">Sanificazione ozono per il settore: {key.title()}</h2>
                    <p class="text-center mb-48">Scopri dove l'ozono può essere applicato per eliminare una vasta gamma di
                        patogeni, odori e altri contaminanti.</p>
                    <div class="grid-3">
                        {articles_curr}
                    </div>
                </div>
            </section>
        '''


    content = content.replace('[articles]', articles)

    util.file_write('public/guide.html', content)





###################################################################################################################
# MAIN
###################################################################################################################

gen_articles_html(regen=True)
gen_article_applications()

# shutil.copy2('missione.html', 'public/missione.html')
# shutil.copy2('contatti.html', 'public/contatti.html')
# shutil.copy2('index.html', 'public/index.html')
# shutil.copy2('sitemap.xml', 'public/sitemap.xml')
gen_pagina_guide()

# shutil.copy2('style.css', 'public/style.css')
# shutil.copy2('style-blog.css', 'public/style-blog.css')
# shutil.copy2('util.css', 'public/util.css')
# shutil.copy2('img.css', 'public/img.css')
# shutil.copy2('logo.ico', 'public/logo.ico')
# shutil.copy2('CNAME', 'public/CNAME')

