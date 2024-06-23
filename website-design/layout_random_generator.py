import random
import lorem
import util

#############################################################
# ATOMS
#############################################################

def title_primary():
    return f'<h1 class="text-64">Medium length title</h1>'

def title_secondary():
    return f'<h2 class="text-48">Medium length title</h2>'

def title_tertiary():
    return f'<h3 class="text-24">Medium length title</h3>'

def link_primary():
    return f'<a class="text-18 no-underline font-bold text-black" href="">Action link</a>'

def link_secondary():
    return f'<a class="text-16 no-underline font-normal text-black uppercase" href="">Item</a>'

    
def list_u(length=8):
    return f'''
        <ul class="ml-24">
            <li class="text-18">{(' '.join(lorem.text().split(' ')[:length]) + '.').replace('..', '.')}</li>
            <li class="text-18">{(' '.join(lorem.text().split(' ')[:length]) + '.').replace('..', '.')}</li>
            <li class="text-18">{(' '.join(lorem.text().split(' ')[:length]) + '.').replace('..', '.')}</li>
            <li class="text-18">{(' '.join(lorem.text().split(' ')[:length]) + '.').replace('..', '.')}</li>
        </ul>
    '''

def paragraph(length=24):
    text = (' '.join(lorem.text().split(' ')[:length]) + '.').replace('..', '.')
    return f'<p class="text-18">{text}</h1>'

def image(src='', height=None):
    if height: height = f"height={height}"

    filepath = 'unsplash/random/urls.txt'
    if src == '': src = random.choice(util.file_read(filepath).split('\n')[:-1])
    return f'<img class="object-cover object-center" src="{src}" alt="" {height}>'





#############################################################
# LAYOUTS
#############################################################

def header_0003():
    html = f'''
        <section class="py-24">
            <div class="container-xl flex justify-between">
                <div>
                    {link_secondary()}
                </div>
                <div>
                    <nav class="flex gap-24">
                        {link_secondary()}
                        {link_secondary()}
                        {link_secondary()}
                        {link_secondary()}
                    </nav>
                </div>
            </div>
        </section>
    '''

    return html


def hero_0005():
    html = f'''
        <section class="py-96">
            <div class="container-xl text-center">
                <div>
                    {paragraph(length=1)}
                    <div class="mb-16"></div>
                    {title_primary()}
                    <div class="mb-16"></div>
                    <div>{link_primary()}</div>
                </div>
            </div>
        </section>
    '''

    return html


def content_0013():
    html = f'''
        <section class="py-96">
            <div class="container-xl flex items-center gap-96">
                <div class="flex-1">
                    {title_primary()}
                    <div class="mb-16"></div>
                    {paragraph()}
                    <div class="mb-16"></div>
                    <div>{link_primary()}</div>
                </div>
                <div class="flex-1">
                    {image()}
                </div>
            </div>
        </section>
    '''

    return html


def content_0000():
    html = f'''
        <section class="py-96">
            <div class="container-xl flex items-center gap-96">
                <div class="flex-1">
                    {title_tertiary()}
                    <div class="mb-16"></div>
                    {paragraph()}
                    <div class="mb-16"></div>
                    {list_u()}
                </div>
                <div class="flex-1">
                    {image()}
                </div>
            </div>
        </section>
    '''

    return html


def features_0002():
    html = f'''
        <section class="py-96">
            <div class="container-xl flex items-center gap-96">
                <div class="flex-1">
                    {title_tertiary()}
                    <div class="mb-16"></div>
                    {paragraph()}
                    <div class="mb-16"></div>
                    {link_primary()}
                </div>
                <div class="flex-1">
                    {title_tertiary()}
                    <div class="mb-16"></div>
                    {paragraph()}
                    <div class="mb-16"></div>
                    {link_primary()}
                </div>
                <div class="flex-1">
                    {title_tertiary()}
                    <div class="mb-16"></div>
                    {paragraph()}
                    <div class="mb-16"></div>
                    {link_primary()}
                </div>
            </div>
        </section>
    '''

    return html


def gallery_0004():
    image_height = 240

    html = f'''
        <section class="py-96">
            <div class="container-xl flex items-center gap-24">
                <div class="flex-1">
                    {image(height=image_height)}
                </div>
                <div class="flex-1">
                    {image(height=image_height)}
                </div>
                <div class="flex-1">
                    {image(height=image_height)}
                </div>
                <div class="flex-1">
                    {image(height=image_height)}
                </div>
            </div>
        </section>
    '''

    return html







#############################################################
# MAIN
#############################################################

# col_num_total = 12
# col_num_allocated = 0
# cols_span = []
# for i in range(999):
#     col_num_rand = random.randint(1, col_num_total)
#     if col_num_rand + col_num_allocated <= col_num_total:
#         cols_span.append(col_num_rand)
#         col_num_allocated += col_num_rand
#     if col_num_allocated == col_num_total:
#         break

# images = []
# for col_span in cols_span:
#     _image = image()
#     _block = f'<div class="flex-{col_span}">{_image}</div>'
#     images.append(_block)

# images = ''.join(images)

# row = f'''
#     <div class="container-xl flex">
#         {images}
#     </div>
# '''
# print(row)

def homepage():

    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
            <link rel="stylesheet" href="style-auto.css">
            <link rel="stylesheet" href="tailwind.css">
        </head>
        <body>
            {row}
        </body>
        </html>
    '''

    with open('layout-random-generator.html', 'w') as f:
        f.write(html)

homepage()