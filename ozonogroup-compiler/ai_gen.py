from groq import Groq
import time
import re

import util

client = Groq(
    api_key='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',
)


def gen_reply(prompt):
    prompt_normalized = '\n'.join([line.strip() for line in prompt.split('\n') if line.strip() != ''])

    completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt_normalized,
            }
        ],
        model="mixtral-8x7b-32768",
    )

    reply = completion.choices[0].message.content
    print()
    print()
    print()
    print("Q:")
    print()
    print(prompt)
    print()
    print("A:")
    print()
    print(reply)
    print()
    return reply


def ai_intro_1(row):
    application = row[0].strip()
    application_a_1 = row[1]
    application_dash = application.lower().replace(' ', '-').replace("'", '-')

    article_filepath = f'articles/public/ozono/sanificazione/applicazioni-auto/{application_dash}.json'
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

    print(prompt_normalized)
    
    completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="mixtral-8x7b-32768",
    )

    print()
    reply = completion.choices[0].message.content
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

    article_filepath = f'articles/public/ozono/sanificazione/applicazioni-auto/{application_dash}.json'
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
    reply = gen_reply(prompt)
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

    article_filepath = f'articles/public/ozono/sanificazione/applicazioni-auto/{application_dash}.json'
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
    reply = gen_reply(prompt)
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

    article_filepath = f'articles/public/ozono/sanificazione/applicazioni-auto/{application_dash}.json'
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
    reply = gen_reply(prompt)
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

    article_filepath = f'articles/public/ozono/sanificazione/applicazioni-auto/{application_dash}.json'
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
    reply = gen_reply(prompt)
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

    article_filepath = f'articles/public/ozono/sanificazione/applicazioni-auto/{application_dash}.json'
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
    reply = gen_reply(prompt)
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

    article_filepath = f'articles/public/ozono/sanificazione/applicazioni-auto/{application_dash}.json'
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
    reply = gen_reply(prompt)
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

    article_filepath = f'articles/public/ozono/sanificazione/applicazioni-auto/{application_dash}.json'
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
    reply = gen_reply(prompt)
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

    article_filepath = f'articles/public/ozono/sanificazione/applicazioni-auto/{application_dash}.json'
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
    reply = gen_reply(prompt)
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


#####################################################################################
# APPLICATIONS PAGE
#####################################################################################

def ai_applications_descriptions():
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
    
ai_applications_descriptions()

#####################################################################################
# SINGLE APPLICATION
#####################################################################################

# filepath = 'database/tables/applications.csv'
# rows = util.csv_get_rows(filepath)[1:]
# for i, row in enumerate(rows):
#     print(f'{i+1}/{len(rows)}')
#     ai_intro_1(row)
#     ai_intro_2(row)
#     ai_definition(row)
#     ai_problems_text(row)
#     ai_problems_list(row)
#     ai_benefits_text(row)
#     ai_benefits_list(row)
#     ai_applications_text(row)
#     ai_applications_list(row)
    