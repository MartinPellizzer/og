from PIL import Image, ImageDraw, ImageFont
import random

def draw_grid():
    for i in range(grid_col_num+1):
        draw.line((grid_col_w*i + grid_col_padding, 0, grid_col_w*i + grid_col_padding, page_h), fill='#ff00ff', width=4)
        draw.line((grid_col_w*i + grid_col_padding - grid_col_gap, 0, grid_col_w*i + grid_col_padding - grid_col_gap, page_h), fill='#ff00ff', width=4)
        draw.line((grid_col_w*i + grid_col_padding + grid_col_gap, 0, grid_col_w*i + grid_col_padding + grid_col_gap, page_h), fill='#ff00ff', width=4)

    for i in range(grid_row_num+1):
        draw.line((0, grid_row_h*i + grid_row_padding, page_w, grid_row_h*i + grid_row_padding), fill='#ff00ff', width=4)

def draw_text_col(lines, col_index, row_index):
    for i, line in enumerate(lines):
        x = grid_col_w*col_index + grid_col_padding + grid_col_gap*col_index
        y = grid_row_h*row_index + grid_row_padding + font_size*i
        draw.text((x, y), line, (0, 0, 0), font=font)


page_w = 2480
page_h = 3508

img = Image.new('RGB', (page_w, page_h), color='white')
draw = ImageDraw.Draw(img) 

# grid
grid_col_num = 3
grid_col_padding = 256
grid_col_gap = 16
grid_col_w = (page_w - grid_col_padding*2) // grid_col_num

grid_row_num = 16
grid_row_padding = 512
grid_row_h = (page_h - grid_row_padding*2) // grid_row_num

draw_grid()


with open('placeholder_text.txt', 'r', encoding='utf-8', errors='ignore') as f: text = f.read()
text = text.replace('\n', ' ')

font_size = 30
font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", font_size)

words = text.split(' ')
lines = []
line_curr = ''
for word in words:
    _, _, line_curr_w, _ = font.getbbox(line_curr)
    _, _, word_w, _ = font.getbbox(word)
    if line_curr_w + word_w < grid_col_w - grid_col_gap*2:
        line_curr += f'{word} '
    else:
        lines.append(line_curr)
        line_curr = f'{word} '
lines.append(line_curr)

# draw_text_col(lines, 0, 0)
# draw_text_col(lines, 1, 8)
# draw_text_col(lines, 2, 3)


rand_cols = random.randint(1, grid_col_num)
rand_rows = random.randint(1, grid_row_num)

x_1 = grid_col_w*0 + grid_col_padding
y_1 = grid_row_h*0 + grid_row_padding
x_2 = x_1 + grid_col_w*rand_cols
y_2 = y_1 + grid_row_h*rand_rows

draw_text_col(lines[:32], 0, 5)

draw.rectangle(((x_1, y_1), (x_2, y_2)), fill="#cdcdcd")

img.show()
# img.save('test.jpg')