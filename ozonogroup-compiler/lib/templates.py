import os
import json

from lib import components

header = components.header()
footer = components.footer()

vault_folderpath = f'/home/ubuntu/vault'

def homepage_section_1():
    # image_filepath = f'/immagini-statiche/sanificazione-ozono-salva-ambiente-artico.png'
    # text_color = 'text-black'
    # opacity = 0.0 
    image_filepath = f'/immagini-statiche/ozono-protegge-terra.png'
    text_color = 'text-white'
    opacity = 0.3
    card = f'bg-white px-48'
    card = f''
    html = f'''
        <section class="h-70v" style="background-image: linear-gradient(rgba(0, 0, 0, {opacity}), rgba(0, 0, 0, {opacity})), url({image_filepath}); background-size: cover; background-position: center;">
            <div class="container-xl h-full flex items-center">
                <div class="flex-3 {card}">
                    <h2 class="{text_color} text-96 font-normal mb-16">Sanifica con l'Ozono, Salva l'Ambiente</h2>
                    <p class="{text_color} text-18 font-normal">Disinfetta i tuoi ambienti e prodotti da batteri, virus, muffe e altri contaminanti in modo efficace e veloce grazie all'ozono, senza lasciare residui chimici tossici per te stesso e l'ecosistema.</p>
                    <a class="button-1-fill" href="/">Prenota Consulenza</a>
                </div>
                <div class="flex-1">
                </div>
            </div>
        </section>
    '''
    return html

def homepage_section_2():
    html = f'''
        <section class="py-96">
            <div class="container-xl flex flex-col items-center">
                <h2 class="text-black text-36 text-center mb-16">Ozonogroup è un produttore di sistemi di sanificazione ad ozono ecologici per applicazioni industriali</h2>
                <p class="container-lg text-center mb-32">Con i sistemi di sanificazione di Ozonogroup risolvi problemi di contaminazione microbica e rimuovi gli agenti patogeni dannosi per la salute umana, animale e ambientale.</p>
                <div class="grid grid-3 gap-32">
                    <div class="relative">
                        <img src="/immagini-statiche/batteri.png">
                        <div class="absolute bottom-0 p-16 bg-black w-75p">
                            <h3 class="text-white mb-8">Batteri</h3>
                            <p class="text-white text-14">Ozonogroup elimina batteri come E. coli, Legionella e Salmonella.</p>
                        </div>
                    </div>
                    <div class="relative">
                        <img src="/immagini-statiche/virus.png">
                        <div class="absolute bottom-0 p-16 bg-black w-75p">
                            <h3 class="text-white mb-8">Virus</h3>
                            <p class="text-white text-14">Ozonogroup inattiva virus come Norovirus, Rotovirus e Adenovirus.</p>
                        </div>
                    </div>
                    <div class="relative">
                        <img src="/immagini-statiche/muffe.png">
                        <div class="absolute bottom-0 p-16 bg-black w-75p">
                            <h3 class="text-white mb-8">Muffe</h3>
                            <p class="text-white text-14">Ozonogroup disgrega muffe come Aspergillus, Fusarium e Trichoderma.</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    '''
    # <a class="button-1 inline-block" href="/">Scopri Tutti i Nostri Servizi</a>
    return html

def homepage_section_3():
    image_filepath = f'/immagini-statiche/ecosistema.png'
    text_color = 'text-black'
    opacity = 0.0
    card = f'bg-white px-24 py-48'
    # card = f''
    html = f'''
        <section class="h-80v py-64" style="background-image: linear-gradient(rgba(0, 0, 0, {opacity}), rgba(0, 0, 0, {opacity})), url({image_filepath}); background-size: cover; background-position: center;">
            <div class="container-xl h-full flex items-center">
                <div class="flex-4">
                </div>
                <div class="flex-3 {card}">
                    <h2 class="{text_color} text-30 font-bold mb-16 text-center">Perche disinfettare con l'ozono?</h2>
                    <p class="{text_color} text-18 font-normal text-center">L'ozono fornito da Ozonogroup permette di raggiungere i piu alti stadard di sanificazione in modo ecologico, rapido e a basso consumo energetico.</p>
                </div>
            </div>
        </section>
    '''
    return html

def homepage_section_4():
    html = f'''
        <section class="py-96">
            <div class="container-xl flex flex-col items-center">
                <div class="grid grid-2 gap-64 mb-48 items-center">
                    <img src="/immagini-statiche/ecologia.png" class="object-cover">
                    <div>
                        <h3 class="mb-8">Sanifica in modo ecologico</h3>
                        <p class="text-18">L'ozono e un gas 100% naturale e non lascia residui dannosi per l'ambiente, al contrario dei prodotti chimici. Infatti, questo gas e composto solamente da molecole di ossigeno (O3), le quali si trasformano in molecole di ossigno respirabile (O2) alla fine del trattamento. Di conseguenza, lascia 0 residuo di ozono in ambienti e prodotti, evitando anche i costi di smaltimento e i danni recati al pianeta.</p>
                    </div>
                </div>
                <div class="grid grid-2 gap-64 items-center">
                    <div>
                        <h3 class="mb-8">Risparmia energia e costi</h3>
                        <p class="text-18">La tecnologia Ozonogroup sfrutta l'effetto Aurora per produrre elevate quanita di ozono con poca energia. Grazie a questa nostra tecnologia puoi risparmiare fino a 10 volte sui costi dei prodotti chimici e fino a 100 volte sui costi the sistemi termici. In piu, funziona a bassa pressione e temperatura, nonche e resistente all'usura e la manutenzione risulta facile e veloce.</p>
                    </div>
                    <img src="/immagini-statiche/energia.png" class="object-cover">
                </div>
            </div>
        </section>
    '''
    return html

def homepage_section_5():
    image_filepath = f'/immagini-statiche/ozonogroup.png'
    text_color = 'text-black'
    opacity = 0.0
    card = f'bg-white px-32 py-48'
    # card = f''
    html = f'''
        <section class="h-80v py-64" style="background-image: linear-gradient(rgba(0, 0, 0, {opacity}), rgba(0, 0, 0, {opacity})), url({image_filepath}); background-size: cover; background-position: center;">
            <div class="container-xl h-full flex items-center">
                <div class="flex-1 {card}">
                    <h2 class="{text_color} text-30 font-bold mb-16">Perche Scegliere Ozonogroup?</h2>
                    <p class="{text_color} text-18 font-normal">Ozonogroup progetta sistemi di sanificazione su misura per le tue necessita, garantendoti la massima efficacia al minimo costo. Inoltre, hai la sicurezza di una sanificazione efficace dato che l'installazione viene eseguita da noi (grazie ai nostri tecnici specializzati) e che le attrezzature vengono regolarmente manutenzionate.</p>
                </div>
                <div class="flex-1">
                </div>
            </div>
        </section>
    '''
    return html

def homepage_section_servizi_2():
    html = f'''
        <section class="py-96">
            <div class="container-xl flex flex-col items-center">
                <div class="grid grid-3 gap-32 mb-32">
                    <div>
                        <img class="mb-16" src="/immagini-statiche/progettazione.png">
                        <h3 class="mb-8">Progettazione</h3>
                        <p class="">Ozongroup analizza la tua richista e progetta il sistema di sanficazionead ozono migliore per te. Chiamaci per fissare un appuntamento telefonico conoscitivo (consulenza gratuita), per esporci le tue necessita. Assieme a te valuteremo se la sanificazione ad ozono e il sistema giusto per te o no.</p>
                    </div>
                    <div>
                        <img class="mb-16" src="/immagini-statiche/installazione.png">
                        <h3 class="mb-8">Installazione</h3>
                        <p class="">Ozonogroup provvede all'installazione, avvio e collaudo del sistema. I nostri tecnici consegnano personalmente le apparecchiature di disinfezione nella tua azienda. Tutto quello che devi fare e concordare con noi la data dell'installazione e comunicarci il nome del responsabile che ci accoglie e supervisiona.</p>
                    </div>
                    <div>
                        <img class="mb-16" src="/immagini-statiche/manutenzione.png">
                        <h3 class="mb-8">Manutenzione</h3>
                        <p class="">Ozongroup manutenziona periodicamente le apparecchiature che producono ozono, in modo da garantire la massima efficienza. Ci occupiamo anche di riparazioni i caso di rottura o malfunzionamento, se mai dovesse succedere. Contattaci per ogni evenienza e agiremo il prima possible.</p>
                    </div>
                </div>
            </div>
        </section>
    '''
    # <a class="button-1 inline-block" href="/">Scopri Tutti i Nostri Servizi</a>
    return html

def homepage_section_8():
    image_filepath = f'/immagini-statiche/ambiente.png'
    text_color = 'text-black'
    opacity = 0.0
    card = f'bg-white px-24 py-48'
    # card = f''
    html = f'''
        <section class="h-80v py-64" style="background-image: linear-gradient(rgba(0, 0, 0, {opacity}), rgba(0, 0, 0, {opacity})), url({image_filepath}); background-size: cover; background-position: center;">
            <div class="container-xl h-full flex items-center">
                <div class="flex-1 {card}">
                    <h2 class="{text_color} text-30 font-bold mb-16 text-center">L'impegno di Ozonogroup nella salvaguardia dell'ambiente</h2>
                    <p class="{text_color} text-18 font-normal text-center">Disinfetta i tuoi ambienti e prodotti da batteri, virus, muffe e altri contaminanti in modo efficace e veloce grazie all'ozono, senza lasciare residui chimici tossici per te stesso e l'ecosistema.</p>
                </div>
                <div class="flex-1">
                </div>
            </div>
        </section>
    '''
    return html

def homepage_section_settori_1():
    image_filepath = f'/immagini-statiche/settori.png'
    text_color = 'text-black'
    opacity = 0.0
    card = f'bg-white px-48 py-48'
    # card = f''
    html = f'''
        <section class="h-80v py-64" style="background-image: linear-gradient(rgba(0, 0, 0, {opacity}), rgba(0, 0, 0, {opacity})), url({image_filepath}); background-size: cover; background-position: center;">
            <div class="container-xl h-full flex items-center">
                <div class="flex-1">
                </div>
                <div class="flex-1 {card}">
                    <h2 class="{text_color} text-30 font-bold mb-16">Con Chi Lavoriamo?</h2>
                    <p class="{text_color} text-18 font-normal">Ozonogroup non e per tutti. Lavoriamo principalmente con aziende e industrie nel settore dell'agricolura, della lavorazione alimenare, del benessere e dell'ospitalita (ma ance altri). Inoltre, serviamo solo clienti che vogliono la nostra tecnologia ad ozono perche hanno a cuore la salute dei loro dipendenti e dell'intero ecosistema, ovvero lavoraimo con clienti che sono in linea con la nostra missione aziendale.</p>
                </div>
            </div>
        </section>
    '''
    return html

def homepage_section_settori_2():
    html = f'''
        <section class="py-96">
            <div class="container-xl">
                <h2 class="text-black text-30 font-bold mb-32">Settori Serviti Da Ozonogrpup</h2>
                <div class="grid grid-4">
                    <div>
                        <img src="/immagini-statiche/agricoltura.png">
                    </div>
                    <div>
                    </div>
                    <div>
                        <img src="/immagini-statiche/alimentare.png">
                    </div>
                    <div>
                    </div>

                    <div>
                    </div>
                    <div>
                        <img src="/immagini-statiche/benessere.png">
                    </div>
                    <div>
                    </div>
                    <div>
                        <img src="/immagini-statiche/accoglienza.png">
                    </div>
                </div>
            </div>
        </section>
    '''
    return html

def get_month_name_from_val(num):
    month_name = ''
    if num == 1: month_name = 'Gen'
    elif num == 2: month_name = 'Feb'
    elif num == 3: month_name = 'Mar'
    elif num == 4: month_name = 'Apr'
    elif num == 5: month_name = 'Mag'
    elif num == 6: month_name = 'Giu'
    elif num == 7: month_name = 'Lug'
    elif num == 8: month_name = 'Ago'
    elif num == 9: month_name = 'Set'
    elif num == 10: month_name = 'Ott'
    elif num == 11: month_name = 'Nov'
    elif num == 12: month_name = 'Dic'
    return month_name

def homepage_section_9():
    news = []

    folderpath_in = f'{vault_folderpath}/ozonogroup/news/done'
    filenames_in = os.listdir(folderpath_in)
    objects = []
    for filename_in in filenames_in:
        filepath_in = f'{folderpath_in}/{filename_in}'
        with open(filepath_in) as f: data = json.load(f)
        date = data['year'] + '/' + data['month'] + '/' + data['day']
        obj = {
            'filename': filename_in,
            'date': date,
        }
        objects.append(obj)
    objects = sorted(objects, key=lambda x: x['date'], reverse=True)

    for obj_i, obj in enumerate(objects):
        filename_in = obj['filename']
        filepath_in = f'{folderpath_in}/{filename_in}'
        with open(filepath_in) as f: data = json.load(f)

        article_id = data['id']
        article_year = data['year']
        article_month = data['month']
        article_day = int(data['day'])
        article_month_name = get_month_name_from_val(int(article_month))
        article_date_str = f'{article_month_name} {article_day}, {article_year}'
        article_category = data['category'].lower().strip()
        article_slug = data['slug'].lower().strip()
        article_title = data['title']
        article_paragraphs = data['body']
        article_content = ' '.join(article_paragraphs)
        article_word_num = len(article_content.split(' '))
        article_time = article_word_num // 100
        article_desc = ' '.join(article_paragraphs[0].split(' ')[:16]) + '...'
        article_desc_md = ' '.join(article_paragraphs[0].split(' ')[:24]) + '...'
        article_desc_lg = ' '.join(article_paragraphs[0].split(' ')[:32]) + '...'

        news.append({
            'title': article_title,
            'date': article_date_str,
            'image': article_slug,
            'desc': article_desc,
            'desc_md': article_desc_md,
            'desc_lg': article_desc_lg,
        })

    print(news[0])

    news_html = ''
    for obj_i, obj in enumerate(news[:15]):
        news_html += f'''
            <div>
                <img class="mb-16" src="/immagini/news/{news[obj_i]['image']}.jpg">
                <h3 class="text-20 mb-8">{news[obj_i]['title']}</h3>
            </div>
        '''
        

    html = f'''
        <section class="py-96">
            <div class="container-xl flex flex-col items-center">
                <h2 class="text-black text-36 text-center mb-16">Guide sull'Ozono</h2>
                <p class="container-lg text-center mb-32">Con i sistemi di sanificazione di Ozonogroup risolvi problemi di contaminazione microbica e rimuovi gli agenti patogeni dannosi per la salute umana, animale e ambientale.</p>
                <div class="grid grid-3 gap-32 mb-32">
                    {news_html}
                </div>
            </div>
        </section>
    '''
    return html

def homepage():
    html = f'''
        <!DOCTYPE html>
        <html lang="en">

        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="/style.css">
            <title>Sanifica con l'Ozone per Salvare l'Ambiente | Ozonogroup</title>
            [gtag]
        </head>

        <body>

            {header}
            <main>

                {homepage_section_1()}
                {homepage_section_2()}
                {homepage_section_3()}
                {homepage_section_4()}
                {homepage_section_5()}
                {homepage_section_servizi_2()}
                {homepage_section_settori_1()}
                {homepage_section_settori_2()}
                {homepage_section_8()}
                {homepage_section_9()}
                
            </main>
            {footer}
            
        </body>

        </html>
    '''
    return html
