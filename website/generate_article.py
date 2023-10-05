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



###################################################################################################################
# images
###################################################################################################################
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


def img_list_double(image_path, title, lst):
    w, h = 768, 512
    background_color = "#f8fafc"
    background_color = "#047857"
    background_color = "#1d4ed8"
    font_color = '#0f172a'
    font_color = '#ffffff'

    half_len = len(lst) / 2
    if half_len.is_integer(): 
        sublist_1_len = int(half_len)
        sublist_2_len = int(half_len)
    else: 
        sublist_1_len = int(half_len + 1)
        sublist_2_len = int(half_len)

    if sublist_1_len > 8: 
        sublist_1 = lst[:8]
        sublist_2 = lst[8:16]
    else: 
        sublist_1 = lst[:sublist_1_len]
        sublist_2 = lst[sublist_1_len:sublist_1_len+sublist_2_len]

    img = Image.new(mode="RGB", size=(w, h), color=background_color)

    draw = ImageDraw.Draw(img)


    font_size = 40
    line_hight = 1.2
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    lines = ['Lista dei patogeni più comuni', 'nell\'industria della quarta gamma']
    lines = [title, 'nell\'industria della quarta gamma']
    # lines = [title]
    for i, line in enumerate(lines):
        line_w = font.getsize(line)[0]
        draw.text((w//2 - line_w//2, 30 + (font_size * line_hight * i)), line, font_color, font=font)
    

    list_y = 160 
    font_size = 24
    line_hight = 1.5
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)


    lines = [f'{i + 1}. {item}' for i, item in enumerate(sublist_1)]
    for i, line in enumerate(lines):
        line_w = font.getsize(line)[0]
        draw.text((30, list_y + (font_size * line_hight * i)), line, font_color, font=font)
        
    lines = [f'{i + 1 + len(sublist_1)}. {item}' for i, item in enumerate(sublist_2)]
    for i, line in enumerate(lines):
        line_w = font.getsize(line)[0]
        draw.text((w//2 + 30, list_y + (font_size * line_hight * i)), line, font_color, font=font)
    
    output_path = image_path.replace('articles', 'articles-images')
    output_path = f'public/assets/images/{"-".join(image_path.split("/")[2:])}'
    img.save(f'{output_path}', format='JPEG', subsampling=0, quality=100)

    return output_path


def img_list_center(image_path, title, lst):
    w, h = 768, 512
    background_color = "#047857"
    background_color = "#1d4ed8"
    font_color = '#ffffff'

    sublist_1 = lst[:8]
    sublist_1_len = len(sublist_1)

    img = Image.new(mode="RGB", size=(w, h), color=background_color)
    draw = ImageDraw.Draw(img)

    font_size = 40
    line_hight = 1.2
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    lines = ['Lista dei patogeni più comuni', 'nell\'industria della quarta gamma']
    lines = [title, 'nell\'industria della quarta gamma']
    # lines = [title]
    for i, line in enumerate(lines):
        line_w = font.getsize(line)[0]
        draw.text((w//2 - line_w//2, 30 + (font_size * line_hight * i)), line, font_color, font=font)
    
    list_y = 160 
    font_size = 24
    line_hight = 1.5
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    lines = [f'{i + 1}. {item}' for i, item in enumerate(sublist_1)]
    for i, line in enumerate(lines):
        line_w = font.getsize(line)[0]
        draw.text((w//2 - line_w//2, list_y + (font_size * line_hight * i)), line, font_color, font=font)
        
    output_path = image_path.replace('articles', 'articles-images')
    output_path = f'public/assets/images/{"-".join(image_path.split("/")[2:])}'
    img.save(f'{output_path}', format='JPEG', subsampling=0, quality=100)

    return output_path


def img_pathogens(item, image_path):
    industry = item['industry']
    industry_ad = item['industry_ad']
    pathogens_bacteria = item['pathogens_bacteria']
    pathogens_virus = item['pathogens_virus']
    pathogens_fungi = item['pathogens_fungi']
    pathogens_protozoa = item['pathogens_protozoa']
    pathogens_parasites = item['pathogens_parasites']

    pathogens_parasites = [f'{x.split("(")[0]}' for x in pathogens_parasites]

    w, h = 768, 1152
    background_color = "#1d4ed8"
    background_color = "#eff6ff"
    blue = "#1d4ed8"
    blue_light = "#eff6ff"
    blue_light_1 = "#dbeafe"
    blue_light_2 = "#bfdbfe"
    white = '#ffffff'
    dark = '#0f172a'

    img = Image.new(mode="RGB", size=(w, h), color=background_color)
    draw = ImageDraw.Draw(img)

    font_size = 36
    line_hight = 1.5
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = f'Patogeni nell\'idustria {industry_ad}{industry}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.rectangle(((0, 0), (w, 30+30+line_h)), fill="#1d4ed8")
    draw.text((30, 30), line, white, font=font)


    # rectangle from text
    # line_h = 0
    # line = f'this is a test'
    # x = 100
    # y = 300 + 20 + line_h
    # line_w = font.getbbox(line)[2]
    # line_h = font.getbbox(line)[3]
    # draw.rectangle(((x-10, y-10), (x+10+line_w, y+10+line_h)), fill=blue)
    # draw.text((x, y), line, white, font=font)
    
    # line = f'why am I even doing this?'
    # x = 100
    # y = y + 20 + line_h
    # line_w = font.getbbox(line)[2]
    # line_h = font.getbbox(line)[3]
    # draw.rectangle(((x-10, y-10), (x+10+line_w, y+10+line_h)), fill=blue_light)
    # draw.text((x, y), line, dark, font=font)
    
    # line = f'another line like this'
    # x = 100
    # y = y + 20 + line_h
    # line_w = font.getbbox(line)[2]
    # line_h = font.getbbox(line)[3]
    # draw.rectangle(((x-10, y-10), (x+10+line_w, y+10+line_h)), fill=blue)
    # draw.text((x, y), line, white, font=font)
    
    # line = f'again and again'
    # x = 100
    # y = y + 20 + line_h
    # line_w = font.getbbox(line)[2]
    # line_h = font.getbbox(line)[3]
    # draw.rectangle(((x-10, y-10), (x+10+line_w, y+10+line_h)), fill=blue_light)
    # draw.text((x, y), line, dark, font=font)

    font_size = 24
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)

    line_h = 0
    x = 50
    y = 130
    bg = 0
    rect_w = w//2
    lines = [x.split(':')[0].replace('*', '') for x in pathogens_bacteria]

    line = "Batteri"
    line_h = font.getbbox(line)[3]
    draw.rectangle(((x-10, y-10), (rect_w, y+10+line_h)), fill=blue)
    draw.text((x, y), line, white, font=font)

    for line in lines:
        y = y + 20 + line_h
        line_w = font.getbbox(line)[2]
        line_h = font.getbbox(line)[3]
        if bg == 0:
            bg = 1
            draw.rectangle(((x-10, y-10), (rect_w, y+10+line_h)), fill=blue_light)
            draw.text((x, y), line, dark, font=font)
        else:
            bg = 0
            draw.rectangle(((x-10, y-10), (rect_w, y+10+line_h)), fill=blue_light_1)
            draw.text((x, y), line, dark, font=font)

    # quit()



    # list_y = 160 
    # font_size = 24
    # line_height = 1.5
    # col_1_x = int(w * 0.07)
    # col_2_x = int(w * 0.5 + col_1_x)
    # col_3_x = int(w * 0.9)
    # font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)

    # lines = [x.split(':')[0].replace('*', '') for x in pathogens_bacteria]
    # max_line_height = 0
    # for i, line in enumerate(lines):
    #     line_h = font.getbbox(line)[3]
    #     if max_line_height < line_h: max_line_height = line_h
        
    # bg = 0
    # for i, line in enumerate(lines):
    #     line_h = font.getbbox(line)[3]
    #     # line_h = max_line_height
    #     rect_y = list_y + (line_h * line_height * i) 
    #     rect_h = list_y + (line_h * line_height * i) + (line_h)
    #     if bg == 0: 
    #         bg = 1
    #         draw.rectangle(((30, rect_y), (w, rect_h)), fill="#1d4ed8")
    #     else: 
    #         bg = 0
    #         draw.rectangle(((30, rect_y), (w, rect_h)), fill="#eff6ff")

    # for i, line in enumerate(lines):
    #     line_w = font.getsize(line)[0]
    #     draw.text((col_1_x, list_y + (font_size * line_height * i)), line, dark, font=font)
    #     draw.text((col_1_x, list_y + (font_size * line_height * i)), line, dark, font=font)
    # # draw.rectangle(((30, list_y), (w, list_y + (max_line_height * line_height * (len(lines)-1)))), fill="#1d4ed8")
    
    # for i, line in enumerate(lines):
    #     line_w = font.getsize(line)[0]
    #     draw.text((col_1_x, list_y + (font_size * line_height * i)), line, dark, font=font)

    # lines = [x.split(':')[0].replace('*', '') for x in pathogens_virus]
    # for i, line in enumerate(lines):
    #     line_w = font.getsize(line)[0]
    #     draw.text((col_1_x, list_y + (font_size * line_height * i) + 300), line, dark, font=font)

    # lines = [x.split(':')[0].replace('*', '') for x in pathogens_fungi]
    # for i, line in enumerate(lines):
    #     line_w = font.getsize(line)[0]
    #     draw.text((col_1_x, list_y + (font_size * line_height * i) + 600), line, dark, font=font)

    # lines = [x.split(':')[0].replace('*', '') for x in pathogens_protozoa]
    # for i, line in enumerate(lines):
    #     line_w = font.getsize(line)[0]
    #     draw.text((col_2_x, list_y + (font_size * line_height * i)), line, dark, font=font)

    # lines = [x.split(':')[0].replace('*', '') for x in pathogens_parasites]
    # for i, line in enumerate(lines):
    #     line_w = font.getsize(line)[0]
    #     draw.text((col_2_x, list_y + (font_size * line_height * i) + 300), line, dark, font=font)

    output_path = image_path.replace('articles', 'articles-images')
    output_path = f'public/assets/images/{"-".join(image_path.split("/")[2:])}'
    img.save(f'{output_path}', format='JPEG', subsampling=0, quality=100)

    return output_path



###################################################################################################################
# articles
###################################################################################################################
for item in data:
    article = ''

    industry = item['industry']
    industry_ad = item['industry_ad']

    chain = item['chain']
    applications = item['applications']
    # pathogens_plain = item['pathogens_plain']
    pathogens = item['pathogens']
    benefits = item['benefits']
    side_effects_product_quality = item['side_effects_product_quality']

    industry_filename = industry.replace(' ', '-')

    # title
    article += f'# Sanificazione ad ozono nell\'industria {industry_ad}{industry}: applicazioni e benefici \n\n'

    image_path = f'articles-images/public/ozono/sanificazione/industria/{industry_filename}/featured.jpg'
    image_path = img_resize(image_path)
    image_path = '/'.join(image_path.split('/')[1:])
    article += f'![alt text](/{image_path} "Title")\n\n'

    # INTRODUCTION ----------------------------------------------------------------------------------------------
    applications_names = [x.split(':')[0] for x in applications]
    applications_intro = f'{applications_names[0].lower()}, {applications_names[1].lower()} e {applications_names[2].lower()}'
    
    chain_names = [x.split(':')[0] for x in chain]
    chain_intro = f'dalla fase di {chain_names[0].lower()} alla fase di {chain_names[-1].lower()}'
    pathogens_names = [x.split(':')[0] for x in pathogens]
    pathogens_intro = f'{pathogens_names[0]}, {pathogens_names[1]} e {pathogens_names[2]}'
    
    benefits_names = [x.split(':')[0] for x in benefits]
    benefits_intro = f'{benefits_names[0].lower()}, {benefits_names[1].lower()} e {benefits_names[2].lower()}'
    quality_effects_names = [x.split(':')[0] for x in side_effects_product_quality]
    quality_effects_intro = f'{quality_effects_names[0].lower()}, {quality_effects_names[1].lower()} e {quality_effects_names[2].lower()}'
    
    article += f'L\'ozono (O3) è un gas che viene utilizzato nell\'industria {industry_ad}{industry} per applicazioni come {applications_intro}.\n\n'
    article += f'Viene impiegato in diverse fasi della filiera di questa industria, {chain_intro}, ed è in grado di eliminare diversi patogeni come {pathogens_intro}.\n\n'
    article += f'Inoltre, è in grado di portare diversi benefici come {benefits_intro}. Però, può anche influire negativamente sulla qualità dei prodotti se usato scorrettamente, come {quality_effects_intro}.\n\n'
    article += f'In questo articolo vengono descritte nel dettaglio le applicazioni dell\'ozno nell\'industria {industry_ad}{industry} e quali sono i benefici che questo gas porta in questa industria.\n\n'

    article = re.sub(' +', ' ', article)
    article += '\n\n'

    # APPLICATIONS ----------------------------------------------------------------------------------------------
    article += f'## Quali sono le applicazioni dell\'ozono nell\'industria {industry_ad}{industry}? \n\n'

    applications_names = [x.split(':')[0] for x in applications]
    applications_intro = f'{applications_names[0].lower()}, {applications_names[1].lower()} e {applications_names[2].lower()}'
    article += f'Le applicazioni dell\'ozono nell\'industria {industry_ad}{industry} sono svariate, come {applications_intro}.\n\n'
    article += f'Qui sotto trovi una lista di queste applicazioni (quelle più comuni).\n\n'
    applications = bold_blt(applications)
    applications_name = [x.split(':')[0] for x in applications]
    article += lst_to_blt(applications)
    article += '\n\n'
    
    lst = [item.split(':')[0].replace('*', '') for item in applications]
    article += f'La seguente illustrazione riassume le applicazioni dell\'ozono nell\'idustria {industry_ad}{industry}.\n\n'
    image_path = f'articles-images/public/ozono/sanificazione/industria/{industry_filename}/applicazioni.jpg'
    image_path = img_list_center(image_path, 'Applicazioni dell\'ozono', lst)
    image_path = '/' + '/'.join(image_path.split('/')[1:])
    article += f'![alt text]({image_path} "Title")\n\n'
    
    ## chain
    article += f'## In quali fasi della filiera {industry_ad}{industry} viene usato l\'ozono? \n\n'

    names = [x.split(':')[0] for x in chain]
    article += f'L\'ozono viene utilizzato con successo nella maggior parte delle fasi della filiera {industry_ad}{industry}, dalla fase di {names[0].lower()} alla fase di {names[-1].lower()}.\n\n'

    article += f'Ecco elencate brevemente le varie fasi della filiera in cui viene usato.\n\n'
    bld = bold_blt(chain)
    article += lst_to_blt(bld)
    article += '\n\n'

    lst = [item.split(':')[0].replace('*', '') for item in chain]
    article += f'La seguente illustrazione riassume le fasi della filiera nell\'idustria {industry_ad}{industry} dove l\'ozono viene usato.\n\n'
    image_path = f'articles-images/public/ozono/sanificazione/industria/{industry_filename}/filiera.jpg'
    image_path = img_list_center(image_path, 'Fasi della filiera', lst)
    image_path = '/' + '/'.join(image_path.split('/')[1:])
    article += f'![alt text]({image_path} "Title")\n\n'

    #####################################################################################################
    # pathogens
    #####################################################################################################
    article += f'## Quali sono i patogeni più comuni nell\'industria {industry_ad}{industry} che l\'ozono può eliminare? \n\n'

    names = [x.split(':')[0] for x in pathogens]
    intro = f'{names[0]}, {names[1]} e {names[2]}'
    article += f'L\'ozono può eliminare la maggior parte dei patogeni che si trovano nei prodotti dell\'industria {industry_ad}{industry}, come {intro}.\n\n'

    image_path = f'articles-images/public/ozono/sanificazione/industria/{industry_filename}/patogeni.jpg'
    image_path = img_pathogens(item, image_path)
    image_path = '/' + '/'.join(image_path.split('/')[1:])
    article += f'![alt text]({image_path} "Title")\n\n'

    # img_filepath = img_pathogens(item)

    # bacteria
    article += f'### Batteri \n\n'
    lst = bold_blt(item['pathogens_bacteria'])
    article += lst_to_blt(lst)
    article += '\n\n'
    
    # virus
    article += f'### Virus \n\n'
    lst = bold_blt(item['pathogens_virus'])
    article += lst_to_blt(lst)
    article += '\n\n'
    
    # fungi
    article += f'### Funghi \n\n'
    lst = bold_blt(item['pathogens_fungi'])
    article += lst_to_blt(lst)
    article += '\n\n'
    
    # protozoa
    article += f'### Protozoi \n\n'
    lst = bold_blt(item['pathogens_protozoa'])
    article += lst_to_blt(lst)
    article += '\n\n'
    
    # parasites
    article += f'### Parassiti \n\n'
    lst = bold_blt(item['pathogens_parasites'])
    article += lst_to_blt(lst)
    article += '\n\n'

    # lst = [item.split(':')[0].replace('*', '') for item in pathogens]
    # article += f'La seguente illustrazione mostra una lista più completa dei patogeni più comuni di questa industria, ordinati dal più frequente al mento frequente.\n\n'
    # image_path = f'articles-images/public/ozono/sanificazione/industria/{industry_filename}/patogeni.jpg'
    # image_path = img_list_double(image_path, 'Lista dei patogeni più comuni', lst)
    # image_path = '/' + '/'.join(image_path.split('/')[1:])
    # article += f'![alt text]({image_path} "Title")\n\n'

    ## benefits
    article += f'## Quali sono i benefici dell\'ozono nell\'industria {industry_ad}{industry}? \n\n'
    
    names = [x.split(':')[0].replace('*', '') for x in benefits]
    intro = f'{names[0].lower()}, {names[1].lower()} e {names[2].lower()}'
    article += f'L\'ozono porta diversi benefici all\'industria {industry_ad}{industry}, come {intro}.\n\n'
    
    article += f'Qui sotto trovi una lista dei principali benefici che l\'ozono porta all\'industria {industry_ad}{industry}.\n\n'
    bld = bold_blt(benefits)
    article += lst_to_blt(bld)
    article += '\n\n'

    benefits_plain = [item.split(':')[0].replace('*', '') for item in benefits]
    article += f'La seguente illustrazione riassume i benefici che l\'ozono porta a questa idustria.\n\n'
    image_path = f'articles-images/public/ozono/sanificazione/industria/{industry_filename}/benefici.jpg'
    image_path = img_list_center(image_path, 'Benefici dell\'ozono', benefits_plain)
    image_path = '/' + '/'.join(image_path.split('/')[1:])
    article += f'![alt text]({image_path} "Title")\n\n'
    
    ## quality effects
    article += f'## Quali sono gli effetti negativi dell\'ozono sulla qualità dei prodotti nell\'industria {industry_ad}{industry}? \n\n'
    
    names = [x.split(':')[0].replace('*', '') for x in side_effects_product_quality]
    intro = f'{names[0].lower()}, {names[1].lower()} e {names[2].lower()}'
    article += f'L\'ozono può avere effetti negativi sulla qualità dei prodotti nell\'industria {industry_ad}{industry} se usato in quantità eccessiva o per un tempo di esposizione prolungato, come {intro}.\n\n'

    article += f'Ecco elencati brevemente i potenziali effetti negativi dell\'ozono sulla qualità dei prodotti {industry_ad}{industry}.\n\n'
    bld = bold_blt(side_effects_product_quality)
    article += lst_to_blt(bld)
    article += '\n\n'

    lst = [item.split(':')[0].replace('*', '') for item in side_effects_product_quality]
    article += f'La seguente illustrazione riassume gli effetti collaterali che l\'ozono può avere sulla qualità dei prodotti di questa idustria.\n\n'
    image_path = f'articles-images/public/ozono/sanificazione/industria/{industry_filename}/qualita-effetti.jpg'
    image_path = img_list_center(image_path, 'Effetti dell\'ozono sulla qualità dei prodotti', lst)
    image_path = '/' + '/'.join(image_path.split('/')[1:])
    article += f'![alt text]({image_path} "Title")\n\n'

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
article_html = article_html.replace('src="/assets/', 'src="public/assets/')


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