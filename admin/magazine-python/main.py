from PIL import Image, ImageDraw, ImageFont
import textwrap
import os


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
    img.save(output_path, quality=quality)

    return output_path



# for image_filename in os.listdir('in'):
#     print(image_filename)
#     image_path_in = 'in/' + image_filename
#     image_path_out = 'out/' + image_filename.replace('.png', '.jpg')
    
#     img_resize(image_path_in, image_path_out, w, h 70)








a4_w, a4_h = 2480, 3508

a4_mx = a4_w//100*5

column_num = 3
column_w = (a4_w - a4_mx*2)//column_num
column_gap = a4_mx*0.5
line_num = column_num-1

img = Image.new("RGB", (a4_w, a4_h), "white")
draw = ImageDraw.Draw(img)

# DRAW MARGINS
# draw.line((a4_mx, 0, a4_mx, a4_h), fill=128)
# draw.line((a4_w - a4_mx, 0, a4_w - a4_mx, a4_h), fill=128)

# DRAW COLUMNS
# for i in range(line_num):
#     draw.line((column_w*(i+1) + a4_mx - column_gap, 0, column_w*(i+1) + a4_mx  - column_gap, a4_h), fill='#a21caf')
#     draw.line((column_w*(i+1) + a4_mx, 0, column_w*(i+1) + a4_mx, a4_h), fill=128)
#     draw.line((column_w*(i+1) + a4_mx + column_gap, 0, column_w*(i+1) + a4_mx  + column_gap, a4_h), fill='#a21caf')

# DRAW IMAGE
image_span = 2
image_w = a4_mx + (column_w * image_span)
draw.rectangle(((a4_mx, 300), (image_w - column_gap, 1500)), fill="#e5e5e5")


img_resize(
    'image.jpg', 'image-resized.jpg', 
    (image_w - column_gap - a4_mx), 
    (1500 - 300), 90)

img_featured = Image.open('image-resized.jpg')
img.paste(img_featured, (a4_mx, 300))

# img.show()
# quit()

# DRAW TITLE
title = '''
Nature\'s
Wonderland
'''

title = title.strip()
title_lines = title.split('\n')

font_size = 192
font = ImageFont.truetype("arial.ttf", font_size)

for i, line in enumerate(title_lines):
    draw.text((a4_mx, 1500 + 200 + font_size*1.0*i), line, font=font, fill="black")






# drap paragraphs
# y = 2200
# for i in range(len(paragraphs)):
#     font_size = 32
#     font = ImageFont.truetype("arial.ttf", font_size)
#     paragraph_index = i
#     if not paragraphs[paragraph_index]:
#         y += font_size*1.2*2
#         pass
#     else:
#         lines_num = len(paragraphs[paragraph_index])

#         if lines_num == 1:
#             subtitle = paragraphs[paragraph_index][0]
#             if subtitle.startswith('## '):
#                 subtitle = subtitle.replace('## ', '').strip()
#                 # font_size = 32
#                 # font = ImageFont.truetype("arial.ttf", font_size)
#                 draw.text((a4_mx, y), subtitle, font=font, fill="black")
            
#         else:
#             for i, line in enumerate(paragraphs[paragraph_index]):
#                 if i != lines_num - 1:
#                     words = line.split(" ")
#                     words_length = sum(draw.textlength(w, font=font) for w in words)
#                     space_length = (text_width - words_length) / (len(words) - 1)
#                     x = 0
#                     for word in words:
#                         draw.text((x + a4_mx, y), word, font=font, fill="black")
#                         x += draw.textlength(word, font=font) + space_length
#                 else:
#                     draw.text((a4_mx, y), line, font=font, fill="black")

def draw_text_column(filename, x_start, y_start):
    # DRAW COLUMN
    font_size = 32
    font = ImageFont.truetype("arial.ttf", font_size)
    text_width = column_w - column_gap

    # split content in paragraphs
    content = file_read(filename)
    paragraph_list = content.split('\n')
    paragraphs = []
    for paragraph in paragraph_list:
        lines = textwrap.wrap(paragraph, width=48)
        paragraphs.append(lines)

    y = y_start
    for i in range(len(paragraphs)):
        paragraph_index = i
        if not paragraphs[paragraph_index]:
            y += font_size*1.2*2
        else:
            lines_num = len(paragraphs[paragraph_index])
            if lines_num == 1:
                line = paragraphs[paragraph_index][0]
                if line.startswith('## '):
                    line = line.replace('## ', '').strip()
                    font_size_title = 48
                    font = ImageFont.truetype("arialbd.ttf", font_size_title)
                    draw.text((x_start + a4_mx, y), line, font=font, fill="black")
                    font_size = 32
                    font = ImageFont.truetype("arial.ttf", font_size)
                    y += font_size_title - font_size
                else:
                    draw.text((x_start + a4_mx, y), line, font=font, fill="black")
            else:
                for i, line in enumerate(paragraphs[paragraph_index]):
                    if i != lines_num - 1:
                        words = line.split(" ")
                        words_length = sum(draw.textlength(w, font=font) for w in words)
                        space_length = (text_width - words_length) / (len(words) - 1)
                        x = x_start
                        for word in words:
                            draw.text((x + a4_mx, y), word, font=font, fill="black")
                            x += draw.textlength(word, font=font) + space_length
                        y += font_size*1.2
                    else:
                        draw.text((x_start + a4_mx, y), line, font=font, fill="black")

draw_text_column('col-1.md', column_w*0, 2200)
draw_text_column('col-2.md', column_w*1+column_gap//2, 2200)
draw_text_column('col-3.md', column_w*2+column_gap, 300)

# y = 2200
# for i in range(len(paragraphs)):
#     paragraph_index = i
#     if not paragraphs[paragraph_index]:
#         y += font_size*1.2*2
#     else:
#         lines_num = len(paragraphs[paragraph_index])
#         for i, line in enumerate(paragraphs[paragraph_index]):
#             if i != lines_num - 1:
#                 words = line.split(" ")
#                 words_length = sum(draw.textlength(w, font=font) for w in words)
#                 space_length = (text_width - words_length) / (len(words) - 1)
#                 x = 0
#                 for word in words:
#                     draw.text((x + a4_mx, y), word, font=font, fill="black")
#                     x += draw.textlength(word, font=font) + space_length
#                 y += font_size*1.2
#             else:
#                 draw.text((a4_mx, y), line, font=font, fill="black")


# img.show()
img.save('template-magazine-1.jpg', quality=50)