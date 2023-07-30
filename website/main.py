import shutil
# shutil.copy2('/style.css', '/')

import markdown
import pathlib
import os

folder = pathlib.Path("articles")

for filepath in folder.rglob("*.md"):

    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    content_html = markdown.markdown(content, extensions=['markdown.extensions.tables'])

    # content_html_formatted = []
    # for line in content_html.split('\n'):
    #     if 'NOTA:' in line:
    #         line = line.replace('<p>', '<p class="nota">').replace('NOTA: ', '')
    #     content_html_formatted.append(line)

    # content_html = '\n'.join(content_html_formatted)

    
    with open('components/header.html', encoding='utf-8') as f:
        header_html = f.read()

    html = f'''
        <!DOCTYPE html>
        <html lang="en">

        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="/style-blog.css">
            <title>Ozonogroup</title>
        </head>

        <body>
            <section class="header-section">
                <div class="container-xl h-full">
                    {header_html}
                </div>
            </section>

            <section class="container-md">
                {content_html}
            </section>

            <section class="footer-section">
                <div class="container-xl h-full">
                    <footer class="flex items-center justify-center">
                        <span class="text-white">Ozonogroup s.r.l. | Tutti i diritti riservati</span>
                    </footer>
                </div>
            </section>
        </body>

        </html>
    '''

    filepath_chunks = str(filepath).split('\\')
    print(filepath_chunks)
    filepath_out_dir = '/'.join(filepath_chunks[1:-1])
    filepath_out = '/'.join(filepath_chunks[1:]).replace('.md', '.html')

    if not os.path.exists(filepath_out_dir):
        os.makedirs(filepath_out_dir)

    with open(filepath_out, 'w', encoding='utf-8') as f:
        f.write(html)

    shutil.copy2('index.html', 'public/index.html')
    shutil.copy2('style.css', 'public/style.css')
    shutil.copy2('style-blog.css', 'public/style-blog.css')
    shutil.copy2('util.css', 'public/util.css')
    shutil.copy2('img.css', 'public/img.css')
    shutil.copy2('logo.ico', 'public/logo.ico')
    shutil.copy2('CNAME', 'public/CNAME')
