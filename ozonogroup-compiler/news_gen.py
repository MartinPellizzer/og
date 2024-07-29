import shutil

import g

title = 'News Ozono | Ozonogroup'

header_html = f'''
    <section class="container-xl">
        <div class="flex justify-between gap-64">
            <div>
                <a href="/">Ozonogroup</a>
            </div>
            <nav class="flex gap-16">
                <a href="/">News</a>
                <a href="/">Servizi</a>
                <a href="/">Guide</a>
                <a href="/">Contatti</a>
            </nav>
        </div>
    </section>
'''

footer_html = f'''
    <section class="footer-section">
        <div class="container-xl h-full">
            <footer class="flex items-center justify-center">
                <span class="text-white">Ozonogroup s.r.l. | Tutti i diritti riservati</span>
            </footer>
        </div>
    </section>
'''

main_html = f'''
    <section class="container-xl py-96">
        <div class="grid grid-2 items-center">
            <img class="object-cover" height=500 src="/immagini/news-test.jpg">
            <div>
                <h2 class="text-48 mb-16">Oceani in pericolo: ozono per bonifica?
                </h2>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean molestie luctus massa sollicitudin eleifend. In hac habitasse platea dictumst. Curabitur luctus auctor auctor. Suspendisse ultricies tellus ac mollis mattis. Donec bibendum lobortis diam. Integer auctor eget ligula vitae vulputate. Etiam massa sapien, volutpat et ultricies sed, auctor et tellus. Phasellus molestie vitae nulla non eleifend. Sed ultrices massa quis ex congue elementum. Donec dignissim tempus commodo. 
                </p>
            </div>
        </div>
    </section>
'''

html = f'''
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="/style.css">
        <title>{title}</title>
        {g.GOOGLE_TAG}
    </head>

    <body>
        {header_html}

        {main_html}

        {footer_html}
    </body>
'''

with open('public/news.html', 'w') as f: f.write(html)

shutil.copy('style.css', 'public/style.css')
