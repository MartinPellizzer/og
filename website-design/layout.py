import random
import requests

import lorem

import util


#############################################################################
# UTILS
#############################################################################

def unsplash_random():
    image_url = ''

    with open('C:/api-keys/unsplash-api-key.txt', 'r') as f:
        ACCESS_KEY = f.read().strip()

    url = f'https://api.unsplash.com/photos/random?client_id={ACCESS_KEY}'
    response = requests.get(url)
    print(response)

    filepath = 'unsplash/random/urls.txt'
    try: 
        data = response.json()
        image_url = data['urls']['regular']

        util.file_append(filepath, f'{image_url}\n')
    except:
        image_url = random.choice(util.file_read(filepath).split('\n')[:-1])


    return image_url



#############################################################################
# COMPONENTS
#############################################################################

def block_title(title, size, color, mb=0):
    return f'<h1 class="{size} {color} mb-{mb}">{title}</h1>'
    

def block_sentence():
    s = lorem.sentence()
    return f'<p>{s}</p>'


# def block_paragraph():
#     p = lorem.paragraph()
#     return f'<p>{p}</p>'


def block_lorem(length, size, color, mb=0):
    if length == 0: t = lorem.text()
    else: t = (' '.join(lorem.text().split(' ')[:length]) + '.').replace('..', '.')
    return f'<p class="{size} {color} mb-{mb}">{t}</p>'


def block_text(text, color, mb=0):
    return f'<p class="text-18 {color} mb-{mb}">{text}</p>'


def block_paragraph(text, size, weight, color, mb):
    return f'<p class="{size} {weight} {color} {mb}">{text}</p>'

    
def block_link(color):
    return f'<a class="text-16 no-underline {color} font-bold" href="">Action link ></a>'


def block_image(height):
    filepath = f'unsplash/nature.txt'
    content = util.file_read(filepath)
    urls = content.strip().split('\n')
    url = random.choice(urls)
    return f'<img class="object-cover" src="{url}" alt="" height={height}>'


def block_image_random(height):
    url = unsplash_random()
    return f'<img class="object-cover" src="{url}" alt="" height={height}>'


def block_list_unordered(color):
    return f'''
        <ul class="ml-24">
            <li class="text-18 {color}">{lorem.sentence()}</li>
            <li class="text-18 {color}">{lorem.sentence()}</li>
            <li class="text-18 {color}">{lorem.sentence()}</li>
            <li class="text-18 {color}">{lorem.sentence()}</li>
        </ul>
    '''


def block_icon(width, mb):
    return f'''
        <svg class="{width} {mb}" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4.26 10.147a60.438 60.438 0 0 0-.491 6.347A48.62 48.62 0 0 1 12 20.904a48.62 48.62 0 0 1 8.232-4.41 60.46 60.46 0 0 0-.491-6.347m-15.482 0a50.636 50.636 0 0 0-2.658-.813A59.906 59.906 0 0 1 12 3.493a59.903 59.903 0 0 1 10.399 5.84c-.896.248-1.783.52-2.658.814m-15.482 0A50.717 50.717 0 0 1 12 13.489a50.702 50.702 0 0 1 7.74-3.342M6.75 15a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm0 0v-3.675A55.378 55.378 0 0 1 12 8.443m-7.007 11.55A5.981 5.981 0 0 0 6.75 15.75v-1.5" />
        </svg>
    '''



#############################################################################
# LAYOUTS
#############################################################################



def hero_0001(theme=''):
    color = ''
    if theme == '':
        color = 'text-neutral-900'

    h1 = block_title('Medium length display headline', size='text-64', color=color, mb=24)
    p = block_lorem(24, size='text-18', color=color, mb=48)
    img = block_image_random(480)
    link = block_link(color)
    
    html = f'''
        <section class="py-96">
            <div class="container-xl flex items-center gap-96">
                <div class="flex-1">
                    {h1}
                    {p}
                    {link}
                </div>
                <div class="flex-1">
                    {img}
                </div>
            </div>
        </section>
    '''

    return html


def cta_0001(theme=''):
    background_color = ''
    color = ''
    if theme == '':
        background_color = ''
        color = 'text-neutral-900'
    elif theme == 'holy':
        background_color = 'bg-neutral-100'
        color = 'text-neutral-900'
    elif theme == 'dark':
        background_color = 'bg-neutral-900'
        color = 'text-neutral-100'

    p = block_text('Tagline', color, mb=24)
    h1 = block_title('Long headline to turn your visitors into users', size='text-64', color=color, mb=24)
    link = block_link(color)
    
    html = f'''
        <section class="py-96 {background_color}">
            <div class="container-md text-center">
                {p}
                {h1}
                {link}
            </div>
        </section>
    '''

    return html

    
def content_0001(theme='', swap=True):
    background_color = ''
    color = ''
    if theme == '':
        background_color = ''
        color = 'text-neutral-900'
    elif theme == 'holy':
        background_color = 'bg-neutral-100'
        color = 'text-neutral-900'
    elif theme == 'dark':
        background_color = 'bg-neutral-900'
        color = 'text-neutral-100'

    if swap: swap='flex-row-reverse'
    else: swap = ''

    title = block_title('Medium length headline', size='text-24', color=color, mb=24)
    paragraph = block_lorem(32, size='text-18', color=color, mb=24)
    list_unordered = block_list_unordered(color=color)
    img = block_image_random(480)
    
    html = f'''
        <section class="py-96 {background_color}">
            <div class="container-xl flex items-center gap-96 {swap}">
                <div class="flex-1"> 
                    {title}
                    {paragraph}
                    {list_unordered}
                </div>
                <div class="flex-1">
                    {img}
                </div>
            </div>
        </section>
    '''

    return html
    

def content_0002(theme='', swap=True):
    background_color = ''
    color = ''

    if theme == '':
        background_color = ''
        color = 'text-neutral-900'
    elif theme == 'holy':
        background_color = 'bg-neutral-100'
        color = 'text-neutral-900'
    elif theme == 'dark':
        background_color = 'bg-neutral-900'
        color = 'text-neutral-100'

    if swap: swap='flex-row-reverse'
    else: swap = ''

    title = block_title('Medium length headline', size='text-24', color=color, mb=24)
    paragraph = block_lorem(32, size='text-18', color=color, mb=24)
    img = block_image_random(480)

    big_number_1 = block_paragraph('32', size='text-64', weight='font-normal', color=color, mb='mb-0')
    big_number_desc_1 = block_paragraph('GB', size='text-18', weight='font-bold', color=color, mb='mb-0')
    paragraph_small_1 = block_lorem(6, size='text-18', color=color, mb=0)

    big_number_2 = block_paragraph('2.6', size='text-64', weight='font-normal', color=color, mb='mb-0')
    big_number_desc_2 = block_paragraph('Milion', size='text-18', weight='font-bold', color=color, mb='mb-0')
    paragraph_small_2 = block_lorem(6, size='text-18', color=color, mb=0)
    
    html = f'''
        <section class="py-96 {background_color}">
            <div class="container-xl flex items-center gap-96 {swap}">
                <div class="flex-1"> 
                    {title}
                    {paragraph}
                    <div class="flex gap-64">
                        <div class="flex-1">
                            <div class="flex items-baseline gap-8">
                                {big_number_1}
                                {big_number_desc_1}
                            </div>
                            {paragraph_small_1}
                        </div>
                        <div class="flex-1">
                            <div class="flex items-baseline gap-8">
                                {big_number_2}
                                {big_number_desc_2}
                            </div>
                            {paragraph_small_2}
                        </div>
                    </div>
                </div>
                <div class="flex-1">
                    {img}
                </div>
            </div>
        </section>
    '''

    return html


def content_0003(theme='', swap=True):
    background_color = ''
    color = ''

    if theme == '':
        background_color = ''
        color = 'text-neutral-900'
    elif theme == 'holy':
        background_color = 'bg-neutral-100'
        color = 'text-neutral-900'
    elif theme == 'dark':
        background_color = 'bg-neutral-900'
        color = 'text-neutral-100'

    if swap: swap='flex-row-reverse'
    else: swap = ''

    title = block_title('Medium length headline', size='text-24', color=color, mb=24)
    paragraph = block_lorem(64, size='text-18', color=color, mb=24)
    img = block_image_random(480)
    icon = block_icon(width='w-48', mb='mb-16')

    html = f'''
        <section class="py-96 {background_color}">
            <div class="container-xl flex items-center gap-96 {swap}">
                <div class="flex-1"> 
                    
                    {title}
                    {paragraph}
                </div>
                <div class="flex-1">
                    {img}
                </div>
            </div>
        </section>
    '''

    return html




functions = [content_0001, content_0002, content_0003]