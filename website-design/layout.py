import requests

import lorem

import util


#############################################################################
# UTILS
#############################################################################

def unsplash_random():
    with open('C:/api-keys/unsplash-api-key.txt', 'r') as f:
        ACCESS_KEY = f.read().strip()

    url = f'https://api.unsplash.com/photos/random?client_id={ACCESS_KEY}'
    response = requests.get(url)

    data = response.json()
    image_url = data['urls']['regular']

    filepath = 'unsplash/random/picture.jpg'
    util.file_append(filepath, f'{image_url}\n')

    return image_url



#############################################################################
# COMPONENTS
#############################################################################

def block_title(title, mb=0):
    return f'<h1 class="text-64 text-neutral-900 mb-{mb}">{title}</h1>'
    

def block_sentence():
    s = lorem.sentence()
    return f'<p>{s}</p>'


def block_paragraph():
    p = lorem.paragraph()
    return f'<p>{p}</p>'


def block_text(length=0, mb=0):
    if length == 0: t = lorem.text()
    else: t = (' '.join(lorem.text().split(' ')[:length]) + '.').replace('..', '.')
    return f'<p class="text-18 text-neutral-900 mb-{mb}">{t}</p>'

    
def block_link():
    return f'<a class="no-underline text-neutral-900 font-bold" href="">Action link ></a>'


def block_image(height):
    filepath = f'unsplash/nature.txt'
    content = util.file_read(filepath)
    urls = content.strip().split('\n')
    url = random.choice(urls)
    return f'<img class="object-cover" src="{url}" alt="" height={height}>'


def block_image_random(height):
    url = unsplash_random()
    return f'<img class="object-cover" src="{url}" alt="" height={height}>'



#############################################################################
# LAYOUTS
#############################################################################

def hero_0001():
    h1 = block_title('Medium length display headline', mb=24)
    p = block_text(24, mb=48)
    img = block_image_random(480)
    link = block_link()
    
    html = f'''
        <section class="py-96">
            <div class="container-lg flex items-center gap-96">
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