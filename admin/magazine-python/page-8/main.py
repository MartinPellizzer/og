from PIL import Image, ImageDraw, ImageFont, ImageOps
import textwrap
import os

TEXT_SIZE = 36
WORDS_SPACING = 42
TEXT_LINE_SPACING = 1.25
TEXT_FONT = 'times.ttf'
TEXT_FONT = 'arial.ttf'


def file_read(filepath):
    with open(filepath, 'a', encoding='utf-8') as f: pass
    with open(filepath, 'r', encoding='utf-8') as f: 
        text = f.read()
    return text


def img_resize(image_path_in, image_path_out, w, h, quality=100):
    img = Image.open(image_path_in)

    start_size = img.size
    end_size = (w, h)

    if start_size[0] / end_size [0] < start_size[1] / end_size [1]:
        ratio = start_size[0] / end_size[0]
        new_end_size = (int(end_size[0]), int(start_size[1] / ratio))
    else:
        ratio = start_size[1] / end_size[1]
        new_end_size = (int(start_size[0] / ratio), int(end_size[1]))

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
    img.save(output_path, quality=quality)

    return output_path





#####################################################################
# ;DEBUG
#####################################################################

def debug_margins():
    draw.line((a4_mx, 0, a4_mx, a4_h), fill='#a21caf')
    draw.line((a4_w - a4_mx, 0, a4_w - a4_mx, a4_h), fill='#a21caf')
    draw.line((0, a4_my, a4_w, a4_my), fill='#a21caf')
    draw.line((0, a4_h - a4_my, a4_w, a4_h - a4_my), fill='#a21caf')


def debug_columns():
    for i in range(column_num-1):
        draw.line((column_w*(i+1) + a4_mx - column_gap, 0, column_w*(i+1) + a4_mx  - column_gap, a4_h), fill='#a21caf')
        draw.line((column_w*(i+1) + a4_mx, 0, column_w*(i+1) + a4_mx, a4_h), fill='#a21caf')
        draw.line((column_w*(i+1) + a4_mx + column_gap, 0, column_w*(i+1) + a4_mx  + column_gap, a4_h), fill='#a21caf')


def debug_rows():
    for i in range(row_num-1):
        draw.line((0, row_h*(i+1) + a4_my, a4_w, row_h*(i+1) + a4_my), fill='#a21caf')


def debug_cells():
    font_size = 64
    font = ImageFont.truetype("arialbd.ttf", font_size)
    for i in range(column_num):
        for k in range(row_num):
            coord = f'({i}, {k})'
            draw.text((a4_mx + column_w*i, a4_my + row_h*k), coord, font=font, fill='#a21c')



#####################################################################
# ;TEXT
#####################################################################
def draw_text_left(text, font, col, row, color):
    x, y, _, _ = get_coord(col, row, 0, 0)

    lines = text_to_lines(text, column_w)
    font = ImageFont.truetype(font, TEXT_SIZE)
    for i, line in enumerate(lines):
        draw.text((x, y + TEXT_SIZE*TEXT_LINE_SPACING*i), line, font=font, fill=color)
    
        
def draw_text_right(text, font, col, row, color):
    x, y, _, _ = get_coord(col, row, 0, 0)

    lines = text_to_lines(text, column_w)
    font = ImageFont.truetype(font, TEXT_SIZE)
    for i, line in enumerate(lines):
        line_w = font.getbbox(line)[2]
        draw.text((x + (column_w - line_w), y + TEXT_SIZE*TEXT_LINE_SPACING*i), line, font=font, fill=color)

    
def draw_page_number_left(page_num, color):
    text = f'{page_num}   |   OZONOGROUP'
    draw_text_left(text, "arialbd.ttf", 0, 32, color)
    

def draw_page_number_right(page_num, color):
    text = f'OZONOGROUP   |   {page_num}'
    draw_text_right(text, "arialbd.ttf", 2, 32, color)



#####################################################################
# ;MAIN
#####################################################################

a4_w, a4_h = 2480, 3508


img = Image.new("RGB", (a4_w, a4_h), "white")
draw = ImageDraw.Draw(img)


a4_mx = a4_w//100*5
a4_my = a4_h//100*5


column_num = 3
column_w = (a4_w - a4_mx*2)//column_num
column_gap = a4_mx*0.5

row_num = 32
row_h = (a4_h - a4_my*2)//row_num
row_gap = a4_my*0.5



def get_coord(cs, rs, ce, re):
    x = a4_mx + column_w*cs
    y = a4_my + row_h*rs
    w = column_w*(ce-cs+1)
    h = row_h*(re-rs+1)
    return x, y, w, h


def text_to_lines(text, text_width):
    font = ImageFont.truetype(TEXT_FONT, TEXT_SIZE)
    words = text.split(' ')
    lines = []
    line_curr = ''
    for word in words:
        word_w = font.getbbox(word)[2]
        line_curr_w = font.getbbox(line_curr)[2]
        if word_w + line_curr_w < text_width:
            line_curr += word + ' '
        else:
            lines.append(line_curr.strip())
            line_curr = word + ' '
    lines.append(line_curr.strip())
    return lines


def text_to_lines_optim(text):
    font = ImageFont.truetype(TEXT_FONT, TEXT_SIZE)
    text_width_optim = 0
    text_width_curr_best = 9999
    step_num = 10
    for i in range(step_num):
        offset = i*TEXT_SIZE
        lines = text_to_lines(text, column_w-offset)

        text_width_min = 9999
        text_width_max = 0
        for line in lines[:-1]:
            line_w = font.getbbox(line)[2]
            if text_width_min > line_w: text_width_min = line_w
            if text_width_max < line_w: text_width_max = line_w
        if text_width_curr_best > text_width_max - text_width_min:
            text_width_curr_best = text_width_max - text_width_min
            text_width_optim = column_w-offset
    
    lines = text_to_lines(text, text_width_optim)
    return lines


def draw_text_column(filename, x_start, y_start, color='#000000'):
    font = ImageFont.truetype(TEXT_FONT, TEXT_SIZE)
    text_width = column_w - column_gap

    content = file_read(filename)
    paragraph_list = content.split('\n')
    paragraphs = []
    for paragraph in paragraph_list:
        lines = textwrap.wrap(paragraph, width=WORDS_SPACING)
        # lines = text_to_lines_optim(paragraph)
        paragraphs.append(lines)

    y = y_start
    for i in range(len(paragraphs)):
        paragraph_index = i
        # IF PARAGRAPH IS NONE OR EMPTY: RENDER BLANK LINE (TO SEPARATE NEXT PARAGRAPH)
        # >> maybe fix "text_to_lines_optim" to get none list instead of empty one 
        if not paragraphs[paragraph_index] or paragraphs[paragraph_index][0] == '':
            y += TEXT_SIZE*TEXT_LINE_SPACING*2
        else:
            lines_num = len(paragraphs[paragraph_index])
            if lines_num == 1:
                line = paragraphs[paragraph_index][0]
                if line.startswith('## '):
                    line = line.replace('## ', '').strip()
                    font_size_title = 48
                    font = ImageFont.truetype("arialbd.ttf", font_size_title)
                    draw.text((x_start, y), line, font=font, fill=color)
                    font = ImageFont.truetype(TEXT_FONT, TEXT_SIZE)
                    y += font_size_title - TEXT_SIZE
                else:
                    draw.text((x_start, y), line, font=font, fill=color)
            else:
                for i, line in enumerate(paragraphs[paragraph_index]):
                    if i != lines_num - 1:
                        words = line.split(" ")
                        words_length = sum(draw.textlength(w, font=font) for w in words)
                        space_length = (text_width - words_length) / (len(words) - 1)
                        x = x_start
                        for word in words:
                            draw.text((x, y), word, font=font, fill=color)
                            x += draw.textlength(word, font=font) + space_length
                        y += TEXT_SIZE*TEXT_LINE_SPACING
                    else:
                        draw.text((x_start, y), line, font=font, fill=color)


def gen_template_1(page_num):
    x, y, w, h = get_coord(0, 1, 1, 12)
    img_resize(f'page-{page_num}/image.jpg', f'page-{page_num}/image-resized.jpg', w - column_gap//2, h, 90)
    img_featured = Image.open(f'page-{page_num}/image-resized.jpg')
    img.paste(img_featured, (x, y))

    title = '''
    Nature\'s
    Wonderland
    '''

    title = title.strip()
    title_lines = title.split('\n')

    font_size = 192
    font = ImageFont.truetype("arial.ttf", font_size)

    x, y, _, _ = get_coord(0, 15, 0, 0)
    for i, line in enumerate(title_lines):
        draw.text((x, y + font_size*1.0*i - int(font_size*0.2)), line.strip(), font=font, fill="black")

    x, y, _, _ = get_coord(0, 20, 0, 0)
    draw_text_column(f'page-{page_num}/col-1.md', x, y)

    x, y, _, _ = get_coord(1, 20, 0, 0)
    draw_text_column(f'page-{page_num}/col-2.md', x+column_gap//2, y)

    x, y, _, _ = get_coord(2, 1, 0, 0)
    draw_text_column(f'page-{page_num}/col-3.md', x+column_gap, y)

    draw_page_number_left(page_num, '#000000')

    img.save(f'exports/page-1.jpg', quality=50)


def gen_template_2(page_num):

    x, y, w, h = get_coord(1, 1, 2, 9)
    img_resize(f'page-{page_num}/0001.jpg', f'page-{page_num}/0001-resized.jpg', int(w-column_gap), h, 90)
    img_featured = Image.open(f'page-{page_num}/0001-resized.jpg')
    img.paste(img_featured, (x+int(column_gap), y))


    x, y, w, h = get_coord(1, 10, 2, 17)
    img_resize(f'page-{page_num}/0002.jpg', f'page-{page_num}/0002-resized.jpg', int(w-column_gap), h, 90)
    img_featured = Image.open(f'page-{page_num}/0002-resized.jpg')
    img.paste(img_featured, (x+int(column_gap), y+int(row_h//2)))


    x, y, w, h = get_coord(1, 19, 2, 30)
    img_resize(f'page-{page_num}/0003.jpg', f'page-{page_num}/0003-resized.jpg', int(w-column_gap), h, 90)
    img_featured = Image.open(f'page-{page_num}/0003-resized.jpg')
    img.paste(img_featured, (x+int(column_gap), y))


    font_size = 32
    font = ImageFont.truetype("arial.ttf", font_size)
    x, y, _, _ = get_coord(0, 1, 0, 0)
    draw_text_column(f'page-{page_num}/col-1.md', x, y)

    draw_page_number_right(page_num, '#000000')

    img.save(f'exports/page-2.jpg', quality=50)


def gen_template_3(page_num):
    global img
    global draw

    title = '''
    Travelling
    Alone
    '''
    title = title.strip()
    title_lines = title.split('\n')
    font_size = 320
    font = ImageFont.truetype("arial.ttf", font_size)
    x, y, _, _ = get_coord(0, 4, 0, 0)
    for i, line in enumerate(title_lines):
        draw.text((x, y + font_size*1.0*i - int(font_size*0.2)), line.strip(), font=font, fill="black")

    font = ImageFont.truetype("arial.ttf", TEXT_SIZE)
    x, y, _, _ = get_coord(0, 12, 0, 0)
    draw_text_column(f'page-{page_num}/col-1.md', x, y)

    font = ImageFont.truetype("arial.ttf", TEXT_SIZE)
    x, y, _, _ = get_coord(1, 12, 0, 0)
    draw_text_column(f'page-{page_num}/col-2.md', x, y)
    
    font = ImageFont.truetype("arial.ttf", TEXT_SIZE)
    x, y, _, _ = get_coord(2, 12, 0, 0)
    draw_text_column(f'page-{page_num}/col-3.md', x, y)

    draw_page_number_left(page_num, '#000000')

    text = '''
    OZONO
    MAGAZINE
    '''
    text = text.strip()
    text_lines = text.split('\n')
    font = ImageFont.truetype("arial.ttf", 48)
    x, y, _, _ = get_coord(1, 0, 0, 0)
    for i, line in enumerate(text_lines):
        line = line.strip()
        line_w = font.getbbox(line)[2]
        draw.text((x + column_w//2 - line_w//2, y + TEXT_SIZE*1.5*i - int(TEXT_SIZE*0.2)), line, font=font, fill="black")

    img.save(f'page-{page_num}/page-2.png', quality=50)


    # CIRCLE IMAGE
    img_circle = Image.new("RGB", (column_w, column_w), "black")
    draw_circle = ImageDraw.Draw(img_circle)
    draw_circle.ellipse((0, 0, column_w-column_gap, column_w-column_gap), fill='white')
    img_circle.save(f'page-{page_num}/circle-mask.jpg', quality=100)

    mask_circle = Image.open(f'page-{page_num}/circle-mask.jpg').convert('L')
    img_circle = Image.open(f'page-{page_num}/0000.jpg')

    img_circle = ImageOps.fit(img_circle, mask_circle.size, centering=(0.5, 0.5))
    img_circle.putalpha(mask_circle)

    img_circle.save(f'page-{page_num}/circle-image.png')

    # CIRCLE COMPOSITE
    img = Image.open(f'page-{page_num}/page-2.png')
    draw = ImageDraw.Draw(img)

    foreground = Image.open(f'page-{page_num}/circle-image.png')

    x, y, _, _ = get_coord(1, 21, 0, 0)
    img.paste(foreground, (x, y), foreground)

    # IMAGE DESCRIPTION
    font = ImageFont.truetype("arial.ttf", TEXT_SIZE)
    x, y, _, _ = get_coord(1, 29, 0, 0)
    draw_text_column(f'page-{page_num}/img-desc.md', x, y)

    # HEADER DESCRIPTION
    font = ImageFont.truetype(TEXT_FONT, TEXT_SIZE)
    filepath = f'page-{page_num}/header-text.md'
    text = file_read(filepath)
    words = text.split(' ')
    lines = []
    line_curr = ''
    for word in words:
        word_w = font.getbbox(word)[2]
        line_curr_w = font.getbbox(line_curr)[2]
        if line_curr_w + word_w < int(column_w*0.75):
            line_curr += word + ' '
        else:
            lines.append(line_curr)
            line_curr = word + ' '
    lines.append(line_curr)

    x, y, _, _ = get_coord(2, 4, 0, 0)
    for i, line in enumerate(lines):
        line = line.strip()
        line_w = font.getbbox(line)[2]
        draw.text((x + int(column_w-line_w), y+TEXT_SIZE*i*TEXT_LINE_SPACING), line, font=font, fill="black")

    img.save(f'exports/page-3.jpg', quality=50)


def gen_template_4(page_num):
    global img
    global draw

    x, y, w, h = get_coord(1, 0, 2, 31)
    img_resize(f'page-{page_num}/0000.jpg', f'page-{page_num}/0000-resized.jpg', a4_w-x, a4_h, 90)
    img_featured = Image.open(f'page-{page_num}/0000-resized.jpg')
    img.paste(img_featured, (x, 0))

    x, y, w, h = get_coord(0, 0, 0, 31)
    draw.rectangle(((0, 0), (w+a4_mx+column_gap, a4_h)), fill="#18181b")

    font = ImageFont.truetype(TEXT_FONT, TEXT_SIZE)
    x, y, _, _ = get_coord(0, 0, 0, 31)
    draw_text_column(f'page-{page_num}/col-1.md', x, y, color='#ffffff')

    draw_page_number_right(page_num, '#ffffff')

    img.save(f'exports/page-4.jpg', quality=50)

    
def gen_template_5(page_num):
    global img
    global draw

    # TITLE
    title = '''
    Uncover
    The Hidden
    Gems
    '''

    title = title.strip()
    title_lines = title.split('\n')

    font_size = 250
    font = ImageFont.truetype("arial.ttf", font_size)

    x, y, _, _ = get_coord(0, 1, 0, 0)
    for i, line in enumerate(title_lines):
        draw.text((x, y + font_size*1.0*i - int(font_size*0.2)), line.strip(), font=font, fill="black")

    # DIVIDER
    div_thickness = 20
    div_length = 128
    x, y, _, _ = get_coord(0, 8, 0, 0)
    draw.rectangle(((x, y+row_h-div_thickness), (x+div_length, y+row_h)), fill="#000000")
        
    # SUBTITLE
    title = '''
    TRAVEL ON MARS
    '''

    title = title.strip()
    title_lines = title.split('\n')

    font_size = 48
    font = ImageFont.truetype("arialbd.ttf", font_size)

    x, y, _, _ = get_coord(0, 10, 0, 0)
    for i, line in enumerate(title_lines):
        draw.text((x, y + font_size*1.0*i - int(font_size*0.2)), line.strip(), font=font, fill="black")

    # TEXT
    # filepath = 'text-1.md'
    # x, y, _, _ = get_coord(0, 11, 0, 0)
    # draw_text_column(f'page-{page_num}/{filepath}', x+column_gap, y, color='#000000')

    # TEXT
    filepath = 'text-1.md'
    text = file_read(f'page-{page_num}/{filepath}')
    lines = text_to_lines(text, column_w*1.5)

    font = ImageFont.truetype("arial.ttf", TEXT_SIZE)
    x, y, _, _ = get_coord(0, 11, 0, 0)
    for i, line in enumerate(lines):
        draw.text((x, y + font_size*1.0*i - int(font_size*0.2)), line.strip(), font=font, fill="#000000")
    # print(lines)
    # quit()

    # x, y, _, _ = get_coord(0, 11, 0, 0)
    # draw_text_column(f'page-{page_num}/{filepath}', x+column_gap, y, color='#000000')


    # IMAGE
    x, y, w, h = get_coord(0, 14, 1, 29)
    img_resize(f'page-{page_num}/0000.jpg', f'page-{page_num}/0000-resized.jpg', w-column_gap, h, 90)
    img_featured = Image.open(f'page-{page_num}/0000-resized.jpg')
    img.paste(img_featured, (x, y))

    # COL 3
    x, y, _, _ = get_coord(2, 1, 0, 0)
    draw_text_column(f'page-{page_num}/col-3.md', x+column_gap, y, color='#000000')

    draw_page_number_left(page_num, '#000000')

    img.save(f'exports/page-{page_num}.jpg', quality=50)


def gen_template_6(page_num):
    global img
    global draw

    
    # IMAGE 1
    x, y, w, h = get_coord(0, 1, 0, 8)
    filename = '0000'
    img_resize(
        f'page-{page_num}/{filename}.jpg', 
        f'page-{page_num}/{filename}-resized.jpg', 
        w-column_gap, h, 90)
    img_featured = Image.open(f'page-{page_num}/{filename}-resized.jpg')
    img.paste(img_featured, (x, y))
    
    # IMAGE 2
    x, y, w, h = get_coord(0, 21, 0, 30)
    filename = '0001'
    img_resize(
        f'page-{page_num}/{filename}.jpg', 
        f'page-{page_num}/{filename}-resized.jpg', 
        w-column_gap, h, 90)
    img_featured = Image.open(f'page-{page_num}/{filename}-resized.jpg')
    img.paste(img_featured, (x, y))
    
    # IMAGE 3
    x, y, w, h = get_coord(2, 19, 2, 30)
    filename = '0002'
    img_resize(
        f'page-{page_num}/{filename}.jpg', 
        f'page-{page_num}/{filename}-resized.jpg', 
        w, h, 90)
    img_featured = Image.open(f'page-{page_num}/{filename}-resized.jpg')
    img.paste(img_featured, (x, y))

    # COL 1
    x, y, _, _ = get_coord(0, 11, 0, 0)
    draw_text_column(f'page-{page_num}/col-1.md', x, y, color='#000000')

    # COL 2
    x, y, _, _ = get_coord(1, 1, 1, 3)
    draw_text_column(f'page-{page_num}/col-2.md', x, y, color='#000000')

    # DIVIDER
    div_w = 3
    div_h = 1750
    x, y, _, _ = get_coord(2, 0, 0, 0)
    draw.rectangle(((x, y-a4_h), (x+div_w, y+div_h)), fill="#000000")
        

    # TEXT 1
    filepath = 'text-1.md'
    text = file_read(f'page-{page_num}/{filepath}')
    lines = text_to_lines(text, column_w-column_gap)
    font = ImageFont.truetype("arial.ttf", TEXT_SIZE)
    x, y, _, _ = get_coord(2, 1, 0, 0)
    for i, line in enumerate(lines):
        draw.text((x+column_gap, y + TEXT_SIZE*TEXT_LINE_SPACING*i), line.strip(), font=font, fill="#000000")

    # PAGE NUM
    draw_page_number_right(page_num, '#000000')

    img.save(f'exports/page-{page_num}.jpg', quality=50)


def draw_title(title, x, y):
    title = title.strip()
    title_lines = title.split('\n')

    font_size = 250
    font = ImageFont.truetype("arial.ttf", font_size)

    for i, line in enumerate(title_lines):
        draw.text((x, y + font_size*1.0*i - int(font_size*0.2)), line.strip(), font=font, fill="black")


def gen_template_7(page_num):
    global img
    global draw
    
    # TITLE
    title = '''
    Travel
    Maldives
    '''
    x, y, _, _ = get_coord(0, 2, 0, 0)
    draw_title(title, x, y)

    # COL 1
    x, y, _, _ = get_coord(0, 8, 0, 30)
    draw_text_column(f'page-{page_num}/col-1.md', x, y, color='#000000')

    # COL 2
    x, y, _, _ = get_coord(1, 8, 1, 30)
    draw_text_column(f'page-{page_num}/col-2.md', x, y, color='#000000')

    img.save(f'page-{page_num}/page-2.png', quality=50)

    # CIRCLE IMAGE
    circle_size = int(column_w*0.8)
    img_circle = Image.new("RGB", (circle_size, circle_size), "black")
    draw_circle = ImageDraw.Draw(img_circle)
    draw_circle.ellipse((0, 0, circle_size-column_gap, circle_size-column_gap), fill='white')
    img_circle.save(f'page-{page_num}/circle-mask.jpg', quality=100)

    mask_circle = Image.open(f'page-{page_num}/circle-mask.jpg').convert('L')
    img_circle = Image.open(f'page-{page_num}/0000.jpg')

    img_circle = ImageOps.fit(img_circle, mask_circle.size, centering=(0.5, 0.5))
    img_circle.putalpha(mask_circle)

    img_circle.save(f'page-{page_num}/circle-image.png')

    # CIRCLE COMPOSITE
    img = Image.open(f'page-{page_num}/page-2.png')
    draw = ImageDraw.Draw(img)

    foreground = Image.open(f'page-{page_num}/circle-image.png')

    x, y, _, _ = get_coord(2, 8, 0, 0)
    img.paste(foreground, (a4_w-a4_mx-circle_size, y), foreground)

    # TEXT 1
    text = file_read(f'page-{page_num}/text-1.md')
    draw_text_right(text, "arial.ttf", 2, 1, '#000000')
    
    # TEXT 2
    text = file_read(f'page-{page_num}/text-2.md')
    draw_text_right(text, "arial.ttf", 2, 15, '#000000')
    
    # PAGE NUM
    draw_page_number_left(page_num, '#000000')

    img.save(f'exports/page-{page_num}.jpg', quality=50)


def gen_template_8(page_num):
    global img
    global draw

    x, y, w, h = 0, 0, column_w*2, a4_h
    img_resize(
        f'page-{page_num}/0000.jpg', 
        f'page-{page_num}/0000-resized.jpg', 
        w, h, 90
    )
    img_featured = Image.open(f'page-{page_num}/0000-resized.jpg')
    img.paste(img_featured, (x, y))
    
    # TEXT 1
    text = file_read(f'page-{page_num}/text-1.md')
    draw_text_right(text, "arial.ttf", 2, 1, '#000000')

    # COL 3
    x, y, _, _ = get_coord(2, 1, 2, 30)
    draw_text_column(f'page-{page_num}/col-3.md', x, y, color='#000000')

    draw_page_number_right(page_num, '#000000')

    img.save(f'exports/page-{page_num}.jpg', quality=50)



# gen_template_1(1)
# gen_template_2(2)
# gen_template_3(3)
# gen_template_4(4)
# gen_template_5(5)
# gen_template_6(6)
# gen_template_7(7)
gen_template_8(8)


# debug_margins()
# debug_columns()
# debug_rows()
# debug_cells()



# print(text_width_optim)

# text = file_read('text.md')
# lines = text.split('\n')

# font = ImageFont.truetype(TEXT_FONT, TEXT_SIZE)
# x, y, _, _ = get_coord(0, 0, 0, 31)
# draw_text_column(f'page-1/col-1.md', x, y, color='#ffffff')

# img.save(f'tmp.jpg', quality=50)
img.show()