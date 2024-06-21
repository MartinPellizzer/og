import random
import requests

import lorem

import g
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
        print(image_url)


    return image_url


def color_scheme(theme):
    background_color = ''
    color = ''
    if theme == 'holy':
        background_color = 'bg-holy'
        color = 'text-dark'
    elif theme == 'dark':
        background_color = 'bg-dark'
        color = 'text-holy'

    return color, background_color




def block_title(title, size, color, mb):
    return f'<h1 class="{size} {color} {mb}">{title}</h1>'
    

def block_sentence():
    s = lorem.sentence()
    return f'<p>{s}</p>'


# def block_paragraph():
#     p = lorem.paragraph()
#     return f'<p>{p}</p>'


def block_lorem(length, size, color, align, mb):
    if length == 0: t = lorem.text()
    else: t = (' '.join(lorem.text().split(' ')[:length]) + '.').replace('..', '.')
    return f'<p class="{size} {color} {align} {mb}">{t}</p>'


def block_text(text, size, color, mb):
    return f'<p class="{size} {color} {mb}">{text}</p>'


def block_paragraph(text, size, weight, color, mb):
    return f'<p class="{size} {weight} {color} {mb}">{text}</p>'

    
def block_link(text, size, weight, color, transform):
    return f'<a class="{size} no-underline {color} {weight} {transform}" href="">{text}</a>'


def block_image(height):
    filepath = f'unsplash/nature.txt'
    content = util.file_read(filepath)
    urls = content.strip().split('\n')
    url = random.choice(urls)
    return f'<img class="object-cover" src="{url}" alt="" height={height}>'


def block_image_random(height, mb):
    url = unsplash_random()
    return f'<img class="object-cover {mb}" src="{url}" alt="" height={height}>'


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
# COMPONENTS
#############################################################################

def title_primary(text, align, color):
    return f'<h1 class="text-64 {align} {color} mb-24">{text}</h1>'


def title_secondary(text, align, color):
    return f'<h2 class="text-48 {align} {color} mb-24">{text}</h2>'


def title_tertiary(text, align, color):
    return f'<h3 class="text-24 {align} {color} mb-24">{text}</h3>'


def link_primary(text, color):
    return block_link(text, 'text-16', 'font-bold', color, transform='')


def link_secondary(text, color):
    return block_link(text, 'text-14', 'font-normal', color, transform='uppercase')




#############################################################################
# LAYOUTS
#############################################################################


def menu_0001(theme, swap=True):
    color, background_color = color_scheme(theme)

    if swap: swap='flex-row-reverse'
    else: swap = ''

    logo = link_secondary('Ozonogroup', color)
    link_1 = link_secondary('Ozono', color)
    link_2 = link_secondary('Proditti', color)
    link_3 = link_secondary('Servizi', color)
    link_4 = link_secondary('Contatti', color)

    html = f'''
        <section class="py-24 {background_color}">
            <div class="container-xl flex justify-between items-center gap-96 {swap}">
                {logo}
                <nav class="flex gap-16">
                    {link_1}
                    {link_2}
                    {link_3}
                    {link_4}
                </nav>
            </div>
        </section>
    '''

    return html


def hero_0001(theme, swap=True):
    color, background_color = color_scheme(theme)

    if swap: swap='flex-row-reverse'
    else: swap = ''

    title = random.choice(util.file_read(f'content/homepage/hero-title.txt').split('\n')[:-1]).strip()
    desc = util.file_read(f'content/homepage/hero-desc.txt').strip()

    title = title_primary(title, align='', color=color)
    p = block_text(desc, g.PARAGRAPH_SIZE, color, mb='mb-48')
    img = block_image_random(480, mb='mb-0')
    link = link_primary('Action Link >', color)
    
    html = f'''
        <section class="py-96 {background_color}">
            <div class="container-xl flex items-center gap-96 {swap}">
                <div class="flex-1">
                    {title}
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


def cta_0001(theme):
    color, background_color = color_scheme(theme)

    p = block_text('Tagline', g.PARAGRAPH_SIZE, color, 'mb-24')
    title = title_primary('Long headline to turn your visitors into users', align='', color=color)
    link = link_primary('Action Link >', color)
    
    html = f'''
        <section class="py-96 {background_color}">
            <div class="container-md text-center">
                {p}
                {title}
                {link}
            </div>
        </section>
    '''

    return html


def content_0001(theme, swap=True):
    color, background_color = color_scheme(theme)

    if swap: swap='flex-row-reverse'
    else: swap = ''

    title = title_tertiary('Medium length headline', align='', color=color)
    paragraph = block_lorem(32, size='text-18', color=color, align='', mb='mb-24')
    list_unordered = block_list_unordered(color=color)
    img = block_image_random(480, mb='mb-0')
    
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
    

def content_0002(theme, swap=True):
    color, background_color = color_scheme(theme)

    if swap: swap='flex-row-reverse'
    else: swap = ''

    title = title_tertiary('Medium length headline', align='', color=color)
    paragraph = block_lorem(32, size='text-18', color=color, align='', mb='mb-24')
    img = block_image_random(480, mb='mb-0')

    big_number_1 = block_paragraph('32', size='text-64', weight='font-normal', color=color, mb='mb-0')
    big_number_desc_1 = block_paragraph('GB', size='text-18', weight='font-bold', color=color, mb='mb-0')
    paragraph_small_1 = block_lorem(6, size='text-18', color=color, align='', mb='mb-24')

    big_number_2 = block_paragraph('2.6', size='text-64', weight='font-normal', color=color, mb='mb-0')
    big_number_desc_2 = block_paragraph('Milion', size='text-18', weight='font-bold', color=color, mb='mb-0')
    paragraph_small_2 = block_lorem(6, size='text-18', color=color, align='', mb='mb-24')
    
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


def content_0003(theme, swap=True):
    color, background_color = color_scheme(theme)

    if swap: swap='flex-row-reverse'
    else: swap = ''

    title = title_tertiary('Medium length headline', align='', color=color)
    paragraph = block_lorem(64, size='text-18', color=color, align='', mb='mb-24')
    img = block_image_random(480, mb='mb-0')
    icon = block_icon(width='w-48', mb='mb-16')

    html = f'''
        <section class="py-96 {background_color}">
            <div class="container-xl flex items-center gap-96 {swap}">
                <div class="flex-1"> 
                    {icon}
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


def features_0001(theme='holy', swap=False):
    color, background_color = color_scheme(theme)

    if swap: swap='flex-row-reverse'
    else: swap = ''

    title_1 = title_tertiary('Feature One', align='text-center', color=color)
    title_2 = title_tertiary('Feature ', align='text-center', color=color)
    desc_1 = block_lorem(24, size='text-18', color=color, align='text-center', mb='mb-24')
    desc_2 = block_lorem(24, size='text-18', color=color, align='text-center', mb='mb-24')
    img = block_image_random(480, mb='mb-0')

    icons = util.file_read('assets/icons/hero.txt').split('\n')[:-1]
    icon_1 = icons[0].replace('<svg', '<svg class="w-48 mb-16"')
    icon_2 = icons[1].replace('<svg', '<svg class="w-48 mb-16"')

    html = f'''
        <section class="py-96 {background_color}">
            <div class="container-xl flex items-center gap-96 {swap}">
                <div class="flex-1 text-center"> 
                    {icon_1}
                    {title_1}
                    {desc_1}
                </div>
                <div class="flex-1 text-center">
                    {icon_2}
                    {title_2}
                    {desc_2}
                </div>
            </div>
        </section>
    '''

    return html


def features_0008(theme='holy', swap=False):
    color, background_color = color_scheme(theme)

    img_h = 240
    desc_word_num = 16

    img_1 = block_image_random(img_h, mb='mb-24')
    title_1 = title_tertiary('Medium length headline', align='text-left', color=color)
    desc_1 = block_lorem(desc_word_num, size='text-18', color=color, align='text-left', mb='mb-24')
    link_1 = link_primary('Action Link >', color)

    img_2 = block_image_random(img_h, mb='mb-24')
    title_2 = title_tertiary('Medium length headline', align='text-left', color=color)
    desc_2 = block_lorem(desc_word_num, size='text-18', color=color, align='text-left', mb='mb-24')
    link_2 = link_primary('Action Link >', color)

    img_3= block_image_random(img_h, mb='mb-24')
    title_3 = title_tertiary('Medium length headline', align='text-left', color=color)
    desc_3 = block_lorem(desc_word_num, size='text-18', color=color, align='text-left', mb='mb-24')
    link_3 = link_primary('Action Link >', color)
    

    html = f'''
        <section class="py-96 {background_color}">
            <div class="container-xl flex items-center gap-96 {swap}">
                <div class="flex-1"> 
                    {img_1}
                    {title_1}
                    {desc_1}
                    {link_1}
                </div>
                <div class="flex-1"> 
                    {img_2}
                    {title_2}
                    {desc_2}
                    {link_2}
                </div>
                <div class="flex-1"> 
                    {img_3}
                    {title_3}
                    {desc_3}
                    {link_3}
                </div>
            </div>
        </section>
    '''

    return html


def footer_0001(theme='holy', swap=False):
    color, background_color = color_scheme(theme)

    copy = block_text('&#169 Ozonogroup s.r.l. 2024 | Tutti i diritti riservati', size='text-18', color=color, mb='mb-0')
    privacy_policy = block_text('Privacy Policy', size='text-18', color=color, mb='mb-0')
    terms_of_service = block_text('Terms of Service', size='text-18', color=color, mb='mb-0')
    

    html = f'''
        <section class="py-24 {background_color}">
            <div class="container-xl flex items-center justify-between {swap}">
                {copy}
                <div class="flex gap-24"> 
                    {privacy_policy}
                    {terms_of_service}
                </div>
            </div>
        </section>
    '''

    return html




def hero_extra_0001(title='', desc='', cta='', img='', theme='holy', swap=False):
    color, background_color = color_scheme(theme)

    title = 'Sanificazione <span class="text-blue-700">Ozono</span>.<br>Veloce, Naturale, Sicura.'
    desc = 'Elimina batteri, virus, muffe e altri patogeni da ambienti e prodotti in modo rapido ed ecologico.'
    cta = 'Richiedi Prova Gratuita'

    _title = title_primary(title, align='align-left', color=color)
    _desc = block_text(desc, size='text-18', color=color, mb='mb-24')
    _cta = link_primary(cta, color=color)
    _img = f'<img class="object-cover object-bottom" src="/assets/hero-03.png" alt="" height="600">'

    html = f'''
        <section class="py-96 {background_color}">
            <div class="container-xl flex items-center gap-96 pb-96 {swap}">
                <div class="flex-3"> 
                    {_title}
                </div>
                <div class="flex-1"> 
                    {_desc}
                    {_cta}
                </div>
            </div>
            {_img}
        </section>
    '''

    return html

contents = [content_0001, content_0002, content_0003]
features = [features_0001, features_0008]