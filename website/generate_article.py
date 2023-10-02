import json
import os
import random
import re
import markdown

# for file in os.listdir('articles_tmp'):
#     os.remove(f'articles_tmp/{file}')


with open("database/json/articles.json", encoding='utf-8') as f:
    data = json.loads(f.read())
with open("database/json/pathogens.json", encoding='utf-8') as f:
    data_pathogens = json.loads(f.read())

    
def lst_to_blt(lst):
    txt = ''
    for item in lst:
        txt += f'- {item}\n'
    return txt.strip()


def lst_to_txt(lst):
    txt = ''
    if len(lst) == 0: txt = ''
    elif len(lst) == 1: txt = lst[0]
    elif len(lst) == 2: txt = f'{lst[0]} e {lst[1]}'
    else: txt = f'{", ".join(lst[:-1])} e {lst[-1]}'
    return txt


def bold_blt(lst):
    bld_lst = []
    for item in lst:
        if ':' in item:
            item_parts = item.split(":")
            bld_lst.append(f'**{item_parts[0]}**: {item_parts[1]}')
        else:
            bld_lst.append(f'{item}')
    return bld_lst


def generate_toc(content_html):
    table_of_contents_html = ''

    # get list of headers and generate IDs
    headers = []
    content_html_with_ids = ''
    current_id = 0
    for line in content_html.split('\n'):
        if '<h2>' in line:
            headers.append(line)
            content_html_with_ids += (line.replace('<h2>', f'<h2 id="{current_id}">'))
            current_id +=1
        elif '<h3>' in line:
            headers.append(line)
            content_html_with_ids += (line.replace('<h3>', f'<h3 id="{current_id}">'))
            current_id +=1
        elif '<h4>' in line:
            headers.append(line)
            content_html_with_ids += (line.replace('<h4>', f'<h4 id="{current_id}">'))
            current_id +=1
        elif '<h5>' in line:
            headers.append(line)
            content_html_with_ids += (line.replace('<h5>', f'<h5 id="{current_id}">'))
            current_id +=1
        elif '<h6>' in line:
            headers.append(line)
            content_html_with_ids += (line.replace('<h6>', f'<h6 id="{current_id}">'))
            current_id +=1
        else:
            content_html_with_ids += (line)
        content_html_with_ids += '\n'

    # generate table
    toc_li = []

    table_of_contents_html += '<div class="toc">'
    table_of_contents_html += '<span class="toc-title">Tabella dei Contenuti</span>'
    table_of_contents_html += '<ul>'
    
    last_header = '<h2>'
    for i, line in enumerate(headers):
        insert_open_ul = False
        insert_close_ul = False

        if '<h2>' in line: 
            if last_header != '<h2>': 
                if int('<h2>'[2]) > int(last_header[2]): insert_open_ul = True
                else: insert_close_ul = True
            last_header = '<h2>'
            line = line.replace('<h2>', '').replace('</h2>', '')

        elif '<h3>' in line:
            if last_header != '<h3>':
                if int('<h3>'[2]) > int(last_header[2]): insert_open_ul = True
                else: insert_close_ul = True

            last_header = '<h3>'
            line = line.replace('<h3>', '').replace('</h3>', '')

        if insert_open_ul: table_of_contents_html += f'<ul>'
        if insert_close_ul: table_of_contents_html += f'</ul>'
        table_of_contents_html += f'<li><a href="#{i}">{line}</a></li>'

    table_of_contents_html += '</ul>'
    table_of_contents_html += '</div>'

    # insert table in article
    content_html_formatted = ''

    toc_inserted = False
    for line in content_html_with_ids.split('\n'):
        if not toc_inserted:
            if '<h2' in line:
                # print(line)
                toc_inserted = True
                content_html_formatted += table_of_contents_html
                content_html_formatted += line
                continue
        content_html_formatted += line

    return content_html_formatted



# pathogens = data['pathogens']
# products = data['products']

# pathogen_effects = data_pathogens[0]['effects'][0]

# output_text += f'## Prodotti\n\n'
# output_text += f'Ecco alcuni prodotti dell\'industria {industry_ad}{industry} che traggono beneficio dall\'ozono.\n\n'
# output_text += lst_to_blt(products)
# output_text += f'\n\n'



# pathogens_with_effects = []
# for pathogen in pathogens:
#     found_effects = False
#     for p in data_pathogens:
#         if p['name'] in pathogen:
#             p_effects_lst = p['effects']
#             if len(p_effects_lst) != 0: found_effects = True
#             else: break

#             p_name_ad = p['name_ad_1'].capitalize()
#             p_name_quantity = p['name_quantity']
#             p_type = p['type']

#             if p_name_quantity == 'singolare': 
#                 p_name_quantity_1 = 'è'
#                 p_name_quantity_2 = 'un'
#                 p_name_quantity_3 = 'causa'
#             else: 
#                 p_name_quantity_1 = 'sono'
#                 p_name_quantity_2 = 'dei'
#                 if p_type == 'batterio': p_type = 'batteri'
#                 p_name_quantity_3 = 'causano'

#             random.shuffle(p_effects_lst)
#             p_effects_txt = lst_to_txt(p_effects_lst[:3]).lower()

#             if p_type: p_type = f'{p_name_quantity_1} {p_name_quantity_2} {p_type} che'

#             pathogen_with_effects = f'**{pathogen}:** {p_name_ad}{pathogen} {p_type} {p_name_quantity_3} problemi di salute come {p_effects_txt}'
#             pathogen_with_effects = re.sub(' +', ' ', pathogen_with_effects)
#             break
#     if found_effects:
#         pathogens_with_effects.append(pathogen_with_effects)
#     else:
#         pathogens_with_effects.append(f'{pathogen}: no data')

# pathogens_llt = lst_to_txt(pathogens)

# output_text += f'## Quali patogeni l\'ozono elimina nell\'industria {industry_ad}{industry}?\n\n'
# output_text += f'L\'ozono elimina patogeni come {pathogens_llt} nell\'industria {industry_ad}{industry}.\n\n'
# output_text += f'Ecco una descrizione più dettagliata di questi patogeni e dei problemi che causano sulla salute umana.\n\n'
# output_text += lst_to_blt(pathogens_with_effects)
# output_text += f'\n\n'


for item in data:
    article = ''

    industry = item['industry']
    industry_ad = item['industry_ad']

    chain = item['chain']
    applications = item['applications']
    pathogens = item['pathogens']
    benefits = item['benefits']
    quality_effects = item['quality_effects']

    # title
    article += f'# Sanificazione ad ozono nell\'industria {industry_ad}{industry}: applicazioni e benefici \n\n'

    article += '![alt text](articles-images/public/ozono/sanificazione/industria/quarta-gamma/featured.jpg "Title")\n\n'

    # intro
    article += '''
    Nell'era moderna, la sicurezza alimentare è diventata una priorità incontestabile per l'industria alimentare, in particolare quando si tratta di prodotti freschi e pronti al consumo. 
    
    L'industria della quarta gamma, che si occupa della preparazione e confezionamento di alimenti freschi come insalate, frutta tagliata e snack sani, ha affrontato sfide sempre più pressanti per garantire la qualità e la sicurezza dei prodotti offerti ai consumatori. 
    
    In questo contesto, la sanificazione ad ozono si è affermata come una soluzione rivoluzionaria e altamente efficace per eliminare batteri, virus e contaminanti dai prodotti della quarta gamma, migliorando la shelf life e la sicurezza alimentare. 
    
    In questo articolo, esploreremo in dettaglio l'innovativo mondo della sanificazione ad ozono e il suo impatto positivo sull'industria della quarta gamma. Scopriremo come questa tecnologia sta ridefinendo gli standard di qualità e sicurezza, consentendo alle aziende di fornire prodotti freschi e salutari con la massima fiducia nei confronti dei consumatori.
    '''
    article = re.sub(' +', ' ', article)
    article += '\n\n'

    ## applications
    article += f'## Quali sono le applicazioni dell\'ozono nell\'industria {industry_ad}{industry}? \n\n'
    article += f'Qui sotto trovi una lista delle applicazioni dell\'ozono nell\'industria {industry_ad}{industry}.\n\n'
    bld = bold_blt(applications)
    article += lst_to_blt(bld)
    article += '\n\n'
    
    ## chain
    bld = bold_blt(chain)
    article += f'## In quali fasi della filiera {industry_ad}{industry} viene usato l\'ozono? \n\n'
    article += f'Qui sotto trovi una lista delle fasi della filiera dell\'industria {industry_ad}{industry} in cui viene utilizzato l\'ozono con successo.\n\n'
    bld = bold_blt(chain)
    article += lst_to_blt(bld)
    article += '\n\n'
    
    ## pathogens
    bld = bold_blt(pathogens)
    article += f'## Quali sono i patogeni più comuni nell\'industria {industry_ad}{industry} che l\'ozono può eliminare? \n\n'
    article += f'Qui sotto trovi una lista dei patogeni più comuni nell\'industria {industry_ad}{industry} che l\'ozono può eliminare.\n\n'
    bld = bold_blt(pathogens)
    article += lst_to_blt(bld)
    article += '\n\n'
    
    ## benefits
    bld = bold_blt(benefits)
    article += f'## Quali sono i benefici dell\'ozono nell\'industria {industry_ad}{industry}? \n\n'
    article += f'Qui sotto trovi una lista dei benefici dell\'ozono nell\'industria {industry_ad}{industry}.\n\n'
    bld = bold_blt(benefits)
    article += lst_to_blt(bld)
    article += '\n\n'
    
    ## quality effects
    bld = bold_blt(quality_effects)
    article += f'## Quali sono gli effetti dell\'ozono sulla qualità dei prodotti nell\'industria {industry_ad}{industry}? \n\n'
    article += f'Qui sotto trovi una lista degli effetti dell\'ozono sulla qualità dei prodotti nell\'industria {industry_ad}{industry}.\n\n'
    bld = bold_blt(quality_effects)
    article += lst_to_blt(bld)
    article += '\n\n'

    # print(item)

    industry_formatted = industry.replace(' ', '-')
    with open(f'articles/public/ozono/sanificazione/industria/{industry_formatted}.md', 'w', encoding='utf-8') as f:
        f.write(article)


# VIEWER
with open('articles/public/ozono/sanificazione/industria/quarta-gamma.md') as f:
    article_md = f.read()

word_count = len(article_md.split(' '))
reading_time_html = str(word_count // 200) + ' minutes'
word_count_html = str(word_count) + ' words'


article_html = markdown.markdown(article_md)

article_html = article_html.replace('<img', '<img class="featured-img"')


# GENERATE TABLE OF CONTENTS ----------------------------------------
article_html = generate_toc(article_html)


html = f'''
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="style-blog.css">
        <title>Document</title>
    </head>

    <body>
        <section class="my-96">
            <div class="container-md">
                {word_count_html} - {reading_time_html}
                {article_html}
            </div>
        </section>
    </body>

    </html>
'''

with open(f'article-viewer.html', 'w') as f:
    f.write(html)