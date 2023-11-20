import shutil
import os

shutil.copy2('servizi.html', 'public/servizi.html')
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