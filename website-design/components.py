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
    return f'<a class="text-18 no-underline {color} rounded-full border-1 border-black border-solid px-16 py-8 inline-block" href="">{text}</a>'
    
def atom_image(src='', height=480):
    filepath = 'unsplash/random/urls.txt'
    if src == '': src = random.choice(util.file_read(filepath).split('\n')[:-1])
    return f'<img class="object-cover object-center" src="{src}" alt="" height={height}>'
    
