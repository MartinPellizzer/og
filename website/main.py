with open('salespage.md', 'r', encoding='"UTF-8"') as f:
    content = f.readlines()

def get_html():
    lines = content
    html = ''
    for line in lines:
        if '\n' == line:
            pass
        elif '###' in line:
            text = line.replace('###', '')
            html += f'<h3 class="mt-md">{text}</h3>'
        elif '##' in line:
            text = line.replace('##', '')
            html += f'<h2 class="mt-xl">{text}</h2>'
        elif '#' in line:
            text = line.replace('#', '')
            html += f'<h1>{text}</h1>'
        else:
            html += f'<p>{line}</p>'
    return html

with open('salespage.html', 'w', encoding='"UTF-8"') as f:
    html = get_html()
    f.write(f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="./css/style-sp.css">
            <title>Document</title>
        </head>
        <body>
            <div class="container-md">
                {html}
            </div>
        </body>
        </html>
    ''')
            