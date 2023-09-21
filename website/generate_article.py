import re
import csv
import markdown

from PIL import Image, ImageFont, ImageDraw, ImageColor 



encoding = 'utf-8'

def csv_get_rows(filename):
    _rows = []
    with open(f"database/{filename}.csv", "r", encoding=encoding) as f:
        reader = csv.reader(f, delimiter="\\")
        for i, line in enumerate(reader):
            _rows.append(line)
    return _rows

    
def row_to_dict(row):
    fields = {}
    for i, col in enumerate(row):
        fields[col] = i
    return fields


def get_line_data_2(row, fields):
    data = {}
    for key, value in fields.items():
        data[key] = row[value]
    return data


def generate_line_application(row, fields):
    data = get_line_data_2(row, fields)
    
    if data['ozone_type'].strip() != '': 
        data['ozone_type'] =  'in forma ' + data['ozone_type']

    if data['o3_concentration'].strip() != '': 
        data['o3_concentration'] =  'a una concentrazione di ' + data['o3_concentration']
        
    if data['treatment_time'].strip() != '': 
        data['treatment_time'] =  'per un tempo di ' + data['treatment_time']
        
    if data['pathogen_reduction_number'].strip() != '': 
        if data['pathogen_reduction_number_unit'].strip() == '%':
            data['pathogen_reduction_number'] =  'del ' + data['pathogen_reduction_number'] + data['pathogen_reduction_number_unit']
        else:
            data['pathogen_reduction_number'] =  'di ' + data['pathogen_reduction_number'] + ' ' + data['pathogen_reduction_number_unit']

    if data['pathogen_reduction_text'].strip() != '': 
        data['pathogen_reduction_text'] =  'in modo ' + data['pathogen_reduction_text']

    sentence = ''

    sentence += f'''
        Riduce 
        il livello di
        {data['problem']}
        {data['pathogen_reduction_number']} 
        {data['pathogen_reduction_text']}
        , se usato 
        {data['ozone_type']}
        {data['w_pressure']} 
        {data['o3_concentration']} 
        {data['treatment_time']} 

        .
        '''

    sentence_formatted = sentence.replace('\n', '')
    sentence_formatted = re.sub(' +', ' ', sentence_formatted)
    sentence_formatted = sentence_formatted.replace(' ,', ',')
    sentence_formatted = sentence_formatted.replace(' .', '.')
    
    return f'- {sentence_formatted}\n'
    

def generate_line_quality(row, fields):
    data = get_line_data_2(row, fields)

    if data['o3_concentration'].strip() != '': 
        data['o3_concentration'] =  'a una concentrazione di ' + data['o3_concentration']
        
    if data['treatment_time'].strip() != '': 
        data['treatment_time'] =  'per un tempo di ' + data['treatment_time']
  
    data['results'] = data['results'].lower().capitalize()

    sentence = ''

    sentence += f'''
        {data['results']} 
        del 
        {data['product']} 
        , se usato 
        {data['o3_concentration']} 
        {data['treatment_time']} 

        .
        '''

    sentence_formatted = sentence.replace('\n', '')
    sentence_formatted = re.sub(' +', ' ', sentence_formatted)
    sentence_formatted = sentence_formatted.replace(' ,', ',')
    sentence_formatted = sentence_formatted.replace(' .', '.')
    
    return f'- {sentence_formatted}\n'




with open('test.md', 'w', encoding=encoding) as f:
    f.write('')












def generate_section_quality(product):
    text_intro = ''

    text_list_intro = ''
    

    # LISTA ------------------------------------------------------------
    text_list = ''

    rows = csv_get_rows('experiments-quality')
    fields = row_to_dict(rows[0])
    rows = rows[1:]

    for i, row in enumerate(rows):
        if row[fields['product_type']].strip().lower() == product.lower().strip():
            text_list += generate_line_quality(row, fields)
            
    # WRITE ON TEST FILE ------------------------------------------------------------
    text = text_intro + text_list_intro + text_list
    with open('test.md', 'a', encoding=encoding) as f:
        f.write(f'### {product.capitalize()}\n\n')
        f.write(f'{text}\n\n')


def generate_section(product):
    text_intro = ''
    
    _rows = csv_get_rows('experiments-reduction')
    _fields = row_to_dict(_rows[0])


    # GET LIST OF PROBLEMS AND STUDIES FORM PRODUCT TYPE -------------------------------
    # TODO: remove duplicates
    problem_list = []
    study_list = []
    study_year_list = []
    for i, _row in enumerate(_rows):
        if _row[_fields['product_type']].strip().lower() == product.lower().strip():
            problem_list.append(_row[_fields['problem']].strip())
            study_list.append(_row[_fields['study']].strip())
            study_year_list.append(_row[_fields['study_year']].strip())

    problem_list = list(dict.fromkeys(problem_list))
    study_list = list(dict.fromkeys(study_list))
    study_year_list = list(dict.fromkeys(study_year_list))

    # GET PRODUCT AD 3
    _rows = csv_get_rows('products')
    _fields = row_to_dict(_rows[0])

    _product_ad = ''
    _product = ''
    for _row in _rows:
        _product = _row[_fields['product_type']].strip().lower()
        if _product == product:
            _product_ad = _row[_fields['product_ad_3']].lower()
            break
  
    # WRITE TEXT
    if len(problem_list) == 0: problems = ''
    elif len(problem_list) == 1: problems = f'{problem_list[0]}'
    elif len(problem_list) == 2: problems = f'{problem_list[0]} e {problem_list[1]}'
    else: problems = f'{problem_list[0]}, {problem_list[1]} e {problem_list[2]}'

    if len(study_list) == 0: studies = ''
    elif len(study_list) == 1: studies = f'{study_list[0]} ({study_year_list[0]})'
    else: studies = f'{study_list[0]} ({study_year_list[0]}) e {study_list[1]} ({study_year_list[1]})'

    text_intro += f'''
        L'ozono viene usato per trattare {_product_ad}{_product}
        , eliminando problemi come {problems}.
        Questo è dimostrato da vari studi, come {studies}.
    '''
    text_intro = text_intro.replace('\n', '').strip()
    text_intro = re.sub(' +', ' ', text_intro)
    text_intro = text_intro.replace(' ,', ',')
    text_intro += '\n\n'
     
    
    # INTRODUZIONE LISTA -----------------------------------------------
    text_list_intro = ''

    _rows = csv_get_rows('products')
    _fields = row_to_dict(_rows[0])
    _rows = _rows[1:]

    _product = ''
    _product_ad_2 = ''
    for i, _row in enumerate(_rows):
        if _row[_fields['product_type']].strip().lower() == product.lower().strip():
            _product = _row[_fields['product_type']]
            _product_ad_2 = _row[_fields['product_ad_2']]
            break

    text_list_intro += f'''
        Ecco una lista di alcune applicazioni dell\'ozono 
        {_product_ad_2}{_product}:
    '''
    text_list_intro = text_list_intro.replace('\n', '').strip()
    text_list_intro = re.sub(' +', ' ', text_list_intro)
    text_list_intro += '\n\n'

    # LISTA ------------------------------------------------------------
    text_list = ''

    _rows = csv_get_rows('experiments-reduction')
    _fields = row_to_dict(_rows[0])
    _rows = _rows[1:]

    for i, _row in enumerate(_rows):
        if _row[_fields['product_type']].strip().lower() == product.lower().strip():
            text_list += generate_line_application(_row, _fields)
            
    # WRITE ON TEST FILE ------------------------------------------------------------
    text = text_intro + text_list_intro + text_list
    with open('test.md', 'a', encoding=encoding) as f:
        f.write(f'### {product.capitalize()}\n\n')
        f.write(f'{text}\n\n')
    


# GENERATE EXPERIMENTS SECTION
_rows = csv_get_rows('experiments-reduction')
_fields = row_to_dict(_rows[0])
product_type_list = []
for _row in _rows:
    if 'lattiero-casearia' == _row[_fields['industry']].strip().lower():
        product_type = _row[_fields['product_type']].strip().lower()
        if product_type not in product_type_list:
            product_type_list.append(product_type)

for product_type in product_type_list:
    generate_section(product_type)


# GENERATE SECTION QUALITY
rows = csv_get_rows('experiments-quality')
fields = row_to_dict(rows[0])

product_type_list = []
for row in rows:
    if 'lattiero-casearia' == row[fields['industry']].strip().lower():
        product_type = row[fields['product_type']].strip().lower()
        if product_type not in product_type_list:
            product_type_list.append(product_type)





for product_type in product_type_list:
    generate_section_quality(product_type)
    # print(product_type)
    pass



quit()


















# IMAGES -----------------------------------------------------------------------------------

def text_split(text, font, img_w, px):
    lines = text.strip().split('\n')

    words = []
    for line in lines:
        if not line:
            words.append('\n')
        else:
            line_words = line.split()
            for word in line_words:
                words.append(word)

    lines = []
    line = ''
    for word in words:
        if word == '\n':
            lines.append(line)
            lines.append('')
            line = ''
        else:
            word_w = font.getsize(word)[0]
            line_w = font.getsize(line)[0]
            if word_w + line_w < img_w - px:
                line += word + ' '
            else:
                lines.append(line)
                line = word + ' '
    lines.append(line)

    return lines


def lines_max_height(lines, font):
    line_height = 0
    for line in lines:
        if line_height < font.getsize(line)[1]: 
            line_height = font.getsize(line)[1]
    return line_height


def generate_image_sanitation(image_out_path):    
    img_w, img_h = 768, 432
    img = Image.new("RGBA", (img_w, img_h), ImageColor.getrgb("#f8fafc"))

    draw = ImageDraw.Draw(img)

    # TITLE
    draw.rectangle(((0, 0), (img_w, 112)), fill=ImageColor.getrgb("#2563eb"))
    
    text_size = 40
    text = 'Sanificazione ad ozono nell\'industria lattiero-casearia'
    px = img_w - img_w * 0.9
    pt = 8

    font = ImageFont.truetype("fonts/arial.ttf", text_size)

    lines = text_split(text, font, img_w, px) 
    line_height = lines_max_height(lines, font) * 1.2
    text_height = line_height * len(lines)

    for i, line in enumerate(lines):
        line_w = font.getsize(line)[0]
        draw.text(
            (img_w//2 - line_w//2, (line_height * i) + pt), 
            line, 
            (255,255,255), 
            font=font
            )


    #ICONS
    icon_size = (128, 128)
    label_y = 64
    pos_y = 224

    

    pos_x = 0.2
    icon_bg = Image.new('RGBA', icon_size, (0, 0, 0, 0))
    icon_fg = Image.new("RGBA", icon_size, ImageColor.getrgb("#2563eb"))
    icon_mask = Image.open('assets/icons/articles/milk.png').convert('L').resize(icon_size)
    icon = Image.composite(icon_bg, icon_fg, icon_mask)
    img.paste(icon, (int(img_w * pos_x) - icon_size[0]//2, pos_y), icon)
    
    text_size = 24
    text = 'Latte'
    text_w = font.getsize(text)[0]
    draw.text((int(img_w * pos_x) - text_w//2, pos_y - label_y), text, ImageColor.getrgb("#2563eb"), font=font)


    pos_x = 0.5
    icon_bg = Image.new('RGBA', icon_size, (0, 0, 0, 0))
    icon_fg = Image.new("RGBA", icon_size, ImageColor.getrgb("#2563eb"))
    icon_mask = Image.open('assets/icons/articles/cheese.png').convert('L').resize(icon_size)
    icon = Image.composite(icon_bg, icon_fg, icon_mask)
    img.paste(icon, (int(img_w * pos_x) - icon_size[0]//2, pos_y), icon)
    
    text_size = 24
    text = 'Formaggio'
    text_w = font.getsize(text)[0]
    draw.text((int(img_w * pos_x) - text_w//2, pos_y - label_y), text, ImageColor.getrgb("#2563eb"), font=font)


    pos_x = 0.8
    icon_bg = Image.new('RGBA', icon_size, (0, 0, 0, 0))
    icon_fg = Image.new("RGBA", icon_size, ImageColor.getrgb("#2563eb"))
    icon_mask = Image.open('assets/icons/articles/yogurt.png').convert('L').resize(icon_size)
    icon = Image.composite(icon_bg, icon_fg, icon_mask)
    img.paste(icon, (int(img_w * pos_x) - icon_size[0]//2, pos_y), icon)
    
    text_size = 24
    text = 'Yogurt'
    text_w = font.getsize(text)[0]
    draw.text((int(img_w * pos_x) - text_w//2, pos_y - label_y), text, ImageColor.getrgb("#2563eb"), font=font)


    img.convert('RGB').save(f'{image_out_path}')
    img.show()

generate_image_sanitation('assets/images/articles/ozono-sanificazione-industria-lattiero-casearia.jpg')

quit()





with open('test.md', encoding=encoding) as f:
    generated_content = f.read()

# generated_content = text

content_html = markdown.markdown(generated_content, extensions=['markdown.extensions.tables', 'meta'])

md = markdown.Markdown(extensions=['meta'])
md.convert(generated_content)


lines = '\n'.join(md.lines)

content_html = markdown.markdown(lines, extensions=['markdown.extensions.tables'])

    
with open(f'_tmp_{table}.html', 'w', encoding=encoding) as f:
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