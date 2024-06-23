import random
import requests

import lorem

import g
import util




def block_lorem(length, size, color, align, mb):
    if length == 0: t = lorem.text()
    else: t = (' '.join(lorem.text().split(' ')[:length]) + '.').replace('..', '.')
    return f'<p class="{size} {color} {align} {mb}">{t}</p>'





#############################################################################
# ATOMS
# single elements: title, paragraph, link, image, etc...
#############################################################################



# TITLES
# ----------------------

def atom_title_primary(text='', color=''):
    if text == '': text = 'Primary title'
    if color == '': color = 'text-dark'
    return f'<h1 class="text-64 {color}">{text}</h1>'
    

def atom_title_secondary(text='', color=''):
    if text == '': text = 'Secondary title'
    if color == '': color = 'text-dark'
    return f'<h1 class="text-48 {color}">{text}</h1>'
    

def atom_title_tertiary(text='', color=''):
    if text == '': text = 'Tertiary title'
    if color == '': color = 'text-dark'
    return f'<h1 class="text-24 {color}">{text}</h1>'



# PARAGRAPHS
# ----------------------

def atom_paragraph_primary(text='', color='', length=32):
    if text == '':
        if length == 0: text = lorem.text()
        else: text = (' '.join(lorem.text().split(' ')[:length]) + '.').replace('..', '.')
    if color == '': color = 'text-dark'
    return f'<p class="text-18 {color}">{text}</h1>'



# LINKS
# ----------------------

def atom_link_primary(text='', color=''):
    if text == '': text = 'Primary link >'
    if color == '': color = 'text-dark'
    return f'<a class="text-18 no-underline {color} font-bold inline-block" href="">{text}</a>'


def atom_link_secondary(text='', color=''):
    if text == '': text = 'Primary link >'
    if color == '': color = 'text-dark'
    return f'<a class="text-14 no-underline {color} font-regular inline-block" href="">{text.upper()}</a>'



# BUTTONS
# ----------------------
def atom_button_primary(text='', color=''):
    if text == '': text = 'Primary button'
    if color == '': color = 'text-dark'
    return f'<a class="text-18 no-underline {color} rounded-full border-1 border-black border-solid px-16 py-4 inline-block" href="">{text}</a>'
    


# IMAGES
# ----------------------
def atom_image(src='', height=480):
    filepath = 'unsplash/random/urls.txt'
    if src == '': src = random.choice(util.file_read(filepath).split('\n')[:-1])
    return f'<img class="object-cover object-center" src="{src}" alt="" height={height}>'
    




#############################################################################
# MOLECULES
# group of atoms: form a block
# ex: title with a paragraph and a call to action
#############################################################################

def molecule_title_paragraph_link():
    html = ''
    html += atom_title_primary()
    html += '<div class="mb-24"></div>'
    html += atom_paragraph_primary()
    html += '<div class="mb-24"></div>'
    html += atom_link_primary()
    return html
    
    
def molecule_paragraph_link():
    html = ''
    html += atom_paragraph_primary()
    html += '<div class="mb-24"></div>'
    html += atom_link_primary()
    return html
    

def molecule_title_paragraph_button():
    html = ''
    html += atom_title_primary()
    html += '<div class="mb-24"></div>'
    html += atom_paragraph_primary()
    html += '<div class="mb-24"></div>'
    html += atom_button_primary()
    return html


def molecule_paragraph_button(paragraph, button):
    html = ''
    html += atom_paragraph_primary(paragraph)
    html += '<div class="mb-16"></div>'
    html += atom_button_primary(button)
    return html


def molecule_menu_horizontal(links):
    html = ''
    html += ''.join([atom_link_secondary(text=link) for link in links])
    return html


def molecule_t3p(title='', paragraph=''):
    html = ''
    html += atom_title_tertiary(title)
    html += '<div class="mb-24"></div>'
    html += atom_paragraph_primary(paragraph)
    return html
    

def molecule_ts_p(atom_0=None, atom_1=None):
    if not atom_0: atom_0 = atom_title_secondary()
    if not atom_1: atom_1 = atom_paragraph_primary()

    html = f'''
        {atom_0}
        <div class="mb-24"></div>
        {atom_1}
    '''

    return html

    


#############################################################################
# ORGANISMS
# group of molecules: form a row
# ex: title with a description on the left and an image on the right
#############################################################################

def organism_tpl_i():
    html = f'''
        <div class="flex items-center gap-96">
            <div class="flex-1">
                {molecule_title_paragraph_link()}
            </div>
            <div class="flex-1">
                {atom_image()}
            </div>
        </div>
    '''
    return html

    
def organism_i_tpl():
    html = f'''
        <div class="flex items-center gap-96">
            <div class="flex-1">
                {atom_image()}
            </div>
            <div class="flex-1">
                {molecule_title_paragraph_link()}
            </div>
        </div>
    '''
    return html

    
def organism_header(logo='', links=''):
    _logo = atom_link_secondary(text=logo)
    _menu = molecule_menu_horizontal(links=links)

    html = f'''
        <header class="py-24">
            <div class="container-xl flex items-center justify-between">
                <div class="">
                    {_logo}
                </div>
                <div class="flex gap-16">
                    {_menu}
                </div>
            </div>
        </header>
    '''

    return html


def organism_tspx3(molecule_0=None, molecule_1=None, molecule_2=None):
    if not molecule_0: molecule_0 = molecule_ts_p()
    if not molecule_1: molecule_1 = molecule_ts_p()
    if not molecule_2: molecule_2 = molecule_ts_p()

    html = f'''
        <div class="container-xl flex gap-96">
            <div class="flex-1">
                {molecule_0}
            </div>
            <div class="flex-1">
                {molecule_1}
            </div>
            <div class="flex-1">
                {molecule_2}
            </div>
        </div>
    '''

    return html


def organism_tsp(molecule_0=None):
    if not molecule_0: molecule_0 = atom_title_secondary()

    html = f'''
        <div class="container-md">
            {molecule_0}
        </div>
    '''

    return html
    


#############################################################################
# POPULATIONS
# group of organisma: form a section on the page (multiple rows)
# ex: a section with 3 rows in a page describing the benefits of a product
#############################################################################


def population_t_pb_i(title='', paragraph='', button='', image=''):
    _title = atom_title_primary(title)
    _paragraph_button = molecule_paragraph_button(paragraph, button)
    _image = atom_image(image)

    html = f'''
        <section class="py-96">
            <div class="container-xl flex gap-96 mb-48">
                <div class="flex-3">
                    {_title}
                </div>
                <div class="flex-1">
                    {_paragraph_button}
                </div>
            </div>
            <div>
                {_image}
            </div>
        </section>
    '''
    return html



def population_tps_tpsx3(organism_0=None, organism_1=None):
    if not organism_0: organism_0 = organism_tps()
    if not organism_1: organism_1 = organism_tspx3()
    
    html = f'''
        <section class="py-96">
            {organism_0}
            <div class="mb-48"></div>
            {organism_1}
        </section>
    '''
    return html




#############################################################################
# ECOSYSTEMS
# group of populations: form a page
# ex: homepage, about page, product page, etc...
#############################################################################





#############################################################################
# BIOSPHERE
# group of ecosystems: form a website
#############################################################################