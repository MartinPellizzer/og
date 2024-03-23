import os
import csv
import json


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




###################################
# JSON
###################################

def json_append(filepath, data):
    with open(filepath, 'a', encoding='utf-8') as f:
        json.dump(data, f)


def json_read(filepath):
    filepath_create(filepath)

    content = file_read(filepath)
    if content.strip() == '': file_write(filepath, '{}')
    with open(filepath, 'r', encoding='utf-8') as f: 
        return json.load(f)


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
# SCIENTIFIC NAME
###################################

def get_scientific_name(common_name, delimiter='\\'):
    rows = csv_get_rows('plants.csv', delimiter=delimiter)
    rows = [
        row 
        for row in rows 
        if row[1].lower().strip().replace(' ', '-') == common_name.lower().strip().replace(' ', '-')]
    scientific_name = rows[0][0].replace('-', ' ')
    return scientific_name
    
def get_common_name(entity, delimiter='\\'):
    rows = csv_get_rows('plants.csv', delimiter=delimiter)
    rows = [
        row 
        for row in rows 
        if row[0].lower().strip().replace(' ', '-') == entity.lower().strip().replace(' ', '-')]
    name = rows[0][1].replace('-', ' ')
    return name




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
