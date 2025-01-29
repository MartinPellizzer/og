import shutil
from nltk import tokenize

from oliark_io import file_read, file_write
from oliark_io import json_read, json_write
from oliark_llm import llm_reply

AUTHOR_NAME = 'Martin Pellizzer'
vault_tmp = '/home/ubuntu/vault-tmp'
model = f'{vault_tmp}/llms/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf'

library_folderpath = f'/home/ubuntu/proj/og/studies/library'

vertices_contaminazioni = json_read('vertices.json')

GOOGLE_TAG = ''' 
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-TV11JVJVKC"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-TV11JVJVKC');
    </script>
'''

def text_format_1N1_html(text):
    text_formatted = ''
    text = text.replace('var.', 'var,')
    lines_tmp = tokenize.sent_tokenize(text)
    lines = []
    for line in lines_tmp:
        line = line.replace('var,', 'var.')
        lines.append(line)
    lines_num = len(lines[1:-1])
    paragraphs = []
    if lines_num > 0: 
        paragraphs.append(lines[0])
    else:
        text_formatted += f'<p>{text}.</p>' + '\n'
        text_formatted = text_formatted.replace('..', '.')
        return text_formatted
    if lines_num > 3: 
        paragraphs.append('. '.join(lines[1:lines_num//2+1]))
        paragraphs.append('. '.join(lines[lines_num//2+1:-1]))
    else:
        paragraphs.append('. '.join(lines[1:-1]))
    paragraphs.append(lines[-1])
    for paragraph in paragraphs:
        if paragraph.strip() != '':
            text_formatted += f'<p>{paragraph}.</p>' + '\n'
    text_formatted = text_formatted.replace('..', '.')
    return text_formatted

def head_html_generate(title, css_filepath):
    head_html = f'''
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="author" content="{AUTHOR_NAME}">
            <link rel="stylesheet" href="{css_filepath}">
            <title>{title}</title>
        </head>
    '''
    return head_html

                # <h1>Il Futuro Della Sanificazione Ecologica Nell'Industria Alimentare</h1>
section_00 = f'''
    <section class="home_hero_section">
        <div class="container-xl flex items-center h-80vh">
            <div class="flex-3">
                <h1>Disinfezione Veloce ed Ecologica (per Aziende Alimentari)</h1>
                <p>Disinfetta i tuoi ambienti e prodotti da batteri, virus, muffe e altri contaminanti in modo efficace e veloce grazie all'ozono, senza lasciare residui chimici tossici per te stesso e l'ambiente.</p>
                <a>Qualificati Per Una Prova Gratuita</a>
            </div>
            <div class="flex-1">
            </div>
        </div>
    </section>
'''
section_00 = f'''
    <section class="home_hero_section">
        <div class="container-xl flex flex-col justify-center h-80vh">
            <h1 class="text-center">Disinfezione Veloce ed Ecologica (per Aziende Alimentari)</h1>
            <p>Disinfetta i tuoi ambienti e prodotti da batteri, virus, muffe e altri contaminanti in modo efficace e veloce grazie all'ozono, senza lasciare residui chimici tossici per te stesso e l'ambiente.</p>
            <div>
            <a>Qualificati Per Una Prova Gratuita</a>
            </div>
        </div>
    </section>
'''

section_01 = f'''
    <section class="pt-48">
        <div class="container-mb">
            <h2>Perche i Richiami Aumentano?</h2>
        </div>
        <div class="container-md mb-32">

            <p>Non e un segreto. I richiami di prodotti alimentari aumentano di anno in anno.</p> 
            <p>Solo nell'ultimo anno, sono aumentati di...</p>

            <p>I motivi? Sono 3:</p>
        </div>
        <div class="container-xl flex gap-16 mb-32">
            <div class="flex-1">
                <img src="/immagini-statiche/controllo-alimentare.png">
                <p class="text-center"><strong>Controlli piu feroci</strong></p>
            </div>
            <div class="flex-1">
                <img src="/immagini-statiche/legislazione-igiene.png">
                <p class="text-center"><strong>Leggi piu restrittive</strong></p>
            </div>
            <div class="flex-1">
                <img src="/immagini-statiche/disinfettante-chimico.png">
                <p class="text-center"><strong>Disinfettanti meno efficaci</strong></p>
            </div>
        </div>
        <div class="container-md">
            <ol class="mb-16">
            </ol>
            <p>Hai paura di essere il prossimo a vedersi ritirare i propri prodotti dal mercato? Temi di perdere la reputazione del tuo marchio e la fiducia dei tuo clienti (nonche di ricevere pesanti multe allo stesso tempo) perche non riesci piu a soddifare i pesanti standard di igiene alimentare che ti impongono le autorita locali e nazionali?</p>

            <p>Se hai questo timore, e del tutto comprensibile.</p>

            <p>Ed e altrettanto compresibile che tu voglia trovare una soluzione. una soluzione come quella che troverai in questa pagina.</p>

            <p>In questa pagina:</p>
            <ul class="mb-16">
                <li>imparerai come i nostri clienti nell'industria alimentare eliminano contaminazioni di batteri, virus e parassiti dai loro ambienti e prodotti in pochi minuti (o addirittura secondi) usando un sistema di disinfezione completamente ecologico.</li>
                <li>imparerai anche come prevenire epidemie di salmonella, listeria, e. coli ed altri comuni patogeni, evitando di subire richiami dei tuoi prodotti e di danneggiare la reputazione del tuo brand.</li>
                <li>e altro...</li>
            </ul>

            <p>Prima di fare questo, pero, ti chiediamo solo una cosa:</p>

            <p>Non perdere tempo e implementa tutto quello che imparerai in questo pagina il prima possibile.</p>

            <p>Ogni secondo che aspetti puo essere la causa di un richiamo dei tuoi prodotti o, ancora peggio, puo essere la causa di malattie e dell'ospedalizzazione dei tuoi consumatori.</p>

            <p>D'accordo? Se si, ecco cosa devi fare</p>

            <h2 class="pt-48">I 3 Punti Critici Che Causano il 90% Delle Contaminazioni</h2>
            
            Dei mille modi per cui i tuoi prodotti possono venire contaminati (e quindi richiamati dal mercato), 3 sono responsabili del 80% dei problemi.

            Prima di trovare la soluzione, bisogna capire bene il problema.

            Sebbene ci possono essere migliaia di ragioni per cui il tuo prodotto viene contaminato, ce ne sono 3 piu importanti. Se comprendi questi 3 hai risolto il 90% dei tuoi problemi.

            Le 3 fasi di produzione piu a rischio (e piu facili da sistemare):
            1. Lavorazione
            2. Stoccaggio
            3. Confezionamento
            
        </div>
        <div class="container-xl flex flex-col gap-48">
            <div class="flex gap-48">
                <div class="flex-1">
                    <img src="/immagini-statiche/lavorazione-prodotti.png">
                </div>
                <div class="flex-1">
                    <h2>Lavorazione</h2>
                </div>
            </div>
            <div class="flex gap-48">
                <div class="flex-1">
                    <h2>Stoccaggio</h2>
                </div>
                <div class="flex-1">
                    <img src="/immagini-statiche/sala-di-stoccaggio.png">
                </div>
            </div>
            <div class="flex gap-48">
                <div class="flex-1">
                    <img src="/immagini-statiche/confezionamento-cibi.png">
                </div>
                <div class="flex-1">
                    <h2>Confezionamento</h2>
                </div>
            </div>
        </div>

        """
        intro
            heres what you should be able to do the first time you go through this product
            here is what it can lead to over time if you continue to do it
            here are the steps (or factors) involved
            heres why these steps or factors are iprotant and why i chose them and put them in this order
        each step
            whi its important. briefly describe in a few sentences the context
            whats involved. briefly deescribe the critical components asssociated with the step/factor
            how to do it. specific advice on what actions to take
            what cna heppen. likely outcomes (1-3) to occur from taking action
        conclusion
            how this can epower you
            how this can improve relationships with others around you
            what you can achieve now, that you might not have been able to before
            how the more you do it the better/easier it will become
            here's encouragement to go do it now.
        """
        <div class="container-xl">
            <h2>3 cose da sanificare</h2>
            <p>superfici</p>
            <p>ambienti</p>
            <p>ingredienti</p>

            <h2>ozono</h2>
            <p>cosa e</p>
            <p>cosa fa</p>
            <p>perche funziona</p>

            <h2>utilizzo per le 3 fasi</h2>
            <p>fase 1: come usarlo, step-by-step, perche funziona</p>
            <p>fase 2: come usarlo, step-by-step, perche funziona</p>
            <p>fase 3: come usarlo, step-by-step, perche funziona</p>

            <h2>transizione</h2>

            <h2>offerta</h2>
            <p>sistema facile, automatizzato, veloce</p>
        </div>
        <div class="container-xl">
            <h2>Il Vecchio Metodo (Sanificazione Tradizionale)</h2>
            <div class="flex gap-48">
                <div class="flex-1">
                    <img src="/immagini-statiche/sanificazione-superfici.png">
                </div>
                <div class="flex-1">
                    <h2>Superfici Contatto</h2>
                    <p>
                        Tavoli, taglieri, utensili, macchinari, contenitori, carrelli e persino nastri trasportatori.
                    </p>
                    <p>
                        Questi sono solo alcuni esempi di superfici con cui i cibi entrano in contatto e che portano a contaminazioni crociate se non sanificate correttamente.
                    </p>
                    <p>
                        Il tipico processo di sanificazione delle superfici prevede di:
                    </p>
                    <ul>
                        <li>
                            <strong>Indossare protezioni</strong>: non devi mai toccare i disinfettanti chimici, visto che hanno un taso di tossicita estremamente elevato ed provocano problemi di salute cronici
                        </li>
                        <li>
                            <strong>Scegliere il giusto disinfettante</strong>: purtroppo, diversi agenti chimici funzionano solo su determinati tipi di microbi, per questo spesso non e chiaro quale sia quello giusto per te
                        </li>
                        <li>
                            <strong>Applicare il disinfettante su tutta la superficie</strong>: se non si copre completamente la superficie, non si eliminano le contaminazioni (difficile da fare, specialmente su superfici irregolari)
                        </li>
                        <li>
                            <strong>Lasciare il disinfettante agire</strong>: i disinfettanti tradizionali agiscono lentamente e questo rallenta la produzione e le altre operazioni
                        </li>
                        <li>
                            <strong>Risciacquare il disinfettante in eccesso</strong>: dato che i disinfettanti chimici lasciano residui tossici, bisogna risciaquare le superfici con abbondante acqua alla fine del processo di sanificazione
                        </li>
                    </ul>
                    <p>
                        Come puoi intuire, questo processo e lungo, problematico e spesso il risultato non e garantito.
                    </p>
                    <p>
                        Detto questo, ce un sistema per elimiare 3 dei passaggi appena elencati e per semplificare gli altri 2 (come vedremo tra poco).
                    </p>
                    <p>
                        Prima pero, vediamo gli altri due problemi.
                    </p>
                </div>
            </div>
        </div>
    </section>
'''



title = 'sanificazione ozono industriale | ozonogroup'
head_html = head_html_generate(title, 'style.css')
html = f'''
    <!DOCTYPE html>
    <html lang="en">
    {head_html}
    <body>
        <header>
        </header>
        <main>
            {section_00}
            {section_01}
        </main>
        <footer>
        </footer>
    </body>
    </html>
'''

file_write(f'public/index.html', html)

def a_contamination(entity_slug):
    entity_name = entity_slug.replace('-', ' ')
    '''
    where (source of contamination): 
        intestine, feces of man, animalss, birds.
        found in soil, water, raw agricultural such as raw milk, raw meat, ray, shellfish
    where foods:
        meat and raw milk
    where animals:
        dairy cattle
    treatments:
        heat processing (pasteurization)
        segregation of raw and cooked foodstuff
        good hygienic working practices
        formulating anf storing the product such that the patogen is inactivated or prevented from growing
            ex. fermented raw sausage
    resistances:
        acid-tolerant
        survive even in fermented sausages, mayonnaise, unpasteurized fruit juices
    subtypes?
    illness:
        typhoid fever
    mechanism for illness:
        produce verotoxins, or shiga-like toxins, which cause bloody diarrhea
        hemolytic uremic syndrome 
        most common cause of renal failure in children
    growth environments:
        raw meat, pultry ,eggs, dairy
    survival:
        long periods in frozen and dry conditions
        persistent environmental contaminant in food plats
    hisorical pandemic cases?
    
        
    '''

    json_data_filepath = f'{library_folderpath}/json-data/{entity_slug}.json'
    json_data = json_read(json_data_filepath)

    ##################################################################################
    # ;article json
    ##################################################################################
    json_article_filepath = f'{library_folderpath}/json-data/{entity_slug}.json'
    json_article = json_read(json_article_filepath, create=True)
    json_article['entity_slug'] = entity_slug
    json_article['entity_name'] = entity_name
    json_write(json_article_filepath, json_article)

    # what is
    key = 'what_is_desc'
    if key not in json_article: json_article[key] = ''
    # json_article[key] = ''
    if json_article[key] == '':
        entity_category = json_data['entity_category']
        prompt = f'''
            Write a 5-sentence short paragraph about what is {entity_name}.
            Include the following INFO about {entity_name}: 
            <INFO>
            - bacteria
            </INFO>
            Pack as much information in as few words as possible.
            Don't write fluff, only proven data.
            Don't include words that communicate the feeling that the data you provide is not proven, like "can", "may", "might" and "is believed to". 
            Don't allucinate.
            Write the paragraph in less than 150 words.
            Write only the paragraph, don't add additional info.
            Don't add references or citations.
            Don't include a conclusory statement with words like overall, in summary, or in conclusion. 
            Start with the following words: {entity_name} is .
        '''
        print(prompt)
        reply = llm_reply(prompt, model)
        lines = []
        for line in reply.split('\n'):
            line = line.strip()
            if line == '': continue
            if ':' in line: continue
            lines.append(line)
        if len(lines) == 1:
            json_article[key] = lines[0]
            json_write(json_article_filepath, json_article)

    # where is 
    key = 'where_is_desc'
    if key not in json_article: json_article[key] = ''
    json_article[key] = ''
    if json_article[key] == '':
        prompt = f'''
            Write a 5-sentence short paragraph about where is {entity_name} found and how do you get it.
            Pack as much information in as few words as possible.
            Don't write fluff, only proven data.
            Don't include words that communicate the feeling that the data you provide is not proven, like "can", "may", "might" and "is believed to". 
            Don't allucinate.
            Write the paragraph in less than 150 words.
            Write only the paragraph, don't add additional info.
            Don't add references or citations.
            Don't include a conclusory statement with words like overall, in summary, or in conclusion. 
            Start with the following words: {entity_name} is found .
        '''
        print(prompt)
        reply = llm_reply(prompt, model)
        lines = []
        for line in reply.split('\n'):
            line = line.strip()
            if line == '': continue
            if ':' in line: continue
            lines.append(line)
        if len(lines) == 1:
            json_article[key] = lines[0]
            json_write(json_article_filepath, json_article)

    ##################################################################################
    # ;article html
    ##################################################################################
    article_html = ''
    article_html += f'<h1 class="">{json_article["entity_name"]}</h1>\n'

    article_html += f'<h2>What is {json_article["entity_name"]}?</h2>\n'
    article_html += f'{text_format_1N1_html(json_article["what_is_desc"])}\n'

    article_html += f'<h2>Where is {json_article["entity_name"]} found?</h2>\n'
    article_html += f'{text_format_1N1_html(json_article["where_is_desc"])}\n'

    head_html = head_html_generate(json_article['entity_name'], '/style.css')

    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {article_html}
        </body>
        </html>
    '''
    html_filepath = f'contaminazioni/batteri/{entity_slug}.html'
    with open(html_filepath, 'w') as f: f.write(html)
    print(html_filepath)
    print('here')

shutil.copy2('style.css', f'public/style.css')

# a_contamination('listeria-monocytogenes')

# ;jump
def a_contaminazioni():
    json_article_filepath = f'database/pagine/contaminazioni.json'
    json_article = json_read(json_article_filepath, create=True)
    json_write(json_article_filepath, json_article)
    for vertex in vertices_contaminazioni:
        contaminazione_type = vertex['entity_type']
        if contaminazione_type != 'contaminazione': continue
        contaminazione_category = vertex['entity_category']
        contaminazione_slug = vertex['entity_slug']
        contaminazione_nome_scientifico = vertex['entity_name_scientific']
        contaminazione_nome_comune = vertex['entity_name_common']
        # init contaminations
        if 'contaminazioni' not in json_article: json_article['contaminazioni'] = []
        found = False
        for contaminazione in json_article['contaminazioni']:
            if contaminazione['contaminazione_slug'] == contaminazione_slug:
                found = True
                break
        if not found:
            json_article['contaminazioni'].append({
                'contaminazione_slug': contaminazione_slug,
                'contaminazione_nome_scientifico': contaminazione_nome_scientifico,
                'contaminazione_nome_comune': contaminazione_nome_comune,
            })
            json_write(json_article_filepath, json_article)
        # update contaminations
        for json_contaminazione in json_article['contaminazioni']:
            contaminazione_nome_scientifico = json_contaminazione['contaminazione_nome_scientifico']
            key = 'contaminazione_desc'
            if key not in json_contaminazione: json_contaminazione[key] = []
            # json_contaminazione[key] = []
            if json_contaminazione[key] == []:
                prompt = f'''
                    Scrivi un paragrafo di 3 frasi sulla seguente contaminazione: {contaminazione_nome_scientifico}.
                '''
                reply = llm_reply(prompt)
                json_contaminazione[key] = reply
                json_write(json_article_filepath, json_article)
    # ;html
    html_article = ''
    for i, json_contaminazione in enumerate(json_article['contaminazioni']):
        contaminazione_slug = json_contaminazione['contaminazione_slug']
        contaminazione_nome_scientifico = json_contaminazione['contaminazione_nome_scientifico']
        contaminazione_nome_comune = json_contaminazione['contaminazione_nome_comune']
        contaminazione_desc = json_contaminazione['contaminazione_desc']
        html_article += f'''<h2>{i+1}. {contaminazione_nome_scientifico.capitalize()}</h2>\n'''
        html_article += f'{text_format_1N1_html(contaminazione_desc)}\n'
        html_article += f'<p><a href="/contaminazioni/{contaminazione_slug}.html">{contaminazione_nome_scientifico}</a></p>\n'
    head_html = head_html_generate('contaminazioni', '/style.css')
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {html_article}
        </body>
        </html>
    '''
    html_filepath = f'public/contaminazioni.html'
    with open(html_filepath, 'w') as f: f.write(html)

def a_contaminazione(vertex_contaminazione):
    contaminazione_slug = vertex_contaminazione['entity_slug']
    contaminazione_nome_scientifico = vertex_contaminazione['entity_name_scientific']
    json_article_filepath = f'database/pagine/contaminazioni/{contaminazione_slug}.json'
    json_article = json_read(json_article_filepath, create=True)
    json_write(json_article_filepath, json_article)
    #####################################################
    # ;json
    #####################################################
    key = 'contaminazione_intro'
    if key not in json_article: json_article[key] = []
    # json_article[key] = []
    if json_article[key] == []:
        prompt = f'''
            Scrivi un paragrafo di 3 frasi sulla seguente contaminazione: {contaminazione_nome_scientifico}.
        '''
        reply = llm_reply(prompt)
        json_article[key] = reply
        json_write(json_article_filepath, json_article)
    key = 'contaminazione_sintomi'
    if key not in json_article: json_article[key] = ''
    # json_article[key] = ''
    if json_article[key] == '':
        sintomi = [sintomo['name'] for sintomo in vertex_contaminazione['symptoms']]
        sintomi_prompt = ', '.join(sintomi)
        prompt = f'''
            Scrivi un paragrafo di 3 frasi sui sintomi causati da: {contaminazione_nome_scientifico}.
            Includi i seguenti sintomi: {sintomi_prompt}.
            Rispondi in italiano.
        '''
        reply = llm_reply(prompt)
        json_article[key] = reply
        json_write(json_article_filepath, json_article)
    key = 'contaminazione_cibi'
    if key not in json_article: json_article[key] = ''
    # json_article[key] = ''
    if json_article[key] == '':
        cibi = [item['name'] for item in vertex_contaminazione['foods']]
        cibi_prompt = ', '.join(cibi)
        # Include some of the following foods: {cibi_prompt}.
        prompt = f'''
            write a 3-sentence paragraph about the foods with greater risk of {contaminazione_nome_scientifico} contamination.
            don't include conclusory statements.
            answer in italian.
        '''
        prompt = f'''
            Scrivi un paragrafo di 5 frasi sui cibi maggiormente a rischio di contaminazione da {contaminazione_nome_scientifico}.
            Includi i seguenti cibi: {cibi_prompt}.
            Rispondi in italiano, come se fossi un madrelingua italiano.
        '''
        reply = llm_reply(prompt)
        if 0:
            prompt = f'''
                Traduci il seguente testo in italiano: {reply}.
            '''
            reply = llm_reply(prompt)
        json_article[key] = reply
        json_write(json_article_filepath, json_article)
    key = 'contaminazione_cibi_lista'
    if key not in json_article: json_article[key] = []
    # json_article[key] = []
    if json_article[key] == []:
        contaminazioni = [item['name'] for item in vertex_contaminazione['foods']]
        contaminazioni_prompt = '\n- '.join(contaminazioni)
        prompt = f'''
            Traduci in italiano la seguente lista:
            {contaminazioni_prompt}
        '''
        reply = llm_reply(prompt)
        lines = []
        for line in reply.split('\n'):
            line = line.strip()
            if line == '': continue
            if not line.startswith('- '): continue
            line = '- '.join(line.split('- ')[1:])
            line = line.strip()
            if line == '': continue
            lines.append(line)
        json_article[key] = lines
        json_write(json_article_filepath, json_article)
    key = 'contaminazione_trattamenti'
    if key not in json_article: json_article[key] = ''
    # json_article[key] = ''
    if json_article[key] == '':
        trattamenti = [trattamento['name'] for trattamento in vertex_contaminazione['treatments']]
        trattamenti_prompt = ', '.join(trattamenti[:10])
        prompt = f'''
            Scrivi un paragrafo di 3 frasi sui trattamenti per {contaminazione_nome_scientifico} nell'industria alimentare.
            Includi i seguenti trattamenti: {trattamenti_prompt}.
            Rispondi in italiano.
            Non spiegare cosa sono o come funzionano questi trattamenti.
            Non elencare tutti i trattamenti subito nella prima frase.
            Comincia la risposta con le seguenti parole: I trattamenti piu usati per {contaminazione_nome_scientifico} sono, 
        '''
        reply = llm_reply(prompt)
        json_article[key] = reply
        json_write(json_article_filepath, json_article)
    key = 'contaminazione_trattamenti_lista'
    if key not in json_article: json_article[key] = []
    # json_article[key] = []
    if json_article[key] == []:
        trattamenti = [item['name'] for item in vertex_contaminazione['treatments']]
        json_article[key] = trattamenti
        json_write(json_article_filepath, json_article)
    #####################################################
    # ;html
    #####################################################
    html_article = ''
    html_article += f'''<h1>{contaminazione_nome_scientifico.capitalize()}</h1>\n'''
    html_article += f'''{text_format_1N1_html(json_article['contaminazione_intro'])}\n'''
    html_article += f'''<h2>Sintomi</h2>\n'''
    html_article += f'''{text_format_1N1_html(json_article['contaminazione_sintomi'])}\n'''
    html_article += f'''<h2>Cibi</h2>\n'''
    html_article += f'''{text_format_1N1_html(json_article['contaminazione_cibi'])}\n'''
    html_article += f'''<p>I cibi con maggior rischio di contaminazione da {contaminazione_nome_scientifico} sono elencati nella seguente lista:</p>\n'''
    html_article += f'''<ul>\n'''
    for item in json_article['contaminazione_cibi_lista'][:10]:
        html_article += f'''<li>{item.capitalize()}</li>\n'''
    html_article += f'''</ul>\n'''
    html_article += f'''<h2>Trattamenti</h2>\n'''
    html_article += f'''{text_format_1N1_html(json_article['contaminazione_trattamenti'])}\n'''
    html_article += f'''<ul>\n'''
    for item in json_article['contaminazione_trattamenti_lista'][:10]:
        html_article += f'''<li>{item.capitalize()}</li>\n'''
    html_article += f'''</ul>\n'''

    head_html = head_html_generate('contaminazioni', '/style.css')

    html_layout = f'''
        <section class="container-md">
            {html_article}
        </section>
    '''
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {html_layout}
        </body>
        </html>
    '''
    html_filepath = f'public/contaminazioni/{contaminazione_slug}.html'
    with open(html_filepath, 'w') as f: f.write(html)

if 1:
    a_contaminazioni()
    for vertex_contaminazione in vertices_contaminazioni:
        a_contaminazione(vertex_contaminazione)

