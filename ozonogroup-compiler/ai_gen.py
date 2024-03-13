import time
import re

import util
import util_ai

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



#####################################################################################
# SINGLE APPLICATION
#####################################################################################


def ai_problems_mix_csv(row):
    pass
    # prompt = f'''
    #     Scrivi in italiano 5 liste.
    #     Nella lista 1, scrivi i nomi dei 10 batteri più presenti {application_a_1}{application_name.lower()}.
    #     Nella lista 2, scrivi i nomi dei 10 virus più presenti {application_a_1}{application_name.lower()}.
    #     Nella lista 3, scrivi i nomi delle 10 muffe più presenti {application_a_1}{application_name.lower()}.
    #     Nella lista 4, scrivi i nomi dei 10 insetti più presenti {application_a_1}{application_name.lower()}.
    #     Nella lista 5, scrivi i nomi dei 10 odori indesiderati più presenti {application_a_1}{application_name.lower()}.
    #     Lista solo i nomi, non aggiungere descrizioni.
    #     Aggiungi un titolo per ogni ogni lista.
    # '''
    # reply = util_ai.gen_reply(prompt)
    # reply = reply.strip()
    # time.sleep(30)
    




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






def batteri_to_json(row):
    problem_name = 'batteri'
    application_name = row[0].strip()
    application_a_1 = row[1]
    application_name_dash = application_name.lower().replace(' ', '-').replace("'", '-')

    filepath = f'database/tables/applicazioni-problemi-{problem_name}.csv'
    csv_rows = []
    try: csv_rows = util.csv_get_rows_by_entity(filepath, application_name_dash)
    except: util.csv_add_rows(filepath, [])
    if csv_rows == []: return

    problems = [csv_row[2] for csv_row in csv_rows]

    filepath = f'articles/public/ozono/sanificazione/applicazioni/{application_name_dash}.json'
    data = util.json_read(filepath)
    data[f'problemi_{problem_name}'] = problems
    util.json_write(filepath, data)


def virus_to_json(row):
    problem_name = 'virus'
    application_name = row[0].strip()
    application_a_1 = row[1]
    application_name_dash = application_name.lower().replace(' ', '-').replace("'", '-')

    filepath = f'database/tables/applicazioni-problemi-{problem_name}.csv'
    csv_rows = []
    try: csv_rows = util.csv_get_rows_by_entity(filepath, application_name_dash)
    except: util.csv_add_rows(filepath, [])
    if csv_rows == []: return

    problems = [csv_row[2] for csv_row in csv_rows]

    filepath = f'articles/public/ozono/sanificazione/applicazioni/{application_name_dash}.json'
    data = util.json_read(filepath)
    data[f'problemi_{problem_name}'] = problems
    util.json_write(filepath, data)


def muffe_to_json(row):
    problem_name = 'muffe'
    application_name = row[0].strip()
    application_a_1 = row[1]
    application_name_dash = application_name.lower().replace(' ', '-').replace("'", '-')

    filepath = f'database/tables/applicazioni-problemi-{problem_name}.csv'
    csv_rows = []
    try: csv_rows = util.csv_get_rows_by_entity(filepath, application_name_dash)
    except: util.csv_add_rows(filepath, [])
    if csv_rows == []: return

    problems = [csv_row[2] for csv_row in csv_rows]

    filepath = f'articles/public/ozono/sanificazione/applicazioni/{application_name_dash}.json'
    data = util.json_read(filepath)
    data[f'problemi_{problem_name}'] = problems
    util.json_write(filepath, data)


def insetti_to_json(row):
    problem_name = 'insetti'
    application_name = row[0].strip()
    application_a_1 = row[1]
    application_name_dash = application_name.lower().replace(' ', '-').replace("'", '-')

    filepath = f'database/tables/applicazioni-problemi-{problem_name}.csv'
    csv_rows = []
    try: csv_rows = util.csv_get_rows_by_entity(filepath, application_name_dash)
    except: util.csv_add_rows(filepath, [])
    if csv_rows == []: return

    problems = [csv_row[2] for csv_row in csv_rows]

    filepath = f'articles/public/ozono/sanificazione/applicazioni/{application_name_dash}.json'
    data = util.json_read(filepath)
    data[f'problemi_{problem_name}'] = problems
    util.json_write(filepath, data)


def odori_to_json(row):
    problem_name = 'odori'
    application_name = row[0].strip()
    application_a_1 = row[1]
    application_name_dash = application_name.lower().replace(' ', '-').replace("'", '-')

    filepath = f'database/tables/applicazioni-problemi-{problem_name}.csv'
    csv_rows = []
    try: csv_rows = util.csv_get_rows_by_entity(filepath, application_name_dash)
    except: util.csv_add_rows(filepath, [])
    if csv_rows == []: return

    problems = [csv_row[2] for csv_row in csv_rows]

    filepath = f'articles/public/ozono/sanificazione/applicazioni/{application_name_dash}.json'
    data = util.json_read(filepath)
    data[f'problemi_{problem_name}'] = problems
    util.json_write(filepath, data)



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






def ai_intro_1(row):
    application = row[0].strip()
    application_a_1 = row[1]
    application_dash = application.lower().replace(' ', '-').replace("'", '-')

    article_filepath = f'articles/public/ozono/sanificazione/applicazioni/{application_dash}.json'
    content = util.file_read(article_filepath)
    if content.strip() == '': util.file_write(article_filepath, '{}')
    data = util.json_read(article_filepath)

    intro_1 = ''
    try: intro_1 = data['intro_1']
    except: data['intro_1'] = ''

    if intro_1 != '': return

    prompt = f'''
        scrivi in italiano 1 paragrafo di 5 frasi corte in meno di 100 parole sui problemi di contaminazione microbiologica {application_a_1}{application}.
        includi i problemi di contaminazione più comuni, qual'è l'impatto globale e quali sono le ripercussioni.
        includi numeri, dati e statistiche senza nominare le sorgenti e gli studi.
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
        data['intro_1'] = reply
        util.json_write(article_filepath, data)
        
    time.sleep(30)


def ai_intro_2(row):
    application = row[0].strip()
    application_a_1 = row[1]
    application_dash = application.lower().replace(' ', '-').replace("'", '-')

    article_filepath = f'articles/public/ozono/sanificazione/applicazioni/{application_dash}.json'
    content = util.file_read(article_filepath)
    if content.strip() == '': util.file_write(article_filepath, '{}')
    data = util.json_read(article_filepath)

    intro_2 = ''
    try: intro_2 = data['intro_2']
    except: data['intro_2'] = ''

    if intro_2 != '': return

    prompt = f'''
        scrivi un paragrafo di 5 frasi in 100 parole spiegando come la sanificazione ad ozono risolve i problemi di contaminazione {application_a_1} {application}.
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
        data['intro_2'] = reply
        util.json_write(article_filepath, data)
        
    time.sleep(30)


def ai_definition(row):
    application = row[0].strip()
    application_a_1 = row[1]
    application_dash = application.lower().replace(' ', '-').replace("'", '-')

    article_filepath = f'articles/public/ozono/sanificazione/applicazioni/{application_dash}.json'
    content = util.file_read(article_filepath)
    if content.strip() == '': util.file_write(article_filepath, '{}')
    data = util.json_read(article_filepath)

    definition = ''
    try: definition = data['definition']
    except: data['definition'] = definition

    if definition != '': return

    prompt = f'''
        scrivi un paragrafo di 100 parole spiegando cos'è la sanificazione ad ozono per {application} e a cosa serve.
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
        data['definition'] = reply
        util.json_write(article_filepath, data)
        
    time.sleep(30)


def ai_problems_text(row):
    application = row[0].strip()
    application_a_1 = row[1]
    application_dash = application.lower().replace(' ', '-').replace("'", '-')

    article_filepath = f'articles/public/ozono/sanificazione/applicazioni/{application_dash}.json'
    content = util.file_read(article_filepath)
    if content.strip() == '': util.file_write(article_filepath, '{}')
    data = util.json_read(article_filepath)

    problems_text = ''
    try: problems_text = data['problems_text']
    except: data['problems_text'] = problems_text

    if problems_text != '': return

    prompt_start = f'La sanificazione ad ozono elimina diversi problemi {application_a_1}{application.lower()}, come '
    prompt = f'''
        scrivi un paragrafo di 100 parole spiegando quali problemi risolve la sanificazione ad ozono per {application}.
        includi nomi di batteri, virus, muffe, parassiti e odori.
        non spiegare cos'è l'ozono e non spiegare come funziona.
        inizia la risposta con queste parole: {prompt_start}
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
        data['problems_text'] = reply
        util.json_write(article_filepath, data)
            
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


def ai_benefits_text(row):
    application = row[0].strip()
    application_a_1 = row[1]
    application_dash = application.lower().replace(' ', '-').replace("'", '-')

    article_filepath = f'articles/public/ozono/sanificazione/applicazioni/{application_dash}.json'
    content = util.file_read(article_filepath)
    if content.strip() == '': util.file_write(article_filepath, '{}')
    data = util.json_read(article_filepath)

    benefits_text = ''
    try: benefits_text = data['benefits_text']
    except: data['benefits_text'] = benefits_text

    if benefits_text != '': return
    
    # TODO: vantaggi ozono su altri sanificanti
    prompt_start = f'La sanificazione ad ozono ha diversi benefici {application_a_1}{application.lower()}, come '
    prompt = f'''
        scrivi un paragrafo di 100 parole spiegando quali sono i benefici della sanificazione ad ozono per per {application}.
        non spiegare cos'è l'ozono e non spiegare come funziona.
        inizia la risposta con queste parole: {prompt_start}
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
        data['benefits_text'] = reply
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


def ai_applications_text(row):
    application = row[0].strip()
    application_a_1 = row[1]
    application_dash = application.lower().replace(' ', '-').replace("'", '-')

    article_filepath = f'articles/public/ozono/sanificazione/applicazioni/{application_dash}.json'
    content = util.file_read(article_filepath)
    if content.strip() == '': util.file_write(article_filepath, '{}')
    data = util.json_read(article_filepath)

    applications_text = ''
    try: applications_text = data['applications_text']
    except: data['applications_text'] = applications_text

    if applications_text != '': return
    
    prompt_start = f'La sanificazione ad ozono ha diverse applicazioni {application_a_1}{application.lower()}, come '
    prompt = f'''
        scrivi un paragrafo di 100 parole spiegando quali sono le applicazioni della sanificazione ad ozono {application_a_1}{application}.
        non spiegare cos'è l'ozono e non spiegare come funziona.
        inizia la risposta con queste parole: {prompt_start}
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
        data['applications_text'] = reply
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
        print(f'{i+1}/{len(rows)}')
        # ai_batteri_csv(row)
        # ai_virus_csv(row)
        # ai_muffe_csv(row)
        # ai_insetti_csv(row)
        ai_odori_csv(row)

        # batteri_to_json(row)
        # virus_to_json(row)
        # muffe_to_json(row)
        # insetti_to_json(row)
        odori_to_json(row)

        # ai_benefici_csv(row)
        
        # ai_intro_1(row)
        # ai_intro_2(row)
        # ai_definition(row)
        # ai_problems_text(row)
        # ai_problems_list(row)
        # ai_benefits_text(row)
        # ai_benefits_list(row)
        # ai_applications_text(row)
        # ai_applications_list(row)

  
ai_applications_main()

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





# ai_applications_page_descriptions()



