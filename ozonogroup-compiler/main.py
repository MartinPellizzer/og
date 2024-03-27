import json
import os
import shutil
import csv
import markdown

import util
import util_img
import g




###################################################################################################################
# META
###################################################################################################################

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





###################################################################################################################
# ARTICLES
###################################################################################################################

def gen_applications():
    folderpath = 'articles/public/ozono/sanificazione/settori'
    rows = util.csv_get_rows('database/tables/applications.csv')

    cols = {}
    for i, item in enumerate(rows[0]): cols[item] = i

    for row in rows[1:]:
        # print(row)
        slug = row[cols['slug']].strip()
        name = row[cols['application']].strip()
        a_1 = row[cols['a-1']].strip()
        sector = row[cols['sector']].strip()
        filename = slug + '.json'

        filepath_in = f'{folderpath}/{sector}/{filename}'
        print(filepath_in)
        filepath_out = filepath_in.replace('articles/', '').replace('.json', '.html')

        data = util.json_read(filepath_in)

        keyword = filename.replace('.json', '')
        application = keyword.lower().replace('-', ' ')
        title = f'Sanificazione {application} con ozono'
        imagepath_out_rel = f'{sector}-{keyword}' 

        article_html = ''

        article_html += f'<h1>{title}</h1>' + '\n'
        image_path = f'/assets/images/ozono-sanificazione-{imagepath_out_rel}-introduzione.jpg'
        intro = ''
        try: intro = data['intro_desc']
        except: print(f'MISSING: INTRO >>> {filename}')
        if intro != '':
            article_html += f'<p><img src="{image_path}" alt=""></p>' + '\n'
            try: article_html += util.text_format_1N1_html(intro) + '\n'
            except: print(f'MISSING: INTRO >>> {filename}')

        definition = ''
        try: definition = data['definition_desc']
        except: print(f'MISSING: DEFINITION >>> {filename}')
        if definition != '':
            article_html += f'<h2>Cos\'è la sanificazione ad ozono per {application}?</h2>' + '\n'
            article_html += f'<p><img src="/assets/images/ozono-sanificazione-{imagepath_out_rel}-definizione.jpg" alt=""></p>' + '\n'
            article_html += util.text_format_1N1_html(definition) + '\n'

        problems_text = ''
        try: problems_text = data['problems_desc']
        except: print(f'MISSING: PROBLEMS_TEXT >>> {filename}')
        if problems_text != '':
            article_html += f'<h2>Quali problemi risolve la sanificazione ad ozono per {application}?</h2>' + '\n'
            article_html += f'<p><img src="/assets/images/ozono-sanificazione-{imagepath_out_rel}-problemi.jpg" alt=""></p>' + '\n'
            article_html += util.text_format_1N1_html(problems_text) + '\n'

        benefits_text = ''
        try: benefits_text = data['benefits_desc']
        except: print(f'MISSING: BENEFITS_TEXT >>> {filename}')
        if benefits_text != '':
            article_html += f'<h2>Quali sono i benefici della sanificazione ad ozono per {application}?</h2>' + '\n'
            image_path = f'/assets/images/ozono-sanificazione-{imagepath_out_rel}-benefici.jpg'
            # if os.path.exists(image_path):
            article_html += f'<p><img src="{image_path}" alt=""></p>' + '\n'
            article_html += util.text_format_1N1_html(benefits_text) + '\n'

        applications_text = ''
        try: applications_text = data['applications_desc']
        except: print(f'MISSING: BENEFITS_TEXT >>> {filename}')
        if applications_text != '':
            article_html += f'<h2>Quali sono le applicazioni della sanificazione ad ozono per {application}?</h2>' + '\n'
            article_html += f'<p><img src="/assets/images/ozono-sanificazione-{imagepath_out_rel}-applicazioni.jpg" alt=""></p>' + '\n'
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
        header_html = component_header_no_logo()

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
                {g.GOOGLE_TAG}
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
        images_article_folder = f'C:/og-assets/images/articles/{sector}/{slug}'
        try: images_filepath = [f'{images_article_folder}/{filepath}' for filepath in os.listdir(images_article_folder)]
        except: 
            print(f'MISSING: IMAGE FOLDER >>> {images_article_folder}')
            continue

        images_filpaths_out = [
            f'public/assets/images/ozono-sanificazione-{sector}-{slug}-introduzione.jpg',
            f'public/assets/images/ozono-sanificazione-{sector}-{slug}-definizione.jpg',
            f'public/assets/images/ozono-sanificazione-{sector}-{slug}-problemi.jpg',
            f'public/assets/images/ozono-sanificazione-{sector}-{slug}-benefici.jpg',
            f'public/assets/images/ozono-sanificazione-{sector}-{slug}-applicazioni.jpg',
        ]

        # print(images_filpaths_out[0])
        for image_filepath_out in images_filpaths_out:
            try:
                image_filepath = images_filepath.pop(0)
                if not os.path.exists(image_filepath_out):
                    util_img.resize(
                        image_filepath, 
                        image_filepath_out
                    )
            except: 
                print(f'MISSING: NOT ENOUGH IMAGES IN FOLDER >> {images_article_folder}')



    # # IMAGES
    # articles_folder = f'articles/public/ozono/sanificazione/settori/{sector}'
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

    #     # print(images_filepath[0])
    #     print(images_filpaths_out[0])
    #     for image_filepath_out in images_filpaths_out:
    #         try:
    #             image_filepath = images_filepath.pop(0)
    #             if not os.path.exists(image_filepath_out):
    #                 util_img.resize(
    #                     image_filepath, 
    #                     image_filepath_out
    #                 )
    #         except: 
    #             print(f'MISSING: NOT ENOUGH IMAGES IN FOLDER >> {article_filename}')


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
            {g.GOOGLE_TAG}
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

def component_header_logo():
    return f'''
        <header>
            <div class="logo">
                <a href="/">
                    <img src="logo-white.png" alt="logo ozonogroup">
                </a>
            </div>
            <nav>
                <input type="checkbox" class="toggle-menu">
                <div class="hamburger"></div>
                <ul class="menu">
                    <li><a href="/">Home</a></li>
                    <li><a href="/servizi.html">Servizi</a></li>
                    <li><a href="/settori.html">Settori</a></li>
                    <li><a href="/missione.html">Missione</a></li>
                    <li><a href="/contatti.html">Contatti</a></li>
                </ul>
            </nav>
        </header>
    '''
    

def component_header_no_logo():
    return f'''
        <header>
            <div class="logo">
                <a href="/">Ozonogroup</a>
            </div>
            <nav>
                <input type="checkbox" class="toggle-menu">
                <div class="hamburger"></div>
                <ul class="menu">
                    <li><a href="/">Home</a></li>
                    <li><a href="/servizi.html">Servizi</a></li>
                    <li><a href="/settori.html">Settori</a></li>
                    <li><a href="/missione.html">Missione</a></li>
                    <li><a href="/contatti.html">Contatti</a></li>
                </ul>
            </nav>
        </header>
    '''


def page_home():
    template = util.file_read('templates/index.html')

    header = component_header_logo()
    
    template = template.replace('[header]', header)
    template = template.replace('[google_tag]', g.GOOGLE_TAG)
    

    util.file_write('public/index.html', template)


def page_servizi():
    template = util.file_read('templates/servizi.html')

    header = component_header_logo()
    
    template = template.replace('[header]', header)
    template = template.replace('[google_tag]', g.GOOGLE_TAG)

    util.file_write('public/servizi.html', template)


def page_settori():
    template = util.file_read('templates/settori.html')

    header = component_header_logo()

    rows = util.csv_get_rows('database/tables/sectors.csv')[1:]
    
    articles = f'''
        <section>
            <div class="container-xl h-full py-96">
                [blocks]
            </div>
        </section>
    '''

    blocks = ''
    for i, row in enumerate(rows):
        sector_name = row[1]
        sector_a = row[2]
        data = util.json_read('database/articles/ozono/sanificazione/settori.json')
        sector_desc = ''
        sector_link = f'<p>Qui trovi una lista completa delle <a href="/ozono/sanificazione/settori/{sector_name}.html">applicazioni dell\'ozono nel settore {sector_a}{sector_name}</a>.</p>'
        for json_sector in data['sectors']:
            if json_sector['slug'] == sector_name:
                sector_desc = util.text_format_1N1_html(json_sector['desc'])
                sector_desc = sector_desc[:400] + '...'
                break
        if i % 2 == 0:
            block = f'''
                <div class="grid-2 items-center reverse mb-96">
                    <div class="grid-col-1">
                        <h2 class="mb-16">{sector_name.title()}</h2>
                        <p>{sector_desc}</p>
                        {sector_link}
                    </div>
                    <div class="grid-col-2">
                        <img src="/assets/images/ozono-sanificazione-settori-{sector_name}.jpg" alt="">
                    </div>
                </div>
            '''
        else:
            block = f'''
                <div class="grid-2 items-center mb-96">
                    <div class="grid-col-1">
                        <img src="/assets/images/ozono-sanificazione-settori-{sector_name}.jpg" alt="">
                    </div>
                    <div class="grid-col-1">
                        <h2 class="mb-16">{sector_name.title()}</h2>
                        <p>{sector_desc}</p>
                        {sector_link}
                    </div>
                </div>
            '''

        print(row)
        blocks += block

    articles = articles.replace('[blocks]', blocks)
    template = template.replace('[articles]', articles)
    template = template.replace('[header]', header)
    template = template.replace('[google_tag]', g.GOOGLE_TAG)

    util.file_write('public/settori.html', template)
    

def page_missione():
    template = util.file_read('templates/missione.html')

    header = component_header_logo()
    
    template = template.replace('[header]', header)
    template = template.replace('[google_tag]', g.GOOGLE_TAG)

    util.file_write('public/missione.html', template)
    

def page_contatti():
    template = util.file_read('templates/contatti.html')

    header = component_header_logo()
    
    template = template.replace('[header]', header)
    template = template.replace('[google_tag]', g.GOOGLE_TAG)

    util.file_write('public/contatti.html', template)




def sectors():
    filepath_in = f'database/articles/ozono/sanificazione/settori.json'
    filepath_out = f'public/ozono/sanificazione/settori.html'

    data = util.json_read(filepath_in)

    article_html = ''
    
    title = data['title']
    article_html += f'<h1>{title}</h1>' + '\n'

    intro = ''
    try: intro = data['intro_desc']
    except: print(f'MISSING: INTRO >>> settori')
    if intro != '':
        # image_path = f'/assets/images/ozono-sanificazione-{keyword}-introduzione.jpg'
        # article_html += f'<p><img src="{image_path}" alt=""></p>' + '\n'
        try: article_html += util.text_format_1N1_html(intro) + '\n'
        except: print(f'MISSING: INTRO >>> settori')
        
    sectors = []
    try: sectors = data['sectors']
    except: print(f'MISSING: SECTORS >>> settori')
    if sectors != []:
        for i, sector in enumerate(sectors):
            slug = sector['slug'].strip()
            name = slug.replace('-', ' ').title()
            desc = sector['desc'].strip()
            a_1 = sector['a_1']
            desc_link = desc.replace(
                f'sanificazione ad ozono nel settore {name.lower()}',
                f'<a href="/ozono/sanificazione/settori/{slug}.html">sanificazione ad ozono nel settore {a_1}{name.lower()}</a>',
                1
            )
            article_html += f'<h2>{i+1}. {name}</h2>' + '\n'
            article_html += f'<p><img src="/assets/images/ozono-sanificazione-settori-{slug}.jpg" alt=""></p>' + '\n'
            article_html += util.text_format_1N1_html(desc_link) + '\n'

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
    header_html = component_header_no_logo()

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
            {g.GOOGLE_TAG}
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
    if sectors != []:
        for i, sector in enumerate(sectors):
            slug = sector['slug'].strip()
            images_article_folder = f'C:/og-assets/images/settori/{slug}'
            try: images_filepath = [f'{images_article_folder}/{filepath}' for filepath in os.listdir(images_article_folder)]
            except: 
                print(f'MISSING: IMAGE FOLDER >>> {slug}')
                continue
            
            print(images_filepath)
            
            images_filpaths_out = [
                f'public/assets/images/ozono-sanificazione-settori-{slug}.jpg',
            ]

            for image_filepath_out in images_filpaths_out:
                try:
                    image_filepath = images_filepath.pop(0)
                    if not os.path.exists(image_filepath_out):
                        util_img.resize(
                            image_filepath, 
                            image_filepath_out
                        )
                except: 
                    print(f'MISSING: NOT ENOUGH IMAGES IN FOLDER >> {article_filename}')



def sector():
    folderpath = 'articles/public/ozono/sanificazione/applicazioni'
    rows = util.csv_get_rows('database/tables/applications.csv')

    cols = {}
    for i, item in enumerate(rows[0]): cols[item] = i
    
    sector_dict = {}
    for row in rows[1:]:
        try: sector_dict[row[cols['sector']]].append(row)
        except: sector_dict[row[cols['sector']]] = [row]
    
    for sector, values in sector_dict.items():
        filepath_in = f'database/articles/ozono/sanificazione/settori/{sector}.json'
        filepath_out = f'public/ozono/sanificazione/settori/{sector}.html'
        print(filepath_in)

        if not os.path.exists(filepath_in): continue

        data = util.json_read(filepath_in)
        title = data['title']
        sector_name = data['sector_name']
        filename = sector_name + '.json'

        article_html = ''
        
        article_html += f'<h1>{title}</h1>' + '\n'
        article_html += f'<p><img src="/assets/images/ozono-sanificazione-settori-{sector}.jpg" alt=""></p>' + '\n'
        
        intro = ''
        try: intro = data['intro_desc']
        except: print(f'MISSING: INTRO >>> {filename}')
        if intro != '':
            try: article_html += util.text_format_1N1_html(intro) + '\n'
            except: print(f'MISSING: INTRO >>> {filename}')
            
        applications = []
        try: applications = data['applications']
        except: print(f'MISSING: APPLICATIONS >>> {filename}')
        if applications != []:
            for i, application in enumerate(applications):
                slug = application['slug'].strip()
                name = application['name'].title()
                a_1 = application['a_1']
                desc = application['desc'].strip()
                # print(f'sanificazione ad ozono {a_1}{name.lower()}')
                desc_link = desc.replace(
                    f'sanificazione ad ozono {a_1}{name.lower()}',
                    f'<a href="/ozono/sanificazione/settori/{sector}/{slug}.html">sanificazione ad ozono {a_1}{name.lower()}</a>',
                    1
                )
                article_html += f'<h2>{i+1}. {name}</h2>' + '\n'
                article_html += f'<p><img src="/assets/images/ozono-sanificazione-{sector}-{slug}-introduzione.jpg" alt=""></p>' + '\n'
                article_html += util.text_format_1N1_html(desc_link) + '\n'


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
        header_html = component_header_no_logo()


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
                {g.GOOGLE_TAG}
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
# MAIN
###################################################################################################################

def static_article(filepath):
    filepath_in = filepath
    filepath_out = filepath_in.replace('articles/', '').replace('.md', '.html')
    
    content = util.file_read(filepath_in)
    title = ''
    for line in content.split('\n'):
        if line.startswith('# '):
            title = line.replace('# ', '')
    article_html = markdown.markdown(content, extensions=['markdown.extensions.tables'])

    # META
    breadcrumbs = generate_breadcrumbs(filepath_in)
    breadcrumbs = breadcrumbs.replace('.Md', '').replace('.md', '')
    reading_time = len(article_html.split(' ')) // 200

    publishing_date = '06/11/2023' # TODO: generate dinamically
    
    author = 'Ozonogroup Staff'
    try: author = md.Meta['author'][0]
    except: pass

    last_update_date = ''
    try: last_update_date = md.Meta['last_update_date'][0]
    except: pass

    article_html = generate_toc(article_html)

    # COMPONENTS
    header_html = component_header_no_logo()

    html = f'''
        <!DOCTYPE html>
        <html lang="en">

        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="/style-blog.css">
            <link rel="stylesheet" href="/util.css">
            <title>{title}</title>
            {g.GOOGLE_TAG}
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



# static_article('articles/public/ozono.md')
# static_article('articles/public/ozono/chimica.md')
# static_article('articles/public/ozono/sanificazione.md')
# static_article('articles/public/ozono/stratosfera.md')
# static_article('articles/public/ozono/troposfera.md')
# static_article('articles/public/ozono/effetti.md')
# static_article('articles/public/ozono/benefici.md')

# gen_applications()

# gen_article_applications()

# shutil.copy2('sitemap.xml', 'public/sitemap.xml')

# page_home()
# page_servizi()
# page_settori()
# page_missione()
# page_contatti()

# sectors()
sector()

# shutil.copy2('style.css', 'public/style.css')
# shutil.copy2('style-blog.css', 'public/style-blog.css')
# shutil.copy2('util.css', 'public/util.css')
# shutil.copy2('img.css', 'public/img.css')
# shutil.copy2('logo.ico', 'public/logo.ico')
# shutil.copy2('CNAME', 'public/CNAME')

