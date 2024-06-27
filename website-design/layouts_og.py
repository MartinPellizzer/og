import random
import lorem

#########################################################################
# ELEMENTS
#########################################################################

def spacer_lg():
    return f'<div class="mb-96"></div>'


def spacer_xl():
    return f'<div class="mb-192"></div>'


def title_big(text=None):
    if not text: text = 'Medium length engaging title'
    html = f'<h1 class="text-64 mb-24">{text}</h1>'
    return html


def title_mid(text=None, color='text-black'):
    if not text: text = 'Medium length engaging title'
    html = f'<h1 class="text-48 mb-24 {color}">{text}</h1>'
    return html

    
def paragraph(text='', length=16, color='text-black'):
    if text == '': text = (' '.join(lorem.text().split(' ')[:length]) + '.').replace('..', '.')
    return f'<p class="text-18 mb-24 {color}">{text}</p>'


def link_secondary(text=None):
    if not text: text = 'Action link'
    return f'<a class="text-16 no-underline font-normal text-black uppercase" href="">{text}</a>'


def bg_image(class_name, h):
    return f'<div class="{class_name} {h}">'


def image(src=None, height=600):
    if not src:
        filepath = f'unsplash/random/urls.txt'
        with open(filepath) as f:
            content = f.read()
        urls = content.strip().split('\n')
        src = random.choice(urls)
    return f'<img class="object-cover object-center" src="{src}" alt="" height={height}>'


#########################################################################
# HEADERS
#########################################################################

def header_0000():
    html = f'''
        <section class="py-24">
            <div class="container-xl flex justify-between">
                <div>
                    {link_secondary('Ozonogroup')}
                </div>
                <div>
                    <nav class="flex gap-24">
                        {link_secondary('Ozono')}
                        {link_secondary('Prodotti')}
                        {link_secondary('Servizi')}
                        {link_secondary('Contatti')}
                    </nav>
                </div>
            </div>
        </section>
    '''

    return html


#########################################################################
# LAYOUTS
#########################################################################

def template_0000():
    html = f'''
        <div class="container-xl flex items-center gap-96 mb-48">
            <div class="flex-3">
                {title_big('Sanificazione Ozono Veloce, Sicura, Ecologica')}
            </div>
            <div class="flex-1">
                {paragraph()}
            </div>
        </div>
        <div class="bg-dark">
            {image(src='assets/hero-03.png', height=600)}
        </div>
    '''

    return html

def template_0001():
    html = f'''
    '''

    return html

def template_content_image(bg_color='', color=''):
    return f'''
        <div class="{bg_color}">
            <div class="container-xl flex items-center gap-96">
                <div class="flex-1">
                    {title_mid(color=color)}
                    <div class="mb-48"></div>
                    {paragraph(length=16, color=color)}
                </div>
                <div class="flex-1">
                    {image()}
                </div>
            </div>
        </div>
    '''

def template_content_image_ext(theme=''):
    bg_color = ''
    color = ''
    if theme == 'dark':
        bg_color = 'bg-dark'
        color = 'text-white'

    return f'''
        <div class="{bg_color} flex items-center">
            <div class="flex-1">
                <div class="container-half ml-auto pl-24 mr-96">
                    {title_mid(color=color)}
                    <div class="mb-48"></div>
                    {paragraph(length=16, color=color)}
                </div>
            </div>
            <div class="flex-1">
                {image(height=800)}
            </div>
        </div>
    '''

def template_image_content(bg_color='', color=''):
    return f'''
        <div class="{bg_color}">
            <div class="container-xl flex items-center gap-96">
                <div class="flex-1">
                    {image()}
                </div>
                <div class="flex-1">
                    {title_mid(color=color)}
                    <div class="mb-48"></div>
                    {paragraph(length=16, color=color)}
                </div>
            </div>
        </div>
    '''

def template_image_content_ext(theme=''):
    bg_color = ''
    color = ''
    if theme == 'dark':
        bg_color = 'bg-dark'
        color = 'text-white'
        
    return f'''
        <div class="{bg_color} flex items-center">
            <div class="flex-1">
                {image(height=800)}
            </div>
            <div class="flex-1">
                <div class="container-half mr-auto pl-24 ml-96">
                    {title_mid(color=color)}
                    <div class="mb-48"></div>
                    {paragraph(length=16, color=color)}
                </div>
            </div>
        </div>
    '''

def template_0004():
    html = f'''
        <section class="py-192">
            <div class="container-xl flex items-center gap-96 mb-48">
                <div class="flex-3">
                    {title_mid('Elimina Microrganismi Patogeni')}
                </div>
                <div class="flex-1">
                    {paragraph()}
                </div>
            </div>
            <div class="flex">
                <div class="flex-1 flex items-end image-bacteria h-600">
                    <div class="bg-dark w-75">
                        {paragraph(length=16, color='text-white')}
                    </div>
                </div>
                <div class="flex-1 flex items-end image-virus h-600">
                    <div class="bg-dark w-75">
                        {paragraph(length=16, color='text-white')}
                    </div>
                </div>
                <div class="flex-1 flex items-end image-mold h-600">
                    <div class="bg-dark w-75">
                        {paragraph(length=16, color='text-white')}
                    </div>
                </div>
            </div>
        </section>
    '''

    return html

def template_0005():
    image_height = 400
    html = f'''
        <section class="pt-96 pb-192">
            <div class="container-xl flex">
                <div class="flex-1 gap-24">
                    {title_mid('Applications')}
                    {paragraph()}
                </div>
                <div class="flex-1">
                </div>
            </div>
            <div class="flex">
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
            <div class="flex">
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




##################################################################
# LAYOUTS: IMAGES
##################################################################

def images_x2():
    return f'''
        <div class="container-xl flex items-center">
            <div class="flex-1">
                {image()}
            </div>
            <div class="flex-1">
                {image()}
            </div>
        </div>
    '''
    
def images_x2_ext():
    return f'''
        <div class="flex items-center">
            <div class="flex-1">
                {image()}
            </div>
            <div class="flex-1">
                {image()}
            </div>
        </div>
    '''
    
def images_x3():
    return f'''
        <div class="container-xl flex items-center">
            <div class="flex-1">
                {image()}
            </div>
            <div class="flex-1">
                {image()}
            </div>
            <div class="flex-1">
                {image()}
            </div>
        </div>
    '''
    
def images_x3_ext():
    return f'''
        <div class="flex items-center">
            <div class="flex-1">
                {image()}
            </div>
            <div class="flex-1">
                {image()}
            </div>
            <div class="flex-1">
                {image()}
            </div>
        </div>
    '''
    
def images_x4():
    return f'''
        <div class="container-xl flex items-center">
            <div class="flex-1">
                {image()}
            </div>
            <div class="flex-1">
                {image()}
            </div>
            <div class="flex-1">
                {image()}
            </div>
            <div class="flex-1">
                {image()}
            </div>
        </div>
    '''
    
def images_x4_ext():
    return f'''
        <div class="flex items-center">
            <div class="flex-1">
                {image()}
            </div>
            <div class="flex-1">
                {image()}
            </div>
            <div class="flex-1">
                {image()}
            </div>
            <div class="flex-1">
                {image()}
            </div>
        </div>
    '''
    
def images_x5():
    return f'''
        <div class="container-xl flex items-center">
            <div class="flex-1">
                {image()}
            </div>
            <div class="flex-1">
                {image()}
            </div>
            <div class="flex-1">
                {image()}
            </div>
            <div class="flex-1">
                {image()}
            </div>
            <div class="flex-1">
                {image()}
            </div>
        </div>
    '''
    
def images_x5_ext():
    return f'''
        <div class="flex items-center">
            <div class="flex-1">
                {image()}
            </div>
            <div class="flex-1">
                {image()}
            </div>
            <div class="flex-1">
                {image()}
            </div>
            <div class="flex-1">
                {image()}
            </div>
            <div class="flex-1">
                {image()}
            </div>
        </div>
    '''
    
def images_x6():
    return f'''
        <div class="container-xl flex items-center">
            <div class="flex-1">
                {image()}
            </div>
            <div class="flex-1">
                {image()}
            </div>
            <div class="flex-1">
                {image()}
            </div>
            <div class="flex-1">
                {image()}
            </div>
            <div class="flex-1">
                {image()}
            </div>
            <div class="flex-1">
                {image()}
            </div>
        </div>
    '''
    
def images_x6_ext():
    return f'''
        <div class="flex items-center">
            <div class="flex-1">
                {image()}
            </div>
            <div class="flex-1">
                {image()}
            </div>
            <div class="flex-1">
                {image()}
            </div>
            <div class="flex-1">
                {image()}
            </div>
            <div class="flex-1">
                {image()}
            </div>
            <div class="flex-1">
                {image()}
            </div>
        </div>
    '''


##################################################################
# FOOTERS
##################################################################

def footer_0000():
    html = f'''
        <section class="bg-black py-24">
            <div class="container-xl flex items-center justify-between">
                <div>
                    {paragraph('Ozonogroup', color='text-white')}
                </div>
                <div class="flex gap-24">
                    {paragraph('Privacy Policy', color='text-white')}
                    {paragraph('Terms of Service', color='text-white')}
                </div>
            </div>
        </section>
    '''

    return html

