import json
import os

for file in os.listdir('articles_tmp'):
    os.remove(f'articles_tmp/{file}')


with open("database/json/articles.json") as f:
    data = json.loads(f.read())
with open("database/json/pathogens.json") as f:
    data_pathogens = json.loads(f.read())

    
def lst_to_blt(lst):
    txt = ''
    for item in lst:
        txt += f'- {item}\n'
    return txt.strip()


output_text = ''

industry = data['industry']
industry_ad = data['industry_ad']
problems = data['problems']
products = data['products']

pathogen_effects = data_pathogens[0]['effects'][0]

output_text += f'## Prodotti\n\n'
output_text += f'Ecco alcuni prodotti dell\'industria {industry_ad}{industry} che traggono beneficio dall\'ozono.\n\n'
output_text += lst_to_blt(products)
output_text += f'\n\n'

pathogens_with_effects = []
for pathogen in problems:
    x = pathogen + ': ' + pathogen_effects
    pathogens_with_effects.append(x)

output_text += f'## Problemi\n\n'
output_text += f'Ecco alcuni microbi comuni nell\'industria {industry_ad}{industry} deboli contro l\'ozono.\n\n'
output_text += lst_to_blt(pathogens_with_effects)
output_text += f'\n\n'


print(output_text)

industry_formatted = industry.replace(' ', '-')
with open(f'articles_tmp/{industry_formatted}.md', 'a') as f:
    f.write(output_text)