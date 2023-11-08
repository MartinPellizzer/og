import json
import os
import random
import re
import markdown
import math
import shutil
import csv
import pathlib

from PIL import Image, ImageFont, ImageDraw, ImageColor

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


def img_resize_2(image_path_in, image_path_out):
    w, h = 768, 576

    img = Image.open(image_path_in)

    start_size = img.size
    end_size = (w, h)

    if start_size[0] / end_size [0] < start_size[1] / end_size [1]:
        ratio = start_size[0] / end_size[0]
        new_end_size = (end_size[0], int(start_size[1] / ratio))
    else:
        ratio = start_size[1] / end_size[1]
        new_end_size = (int(start_size[0] / ratio), end_size[1])

    img = img.resize(new_end_size, Image.Resampling.LANCZOS)

    w_crop = new_end_size[0] - end_size[0]
    h_crop = new_end_size[1] - end_size[1]
    
    area = (
        w_crop // 2, 
        h_crop // 2,
        new_end_size[0] - w_crop // 2,
        new_end_size[1] - h_crop // 2
    )
    img = img.crop(area)

    output_path = image_path_out
    img.save(output_path, quality=100)

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


def img_cheasheet(item, title, lst, img_name):
    industry = item['industry']
    industry_ad = item['industry_ad']

    img_w, img_h = 768, 2000
    bg_dark_1 = "#1d4ed8"
    bg_light_1 = "#eff6ff"
    bg_light_2 = "#dbeafe"
    # bg_light_3 = "#a7f3d0"
    fg_light = '#ffffff'
    fg_dark = '#0f172a'

    img = Image.new(mode="RGB", size=(img_w, img_h), color=bg_light_1)
    draw = ImageDraw.Draw(img)

    rect_h = 0
    line_x = 50
    line_y = 20

    font_size = 36
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    lines = [title, f'{industry_ad}{industry}']
    for i, line in enumerate(lines):
        rect_h += font.getbbox('y')[3]
    rect_h += line_y * 2
        
    draw.rectangle(((0, 0), (img_w, rect_h)), fill=bg_dark_1)
    for i, line in enumerate(lines):
        line_w = font.getbbox(line)[2]
        line_h = font.getbbox('y')[3]
        draw.text((img_w//2 - line_w//2, line_y + line_h * i), line, fg_light, font=font)

    font_size = 16
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    
    title_rect_h = rect_h
    line_y = title_rect_h + 50

    rect_h = 0

    full_len = len(lst)
    half_len_1 = math.ceil(full_len/2)
    half_len_2 = full_len - half_len_1
    sublist_1 = lst[:half_len_1]
    sublist_2 = lst[half_len_1:]

    for l in sublist_1:
        bg = 0
        for i, x in enumerate(l):
            line = x
            line_x = 50
            line_y += rect_h
            line_w = font.getbbox(line)[2]
            line_h = font.getbbox('y')[3]
            rect_x = line_x - 20
            rect_y = line_y - 10
            rect_w = img_w//2 - 50
            rect_h = line_h + 20
            if i == 0:
                draw.rectangle(((rect_x, rect_y), (rect_x + rect_w, rect_y + rect_h)), fill=bg_dark_1)
                draw.text((line_x, line_y), line, fg_light, font=font)
            elif bg == 0:
                bg = 1
                draw.rectangle(((rect_x, rect_y), (rect_x + rect_w, rect_y + rect_h)), fill=bg_light_2)
                draw.text((line_x, line_y), line, fg_dark, font=font)
            else:
                bg = 0
                draw.rectangle(((rect_x, rect_y), (rect_x + rect_w, rect_y + rect_h)), fill=bg_light_1)
                draw.text((line_x, line_y), line, fg_dark, font=font)
        line_y += rect_h
        rect_y = line_y - 10
        draw.rectangle(((rect_x, rect_y), (rect_x + rect_w, rect_y + 5)), fill=bg_dark_1) 

    max_height = line_y
    
    line_y = title_rect_h + 50

    rect_h = 0
    for l in sublist_2:
        bg = 0
        for i, x in enumerate(l):
            line = x
            line_x = img_w//2 + 36
            line_y += rect_h
            line_w = font.getbbox(line)[2]
            line_h = font.getbbox('y')[3]
            rect_x = line_x - 20
            rect_y = line_y - 10
            rect_w = img_w//2 - 50
            rect_h = line_h + 20
            if i == 0:
                draw.rectangle(((rect_x, rect_y), (rect_x + rect_w, rect_y + rect_h)), fill=bg_dark_1)
                draw.text((line_x, line_y), line, fg_light, font=font)
            elif bg == 0:
                bg = 1
                draw.rectangle(((rect_x, rect_y), (rect_x + rect_w, rect_y + rect_h)), fill=bg_light_2)
                draw.text((line_x, line_y), line, fg_dark, font=font)
            else:
                bg = 0
                draw.rectangle(((rect_x, rect_y), (rect_x + rect_w, rect_y + rect_h)), fill=bg_light_1)
                draw.text((line_x, line_y), line, fg_dark, font=font)
        line_y += rect_h
        rect_y = line_y - 10
        draw.rectangle(((rect_x, rect_y), (rect_x + rect_w, rect_y + 6)), fill=bg_dark_1) 

    if max_height < line_y : max_height = line_y

    area = (0, 0, img_w, max_height + 30)
    img = img.crop(area)

    
    output_filename = industry.lower().replace(' ', '-')
    output_path = f'public/assets/images/ozono-sanificazione-{output_filename}-{img_name}.jpg'
    img.save(f'{output_path}', format='JPEG', subsampling=0, quality=100)

    return output_path


def generate_featured_image(attribute):
    image_path_in = f'articles-images/public/ozono/sanificazione/{attribute}/featured.jpg'
    image_filename_out = f'{attribute.replace("/", "-")}-featured.jpg'
    image_filepath_out = f'/assets/images/{image_filename_out}'
    image_path_out = f'public/assets/images/{image_filename_out}'
    img_resize_2(image_path_in, image_path_out)

    return image_filepath_out


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
        
    img.save(f'{image_path_out}')



###################################################################################################################
# articles html
###################################################################################################################
def generate_article_html(date, attribute, article, title):
    with open(f'articles/public/ozono/sanificazione/{attribute}.md', 'w', encoding='utf-8') as f:
        f.write(article)

    with open(f'articles/public/ozono/sanificazione/{attribute}.md', encoding='utf-8') as f:
        article_md = f.read()

    word_count = len(article_md.split(' '))
    reading_time = str(word_count // 200) + ' minuti'
    # word_count_html = str(word_count) + ' words'

    # article_html = markdown.markdown(article_md)
    article_html = markdown.markdown(article_md, extensions=['markdown.extensions.tables'])


    # GENERATE TABLE OF CONTENTS ----------------------------------------
    article_html = generate_toc(article_html)

    with open('components/header.html', encoding='utf-8') as f:
            header_html = f.read()

    author = 'Ozonogroup'

    html = f'''
        <!DOCTYPE html>
        <html lang="en">

        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="/style-blog.css">
            <title>{title}</title>
        </head>

        <body>
            <section class="header-section">
                <div class="container-xl">
                    {header_html}
                </div>
            </section>

            <section class="meta-section mt-48">
                <div class="container-md px-16">
                    <div class="flex justify-between mb-8">
                        <span>by {author} • {date}</span>
                        <span>Tempo Lettura: {reading_time}</span>
                    </div>
                </div>
            </section>

            <section class="mb-96">
                <div class="container-md px-16">
                    {article_html}
                </div>
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

    with open(f'public/ozono/sanificazione/{attribute}.html', 'w', encoding='utf-8') as f:
        f.write(html)


def generate_home_html(home_articles):
    articles_html = ''
    for article in home_articles:
        articles_html += f'''
            <a class="decoration-none" href="{article['href']}">
                <img src="{article['src']}" alt="">
                <h3>{article['title']}</h3>
            </a>
        '''

    with open("home.html", encoding='utf-8') as f:
        html = f.read()

    html = html.replace('<!-- insert_articles_here -->', articles_html)

    with open("public/index.html", 'w', encoding='utf-8') as f:
        f.write(html)


def get_csv_table(filepath):
    lines = []
    with open(filepath, encoding='utf-8') as f:
        reader = csv.reader(f, delimiter="|")
        for i, line in enumerate(reader):
            lines.append([line[0].strip(), line[1].strip()])
    return lines


def generate_table(lines):
    text = ''
    for i, line in enumerate(lines):
        if i == 0: 
            text += f'| {line[0].title()} | Problemi | \n'
            text += f'| --- | --- |\n'
        else:
            text += f'| {line[0].capitalize()} | {line[1].capitalize()} |\n'
    text += f'\n'
    return text


def generate_manual_article_html():
    folder = pathlib.Path("articles")

    w, h = 768, 432
    generate_image_plain(
        'assets/images/featured/ozono-chimica.jpg', 
        w, h,
        'public/assets/images/ozono-chimica.jpg',
    )
    generate_image_plain(
        'assets/images/featured/ozono-stratosferico.jpg', 
        w, h, 
        'public/assets/images/ozono-stratosferico.jpg', 
    )
    generate_image_plain(
        'assets/images/featured/ozono-troposferico.jpg', 
        w, h, 
        'public/assets/images/ozono-troposferico.jpg', 
    )
    generate_image_plain(
        'assets/images/featured/ozono-effetti.jpg', 
        w, h, 
        'public/assets/images/ozono-effetti.jpg', 
    )
    generate_image_plain(
        'assets/images/featured/ozono-benefici.jpg', 
        w, h, 
        'public/assets/images/ozono-benefici.jpg', 
    )
    generate_image_plain(
        'assets/images/featured/ozono-sanificazione.jpg', 
        w, h, 
        'public/assets/images/ozono-sanificazione.jpg', 
    )

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
                
        # <section class="breadcrumbs-section">
        #     <div class="container-xl h-full">
        #         <a href="/index.html">Home</a>{''.join(breadcrumbs)}
        #     </div>
        # </section>
                
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
        print(filepath_out)

        if not os.path.exists(filepath_out_dir):
            os.makedirs(filepath_out_dir)

        with open(filepath_out, 'w', encoding='utf-8') as f:
            f.write(html)


def copy_images():
    articles_images_path = 'assets/images/articles/'
    for f in os.listdir(articles_images_path):
        shutil.copy2(f'{articles_images_path}{f}', f'public/assets/images/{f}')
        
    articles_images_path = 'assets/images/home/'
    for f in os.listdir(articles_images_path):
        shutil.copy2(f'{articles_images_path}{f}', f'public/assets/images/{f}')

###################################################################################################################
# articles
###################################################################################################################
# try: shutil.rmtree('articles/public/ozono/sanificazione/')
# except: pass
# try: os.mkdir('articles/public/ozono/sanificazione/')
# except: pass

try: shutil.rmtree('public/ozono/sanificazione/')
except: pass
try: os.mkdir('public/ozono/sanificazione/')
except: pass

home_articles = []

for item in data:
    article = ''

    if item['status'] == 'draft': continue

    date = item['date']
    attribute = item['attribute']
    entity = item['entity']

    # # TODO: remove
    # if 'ittica' not in attribute: continue
    
    folders = attribute.split('/')
    path = ''
    for folder in folders:
        path += folder + '/'
        try: os.mkdir(f'articles/public/ozono/sanificazione/{path}')
        except: pass
        try: os.mkdir(f'public/ozono/sanificazione/{path}')
        except: pass
    
    industry = item['industry']
    industry_ad = item['industry_ad']

    if 'applicazioni' in attribute: 
        applications = item['applications']

        # title
        title = f'{len(applications)} Applicazioni dell\'Ozono nell\'Industria {industry_ad}{industry.title()}'
        article += f'# {title} \n\n'

        # image
        try:
            img_filepath = generate_featured_image(attribute)
            article += f'![{title}]({img_filepath} "{title}")\n\n'
        except:
            print(f'WARNING: missing image > {attribute}')
        
        # intro 
        applications_intro = item['applications_intro']
        article +=  '\n\n'.join(applications_intro) + '\n\n'
        applications_titles = [application["title"] for application in applications]
        article += f'In questo articolo vengono descritte nel dettaglio le applicazioni dell\'ozono nell\'industria {industry_ad}{industry} elencate nella seguente lista.\n\n'
        article += lst_to_blt(applications_titles) + '\n\n'

        # list
        for i, application in enumerate(applications):
            article += f'## {i+1}. {application["title"].capitalize()}\n\n'
            article += '\n\n'.join(application['description']) + '\n\n'
            application_title = application['title'].replace(' ', '-')
            
            try: application_table = application['table'].replace(' ', '-')
            except: continue
            lines = get_csv_table(f'database/tables/{industry}/{application_table}/{application_table}.csv')
            article += generate_table(lines)

            # for problem in application['problems']:
            #     article += f'### {problem["type"].title()}\n\n'
            #     article += '\n\n'.join(problem['description']) + '\n\n'

            #     application_title = application['title'].replace(' ', '-')
            #     application_problem_type = problem["type"].replace(' ', '-')

            #     # get csv table
            #     lines = get_csv_table(f'database/tables/{industry}/{application_title}/{application_problem_type}.csv')

            #     # generate table
            #     article += generate_table(lines)
                
            try:
                lst = application['list']
                if application['table'] == 'aria-ambienti':
                    article += f'L\'ozono sanifica diversi tipi di ambienti nell\'industria {industry_ad}{industry}, come quelli elencanti nella seguente lista.\n\n'
                elif application['table'] == 'attrezzature':
                    article += f'L\'ozono sanifica diversi tipi di attrezzature nell\'industria {industry_ad}{industry}, come quelle elencante nella seguente lista.\n\n'
                elif application['table'] == 'prodotti-alimentari':
                    article += f'L\'ozono sanifica diversi tipi di prodotti alimentari nell\'industria {industry_ad}{industry}, come quelli elencanti nella seguente lista.\n\n'
                article += lst_to_blt(lst) + '\n\n'
            except: pass

    else:
        applications = item['applications']
        chain = item['chain']
        pathogens = item['pathogens']
        benefits = item['benefits']
        side_effects_product_quality = item['side_effects_product_quality']

        industry_filename = industry.replace(' ', '-')

        # title
        title = f'Sanificazione ad Ozono nell\'industria {industry_ad}{industry.title()}'
        article += f'# Sanificazione ad ozono nell\'industria {industry_ad}{industry}: applicazioni e benefici \n\n'

        img_filepath = generate_featured_image(attribute)
        article += f'![tesst]({img_filepath} "Title")\n\n'

        # INTRODUCTION ----------------------------------------------------------------------------------------------
        applications_names = [x.split(':')[0] for x in applications]
        applications_intro = f'{applications_names[0].lower()}, {applications_names[1].lower()} e {applications_names[2].lower()}'
        
        chain_names = [x.split(':')[0] for x in chain]
        chain_intro = f'dalla fase di {chain_names[0].lower()} alla fase di {chain_names[-1].lower()}'
        pathogens_names = [x.split(':')[0] for x in item['pathogens_bacteria']]
        pathogens_intro = f'{pathogens_names[0]}, {pathogens_names[1]} e {pathogens_names[2]}'
        
        benefits_names = [x.split(':')[0] for x in benefits]
        benefits_intro = f'{benefits_names[0].lower()}, {benefits_names[1].lower()} e {benefits_names[2].lower()}'
        quality_effects_names = [x.split(':')[0] for x in side_effects_product_quality]
        quality_effects_intro = f'{quality_effects_names[0].lower()}, {quality_effects_names[1].lower()} e {quality_effects_names[2].lower()}'
        
        article += f'L\'ozono (O3) è un gas che viene utilizzato nell\'industria {industry_ad}{industry} per applicazioni come {applications_intro}.\n\n'
        article += f'Viene impiegato in diverse fasi della filiera di questa industria, {chain_intro}, ed è in grado di eliminare diversi patogeni come {pathogens_intro}.\n\n'
        # article += f'Inoltre, è in grado di portare diversi benefici come {benefits_intro}. Però, può anche influire negativamente sulla qualità dei prodotti se usato scorrettamente, come {quality_effects_intro}.\n\n'
        article += f'Inoltre, è in grado di portare diversi benefici come {benefits_intro}. Però, può anche influire negativamente sulla qualità dei prodotti se usato scorrettamente.\n\n'
        article += f'In questo articolo vengono descritte nel dettaglio le applicazioni dell\'ozno nell\'industria {industry_ad}{industry} e quali sono i benefici che questo gas porta in questa industria.\n\n'

        article = re.sub(' +', ' ', article)
        article += '\n\n'

        # APPLICATIONS ----------------------------------------------------------------------------------------------
        article += f'## Quali sono le applicazioni dell\'ozono nell\'industria {industry_ad}{industry}? \n\n'

        # i = 0
        # for application in item['applications_extended']:
        #     i += 1
        #     application_title = application['title']
        #     application_description = '\n\n'.join(application['description'])

        #     article += f'### {i}. {application_title} \n\n'
        #     article += f'{application_description} \n\n'
        article += lst_to_blt(bold_blt(applications)) + '\n\n'




        # applications_names = [x.split(':')[0] for x in applications]
        # applications_intro = f'{applications_names[0].lower()}, {applications_names[1].lower()} e {applications_names[2].lower()}'
        # article += f'Le applicazioni dell\'ozono nell\'industria {industry_ad}{industry} sono svariate, come {applications_intro}.\n\n'
        # article += f'Qui sotto trovi una lista di queste applicazioni (quelle più comuni).\n\n'
        # applications = bold_blt(applications)
        # applications_name = [x.split(':')[0] for x in applications]
        # article += lst_to_blt(applications)
        # article += '\n\n'
        
        # lst = [item.split(':')[0].replace('*', '') for item in applications]
        # article += f'La seguente illustrazione riassume le applicazioni dell\'ozono nell\'idustria {industry_ad}{industry}.\n\n'
        # image_path = f'articles-images/public/ozono/sanificazione/industria/{industry_filename}/applicazioni.jpg'
        # image_path = img_list_center(image_path, 'Applicazioni dell\'ozono', lst)
        # image_path = '/' + '/'.join(image_path.split('/')[1:])
        # article += f'![alt text]({image_path} "Title")\n\n'
        
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
        image_path = f'articles-images/public/ozono/sanificazione/{industry_filename}/filiera.jpg'
        image_path = img_list_center(image_path, 'Fasi della filiera', lst)
        image_path = '/' + '/'.join(image_path.split('/')[1:])
        article += f'![alt text]({image_path} "Title")\n\n'

        #####################################################################################################
        # PATHOGENS
        #####################################################################################################
        article += f'## Quali sono i patogeni più comuni nell\'industria {industry_ad}{industry} che l\'ozono può eliminare? \n\n'

        # INTRO
        bacteria_lst = [x.split(':')[0].split('(')[0].strip() for x in item['pathogens_bacteria'][:3]]
        virus_lst = [x.split(':')[0].split('(')[0].strip() for x in item['pathogens_virus'][:3]]
        fungi_lst = [x.split(':')[0].split('(')[0].strip() for x in item['pathogens_fungi'][:3]]
        protozoa_lst = [x.split(':')[0].split('(')[0].strip() for x in item['pathogens_protozoa'][:3]]
        parasites_lst = [x.split(':')[0].split('(')[0].strip() for x in item['pathogens_parasites'][:3]]
        bacteria_txt = lst_to_txt(bacteria_lst)
        virus_txt = lst_to_txt(virus_lst)
        fungi_txt = lst_to_txt(fungi_lst)
        protozoa_txt = lst_to_txt(protozoa_lst)
        parasites_txt = lst_to_txt(parasites_lst)
        article += f'L\'ozono elimina i batteri patogeni più comuni nell\'industria {industry_ad}{industry}, come {bacteria_txt}.\n\n'
        article += f'Elimina ance i virus (come {virus_txt}), i funghi (come {fungi_txt}) e i protozoi ({protozoa_txt}).\n\n'
        article += f'Infine, repelle diversi tipi di insetti e parassiti (come {parasites_txt}).\n\n'

        # CHEAT SHEET
        lst = []
        pathogens_lst = [x.split(':')[0].split('(')[0] for x in item['pathogens_bacteria'][:7]]
        pathogens_lst.insert(0, 'Batteri')
        lst.append(pathogens_lst)
        pathogens_lst = [x.split(':')[0].split('(')[0] for x in item['pathogens_virus'][:7]]
        pathogens_lst.insert(0, 'Virus')
        lst.append(pathogens_lst)
        pathogens_lst = [x.split(':')[0].split('(')[0] for x in item['pathogens_fungi'][:7]]
        pathogens_lst.insert(0, 'Funghi')
        lst.append(pathogens_lst)
        pathogens_lst = [x.split(':')[0].split('(')[0] for x in item['pathogens_protozoa'][:7]]
        pathogens_lst.insert(0, 'Protozoi')
        lst.append(pathogens_lst)
        pathogens_lst = [x.split(':')[0].split('(')[0] for x in item['pathogens_parasites'][:7]]
        pathogens_lst.insert(0, 'Parassiti')
        lst.append(pathogens_lst)

        img_path = f'articles/public/ozono/sanificazione/{industry_filename}/patogeni.jpg'
        img_path = img_cheasheet(item, 'Patogeni comuni nell\'industria', lst, 'patogeni')
        img_path = '/' + '/'.join(img_path.split('/')[1:])
        article += f'La seguente immagine mostra un elenco dei patogeni più comuni in questa industria.\n\n'
        article += f'![alt]({img_path} "title")\n\n'

        article += f'A seguire, viene data una breve descrizione di ogni singolo patogeno. I patogeni sono divisi per categorie, quali batteri, virus, fungi, protozoi e parassiti.\n\n'


        # img_filepath = img_pathogens(item)

        # bacteria
        article += f'### Batteri \n\n'
        article += f'Ecco una descrizione dei batteri più comuni in questa industria.\n\n'
        lst = bold_blt(item['pathogens_bacteria'])
        article += lst_to_blt(lst)
        article += '\n\n'
        
        # virus
        article += f'### Virus \n\n'
        article += f'Ecco una descrizione dei virus più comuni in questa industria.\n\n'
        lst = bold_blt(item['pathogens_virus'])
        article += lst_to_blt(lst)
        article += '\n\n'
        
        # fungi
        article += f'### Funghi \n\n'
        article += f'Ecco una descrizione dei funghi più comuni in questa industria.\n\n'
        lst = bold_blt(item['pathogens_fungi'])
        article += lst_to_blt(lst)
        article += '\n\n'
        
        # protozoa
        article += f'### Protozoi \n\n'
        article += f'Ecco una descrizione dei protozoi più comuni in questa industria.\n\n'
        lst = bold_blt(item['pathogens_protozoa'])
        article += lst_to_blt(lst)
        article += '\n\n'
        
        # parasites
        article += f'### Parassiti \n\n'
        article += f'Ecco una descrizione dei parassiti più comuni in questa industria.\n\n'
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
        article += f'Si consiglia quindi di contattare un professionista prima di applicare questa tecnologia di sanificazione.\n\n'

        article += f'Ecco elencati brevemente i potenziali effetti negativi dell\'ozono sulla qualità dei prodotti {industry_ad}{industry}.\n\n'
        bld = bold_blt(side_effects_product_quality)
        article += lst_to_blt(bld)
        article += '\n\n'

        lst = [item.split(':')[0].replace('*', '') for item in side_effects_product_quality]
        article += f'La seguente illustrazione riassume gli effetti collaterali che l\'ozono può avere sulla qualità dei prodotti di questa idustria.\n\n'
        image_path = f'articles-images/public/ozono/sanificazione/{industry_filename}/qualita-effetti.jpg'
        image_path = img_list_center(image_path, 'Effetti dell\'ozono sulla qualità dei prodotti', lst)
        image_path = '/' + '/'.join(image_path.split('/')[1:])
        article += f'![alt text]({image_path} "Title")\n\n'

        # print(item)

        industry_formatted = industry.replace(' ', '-')
        with open(f'articles/public/ozono/sanificazione/{industry_formatted}.md', 'w', encoding='utf-8') as f:
            f.write(article)


    # generate html
    generate_article_html(date, attribute, article, title)

    home_article = {
        'href': f'/ozono/sanificazione/{attribute}.html',
        'src': f'{img_filepath}',
        'title': f'{title}'
    }

    home_articles.append(home_article)
        


generate_home_html(home_articles) 

generate_manual_article_html()
copy_images()

# # VIEWER
# with open('articles/public/ozono/sanificazione/quarta-gamma/applicazioni.md') as f:
#     article_md = f.read()

# word_count = len(article_md.split(' '))
# reading_time_html = str(word_count // 200) + ' minutes'
# word_count_html = str(word_count) + ' words'


# article_html = markdown.markdown(article_md)

# article_html = article_html.replace('<img', '<img class="featured-img"')
# article_html = article_html.replace('src="/assets/', 'src="public/assets/')


# # GENERATE TABLE OF CONTENTS ----------------------------------------
# article_html = generate_toc(article_html)


# html = f'''
#     <!DOCTYPE html>
#     <html lang="en">

#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <link rel="stylesheet" href="style-blog.css">
#         <title>Document</title>
#     </head>

#     <body>
#         <section class="my-96">
#             <div class="container-md">
#                 {word_count_html} - {reading_time_html}
#                 {article_html}
#             </div>
#         </section>
#     </body>

#     </html>
# '''

# with open(f'article-viewer.html', 'w') as f:
#     f.write(html)