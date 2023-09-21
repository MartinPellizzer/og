
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


fields_list = rows[0]
rows = rows[1:]





def get_line_data(row):
    data = {}
    for i, col in enumerate(row):
        data[fields[i]] = col

    return data

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