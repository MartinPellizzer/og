import re
import csv
import markdown


encoding = 'utf-8'

table = 'meat'

# Get all rows in table -------------------------------------------
rows = []
with open(f"database/{table}.csv", "r", encoding=encoding) as f:
    reader = csv.reader(f, delimiter="\\")
    for i, line in enumerate(reader):
        rows.append(line)



fields = {}
for i, col in enumerate(rows[0]):
    fields[col] = i

for key, value in fields.items():
    print(key + " - " +  str(value))
    pass

fields_list = rows[0]
rows = rows[1:]



def generate_line(i, row):
    studio = row[fields['studio']].strip()
    anno = row[fields['anno']].strip()
    
    problema_articolo_determinativo = row[fields['problema_articolo_determinativo']].lower()
    problema = row[fields['problema']].strip()
    
    prodotto_articolo_determinativo = row[fields['prodotto_articolo_determinativo']].lower()
    prodotto = row[fields['prodotto']].strip()
    sotto_prodotto = row[fields['sotto_prodotto']].strip()

    riduzione_ad = row[fields['riduzione_articolo_determinativo']].lower()
    riduzione = row[fields['riduzione']].strip()
    
    forma = row[fields['forma']].strip()
    dose = row[fields['dose']].strip()
    tempo = row[fields['tempo']].strip()
    giorni = row[fields['giorni']].strip()
    
    effetti_qualita = row[fields['effetti_qualita']].strip()
    
    temperatura = row[fields['temperatura']].strip()
    umidita = row[fields['umidita']].strip()
    ph = row[fields['ph']].strip()

    combinato = row[fields['combinato']].strip()

    # if riduzione.strip() == '': 
    #     return ''
    
    if forma.strip() != '': forma = f'in forma {forma} '
    else: forma = ''
    if dose.strip() != '': dose = f'a {dose} '
    else: dose = ''
    if tempo.strip() != '': tempo = f'per {tempo} '
    else: tempo = ''
    if giorni.strip() != '': giorni = f'per {giorni} '
    else: giorni = ''


    if riduzione_ad.strip() != '': riduzione_ad = f'{riduzione_ad} '
    else: riduzione_ad = ''
    if riduzione.strip() != '': riduzione = f'{riduzione} '
    else: riduzione = ''

    if temperatura.strip() != '': temperatura = f'a temperatura {temperatura}'
    else: temperatura = ''
    if umidita.strip() != '': umidita = f'con umidità {umidita}'
    else: umidita = ''
    if ph.strip() != '': ph = f'in pH {ph} '
    else: ph = ''
    
    if combinato.strip() != '': combinato = f'(combinato a {combinato}) '
    else: combinato = ''

    if (temperatura != '' or umidita != '' or ph != ''): conjunction_0 = ', '
    else: conjunction_0 = ''

    if (forma != '' or dose != '' or tempo != '' or giorni != ''): if_used = ', se usato'
    else: if_used = ''



    sentence = f'''
        Riduce 
        {problema_articolo_determinativo}{problema} 
        {prodotto_articolo_determinativo}{prodotto} {sotto_prodotto}
        {riduzione_ad}{riduzione}
        {combinato}
        {if_used} 
            {forma} 
            {dose} 
            {tempo} 
            {giorni} 
        {conjunction_0} 
            {temperatura} 
            {umidita} 
            {ph} 

        ({studio}, {anno}).
        '''

    print(sentence)

    sentence_formatted = sentence.replace('\n', '')
    # sentence_formatted = re.sub('|[^>]+!', '', sentence_formatted)
    sentence_formatted = re.sub(' +', ' ', sentence_formatted)
    sentence_formatted = sentence_formatted.replace(' ,', ',')
    
    print(sentence_formatted)


    return f'- {sentence_formatted}\n'

def generate_benefits(i, row):
    studio = row[fields['studio']].strip()
    anno = row[fields['anno']].strip()
    
    problema_articolo_determinativo = row[fields['problema_articolo_determinativo']].lower()
    problema = row[fields['problema']].strip()
    
    prodotto_articolo_determinativo = row[fields['prodotto_articolo_determinativo']].lower()
    prodotto_ad_benefici = row[fields['prodotto_ad_benefici']].lower()
    prodotto = row[fields['prodotto']].strip()
    sotto_prodotto = row[fields['sotto_prodotto']].strip()

    riduzione_ad = row[fields['riduzione_articolo_determinativo']].lower()
    riduzione = row[fields['riduzione']].strip()
    
    forma = row[fields['forma']].strip()
    dose = row[fields['dose']].strip()
    tempo = row[fields['tempo']].strip()
    giorni = row[fields['giorni']].strip()
    
    effetti_qualita = row[fields['effetti_qualita']].strip()
    
    temperatura = row[fields['temperatura']].strip()
    umidita = row[fields['umidita']].strip()
    ph = row[fields['ph']].strip()

    combinato = row[fields['combinato']].strip()

    # if riduzione.strip() == '': 
    #     return ''
    
    if forma.strip() != '': forma = f'in forma {forma} '
    else: forma = ''
    if dose.strip() != '': dose = f'a {dose} '
    else: dose = ''
    if tempo.strip() != '': tempo = f'per {tempo} '
    else: tempo = ''
    if giorni.strip() != '': giorni = f'per {giorni} '
    else: giorni = ''

    if riduzione_ad.strip() != '': riduzione_ad = f'{riduzione_ad} '
    else: riduzione_ad = ''
    if riduzione.strip() != '': riduzione = f'{riduzione} '
    else: riduzione = ''

    if temperatura.strip() != '': temperatura = f'a temperatura {temperatura}'
    else: temperatura = ''
    if umidita.strip() != '': umidita = f'con umidità {umidita}'
    else: umidita = ''
    if ph.strip() != '': ph = f'in pH {ph} '
    else: ph = ''

    if effetti_qualita.strip() != '': effetti_qualita = f'{effetti_qualita} '
    else: effetti_qualita = ''
    
    if combinato.strip() != '': combinato = f'(combinato a {combinato}) '
    else: combinato = ''

    if (temperatura != '' or umidita != '' or ph != ''): conjunction_0 = ', '
    else: conjunction_0 = ''

    if (forma != '' or dose != '' or tempo != '' or giorni != ''): if_used = ', se usato'
    else: if_used = ''

    '''
    Kurtz et al. (1969) latte scremato e intero in polvere 32 ppb 
    '''

    '''
    Riduce la qualità sensoriale del latte in polvere intero e scremato 
    (ma maggiormente di quello intero), 
    se usato a 32 ppb (Kurtz et al., 1969).
    '''

    sentence = f'''
        {effetti_qualita}
        {prodotto_ad_benefici}{prodotto} {sotto_prodotto}
        {if_used} 
            {forma} 
            {dose} 
            {tempo} 
            {giorni} 
        {conjunction_0} 
            {temperatura} 
            {umidita} 
            {ph} 

        ({studio}, {anno}).
        '''

    print(sentence)

    sentence_formatted = sentence.replace('\n', '')
    # sentence_formatted = re.sub('|[^>]+!', '', sentence_formatted)
    sentence_formatted = re.sub(' +', ' ', sentence_formatted)
    sentence_formatted = sentence_formatted.replace(' ,', ',')
    
    print(sentence_formatted)


    return f'- {sentence_formatted}\n'



def get_line_data(row):
    data = {}
    for i, col in enumerate(row):
        data[fields_list[i]] = col

    return data


def generate_line_application(row):
    data = get_line_data(row)

    if data['treatment_type'].strip() == 'ow': data['treatment_type'] = 'in forma acquosa '
    else: data['treatment_type'] = ''
    
    if data['w_pressure'].strip() != '': 
        data['w_pressure'] =  'a una pressione di ' + data['w_pressure']
    
    if data['w_pressure'].strip() != '': 
        data['w_pressure'] =  'a una pressione di ' + data['w_pressure']

    if data['o3_concentration'].strip() != '': 
        data['o3_concentration'] =  'a una concentrazione di ' + data['o3_concentration']
        
    if data['treatment_time'].strip() != '': 
        data['treatment_time'] =  'per un tempo di ' + data['treatment_time']
        
    if data['pathogen_reduction_number'].strip() != '': 
        data['pathogen_reduction_number'] =  'di ' + data['pathogen_reduction_number']
        
    if data['pathogen_reduction_text'].strip() != '': 
        data['pathogen_reduction_text'] =  'in modo ' + data['pathogen_reduction_text']


    
    sentence = ''
    
        
    

    sentence += f'''
        Riduce 
        il livello di
        {data['problem']}
        {data['product_ad_1']}{data['product']}
        {data['pathogen_reduction_number']}
        {data['pathogen_reduction_text']}
        , se usato 
        {data['treatment_type']} {(data['treatment'])}
        {data['w_pressure']} 
        {data['o3_concentration']} 
        {data['treatment_time']} 

        ({data['study']}, {data['study_year']}).
        '''

    print()
    print()
    print(sentence)


    sentence_formatted = sentence.replace('\n', '')
    # sentence_formatted = re.sub('|[^>]+!', '', sentence_formatted)
    sentence_formatted = re.sub(' +', ' ', sentence_formatted)
    sentence_formatted = sentence_formatted.replace(' ,', ',')
    
    
    print()
    print(sentence_formatted)
    print()

    return f'- {sentence_formatted}\n'




with open('test.md', 'w', encoding=encoding) as f:
    f.write('')


def generate_section(product):
    text = ''

    problem_list = []
    study_list = []
    for i, row in enumerate(rows):
        if row[fields['product']].strip().lower() == product.lower().strip():
            problem_list.append(row[fields['problem']].strip().lower())
            study_list.append(row[fields['study']].strip().lower())

    print(problem_list)
    print(study_list)



    text += f'''
        L'ozono viene usato per trattare {product}
        , eliminando problemi come {problem_list[0]} {problem_list[1]} e {problem_list[2]}
        , come dimostrato da diversi studi (ad esempio {study_list[0]} e {study_list[1]}).
    '''
    text = text.replace('\n', '').strip()
    text = re.sub(' +', ' ', text)
    text += '\n\n'

     
    
    # INTRODUZIONE LISTA -----------------------------------------------
    for i, row in enumerate(rows):
        if row[fields['product']].strip().lower() == product.lower().strip():
            data = get_line_data(row)
            break
    
    text += f'''
        Ecco una lista di alcune applicazioni dell\'ozono 
        {data['product_ad_2']}{data['product']}:
    '''
    text = text.replace('\n', '').strip()
    text = re.sub(' +', ' ', text)
    text += '\n\n'

    # LISTA ------------------------------------------------------------
    for i, row in enumerate(rows):
        if row[fields['product']].strip().lower() == product.lower().strip():
            text += generate_line_application(row)

    with open('test.md', 'a', encoding=encoding) as f:
        f.write(f'### {product.capitalize()}\n\n')
        f.write(f'{text}\n\n')





generate_section('carcasse di manzo')
generate_section('petto di manzo')
generate_section('ritagli di manzo')
# generate_section('prosciutto')




def generate_image_sanitation(image_out_path):    
    img_w, img_h = 768, 432
    img = Image.new("RGBA", (img_w, img_h), ImageColor.getrgb("#f8fafc"))

    draw = ImageDraw.Draw(img)

    
    icon_w = 96
    icon_h = 96

    icon = Image.open("assets/icons/milk.png").convert("RGBA")
    icon = icon.resize((icon_w, icon_h))
    img.paste(icon, (0, 0), icon)

    icon = Image.open("assets/icons/milk.png").convert("RGBA")
    icon = icon.resize((icon_w, icon_h))
    img.paste(icon, (200, 0), icon)

    icon = Image.open("assets/icons/milk.png").convert("RGBA")
    icon = icon.resize((icon_w, icon_h))
    img.paste(icon, (400, 0), icon)

    icon = Image.open("assets/icons/milk.png").convert("RGBA")
    icon = icon.resize((icon_w, icon_h))
    img.paste(icon, (600, 0), icon)
    
    icon = Image.open("assets/icons/milk.png").convert("RGBA")
    icon = icon.resize((icon_w, icon_h))
    img.paste(icon, (100, 200), icon)

    icon = Image.open("assets/icons/milk.png").convert("RGBA")
    icon = icon.resize((icon_w, icon_h))
    img.paste(icon, (300, 200), icon)

    icon = Image.open("assets/icons/milk.png").convert("RGBA")
    icon = icon.resize((icon_w, icon_h))
    img.paste(icon, (500, 200), icon)

    img.convert('RGB').save(f'{image_out_path}')
    # img.show()

# generate_image_sanitation('assets/images/articles/ozono-sanificazione-caseifici.jpg')





with open('test.md', encoding=encoding) as f:
    generated_content = f.read()

# generated_content = text

content_html = markdown.markdown(generated_content, extensions=['markdown.extensions.tables', 'meta'])

md = markdown.Markdown(extensions=['meta'])
md.convert(generated_content)


lines = '\n'.join(md.lines)

content_html = markdown.markdown(lines, extensions=['markdown.extensions.tables'])

    
with open(f'_tmp_{table}.html', 'w', encoding=encoding) as f:
    html = f'''
        <!DOCTYPE html>
        <html lang="en">

        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="/style-blog.css">
            <link rel="stylesheet" href="/util.css">
            <title>Ozonogroup</title>
        </head>

        <body>
            <section class="header-section">
                <div class="container-xl h-full">
                </div>
            </section>

            <section class="breadcrumbs-section">
                <div class="container-xl h-full">
                </div>
            </section>

            <section class="meta-section mt-48">
                <div class="container-md h-full">
                    <div class="flex justify-between mb-8">
                    </div>
                </div>
            </section>

            <section class="container-md">
                {content_html}
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

    f.write(html)