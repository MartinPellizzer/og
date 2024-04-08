import util
import os
import pathlib


def sitemap_all():
    sitemap = ''
    sitemap += '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += sitemap_pages()
    sitemap += sitemap_ozono()
    sitemap += '</urlset>\n'
    util.file_write('sitemap.xml', sitemap.strip())


def sitemap_ozono():
    lastmod_dummy = '2024-03-17'
    urls = ''

    path = pathlib.Path('public/ozono')
    filepaths = path.rglob("*.html")

    for filepath in filepaths: 
        filepath = str(filepath)
        filepath_in = filepath.replace('\\', '/')
        filepath_out = filepath_in.replace('public/', '').replace('.json', '.html')

        lastmod = lastmod_dummy
        urls += f'<url>\n'
        urls += f'  <loc>https://ozonogroup.it/{filepath_out}</loc>\n'
        urls += f'  <lastmod>{lastmod}</lastmod>\n'
        urls += f'</url>\n'

    return urls


def sitemap_pages():
    # HOME
    urls = ''
    urls += f'<url>\n'
    urls += f'  <loc>https://ozonogroup.it/</loc>\n'
    urls += f'  <lastmod>2024-03-17</lastmod>\n'
    urls += f'</url>\n'

    # PAGES
    pages_slugs = [
        'servizi',
        'settori',
        'missione',
        'contatti',
        'ozono',
    ]

    for page_slug in pages_slugs:
        urls += f'<url>\n'
        urls += f'  <loc>https://ozonogroup.it/{page_slug}.html</loc>\n'
        urls += f'  <lastmod>2024-03-17</lastmod>\n'
        urls += f'</url>\n'
  
    return urls


sitemap_all()
    
