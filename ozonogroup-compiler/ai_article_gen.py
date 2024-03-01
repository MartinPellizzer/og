import util

application = 'bed and breakfast'
application_article = 'nei'
application_dash = application.replace(' ', '-')
title = f'Sanificazione Ozono Per Bed And Breakfast'

def article_init():
    applications_folder = 'articles/public/ozono/sanificazione/applicazioni'

    filepath = f'{applications_folder}/{application_dash}.md'
    util.file_append(filepath, '')
    content = util.file_read(filepath)

    content = content.strip()

    if content != '': return

    content = ''
    content += f"---\n"
    content += f"title: {title}\n"
    content += f"---\n\n"
    content += f"# Sanificazione ad ozono per {application}: cos'è, problemi, benefici e applicazioni\n\n"
    content += f"![Ozono Sanificazione {application.title()}](/assets/images/ozono-sanificazione-{application_dash}.jpg)\n\n"
    content += f"<!-- content -->\n\n"
    content += f"In questo articolo viene descritto nel dettaglio cos'è la sanificazione ad ozono per {application}, a cosa serve, quali problemi risolve, quali benefici porta e quali sono le sue applicazioni.\n\n"
    content += f"## Cos'è la sanificazione ad ozono per {application} e a cosa serve?\n\n"
    content += f"<!-- content -->\n\n"
    content += f"![Ozono Sanificazione {application.title()} Definizione](/assets/images/ozono-sanificazione-{application_dash}-definizione.jpg)\n\n"
    content += f"## Quali problemi risolve la sanificazione ad ozono per {application}?\n\n"
    content += f"<!-- content -->\n\n"
    content += f"![Ozono Sanificazione {application.title()} Problemi](/assets/images/ozono-sanificazione-{application_dash}-problemi.jpg)\n\n"
    content += f"La seguente lista elenca i problemi principali di contaminazione che l'ozono può risolvere {application_article} {application}.\n\n- Batteri\n- Virus\n- Muffe\n- Parassiti\n- Odori\n\n"
    content += f"### Batteri\n\n"
    content += f"<!-- content -->\n\n"
    content += f"I batteri più comuni presenti {application_article} {application} che si possono eliminare con l'ozono sono elencati nella seguente lista.\n\n"
    content += f"<!-- list -->\n\n"
    content += f"### Virus\n\n"
    content += f"<!-- content -->\n\n"
    content += f"I virus più comuni presenti {application_article} {application} che si possono inattivare con l'ozono sono elencati nella seguente lista.\n\n"
    content += f"<!-- list -->\n\n"
    content += f"### Muffe\n\n"
    content += f"<!-- content -->\n\n"
    content += f"Le muffe più comuni presenti {application_article} {application} che si possono ossidare con l'ozono sono elencati nella seguente lista.\n\n"
    content += f"<!-- list -->\n\n"
    content += f"### Parassiti\n\n"
    content += f"<!-- content -->\n\n"
    content += f"I parassiti più comuni presenti {application_article} {application} che si possono repellere con l'ozono sono elencati nella seguente lista.\n\n"
    content += f"<!-- list -->\n\n"
    content += f"### Odori\n\n"
    content += f"<!-- content -->\n\n"
    content += f"Gli odori più comuni presenti {application_article} {application} che si possono disgregare con l'ozono sono elencati nella seguente lista.\n\n"
    content += f"<!-- list -->\n\n"
    content += f"## Quali sono i benefici della sanificazione ad ozono per {application}?\n\n"
    content += f"<!-- content -->\n\n"
    content += f"![Ozono Sanificazione {application.title()} Benefici](/assets/images/ozono-sanificazione-{application_dash}-benefici.jpg)\n\n"
    content += f"La seguente lista elenca i principali benefici della sanificazione ad ozono per {application}.\n\n"
    content += f"<!-- list -->\n\n"
    content += f"## Quali sono le applicazioni della sanificazione ad ozono per {application}?\n\n"
    content += f"<!-- content -->\n\n"
    content += f"![Ozono Sanificazione {application.title()} Applicazioni](/assets/images/ozono-sanificazione-{application_dash}-applicazioni.jpg)\n\n"
    content += f"Qui sotto trovi una lista dettagliata delle principali applicazioni della sanificazione ad ozono {application_article} {application}.\n\n"
    content += f"<!-- list -->\n\n"
    content += f"\n\n"

    util.file_write(filepath, content)



def article_prompt():

    print(f'''
===================================================================
INTRO
===================================================================

scrivi un paragrafo di 5 frasi in 100 parole sui problemi di contaminazione microbiologica {application_article} {application}.
includi quali sono i problemi di contaminazione più comuni e dannosi.
includi qual'è l'impatto globale di questi problemi.
includi quali sono le ripercussioni di questi problemi.
includi numeri, dati e statistiche.

-------------------------------------------------------------------
    ''')

    print(f'''
scrivi un paragrafo di 5 frasi in 100 parole spiegando come la sanificazione ad ozono risolve i problemi di contaminazione {application_article} {application}.

-------------------------------------------------------------------
    ''')

    
    
    print(f'''
===================================================================
DEFINIZIONE
===================================================================

scrivi un paragrafo di 5 frasi in 100 parole su cos'è la sanificazione ad ozono per {application} e a cosa serve.

-------------------------------------------------------------------
    ''')



    print(f'''
===================================================================
PROBLEMI
===================================================================

scrivi 5 liste.

nella lista 1, scrivi i batteri più comuni e problematici presenti {application_article} {application}. 
nella lista 2, scrivi i virus più comuni e problematici presenti {application_article} {application}. 
nella lista 3, scrivi i muffe più comuni e problematici presenti {application_article} {application}. 
nella lista 4, scrivi i parassiti più comuni e problematici presenti {application_article} {application}. 
nella lista 5, scrivi gli odori più comuni e problematici presenti {application_article} {application}. 

ordina i patogeni delle liste dal più frequente a qello meno frequente. dammi sono i nomi, non aggiungere descrizioni.

-------------------------------------------------------------------
    ''')

    print(f'''
scrivi 5 frasi.

nella frase 1, spiega che l'ozono sanifica i batteri tipici {application_article} {application} e includi esempi.
nella frase 2, spiega che l'ozono sanifica i virus tipici {application_article} {application} e includi esempi.
nella frase 3, spiega che l'ozono sanifica le muffe tipiche {application_article} {application} e includi esempi.
nella frase 4, spiega che l'ozono sanifica i parassiti tipici {application_article} {application} e includi esempi.
nella frase 5, spiega che l'ozono sanifica gli tipici {application_article} {application} e includi esempi.

inizia le frasi con le seguenti parole: L'ozono sanifica 

-------------------------------------------------------------------
    ''')

    print(f'''
scrivi un paragrafo di 5 righe che riassuma il seguente testo:

[insert all content of the "problem section" here]

-------------------------------------------------------------------
    ''')



    print(f'''
===================================================================
BENEFICI
===================================================================

scrivi una lista dei benefici della sanificazione ad ozono per {application}. 

-------------------------------------------------------------------
    ''')

    print(f'''
scrivi un paragrafo di 5 frasi in 100 paraole sui benefici della sanificazione ad ozono per {application}.

-------------------------------------------------------------------
    ''')



    print(f'''
===================================================================
APPLICAZIONI
===================================================================

lista le applicazioni della sanificazione ad ozono per {application}.

-------------------------------------------------------------------
    ''')

    print(f'''
scrivi un paragrafo di 5 frasi in 100 parole sulle applicazioni della sanificazione ad ozono per {application}. 

-------------------------------------------------------------------
    ''')



article_init()
article_prompt()

