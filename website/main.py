import os
import json
import shutil

from nltk import tokenize

import torch
from diffusers import DiffusionPipeline, StableDiffusionXLPipeline
from diffusers import DPMSolverMultistepScheduler
from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps

from oliark_io import file_read, file_write
from oliark_io import json_read, json_write
from oliark_llm import llm_reply

AUTHOR_NAME = 'Ozonogroup'

vault = '/home/ubuntu/vault'
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

###########################################################################
# ;images gen ai
###########################################################################
pipe = None
checkpoint_filepath = f'{vault}/stable-diffusion/checkpoints/xl/juggernautXL_juggXIByRundiffusion.safetensors'
def gen_image_food(food_name_eng, food_name_ita):
    image_web_filepath = f'public/immagini/alimenti/{food_name_ita}.jpg'
    if os.path.exists(image_web_filepath): return
    global pipe
    if pipe == None:
        pipe = StableDiffusionXLPipeline.from_single_file(
            checkpoint_filepath, 
            torch_dtype=torch.float16, 
            use_safetensors=True, 
            variant="fp16"
        ).to('cuda')
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    prompt = f'''
        close-up of {food_name_eng},
        on a stainless steel table,
        natural lighting,
        depth of field, bokeh,
        high resolution,
        cinematic
    '''
    print(prompt)
    image = pipe(prompt=prompt, width=1024, height=1024, num_inference_steps=30, guidance_scale=7.0).images[0]
    image.save(f'public/immagini/alimenti/{food_name_ita}.jpg')

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

def a_contamination(contamination_slug):
    contamination_name = contamination_slug.replace('-', ' ')
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

    json_data_filepath = f'{library_folderpath}/json-data/{contamination_slug}.json'
    json_data = json_read(json_data_filepath)

    ##################################################################################
    # ;article json
    ##################################################################################
    json_article_filepath = f'{library_folderpath}/json-data/{contamination_slug}.json'
    json_article = json_read(json_article_filepath, create=True)
    json_article['contamination_slug'] = contamination_slug
    json_article['contamination_name'] = contamination_name
    json_write(json_article_filepath, json_article)

    # what is
    key = 'what_is_desc'
    if key not in json_article: json_article[key] = ''
    # json_article[key] = ''
    if json_article[key] == '':
        contamination_category = json_data['contamination_category']
        prompt = f'''
            Write a 5-sentence short paragraph about what is {contamination_name}.
            Include the following INFO about {contamination_name}: 
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
            Start with the following words: {contamination_name} is .
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
            Write a 5-sentence short paragraph about where is {contamination_name} found and how do you get it.
            Pack as much information in as few words as possible.
            Don't write fluff, only proven data.
            Don't include words that communicate the feeling that the data you provide is not proven, like "can", "may", "might" and "is believed to". 
            Don't allucinate.
            Write the paragraph in less than 150 words.
            Write only the paragraph, don't add additional info.
            Don't add references or citations.
            Don't include a conclusory statement with words like overall, in summary, or in conclusion. 
            Start with the following words: {contamination_name} is found .
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
    article_html += f'<h1 class="">{json_article["contamination_name"]}</h1>\n'

    article_html += f'<h2>What is {json_article["contamination_name"]}?</h2>\n'
    article_html += f'{text_format_1N1_html(json_article["what_is_desc"])}\n'

    article_html += f'<h2>Where is {json_article["contamination_name"]} found?</h2>\n'
    article_html += f'{text_format_1N1_html(json_article["where_is_desc"])}\n'

    head_html = head_html_generate(json_article['contamination_name'], '/style.css')

    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {article_html}
        </body>
        </html>
    '''
    html_filepath = f'contaminazioni/batteri/{contamination_slug}.html'
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
        contaminazione_category = vertex['contamination_category']
        contaminazione_slug = vertex['contamination_slug']
        contaminazione_nome_scientifico = vertex['contamination_name_scientific']
        contaminazione_nome_comune = vertex['contamination_name_common']
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
    contaminazione_slug = vertex_contaminazione['contamination_slug']
    contaminazione_nome_scientifico = vertex_contaminazione['contamination_name_scientific']

    json_foods_filepath = f'database/pagine/contaminazioni/{contaminazione_slug}-foods.json'
    if not os.path.exists(json_foods_filepath):
    # if True:
        foods_groups = []
        for food in vertex_contaminazione['foods'][:]:
            if food['score_tot'] < 10: continue
            # if food['mentions'] < 3: continue
            food_name = food['name']
            foods_categories = ['latticini', 'carni', 'frutta e verdura', 'pesce', 'dolci', 'bevande', 'altro']
            foods_categories_prompt = ', '.join(foods_categories)
            prompt = f'''
                I will give you the name of a FOOD and the names of FOODS CATEGORIES.
                I want you to choose the most relevant category for the food i will give you.
                For "category", I mean the type of food industry that is responsible to making that food.
                You must choose the most relevant category only from the categories provided.
                FOOD: {food_name}
                FOODS CATEGORIES: {foods_categories_prompt}.
                Reply in italian the name of the food and the category.
                Reply in JSON using the format below:
                {{
                    "food": "insert name of food in italian here",
                    "category": "insert name of category in italian here",
                }}
                Reply only with the JSON.
            '''
            reply = llm_reply(prompt)
            print(prompt)
            try: json_reply = json.loads(reply)
            except: json_reply = {}
            if json_reply != {}:
                try: reply_food_name = json_reply['food'].lower().strip()
                except: continue
                try: reply_food_category = json_reply['category'].lower().strip()
                except: continue
                if reply_food_name != food_name: continue
                if reply_food_category not in foods_categories: continue
                found = False
                for food_group in foods_groups:
                    if reply_food_category == food_group['food_category']:
                        food_group['foods_names'].append(reply_food_name)
                        found = True
                        break
                if not found:
                    foods_groups.append({
                        'food_category': reply_food_category,
                        'foods_names': [reply_food_name],
                    })

        j = json.dumps(foods_groups, indent=4)
        with open(f'database/pagine/contaminazioni/{contaminazione_slug}-foods.json', 'w') as f:
            print(j, file=f)

        for food in foods_groups:
            print(food)

    json_article_filepath = f'database/pagine/contaminazioni/{contaminazione_slug}.json'
    json_article = json_read(json_article_filepath, create=True)
    json_write(json_article_filepath, json_article)

    #####################################################
    # ;json
    #####################################################
    sections = [
        {'exe': 1, 'slug': 'what', 'keyword': 'what is', 'level': 2, 'regen': False},
            {'exe': 1, 'slug': 'definition', 'keyword': 'definition', 'level': 3, 'regen': False},
            {'exe': 1, 'slug': 'family', 'keyword': 'family', 'level': 3, 'regen': False},
            {'exe': 1, 'slug': 'genus', 'keyword': 'genus', 'level': 3, 'regen': False},
            {'exe': 1, 'slug': 'gram', 'keyword': 'gram', 'level': 3, 'regen': False},
            {'exe': 1, 'slug': 'microscope', 'keyword': 'under microscope', 'level': 3, 'regen': False},
        {'exe': 1, 'slug': 'where', 'keyword': 'where is found', 'level': 2, 'regen': False},
            {'exe': 1, 'slug': 'how_to_get', 'keyword': 'how do you get', 'level': 3, 'regen': False},
            {'exe': 1, 'slug': 'aliments', 'keyword': 'aliments', 'level': 3, 'regen': False},
            {'exe': 1, 'slug': 'biofilm', 'keyword': 'biofilm', 'level': 3, 'regen': False},
            {'exe': 1, 'slug': 'habitat', 'keyword': 'habitat', 'level': 3, 'regen': False},
            {'exe': 1, 'slug': 'growth_conditions', 'keyword': 'growth conditions', 'level': 3, 'regen': False},
            {'exe': 1, 'slug': 'growth_temperature', 'keyword': 'growth temperature', 'level': 3, 'regen': False},
        {'exe': 1, 'slug': 'kill', 'keyword': 'how to kill', 'level': 2, 'regen': False},
            {'exe': 1, 'slug': 'heat kill', 'keyword': 'heat kill', 'level': 3, 'regen': False},
            {'exe': 1, 'slug': 'freezing', 'keyword': 'freezing', 'level': 3, 'regen': False},
            {'exe': 1, 'slug': 'haccp', 'keyword': 'haccp', 'level': 3, 'regen': False},
        {'exe': 1, 'slug': 'effects', 'keyword': 'effects', 'level': 2, 'regen': False},
            {'exe': 1, 'slug': 'symptoms', 'keyword': 'symptoms', 'level': 3, 'regen': False},
            {'exe': 1, 'slug': 'duration', 'keyword': 'how long does it last', 'level': 3, 'regen': False},
            {'exe': 1, 'slug': 'prevention', 'keyword': 'how to prevent', 'level': 3, 'regen': False},
            {'exe': 1, 'slug': 'treatments', 'keyword': 'how to treat', 'level': 3, 'regen': False},
            {'exe': 1, 'slug': 'diagnosis', 'keyword': 'diagnosis', 'level': 3, 'regen': False},
            {'exe': 1, 'slug': 'how_long_before_symptoms', 'keyword': 'diagnosis', 'level': 3, 'regen': False},
            {'exe': 1, 'slug': 'how_to_prevent', 'keyword': 'how to prevent', 'level': 3, 'regen': False},
            {'exe': 1, 'slug': 'how_to_treat', 'keyword': 'how to treat', 'level': 4, 'regen': False},
                {'exe': 1, 'slug': 'antibiotic', 'keyword': 'antibiotic', 'level': 4, 'regen': False},
                {'exe': 1, 'slug': 'antibiotic_resistance', 'keyword': 'antibiotic resistance', 'level': 3, 'regen': False},
            {'exe': 1, 'slug': 'pregnancy', 'keyword': 'pregnancy', 'level': 3, 'regen': False},
            {'exe': 1, 'slug': 'breastfeeding', 'keyword': 'breastfeeding', 'level': 3, 'regen': False},
            {'exe': 1, 'slug': 'kids', 'keyword': 'kids', 'level': 3, 'regen': False},
    ]

    sections = [
        {
            'exe': 1, 
            'slug': 'what', 
            'title': f'Cos\'è {contaminazione_nome_scientifico}?', 
            'level': 2, 
            'style': 'p', 
            'regen': False,
            'prompt': f'''
                write a short 5-sentence paragraph about the following query regarding {contaminazione_nome_scientifico}: what is.
                reply only with the paragraph.
                reply in italian.
            ''',
        },
        {
            'exe': 1, 
            'slug': 'where', 
            'title': f'Dove si trova {contaminazione_nome_scientifico}?', 
            'level': 2, 
            'style': 'p', 
            'regen': False,
            'prompt': f'''
                write a short 5-sentence paragraph about the following query regarding {contaminazione_nome_scientifico}: where do you find it.
                reply only with the paragraph.
                reply in italian.
            ''',
        },
            {
                'exe': 1, 
                'slug': 'foods', 
                'title': f'Quali sono gli alimenti ad alto rischio di {contaminazione_nome_scientifico}?',
                'level': 3, 
                'style': 'li', 
                'opening': 'I cibi ad alto rischio di listeria sono elencati nella lista seguente.', 
                'regen': True,
                'prompt': f'''
                    Write a list of the 10 foods with highest risk of being contaminated with {contaminazione_nome_scientifico}.
                    write only one food for each list item.
                    reply in as few words as possible.
                    reply only with the names of foods.
                    reply only with the list.
                    reply in italian.
                ''',
            },
        {
            'exe': 1, 
            'slug': 'treatments', 
            'title': f'Quali sono i trattamenti convenzionali per eliminare {contaminazione_nome_scientifico}?',
            'level': 2, 
            'style': 'p', 
            'regen': False,
            'prompt': f'''
                write a short 5-sentence paragraph about the following query regarding {contaminazione_nome_scientifico}: what are the traditional sanitization techniques in the food industry.
                reply only with the paragraph.
                reply in italian.
            ''',
        },
        {
            'exe': 1, 
            'slug': 'ozone', 
            'title': f'Come eliminare {contaminazione_nome_scientifico} con ozono?', 
            'level': 2, 
            'style': 'p', 
            'regen': False,
            'prompt': f'''
                write a short 5-sentence paragraph about the following query regarding {contaminazione_nome_scientifico}: come eliminare con ozono. 
                reply only with the paragraph.
                reply in italian.
            ''',
        },
        {
            'exe': 1, 
            'slug': 'health', 
            'title': f'Quali sono gli effetti sulla salute di {contaminazione_nome_scientifico} con ozono?', 
            'level': 2, 
            'style': 'p', 
            'regen': False,
            'prompt': f'''
                write a short 5-sentence paragraph about the following query regarding {contaminazione_nome_scientifico}: quali sono gli effetti sulla salute.
                reply only with the paragraph.
                reply in italian.
            ''',
        },
    ]

    key = 'where_aliments_intro'
    if key not in json_article: json_article[key] = []
    # json_article[key] = []
    if json_article[key] == []:
        foods_names = [food['name'] for food in vertex_contaminazione['foods']]
        foods_names_prompt = ', '.join(foods_names)
        prompt = f'''
            write a short 3-sentence paragraph about the aliments at higher risk of being contaminated with {contaminazione_nome_scientifico}.
            reply only with the paragraph.
            include the following foods: {foods_names_prompt}.
            start with the following words: Gli alimenti col maggior rischio di contaminazione da {contaminazione_nome_scientifico} sono .
            reply in italian.
        '''
        print(prompt)
        reply = llm_reply(prompt)
        json_article[key] = reply
        json_write(json_article_filepath, json_article)

    if 0:
        for section in sections:
            key = section['slug']
            aspect = section['keyword']
            level = section['level']
            regen = section['regen']
            if key not in json_article: json_article[key] = []
            # json_article[key] = []
            if json_article[key] == [] or regen == True:
                prompt = f'''
                    write a short 5-sentence paragraph about the following aspect regarding {contaminazione_nome_scientifico}: {aspect}.
                    reply only with the paragraph.
                    reply in italian.
                '''
                print(prompt)
                reply = llm_reply(prompt)
                json_article[key] = reply
                json_write(json_article_filepath, json_article)
    if 0:
        for section in sections:
            key = section['slug']
            style = section['style']
            level = section['level']
            regen = section['regen']
            prompt = section['prompt']
            if key not in json_article: json_article[key] = []
            # json_article[key] = []
            if json_article[key] == [] or regen == True:
                print(prompt)
                reply = llm_reply(prompt)
                if style == 'p':
                    json_article[key] = reply
                    json_write(json_article_filepath, json_article)
                elif style == 'li':
                    lines = []
                    for line in reply.split('\n'):
                        line = line.strip()
                        if line == '': continue
                        if not line[0].isdigit(): continue
                        if '. ' not in line: continue
                        line = '. '.join(line.split('. ')[1:])
                        if line[-1] == '.': line = line[:-1]
                        line = line.strip()
                        if line == '': continue
                        lines.append(line)
                    json_article[key] = lines
                    json_write(json_article_filepath, json_article)

    #####################################################
    # ;images
    #####################################################
    gen_image_food('cheese', 'formaggio')
    gen_image_food('ricotta', 'ricotta')
    gen_image_food('ham', 'prosciutto')
    gen_image_food('cake', 'torta')
    gen_image_food('tomato', 'pomodoro')
    gen_image_food('melon', 'melone')
    gen_image_food('salmon', 'salmone')
    gen_image_food('milk', 'latte')
    gen_image_food('honey', 'miele')
    gen_image_food('brie', 'brie')

    #####################################################
    # ;html
    #####################################################
    html_article = ''
    if 0:
        html_article += f'''<h1>{contaminazione_nome_scientifico.capitalize()}</h1>\n'''
        html_article += f'''{text_format_1N1_html(json_article['contaminazione_intro'])}\n'''
        html_article += f'''<h2>Sintomi</h2>\n'''
        html_article += f'''{text_format_1N1_html(json_article['contaminazione_sintomi'])}\n'''
        ## where is found
        html_article += f'''<h2>Dove si trova {contaminazione_nome_scientifico}?</h2>\n'''
        html_article += f'''{text_format_1N1_html(json_article['where_is_found'])}\n'''
        ## habitat
        html_article += f'''<h3>Quale e l'habitat ideale per {contaminazione_nome_scientifico}?</h3>\n'''
        html_article += f'''{text_format_1N1_html(json_article['habitat'])}\n'''
        ## growth conditions
        html_article += f'''<h3>Quali sono le condizioni di crescita per {contaminazione_nome_scientifico}?</h3>\n'''
        html_article += f'''{text_format_1N1_html(json_article['growth_conditions'])}\n'''
        ## growth temperature
        html_article += f'''<h3>Quali sono le temperature di crescita per {contaminazione_nome_scientifico}?</h3>\n'''
        html_article += f'''{text_format_1N1_html(json_article['growth_temperature'])}\n'''
        ## how you get it
        html_article += f'''<h3>Come si prende {contaminazione_nome_scientifico}?</h3>\n'''
        html_article += f'''{text_format_1N1_html(json_article['how_you_get_it'])}\n'''
        ### foods
        html_article += f'''<h3>{contaminazione_nome_scientifico.capitalize()} Alimenti</h3>\n'''
        # html_article += f'''{text_format_1N1_html(json_article['contaminazione_cibi'])}\n'''
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

    html_article += f'''<h1>{contaminazione_nome_scientifico.capitalize()}</h1>\n'''
    for section in sections:
        exe = section['exe']
        if exe == 0: continue
        key = section['slug']
        title = section['title']
        style = section['style']
        level = section['level']
        try: opening = section['opening']
        except: opening = ''
        content = json_article[key]
        if level == 2:
            html_article += f'''<h2>{title}</h2>\n'''
        elif level == 3:
            html_article += f'''<h3>{title}</h3>\n'''
        elif level == 4:
            html_article += f'''<h4>{title}</h4>\n'''
        if style == 'p':
            html_article += f'''{text_format_1N1_html(content)}\n'''
        elif style == 'li':
            if opening != '':
                html_article += f'''<p>{opening}</p>\n'''
            html_article += f'''<ul>\n'''
            for item in content:
                html_article += f'''<li>{item}</li>\n'''
            html_article += f'''</ul>\n'''

    with open(json_foods_filepath) as f:
        foods_categories = json.load(f)
    html_table = ''
    html_table += f'<table>\n'
    html_table += f'<tr>\n'
    html_table += f'<th>Categorie</th>\n'
    html_table += f'<th>Alimenti</th>\n'
    html_table += f'</tr>\n'
    for food in foods_categories:
        food_category = food['food_category']
        foods_names = food['foods_names'][:6]
        foods_names_str = ', '.join(foods_names)
        html_table += f'<tr>\n'
        html_table += f'''<td>{food_category.title()}</td>\n'''
        html_table += f'''<td>{foods_names_str.title()}</td>\n'''
        html_table += f'</tr>\n'
    html_table += f'</table>\n'

    images_filepaths = []
    for food in foods_categories:
        for food_name in food['foods_names'][:6]:
            food_name = food_name.lower().strip()
            image_filepath = f'public/immagini/alimenti/{food_name}.jpg'
            image_web_filepath = f'/immagini/alimenti/{food_name}.jpg'
            print(image_filepath)
            if os.path.exists(image_filepath):
                images_filepaths.append(image_web_filepath)
    html_images = ''
    for image_filepath in images_filepaths[:9]:
        html_images += f'''
            <img src="{image_filepath}" class="food-grid-img">
        '''
    
    html_section_foods = f'''
        <section class="container-xl mt-48">
            <h3>Quali alimenti sono ad altro rischio di {contaminazione_nome_scientifico}?</h3>
            {text_format_1N1_html(json_article['where_aliments_intro'])}
            <div class="separator_line"></div>
            <div class="grid-2 gap-48">
                <div>
                    <p>La seguente tabella lista alcuni esempi di cibi a maggior rischio di {contaminazione_nome_scientifico} raggruppati per categoria.</p>
                    {html_table}
                </div>
                <div>
                    <p>Le seguenti immaigni raffigurano alcuni esempi di cibi a maggior rischio di {contaminazione_nome_scientifico}.</p>
                    <div class="grid-3 gap-16">
                        {html_images}
                    </div>
                </div>
            </div>
        </section>
    '''

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
            {html_section_foods}
        </body>
        </html>
    '''
    html_filepath = f'public/contaminazioni/{contaminazione_slug}.html'
    with open(html_filepath, 'w') as f: f.write(html)

if 1:
    a_contaminazioni()
    for vertex_contaminazione in vertices_contaminazioni:
        a_contaminazione(vertex_contaminazione)

