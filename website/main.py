# import shutil
# shutil.copy2('/style.css', '/')

import markdown
import pathlib
import os

folder = pathlib.Path("articles")

for filepath in folder.rglob("*.md"):

    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    content_html = markdown.markdown(content)

    html = f'''
        <!DOCTYPE html>
        <html lang="en">

        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="/style.css">
            <title>Ozonogroup</title>
        </head>

        <body>
            <header>
                <a href="/index.html">Logo</a>
                <nav>
                    <a href="/ozono/index.html">Ozono Doc</a>
                    <a href="/prodotti.html">Prodotti</a>
                    <a href="/contatti.html">Contatti</a>
                </nav>
            </header>

            <section class="container-md">
                {content_html}
            </section>
        </body>

        </html>
    '''

    filepath_chunks = str(filepath).split('\\')
    filepath_out_dir = '/'.join(filepath_chunks[1:-1])
    filepath_out = '/'.join(filepath_chunks[1:]).replace('.md', '.html')

    if not os.path.exists(filepath_out_dir):
        os.makedirs(filepath_out_dir)

    with open(filepath_out, 'w', encoding='utf-8') as f:
        f.write(html)