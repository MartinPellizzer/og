import os
import time
import datetime

import g
import util
import util_ai
import util_img

applications_csv_filepath = 'database/csv/applications.csv'
applications_rows = util.csv_get_rows(applications_csv_filepath)
applications_cols = util.csv_get_header_dict(applications_rows)




def applications_pages():
    sectors_csv_filepath = g.CSV_SECTORS_FILEPATH
    sectors_rows = util.csv_get_rows(sectors_csv_filepath)
    sectors_cols = util.csv_get_header_dict(sectors_rows)

    for application_row in applications_rows[1:]:
        application_id = application_row[applications_cols['application_id']]
        application_name = application_row[applications_cols['application_name']].strip().lower()
        application_slug = application_row[applications_cols['application_slug']].strip().lower()
        application_a_1 = application_row[applications_cols['application_a_1']].lower()
        application_sector_id = application_row[applications_cols['application_sector_id']]
        title = f'Sanificazione ozono {application_a_1}{application_name}'

        sector_row = util.csv_get_rows_by_entity(sectors_csv_filepath, application_sector_id, col_num=sectors_cols['sector_id'])[0]
        sector_slug = sector_row[sectors_cols['sector_slug']].strip().lower()

        # JSON
        application_json_filepath = f'database/json/ozono/sanificazione/settori/{sector_slug}/{application_slug}.json'
        util.create_folder_for_filepath(application_json_filepath)
        util.json_generate_if_not_exists(application_json_filepath)
        data = util.json_read(application_json_filepath)
        data['application_id'] = application_id
        data['application_name'] = application_name
        data['application_slug'] = application_slug
        data['application_a_1'] = application_a_1
        data['application_sector_id'] = application_sector_id
        data['title'] = title
        lastmod = str(datetime.date.today())
        if 'lastmod' not in data: data['lastmod'] = lastmod
        else: lastmod = data['lastmod']
        util.json_write(application_json_filepath, data)

        # JSON AI
        key = 'intro'
        # del data[key] # (debug only)
        if key not in data:
            prompt = f'''
                Scrivi in Italiano 5 frasi brevi sulla sanificazione ad ozono {application_a_1}{application_name}.
                Nella frase 2, spiega cos'è la sanificazione ad ozono {application_a_1}{application_name} e quali problemi elimina {application_a_1}{application_name}.
                Nella frase 2, spiega quali sono le ripercussioni di questi problemi in termini di salute.
                Nella frase 3, spiega quali sono le ripercussioni di questi problemi in termini econimici.
                Nella frase 4, spiega quali sono le applicazioni dell'ozono {application_a_1}{application_name}.
                Nella frase 5, spiega quali sono i vantaggi dell'ozono {application_a_1}{application_name} confronto ad altri metodi di sanificazione.
                Rispondi in meno di 100 parole.
                Rispondi con una lista numerata.
            '''
            reply = util_ai.gen_reply(prompt).strip()
            reply = util_ai.reply_list_to_paragraph(reply)
            data[key] = reply
            util.json_write(application_json_filepath, data)
            time.sleep(30)
            
        key = 'definition'
        # del data[key] # (debug only)
        if key not in data:
            prompt = f'''
                scrivi un paragrafo di 100 parole spiegando cos'è e a cosa serve la sanificazione ad ozono per il seguente campo di applicazioni: {application_name}.
                Includi solo informazioni specifiche su questo campo di applicazione, e non informazioni generiche sull'ozono.
            '''
            reply = util_ai.gen_reply(prompt).strip()
            data[key] = reply
            util.json_write(application_json_filepath, data)
            time.sleep(30)
            
        key = 'problems'
        # del data[key] # (debug only)
        if key not in data:
            prompt = f'''
                scrivi un paragrafo di 100 parole spiegando quali problemi risolve la sanificazione ad ozono {application_a_1}{application_name}.
                includi nomi di batteri, virus, muffe, parassiti e odori.
                non spiegare cos'è l'ozono e non spiegare come funziona.
                inizia la risposta con queste parole: La sanificazione ad ozono elimina diversi problemi {application_a_1}{application_name}, come 
            '''
            reply = util_ai.gen_reply(prompt).strip()
            data[key] = reply
            util.json_write(application_json_filepath, data)
            time.sleep(30)
            
        key = 'benefits'
        # del data[key] # (debug only)
        if key not in data:
            prompt = f'''
                scrivi un paragrafo di 100 parole spiegando quali sono i benefici della sanificazione ad ozono per {application_a_1}{application_name}.
                non spiegare cos'è l'ozono e non spiegare come funziona.
                inizia la risposta con queste parole: La sanificazione ad ozono ha diversi benefici {application_a_1}{application_name}, come
            '''
            reply = util_ai.gen_reply(prompt).strip()
            data[key] = reply
            util.json_write(application_json_filepath, data)
            time.sleep(30)
            
        key = 'applications'
        # del data[key] # (debug only)
        if key not in data:
            prompt = f'''
                scrivi un paragrafo di 100 parole spiegando quali sono le applicazioni della sanificazione ad ozono {application_a_1}{application_name}.
                non spiegare cos'è l'ozono e non spiegare come funziona.
                inizia la risposta con queste parole: La sanificazione ad ozono ha diverse applicazioni {application_a_1}{application_name}, come 
            '''
            reply = util_ai.gen_reply(prompt).strip()
            data[key] = reply
            util.json_write(application_json_filepath, data)
            time.sleep(30)

        studies = 'studies'
        # del data[key] # (debug only)
        if key not in data:
            prompt = f'''
                scrivi un paragrafo di 100 parole spiegando quali sono le applicazioni della sanificazione ad ozono {application_a_1}{application_name}.
                non spiegare cos'è l'ozono e non spiegare come funziona.
                inizia la risposta con queste parole: La sanificazione ad ozono ha diverse applicazioni {application_a_1}{application_name}, come 
            '''
            reply = util_ai.gen_reply(prompt).strip()
            data[key] = reply
            util.json_write(application_json_filepath, data)
            time.sleep(30)

        # HTML
        intro = data['intro']
        definition = data['definition']
        problems = data['problems']
        benefits = data['benefits']
        applications = data['applications']

        application_sector_slug = ''
        application_sector_name = ''
        for sector_row in sectors_rows[1:]:
            sector_id = sector_row[sectors_cols['sector_id']]
            sector_slug = sector_row[sectors_cols['sector_slug']]
            sector_name = sector_row[sectors_cols['sector_name']]
            if application_sector_id == sector_id:
                application_sector_slug = sector_slug
                application_sector_name = sector_name
                break

        article_html = ''
        article_html += f'<h1>{title}</h1>\n'
        image_path = f'/assets/images/ozono-sanificazione-{application_sector_slug}-{application_slug}-introduzione.jpg'
        if os.path.exists(f'public{image_path}'):
            article_html += f'<p><img src="{image_path}" alt="ozono sanificazione {sector_name} {application_name} introduzione"></p>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(intro)}</p>\n'
        article_html += f'<h2>Cosa è la sanificazione ad ozono {application_a_1}{application_name} e a cosa serve?</h2>\n'
        image_path = f'/assets/images/ozono-sanificazione-{application_sector_slug}-{application_slug}-definizione.jpg'
        if os.path.exists(f'public{image_path}'):
            article_html += f'<p><img src="{image_path}" alt="ozono sanificazione {sector_name} {application_name} definizione"></p>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(definition)}</p>\n'
        article_html += f'<h2>Quali problemi risolve la sanificazione ad ozono {application_a_1}{application_name}?</h2>\n'
        image_path = f'/assets/images/ozono-sanificazione-{application_sector_slug}-{application_slug}-problemi.jpg'
        if os.path.exists(f'public{image_path}'):
            article_html += f'<p><img src="{image_path}" alt="ozono sanificazione {sector_name} {application_name} problemi"></p>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(problems)}</p>\n'
        article_html += f'<h2>Quali benefici porta la sanificazione ad ozono {application_a_1}{application_name}?</h2>\n'
        image_path = f'/assets/images/ozono-sanificazione-{application_sector_slug}-{application_slug}-benefici.jpg'
        if os.path.exists(f'public{image_path}'):
            article_html += f'<p><img src="{image_path}" alt="ozono sanificazione {sector_name} {application_name} benefici"></p>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(benefits)}</p>\n'
        article_html += f'<h2>Quali applicazioni ha la sanificazione ad ozono {application_a_1}{application_name}?</h2>\n'
        image_path = f'/assets/images/ozono-sanificazione-{application_sector_slug}-{application_slug}-applicazioni.jpg'
        if os.path.exists(f'public{image_path}'):
            article_html += f'<p><img src="{image_path}" alt="ozono sanificazione {sector_name} {application_name} applicazioni"></p>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(applications)}</p>\n'

        breadcrumbs = util.generate_breadcrumbs(application_json_filepath)
        header_html = util.component_header_no_logo()
        reading_time = util.meta_reading_time(article_html)
        article_html = util.generate_toc(article_html)

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
                            <span>Autore: {g.ARTICLES_AUTHOR}</span>
                            <span>Tempo Lettura: {reading_time} min</span>
                        </div>
                        <div class="flex justify-between mb-8">
                            <span>Aggiornato: {lastmod}</span>
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

        application_html_filepath = f'public/ozono/sanificazione/settori/residenziale/{application_slug}.html'
        util.file_write(application_html_filepath, html)


def sector_page():
    sectors_csv_filepath = g.CSV_SECTORS_FILEPATH
    sectors_rows = util.csv_get_rows(sectors_csv_filepath)
    sectors_cols = util.csv_get_header_dict(sectors_rows)

    for sector_row in sectors_rows[1:]:
        sector_id = sector_row[sectors_cols['sector_id']]
        sector_name = sector_row[sectors_cols['sector_name']].lower().strip()
        sector_slug = sector_row[sectors_cols['sector_slug']].lower().strip()
        sector_a_1 = sector_row[sectors_cols['sector_a_1']].lower()

        # GET NUM APPLICATIONS PER SECTOR
        applications_num = 0
        for application_row in applications_rows[1:]:
            application_sector_id = application_row[applications_cols['application_sector_id']]
            if application_sector_id == sector_id:
                applications_num += 1

        title = f'{applications_num} applicazioni della sanificazione ad ozono nel settore {sector_a_1}{sector_name}'

        # JSON
        sector_json_filepath = f'database/json/ozono/sanificazione/settori/{sector_slug}.json'
        util.create_folder_for_filepath(sector_json_filepath)
        util.json_generate_if_not_exists(sector_json_filepath)
        sector_data = util.json_read(sector_json_filepath)
        sector_data['sector_id'] = sector_id
        sector_data['sector_name'] = sector_name
        sector_data['sector_slug'] = sector_slug
        sector_data['sector_a_1'] = sector_a_1
        sector_data['title'] = title
        lastmod = str(datetime.date.today())
        if 'lastmod' not in sector_data: sector_data['lastmod'] = lastmod
        else: lastmod = sector_data['lastmod']
        util.json_write(sector_json_filepath, sector_data)

        key = 'intro'
        # del sector_data[key] # (debug only)
        if key not in sector_data:
            prompt = f'''
                Scrivi in Italiano un paragrafo di 100 parole facendo molti esempi delle applicazioni della sanificazione ad ozono nel settore {sector_a_1}{sector_name}.
                Non spiegare cos'è e come funziona l'ozono.
                Inizia la tua risposta con le seguenti parole: L'ozono viene uato nel settore {sector_a_1}{sector_name} per .
            '''
            reply = util_ai.gen_reply(prompt).strip()
            sector_data[key] = reply
            util.json_write(sector_json_filepath, sector_data)
            time.sleep(30)

        if 'applications' not in sector_data: sector_data['applications'] = []
        applications_rows_filtered = []
        for application_row in applications_rows[1:]:
            application_sector_id = application_row[applications_cols['application_sector_id']]
            if application_sector_id == sector_id:
                application_id = application_row[applications_cols['application_id']].strip()
                application_slug = application_row[applications_cols['application_slug']].strip().lower()
                application_name = application_row[applications_cols['application_name']].strip().lower()
                application_a_1 = application_row[applications_cols['application_a_1']].lower()
                found = False
                for sector_application in sector_data['applications']:
                    sector_application_name = sector_application['application_name']
                    if sector_application_name == application_name:
                        found = True
                        break
                if not found:
                    applications_rows_filtered.append({
                        'application_id': application_id, 
                        'application_slug': application_slug, 
                        'application_name': application_name, 
                        'application_a_1': application_a_1
                    })
                else:
                    applications_rows_filtered.append(sector_application)
        sector_data['applications'] = applications_rows_filtered
        util.json_write(sector_json_filepath, sector_data)

        for application_obj in sector_data['applications']:
            key = 'application_desc'
            if key not in application_obj:
                application_name = application_obj['application_name']
                application_a_1 = application_obj['application_a_1']
                prompt = f'''
                    Scrivi in Italiano un paragrafo di 100 parole facendo molti esempi delle applicazioni della sanificazione ad ozono {application_a_1}{application_name}.
                    Non spiegare cos'è e come funziona l'ozono.
                    Comincia la tua risposta usando queste parole: La sanificazione ad ozono {application_a_1}{application_name} serve per 
                '''
                reply = util_ai.gen_reply(prompt).strip()
                application_obj[key] = reply
                util.json_write(sector_json_filepath, sector_data)
                time.sleep(30)


        # HTML
        intro = sector_data['intro']

        article_html = ''
        article_html += f'<h1>{title}</h1>\n'
        image_path = f'/assets/images/ozono-sanificazione-settori-{sector_slug}.jpg'
        if os.path.exists(f'public{image_path}'):
            article_html += f'<p><img src="{image_path}" alt="ozono sanificazione settore {sector_a_1}{sector_name} introduzione"></p>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(intro)}</p>\n'

        i = 0
        for application_obj in sector_data['applications']:
            i += 1
            application_slug = application_obj['application_slug']
            application_name = application_obj['application_name'].strip().lower()
            application_a_1 = application_obj['application_a_1'].strip().lower()
            application_desc = application_obj['application_desc']
            article_html += f'<h2>{i}. {application_name.title()}</h2>\n'
            image_path = f'/assets/images/ozono-sanificazione-{sector_slug}-{application_slug}-introduzione.jpg'
            if os.path.exists(f'public{image_path}'):
                article_html += f'<p><img src="{image_path}" alt="ozono sanificazione settore {application_a_1}{application_name} introduzione"></p>' + '\n'
            article_html += f'<p>{util.text_format_1N1_html(application_desc)}</p>\n'
            article_html += f'<p><a href="/ozono/sanificazione/settori/{sector_slug}/{application_slug}.html">{application_name}</a></p>\n'

        breadcrumbs = util.generate_breadcrumbs(sector_json_filepath)
        header_html = util.component_header_no_logo()
        reading_time = util.meta_reading_time(article_html)
        article_html = util.generate_toc(article_html)

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
                            <span>Autore: {g.ARTICLES_AUTHOR}</span>
                            <span>Tempo Lettura: {reading_time} min</span>
                        </div>
                        <div class="flex justify-between mb-8">
                            <span>Aggiornato: {lastmod}</span>
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

        application_html_filepath = f'public/ozono/sanificazione/settori/{sector_slug}.html'
        util.file_write(application_html_filepath, html)


def sectors_page():
    sectors_csv_filepath = 'database/csv/sectors.csv'
    sectors_rows = util.csv_get_rows(sectors_csv_filepath)
    sectors_cols = util.csv_get_header_dict(sectors_rows)

    sectors_json_filepath = f'database/json/ozono/sanificazione/settori.json'
    util.create_folder_for_filepath(sectors_json_filepath)
    util.json_generate_if_not_exists(sectors_json_filepath)
    sectors_data = util.json_read(sectors_json_filepath)

    lastmod = str(datetime.date.today())
    if 'lastmod' not in sectors_data: sectors_data['lastmod'] = lastmod
    else: lastmod = sectors_data['lastmod']
    sectors_num = len(sectors_rows[1:])
    sectors_data['sectors_num'] = sectors_num
    sectors_data['title'] = f'{sectors_num} settori di applicazione della sanificazione ad ozono'
    util.json_write(sectors_json_filepath, sectors_data)

    key = 'intro'
    if key not in sectors_data:
        prompt = f'''
            Scrivi in Italiano un paragrafo di 100 parole facendo molti esempi di settori di applicazione della sanificazione ad ozono.
            Non spiegare cos'è e come funziona l'ozono.
            Non scrivere liste.
            Inizia la tua risposta con le seguenti parole: L'ozono viene usato in diversi settori, come .
        '''
        reply = util_ai.gen_reply(prompt).strip()
        sectors_data[key] = reply
        util.json_write(sectors_json_filepath, sectors_data)
        time.sleep(30)

    if 'sectors' not in sectors_data: sectors_data['sectors'] = []
    for sector_row in sectors_rows[1:]:
        sector_id = sector_row[sectors_cols['sector_id']]
        sector_slug = sector_row[sectors_cols['sector_slug']].strip().lower()
        sector_name = sector_row[sectors_cols['sector_name']].strip().lower()
        sector_a_1 = sector_row[sectors_cols['sector_a_1']]

        found = False
        for sector_obj in sectors_data['sectors']:
            if sector_obj['sector_id'] == sector_id:
                found = True
                break

        if not found:
            sectors_data['sectors'].append({
                'sector_id': sector_id, 
                'sector_name': sector_name, 
                'sector_slug': sector_slug, 
                'sector_a_1': sector_a_1, 
            })
    util.json_write(sectors_json_filepath, sectors_data)

    for sector_obj in sectors_data['sectors']:
        sector_name = sector_obj['sector_name'].strip().lower()
        sector_a_1 = sector_obj['sector_a_1']

        key = 'sector_desc'
        if key not in sector_obj:
            prompt = f'''
                Scrivi un paragrafo di 100 parole facendo molti esempi delle applicazioni della sanificazione ad ozono nel settore {sector_a_1}{sector_name}.
                Non spiegare cos'è e come funziona l'ozono.
                Comincia la tua risposta usando queste parole: La sanificazione ad ozono nel settore {sector_a_1}{sector_name} serve per 
            '''
            reply = util_ai.gen_reply(prompt).strip()
            sector_obj[key] = reply
            util.json_write(sectors_json_filepath, sectors_data)
            time.sleep(30)

    # HTML
    title = sectors_data['title']
    intro = sectors_data['intro']

    article_html = ''
    article_html += f'<h1>{title}</h1>\n'

    image_filepath_in = f'C:/og-assets/images/articles/0000.jpg'
    image_filepath_out = f'public/assets/images/ozono-sanificazione-settori.jpg'
    image_filepath_website = f'/assets/images/ozono-sanificazione-settori.jpg'
    if not os.path.exists(image_filepath_out):
        util_img.resize(image_filepath_in, image_filepath_out)
    if os.path.exists(image_filepath_out):
        article_html += f'<p><img src="{image_filepath_website}" alt="ozono sanificazione settori introduzione"></p>' + '\n'

    article_html += f'<p>{util.text_format_1N1_html(intro)}</p>\n'

    i = 0
    for sector_obj in sectors_data['sectors']:
        i += 1
        sector_name = sector_obj['sector_name'].lower().strip()
        sector_slug = sector_obj['sector_slug']
        sector_desc = sector_obj['sector_desc']
        sector_a_1 = sector_obj['sector_a_1']
        article_html += f'<h2>{i}. {sector_name.title()}</h2>\n'
        image_path = f'/assets/images/ozono-sanificazione-settori-{sector_slug}.jpg'
        if os.path.exists(f'public{image_path}'):
            article_html += f'<p><img src="{image_path}" alt="ozono sanificazione settore {sector_a_1}{sector_name} introduzione"></p>' + '\n'
            print(sector_name)
        sector_desc = sector_desc.replace(
            f'sanificazione ad ozono nel settore {sector_a_1}{sector_name}',
            f'<a href="/ozono/sanificazione/settori/{sector_slug}.html">sanificazione ad ozono nel settore {sector_a_1}{sector_name}</a>',
            1,
        )
        article_html += f'<p>{util.text_format_1N1_html(sector_desc)}</p>\n'
        # article_html += f'<p><a href="/ozono/sanificazione/settori/{sector_slug}.html">{sector_name}</a></p>\n'

    breadcrumbs = util.generate_breadcrumbs(sectors_json_filepath)
    header_html = util.component_header_no_logo()
    reading_time = util.meta_reading_time(article_html)
    article_html = util.generate_toc(article_html)

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
                        <span>Autore: {g.ARTICLES_AUTHOR}</span>
                        <span>Tempo Lettura: {reading_time} min</span>
                    </div>
                    <div class="flex justify-between mb-8">
                        <span>Aggiornato: {lastmod}</span>
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

    sectors_html_filepath = f'public/ozono/sanificazione/settori.html'
    util.file_write(sectors_html_filepath, html)


def applications_missing_images_csv():
    sectors_csv_filepath = g.CSV_SECTORS_FILEPATH
    sectors_rows = util.csv_get_rows(sectors_csv_filepath)
    sectors_cols = util.csv_get_header_dict(sectors_rows)

    applications_csv_filepath = g.CSV_APPLICATIONS_FILEPATH
    applications_rows = util.csv_get_rows(applications_csv_filepath)
    applications_cols = util.csv_get_header_dict(applications_rows)

    for sector_row in sectors_rows[1:]:
        sector_id = sector_row[sectors_cols['sector_id']]
        sector_slug = sector_row[sectors_cols['sector_slug']]
        # print(sector_row)
        print(sector_id)

        applications_rows_filtered = []
        for application_row in applications_rows:
            application_sector_id = application_row[applications_cols['application_sector_id']]
            if application_sector_id == sector_id:
                applications_rows_filtered.append(application_row)
                # print(application_row)

        for application_row in applications_rows_filtered:
            application_slug = application_row[applications_cols['application_slug']]

            application_images_folderpath = f'C:/og-assets/images/articles/{sector_slug}/{application_slug}'
            print(application_images_folderpath)

# applications_pages()
# sector_page()
# sectors_page()

applications_missing_images_csv()