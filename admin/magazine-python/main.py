from PIL import Image, ImageDraw, ImageFont, ImageOps
import textwrap
import os

BODY_FONT_SIZE = 44
WORDS_SPACING = 42
BODY_LINE_SPACING = 1.25
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
    draw.line((a4_mx, 0, a4_mx, A4_H), fill='#a21caf')
    draw.line((A4_W - a4_mx, 0, A4_W - a4_mx, A4_H), fill='#a21caf')
    draw.line((0, a4_my, A4_W, a4_my), fill='#a21caf')
    draw.line((0, A4_H - a4_my, A4_W, A4_H - a4_my), fill='#a21caf')


def debug_columns():
    for i in range(column_num-1):
        draw.line((column_w*(i+1) + a4_mx - column_gap, 0, column_w*(i+1) + a4_mx  - column_gap, A4_H), fill='#a21caf')
        draw.line((column_w*(i+1) + a4_mx, 0, column_w*(i+1) + a4_mx, A4_H), fill='#a21caf')
        draw.line((column_w*(i+1) + a4_mx + column_gap, 0, column_w*(i+1) + a4_mx  + column_gap, A4_H), fill='#a21caf')


def debug_rows():
    for i in range(row_num-1):
        draw.line((0, row_h*(i+1) + a4_my, A4_W, row_h*(i+1) + a4_my), fill='#a21caf')


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
    font = ImageFont.truetype(font, BODY_FONT_SIZE)
    for i, line in enumerate(lines):
        draw.text((x, y + BODY_FONT_SIZE*BODY_LINE_SPACING*i), line, font=font, fill=color)
    
        
def draw_text_right(text, font, col, row, color):
    x, y, _, _ = get_coord(col, row, 0, 0)

    lines = text_to_lines(text, column_w)
    font = ImageFont.truetype(font, BODY_FONT_SIZE)
    for i, line in enumerate(lines):
        line_w = font.getbbox(line)[2]
        draw.text((x + (column_w - line_w), y + BODY_FONT_SIZE*BODY_LINE_SPACING*i), line, font=font, fill=color)


def draw_text_right_2(text, font, x, y, color):
    lines = text_to_lines(text, column_w)
    font = ImageFont.truetype(font, BODY_FONT_SIZE)
    for i, line in enumerate(lines):
        line_w = font.getbbox(line)[2]
        draw.text((x + (column_w - line_w), y + BODY_FONT_SIZE*BODY_LINE_SPACING*i), line, font=font, fill=color)

    
def draw_page_number_left(page_num, color):
    text = f'{page_num}   |   OZONOGROUP'
    draw_text_left(text, "arialbd.ttf", 0, 32, color)
    

def draw_page_number_right(page_num, color):
    text = f'OZONOGROUP   |   {page_num}'
    draw_text_right(text, "arialbd.ttf", 2, 32, color)


def draw_title(title, x, y):
    title = title.strip()
    title_lines = title.split('\n')

    font_size = 250
    font = ImageFont.truetype("arial.ttf", font_size)

    for i, line in enumerate(title_lines):
        draw.text((x, y + font_size*1.0*i - int(font_size*0.2)), line.strip(), font=font, fill="black")



#####################################################################
# ;MAIN
#####################################################################

A4_W, A4_H = 2480, 3508


img = Image.new("RGB", (A4_W, A4_H), "white")
draw = ImageDraw.Draw(img)


a4_mx = A4_W//100*5
a4_my = A4_H//100*5


column_num = 2
column_w = (A4_W - a4_mx*2)//column_num
column_gap = a4_mx*0.5

row_num = 32
row_h = (A4_H - a4_my*2)//row_num
row_gap = a4_my*0.5



def get_coord(cs, rs, ce, re):
    x = a4_mx + column_w*cs
    y = a4_my + row_h*rs
    w = column_w*(ce-cs+1)
    h = row_h*(re-rs+1)
    return x, y, w, h


def text_to_lines(text, text_width):
    font = ImageFont.truetype(TEXT_FONT, BODY_FONT_SIZE)
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
    font = ImageFont.truetype(TEXT_FONT, FONT_SIZE)
    text_width_optim = 0
    text_width_curr_best = 9999
    step_num = 10
    for i in range(step_num):
        offset = i*FONT_SIZE
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


def draw_text_column(filename, x_start, y_start, color='#000000', align='left'):
    font = ImageFont.truetype(TEXT_FONT, FONT_SIZE)
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
            y += FONT_SIZE*TEXT_LINE_SPACING*2
        else:
            if align == 'left':
                lines_num = len(paragraphs[paragraph_index])
                if lines_num == 1:
                    line = paragraphs[paragraph_index][0]
                    if line.startswith('## '):
                        line = line.replace('## ', '').strip()
                        font_size_title = 48
                        font = ImageFont.truetype("arialbd.ttf", font_size_title)
                        draw.text((x_start, y), line, font=font, fill=color)
                        font = ImageFont.truetype(TEXT_FONT, FONT_SIZE)
                        y += font_size_title - FONT_SIZE
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
                                y += FONT_SIZE*TEXT_LINE_SPACING
                            else:
                                draw.text((x_start, y), line, font=font, fill=color)
            elif align == 'center':
                for i, line in enumerate(paragraphs[paragraph_index]):
                    line_w = font.getbbox(line)[2]
                    draw.text((x_start + column_w//2 - line_w//2, y), line, font=font, fill=color)
                    y += FONT_SIZE*TEXT_LINE_SPACING


def gen_template_1(page_num):
    x, y, w, h = get_coord(0, 1, 1, 12)
    img_resize(f'page-{page_num}/image.jpg', f'page-{page_num}/image-resized.jpg', w - column_gap//2, h, 90)
    img_featured = Image.open(f'page-{page_num}/image-resized.jpg')
    img.paste(img_featured, (x, y))

    title = '''
    Stagionatura
    Formaggio
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

    font = ImageFont.truetype("arial.ttf", FONT_SIZE)
    x, y, _, _ = get_coord(0, 12, 0, 0)
    draw_text_column(f'page-{page_num}/col-1.md', x, y)

    font = ImageFont.truetype("arial.ttf", FONT_SIZE)
    x, y, _, _ = get_coord(1, 12, 0, 0)
    draw_text_column(f'page-{page_num}/col-2.md', x, y)
    
    font = ImageFont.truetype("arial.ttf", FONT_SIZE)
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
        draw.text((x + column_w//2 - line_w//2, y + FONT_SIZE*1.5*i - int(FONT_SIZE*0.2)), line, font=font, fill="black")

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
    font = ImageFont.truetype("arial.ttf", FONT_SIZE)
    x, y, _, _ = get_coord(1, 29, 0, 0)
    draw_text_column(f'page-{page_num}/img-desc.md', x, y)

    # HEADER DESCRIPTION
    font = ImageFont.truetype(TEXT_FONT, FONT_SIZE)
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
        draw.text((x + int(column_w-line_w), y+FONT_SIZE*i*TEXT_LINE_SPACING), line, font=font, fill="black")

    img.save(f'exports/page-3.jpg', quality=50)


def gen_template_4(page_num):
    global img
    global draw

    x, y, w, h = get_coord(1, 0, 2, 31)
    img_resize(f'page-{page_num}/0000.jpg', f'page-{page_num}/0000-resized.jpg', A4_W-x, A4_H, 90)
    img_featured = Image.open(f'page-{page_num}/0000-resized.jpg')
    img.paste(img_featured, (x, 0))

    x, y, w, h = get_coord(0, 0, 0, 31)
    draw.rectangle(((0, 0), (w+a4_mx+column_gap, A4_H)), fill="#18181b")

    font = ImageFont.truetype(TEXT_FONT, FONT_SIZE)
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

    font = ImageFont.truetype("arial.ttf", FONT_SIZE)
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
    draw.rectangle(((x, y-A4_H), (x+div_w, y+div_h)), fill="#000000")
        

    # TEXT 1
    filepath = 'text-1.md'
    text = file_read(f'page-{page_num}/{filepath}')
    lines = text_to_lines(text, column_w-column_gap)
    font = ImageFont.truetype("arial.ttf", FONT_SIZE)
    x, y, _, _ = get_coord(2, 1, 0, 0)
    for i, line in enumerate(lines):
        draw.text((x+column_gap, y + FONT_SIZE*TEXT_LINE_SPACING*i), line.strip(), font=font, fill="#000000")

    # PAGE NUM
    draw_page_number_right(page_num, '#000000')

    img.save(f'exports/page-{page_num}.jpg', quality=50)


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
    img.paste(foreground, (A4_W-a4_mx-circle_size, y), foreground)

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

    x, y, w, h = 0, 0, column_w*2, A4_H
    img_resize(
        f'page-{page_num}/0000.jpg', 
        f'page-{page_num}/0000-resized.jpg', 
        w, h, 90
    )
    img_featured = Image.open(f'page-{page_num}/0000-resized.jpg')
    img.paste(img_featured, (x, y))
    
    # TEXT 1
    x, y, _, _ = get_coord(1, 31, 0, 0)
    text = file_read(f'page-{page_num}/text-1.md')
    draw_text_right_2(text, "arial.ttf", x-column_gap*4, y, '#ffffff')

    # COL 3
    x, y, _, _ = get_coord(2, 1, 2, 30)
    draw_text_column(f'page-{page_num}/col-3.md', x, y, color='#000000')

    draw_page_number_right(page_num, '#000000')

    img.save(f'exports/page-{page_num}.jpg', quality=50)
    

def draw_img_circle(filepath, x, y, d):    
    # CREATE MASK
    mask = Image.new("L", (d, d), "black")
    draw_circle = ImageDraw.Draw(mask)
    draw_circle.ellipse((0, 0, d, d), fill='white')

    # CLIP IMAGE TO MASK
    img_circle = Image.open(filepath)
    img_circle = ImageOps.fit(img_circle, mask.size, centering=(0.5, 0.5))
    img_circle.putalpha(mask)

    # PASTE CIRCLE IMAGE TO PAGE
    img.paste(img_circle, (x, y), img_circle)


def get_xy_from_cr(c, r):
    x = a4_mx + column_w*c
    y = a4_my + row_h*r
    return x, y


# TODO: RETURN LIST OF PARAGRAPHS INSTEAD OF FLAT LIST
# YOU NEED SEPARATE PARAGRAPHS FOR DRAWING JUSTIFY CONTENT CORRECTLY
# (MANAGING LAST LINE OF PARAGRAPH AS LEFT ALIGN IN JUSTIFY)
def get_lines_from_text(font, text, text_width):
    paragraphs = text.split('\n\n')
    lines = []
    for paragraph in paragraphs:
        words = paragraph.split(' ')
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
        lines.append('\n\n')

    # REMOVE LAST EMPTY LINE
    print(lines)
    lines = lines[:-1]
    print(lines)
    quit()

    return lines


def get_lines_from_text_2(text, text_width, font):
    paragraphs_lines = []

    paragraphs = text.split('\n\n')
    for paragraph in paragraphs:
        words = paragraph.split(' ')
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
        paragraphs_lines.append(lines)

    return paragraphs_lines


def draw_text(text, x, y, w, font_size, font_family='arial.ttf', align='left'):
    text = text.strip()
    text_lines = text.split('\n')

    font = ImageFont.truetype(font_family, font_size)

    if align == 'left':
        for i, line in enumerate(text_lines):
            draw.text((x, y + font_size*1.0*i - int(font_size*0.2)), line.strip(), font=font, fill="black")
    if align == 'center':
        for i, line in enumerate(text_lines):
            line = line.strip()
            line_w = font.getbbox(line)[2]
            draw.text((x + w//2 - line_w//2, y + font_size*1.0*i - int(font_size*0.2)), line.strip(), font=font, fill="black")


def draw_text_2(lines, x, y, w, font_size, font_family='arial.ttf', align='left'):
    font = ImageFont.truetype(font_family, font_size)

    if align == 'left':
        for i, line in enumerate(lines):
            draw.text((x, y + font_size*1.0*i - int(font_size*0.2)), line.strip(), font=font, fill="black")
    if align == 'center':
        for i, line in enumerate(lines):
            line = line.strip()
            line_w = font.getbbox(line)[2]
            draw.text((x + w//2 - line_w//2, y + font_size*1.0*i - int(font_size*0.2)), line.strip(), font=font, fill="black")


def gen_template_9(page_num):

    d = int(column_w-column_gap)
    x, y, _, _ = get_coord(0, 9, 0, 0)
    draw_img_circle(f'page-{page_num}/0000.jpg', x, y, d)
    
    d = int(column_w-column_gap)
    x, y, _, _ = get_coord(1, 9, 0, 0)
    draw_img_circle(f'page-{page_num}/0001.jpg', x, y, d)
    
    d = int(column_w-column_gap)
    x, y, _, _ = get_coord(2, 9, 0, 0)
    draw_img_circle(f'page-{page_num}/0002.jpg', x, y, d)

    text = '''
    EMPEIT
    '''
    x, y = get_xy_from_cr(0, 17)
    draw_text(text, x, y, column_w, 96, 'arialbd.ttf', 'center')

    text = '''
    EMPORIST
    BEACH
    '''
    x, y = get_xy_from_cr(1, 17)
    draw_text(text, x, y, column_w, 96, 'arialbd.ttf', 'center')

    text = '''
    OCCULPA
    '''
    x, y = get_xy_from_cr(2, 17)
    draw_text(text, x, y, column_w, 96, 'arialbd.ttf', 'center')




    x, y = get_xy_from_cr(0, 19)
    draw_text_column(f'page-{page_num}/col-1.md', x, y, color='#000000', align='center')

    x, y = get_xy_from_cr(1, 20)
    draw_text_column(f'page-{page_num}/col-2.md', x+column_gap//2, y, color='#000000', align='center')

    x, y = get_xy_from_cr(2, 19)
    draw_text_column(f'page-{page_num}/col-3.md', x+column_gap, y, color='#000000', align='center')



    # DIVIDER
    div_thickness = 3
    x, y = get_xy_from_cr(0, 6)
    draw.rectangle(((x, y), (A4_W, y+div_thickness)), fill="#000000")

    # DIVIDER
    div_thickness = 3
    x1, y1 = get_xy_from_cr(1, 3)
    x2, y2 = get_xy_from_cr(1, 6)
    draw.rectangle(((x1, y1), (x1+div_thickness, y2)), fill="#000000")

    # DIVIDER
    div_thickness = 3
    x1, y1 = get_xy_from_cr(2, 3)
    x2, y2 = get_xy_from_cr(2, 6)
    draw.rectangle(((x1, y1), (x1+div_thickness, y2)), fill="#000000")

    
    x, y = get_xy_from_cr(0, 4)
    draw_text_column(f'page-{page_num}/text-1.md', x, y, color='#000000', align='center')
    
    x, y = get_xy_from_cr(1, 4)
    draw_text_column(f'page-{page_num}/text-2.md', x, y, color='#000000', align='center')
    
    x, y = get_xy_from_cr(2, 4)
    draw_text_column(f'page-{page_num}/text-3.md', x, y, color='#000000', align='center')

    
    text = '''
    YOUR
    TRAVEL
    '''
    x, y = get_xy_from_cr(1, 0)
    draw_text(text, x, y, column_w, 48, 'arialbd.ttf', 'center')


    draw_page_number_left(page_num, '#000000')

    img.save(f'exports/page-{page_num}.jpg', quality=50)


def gen_template_10(page_num):

    d = int(column_w-column_gap)
    x, y, _, _ = get_coord(0, 9, 0, 0)
    draw_img_circle(f'page-{page_num}/0000.jpg', x, y, d)
    
    d = int(column_w-column_gap)
    x, y, _, _ = get_coord(1, 9, 0, 0)
    draw_img_circle(f'page-{page_num}/0001.jpg', x, y, d)
    
    d = int(column_w-column_gap)
    x, y, _, _ = get_coord(2, 9, 0, 0)
    draw_img_circle(f'page-{page_num}/0002.jpg', x, y, d)

    text = '''
    IHITI DESED
    TORPOR
    '''
    x, y = get_xy_from_cr(0, 17)
    draw_text(text, x, y, column_w, 96, 'arialbd.ttf', 'center')

    text = '''
    OVITEC
    '''
    x, y = get_xy_from_cr(1, 17)
    draw_text(text, x, y, column_w, 96, 'arialbd.ttf', 'center')

    text = '''
    EDIET AUT
    '''
    x, y = get_xy_from_cr(2, 17)
    draw_text(text, x, y, column_w, 96, 'arialbd.ttf', 'center')




    x, y = get_xy_from_cr(0, 20)
    draw_text_column(f'page-{page_num}/col-1.md', x, y, color='#000000', align='center')

    x, y = get_xy_from_cr(1, 19)
    draw_text_column(f'page-{page_num}/col-2.md', x+column_gap//2, y, color='#000000', align='center')

    x, y = get_xy_from_cr(2, 19)
    draw_text_column(f'page-{page_num}/col-3.md', x+column_gap, y, color='#000000', align='center')



    # DIVIDER
    div_thickness = 3
    x, y = get_xy_from_cr(0, 6)
    draw.rectangle(((0, y), (A4_W-a4_mx, y+div_thickness)), fill="#000000")

    # DIVIDER
    div_thickness = 3
    x1, y1 = get_xy_from_cr(1, 3)
    x2, y2 = get_xy_from_cr(1, 6)
    draw.rectangle(((x1, y1), (x1+div_thickness, y2)), fill="#000000")

    # DIVIDER
    div_thickness = 3
    x1, y1 = get_xy_from_cr(2, 3)
    x2, y2 = get_xy_from_cr(2, 6)
    draw.rectangle(((x1, y1), (x1+div_thickness, y2)), fill="#000000")

    
    x, y = get_xy_from_cr(0, 4)
    draw_text_column(f'page-{page_num}/text-1.md', x, y, color='#000000', align='center')
    
    x, y = get_xy_from_cr(1, 4)
    draw_text_column(f'page-{page_num}/text-2.md', x, y, color='#000000', align='center')
    
    x, y = get_xy_from_cr(2, 4)
    draw_text_column(f'page-{page_num}/text-3.md', x, y, color='#000000', align='center')

    
    text = '''
    YOUR
    TRAVEL
    '''
    x, y = get_xy_from_cr(1, 0)
    draw_text(text, x, y, column_w, 48, 'arialbd.ttf', 'center')


    draw_page_number_right(page_num, '#000000')

    img.save(f'exports/page-{page_num}.jpg', quality=50)




def get_coord_2(cs, rs, ce, re):
    x = a4_mx + column_w*cs
    y = a4_my + row_h*rs
    w = a4_mx + column_w*ce
    h = a4_my + row_h*re
    return [x, y, w, h]


def draw_line_justify(words, font, x, y, w):
    words_length = sum(draw.textlength(w, font=font) for w in words)
    space_length = (column_w - column_gap - words_length) / (len(words) - 1)
    for word in words:
        draw.text((x, y), word, font=font, fill="#000000")
        x += draw.textlength(word, font=font) + space_length


def draw_cols_text(cols, article, align='left'):
    font_family = 'arial.ttf'

    font_size = BODY_FONT_SIZE
    line_spacing = BODY_LINE_SPACING   
    font = ImageFont.truetype(font_family, font_size)

    paragraphs = get_lines_from_text_2(article, column_w-column_gap, font)
    
    
    col_index = 0
    x, y, w, h = cols[col_index]

    for paragraph in paragraphs:
        lines = paragraph
        lines_num = len(lines)
        for i, line in enumerate(lines):
            if y > h:
                col_index += 1
                if col_index >= len(cols): break
                x, y, w, h = cols[col_index]

            line_w = font.getbbox(line)[2]
            line_h = font.getbbox(line)[3]
            if align == 'left':
                draw.text((x, y), line, font=font, fill="#000000")
            elif align == 'right':
                draw.text((x + column_w-column_gap-line_w, y), line, font=font, fill="#000000")
            elif align == 'center':
                draw.text((x + column_w//2-line_w//2 - column_gap//2, y), line, font=font, fill="#000000")
            elif align == 'justify':
                if i != lines_num - 1:
                    words = line.split(" ")
                    if len(words) != 1:
                        draw_line_justify(words, font, x, y, w)
                    else:
                        draw.text((x, y), line, font=font, fill="#000000")
                else:
                    draw.text((x, y), line, font=font, fill="#000000")

            y += font_size*line_spacing
        y += font_size*line_spacing





# TODO: manage cols with different width
# to do that, manage one line at the time when splitting lines
# and do the splitting inside the loop
def gen_template_11(page_num):
    draw.rectangle(((0, 0), (A4_W, A4_H)), fill="#ffffff")

    # ARTICLE
    article = file_read(f'page-{page_num}/article.md')
    cols = [
        get_coord_2(0, 20, 1, 30), 
        get_coord_2(1, 20, 2, 30), 
        get_coord_2(2, 1, 3, 30),
    ]
    cols[1][0] += column_gap//2
    cols[2][0] += column_gap
    draw_cols_text(cols, article, align='justify')

    # IMAGE
    images = [image for image in os.listdir(f'page-{page_num}') if 'resized' not in image]

    image_name, image_ext = images[0].split('.')
    x, y, w, h = get_coord(0, 1, 1, 12)
    img_resize(
        f'page-{page_num}/{image_name}.{image_ext}', 
        f'page-{page_num}/{image_name}-resized.{image_ext}', 
        w - column_gap//2, h, 50)
    img_featured = Image.open(f'page-{page_num}/{image_name}-resized.{image_ext}')
    img.paste(img_featured, (x, y))

    # TITLE
    text = f'''
    Come Inattivare Le Muffe 
    Nelle Sale Di Stagionatura
    Dei Formaggi
    '''
    lines = [line.strip() for line in text.split('\n') if line.strip() != '']
    x, y, w, h = get_coord(0, 15, 0, 0)
    font_size = 112
    draw_text_2(lines, x, y, w, font_size, font_family='arialbd.ttf', align='left')

    # PAGE NUMBER
    if page_num % 2 != 0: draw_page_number_left(page_num, '#000000')
    else: draw_page_number_right(page_num, '#000000')

    img.save(f'exports/page-{page_num}.jpg', quality=50)

    
def gen_template_12(page_num):

    # IMAGE
    images = [image for image in os.listdir(f'page-{page_num}') if 'resized' not in image]

    image_name, image_ext = images[0].split('.')
    x, y, w, h = get_coord(1, 1, 2, 9)
    img_resize(
        f'page-{page_num}/{image_name}.{image_ext}', 
        f'page-{page_num}/{image_name}-resized.{image_ext}', 
        w - column_gap, h, 50)
    img_featured = Image.open(f'page-{page_num}/{image_name}-resized.{image_ext}')
    img.paste(img_featured, (x+int(column_gap), y))

    image_name, image_ext = images[1].split('.')
    x, y, w, h = get_coord(1, 10, 2, 17)
    img_resize(
        f'page-{page_num}/{image_name}.{image_ext}', 
        f'page-{page_num}/{image_name}-resized.{image_ext}', 
        w - column_gap, h, 50)
    img_featured = Image.open(f'page-{page_num}/{image_name}-resized.{image_ext}')
    img.paste(img_featured, (x+int(column_gap), y+int(row_h//2)))

    
    image_name, image_ext = images[2].split('.')
    x, y, w, h = get_coord(1, 19, 2, 30)
    img_resize(
        f'page-{page_num}/{image_name}.{image_ext}', 
        f'page-{page_num}/{image_name}-resized.{image_ext}', 
        w - column_gap, h, 50)
    img_featured = Image.open(f'page-{page_num}/{image_name}-resized.{image_ext}')
    img.paste(img_featured, (x+int(column_gap), y))

    # ARTICLE
    article = file_read(f'page-{page_num}/article.md')
    cols = [
        get_coord_2(0, 1, 1, 30), 
    ]
    draw_cols_text(cols, article, align='justify')

    # PAGE NUMBER
    if page_num % 2 != 0: draw_page_number_left(page_num, '#000000')
    else: draw_page_number_right(page_num, '#000000')

    img.save(f'exports/page-{page_num}.jpg', quality=50)
    

    
    
def preview_template_full(page_num_1, page_num_2):
    
    A4_W_full, A4_H_full = 2480*2, 3508

    img_full = Image.new("RGB", (A4_W_full, A4_H_full), "white")
    draw_full = ImageDraw.Draw(img)

    img_1 = Image.open(f'exports/page-{page_num_1}.jpg')
    img_2 = Image.open(f'exports/page-{page_num_2}.jpg')

    img_full.paste(img_1, (0, 0))
    img_full.paste(img_2, (2480, 0))

    img_full.save(f'exports/export-{page_num_1}-{page_num_2}.jpg', quality=50)
    img_full.show()
    
        
def gen_template_13(page_num):

    # IMAGE
    images_folderpath = f'page-{page_num}/img'
    images = [image for image in os.listdir(images_folderpath)]

    image_name, image_ext = images[0].split('.')
    x, y, w, h = get_coord(0, 1, 0, 12)
    img_resize(
        f'{images_folderpath}/{image_name}.{image_ext}', 
        f'page-{page_num}/{image_name}-resized.{image_ext}', 
        w-int(column_gap), h, 50)
    img_featured = Image.open(f'page-{page_num}/{image_name}-resized.{image_ext}')
    img.paste(img_featured, (x, y))


    # TITLE
    text = f'''
    Come Inattivare Le Muffe 
    Nelle Sale Di Stagionatura
    Dei Formaggi
    '''
    lines = [line.strip() for line in text.split('\n') if line.strip() != '']
    x, y, w, h = get_coord(0, 14, 0, 0)
    font_size = 80
    draw_text_2(lines, x, y, w, font_size, font_family='arialbd.ttf', align='left')


    # ARTICLE
    article = file_read(f'page-{page_num}/article.md')
    cols = [
        get_coord_2(0, 17, 2, 30),
        get_coord_2(1, 1, 2, 30),
    ]
    cols[1][0] += column_gap
    draw_cols_text(cols, article, align='justify')


    # PAGE NUMBER
    if page_num % 2 != 0: draw_page_number_left(page_num, '#000000')
    else: draw_page_number_right(page_num, '#000000')

    img.save(f'exports/page-{page_num}.jpg', quality=50)
    

def gen_template_14(page_num):


    # IMAGE
    images_folderpath = f'page-{page_num}/img'
    images = [image for image in os.listdir(images_folderpath)]

    
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



    image_name, image_ext = images[0].split('.')
    x, y, w, h = get_coord(0, 1, 0, 12)
    img_resize(
        f'{images_folderpath}/{image_name}.{image_ext}', 
        f'page-{page_num}/{image_name}-resized.{image_ext}', 
        w-int(column_gap), h, 50)
    img_featured = Image.open(f'page-{page_num}/{image_name}-resized.{image_ext}')
    img.paste(img_featured, (x, y))


    # TITLE
    text = f'''
    Come Inattivare Le Muffe 
    Nelle Sale Di Stagionatura
    Dei Formaggi
    '''
    lines = [line.strip() for line in text.split('\n') if line.strip() != '']
    x, y, w, h = get_coord(0, 14, 0, 0)
    font_size = 80
    draw_text_2(lines, x, y, w, font_size, font_family='arialbd.ttf', align='left')


    # ARTICLE
    article = file_read(f'page-{page_num}/article.md')
    cols = [
        get_coord_2(0, 17, 2, 30),
        get_coord_2(1, 1, 2, 30),
    ]
    cols[1][0] += column_gap
    draw_cols_text(cols, article, align='justify')


    # PAGE NUMBER
    if page_num % 2 != 0: draw_page_number_left(page_num, '#000000')
    else: draw_page_number_right(page_num, '#000000')

    img.save(f'exports/page-{page_num}.jpg', quality=50)
    


# gen_template_1(1)
# gen_template_2(2)
# gen_template_3(3)
# gen_template_4(4)
# gen_template_5(5)
# gen_template_6(6)
# gen_template_7(7)
# gen_template_8(8)
# gen_template_9(9)
# gen_template_10(10)
# gen_template_11(1)
# gen_template_12(2)
# gen_template_13(13)
gen_template_14(14)
# preview_template_full(1, 2)

debug_margins()
debug_columns()
debug_rows()
debug_cells()

# img.show()




# images = [
#     Image.open("exports/" + f)
#     for f in ['page-9.jpg', 'page-10.jpg', 'page-1.jpg', 'page-2.jpg', 'page-3.jpg', 'page-4.jpg', 'page-5.jpg', 'page-6.jpg', 'page-7.jpg', 'page-8.jpg']
# ]

# pdf_path = "magazine.pdf"
    
# images[0].save(
#     pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
# )