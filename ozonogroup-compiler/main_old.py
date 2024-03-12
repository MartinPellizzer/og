import shutil
# shutil.copy2('/style.css', '/')

import markdown
import pathlib
import os

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from PIL import ImageColor 

import random
import re
import csv

encoding = 'utf-8'

# DB TO ARTICLE ----------------------------------------------------




w, h = 800, 600
generate_image_plain('assets/images/home/pasta-raw.jpg', w, h, 'assets/images/home/pasta.jpg')
generate_image_plain('assets/images/home/clinica-raw.jpg', w, h, 'assets/images/home/clinica.jpg')
generate_image_plain('assets/images/home/trasporti-raw.jpg', w, h, 'assets/images/home/trasporti.jpg')













shutil.copy2('index.html', 'public/index.html')




# else:
    #     applications = item['applications']
    #     chain = item['chain']
    #     pathogens = item['pathogens']
    #     benefits = item['benefits']
    #     side_effects_product_quality = item['side_effects_product_quality']

    #     industry_filename = industry.replace(' ', '-')

    #     # title
    #     title = f'Sanificazione ad Ozono nell\'industria {industry_ad}{industry.title()}'
    #     article += f'# Sanificazione ad ozono nell\'industria {industry_ad}{industry}: applicazioni e benefici \n\n'

    #     img_filepath = generate_featured_image(attribute, industry)
    #     article += f'![tesst]({img_filepath} "Title")\n\n'

    #     # INTRODUCTION ----------------------------------------------------------------------------------------------
    #     applications_names = [x.split(':')[0] for x in applications]
    #     applications_intro = f'{applications_names[0].lower()}, {applications_names[1].lower()} e {applications_names[2].lower()}'
        
    #     chain_names = [x.split(':')[0] for x in chain]
    #     chain_intro = f'dalla fase di {chain_names[0].lower()} alla fase di {chain_names[-1].lower()}'
    #     pathogens_names = [x.split(':')[0] for x in item['pathogens_bacteria']]
    #     pathogens_intro = f'{pathogens_names[0]}, {pathogens_names[1]} e {pathogens_names[2]}'
        
    #     benefits_names = [x.split(':')[0] for x in benefits]
    #     benefits_intro = f'{benefits_names[0].lower()}, {benefits_names[1].lower()} e {benefits_names[2].lower()}'
    #     quality_effects_names = [x.split(':')[0] for x in side_effects_product_quality]
    #     quality_effects_intro = f'{quality_effects_names[0].lower()}, {quality_effects_names[1].lower()} e {quality_effects_names[2].lower()}'
        
    #     article += f'L\'ozono (O3) è un gas che viene utilizzato nell\'industria {industry_ad}{industry} per applicazioni come {applications_intro}.\n\n'
    #     article += f'Viene impiegato in diverse fasi della filiera di questa industria, {chain_intro}, ed è in grado di eliminare diversi patogeni come {pathogens_intro}.\n\n'
    #     # article += f'Inoltre, è in grado di portare diversi benefici come {benefits_intro}. Però, può anche influire negativamente sulla qualità dei prodotti se usato scorrettamente, come {quality_effects_intro}.\n\n'
    #     article += f'Inoltre, è in grado di portare diversi benefici come {benefits_intro}. Però, può anche influire negativamente sulla qualità dei prodotti se usato scorrettamente.\n\n'
    #     article += f'In questo articolo vengono descritte nel dettaglio le applicazioni dell\'ozno nell\'industria {industry_ad}{industry} e quali sono i benefici che questo gas porta in questa industria.\n\n'

    #     article = re.sub(' +', ' ', article)
    #     article += '\n\n'

    #     # APPLICATIONS ----------------------------------------------------------------------------------------------
    #     article += f'## Quali sono le applicazioni dell\'ozono nell\'industria {industry_ad}{industry}? \n\n'

    #     # i = 0
    #     # for application in item['applications_extended']:
    #     #     i += 1
    #     #     application_title = application['title']
    #     #     application_description = '\n\n'.join(application['description'])

    #     #     article += f'### {i}. {application_title} \n\n'
    #     #     article += f'{application_description} \n\n'
    #     article += lst_to_blt(bold_blt(applications)) + '\n\n'




    #     # applications_names = [x.split(':')[0] for x in applications]
    #     # applications_intro = f'{applications_names[0].lower()}, {applications_names[1].lower()} e {applications_names[2].lower()}'
    #     # article += f'Le applicazioni dell\'ozono nell\'industria {industry_ad}{industry} sono svariate, come {applications_intro}.\n\n'
    #     # article += f'Qui sotto trovi una lista di queste applicazioni (quelle più comuni).\n\n'
    #     # applications = bold_blt(applications)
    #     # applications_name = [x.split(':')[0] for x in applications]
    #     # article += lst_to_blt(applications)
    #     # article += '\n\n'
        
    #     # lst = [item.split(':')[0].replace('*', '') for item in applications]
    #     # article += f'La seguente illustrazione riassume le applicazioni dell\'ozono nell\'idustria {industry_ad}{industry}.\n\n'
    #     # image_path = f'articles-images/public/ozono/sanificazione/industria/{industry_filename}/applicazioni.jpg'
    #     # image_path = img_list_center(image_path, 'Applicazioni dell\'ozono', lst)
    #     # image_path = '/' + '/'.join(image_path.split('/')[1:])
    #     # article += f'![alt text]({image_path} "Title")\n\n'
        
    #     ## chain
    #     article += f'## In quali fasi della filiera {industry_ad}{industry} viene usato l\'ozono? \n\n'

    #     names = [x.split(':')[0] for x in chain]
    #     article += f'L\'ozono viene utilizzato con successo nella maggior parte delle fasi della filiera {industry_ad}{industry}, dalla fase di {names[0].lower()} alla fase di {names[-1].lower()}.\n\n'

    #     article += f'Ecco elencate brevemente le varie fasi della filiera in cui viene usato.\n\n'
    #     bld = bold_blt(chain)
    #     article += lst_to_blt(bld)
    #     article += '\n\n'

    #     lst = [item.split(':')[0].replace('*', '') for item in chain]
    #     article += f'La seguente illustrazione riassume le fasi della filiera nell\'idustria {industry_ad}{industry} dove l\'ozono viene usato.\n\n'
    #     image_path = f'articles-images/public/ozono/sanificazione/{industry_filename}/filiera.jpg'
    #     image_path = img_list_center(image_path, 'Fasi della filiera', lst)
    #     image_path = '/' + '/'.join(image_path.split('/')[1:])
    #     article += f'![alt text]({image_path} "Title")\n\n'

    #     #####################################################################################################
    #     # PATHOGENS
    #     #####################################################################################################
    #     article += f'## Quali sono i patogeni più comuni nell\'industria {industry_ad}{industry} che l\'ozono può eliminare? \n\n'

    #     # INTRO
    #     bacteria_lst = [x.split(':')[0].split('(')[0].strip() for x in item['pathogens_bacteria'][:3]]
    #     virus_lst = [x.split(':')[0].split('(')[0].strip() for x in item['pathogens_virus'][:3]]
    #     fungi_lst = [x.split(':')[0].split('(')[0].strip() for x in item['pathogens_fungi'][:3]]
    #     protozoa_lst = [x.split(':')[0].split('(')[0].strip() for x in item['pathogens_protozoa'][:3]]
    #     parasites_lst = [x.split(':')[0].split('(')[0].strip() for x in item['pathogens_parasites'][:3]]
    #     bacteria_txt = lst_to_txt(bacteria_lst)
    #     virus_txt = lst_to_txt(virus_lst)
    #     fungi_txt = lst_to_txt(fungi_lst)
    #     protozoa_txt = lst_to_txt(protozoa_lst)
    #     parasites_txt = lst_to_txt(parasites_lst)
    #     article += f'L\'ozono elimina i batteri patogeni più comuni nell\'industria {industry_ad}{industry}, come {bacteria_txt}.\n\n'
    #     article += f'Elimina ance i virus (come {virus_txt}), i funghi (come {fungi_txt}) e i protozoi ({protozoa_txt}).\n\n'
    #     article += f'Infine, repelle diversi tipi di insetti e parassiti (come {parasites_txt}).\n\n'

    #     # CHEAT SHEET
    #     lst = []
    #     pathogens_lst = [x.split(':')[0].split('(')[0] for x in item['pathogens_bacteria'][:7]]
    #     pathogens_lst.insert(0, 'Batteri')
    #     lst.append(pathogens_lst)
    #     pathogens_lst = [x.split(':')[0].split('(')[0] for x in item['pathogens_virus'][:7]]
    #     pathogens_lst.insert(0, 'Virus')
    #     lst.append(pathogens_lst)
    #     pathogens_lst = [x.split(':')[0].split('(')[0] for x in item['pathogens_fungi'][:7]]
    #     pathogens_lst.insert(0, 'Funghi')
    #     lst.append(pathogens_lst)
    #     pathogens_lst = [x.split(':')[0].split('(')[0] for x in item['pathogens_protozoa'][:7]]
    #     pathogens_lst.insert(0, 'Protozoi')
    #     lst.append(pathogens_lst)
    #     pathogens_lst = [x.split(':')[0].split('(')[0] for x in item['pathogens_parasites'][:7]]
    #     pathogens_lst.insert(0, 'Parassiti')
    #     lst.append(pathogens_lst)

    #     img_path = f'articles/public/ozono/sanificazione/{industry_filename}/patogeni.jpg'
    #     img_path = img_cheasheet(item, 'Patogeni comuni nell\'industria', lst, 'patogeni')
    #     img_path = '/' + '/'.join(img_path.split('/')[1:])
    #     article += f'La seguente immagine mostra un elenco dei patogeni più comuni in questa industria.\n\n'
    #     article += f'![alt]({img_path} "title")\n\n'

    #     article += f'A seguire, viene data una breve descrizione di ogni singolo patogeno. I patogeni sono divisi per categorie, quali batteri, virus, fungi, protozoi e parassiti.\n\n'


    #     # img_filepath = img_pathogens(item)

    #     # bacteria
    #     article += f'### Batteri \n\n'
    #     article += f'Ecco una descrizione dei batteri più comuni in questa industria.\n\n'
    #     lst = bold_blt(item['pathogens_bacteria'])
    #     article += lst_to_blt(lst)
    #     article += '\n\n'
        
    #     # virus
    #     article += f'### Virus \n\n'
    #     article += f'Ecco una descrizione dei virus più comuni in questa industria.\n\n'
    #     lst = bold_blt(item['pathogens_virus'])
    #     article += lst_to_blt(lst)
    #     article += '\n\n'
        
    #     # fungi
    #     article += f'### Funghi \n\n'
    #     article += f'Ecco una descrizione dei funghi più comuni in questa industria.\n\n'
    #     lst = bold_blt(item['pathogens_fungi'])
    #     article += lst_to_blt(lst)
    #     article += '\n\n'
        
    #     # protozoa
    #     article += f'### Protozoi \n\n'
    #     article += f'Ecco una descrizione dei protozoi più comuni in questa industria.\n\n'
    #     lst = bold_blt(item['pathogens_protozoa'])
    #     article += lst_to_blt(lst)
    #     article += '\n\n'
        
    #     # parasites
    #     article += f'### Parassiti \n\n'
    #     article += f'Ecco una descrizione dei parassiti più comuni in questa industria.\n\n'
    #     lst = bold_blt(item['pathogens_parasites'])
    #     article += lst_to_blt(lst)
    #     article += '\n\n'

    #     # lst = [item.split(':')[0].replace('*', '') for item in pathogens]
    #     # article += f'La seguente illustrazione mostra una lista più completa dei patogeni più comuni di questa industria, ordinati dal più frequente al mento frequente.\n\n'
    #     # image_path = f'articles-images/public/ozono/sanificazione/industria/{industry_filename}/patogeni.jpg'
    #     # image_path = img_list_double(image_path, 'Lista dei patogeni più comuni', lst)
    #     # image_path = '/' + '/'.join(image_path.split('/')[1:])
    #     # article += f'![alt text]({image_path} "Title")\n\n'

    #     ## benefits
    #     article += f'## Quali sono i benefici dell\'ozono nell\'industria {industry_ad}{industry}? \n\n'
        
    #     names = [x.split(':')[0].replace('*', '') for x in benefits]
    #     intro = f'{names[0].lower()}, {names[1].lower()} e {names[2].lower()}'
    #     article += f'L\'ozono porta diversi benefici all\'industria {industry_ad}{industry}, come {intro}.\n\n'
        
    #     article += f'Qui sotto trovi una lista dei principali benefici che l\'ozono porta all\'industria {industry_ad}{industry}.\n\n'
    #     bld = bold_blt(benefits)
    #     article += lst_to_blt(bld)
    #     article += '\n\n'

    #     benefits_plain = [item.split(':')[0].replace('*', '') for item in benefits]
    #     article += f'La seguente illustrazione riassume i benefici che l\'ozono porta a questa idustria.\n\n'
    #     image_path = f'articles-images/public/ozono/sanificazione/industria/{industry_filename}/benefici.jpg'
    #     image_path = img_list_center(image_path, 'Benefici dell\'ozono', benefits_plain)
    #     image_path = '/' + '/'.join(image_path.split('/')[1:])
    #     article += f'![alt text]({image_path} "Title")\n\n'
        
    #     ## quality effects
    #     article += f'## Quali sono gli effetti negativi dell\'ozono sulla qualità dei prodotti nell\'industria {industry_ad}{industry}? \n\n'
        
    #     names = [x.split(':')[0].replace('*', '') for x in side_effects_product_quality]
    #     intro = f'{names[0].lower()}, {names[1].lower()} e {names[2].lower()}'
    #     article += f'L\'ozono può avere effetti negativi sulla qualità dei prodotti nell\'industria {industry_ad}{industry} se usato in quantità eccessiva o per un tempo di esposizione prolungato, come {intro}.\n\n'
    #     article += f'Si consiglia quindi di contattare un professionista prima di applicare questa tecnologia di sanificazione.\n\n'

    #     article += f'Ecco elencati brevemente i potenziali effetti negativi dell\'ozono sulla qualità dei prodotti {industry_ad}{industry}.\n\n'
    #     bld = bold_blt(side_effects_product_quality)
    #     article += lst_to_blt(bld)
    #     article += '\n\n'

    #     lst = [item.split(':')[0].replace('*', '') for item in side_effects_product_quality]
    #     article += f'La seguente illustrazione riassume gli effetti collaterali che l\'ozono può avere sulla qualità dei prodotti di questa idustria.\n\n'
    #     image_path = f'articles-images/public/ozono/sanificazione/{industry_filename}/qualita-effetti.jpg'
    #     image_path = img_list_center(image_path, 'Effetti dell\'ozono sulla qualità dei prodotti', lst)
    #     image_path = '/' + '/'.join(image_path.split('/')[1:])
    #     article += f'![alt text]({image_path} "Title")\n\n'

    #     # print(item)

    #     industry_formatted = industry.replace(' ', '-')
    #     with open(f'articles/public/ozono/sanificazione/{industry_formatted}.md', 'w', encoding='utf-8') as f:
    #         f.write(article)





# def gen_article_applications():
    # folderpath = 'articles/public/ozono/sanificazione/applicazioni'
    # for filename in os.listdir(folderpath):
    #     print(filename)
    #     filepath_in = f'{folderpath}/{filename}'
    #     filepath_out = filepath_in.replace('articles/', '').replace('.json', '.html')
    #     data = util.json_read(filepath_in)

    #     keyword = filename.replace('.json', '')
    #     title = keyword.title().replace('-', ' ')
    #     application = title.lower()

    #     article_html = ''
    #     article_html += f'<h1>{title}</h1>' + '\n'
    #     article_html += f'<img src="/assets/images/ozono-sanificazione-{keyword}-introduzione.jpg" alt="">' + '\n'
    #     article_html += util.text_format_1N1_html(data['intro_1']) + '\n'
    #     article_html += util.text_format_1N1_html(data['intro_2']) + '\n'
    #     article_html += f'<h2>Cos\'è la sanificazione ad ozono per {application}?</h2>' + '\n'
    #     article_html += f'<img src="/assets/images/ozono-sanificazione-{keyword}-definizione.jpg" alt="">' + '\n'
    #     article_html += util.text_format_1N1_html(data['intro_1']) + '\n'
    #     article_html += f'<h2>Quali problemi risolve la sanificazione ad ozono per {application}?</h2>' + '\n'
    #     article_html += f'<img src="/assets/images/ozono-sanificazione-{keyword}-problemi.jpg" alt="">' + '\n'
    #     article_html += util.text_format_1N1_html(data['problems_text']) + '\n'
    #     article_html += '<ul>' + ''.join([f'<li>{item}</li>\n' for item in data['problems_list']]) + '</ul>' + '\n'
    #     article_html += f'<h2>Quali sono i benefici della sanificazione ad ozono per {application}?</h2>' + '\n'
    #     article_html += f'<img src="/assets/images/ozono-sanificazione-{keyword}-benefici.jpg" alt="">' + '\n'
    #     article_html += util.text_format_1N1_html(data['benefits_text']) + '\n'
    #     article_html += '<ul>' + ''.join([f'<li>{item}</li>\n' for item in data['benefits_list']]) + '</ul>' + '\n'
    #     article_html += f'<h2>Quali sono le applicazioni della sanificazione ad ozono per {application}?</h2>' + '\n'
    #     article_html += f'<img src="/assets/images/ozono-sanificazione-{keyword}-applicazioni.jpg" alt="">' + '\n'
    #     article_html += util.text_format_1N1_html(data['applications_text']) + '\n'
    #     article_html += '<ul>' + ''.join([f'<li>{item}</li>\n' for item in data['applications_list']]) + '</ul>' + '\n'

    #     # BREADCRUMBS  ---------------------------------------------
    #     filepath_chunks = filepath_in.split('\\')
    #     breadcrumbs = generate_breadcrumbs(filepath_chunks)

    #     # READING TIME  --------------------------------------------
    #     reading_time = len(article_html.split(' ')) // 200

    #     # PUBLICATION DATE  ----------------------------------------
    #     publishing_date = ''
    #     try: publishing_date = md.Meta['publishing_date'][0]
    #     except: pass

    #     # AUTHOR ----------------------------------------
    #     author = 'Ozonogroup Staff'
    #     try: author = md.Meta['author'][0]
    #     except: pass

    #     last_update_date = ''
    #     try: last_update_date = md.Meta['last_update_date'][0]
    #     except: pass

    #     # GENERATE TABLE OF CONTENTS ----------------------------------------
    #     article_html = generate_toc(article_html)

    #     with open('components/header.html', encoding='utf-8') as f:
    #         header_html = f.read()

    #     html = f'''
    #         <!DOCTYPE html>
    #         <html lang="en">

    #         <head>
    #             <meta charset="UTF-8">
    #             <meta name="viewport" content="width=device-width, initial-scale=1.0">
    #             <link rel="stylesheet" href="/style-blog.css">
    #             <link rel="stylesheet" href="/util.css">
    #             <title>{title}</title>
    #             {GOOGLE_TAG}
    #         </head>

    #         <body>
    #             <section class="header-section">
    #                 <div class="container-xl h-full">
    #                     {header_html}
    #                 </div>
    #             </section>

    #             <section class="breadcrumbs-section">
    #                 <div class="container-xl h-full">
    #                     <a href="/index.html">Home</a>{''.join(breadcrumbs)}
    #                 </div>
    #             </section>

    #             <section class="meta-section mt-48">
    #                 <div class="container-md h-full">
    #                     <div class="flex justify-between mb-8">
    #                         <span>by {author} • {publishing_date}</span>
    #                         <span>Tempo Lettura: {reading_time} min</span>
    #                     </div>
    #                 </div>
    #             </section>

    #             <section class="container-md">
    #                 {article_html}
    #             </section>

    #             <section class="footer-section">
    #                 <div class="container-xl h-full">
    #                     <footer class="flex items-center justify-center">
    #                         <span class="text-white">Ozonogroup s.r.l. | Tutti i diritti riservati</span>
    #                     </footer>
    #                 </div>
    #             </section>
    #         </body>

    #         </html>
    #     '''

    #     chunks = filepath_out.split('/')[:-1]
    #     chunk_curr = ''
    #     for chunk in chunks:
    #         chunk_curr += f'{chunk}/'
    #         try: os.makedirs(chunk_curr)
    #         except: pass

    #     util.file_write(filepath_out, html)


    # articles_folder = 'articles/public/ozono/sanificazione/applicazioni'
    # for article_filename in os.listdir(articles_folder):
    #     article_filename_no_ext = article_filename.replace('.json', '')

    #     article_filepath = f'{article_filename}/{article_filename}'
    #     images_articles_folder = f'C:/og-assets/images/articles'
    #     images_article_folder = f'{images_articles_folder}/{article_filename_no_ext}'
    #     images_filepath = [f'{images_article_folder}/{filepath}' for filepath in os.listdir(images_article_folder)]

    #     images_filpaths_out = [
    #         f'public/assets/images/ozono-sanificazione-{article_filename_no_ext}-introduzione.jpg',
    #         f'public/assets/images/ozono-sanificazione-{article_filename_no_ext}-definizione.jpg',
    #         f'public/assets/images/ozono-sanificazione-{article_filename_no_ext}-problemi.jpg',
    #         f'public/assets/images/ozono-sanificazione-{article_filename_no_ext}-benefici.jpg',
    #         f'public/assets/images/ozono-sanificazione-{article_filename_no_ext}-applicazioni.jpg',
    #     ]
    #     for image_filepath_out in images_filpaths_out:
    #         image_filepath = images_filepath.pop(0)
    #         if not os.path.exists(image_filepath_out):
    #             img_resize_2(
    #                 image_filepath, 
    #                 image_filepath_out
    #             )

