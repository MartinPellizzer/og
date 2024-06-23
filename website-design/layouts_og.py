import random
import lorem

#########################################################################
# ELEMENTS
#########################################################################

def title_big(text=None):
    if not text: text = 'Medium length engaging title'
    html = f'<h1 class="text-64 mb-24">{text}</h1>'
    return html

def title_mid(text=None, color='text-black'):
    if not text: text = 'Medium length engaging title'
    html = f'<h1 class="text-48 mb-24 {color}">{text}</h1>'
    return html

    
def paragraph(length=16, color='text-black'):
    text = (' '.join(lorem.text().split(' ')[:length]) + '.').replace('..', '.')
    return f'<p class="text-18 mb-24 {color}">{text}</p>'


def link_secondary(text=None):
    if not text: text = 'Action link'
    return f'<a class="text-16 no-underline font-normal text-black uppercase" href="">{text}</a>'


def image(src=None, height=600):
    if not src:
        filepath = f'unsplash/random/urls.txt'
        with open(filepath) as f:
            content = f.read()
        urls = content.strip().split('\n')
        src = random.choice(urls)
    return f'<img class="object-cover object-center" src="{src}" alt="" height={height}>'


#########################################################################
# LAYOUTS
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


def template_0000():
    html = f'''
        <div class="container-xl flex items-center gap-96">
            <div class="flex-3">
                {title_big('Sanificazione Ozono Veloce, Sicura, Ecologica')}
            </div>
            <div class="flex-1">
                {paragraph()}
            </div>
        </div>
    '''

    return html

    
def template_0001():
    html = f'''
        <div class="bg-dark">
            {image(src='assets/hero-03.png', height=600)}
        </div>
    '''

    return html


def template_0002():
    html = f'''
        <div class="bg-dark">
            <div class="container-xl flex items-center gap-96">
                <div class="flex-1">
                    {title_mid(text='Our Work', color='text-white')}
                    <div class="mb-48"></div>
                    {paragraph(length=16, color='text-white')}
                </div>
                <div class="flex-1">
                    {image()}
                </div>
            </div>
        </div>
    '''

    return html


def template_0003():
    html = f'''
        <div class="bg-dark flex items-center gap-96">
            <div class="flex-1">
                <div class="container-half ml-auto pl-24">
                    {title_mid(text='Our Work', color='text-white')}
                    <div class="mb-48"></div>
                    {paragraph(length=16, color='text-white')}
                </div>
            </div>
            <div class="flex-1">
                {image()}
            </div>
        </div>
    '''

    return html


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
                <div class="flex-1">
                    {image(src='images/bacteria-03.jpeg')}
                </div>
                <div class="flex-1">
                    {image(src='images/virus-03.jpeg')}
                </div>
                <div class="flex-1">
                    {image(src='images/mold-04.jpeg')}
                </div>
            </div>
        </section>
    '''

    return html


templates = [
    template_0000,
    template_0001,
    template_0002,
    template_0003,
    template_0004,
]