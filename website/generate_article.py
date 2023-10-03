import json
import os
import random
import re
import markdown

from PIL import Image, ImageFont, ImageDraw, ImageColor

# for file in os.listdir('articles_tmp'):
#     os.remove(f'articles_tmp/{file}')


with open("database/json/articles.json", encoding='utf-8') as f:
    data = json.loads(f.read())


    
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


def img_resize(image_path):
    w, h = 768, 512

    img = Image.open(image_path)

    start_size = img.size
    end_size = (w, h)

    if start_size[0] / end_size [0] < start_size[1] / end_size [1]:
        ratio = start_size[0] / end_size[0]
        new_end_size = (end_size[0], int(start_size[1] / ratio))
    else:
        ratio = start_size[1] / end_size[1]
        new_end_size = (int(start_size[0] / ratio), end_size[1])

    img = img.resize(new_end_size)

    w_crop = new_end_size[0] - end_size[0]
    h_crop = new_end_size[1] - end_size[1]
    
    area = (
        w_crop // 2, 
        h_crop // 2,
        new_end_size[0] - w_crop // 2,
        new_end_size[1] - h_crop // 2
    )
    img = img.crop(area)

    output_path = image_path.replace('articles', 'articles-images')
    output_path = f'public/assets/images/{"-".join(image_path.split("/")[2:])}'
    img.save(f'{output_path}')

    return output_path


def img_pathogens(image_path):
    w, h = 768, 512
    img = Image.new(mode="RGB", size=(w, h), color='#047857')

    draw = ImageDraw.Draw(img)


    font_size = 40
    line_hight = 1.2
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    lines = ['Lista dei patogeni più comuni', 'nell\'industria della quarta gamma']
    for i, line in enumerate(lines):
        line_w = font.getsize(line)[0]
        draw.text(
            (w//2 - line_w//2, 30 + (font_size * line_hight * i)), 
            line, 
            (255,255,255), 
        font=font)
    

    list_y = 160 

    font_size = 24
    line_hight = 1.5
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    lines = [
        "1. Salmonella",
        "2. Escherichia coli",
        "3. Listeria monocytogenes",
        "4. Campylobacter",
        "5. Staphylococcus aureus",
        "6. Clostridium botulinum",
        "7. Vibrio parahaemolyticus",
        "8. Norovirus",
        ]
    for i, line in enumerate(lines):
        line_w = font.getsize(line)[0]
        draw.text(
            (30, list_y + (font_size * line_hight * i)), 
            line, 
            (255,255,255), 
        font=font)
        

    font_size = 24
    line_hight = 1.5
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    lines = [
        "9. Rotavirus",
        "10. Hepatitis A",
        "11. Shigella",
        "12. Giardia",
        "13. Cryptosporidium",
        "14. Clostridium perfringens",
        "15. Yersinia enterocolitica",
        "16. Bacillus cereus",
        # "17. Aeromonas",
        # "18. Plesiomonas shigelloides",
        # "19. Enterobacter sakazakii",
        # "20. Enterococcus faecalis",
        ]
    for i, line in enumerate(lines):
        line_w = font.getsize(line)[0]
        draw.text(
            (w//2 + 30, list_y + (font_size * line_hight * i)), 
            line, 
            (255,255,255), 
        font=font)
    
    output_path = image_path.replace('articles', 'articles-images')
    output_path = f'public/assets/images/{"-".join(image_path.split("/")[2:])}'
    img.save(f'{output_path}', format='JPEG', subsampling=0, quality=100)

    return output_path



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
    side_effects_product_quality = item['side_effects_product_quality']

    # title
    article += f'# Sanificazione ad ozono nell\'industria {industry_ad}{industry}: applicazioni e benefici \n\n'

    image_path = 'articles-images/public/ozono/sanificazione/industria/quarta-gamma/featured.jpg'
    image_path = img_resize(image_path)
    article += f'![alt text]({image_path} "Title")\n\n'

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

    applications_names = [x.split(':')[0] for x in applications]
    applications_intro = f'{applications_names[0].lower()}, {applications_names[1].lower()} e {applications_names[2].lower()}'
    article += f'Le applicazioni dell\'ozono nell\'industria {industry_ad}{industry} sono svariate, come {applications_intro}.\n\n'
    article += f'Qui sotto trovi una lista di queste applicazioni (quelle più comuni).\n\n'
    applications = bold_blt(applications)
    applications_name = [x.split(':')[0] for x in applications]
    article += lst_to_blt(applications)
    article += '\n\n'
    # article += '''
    # La tecnologia di ozonizzazione ha diverse applicazioni cruciali in diversi settori, soprattutto nell'industria alimentare e nella produzione di alimenti. Uno dei suoi utilizzi principali riguarda la sanificazione dell'acqua, dove viene sfruttata per trattare l'acqua utilizzata nel processo di lavaggio e igienizzazione delle verdure. Questo processo aiuta a eliminare batteri, virus e altri microrganismi patogeni presenti nell'acqua.

    # Oltre alla sanificazione dell'acqua, l'ozono viene impiegato anche nella disinfezione dell'aria all'interno degli impianti di produzione alimentare. Questo contribuisce notevolmente a ridurre la contaminazione microbica nell'ambiente di lavoro, garantendo la sicurezza degli alimenti prodotti.

    # Un altro impiego importante riguarda il lavaggio e la disinfezione dei prodotti alimentari stessi, come verdure e frutta. L'ozono viene utilizzato in questo processo per eliminare residui di pesticidi, batteri e altri contaminanti superficiali, migliorando così la qualità e la sicurezza degli alimenti.

    # Inoltre, l'ozonizzazione trova applicazione nella conservazione degli alimenti. Questa tecnologia è utilizzata per estendere la vita utile dei prodotti della quarta gamma, inibendo la crescita di microrganismi deterioranti e preservando la freschezza degli alimenti.

    # Non solo, ma l'ozono è anche impiegato nel trattamento delle acque reflue generate durante il processo di produzione alimentare. Questo contribuisce a rimuovere contaminanti organici e inorganici prima dello scarico nell'ambiente, riducendo l'impatto ambientale dell'industria alimentare.

    # L'ozono viene sfruttato anche per la rimozione di odori indesiderati dai prodotti alimentari stessi o dall'ambiente di produzione, migliorando l'esperienza del consumatore.

    # Un beneficio notevole è la possibilità di ridurre l'uso di agenti conservanti chimici grazie all'ozonizzazione, migliorando la percezione di prodotti più naturali da parte dei consumatori.

    # Inoltre, l'ozono contribuisce al miglioramento della qualità complessiva degli alimenti, mantenendone la freschezza, il colore e la consistenza.

    # Infine, l'ozono è prezioso anche per il prolungamento della shelf life degli alimenti, contribuendo a ridurre gli sprechi alimentari e i costi associati alla produzione, oltre a migliorare la sicurezza alimentare riducendo il rischio di contaminazione microbiologica dei prodotti.
    # '''
    # article = re.sub(' +', ' ', article)
    # article += '\n\n'
    
    ## chain
    article += f'## In quali fasi della filiera {industry_ad}{industry} viene usato l\'ozono? \n\n'
    
    names = [x.split(':')[0] for x in chain]
    article += f'L\'ozono viene utilizzato con successo nella maggior parte delle fasi della filiera {industry_ad}{industry}, dalla fase di {names[0].lower()} alla fase di {names[-1].lower()}.\n\n'

    article += f'Ecco elencate brevemente le varie fasi della filiera in cui viene usato.\n\n'
    bld = bold_blt(chain)
    article += lst_to_blt(bld)
    article += '\n\n'
    
    ## pathogens
    article += f'## Quali sono i patogeni più comuni nell\'industria {industry_ad}{industry} che l\'ozono può eliminare? \n\n'

    names = [x.split(':')[0] for x in pathogens]
    intro = f'{names[0]}, {names[1]} e {names[2]}'
    article += f'L\'ozono può eliminare la maggior parte dei patogeni che si trovano nei prodotti dell\'industria {industry_ad}{industry}, come {intro}.\n\n'
    
    article += f'Nella seguente lista, trovi elencati alcuni di questi patogeni (quelli più comuni).\n\n'
    bld = bold_blt(pathogens)
    article += lst_to_blt(bld)
    article += '\n\n'
    
    article += f'La seguente illustrazione mostra una lista più completa dei patogeni più comuni di questa industria, ordinati dal più frequente al mento frequente.\n\n'
    image_path = 'articles-images/public/ozono/sanificazione/industria/quarta-gamma/pathogens.jpg'
    image_path = img_pathogens(image_path)
    article += f'![alt text]({image_path} "Title")\n\n'
    
    ## benefits
    article += f'## Quali sono i benefici dell\'ozono nell\'industria {industry_ad}{industry}? \n\n'
    
    names = [x.split(':')[0] for x in benefits]
    intro = f'{names[0].lower()}, {names[1].lower()} e {names[2].lower()}'
    article += f'L\'ozono porta diversi benefici all\'industria {industry_ad}{industry}, come {intro}.\n\n'
    
    article += f'Qui sotto trovi una lista dei principali benefici che l\'ozono porta all\'industria {industry_ad}{industry}.\n\n'
    bld = bold_blt(benefits)
    article += lst_to_blt(bld)
    article += '\n\n'
    
    ## quality effects
    article += f'## Quali sono gli effetti negativi dell\'ozono sulla qualità dei prodotti nell\'industria {industry_ad}{industry}? \n\n'
    
    names = [x.split(':')[0] for x in side_effects_product_quality]
    intro = f'{names[0].lower()}, {names[1].lower()} e {names[2].lower()}'
    article += f'L\'ozono può avere effetti negativi sulla qualità dei prodotti nell\'industria {industry_ad}{industry} se usato in quantità eccessiva o per un tempo di esposizione prolungato, come {intro}.\n\n'

    article += f'Ecco elencati brevemente i potenziali effetti negativi dell\'ozono sulla qualità dei prodotti {industry_ad}{industry}.\n\n'
    bld = bold_blt(side_effects_product_quality)
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