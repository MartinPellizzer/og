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

    filepath_chunks = str(filepath).split('\\')



    # GENERATE BREADCRUMBS ----------------------------------------------

    breadcrumbs = [f.replace('.md', '').title() for f in filepath_chunks[2:-1]]
    
    breadcrumbs_hrefs = []
    total_path = ''
    for b in breadcrumbs:
        total_path += b + '/'
        breadcrumbs_hrefs.append('/' + total_path[:-1].lower() + '.html')
    
    breadcrumbs_text = total_path.split('/')

    breadcrumbs_html = []
    for i in range(len(breadcrumbs_hrefs)):
        html = f'<a href="{breadcrumbs_hrefs[i]}">{breadcrumbs_text[i]}</a>'
        breadcrumbs_html.append(html)

    breadcrumbs_html_formatted = [f' > {f}' for f in breadcrumbs_html]



    # GENERATE TABLE OF CONTENTS ----------------------------------------

    table_of_contents_html = ''

    
    content_html_with_ids = ''
    current_id = 0
    for line in content_html.split('\n'):
        if '<h2>' in line:
            content_html_with_ids += (line.replace('<h2>', f'<h2 id="{current_id}">'))
            current_id +=1
        elif '<h3>' in line:
            content_html_with_ids += (line.replace('<h3>', f'<h3 id="{current_id}">'))
            current_id +=1
        elif '<h4>' in line:
            content_html_with_ids += (line.replace('<h4>', f'<h4 id="{current_id}">'))
            current_id +=1
        elif '<h5>' in line:
            content_html_with_ids += (line.replace('<h5>', f'<h5 id="{current_id}">'))
            current_id +=1
        elif '<h6>' in line:
            content_html_with_ids += (line.replace('<h6>', f'<h6 id="{current_id}">'))
            current_id +=1
        else:
            content_html_with_ids += (line)
        content_html_with_ids += '\n'


    headers = []
    for line in content_html.split('\n'):
        if '<h2>' in line:
            headers.append(line)
        elif '<h3>' in line:
            headers.append(line)
        elif '<h4>' in line:
            headers.append(line)
        elif '<h5>' in line:
            headers.append(line)
        elif '<h6>' in line:
            headers.append(line)

    # for x in headers:
    #     print(x)

    table_of_contents_html += '<div class="toc">'
    table_of_contents_html += '<span class="toc-title">Table of Contents</span>'
    table_of_contents_html += '<ul>'

    toc_li = []
    
    last_header = '<h2>'
    for i, line in enumerate(headers):
        insert_open_ul = False
        insert_close_ul = False

        if '<h2>' in line: 
            if last_header != '<h2>': 
                if int('<h2>'[2]) > int(last_header[2]): insert_open_ul = True
                else: insert_close_ul = True
            last_header = '<h2>'
            line = line.replace('<h2>', '').replace('</h2>', '')

        elif '<h3>' in line:
            if last_header != '<h3>':
                if int('<h3>'[2]) > int(last_header[2]): insert_open_ul = True
                else: insert_close_ul = True

            last_header = '<h3>'
            line = line.replace('<h3>', '').replace('</h3>', '')

        if insert_open_ul: table_of_contents_html += f'<ul>'
        if insert_close_ul: table_of_contents_html += f'</ul>'
        table_of_contents_html += f'<li><a href="#{i}">{line}</a></li>'

    table_of_contents_html += '</ul>'
    table_of_contents_html += '</div>'

    # for line in table_of_contents_html:
    # print(table_of_contents_html)
        
    print()

    content_html_formatted = ''

    toc_inserted = False
    for line in content_html_with_ids.split('\n'):
        if not toc_inserted:
            if '<h2' in line:
                print(line)
                toc_inserted = True
                content_html_formatted += table_of_contents_html
                content_html_formatted += line
                continue
        content_html_formatted += line

        # print(line)

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

            <section class="breadcrumbs-section">
                <div class="container-xl h-full">
                    <a href="/index.html">Home</a>{''.join(breadcrumbs_html_formatted)}
                </div>
            </section>

            <section class="container-md">
                {content_html_formatted}
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

    # COPY IMAGES -----------------------------------------------------

    for f in os.listdir('assets/images/'):
        shutil.copy2(f'assets/images/{f}', f'public/assets/images/{f}')

