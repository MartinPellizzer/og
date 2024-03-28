import time
import re
import os

import util
import util_ai
import prompts

def ai_problems_csv():
    filepath = 'database/tables/applications.csv'
    applications = util.csv_get_rows(filepath)[1:]
    for application in applications:
        application_name = application[0].strip()
        application_a = application[1].strip()
        application_name_dash = application_name.lower().replace(' ', '-').replace("'", '-')

        rows = util.csv_get_rows_by_entity(filepath, application_name_dash)
        if rows != []: continue

        print(application_name_dash)

        prompt_num = 10
        prompt = f'''
            Scrivi in italiano una lista numerata dei {prompt_num} batteri patogeni più comuni presenti {application_a}{application_name}.
            Scrivi solo i nomi dei batteri patogeni, non le descrizioni.
        '''

        
        reply = util_ai.gen_reply(prompt)
        reply = reply.strip()

        if prompt_paragraphs_num == len(reply_formatted):
            print('***************************************')
            for line in reply_formatted:
                print(line)
            print('***************************************')

            # util.csv_add_rows(filepath, reply_formatted)




    # for index, plant in enumerate(plants):
    #     latin_name = plant[cols['latin_name']].strip().capitalize()
    #     common_name = plant[cols['common_name']].strip().title()
    #     entity = latin_name.lower().replace(' ', '-')

    #     print(index, '-', len(plants), '>>' , latin_name, '|', 'benefits')

    #     rows = util.csv_get_rows_by_entity(filepath, entity)
    #     if rows != []: continue

    #     prompt_paragraphs_num = 10
    #     prompt = f'''
    #         Write a numbered list of the {prompt_paragraphs_num} best health benefits of {common_name} ({latin_name}).
    #         Start each benefit with a third-person singular action verb.
    #         Write only the names of the benefits, not the descriptions.
    #         Write each benefit name in less than 5 words.
    #     '''

    #     
    #     reply = util_ai.gen_reply(prompt)
    #     reply = reply.strip()

    #     reply_formatted = []
    #     for line in reply.split('\n'):
    #         line = line.strip()
    #         if line == '': continue
    #         if ':' in line: continue 
    #         if line[0].isdigit():
    #             if '. ' in line: line = line.split('. ')[1].strip()
    #             if line == '': continue
    #             if line.endswith('.'): line = line[0:-1]
    #             reply_formatted.append([entity, line, ''])

    #     if prompt_paragraphs_num == len(reply_formatted):
    #         print('***************************************')
    #         for line in reply_formatted:
    #             print(line)
    #         print('***************************************')

    #         util.csv_add_rows(filepath, reply_formatted)





def json_applications_clear_field(field_name):
    filepath = 'database/tables/applications.csv'
    rows = util.csv_get_rows(filepath)[1:]
    for i, row in enumerate(rows):
        print(f'{i+1}/{len(rows)} >>>> {row[0].strip()} | {row[2].strip()}')
        application_name = row[0].strip().lower()
        application_name_dash = application_name.replace(' ', '-').replace("'", '-')
        application_a_1 = row[1]
        json_filepath = f'articles/public/ozono/sanificazione/applicazioni/{application_name_dash}.json'

        data = util.json_read(json_filepath)
        data[field_name] = ''
        util.json_write(json_filepath, data)





#####################################################################################
# DETAILED REPLY FOR APPLICATION (expensive!)
#####################################################################################

def ai_batteri_csv(row):
    problem_name = 'batteri'
    application_name = row[0].strip()
    application_a_1 = row[1]
    application_name_dash = application_name.lower().replace(' ', '-').replace("'", '-')

    filepath = f'database/tables/applicazioni-problemi-{problem_name}.csv'
    csv_rows = []
    try: csv_rows = util.csv_get_rows_by_entity(filepath, application_name_dash)
    except: util.csv_add_rows(filepath, [])
    if csv_rows != []: return
    
    prompt = f'''
        Scrivi in italiano una lista numerata dei nomi dei 10 {problem_name} patogeni più comuni {application_a_1}{application_name.lower()}.
        Lista solo i nomi, non aggiungere descrizioni.
        Scrivi SOLO nomi di {problem_name}, non di altri tipi di patogeni.
    '''
    reply = util_ai.gen_reply(prompt)
    reply = reply.strip()

    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if not line[0].isdigit(): continue
        if '. ' not in line: continut
        else: line = '. '.join(line.split('. ')[1:]).strip()
        if '(' in line: line = line.split('(')[0].strip()
        reply_formatted.append([application_name_dash, problem_name, line])

    reply_formatted = reply_formatted
    if len(reply_formatted) == 10:
        print('------------------------------')
        for e in reply_formatted:
            print(e)
        print('------------------------------')
        util.csv_add_rows(filepath, reply_formatted)

    time.sleep(30)


def ai_virus_csv(row):
    problem_name = 'virus'
    application_name = row[0].strip()
    application_a_1 = row[1]
    application_name_dash = application_name.lower().replace(' ', '-').replace("'", '-')

    filepath = f'database/tables/applicazioni-problemi-{problem_name}.csv'
    csv_rows = []
    try: csv_rows = util.csv_get_rows_by_entity(filepath, application_name_dash)
    except: util.csv_add_rows(filepath, [])
    if csv_rows != []: return
    
    prompt = f'''
        Scrivi in Italiano una lista numerata dei nomi scientifici di 10 {problem_name} patogeni per l'uomo che si possono trovare {application_a_1}{application_name.lower()}.
        Scrivi solo i nomi scientifici di {problem_name}, non aggiungere descrizioni.
    '''
    reply = util_ai.gen_reply(prompt)
    reply = reply.strip()

    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        line = line.replace('*', '')
        if not line[0].isdigit(): continue
        if '. ' not in line: continue
        else: line = '. '.join(line.split('. ')[1:]).strip()
        if '(' in line: line = line.split('(')[0].strip()
        if ': ' in line: line = line.split(': ')[0].strip()
        reply_formatted.append([application_name_dash, problem_name, line])

    reply_formatted = reply_formatted
    if len(reply_formatted) == 10:
        print('------------------------------')
        for e in reply_formatted:
            print(e)
        print('------------------------------')
        util.csv_add_rows(filepath, reply_formatted)

    time.sleep(30)


def ai_muffe_csv(row):
    problem_name = 'muffe'
    application_name = row[0].strip()
    application_a_1 = row[1]
    application_name_dash = application_name.lower().replace(' ', '-').replace("'", '-')

    filepath = f'database/tables/applicazioni-problemi-{problem_name}.csv'
    csv_rows = []
    try: csv_rows = util.csv_get_rows_by_entity(filepath, application_name_dash)
    except: util.csv_add_rows(filepath, [])
    if csv_rows != []: return
    
    prompt = f'''
        Scrivi in Italiano una lista numerata dei nomi scientifici di 10 {problem_name} patogeni per l'uomo che si possono trovare {application_a_1}{application_name.lower()}.
        Scrivi solo i nomi scientifici di {problem_name}, non aggiungere descrizioni.
    '''
    reply = util_ai.gen_reply(prompt)
    reply = reply.strip()

    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if not line[0].isdigit(): continue
        if '. ' not in line: continut
        else: line = '. '.join(line.split('. ')[1:]).strip()
        if '(' in line: line = line.split('(')[0].strip()
        line = line.replace('*', '')
        reply_formatted.append([application_name_dash, problem_name, line])

    reply_formatted = reply_formatted
    if len(reply_formatted) == 10:
        print('------------------------------')
        for e in reply_formatted:
            print(e)
        print('------------------------------')
        util.csv_add_rows(filepath, reply_formatted)

    time.sleep(30)


def ai_insetti_csv(row):
    problem_name = 'insetti'
    application_name = row[0].strip()
    application_a_1 = row[1]
    application_name_dash = application_name.lower().replace(' ', '-').replace("'", '-')

    filepath = f'database/tables/applicazioni-problemi-{problem_name}.csv'
    csv_rows = []
    try: csv_rows = util.csv_get_rows_by_entity(filepath, application_name_dash)
    except: util.csv_add_rows(filepath, [])
    if csv_rows != []: return
    
    prompt = f'''
        Scrivi in Italiano una lista numerata dei nomi scientifici di 10 {problem_name} indesiderati per l'uomo che si possono trovare {application_a_1}{application_name.lower()}.
        Scrivi solo i nomi scientifici di {problem_name}, non aggiungere descrizioni.
    '''
    reply = util_ai.gen_reply(prompt)
    reply = reply.strip()

    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if not line[0].isdigit(): continue
        if '. ' not in line: continut
        else: line = '. '.join(line.split('. ')[1:]).strip()
        if '(' in line: line = line.split('(')[0].strip()
        line = line.replace('*', '')
        reply_formatted.append([application_name_dash, problem_name, line])

    reply_formatted = reply_formatted
    if len(reply_formatted) == 10:
        print('------------------------------')
        for e in reply_formatted:
            print(e)
        print('------------------------------')
        util.csv_add_rows(filepath, reply_formatted)

    time.sleep(30)


def ai_odori_csv(row):
    problem_name = 'odori'
    application_name = row[0].strip()
    application_a_1 = row[1]
    application_name_dash = application_name.lower().replace(' ', '-').replace("'", '-')

    filepath = f'database/tables/applicazioni-problemi-{problem_name}.csv'
    csv_rows = []
    try: csv_rows = util.csv_get_rows_by_entity(filepath, application_name_dash)
    except: util.csv_add_rows(filepath, [])
    if csv_rows != []: return
    
    prompt = f'''
        Scrivi in Italiano una lista numerata di 10 {problem_name} indesiderati per l'uomo che si possono trovare {application_a_1}{application_name.lower()}.
        Scrivi solo i nomi di {problem_name}, non aggiungere descrizioni.
    '''
    reply = util_ai.gen_reply(prompt)
    reply = reply.strip()

    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if not line[0].isdigit(): continue
        if '. ' not in line: continut
        else: line = '. '.join(line.split('. ')[1:]).strip()
        if '(' in line: line = line.split('(')[0].strip()
        line = line.replace('*', '')
        reply_formatted.append([application_name_dash, problem_name, line])

    reply_formatted = reply_formatted
    if len(reply_formatted) >= 5:
        print('------------------------------')
        for e in reply_formatted:
            print(e)
        print('------------------------------')
        util.csv_add_rows(filepath, reply_formatted)

    time.sleep(30)






def ai_benefici_csv(row):
    application_name = row[0].strip()
    application_a_1 = row[1]
    application_name_dash = application_name.lower().replace(' ', '-').replace("'", '-')

    filepath = f'database/tables/applicazioni-benefici.csv'

    csv_rows = []
    try: csv_rows = util.csv_get_rows_by_entity(filepath, application_name_dash)
    except: util.csv_add_rows(filepath, [])
    if csv_rows != []: return
    
    prompt = f'''
        Scrivi in Italiano una lista numerata dei 10 benefici più comuni della sanificazione ad ozono {application_a_1}{application_name.lower()} confronto altri metodi di sanificazione.
        Lista solo i nomi dei benefici, non aggiungere descrizioni.
    '''
    reply = util_ai.gen_reply(prompt)
    reply = reply.strip()

    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if not line[0].isdigit(): continue
        if '. ' not in line: continut
        else: line = '. '.join(line.split('. ')[1:]).strip()
        if '(' in line: line = line.split('(')[0].strip()
        reply_formatted.append([application_name_dash, line])

    reply_formatted = reply_formatted
    if len(reply_formatted) == 10:
        print('------------------------------')
        for e in reply_formatted:
            print(e)
        print('------------------------------')
        util.csv_add_rows(filepath, reply_formatted)

    time.sleep(30)





#####################################################################################
# APPLICATION
#####################################################################################

def ai_gen(json_filepath, section, prompt):
    var_val = ''
    var_name = f'{section}_desc'

    data = util.json_read(json_filepath)

    try: var_val = data[var_name]
    except: data[var_name] = var_val
    if var_val != '': return

    reply = util_ai.gen_reply(prompt)
    # reply = util_ai.list_to_paragraph(reply)
    reply = util_ai.text_to_paragraph(reply)

    if reply != '':
        print('------------------------------')
        print(reply)
        print('------------------------------')
        print()
        data[var_name] = reply
        util.json_write(json_filepath, data)
        
    time.sleep(30)


def ai_problems_list(row):
    application = row[0].strip()
    application_a_1 = row[1]
    application_dash = application.lower().replace(' ', '-').replace("'", '-')

    article_filepath = f'articles/public/ozono/sanificazione/applicazioni/{application_dash}.json'
    content = util.file_read(article_filepath)
    if content.strip() == '': util.file_write(article_filepath, '{}')
    data = util.json_read(article_filepath)

    problems_list = ''
    try: problems_list = data['problems_list']
    except: data['problems_list'] = problems_list

    if problems_list != '': return

    prompt = f'''
        scrivi in italiano una lista di 10 problemi {application_a_1}{application.lower()} che la sanificazione ad ozono elimina.
        includi 2 batteri, 2 virus, 2 muffe, 2 parassiti e 2 odori.
        scrivi i problemi usando questa struttura: [nome problema]: [descrizione problema].
    '''
    reply = util_ai.gen_reply(prompt)
    reply = reply.strip()

    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if not line[0].isdigit(): continue
        if '. ' in line: line = '. '.join(line.split('. ')[1:]).strip()
        if len(line.split(' ')) < 10: continue
        reply_formatted.append(line)

    reply = reply.replace('\n', ' ')
    reply = re.sub("\s\s+" , " ", reply)

    if len(reply_formatted) == 10:
        print('------------------------------')
        print(reply_formatted)
        print('------------------------------')
        print()
        data['problems_list'] = reply_formatted
        util.json_write(article_filepath, data)

    time.sleep(30)


def ai_benefits_list(row):
    application = row[0].strip()
    application_a_1 = row[1]
    application_dash = application.lower().replace(' ', '-').replace("'", '-')

    article_filepath = f'articles/public/ozono/sanificazione/applicazioni/{application_dash}.json'
    content = util.file_read(article_filepath)
    if content.strip() == '': util.file_write(article_filepath, '{}')
    data = util.json_read(article_filepath)

    benefits_list = ''
    try: benefits_list = data['benefits_list']
    except: data['benefits_list'] = benefits_list

    if benefits_list != '': return

    prompt = f'''
        scrivi in italiano una lista di 10 benefici della sanificazione ad ozono {application_a_1}{application.lower()}.
        scrivi i problemi usando questa struttura: [nome benficio]: [descrizione beneficio].
    '''
    reply = util_ai.gen_reply(prompt)
    reply = reply.strip()

    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if not line[0].isdigit(): continue
        if '. ' in line: line = '. '.join(line.split('. ')[1:]).strip()
        if len(line.split(' ')) < 10: continue
        reply_formatted.append(line)

    reply = reply.replace('\n', ' ')
    reply = re.sub("\s\s+" , " ", reply)

    if len(reply_formatted) == 10:
        print('------------------------------')
        print(reply_formatted)
        print('------------------------------')
        print()
        data['benefits_list'] = reply_formatted
        util.json_write(article_filepath, data)

    time.sleep(30)


def ai_applications_list(row):
    application = row[0].strip()
    application_a_1 = row[1]
    application_dash = application.lower().replace(' ', '-').replace("'", '-')

    article_filepath = f'articles/public/ozono/sanificazione/applicazioni/{application_dash}.json'
    content = util.file_read(article_filepath)
    if content.strip() == '': util.file_write(article_filepath, '{}')
    data = util.json_read(article_filepath)

    applications_list = ''
    try: applications_list = data['applications_list']
    except: data['applications_list'] = applications_list

    if applications_list != '': return

    prompt = f'''
        scrivi in italiano una lista di 10 applicazioni della sanificazione ad ozono {application_a_1}{application.lower()}.
        scrivi i problemi usando questa struttura: [nome applicazione]: [descrizione applicazione].
    '''
    reply = util_ai.gen_reply(prompt)
    reply = reply.strip()

    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if not line[0].isdigit(): continue
        if '. ' in line: line = '. '.join(line.split('. ')[1:]).strip()
        if len(line.split(' ')) < 10: continue
        reply_formatted.append(line)

    reply = reply.replace('\n', ' ')
    reply = re.sub("\s\s+" , " ", reply)

    if len(reply_formatted) == 10:
        print('------------------------------')
        print(reply_formatted)
        print('------------------------------')
        print()
        data['applications_list'] = reply_formatted
        util.json_write(article_filepath, data)

    time.sleep(30)


def ai_applications_main():
    filepath = 'database/tables/applications.csv'
    rows = util.csv_get_rows(filepath)[1:]
    for i, row in enumerate(rows):
        print(f'{i+1}/{len(rows)} >>>> {row[0].strip()} | {row[2].strip()}')
        application_name = row[0].strip().lower()
        application_a_1 = row[1]
        application_category = row[2]
        application_slug = row[3]
        json_filepath = f'articles/public/ozono/sanificazione/settori/{application_category}/{application_slug}.json'

        if not os.path.exists(json_filepath):
            with open(json_filepath, 'a', encoding='utf-8') as f:
                f.write('')

        # ai_batteri_csv(row)
        # ai_virus_csv(row)
        # ai_muffe_csv(row)
        # ai_insetti_csv(row)
        # ai_odori_csv(row)

        # ai_benefici_csv(row)

        # INTRO
        for prompt in prompts.intro:
            prompt = prompt.replace('[application_a_1]', application_a_1)
            prompt = prompt.replace('[application_name]', application_name)
            ai_gen(json_filepath, 'intro', prompt)
            
        # DEFINITION
        for prompt in prompts.definition:
            prompt = prompt.replace('[application_a_1]', application_a_1)
            prompt = prompt.replace('[application_name]', application_name)
            ai_gen(json_filepath, 'definition', prompt)
            
        # PROBLEMS
        for prompt in prompts.problems:
            prompt = prompt.replace('[application_a_1]', application_a_1)
            prompt = prompt.replace('[application_name]', application_name)
            ai_gen(json_filepath, 'problems', prompt)
            
        # BENEFITS
        for prompt in prompts.benefits:
            prompt = prompt.replace('[application_a_1]', application_a_1)
            prompt = prompt.replace('[application_name]', application_name)
            ai_gen(json_filepath, 'benefits', prompt)
            
        # APPLICATIONS
        for prompt in prompts.applications:
            prompt = prompt.replace('[application_a_1]', application_a_1)
            prompt = prompt.replace('[application_name]', application_name)
            ai_gen(json_filepath, 'applications', prompt)

        # ai_problems_list(row)
        # ai_benefits_list(row)
        # ai_applications_list(row)


#####################################################################################
# APPLICATIONS PAGE
#####################################################################################

def ai_applications_page_descriptions():
    article_filepath = 'articles/public/ozono/sanificazione/applicazioni.json'
    # try: util.file_read()
    # except: util.file_append(article_filepath, '{}')

    data = util.json_read(article_filepath)

    json_applications = []
    try: json_applications = data['applications']
    except: data['applications'] = json_applications

    applications = [row[0] for row in util.csv_get_rows('database/tables/applications.csv')[1:]]
    applications_new = []
    for application in applications:
        application_name = application.strip().lower()
        found = False
        for json_application in json_applications:
            if application_name == json_application['application_name'].lower().strip():
                found = True
                applications_new.append(json_application)
                break

        if not found:
            applications_new.append({'application_name': application})

    data['applications'] = applications_new
    util.json_write(article_filepath, data)

    # APPLICATIONS DESCRIPTIONS
    data = util.json_read(article_filepath)
    for application_index, application in enumerate(data['applications']):
        application_name = application['application_name']
        application_name_dash = application_name.lower().replace(' ', '-').replace("'", '-')

        application_desc = ''
        try: application_desc = data['applications'][application_index]['application_desc']
        except: data['applications'][application_index]['application_desc'] = application_desc

        if application_desc != '': continue

        csv_application = util.csv_get_rows_by_entity(f'database/tables/applications.csv', application_name)[0]
        application_a_1 = csv_application[1]

        prompt_start = f'La sanificazione ad ozono {application_a_1}{application_name.lower()} viene principalmente utilizzata per '
        prompt = f'''
            Scrivi un paragrafo di 100 parole sulla sanificazione ad ozono per {application_a_1}{application}.
            Includi quali sono i problemi che risolve {application_a_1}{application_name.lower()}, i benefici che porta {application_a_1}{application_name.lower()} e le applicazioni che ha {application_a_1}{application_name.lower()}.
            Non spiegare cos'è l'ozono e non spiegare come funziona.
            Inizia la risposta con queste parole: {prompt_start}
        '''
        reply = util_ai.gen_reply(prompt)
        reply = reply.strip()
        reply = reply.replace('\n', ' ')
        reply = re.sub("\s\s+" , " ", reply)

        if reply != '':
            print('------------------------------')
            print(reply)
            print('------------------------------')
            print()
            data['applications'][application_index]['application_desc'] = reply
            util.json_write(article_filepath, data)

        time.sleep(30)



#####################################################################################
# SETTORE
#####################################################################################

def ai_sector():
    sectors_rows = util.csv_get_rows('database/tables/sectors.csv')[1:]
    for sector_row in sectors_rows:
        sector_name = sector_row[1]
        a_1 = sector_row[2]
        
        applications_rows = util.csv_get_rows_by_entity('database/tables/applications.csv', sector_name, col_num=2)
        applications_names = [row[0].lower() for row in applications_rows]
        applications_names_text = ', '.join(applications_names)
        
        for application in applications_names:
            print(application)
        
        json_filepath = f'database/articles/ozono/sanificazione/settori/{sector_name}.json'
        
        data = util.json_read(json_filepath)
        data['sector_name'] = sector_name
        data['applications_num'] = len(applications_names)
        data['title'] = f'{str(data["applications_num"])} applicazioni della sanificazione ad ozono nel settore {a_1}{sector_name.lower()}'
        util.json_write(json_filepath, data)
        print(len(applications_names))

        data = util.json_read(json_filepath)
        intro_desc = []
        try: intro_desc = data['intro_desc']
        except: data['intro_desc'] = intro_desc

        if intro_desc == []:
            prompt = f'''
                Scrivi un paragrafo di 100 parole facendo molti esempi delle applicazioni della sanificazione ad ozono nel settore {a_1}{sector_name}.
                Non spiegare cos'è e come funziona l'ozono.
                includi le seguenti applicazioni: {applications_names_text}.
                Inizia la tua risposta con le seguenti parole: L'ozono viene uato nel settore {a_1}{sector_name} per .
            '''
            reply = util_ai.gen_reply(prompt)
            reply = reply.replace('\n', ' ')
            reply = re.sub("\s\s+" , " ", reply)

            if reply != '':
                print('------------------------------')
                print(reply)
                print('------------------------------')
                print()
                data['intro_desc'] = reply
                util.json_write(json_filepath, data)

            time.sleep(30)

        applications_rows = util.csv_get_rows_by_entity('database/tables/applications.csv', sector_name, col_num=2)
        for row in applications_rows:
            print(row)
            application_name = row[0]
            a_1 = row[1]
            sector = row[2]
            slug = row[3]

            data = util.json_read(json_filepath)
            applications = []
            try: applications = data['applications']
            except: data['applications'] = applications

            found = False
            for application in applications:
                if application['slug'].strip().lower() == slug.strip().lower():
                    found = True

            if not found:
                prompt = f'''
                    Scrivi un paragrafo di 100 parole facendo molti esempi delle applicazioni della sanificazione ad ozono {a_1}{application_name.lower()}.
                    Non spiegare cos'è e come funziona l'ozono.
                    Comincia la tua risposta usando queste parole: La sanificazione ad ozono {a_1}{application_name.lower()} serve per 
                '''
                reply = util_ai.gen_reply(prompt)
                reply = reply.replace('\n', ' ')
                reply = re.sub("\s\s+" , " ", reply)

                if reply != '':
                    print('------------------------------')
                    print(reply)
                    print('------------------------------')
                    print()
                    data['applications'].append({'slug': slug, 'name': application_name, 'a_1': a_1, 'desc': reply})
                    util.json_write(json_filepath, data)

                time.sleep(30)


def ai_sectors():
    sector_rows = util.csv_get_rows('database/tables/applications.csv')[1:]
    sectors = [row[2] for row in sector_rows]
    sectors = list(dict.fromkeys(sectors))
    
    json_filepath = f'database/articles/ozono/sanificazione/settori.json'

    data = util.json_read(json_filepath)
    data['sectors_num'] = len(sectors)
    data['title'] = f'{str(data["sectors_num"])} settori di applicazione della sanificazione ad ozono'
    util.json_write(json_filepath, data)

    for sector in sectors:
        data = util.json_read(json_filepath)

        var_val = []
        var_name = 'sectors'
        try: var_val = data[var_name]
        except: data[var_name] = var_val

        found = False
        for sector_json in var_val:
            if sector_json['slug'].strip().lower() == sector.strip().lower():
                found = True

        if not found:
            prompt = f'''
                Scrivi un paragrafo di 100 parole facendo molti esempi delle applicazioni della sanificazione ad ozono nel settore {sector.lower()}.
                Non spiegare cos'è e come funziona l'ozono.
                Comincia la tua risposta usando queste parole: La sanificazione ad ozono nel settore {sector.lower()} serve per 
            '''
            reply = util_ai.gen_reply(prompt)
            reply = reply.replace('\n', ' ')
            reply = re.sub("\s\s+" , " ", reply)

            if reply != '':
                print('------------------------------')
                print(reply)
                print('------------------------------')
                print()
                data[var_name].append({'slug': sector, 'desc': reply})
                util.json_write(json_filepath, data)

            time.sleep(30)



# ai_sectors()


# ai_sector()

def ai_og_settori():
    applications_rows = util.csv_get_rows('database/tables/applications.csv')[1:]
    sectors = [row[2] for row in applications_rows]
    sectors = list(dict.fromkeys(sectors))
    
    json_filepath = f'database/pages/settori.json'

    data = util.json_read(json_filepath)
    data['sectors_num'] = len(sectors)
    data['title'] = f'I {str(data["sectors_num"])} settori principalmente serviti da Ozonogroup'
    util.json_write(json_filepath, data)

    for sector in sectors:
        var_val = []
        var_name = 'sectors'
        try: var_val = data[var_name]
        except: data[var_name] = var_val

        found = False
        for sector_json in var_val:
            if sector_json['slug'].strip().lower() == sector.strip().lower():
                found = True

        if not found:
            sector_row = util.csv_get_rows_by_entity('database/tables/sectors.csv', sector, col_num=1)[0]
            sector_name = sector_row[1]
            sector_a_1 = sector_row[2]

            applications_names = [row[0].lower() for row in applications_rows if row[2] == sector_name]
            applications_names_str = ', '.join(applications_names)
            prompt = f'''
                Scrivi in Italiano una lista di 3 elementi facendo esempi di alcune applicazioni della sanificazione ad ozono nel settore {sector_a_1}{sector_name}.
                Includi tutte queste applicazioni: {applications_names_str}.
                Usa il minor numero di parole possibili.
                Comincia ogni elemento della lista con un verbo azionabile.
                Comincia la tua risposta usando queste parole: Ozonogroup usa la sanificazione ad ozono nel settore {sector_a_1}{sector_name} principalmente per: .
            '''
            reply = util_ai.gen_reply(prompt)
            # reply = reply.replace('\n', ' ')
            # reply = re.sub("\s\s+" , " ", reply)

            lines = []
            for line in reply.split('\n'):
                line = line.strip()
                if line == '': continue

                if not line[0].isdigit(): continue
                if '. ' not in line: continue 
                
                line = '. '.join(line.split('. ')[1:])
                line.strip()

                lines.append(line)
                
            if len(lines) == 3:
                print('------------------------------')
                print(reply)
                print('------------------------------')
                print()
                data[var_name].append({'slug': sector_name, 'desc': lines})
                util.json_write(json_filepath, data)

            time.sleep(30)

ai_og_settori()

# json_applications_clear_field('definition')

# ai_applications_main()

# ai_applications_page_descriptions()
