import os
import csv
import json
import datetime





###################################
# DATETIME
###################################

def date_today():
    return str(datetime.date.today())





###################################
# CSV
###################################

def csv_get_rows(filepath, delimiter='\\'):
    rows = []
    with open(filepath, encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f, delimiter=delimiter)
        for i, line in enumerate(reader):
            if line != []:
                rows.append(line)
    return rows


def csv_add_rows(filepath, rows, delimiter='\\'):
    with open(filepath, 'a', encoding='utf-8', errors='ignore', newline='') as f:
        writer = csv.writer(f, delimiter=delimiter)
        writer.writerows(rows)


def csv_set_rows(filepath, rows, delimiter='\\'):
    with open(filepath, 'w', encoding='utf-8', errors='ignore', newline='') as f:
        writer = csv.writer(f, delimiter=delimiter)
        writer.writerows(rows)
        

def csv_get_rows_by_entity(filepath, entity, delimiter='\\', col_num=0):
    rows = []
    with open(filepath, encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f, delimiter=delimiter)
        for i, line in enumerate(reader):
            if line != []:
                if line[col_num].lower().strip().replace(' ', '-').replace("'", '-') == entity.lower().strip().replace(' ', '-').replace("'", '-'):
                    rows.append(line)
    return rows


def folder_create(path):
    if not os.path.exists(path): os.makedirs(path)


def filepath_create(filepath, debug=False):
    chunks = filepath.split('/')
    chunk_curr = ''
    for chunk in chunks[:-1]:
        chunk_curr += f'{chunk}/'
        try: os.makedirs(chunk_curr)
        except: 
            if debug: print(f'WARNING: folder already exists? >> {chunk_curr}')
    file_append(filepath, '')


# def get_csv_table(filepath):
#     lines = []
#     with open(filepath, encoding='utf-8') as f:
#         reader = csv.reader(f, delimiter="|")
#         for i, line in enumerate(reader):
#             lines.append([line[0].strip(), line[1].strip()])
#     return lines


def csv_get_header_dict(rows):
    cols = {}
    i = 0
    for col_name in rows[0]:
        cols[col_name] = i
        i += 1
    return cols



def csv_get_cols(rows):
    cols = {}
    i = 0
    for col_name in rows[0]:
        cols[col_name] = i
        i += 1
    return cols


def csv_get_rows_by_col_val(filepath, col_index, cell_val, delimiter='\\'):
    rows = []
    with open(filepath, encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f, delimiter=delimiter)
        for i, line in enumerate(reader):
            if line != []:
                line_formatted = line[col_index].lower().strip().replace(' ', '-').replace("'", '-')
                cell_val_formatted = cell_val.lower().strip().replace(' ', '-').replace("'", '-')
                if line_formatted == cell_val_formatted:
                    rows.append(line)
    return rows



###################################
# MD
###################################

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





###################################
# FILE
###################################

def file_append(filepath, text):
    with open(filepath, 'a', encoding='utf-8') as f: 
        f.write(text)


def file_read(filepath):
    file_append(filepath, '')
    with open(filepath, 'r', encoding='utf-8') as f: 
        text = f.read()
    return text


def file_write(filepath, text):
    chunks = filepath.split('/')[:-1]
    chunk_curr = ''
    for chunk in chunks:
        chunk_curr += f'{chunk}/'
        try: os.makedirs(chunk_curr)
        except: pass

    with open(filepath, 'w', encoding='utf-8') as f: 
        f.write(text)




def create_folder_for_filepath(filepath):
    chunks = filepath.split('/')
    chunk_curr = ''
    for chunk in chunks[:-1]:
        chunk_curr += chunk + '/'
        try: os.makedirs(chunk_curr)
        except: pass


###################################
# JSON
###################################

def json_generate_if_not_exists(filepath):
    if not os.path.exists(filepath):
        file_append(filepath, '')

    if file_read(filepath).strip() == '':
        file_append(filepath, '{}')

def json_read(filepath):    
    with open(filepath, 'r', encoding='utf-8') as f: 
        return json.load(f)


def json_append(filepath, data):
    with open(filepath, 'a', encoding='utf-8') as f:
        json.dump(data, f)


# def json_read(filepath):
#     print(filepath)
#     content = file_read(filepath)
#     if content.strip() == '': file_write(filepath, '{}')
#     with open(filepath, 'r', encoding='utf-8') as f: 
#         return json.load(f)


def json_write(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f)





###################################
# FORMAT
###################################

def text_format_131(text):
    text_formatted = ''
    lines = text.split('. ')
    line_0 = lines[0]
    line_1 = '. '.join(lines[1:-1])
    line_2 = lines[-1]
    text_formatted += f'{line_0}.\n\n'
    text_formatted += f'{line_1}.\n\n'
    text_formatted += f'{line_2}.\n\n'
    text_formatted = text_formatted.replace('..', '.')
    return text_formatted

    
def text_format_131_html(text):
    text_formatted = ''
    lines = text.split('. ')
    line_0 = lines[0]
    line_1 = '. '.join(lines[1:-1])
    line_2 = lines[-1]
    text_formatted += f'<p>{line_0}.</p>' + '\n'
    text_formatted += f'<p>{line_1}.</p>' + '\n'
    text_formatted += f'<p>{line_2}.</p>' + '\n'
    text_formatted = text_formatted.replace('..', '.')
    return text_formatted




    
def text_format_1N1_html(text):
    text_formatted = ''
    lines = text.split('. ')
    lines_num = len(lines[1:-1])
    paragraphs = []
    paragraphs.append(lines[0])
    if lines_num > 3: 
        paragraphs.append('. '.join(lines[1:lines_num//2+1]))
        paragraphs.append('. '.join(lines[lines_num//2+1:-1]))
    else:
        paragraphs.append('. '.join(lines[1:-1]))
    paragraphs.append(lines[-1])
    for paragraph in paragraphs:
        text_formatted += f'<p>{paragraph}.</p>' + '\n'
    text_formatted = text_formatted.replace('..', '.')
    return text_formatted


def list_to_html(lst):
    html = ''
    html += '<ul>\n'
    for item in lst: 
        html += f'<li>{item}</li>\n'
    html += '</ul>\n'
    return html


def list_bold_to_html(lst):
    html = ''
    html += '<ul>\n'
    for item in lst: 
        if ':' in item:
            item_parts = item.split(":")
            html += f'<li><strong>{item_parts[0]}</strong>: {item_parts[1]}</li>\n'
        else:
            html += f'<li>{item}</li>\n'
    html += '</ul>\n'
    return html


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





###################################
# IMAGES
###################################

def img_resize(img, w=768, h=578):
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

    return img






###################################################################################################################
# COMPONENTS
###################################################################################################################

def component_header():
    return f'''
        <header>
            <div class="logo">
                [logo]
            </div>
            <nav>
                <input type="checkbox" class="toggle-menu">
                <div class="hamburger"></div>
                <ul class="menu">
                    <li><a href="/">Home</a></li>
                    <li><a href="/settori.html">Settori</a></li>
                    <li><a href="/servizi.html">Servizi</a></li>
                    <li><a href="/missione.html">Missione</a></li>
                    <li><a href="/contatti.html">Contatti</a></li>
                    <li><a href="/ozono.html">Ozono</a></li>
                </ul>
            </nav>
        </header>
    '''
                    # <li><a href="/prodotti.html">Prodotti</a></li>


def component_header_logo():
    logo = '<a href="/"><img src="logo-white.png" alt="logo ozonogroup"></a>'
    header = component_header()
    header = header.replace('[logo]', logo)
    return header
    

def component_header_no_logo():
    logo = '<a href="/">Ozonogroup</a>'
    header = component_header()
    header = header.replace('[logo]', logo)
    return header



###################################################################################################################
# META
###################################################################################################################

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


def meta_reading_time(article_html):
    reading_time = len(article_html.split(' ')) // 200
    return reading_time


def generate_breadcrumbs(filepath_in):
    filepath_chunks = filepath_in.split('/')
    breadcrumbs = [f.replace('.json', '').title() for f in filepath_chunks[2:-1]]
    article_name = filepath_chunks[-1].replace('.json', '').replace('-', ' ').title()
    
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
    breadcrumbs_html_formatted.append(f' > {article_name}')

    breadcrumbs_html_formatted = ''.join(breadcrumbs_html_formatted)

    return breadcrumbs_html_formatted


