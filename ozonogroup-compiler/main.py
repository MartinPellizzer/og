import json
import os
import shutil
import csv

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
    articles_folder = 'articles/public/ozono/sanificazione/applicazioni'
    for article_filename in os.listdir(articles_folder):
        article_filename_no_ext = article_filename.replace('.json', '')

        article_filepath = f'{article_filename}/{article_filename}'
        images_articles_folder = f'C:/og-assets/images/articles'
        images_article_folder = f'{images_articles_folder}/{article_filename_no_ext}'
        try: images_filepath = [f'{images_article_folder}/{filepath}' for filepath in os.listdir(images_article_folder)]
        except: 
            print(f'MISSING: IMAGE FOLDER >>> {article_filename}')
            continue

        images_filpaths_out = [
            f'public/assets/images/ozono-sanificazione-{article_filename_no_ext}-introduzione.jpg',
            f'public/assets/images/ozono-sanificazione-{article_filename_no_ext}-definizione.jpg',
            f'public/assets/images/ozono-sanificazione-{article_filename_no_ext}-problemi.jpg',
            f'public/assets/images/ozono-sanificazione-{article_filename_no_ext}-benefici.jpg',
            f'public/assets/images/ozono-sanificazione-{article_filename_no_ext}-applicazioni.jpg',
        ]

        # print(images_filepath[0])
        print(images_filpaths_out[0])
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


def sector():
    folderpath = 'articles/public/ozono/sanificazione/applicazioni'
    rows = util.csv_get_rows('database/tables/applications.csv')

    cols = {}
    for i, item in enumerate(rows[0]): cols[item] = i
    
    sector_dict = {}
    for row in rows[1:]:
        try: sector_dict[row[cols['sector']]].append(row)
        except: sector_dict[row[cols['sector']]] = [row]
    
    for key, values in sector_dict.items():
        template = util.file_read('templates/settori.html')
        # print(key, '>>', values)
        print()
        print(key)

        articles_curr = ''
        for application in values:
            print(application)
            application_name = application[cols['application']]
            application_slug = application[cols['slug']]
            articles_curr += f'''
                <a class="decoration-none" href="/ozono/sanificazione/applicazioni/{application_slug}.html">
                    <img src="/assets/images/ozono-sanificazione-{application_slug}-introduzione.jpg" alt="">
                    <h3>Sanificazione ad ozono per {application_name.lower()}</h3>
                </a>
            '''

        articles = f'''
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
        template = template.replace('[articles]', articles)
        template = template.replace('[google_tag]', g.GOOGLE_TAG)
        util.file_write(f'public/settori/{key}.html', template)




###################################################################################################################
# PAGINE
###################################################################################################################

def guides():
    content = util.file_read('templates/guide.html')
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


def sectors():
    template = util.file_read('templates/settori.html')
    rows = util.csv_get_rows('database/tables/applications.csv')[1:]


    categories_dict = {}
    for row in rows:
        try: categories_dict[row[2]].append([row[0], row[1], row[3]])
        except: categories_dict[row[2]] = [[row[0], row[1], row[3]]]

    articles = ''
    for key, values in categories_dict.items():
        # articles_curr = ''
        # for value in values:
        #     application_name = value[0].strip()
        #     application_slug = value[2]
        #     articles_curr += f'''
        #     <a class="decoration-none" href="/ozono/sanificazione/applicazioni/{application_slug}.html">
        #         <img src="/assets/images/ozono-sanificazione-{application_slug}-introduzione.jpg" alt="">
        #         <h3>Sanificazione ad ozono per {application_name.lower()}</h3>
        #     </a>
        # '''

        # articles += f'''
        #     <section id="articoli-1" class="pb-96">
        #         <div class="container h-full">
        #             <h2 class="text-center mb-16">Sanificazione ozono per il settore: {key.title()}</h2>
        #             <p class="text-center mb-48">Scopri dove l'ozono può essere applicato per eliminare una vasta gamma di
        #                 patogeni, odori e altri contaminanti.</p>
        #             <div class="grid-3">
        #                 {articles_curr}
        #             </div>
        #         </div>
        #     </section>
        # '''

        articles += f'''
            <section id="articoli-1" class="pb-96">
                <div class="container h-full">
                    <h2 class="text-center mb-16">Sanificazione ozono per il settore: <a href="/settori/{key}.html">{key.title()}</a></h2>
                    <p class="text-center mb-48">Scopri dove l'ozono può essere applicato per eliminare una vasta gamma di
                        patogeni, odori e altri contaminanti.</p>
                </div>
            </section>
        '''

    template = template.replace('[articles]', articles)
    template = template.replace('[google_tag]', g.GOOGLE_TAG)

    util.file_write('public/settori.html', template)




###################################################################################################################
# MAIN
###################################################################################################################

# gen_articles_html(regen=True)
# gen_article_applications()

# shutil.copy2('templates/index.html', 'public/index.html')
# shutil.copy2('templates/servizi.html', 'public/servizi.html')
# shutil.copy2('templates/missione.html', 'public/missione.html')
# shutil.copy2('templates/contatti.html', 'public/contatti.html')
# shutil.copy2('sitemap.xml', 'public/sitemap.xml')

# guides()
sectors()
sector()

# shutil.copy2('style.css', 'public/style.css')
# shutil.copy2('style-blog.css', 'public/style-blog.css')
# shutil.copy2('util.css', 'public/util.css')
# shutil.copy2('img.css', 'public/img.css')
# shutil.copy2('logo.ico', 'public/logo.ico')
# shutil.copy2('CNAME', 'public/CNAME')

