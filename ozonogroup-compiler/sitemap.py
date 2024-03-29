import util
import os
import pathlib


desktop = pathlib.Path("Desktop")
desktop.rglob("*")

def sitemap_all():
    sitemap = ''
    sitemap += '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += sitemap_main()
    sitemap += sitemap_sectors()
    sitemap += '</urlset>\n'
    util.file_write('sitemap.xml', sitemap.strip())




def sitemap_sectors():
    lastmod_dummy = '2024-03-17'
    urls = ''

    path = pathlib.Path('public/ozono/sanificazione/settori')
    filepaths = path.rglob("*.html")

    for filepath in filepaths: 
        filepath = str(filepath)
        filepath_in = filepath.replace('\\', '/')
        filepath_out = filepath_in.replace('public/', '').replace('.json', '.html')

        lastmod = lastmod_dummy
        urls += f'<url>\n'
        urls += f'  <loc>https://ozonogroup.com/{filepath_out}</loc>\n'
        urls += f'  <lastmod>{lastmod}</lastmod>\n'
        urls += f'</url>\n'

    return urls





def sitemap_main():
    urls = ''
    urls += f'''
<url>
  <loc>https://ozonogroup.it/</loc>
  <lastmod>2024-03-17</lastmod>
</url>
'''.strip() + '\n'
    urls += f'''
<url>
  <loc>https://ozonogroup.it/servizi.html</loc>
  <lastmod>2024-03-17</lastmod>
</url>
'''.strip() + '\n'
    urls += f'''
<url>
  <loc>https://ozonogroup.it/settori/tea.html</loc>
  <lastmod>2024-03-17</lastmod>
</url>
'''.strip() + '\n'
    urls += f'''
<url>
  <loc>https://ozonogroup.it/missione.html</loc>
  <lastmod>2024-03-17</lastmod>
</url>
'''.strip() + '\n'
    urls += f'''
<url>
  <loc>https://ozonogroup.it/contatti.html</loc>
  <lastmod>2024-03-17</lastmod>
</url>
'''.strip() + '\n'
    urls += f'''
<url>
  <loc>https://ozonogroup.it/ozono.html</loc>
  <lastmod>2024-03-17</lastmod>
</url>
'''.strip() + '\n'

    return urls



    
