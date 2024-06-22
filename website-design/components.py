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


def atom_paragraph_primary(text='', color='', length=32):
    if text == '':
        if length == 0: text = lorem.text()
        else: text = (' '.join(lorem.text().split(' ')[:length]) + '.').replace('..', '.')
    if color == '': color = 'text-dark'
    return f'<p class="text-18 {color}">{text}</h1>'


def atom_link_primary(text='', color=''):
    if text == '': text = 'Primary link >'
    if color == '': color = 'text-dark'
    return f'<a class="text-18 no-underline {color} font-bold inline-block" href="">{text}</a>'


def atom_button_primary(text='', color=''):
    if text == '': text = 'Primary button'
    if color == '': color = 'text-dark'
    return f'<a class="text-18 no-underline {color} rounded-full border-1 border-black border-solid px-16 py-4 inline-block" href="">{text}</a>'
    

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
    html += '<div class="mb-24"></div>'
    html += atom_button_primary(button)
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





#############################################################################
# POPULATIONS
# group of molecules: form a section on the page (multiple rows)
# ex: a section with 3 rows in a page describing the benefits of a product
#############################################################################

def population_tpl_i_x3_alt():
    html = f'''
        <section class="py-96">
            <div class="container-xl">
                {organism_tpl_i()}
                <div class="mb-96"></div>
                {organism_i_tpl()}
                <div class="mb-96"></div>
                {organism_tpl_i()}
            </div>
        </section>
    '''
    return html


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





#############################################################################
# ECOSYSTEMS
# group of molecules: form a page
# ex: homepage, about page, product page, etc...
#############################################################################





#############################################################################
# BIOSPHERE
# group of molecules: form a website
#############################################################################