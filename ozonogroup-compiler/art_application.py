import time
import datetime

import g
import util
import util_ai

applications_rows = util.csv_get_rows('database/csv/applications.csv')
applications_cols = util.csv_get_header_dict(applications_rows)

for application_row in applications_rows[1:]:
    # CSV
    application_id = application_row[applications_cols['application_id']]
    application_name = application_row[applications_cols['application_name']].strip().lower()
    application_slug = application_row[applications_cols['application_slug']].strip().lower()
    application_a_1 = application_row[applications_cols['application_a_1']].lower()
    application_sector_id = application_row[applications_cols['application_sector_id']]
    title = f'Sanificazione ozono {application_a_1}{application_name}'

    # print(application_id)
    # print(application_name)
    # print(application_slug)
    # print(application_a_1)
    # print(application_sector_id)

    # JSON
    application_json_filepath = f'database/json/ozono/sanificazione/settori/residenziale/{application_slug}.json'
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
            scrivi un paragrafo di 100 parole spiegando quali sono i benefici della sanificazione ad ozono per per {application_a_1}{application_name}.
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

    # HTML
    intro = data['intro']
    definition = data['definition']
    problems = data['problems']
    benefits = data['benefits']
    applications = data['applications']

    article_html = ''
    article_html += f'<h1>{title}</h1>\n'
    article_html += f'<p>{intro}</p>\n'
    article_html += f'<h2>Cosa è la sanificazione ad ozono {application_a_1}{application_name} e a cosa serve?</h2>\n'
    article_html += f'<p>{definition}</p>\n'
    article_html += f'<h2>Quali problemi risolve la sanificazione ad ozono {application_a_1}{application_name}?</h2>\n'
    article_html += f'<p>{problems}</p>\n'
    article_html += f'<h2>Quali benefici porta la sanificazione ad ozono {application_a_1}{application_name}?</h2>\n'
    article_html += f'<p>{benefits}</p>\n'
    article_html += f'<h2>Quali applicazioni ha la sanificazione ad ozono {application_a_1}{application_name}?</h2>\n'
    article_html += f'<p>{applications}</p>\n'

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

    break



sectors_rows = util.csv_get_rows('database/csv/sectors.csv')
sectors_cols = util.csv_get_header_dict(sectors_rows)

for sector_row in sectors_rows[1:]:
    sector_id = sector_row[sectors_cols['sector_id']]
    sector_name = sector_row[sectors_cols['sector_name']].lower().strip()
    sector_slug = sector_row[sectors_cols['sector_slug']].lower().strip()
    sector_a_1 = sector_row[sectors_cols['sector_a_1']].lower()
    title = f'?? applicazioni della sanificazione ad ozono nel settore {sector_a_1}{sector_name}'

    print(sector_id)
    print(sector_name)
    print(sector_slug)
    print(sector_a_1)

    # JSON
    sector_json_filepath = f'database/json/ozono/sanificazione/settori/{sector_slug}.json'
    util.create_folder_for_filepath(sector_json_filepath)
    util.json_generate_if_not_exists(sector_json_filepath)
    data = util.json_read(sector_json_filepath)
    data['sector_id'] = sector_id
    data['sector_name'] = sector_name
    data['sector_slug'] = sector_slug
    data['sector_a_1'] = sector_a_1
    data['title'] = title
    lastmod = str(datetime.date.today())
    if 'lastmod' not in data: data['lastmod'] = lastmod
    else: lastmod = data['lastmod']

    if 'applications' not in data: data['applications'] = []
    applications_rows_filtered = []
    for application_row in applications_rows[1:]:
        application_sector_id = application_row[applications_cols['application_sector_id']]
        if application_sector_id == sector_id:
            application_name = application_row[applications_cols['application_name']].strip().lower()
            application_a_1 = application_row[applications_cols['application_a_1']].lower()
            found = False
            for sector_application in data['applications']:
                sector_application_name = sector_application['application_name']
                if sector_application_name == application_name:
                    found = True
                    break
            if not found:
                applications_rows_filtered.append({'application_name': application_name, 'application_a_1': application_a_1})
            else:
                applications_rows_filtered.append(sector_application)
    data['applications'] = applications_rows_filtered
    util.json_write(sector_json_filepath, data)

    # JSON AI
    key = 'intro'
    # del data[key] # (debug only)
    if key not in data:
        prompt = f'''
            Scrivi in Italiano un paragrafo di 100 parole facendo molti esempi delle applicazioni della sanificazione ad ozono nel settore {sector_a_1}{sector_name}.
            Non spiegare cos'è e come funziona l'ozono.
            Inizia la tua risposta con le seguenti parole: L'ozono viene uato nel settore {sector_a_1}{sector_name} per .
        '''
        reply = util_ai.gen_reply(prompt).strip()
        data[key] = reply
        util.json_write(sector_json_filepath, data)
        time.sleep(30)

    for application_obj in data['applications']:
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
            util.json_write(sector_json_filepath, data)
            time.sleep(30)



    # HTML
    intro = data['intro']

    article_html = ''
    article_html += f'<h1>{title}</h1>\n'
    article_html += f'<p>{intro}</p>\n'
    i = 0
    for application_obj in data['applications']:
        i += 1
        application_name = application_obj['application_name']
        application_desc = application_obj['application_desc']
        article_html += f'<h2>{i}. {application_name}</h2>\n'
        article_html += f'<p>{application_desc}</p>\n'

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

    application_html_filepath = f'public/ozono/sanificazione/settori/{sector_slug}.html'
    util.file_write(application_html_filepath, html)

    break
