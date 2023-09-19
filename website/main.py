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


# DB TO ARTICLE ----------------------------------------------------






# print(rows[0])


# random.shuffle(rows)

# for row in rows:
#     print(row)

"""
L'ozono viene usato per trattare il latte crudo, 
inattivando in microrganismi patogeni 
e minimizzando la perdita di proprietà nutritive 
(al contrario dei trattamenti termici). 

Studi dimostrano che l'ozono elimina il Cronobacter sakazaki 
dal latte in polvere, 
se utilizzato in concentrazioni di 2.8 mg L-1 per 120 minuti, 
riducendo la carica batterica di 2.71 log. 

Riduce anche gli psicrotrofi 
(batteri che crescono a temperature pari o inferiori a 7°C) 
dal latte scremato, 
se utilizzato in concentrazioni di 5-35 mg L-1 per 5-25 minuti. 
"""

print()

fields = {}
for i, col in enumerate(rows[0]):
    fields[col] = i

for key, value in fields.items():
    print(key + " - " +  str(value))
    pass

rows = rows[1:]

print()

# quit()


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




encoding = 'utf-8'

with open('test.md', 'w', encoding=encoding) as f:
    f.write('')


    

text = ''
for i, row in enumerate(rows):
    if row[fields['effetti_qualita']].lower() != ''.lower().strip():
        text += generate_benefits(i, row)
text = re.sub(' +', ' ', text)
with open('test.md', 'a', encoding=encoding) as f:
    f.write('### Latte\n\n')
    f.write(f'{text}\n\n')


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

generate_image_sanitation('assets/images/articles/ozono-sanificazione-caseifici.jpg')





# quit()




# # LATTE
# text = ''
# for i, row in enumerate(rows):
#     if row[fields['prodotto']].lower() == 'latte'.lower():
#         text += generate_line(i, row)
# text = re.sub(' +', ' ', text)
# with open('test.md', 'a', encoding=encoding) as f:
#     f.write('### Latte\n\n')
#     f.write(f'{text}\n\n')



# # ACQUE REFLUE
# text = ''
# for i, row in enumerate(rows):
#     if row[fields['prodotto']].lower() == 'acque reflue'.lower():
#         text += generate_line(i, row)
# text = re.sub(' +', ' ', text)
# with open('test.md', 'a', encoding=encoding) as f:
#     f.write('### Acque Reflue\n\n')
#     f.write(f'{text}\n\n')



# # FORMAGGIO
# text = ''
# for i, row in enumerate(rows):
#     if row[fields['prodotto']].lower() == 'formaggio'.lower():
#         text += generate_line(i, row)
# text = re.sub(' +', ' ', text)
# with open('test.md', 'a', encoding=encoding) as f:
#     f.write('### Formaggio\n\n')
#     f.write(f'{text}\n\n')


with open('test.md', encoding=encoding) as f:
    generated_content = f.read()

# generated_content = text

content_html = markdown.markdown(generated_content, extensions=['markdown.extensions.tables', 'meta'])

md = markdown.Markdown(extensions=['meta'])
md.convert(generated_content)


lines = '\n'.join(md.lines)

content_html = markdown.markdown(lines, extensions=['markdown.extensions.tables'])

    
with open('test_caseifici.html', 'w', encoding=encoding) as f:
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

# quit()




def generate_image_plain(image_path, w, h, image_path_out):
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

    name = image_path.split('/')[-1]
    path = image_path.split('/')[:-1]

    print(image_path_out)

        
    img.save(f'{image_path_out}')
    if image_path_out == 'public/assets/images/ozono-effetti.jpg':
        img.show()


w, h = 800, 600
generate_image_plain('assets/images/home/ristorante-raw.jpg', w, h, 'assets/images/home/ristorante.jpg')
generate_image_plain('assets/images/home/clinica-raw.jpg', w, h, 'assets/images/home/clinica.jpg')
generate_image_plain('assets/images/home/trasporti-raw.jpg', w, h, 'assets/images/home/trasporti.jpg')





def generate_image(image_path, text, w, h, image_out_path):

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

    font = ImageFont.truetype("assets/fonts/arial.ttf", 32)

    words = text.split()
    lines = []
    line = ''
    for word in words:
        word_width = font.getsize(word)[0]
        line_width = font.getsize(line)[0]
        if word_width + line_width < int(w * 0.66):
            line += word + ' '
        else:
            lines.append(line)
            line = word + ' '
    lines.append(line)


    text_h = 0
    for line in lines:
        text_h += font.getsize(line)[1]
    start_text_y = h - text_h - 50




    
    # rect_size = [600, 80]

    draw = ImageDraw.Draw(img)
    

    text_size = font.getsize(lines[0])
    
    
    logo = Image.open("logo-og-light.png")


    text_width_max = 0
    for line in lines:
        if font.getsize(line)[0] > text_width_max:
            text_width_max = font.getsize(line)[0]

    box = (
        (0, start_text_y - 10),
        (text_width_max + 20 + 50 + 100, start_text_y + text_h + 15)
    )
    draw.rectangle(box, fill=(37, 99, 235))
    rectangle_h = box[1][1] - box[0][1]

    line_height_max = 0
    for line in lines:
        if font.getsize(line)[1] > line_height_max:
            line_height_max = font.getsize(line)[1]

    for i, line in enumerate(lines):
        line_offset = i * line_height_max
        draw.text((20, line_offset + start_text_y), line, (255,255,255), font=font)
        
    img.paste(logo, (text_width_max + 50, start_text_y - 10 + (rectangle_h // 2) - (logo.size[1] // 2)), logo)
    

    # print(image_out_path)

        
    img.save(f'{image_out_path}')
    # if image_out_path == 'assets/images/ozono-benefici.jpg':
    #     img.show()




# generate_image('assets/images/featured/ozono-effetti.jpg', 768, 432)
i = 1
w, h = 768, 432
generate_image_plain(
    'assets/images/featured/ozono-chimica.jpg', 
    w, h,
    'public/assets/images/ozono-chimica.jpg',
)
i += 1
generate_image_plain(
    'assets/images/featured/ozono-stratosferico.jpg', 
    w, h, 
    'public/assets/images/ozono-stratosferico.jpg', 
)
i += 1
generate_image_plain(
    'assets/images/featured/ozono-troposferico.jpg', 
    w, h, 
    'public/assets/images/ozono-troposferico.jpg', 
)
i += 1
# generate_image_plain(
#     'assets/images/featured/ozono-effetti.jpg', 
#     w, h, 
#     'public/assets/images/ozono-effetti.jpg', 
# )
i += 1
generate_image_plain(
    'assets/images/featured/ozono-benefici.jpg', 
    w, h, 
    'public/assets/images/ozono-benefici.jpg', 
)
i += 1




folder = pathlib.Path("articles")

def generate_breadcrumbs(filepath_chunks):
    breadcrumbs = [f.replace('.md', '').title() for f in filepath_chunks[2:-1]]
    
    breadcrumbs_hrefs = []
    total_path = ''
    for b in breadcrumbs:
        total_path += b + '/'
        breadcrumbs_hrefs.append('/' + total_path[:-1].lower() + '.html')
    
    breadcrumbs_text = total_path.split('/')

    breadcrumbs_html = []
    for i in range(len(breadcrumbs_hrefs)):
        html = f'<a href="{breadcrumbs_hrefs[i]}">{breadcrumbs_text[i]}</a>'
        breadcrumbs_html.append(html)

    breadcrumbs_html_formatted = [f' > {f}' for f in breadcrumbs_html]

    return breadcrumbs_html_formatted


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


for filepath in folder.rglob("*.md"):

    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    content_html = markdown.markdown(content, extensions=['markdown.extensions.tables', 'meta'])

    md = markdown.Markdown(extensions=['meta'])
    md.convert(content)


    lines = '\n'.join(md.lines)

    content_html = markdown.markdown(lines, extensions=['markdown.extensions.tables'])


    filepath_chunks = str(filepath).split('\\')


    # BREADCRUMBS  ---------------------------------------------
    breadcrumbs = generate_breadcrumbs(filepath_chunks)

    # READING TIME  ---------------------------------------------
    reading_time = len(content.split(' ')) // 200

    # PUBLICATION DATE  ----------------------------------------
    publishing_date = ''
    try: publishing_date = md.Meta['publishing_date'][0]
    except: pass

    # AUTHOR ----------------------------------------
    author = 'Ozonogroup Staff'
    try: author = md.Meta['author'][0]
    except: pass

    last_update_date = ''
    try: last_update_date = md.Meta['last_update_date'][0]
    except: pass

    # GENERATE TABLE OF CONTENTS ----------------------------------------
    toc_html = generate_toc(content_html)
    
    
    with open('components/header.html', encoding='utf-8') as f:
        header_html = f.read()
            
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
                    {header_html}
                </div>
            </section>

            <section class="breadcrumbs-section">
                <div class="container-xl h-full">
                    <a href="/index.html">Home</a>{''.join(breadcrumbs)}
                </div>
            </section>

            <section class="meta-section mt-48">
                <div class="container-md h-full">
                    <div class="flex justify-between mb-8">
                        <span>by {author} • {publishing_date}</span>
                        <span>Tempo Lettura: {reading_time} min</span>
                    </div>
                </div>
            </section>

            <section class="container-md">
                {toc_html}
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


    filepath_out_dir = '/'.join(filepath_chunks[1:-1])
    filepath_out = '/'.join(filepath_chunks[1:]).replace('.md', '.html')

    if not os.path.exists(filepath_out_dir):
        os.makedirs(filepath_out_dir)

    with open(filepath_out, 'w', encoding='utf-8') as f:
        f.write(html)

    shutil.copy2('index.html', 'public/index.html')

    shutil.copy2('style.css', 'public/style.css')
    shutil.copy2('style-blog.css', 'public/style-blog.css')
    shutil.copy2('util.css', 'public/util.css')
    shutil.copy2('img.css', 'public/img.css')
    shutil.copy2('logo.ico', 'public/logo.ico')
    shutil.copy2('CNAME', 'public/CNAME')

    # COPY IMAGES -----------------------------------------------------

    articles_images_path = 'assets/images/articles/'
    for f in os.listdir(articles_images_path):
        shutil.copy2(f'{articles_images_path}{f}', f'public/assets/images/{f}')
        
    articles_images_path = 'assets/images/home/'
    for f in os.listdir(articles_images_path):
        shutil.copy2(f'{articles_images_path}{f}', f'public/assets/images/{f}')

