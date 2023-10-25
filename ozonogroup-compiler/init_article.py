import os
import sys

if len(sys.argv) != 3:
    print('ERR: wrong arguments (ENTITY, ATTRIBUTE)')
    print('> init_articles.py lattiero-casearia applicazioni')
    quit()

entity = sys.argv[1].strip().lower().replace(' ', '-')
attribute = sys.argv[2].strip().lower().replace(' ', '-')

print(entity)
print(attribute)

try: os.mkdir(f'database/tables/{entity}')
except: pass

if attribute == 'applicazioni':
    try: os.mkdir(f'database/tables/{entity}/acque-reflue')
    except: pass
    with open(f'database/tables/{entity}/acque-reflue/acque-reflue.csv', 'a', encoding='utf-8') as f: pass

    try: os.mkdir(f'database/tables/{entity}/attrezzature')
    except: pass
    with open(f'database/tables/{entity}/attrezzature/attrezzature.csv', 'a', encoding='utf-8') as f: pass

    try: os.mkdir(f'database/tables/{entity}/aria-ambienti')
    except: pass
    with open(f'database/tables/{entity}/aria-ambienti/aria-ambienti.csv', 'a', encoding='utf-8') as f: pass

    try: os.mkdir(f'articles-images/public/ozono/sanificazione/{entity}')
    except: pass
    try: os.mkdir(f'articles-images/public/ozono/sanificazione/{entity}/{attribute}')
    except: pass