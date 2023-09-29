import json
import os
import random
import re

for file in os.listdir('articles_tmp'):
    os.remove(f'articles_tmp/{file}')


with open("database/json/articles.json", encoding='utf-8') as f:
    data = json.loads(f.read())
with open("database/json/pathogens.json", encoding='utf-8') as f:
    data_pathogens = json.loads(f.read())

    
def lst_to_blt(lst):
    txt = ''
    for item in lst:
        txt += f'- {item}\n'
    return txt.strip()


def lst_to_txt(lst):
    txt = ''
    if len(lst) == 0: txt = ''
    elif len(lst) == 1: txt = lst[0]
    elif len(lst) == 2: txt = f'{lst[0]} e {lst[1]}'
    else: txt = f'{", ".join(lst[:-1])} e {lst[-1]}'
    return txt


output_text = ''

industry = data['industry']
industry_ad = data['industry_ad']
pathogens = data['pathogens']
products = data['products']

pathogen_effects = data_pathogens[0]['effects'][0]

output_text += f'## Prodotti\n\n'
output_text += f'Ecco alcuni prodotti dell\'industria {industry_ad}{industry} che traggono beneficio dall\'ozono.\n\n'
output_text += lst_to_blt(products)
output_text += f'\n\n'



pathogens_with_effects = []
for pathogen in pathogens:
    found_effects = False
    for p in data_pathogens:
        if p['name'] in pathogen:
            p_effects_lst = p['effects']
            if len(p_effects_lst) != 0: found_effects = True
            else: break

            p_name_ad = p['name_ad_1'].capitalize()
            p_name_quantity = p['name_quantity']
            p_type = p['type']

            if p_name_quantity == 'singolare': 
                p_name_quantity_1 = 'è'
                p_name_quantity_2 = 'un'
                p_name_quantity_3 = 'causa'
            else: 
                p_name_quantity_1 = 'sono'
                p_name_quantity_2 = 'dei'
                if p_type == 'batterio': p_type = 'batteri'
                p_name_quantity_3 = 'causano'

            random.shuffle(p_effects_lst)
            p_effects_txt = lst_to_txt(p_effects_lst[:3]).lower()

            if p_type: p_type = f'{p_name_quantity_1} {p_name_quantity_2} {p_type} che'

            pathogen_with_effects = f'**{pathogen}:** {p_name_ad}{pathogen} {p_type} {p_name_quantity_3} problemi di salute come {p_effects_txt}'
            pathogen_with_effects = re.sub(' +', ' ', pathogen_with_effects)
            break
    if found_effects:
        pathogens_with_effects.append(pathogen_with_effects)
    else:
        pathogens_with_effects.append(f'{pathogen}: no data')

pathogens_llt = lst_to_txt(pathogens)

output_text += f'## Quali patogeni l\'ozono elimina nell\'industria {industry_ad}{industry}?\n\n'
output_text += f'L\'ozono elimina patogeni come {pathogens_llt} nell\'industria {industry_ad}{industry}.\n\n'
output_text += f'Ecco una descrizione più dettagliata di questi patogeni e dei problemi che causano sulla salute umana.\n\n'
output_text += lst_to_blt(pathogens_with_effects)
output_text += f'\n\n'


# print(output_text)

industry_formatted = industry.replace(' ', '-')
with open(f'articles/public/ozono/sanificazione/industria/{industry_formatted}.md', 'w', encoding='utf-8') as f:
    f.write(output_text)