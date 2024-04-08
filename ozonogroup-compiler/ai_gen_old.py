

# def batteri_to_json(row):
#     problem_name = 'batteri'
#     application_name = row[0].strip()
#     application_a_1 = row[1]
#     application_name_dash = application_name.lower().replace(' ', '-').replace("'", '-')

#     filepath = f'database/tables/applicazioni-problemi-{problem_name}.csv'
#     csv_rows = []
#     try: csv_rows = util.csv_get_rows_by_entity(filepath, application_name_dash)
#     except: util.csv_add_rows(filepath, [])
#     if csv_rows == []: return

#     problems = [csv_row[2] for csv_row in csv_rows]

#     filepath = f'articles/public/ozono/sanificazione/applicazioni/{application_name_dash}.json'
#     data = util.json_read(filepath)
#     data[f'problemi_{problem_name}'] = problems
#     util.json_write(filepath, data)


# def virus_to_json(row):
#     problem_name = 'virus'
#     application_name = row[0].strip()
#     application_a_1 = row[1]
#     application_name_dash = application_name.lower().replace(' ', '-').replace("'", '-')

#     filepath = f'database/tables/applicazioni-problemi-{problem_name}.csv'
#     csv_rows = []
#     try: csv_rows = util.csv_get_rows_by_entity(filepath, application_name_dash)
#     except: util.csv_add_rows(filepath, [])
#     if csv_rows == []: return

#     problems = [csv_row[2] for csv_row in csv_rows]

#     filepath = f'articles/public/ozono/sanificazione/applicazioni/{application_name_dash}.json'
#     data = util.json_read(filepath)
#     data[f'problemi_{problem_name}'] = problems
#     util.json_write(filepath, data)


# def muffe_to_json(row):
#     problem_name = 'muffe'
#     application_name = row[0].strip()
#     application_a_1 = row[1]
#     application_name_dash = application_name.lower().replace(' ', '-').replace("'", '-')

#     filepath = f'database/tables/applicazioni-problemi-{problem_name}.csv'
#     csv_rows = []
#     try: csv_rows = util.csv_get_rows_by_entity(filepath, application_name_dash)
#     except: util.csv_add_rows(filepath, [])
#     if csv_rows == []: return

#     problems = [csv_row[2] for csv_row in csv_rows]

#     filepath = f'articles/public/ozono/sanificazione/applicazioni/{application_name_dash}.json'
#     data = util.json_read(filepath)
#     data[f'problemi_{problem_name}'] = problems
#     util.json_write(filepath, data)


# def insetti_to_json(row):
#     problem_name = 'insetti'
#     application_name = row[0].strip()
#     application_a_1 = row[1]
#     application_name_dash = application_name.lower().replace(' ', '-').replace("'", '-')

#     filepath = f'database/tables/applicazioni-problemi-{problem_name}.csv'
#     csv_rows = []
#     try: csv_rows = util.csv_get_rows_by_entity(filepath, application_name_dash)
#     except: util.csv_add_rows(filepath, [])
#     if csv_rows == []: return

#     problems = [csv_row[2] for csv_row in csv_rows]

#     filepath = f'articles/public/ozono/sanificazione/applicazioni/{application_name_dash}.json'
#     data = util.json_read(filepath)
#     data[f'problemi_{problem_name}'] = problems
#     util.json_write(filepath, data)


# def odori_to_json(row):
#     problem_name = 'odori'
#     application_name = row[0].strip()
#     application_a_1 = row[1]
#     application_name_dash = application_name.lower().replace(' ', '-').replace("'", '-')

#     filepath = f'database/tables/applicazioni-problemi-{problem_name}.csv'
#     csv_rows = []
#     try: csv_rows = util.csv_get_rows_by_entity(filepath, application_name_dash)
#     except: util.csv_add_rows(filepath, [])
#     if csv_rows == []: return

#     problems = [csv_row[2] for csv_row in csv_rows]

#     filepath = f'articles/public/ozono/sanificazione/applicazioni/{application_name_dash}.json'
#     data = util.json_read(filepath)
#     data[f'problemi_{problem_name}'] = problems
#     util.json_write(filepath, data)




# def ai_intro_1(row):
#     application = row[0].strip()
#     application_a_1 = row[1]
#     application_dash = application.lower().replace(' ', '-').replace("'", '-')

#     article_filepath = f'articles/public/ozono/sanificazione/applicazioni/{application_dash}.json'
#     content = util.file_read(article_filepath)
#     if content.strip() == '': util.file_write(article_filepath, '{}')
#     data = util.json_read(article_filepath)

#     intro_1 = ''
#     try: intro_1 = data['intro_1']
#     except: data['intro_1'] = ''

#     if intro_1 != '': return

#     prompt = f'''
#         scrivi in italiano 1 paragrafo di 5 frasi corte in meno di 100 parole sui problemi di contaminazione microbiologica {application_a_1}{application}.
#         includi i problemi di contaminazione più comuni, qual'è l'impatto globale e quali sono le ripercussioni.
#         includi numeri, dati e statistiche senza nominare le sorgenti e gli studi.
#     '''
    
#     reply = util_ai.gen_reply(prompt)
#     reply = reply.strip()
#     reply = reply.replace('\n', ' ')
#     reply = re.sub("\s\s+" , " ", reply)

#     if reply != '':
#         print('------------------------------')
#         print(reply)
#         print('------------------------------')
#         print()
#         data['intro_1'] = reply
#         util.json_write(article_filepath, data)
        
#     time.sleep(30)


# def ai_intro_2(row):
#     application = row[0].strip()
#     application_a_1 = row[1]
#     application_dash = application.lower().replace(' ', '-').replace("'", '-')

#     article_filepath = f'articles/public/ozono/sanificazione/applicazioni/{application_dash}.json'
#     content = util.file_read(article_filepath)
#     if content.strip() == '': util.file_write(article_filepath, '{}')
#     data = util.json_read(article_filepath)

#     intro_2 = ''
#     try: intro_2 = data['intro_2']
#     except: data['intro_2'] = ''

#     if intro_2 != '': return

#     prompt = f'''
#         scrivi un paragrafo di 5 frasi in 100 parole spiegando come la sanificazione ad ozono risolve i problemi di contaminazione {application_a_1} {application}.
#     '''
#     reply = util_ai.gen_reply(prompt)
#     reply = reply.strip()
#     reply = reply.replace('\n', ' ')
#     reply = re.sub("\s\s+" , " ", reply)

#     if reply != '':
#         print('------------------------------')
#         print(reply)
#         print('------------------------------')
#         print()
#         data['intro_2'] = reply
#         util.json_write(article_filepath, data)
        
#     time.sleep(30)




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
