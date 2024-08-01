import os
import time
import datetime

import g
import util
import util_ai
import util_img

applications_rows = util.csv_get_rows(g.CSV_APPLICATIONS_FILEPATH)
applications_cols = util.csv_get_header_dict(applications_rows)
applications_rows = applications_rows[1:]

sectors_rows = util.csv_get_rows(g.CSV_SECTORS_FILEPATH)
sectors_cols = util.csv_get_header_dict(sectors_rows)

studies_rows = util.csv_get_rows(g.CSV_APPLICATIONS_STUDIES_FILEPATH)
studies_cols = util.csv_get_cols(studies_rows)



bacteria_rows = util.csv_get_rows(g.CSV_BACTERIA_FILEPATH)
bacteria_cols = util.csv_get_cols(bacteria_rows)
bacteria_rows = bacteria_rows[1:]
applications_bacteria_rows = util.csv_get_rows(g.CSV_APPLICATIONS_BACTERIA_FILEPATH)
applications_bacteria_cols = util.csv_get_cols(applications_bacteria_rows)
applications_bacteria_rows = applications_bacteria_rows[1:]

virus_rows = util.csv_get_rows(g.CSV_VIRUS_FILEPATH)
virus_cols = util.csv_get_cols(virus_rows)
virus_rows = virus_rows[1:]
applications_virus_rows = util.csv_get_rows(g.CSV_APPLICATIONS_VIRUS_FILEPATH)
applications_virus_cols = util.csv_get_cols(applications_virus_rows)
applications_virus_rows = applications_virus_rows[1:]

molds_rows = util.csv_get_rows(g.CSV_MOLDS_FILEPATH)
molds_cols = util.csv_get_cols(molds_rows)
molds_rows = molds_rows[1:]
applications_molds_rows = util.csv_get_rows(g.CSV_APPLICATIONS_MOLDS_FILEPATH)
applications_molds_cols = util.csv_get_cols(applications_molds_rows)
applications_molds_rows = applications_molds_rows[1:]

insects_rows = util.csv_get_rows(g.CSV_INSECTS_FILEPATH)
insects_cols = util.csv_get_cols(insects_rows)
insects_rows = insects_rows[1:]
applications_insects_rows = util.csv_get_rows(g.CSV_APPLICATIONS_INSECTS_FILEPATH)
applications_insects_cols = util.csv_get_cols(applications_insects_rows)
applications_insects_rows = applications_insects_rows[1:]



num_applications = 0


def delete_applications_key(key):
    for application_row in applications_rows:
        application_id = application_row[applications_cols['application_id']]
        application_slug = application_row[applications_cols['application_slug']].strip().lower()
        application_sector_id = application_row[applications_cols['application_sector_id']]

        sector_row = util.csv_get_rows_by_entity(g.CSV_SECTORS_FILEPATH, application_sector_id, col_num=sectors_cols['sector_id'])[0]
        sector_slug = sector_row[sectors_cols['sector_slug']].strip().lower()

        application_json_filepath = f'database/json/ozono/sanificazione/settori/{sector_slug}/{application_slug}.json'
        util.create_folder_for_filepath(application_json_filepath)
        util.json_generate_if_not_exists(application_json_filepath)
        data = util.json_read(application_json_filepath)

        # if application_sector_id == '9':
        if key in data: del data[key] # (debug only)
        util.json_write(application_json_filepath, data)

# delete_applications_key('benefits_list')
# quit()


############################################################
# JUNCTIONS
############################################################

def csv_get_bacteria_by_application(application_id):
    applications_bacteria_rows_filtered = util.csv_get_rows_by_col_val(
        g.CSV_APPLICATIONS_BACTERIA_FILEPATH, applications_bacteria_cols['application_id'], application_id
    )

    bacteria_rows_filtered = []
    for application_bacteria_row in applications_bacteria_rows_filtered:
        bacteria_id = application_bacteria_row[applications_bacteria_cols['problem_id']]
        for bacteria_row in bacteria_rows:
            if bacteria_row[bacteria_cols['bacteria_id']] == bacteria_id:
                bacteria_rows_filtered.append(bacteria_row)
                break

    return bacteria_rows_filtered


def csv_get_virus_by_application(application_id):
    applications_virus_rows_filtered = util.csv_get_rows_by_col_val(
        g.CSV_APPLICATIONS_VIRUS_FILEPATH, applications_virus_cols['application_id'], application_id
    )

    virus_rows_filtered = []
    for application_virus_row in applications_virus_rows_filtered:
        virus_id = application_virus_row[applications_virus_cols['virus_id']]
        for virus_row in virus_rows:
            if virus_row[virus_cols['virus_id']] == virus_id:
                virus_rows_filtered.append(virus_row)
                break

    return virus_rows_filtered


def csv_get_molds_by_application(application_id):
    applications_molds_rows_filtered = util.csv_get_rows_by_col_val(
        g.CSV_APPLICATIONS_MOLDS_FILEPATH, applications_molds_cols['application_id'], application_id
    )

    molds_rows_filtered = []
    for application_mold_row in applications_molds_rows_filtered:
        mold_id = application_mold_row[applications_molds_cols['mold_id']]
        for mold_row in molds_rows:
            if mold_row[molds_cols['mold_id']] == mold_id:
                molds_rows_filtered.append(mold_row)
                break

    return molds_rows_filtered


def csv_get_insects_by_application(application_id):
    applications_insects_rows_filtered = util.csv_get_rows_by_col_val(
        g.CSV_APPLICATIONS_INSECTS_FILEPATH, applications_insects_cols['application_id'], application_id
    )

    insects_rows_filtered = []
    for application_insect_row in applications_insects_rows_filtered:
        insect_id = application_insect_row[applications_insects_cols['insect_id']]
        for insect_row in insects_rows:
            if insect_row[insects_cols['insect_id']] == insect_id:
                insects_rows_filtered.append(insect_row)
                break

    return insects_rows_filtered


############################################################
# APPLICATIONS
############################################################

def ai_sentences(json_filepath, data, key, lines_num, prompt):
    print('here')
    if key not in data:

        reply = util_ai.gen_reply(prompt).strip()

        lines = reply.split('\n')
        lines_formatted = []
        for line in lines:
            line = line.strip()
            if line == '': continue
            if ':' in line: continue
            if ';' in line: continue
            if not line[0].isdigit(): continue
            if '.' not in line: continue
            line = '.'.join(line.split('.')[1:])
            line = line.strip()
            if line == '': continue
            lines_formatted.append(line)
        
        if len(lines_formatted) == lines_num:
            paragraph = ' '.join(lines_formatted)
            print('**************************************************')
            print(paragraph)
            print('**************************************************')
            data[key] = paragraph
            util.json_write(json_filepath, data)

        time.sleep(g.PROMPT_DELAY_TIME)


def ai_paragraph(json_filepath, data, key, prompt):
    if key not in data:

        reply = util_ai.gen_reply(prompt).strip()

        reply = reply.replace('\n', ' ')
        reply = reply.replace('  ', ' ')

        # paragraphs = reply.split('\n')
        # paragraphs_formatted = []
        # for paragraph in paragraphs:
        #     paragraph = paragraph.strip()
        #     if paragraph == '': continue
        #     if paragraph[0].isdigit(): continue
        #     if ':' in paragraph: continue
        #     paragraphs_formatted.append(paragraph)
        
        if reply != '':
            print('**************************************************')
            print(reply)
            print('**************************************************')
            data[key] = reply
            util.json_write(json_filepath, data)

        time.sleep(g.PROMPT_DELAY_TIME)


def ai_list(json_filepath, data, key, items_num, prompt):
    prompt = prompt.replace('[items_num]', items_num)
    if key not in data:
        reply = util_ai.gen_reply(prompt).strip()

        lines = reply.split('\n')
        list_items = []
        for line in lines:
            line = line.strip()
            if line == '': continue
            if not line[0].isdigit(): continue
            line = '.'.join(line.split('.')[1:])
            line = line.replace('*', '')
            line = line.strip()
            if line == '': continue
            list_items.append(line)

        if len(list_items) == items_num:
            print('*****************************************')
            print(list_items)
            print('*****************************************')
            data[key] = list_items
            util.json_write(application_json_filepath, data)

        time.sleep(g.PROMPT_DELAY_TIME)


def ai_problems(application_json_filepath, data):
    
    key = 'problems_list'
    if key not in data:
        application_name = data['application_name']
        application_a_1 = data['application_a_1']
        items_num = 10
        prompt = f'''
            Scrivi in Italiano una lista numerata di {items_num} problemi che la sanificazione ad ozono risolve {application_a_1}{application_name}.
            Includi una breve descrizione di una frase per ogni problema, spiegando perché l'ozono risolve questo problema {application_a_1}{application_name}.
            Sistema eventuali errori grammaticali e ortografici.
        '''
        reply = util_ai.gen_reply(prompt).strip()

        lines = reply.split('\n')
        list_items = []
        for line in lines:
            line = line.strip()
            if line == '': continue

            if not line[0].isdigit(): continue
            line = '.'.join(line.split('.')[1:])
            line = line.replace('*', '')

            line = line.strip()
            if line == '': continue
            list_items.append(line)

        if len(list_items) == items_num:
            print('*****************************************')
            print(list_items)
            print('*****************************************')
            data[key] = list_items
            util.json_write(application_json_filepath, data)
        time.sleep(g.PROMPT_DELAY_TIME)





def json_application_intro(json_filepath, data):
    application_name = data['application_name']
    application_a_1 = data['application_a_1']

    key = 'intro_desc'
    if key not in data:
        prompt = f'''
            Scrivi in Italiano 5 frasi brevi sulla sanificazione ad ozono {application_a_1}{application_name}.
            Nella frase 1, spiega cos'è la sanificazione ad ozono {application_a_1}{application_name} e quali problemi elimina {application_a_1}{application_name}.
            Nella frase 2, spiega quali sono le ripercussioni di questi problemi in termini di salute.
            Nella frase 3, spiega quali sono le ripercussioni di questi problemi in termini econimici.
            Nella frase 4, spiega quali sono le applicazioni dell'ozono {application_a_1}{application_name}.
            Nella frase 5, spiega quali sono i vantaggi dell'ozono {application_a_1}{application_name} confronto ad altri metodi di sanificazione.
            Rispondi con una lista numerata.
        '''
        reply = util_ai.gen_reply(prompt).strip()

        lines = reply.split('\n')
        lines_formatted = []
        for line in lines:
            line = line.strip()
            if line == '': continue
            if ':' in line: continue
            if ';' in line: continue
            if not line[0].isdigit(): continue
            if '.' not in line: continue
            line = '.'.join(line.split('.')[1:])
            line = line.strip()
            if line == '': continue
            lines_formatted.append(line)
        
        if len(lines_formatted) == 5:
            paragraph = ' '.join(lines_formatted)
            print('**************************************************')
            print(paragraph)
            print('**************************************************')
            data[key] = paragraph
            util.json_write(json_filepath, data)

        time.sleep(g.PROMPT_DELAY_TIME)


def json_application_definition(json_filepath, data):
    application_name = data['application_name']
    application_a_1 = data['application_a_1']

    key = 'definition_desc'
    if key not in data:
        prompt = f'''
            Scrivi un paragrafo di 100 parole spiegando cos'è e a cosa serve la sanificazione ad ozono per il seguente campo di applicazioni: {application_name}.
            Includi solo informazioni specifiche su questo campo di applicazione, e non informazioni generiche sull'ozono.
        '''

        reply = util_ai.gen_reply(prompt).strip()

        reply = reply.replace('\n', ' ')
        reply = reply.replace('  ', ' ')

        
        if reply != '':
            print('**************************************************')
            print(reply)
            print('**************************************************')
            data[key] = reply
            util.json_write(json_filepath, data)

        time.sleep(g.PROMPT_DELAY_TIME)


def json_application_problems(json_filepath, data):
    application_name = data['application_name']
    application_a_1 = data['application_a_1']

    key = 'problems_desc'
    if key not in data:
        prompt = f'''
            Scrivi un paragrafo di 100 parole spiegando quali problemi risolve la sanificazione ad ozono {application_a_1}{application_name}.
            Icludi nomi di batteri, virus, muffe, parassiti e odori.
            Non spiegare cos'è l'ozono e non spiegare come funziona.
            Inizia la risposta con queste parole: La sanificazione ad ozono elimina diversi problemi {application_a_1}{application_name}, come 
        '''

        reply = util_ai.gen_reply(prompt).strip()

        reply = reply.replace('\n', ' ')
        reply = reply.replace('  ', ' ')

        
        if reply != '':
            print('**************************************************')
            print(reply)
            print('**************************************************')
            data[key] = reply
            util.json_write(json_filepath, data)

        time.sleep(g.PROMPT_DELAY_TIME)


def json_application_bacteria(json_filepath, data):
    key = 'bacteria_desc'
    if key not in data:
        items_num = 3
        application_id = data['application_id']
        application_slug = data['application_slug']
        application_name = data['application_name'].lower().strip()
        application_a_1 = data['application_a_1']

        bacteria_rows_filtered = csv_get_bacteria_by_application(application_id)
        bacteria_names = [bacteria_row[bacteria_cols['bacteria_name']].capitalize() for bacteria_row in bacteria_rows_filtered]
        bacteria_a_1 = [bacteria_row[bacteria_cols['bacteria_a_1']].capitalize() for bacteria_row in bacteria_rows_filtered]

        bacteria_names_prompt_list = ''
        for bacteria_name in bacteria_names[:items_num]:
            bacteria_names_prompt_list += f'- {bacteria_name}\n'

        prompt = f'''
            Per ogni batterio della seguente lista:
            {bacteria_names_prompt_list}

            Scrivi 1 breve frase facendo esempi di dove questo batterio si trova {application_a_1}{application_name} e perché questo battrio è un problema per le persone.
            Includi "{application_name}" in ogni frase.
            Rispondi con il minor numero di parole possibili.
            Rispondi con una lista numerata.
            Rispondi con fatti certi, non con fatti possibili.
            Inizia la risposta con le seguenti parole: {bacteria_a_1[0]}{bacteria_names[0]} si trova . 
            Scrivi in Italiano, non includere parole inglesi.
        '''

        reply = util_ai.gen_reply(prompt).strip()

        lines = reply.split('\n')
        lines_formatted = []
        for line in lines:
            line = line.strip()
            if line == '': continue
            if ':' in line: continue
            if ';' in line: continue
            if not line[0].isdigit: continue
            if '.' not in line: continue
            line = '.'.join(line.split('.')[1:])
            line = line.strip()
            if line == '': continue
            lines_formatted.append(line)

        if len(lines_formatted) == items_num:
            # reply_formatted = ' '.join(lines_formatted)
            print('**************************************************')
            print(lines_formatted)
            print('**************************************************')
            data[key] = lines_formatted
            util.json_write(json_filepath, data)

        time.sleep(g.PROMPT_DELAY_TIME)


def json_application_virus(json_filepath, data):
    key = 'virus_desc'
    if key not in data:
        items_num = 3
        application_id = data['application_id']
        application_slug = data['application_slug']
        application_name = data['application_name'].lower().strip()
        application_a_1 = data['application_a_1']

        virus_rows_filtered = csv_get_virus_by_application(application_id)
        virus_names = [virus_row[virus_cols['virus_name']] for virus_row in virus_rows_filtered]
        virus_a_1 = [virus_row[virus_cols['virus_a_1']].capitalize() for virus_row in virus_rows_filtered]
        virus_names_prompt = ', '.join(virus_names[:5])

        virus_names_prompt_list = ''
        for virus_name in virus_names[:items_num]:
            virus_names_prompt_list += f'- {virus_name}\n'

        prompt = f'''
            Per ogni virus della seguente lista:
            {virus_names_prompt_list}

            Scrivi 1 breve frase facendo esempi di dove questo virus si trova {application_a_1}{application_name} e perché questo virus è un problema per le persone.
            Includi "{application_name}" in ogni frase.
            Rispondi con il minor numero di parole possibili.
            Rispondi con una lista numerata.
            Rispondi con fatti certi, non con fatti possibili.
            Inizia la risposta con le seguenti parole: {virus_a_1[0]}{virus_names[0]} si trova . 
            Scrivi in Italiano, non includere parole inglesi.
        '''
        reply = util_ai.gen_reply(prompt).strip()

        lines = reply.split('\n')
        lines_formatted = []
        for line in lines:
            line = line.strip()
            if line == '': continue
            if ':' in line: continue
            if ';' in line: continue
            if not line[0].isdigit: continue
            if '.' not in line: continue
            line = '.'.join(line.split('.')[1:])
            line = line.strip()
            if line == '': continue
            lines_formatted.append(line)

        if len(lines_formatted) == items_num:
            # reply_formatted = ' '.join(lines_formatted)
            print('**************************************************')
            print(lines_formatted)
            print('**************************************************')
            data[key] = lines_formatted
            util.json_write(json_filepath, data)

        time.sleep(g.PROMPT_DELAY_TIME)


def json_application_molds(json_filepath, data):
    key = 'molds_desc'
    if key not in data:
        items_num = 3
        application_id = data['application_id']
        application_slug = data['application_slug']
        application_name = data['application_name'].lower().strip()
        application_a_1 = data['application_a_1']

        molds_rows_filtered = csv_get_molds_by_application(application_id)
        molds_names = [molds_row[molds_cols['mold_name']] for molds_row in molds_rows_filtered]
        molds_a_1 = [mold_row[molds_cols['mold_a_1']].capitalize() for mold_row in molds_rows_filtered]
        molds_names_prompt = ', '.join(molds_names[:5])
        
        molds_names_prompt_list = ''
        for mold_name in molds_names[:items_num]:
            molds_names_prompt_list += f'- {mold_name}\n'

        prompt = f'''
            Per ogni muffa della seguente lista:
            {molds_names_prompt_list}

            Scrivi 1 breve frase facendo esempi di dove questa muffa si trova {application_a_1}{application_name} e perché questa muffa è un problema per le persone.
            Includi "{application_name}" in ogni frase.
            Rispondi con il minor numero di parole possibili.
            Rispondi con una lista numerata.
            Rispondi con fatti certi, non con fatti possibili.
            Inizia la risposta con le seguenti parole: {molds_a_1[0]}{molds_names[0]} si trova . 
            Scrivi in Italiano, non includere parole inglesi.
        '''
        reply = util_ai.gen_reply(prompt).strip()

        lines = reply.split('\n')
        lines_formatted = []
        for line in lines:
            line = line.strip()
            if line == '': continue
            if ':' in line: continue
            if ';' in line: continue
            if not line[0].isdigit: continue
            if '.' not in line: continue
            line = '.'.join(line.split('.')[1:])
            line = line.strip()
            if line == '': continue
            lines_formatted.append(line)

        if len(lines_formatted) == items_num:
            # reply_formatted = ' '.join(lines_formatted)
            print('**************************************************')
            print(lines_formatted)
            print('**************************************************')
            data[key] = lines_formatted
            util.json_write(json_filepath, data)

        time.sleep(g.PROMPT_DELAY_TIME)


def json_application_insects(json_filepath, data):
    key = 'insects_desc'
    if key not in data:
        items_num = 3
        application_id = data['application_id']
        application_slug = data['application_slug']
        application_name = data['application_name'].lower().strip()
        application_a_1 = data['application_a_1']

        insects_rows_filtered = csv_get_insects_by_application(application_id)
        insects_names = [insects_row[insects_cols['insect_name']] for insects_row in insects_rows_filtered]
        insects_a_1 = [insect_row[insects_cols['insect_a_1']].capitalize() for insect_row in insects_rows_filtered]
        insects_names_prompt = ', '.join(insects_names[:5])
        
        insects_names_prompt_list = ''
        for insect_name in insects_names[:items_num]:
            insects_names_prompt_list += f'- {insect_name}\n'

        prompt = f'''
            Per ogni insetto della seguente lista:
            {insects_names_prompt_list}

            Scrivi 1 breve frase facendo esempi di dove questo insetto si trova {application_a_1}{application_name} e perché questo insetto è un problema per le persone.
            Includi "{application_name}" in ogni frase.
            Rispondi con il minor numero di parole possibili.
            Rispondi con una lista numerata.
            Rispondi con fatti certi, non con fatti possibili.
            Inizia la risposta con le seguenti parole: {insects_a_1[0]}{insects_names[0]} si trova . 
            Scrivi in Italiano, non includere parole inglesi.
        '''
        reply = util_ai.gen_reply(prompt).strip()

        lines = reply.split('\n')
        lines_formatted = []
        for line in lines:
            line = line.strip()
            if line == '': continue
            if ':' in line: continue
            if ';' in line: continue
            if not line[0].isdigit: continue
            if '.' not in line: continue
            line = '.'.join(line.split('.')[1:])
            line = line.strip()
            if line == '': continue
            lines_formatted.append(line)

        if len(lines_formatted) == items_num:
            # reply_formatted = ' '.join(lines_formatted)
            print('**************************************************')
            print(lines_formatted)
            print('**************************************************')
            data[key] = lines_formatted
            util.json_write(json_filepath, data)

        time.sleep(g.PROMPT_DELAY_TIME)





def ai_benefits(application_json_filepath, data):
    key = 'benefits'
    if key not in data:
        application_name = data['application_name']
        application_a_1 = data['application_a_1']
        prompt = f'''
            scrivi un paragrafo di 100 parole spiegando quali sono i benefici della sanificazione ad ozono per {application_a_1}{application_name}.
            non spiegare cos'è l'ozono e non spiegare come funziona.
            inizia la risposta con queste parole: La sanificazione ad ozono ha diversi benefici {application_a_1}{application_name}, come
        '''
        reply = util_ai.gen_reply(prompt).strip()
        data[key] = reply
        util.json_write(application_json_filepath, data)
        time.sleep(g.PROMPT_DELAY_TIME)

    key = 'benefits_list'
    if key not in data:
        application_name = data['application_name']
        application_a_1 = data['application_a_1']
        items_num = 10
        prompt = f'''
            Scrivi in Italiano una lista numerata di {items_num} benefici che la sanificazione ad ozono ha {application_a_1}{application_name} confronto ad altri sistemi tradizionali di sanificazione.
            Includi una breve descrizione di una frase per ogni beneficio, spiegando perché l'ozono ha questo beneficio {application_a_1}{application_name} confronto i sistemi di sanificazione tradizionale.
            Sistema eventuali errori grammaticali e ortografici.
        '''
        reply = util_ai.gen_reply(prompt).strip()

        lines = reply.split('\n')
        list_items = []
        for line in lines:
            line = line.strip()
            if line == '': continue

            if not line[0].isdigit(): continue
            line = '.'.join(line.split('.')[1:])
            line = line.replace('*', '')

            line = line.strip()
            if line == '': continue
            list_items.append(line)

        if len(list_items) == items_num:
            print('*****************************************')
            print(list_items)
            print('*****************************************')
            data[key] = list_items
            util.json_write(application_json_filepath, data)
            time.sleep(g.PROMPT_DELAY_TIME)


def ai_applications(application_json_filepath, data):           
    key = 'applications'
    if key not in data:
        application_name = data['application_name']
        application_a_1 = data['application_a_1']
        prompt = f'''
            scrivi un paragrafo di 100 parole spiegando quali sono le applicazioni della sanificazione ad ozono {application_a_1}{application_name}.
            non spiegare cos'è l'ozono e non spiegare come funziona.
            inizia la risposta con queste parole: La sanificazione ad ozono ha diverse applicazioni {application_a_1}{application_name}, come 
        '''
        reply = util_ai.gen_reply(prompt).strip()
        data[key] = reply
        util.json_write(application_json_filepath, data)
        time.sleep(g.PROMPT_DELAY_TIME)


def ai_applications_equipment(application_json_filepath, data):
    key = 'applications_equipment_desc'
    if key not in data:
        application_name = data['application_name']
        application_a_1 = data['application_a_1']
        prompt = f'''
            Scrivi in Italiano un paragrafo di 100 parole spiegando quali attrezzature {application_a_1}{application_name} l'ozono può sanificare.
            inizia la risposta con queste parole: L'ozono viene usato per sanificare diverse attrezzature {application_a_1}{application_name}, come 
        '''
        reply = util_ai.gen_reply(prompt).strip()
        data[key] = reply
        util.json_write(application_json_filepath, data)
        time.sleep(g.PROMPT_DELAY_TIME)

    key = 'applications_equipment_list'
    if key not in data:
        application_name = data['application_name']
        application_a_1 = data['application_a_1']
        items_num = 10
        prompt = f'''
            Scrivi in Italiano una lista numerata di {items_num} attrezzature {application_a_1}{application_name} che l'ozono può sanificare.
            Includi una breve descrizione per ogni attrezzatura spiegando come l'ozono sanifica quell'attrezzatura.
        '''
        reply = util_ai.gen_reply(prompt).strip()

        lines = reply.split('\n')
        list_items = []
        for line in lines:
            line = line.strip()
            if line == '': continue

            if not line[0].isdigit(): continue
            line = '.'.join(line.split('.')[1:])
            line = line.replace('*', '')

            line = line.strip()
            if line == '': continue
            list_items.append(line)

        if len(list_items) == items_num:
            print('*****************************************')
            print(list_items)
            print('*****************************************')
            data[key] = list_items
            util.json_write(application_json_filepath, data)
        time.sleep(g.PROMPT_DELAY_TIME)


def html_sectors_sector_applications_problems_table(data):
    application_id = data['application_id']
    application_name = data['application_name']
    application_a_1 = data['application_a_1']
    article_html = ''

    bacteria_rows_filtered = csv_get_bacteria_by_application(application_id)
    bacteria_names = [bacteria_row[bacteria_cols['bacteria_name']].capitalize() for bacteria_row in bacteria_rows_filtered]
    bacteria_names_str = ', '.join(bacteria_names[:3])

    virus_rows_filtered = csv_get_virus_by_application(application_id)
    virus_names = [virus_row[virus_cols['virus_name']].capitalize() for virus_row in virus_rows_filtered]
    virus_names_str = ', '.join(virus_names[:3])

    molds_rows_filtered = csv_get_molds_by_application(application_id)
    molds_names = [molds_row[molds_cols['mold_name']].capitalize() for molds_row in molds_rows_filtered]
    molds_names_str = ', '.join(molds_names[:3])

    insects_rows_filtered = csv_get_insects_by_application(application_id)
    insects_names = [insects_row[insects_cols['insect_name']].capitalize() for insects_row in insects_rows_filtered]
    insects_names_str = ', '.join(insects_names[:3])

    article_html += f'<p>I problemi principali che l\'ozono risolve {application_a_1}{application_name} sono elencati nella seguente tabella.</p>'
    article_html += f'''
        <table>
            <tr>
                <th>Categoria Problema</th>
                <th>Nomi Problemi</th>
            </tr>
            <tr>
                <td>Batteri</td>
                <td>{bacteria_names_str}</td>
            </tr>
            <tr>
                <td>Virus</td>
                <td>{virus_names_str}</td>
            </tr>
            <tr>
                <td>Muffe</td>
                <td>{molds_names_str}</td>
            </tr>
            <tr>
                <td>Insetti</td>
                <td>{insects_names_str}</td>
            </tr>
        </table>
    '''

    return article_html



def art_applications(_id=-1):
    if _id == -1:
        if num_applications == 0:
            applications_rows_filtered = applications_rows
        else:
            applications_rows_filtered = applications_rows[:num_applications]
    else:
        applications_rows_filtered = util.csv_get_rows_by_col_val(
            g.CSV_APPLICATIONS_FILEPATH, applications_cols['application_id'], str(_id)
        )

    for application_row in applications_rows_filtered:
        application_id = application_row[applications_cols['application_id']]
        application_name = application_row[applications_cols['application_name']].strip().lower()
        application_slug = application_row[applications_cols['application_slug']].strip().lower()
        application_a_1 = application_row[applications_cols['application_a_1']].lower()
        application_sector_id = application_row[applications_cols['application_sector_id']]
        to_process = application_row[applications_cols['to_process']].strip().lower()

        if to_process == '': continue

        print(f'>> {application_name}')

        title = f'Sanificazione {application_name} con ozono'

        sector_row = util.csv_get_rows_by_entity(g.CSV_SECTORS_FILEPATH, application_sector_id, col_num=sectors_cols['sector_id'])[0]
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
        json_application_intro(application_json_filepath, data)
        json_application_definition(application_json_filepath, data)

        json_application_problems(application_json_filepath, data)
        # json_application_bacteria(application_json_filepath, data)
        # json_application_virus(application_json_filepath, data)
        # json_application_molds(application_json_filepath, data)
        # json_application_insects(application_json_filepath, data)

        # ai_benefits(application_json_filepath, data)

        ai_applications(application_json_filepath, data)
        if application_sector_id == '9':
            ai_applications_equipment(application_json_filepath, data)


        # STUDIES
        key = 'studies'
        if key not in data: data[key] = []

        studies_rows_filtered = util.csv_get_rows_by_entity(g.CSV_APPLICATIONS_STUDIES_FILEPATH, application_id, col_num=studies_cols['application_id'])
        for study_row in studies_rows_filtered:
            study_id = study_row[studies_cols['study_id']]
            study_title = study_row[studies_cols['study_title']]
            study_journal = study_row[studies_cols['study_journal']]
            study_abstract = study_row[studies_cols['study_abstract']]
            found = False
            for study_obj in data[key]:
                if study_obj['study_id'] == study_id:
                    found = True
                    break
            if not found:
                data[key].append({
                    'study_id': study_id,
                    'study_title': study_title,
                    'study_journal': study_journal,
                    'study_abstract': study_abstract,
                })

        util.json_write(application_json_filepath, data)

        for study_obj in data['studies']:
            key = 'study_summary'
            if key not in study_obj:
                study_journal = study_obj['study_journal']
                study_abstract = study_obj['study_abstract']

                prompt = f'''
                    Scrivi in Italiano un riassunto del seguente studio scientifico sulla sanificazione ad ozono {application_a_1}{application_name} : {study_abstract}
                    Inizia la risposta con queste parole: Secondo uno studio scientifico pubblicato dal {study_journal}, 
                '''

                reply = util_ai.gen_reply(prompt).strip()
                study_obj[key] = reply
                util.json_write(application_json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)

        # if key not in data:
            # prompt = f'''
            #     scrivi un paragrafo di 100 parole spiegando quali sono le applicazioni della sanificazione ad ozono {application_a_1}{application_name}.
            #     non spiegare cos'è l'ozono e non spiegare come funziona.
            #     inizia la risposta con queste parole: La sanificazione ad ozono ha diverse applicazioni {application_a_1}{application_name}, come 
            # '''
            # reply = util_ai.gen_reply(prompt).strip()
            # data[key] = reply
            # util.json_write(application_json_filepath, data)
            # time.sleep(g.PROMPT_DELAY_TIME)





        # HTML
        intro = data['intro_desc']
        definition = data['definition_desc']
        problems = data['problems_desc']
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


        article_html += html_sectors_sector_applications_problems_table(data)

        key = 'bacteria_desc'
        if key in data:
            bacteria_rows_filtered = csv_get_bacteria_by_application(application_id)
            bacteria_names = [bacteria_row[bacteria_cols['bacteria_name']].capitalize() for bacteria_row in bacteria_rows_filtered]
            bacteria_names_str = ', '.join(bacteria_names[:3])
            article_html += f'<h3>Batteri {application_a_1}{application_name}</h3>\n'
            article_html += f'<p>La sanificazione ad ozono elimina i principali batteri presenti {application_a_1}{application_name}, come {bacteria_names_str}.</p>\n'
            # article_html += f'{util.text_format_1N1_html(data["bacteria_desc"])}\n'
            for item in data[key]:
                article_html += f'<p>{item}</p>\n'
            article_html += f'<p>I batteri più comuni che si trovano {application_a_1}{application_name} sono elencati nella seguente lista.</p>\n'
            article_html += '<ul>\n'
            for bacteria_name in bacteria_names[:7]:
                article_html += f'<li>{bacteria_name}</li>\n'
            article_html += '</ul>\n'


        key = 'virus_desc'
        if key in data:
            virus_rows_filtered = csv_get_virus_by_application(application_id)
            virus_names = [virus_row[virus_cols['virus_name']].capitalize() for virus_row in virus_rows_filtered]
            virus_names_str = ', '.join(virus_names[:3])
            article_html += f'<h3>Virus {application_a_1}{application_name}</h3>\n'
            article_html += f'<p>La sanificazione ad ozono inattiva i principali virus presenti {application_a_1}{application_name}, come {virus_names_str}.</p>\n'
            # article_html += f'{util.text_format_1N1_html(data["virus_desc"])}\n'
            for item in data[key]:
                article_html += f'<p>{item}</p>\n'
            article_html += f'<p>I virus più comuni che si trovano {application_a_1}{application_name} sono elencati nella seguente lista.</p>\n'
            article_html += '<ul>\n'
            for virus_name in virus_names[:7]:
                article_html += f'<li>{virus_name}</li>\n'
            article_html += '</ul>\n'



        key = 'molds_desc'
        if key in data:
            molds_rows_filtered = csv_get_molds_by_application(application_id)
            molds_names = [row[molds_cols['mold_name']].capitalize() for row in molds_rows_filtered]
            molds_names_str = ', '.join(molds_names[:3])
            article_html += f'<h3>Muffe {application_a_1}{application_name}</h3>\n'
            article_html += f'<p>La sanificazione ad ozono inattiva le principali muffe presenti {application_a_1}{application_name}, come {molds_names_str}.</p>\n'
            # article_html += f'{util.text_format_1N1_html(data["molds_desc"])}\n'
            for item in data[key]:
                article_html += f'<p>{item}</p>\n'
            article_html += f'<p>Le muffe più comuni che si trovano {application_a_1}{application_name} sono elencate nella seguente lista.</p>\n'
            article_html += '<ul>\n'
            for mold_name in molds_names[:7]:
                article_html += f'<li>{mold_name}</li>\n'
            article_html += '</ul>\n'


        key = 'insects_desc'
        if key in data:
            insects_rows_filtered = csv_get_molds_by_application(application_id)
            insects_names = [row[insects_cols['insect_name']].capitalize() for row in insects_rows_filtered]
            insects_names_str = ', '.join(insects_names[:3])
            article_html += f'<h3>Insetti {application_a_1}{application_name}</h3>\n'
            article_html += f'<p>La sanificazione ad ozono repelle i principali insetti presenti {application_a_1}{application_name}, come {insects_names_str}.</p>\n'
            # article_html += f'{util.text_format_1N1_html(data["insects_desc"])}\n'
            for item in data[key]:
                article_html += f'<p>{item}</p>\n'
            article_html += f'<p>Gli insetti più comuni che si trovano {application_a_1}{application_name} sono elencati nella seguente lista.</p>\n'
            article_html += '<ul>\n'
            for insect_name in insects_names[:7]:
                article_html += f'<li>{insect_name}</li>\n'
            article_html += '</ul>\n'




        article_html += f'<h2>Quali benefici porta la sanificazione ad ozono {application_a_1}{application_name}?</h2>\n'
        image_path = f'/assets/images/ozono-sanificazione-{application_sector_slug}-{application_slug}-benefici.jpg'
        if os.path.exists(f'public{image_path}'):
            article_html += f'<p><img src="{image_path}" alt="ozono sanificazione {sector_name} {application_name} benefici"></p>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(benefits)}</p>\n'

        if 'benefits_list' in data:
            benefits_list = data['benefits_list']
            article_html += f'<ul>\n'
            for item in benefits_list:
                chunk_1 = item.split(':')[0]
                chunk_2 = ':'.join(item.split(':')[1:])
                article_html += f'<li><strong>{chunk_1}</strong>: {chunk_2}</li>\n'
            article_html += f'</ul>\n'



        article_html += f'<h2>Quali applicazioni ha la sanificazione ad ozono {application_a_1}{application_name}?</h2>\n'
        image_path = f'/assets/images/ozono-sanificazione-{application_sector_slug}-{application_slug}-applicazioni.jpg'
        if os.path.exists(f'public{image_path}'):
            article_html += f'<p><img src="{image_path}" alt="ozono sanificazione {sector_name} {application_name} applicazioni"></p>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(applications)}</p>\n'

        if 'applications_equipment_desc' in data and 'applications_equipment_list' in data:
            applications_equipment_desc = data['applications_equipment_desc']
            applications_equipment_list = data['applications_equipment_list']
            article_html += f'<h3>Quali attrezzature l\'ozono sanifica {application_a_1}{application_name}?</h3>\n'
            article_html += f'<p>{util.text_format_1N1_html(applications_equipment_desc)}</p>\n'

            article_html += f'<ul>\n'
            for item in applications_equipment_list:
                chunk_1 = item.split(':')[0]
                chunk_2 = ':'.join(item.split(':')[1:])
                article_html += f'<li><strong>{chunk_1}</strong>: {chunk_2}</li>\n'
            article_html += f'</ul>\n'

        studies_objs = data['studies']
        if len(studies_objs) > 0:
            article_html += f'<h2>Quali studi scientifici provano l\'efficacia della sanificazione ad ozono {application_a_1}{application_name}?</h2>\n'
            image_path = f'/assets/images/ozono-sanificazione-{application_sector_slug}-{application_slug}-studi.jpg'
            if os.path.exists(f'public{image_path}'):
                article_html += f'<p><img src="{image_path}" alt="ozono sanificazione {sector_name} {application_name} studi"></p>' + '\n'
            for study_obj in studies_objs:
                study_title = study_obj['study_title']
                study_summary = study_obj['study_summary']
                article_html += f'<h3>{study_title}</h3>\n'
                article_html += f'<p>{util.text_format_1N1_html(study_summary)}</p>\n'


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

        application_html_filepath = f'public/ozono/sanificazione/settori/{sector_slug}/{application_slug}.html'
        util.file_write(application_html_filepath, html)





############################################################
# SECTORS
############################################################

def json_sectors_sector_intro(json_filepath, data):
    key = 'intro'
    # del data[key] # (debug only)
    if key not in data:
        sector_a_1 = data['sector_a_1']
        sector_name = data['sector_name']

        prompt = f'''
            Scrivi in Italiano un paragrafo di 100 parole facendo molti esempi delle applicazioni della sanificazione ad ozono nel settore {sector_a_1}{sector_name}.
            Non spiegare cos'è e come funziona l'ozono.
            Inizia la tua risposta con le seguenti parole: L'ozono viene uato nel settore {sector_a_1}{sector_name} per .
        '''
        reply = util_ai.gen_reply(prompt).strip()

        data[key] = reply
        util.json_write(json_filepath, data)

        time.sleep(g.PROMPT_DELAY_TIME)


def json_sectors_sector_applications(json_filepath, data):
    sector_id = data['sector_id']

    if 'applications' not in data: data['applications'] = []
    applications_rows_filtered = []
    for application_row in applications_rows:
        application_sector_id = application_row[applications_cols['application_sector_id']]

        if application_sector_id == sector_id:
            application_id = application_row[applications_cols['application_id']].strip()
            application_slug = application_row[applications_cols['application_slug']].strip().lower()
            application_name = application_row[applications_cols['application_name']].strip().lower()
            application_a_1 = application_row[applications_cols['application_a_1']].lower()

            found = False
            for sector_application in data['applications']:
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

    data['applications'] = applications_rows_filtered
    util.json_write(json_filepath, data)

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
            util.json_write(json_filepath, data)

            time.sleep(g.PROMPT_DELAY_TIME)


def sector_page():
    for sector_row in sectors_rows[1:]:
        sector_id = sector_row[sectors_cols['sector_id']]
        sector_name = sector_row[sectors_cols['sector_name']].lower().strip()
        sector_slug = sector_row[sectors_cols['sector_slug']].lower().strip()
        sector_a_1 = sector_row[sectors_cols['sector_a_1']].lower()

        # GET NUM APPLICATIONS PER SECTOR
        applications_num = 0
        for application_row in applications_rows:
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

        json_sectors_sector_intro(sector_json_filepath, sector_data)
        json_sectors_sector_applications(sector_json_filepath, sector_data)

        


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
            application_a_1 = application_obj['application_a_1'].lower()
            application_desc = application_obj['application_desc']
            article_html += f'<h2>{i}. {application_name.title()}</h2>\n'
            image_path = f'/assets/images/ozono-sanificazione-{sector_slug}-{application_slug}-introduzione.jpg'
            if os.path.exists(f'public{image_path}'):
                article_html += f'<p><img src="{image_path}" alt="ozono sanificazione settore {application_a_1}{application_name} introduzione"></p>' + '\n'

            application_desc = application_desc.replace(
                f'sanificazione ad ozono {application_a_1}{application_name}',
                f'<a href="/ozono/sanificazione/settori/{sector_slug}/{application_slug}.html">sanificazione ad ozono {application_a_1}{application_name}</a>',
                1,
            )
            article_html += f'<p>{util.text_format_1N1_html(application_desc)}</p>\n'

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
        time.sleep(g.PROMPT_DELAY_TIME)

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
            time.sleep(g.PROMPT_DELAY_TIME)

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


art_ozone()

art_applications()
# sector_page()
# sectors_page()

# applications_missing_images_csv()
