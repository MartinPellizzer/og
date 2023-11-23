import shutil
import os

with open('home.html', 'r') as f: content = f.read()
with open('components/header.html', 'r') as f: header = f.read()
content = content.replace('<!-- insert header here -->', header)
with open('index.html', 'w') as f: content = f.write(content)

with open('servizi_edit.html', 'r') as f: content = f.read()
with open('components/header.html', 'r') as f: header = f.read()
content = content.replace('<!-- insert header here -->', header)
with open('servizi.html', 'w') as f: content = f.write(content)

with open('missione_edit.html', 'r') as f: content = f.read()
with open('components/header.html', 'r') as f: header = f.read()
content = content.replace('<!-- insert header here -->', header)
with open('missione.html', 'w') as f: content = f.write(content)

with open('contatti_edit.html', 'r') as f: content = f.read()
with open('components/header.html', 'r') as f: header = f.read()
content = content.replace('<!-- insert header here -->', header)
with open('contatti.html', 'w') as f: content = f.write(content)

with open('guide_edit.html', 'r') as f: content = f.read()
with open('components/header.html', 'r') as f: header = f.read()
content = content.replace('<!-- insert header here -->', header)
with open('guide.html', 'w') as f: content = f.write(content)

shutil.copy2('index.html', 'public/index.html')
shutil.copy2('servizi.html', 'public/servizi.html')
shutil.copy2('guide.html', 'public/guide.html')
shutil.copy2('missione.html', 'public/missione.html')
shutil.copy2('contatti.html', 'public/contatti.html')

shutil.copy2('style.css', 'public/style.css')
shutil.copy2('style-blog.css', 'public/style-blog.css')
shutil.copy2('util.css', 'public/util.css')
shutil.copy2('img.css', 'public/img.css')

for f in os.listdir('assets/images/static'):
    shutil.copy2(f'assets/images/static/{f}', f'public/assets/images/{f}')

shutil.copy2('logo.ico', 'public/logo.ico')
shutil.copy2('CNAME', 'public/CNAME')