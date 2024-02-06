from PIL import Image, ImageDraw, ImageFont
import textwrap


def file_read(filepath):
    with open(filepath, 'a', encoding='utf-8') as f: pass
    with open(filepath, 'r', encoding='utf-8') as f: 
        text = f.read()
    return text




a4_w, a4_h = 2480, 3508

a4_mx = a4_w//100*5

column_num = 3
column_w = (a4_w - a4_mx*2)//column_num
column_gap = a4_mx*0.5
line_num = column_num-1

img = Image.new("RGB", (a4_w, a4_h), "white")
draw = ImageDraw.Draw(img)

# DRAW MARGINS
draw.line((a4_mx, 0, a4_mx, a4_h), fill=128)
draw.line((a4_w - a4_mx, 0, a4_w - a4_mx, a4_h), fill=128)

# DRAW COLUMNS
# for i in range(line_num):
#     draw.line((column_w*(i+1) + a4_mx - column_gap, 0, column_w*(i+1) + a4_mx  - column_gap, a4_h), fill='#a21caf')
#     draw.line((column_w*(i+1) + a4_mx, 0, column_w*(i+1) + a4_mx, a4_h), fill=128)
#     draw.line((column_w*(i+1) + a4_mx + column_gap, 0, column_w*(i+1) + a4_mx  + column_gap, a4_h), fill='#a21caf')

# DRAW IMAGE
image_span = 2
image_w = a4_mx + (column_w * image_span)
draw.rectangle(((a4_mx, 300), (image_w - column_gap, 1500)), fill="#e5e5e5")

# DRAW TEXT
font_size = 32
font = ImageFont.truetype("arial.ttf", 32)
text_width = column_w - column_gap


content = file_read('col-1.md')
lines = textwrap.wrap(content, width=48)
y = 1500 + 200
for line in lines:
    words = line.split(" ")
    words_length = sum(draw.textlength(w, font=font) for w in words)
    space_length = (text_width - words_length) / (len(words) - 1)
    x = 0
    for word in words:
        draw.text((x + a4_mx, y), word, font=font, fill="black")
        x += draw.textlength(word, font=font) + space_length
    y += font_size*1.2

content = file_read('col-2.md')
lines = textwrap.wrap(content, width=48)
y = 1500 + 200
for line in lines:
    words = line.split(" ")
    words_length = sum(draw.textlength(w, font=font) for w in words)
    space_length = (text_width - words_length) / (len(words) - 1)
    x = 0
    for word in words:
        draw.text((x + a4_mx + column_w + column_gap//2, y), word, font=font, fill="black")
        x += draw.textlength(word, font=font) + space_length
    y += font_size*1.2

content = file_read('col-3.md')
lines = textwrap.wrap(content, width=48)
y = 300
for line in lines:
    words = line.split(" ")
    words_length = sum(draw.textlength(w, font=font) for w in words)
    space_length = (text_width - words_length) / (len(words) - 1)
    x = 0
    for word in words:
        draw.text((x + a4_mx + column_w*2 + column_gap, y), word, font=font, fill="black")
        x += draw.textlength(word, font=font) + space_length
    y += font_size*1.2

img.show()