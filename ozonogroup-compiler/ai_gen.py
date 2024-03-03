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


def gen(row):
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


filepath = 'database/tables/applications.csv'
rows = util.csv_get_rows(filepath)[1:]
for row in rows:
    # gen(row)
    ai_intro_2(row)
    