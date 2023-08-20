import shutil
# shutil.copy2('/style.css', '/')

import markdown
import pathlib
import os

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 


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


w, h = 800, 600
generate_image_plain('assets/images/home/ristorante-raw.jpg', w, h, 'assets/images/home/ristorante.jpg')
generate_image_plain('assets/images/home/clinica-raw.jpg', w, h, 'assets/images/home/clinica.jpg')
generate_image_plain('assets/images/home/trasporti-raw.jpg', w, h, 'assets/images/home/trasporti.jpg')





def generate_image(image_path, text, w, h, iamge_out_path):

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

    # new_end_size


    # print(w, h)
    # print(img.size)

    # print(img.size)
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
    
    img.save(f'{iamge_out_path}')

    # img.show()

# generate_image('assets/images/featured/ozono-effetti.jpg', 768, 432)
i = 1
w, h = 768, 432
generate_image(
    'assets/images/featured/ozono-chimica.jpg', 
    'Ozono: Tutto quello che volevi sapere su questo gas',
    w, h,
    'assets/images/ozono-chimica.jpg',
)
i += 1
generate_image(
    'assets/images/featured/ozono-stratosferico.jpg', 
    'Ozono Statosferico: Funzione, Formazione e Protezione',
    w, h, 
    'assets/images/ozono-stratosferico.jpg', 
)
i += 1
generate_image(
    'assets/images/featured/ozono-troposferico.jpg', 
    'Ozono Troposferico: Formazione, Effetti e Prevenzione',
    w, h, 
    'assets/images/ozono-troposferico.jpg', 
)
i += 1
generate_image(
    'assets/images/featured/ozono-effetti.jpg', 
    '10 Effetti Dannosi dell\'Ozono: Salute, Ambiente e Materiali',
    w, h, 
    'assets/images/ozono-effetti.jpg', 
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
                    <div class="flex justify-between">
                        <span>Ozonogroup Staff • {publishing_date}</span>
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

