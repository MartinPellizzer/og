import csv
import re
import random
import random

def csv_get_rows(table):
    rows = []
    with open(f"database/{table}.csv", "r", encoding='utf-8') as f:
        reader = csv.reader(f, delimiter="\\")
        for line in reader:
            rows.append(line)
    return rows


def fields_to_dict(row):
    fields = {}
    for i, cell in enumerate(row):
        fields[cell] = i
    return fields


def get_rows_by_field_value(rows, fields, field, value):
    filtered_rows = []
    for row in rows:
        if row[fields[field]] == value:
            filtered_rows.append(row)
    return filtered_rows

    
def get_product_types(rows, fields, field):
    product_types = []
    for row in rows:
        product_type = row[fields[field]]
        if product_type not in product_types:
            product_types.append(product_type)
    return product_types


def get_ad(rows, fields, field_subject, cell_val, field_ad):
    ad = ''
    for row in rows:
        cell_val_tmp = row[fields[field_subject]]
        if cell_val.strip().lower() == cell_val_tmp.strip().lower():
            ad = row[fields[field_ad]]
            break
    return ad.lower()


def list_to_text(lst):
    txt = ''
    if len(lst) == 0: txt = ''
    elif len(lst) == 1: txt = lst[0]
    elif len(lst) == 2: txt = ' e '.join(lst[:2])
    else: txt = ', '.join(lst[:2]) + f' e {lst[2]}'
    return txt


def format_line(line):
    line = line.replace('\n', '')
    line = re.sub(' +', ' ', line)
    line = line.replace(' ,', ',')
    line = line.replace(' .', '.')
    line = line.replace(' %', '%')
    line = line.strip()
    line = f'{line}\n\n'
    return line




industry = 'lavorazione carni'

experiments_rows = csv_get_rows('experiments')
experiments_fields = fields_to_dict(experiments_rows[0])
experiments_rows = experiments_rows[1:]

problems_rows = csv_get_rows('problems')
problems_fields = fields_to_dict(problems_rows[0])
problems_rows = problems_rows[1:]

products_rows = csv_get_rows('products')
products_fields = fields_to_dict(products_rows[0])
products_rows = products_rows[1:]

industries_rows = csv_get_rows('industries')
industries_fields = fields_to_dict(industries_rows[0])
industries_rows = industries_rows[1:]


industry_rows = get_rows_by_field_value(experiments_rows, experiments_fields, 'industry', industry)
product_types = get_product_types(industry_rows, experiments_fields, 'product_type')

applications_products = []
applications_products_type = []
applications_intro_problems = []
applications_problems_list = []
for product_type in product_types:
    experiments_rows_filtered = [row for row in industry_rows if row[experiments_fields['product_type']] == product_type]

    rows = experiments_rows_filtered
    fields = experiments_fields

    item_list = []
    study_done_list = []
    problem_list = []
    product_list = []
    for row in rows:
        study = row[fields['study']]
        study_year = row[fields['study_year']]
        product = row[fields['product']]
        treatment_type = row[fields['treatment_type']]
        ozone_type = row[fields['ozone_type']]
        problem = row[fields['problem']]
        pathogen_reduction_number = row[fields['pathogen_reduction_number']]
        pathogen_reduction_number_unit = row[fields['pathogen_reduction_number_unit']]
        pathogen_reduction_text = row[fields['pathogen_reduction_text']]
        o3_concentration = row[fields['o3_concentration']]
        o3_concentration_unit = row[fields['o3_concentration_unit']]
        treatment_time = row[fields['treatment_time']]
        treatment_time_unit = row[fields['treatment_time_unit']]

        if treatment_type.strip() != 'ozono': continue
        if not problem: continue

        if study not in study_done_list: study_done_list.append(study)
        else: continue

        if problem not in problem_list: problem_list.append(problem)
        problem_ad = get_ad(problems_rows, problems_fields, 'problem', problem, 'ad_3')
        problem_formatted = f'{problem_ad}{problem}'
        
        if product not in product_list: product_list.append(product)
        product_ad = get_ad(products_rows, products_fields, 'product', product, 'ad_2')
        product_formatted = f'{product_ad}{product}'
        
        if pathogen_reduction_number.strip() != '': pathogen_reduction_number = f'di {pathogen_reduction_number}'
        if pathogen_reduction_text.strip() != '': pathogen_reduction_text = f'in modo {pathogen_reduction_text}'
        pathogen_reduction_formatted = f'{pathogen_reduction_number} {pathogen_reduction_number_unit} {pathogen_reduction_text}'

        condition_list = []
        if ozone_type.strip() != '': condition_list.append(f'in forma {ozone_type}')
        if o3_concentration.strip() != '': condition_list.append(f'con una concentrazione di {o3_concentration} {o3_concentration_unit}')
        if treatment_time.strip() != '': condition_list.append(f'per un tempo di {treatment_time} {treatment_time_unit}')

        conditions_formatted = ''
        if len(condition_list) != 0:
            conditions_formatted = ', se usato ' + ' '.join(condition_list)

        line = f'''
            Riduce 
            {problem_formatted}
            {product_formatted}
            {pathogen_reduction_formatted}
            {conditions_formatted}
            ({study}, {study_year})
            .
        '''
        # ({study}, {study_year})

        line = line.replace('\n', '')
        line = re.sub(' +', ' ', line)
        line = line.replace(' ,', ',')
        line = line.replace(' .', '.')
        line = line.replace(' %', '%')
        line = line.strip()
        line = line[0].capitalize() + line[1:]
        line = f'- {line}\n'
        

        item_list.append(line)
        # print(line)
        # print()

    applications_products.append(product_list)
    applications_products_type.append(product_type)
    applications_intro_problems.append(problem_list)
    applications_problems_list.append(item_list)


qualities_products_type = []
qualities_products_intro = []
qualities_products_list = []
for product_type in product_types:
    rows = [row for row in industry_rows if row[experiments_fields['product_type']] == product_type]
    fields = experiments_fields

    item_list = []
    study_done_list = []
    quality_list = []
    product_list = []
    for row in rows:
        study = row[fields['study']]
        study_year = row[fields['study_year']]

        product = row[fields['product']]
        treatment_type = row[fields['treatment_type']]
        ozone_type = row[fields['ozone_type']]
        
        o3_concentration = row[fields['o3_concentration']]
        o3_concentration_unit = row[fields['o3_concentration_unit']]
        treatment_time = row[fields['treatment_time']]
        treatment_time_unit = row[fields['treatment_time_unit']]

        color = row[fields['color']]
        odor = row[fields['odor']]
        flavor = row[fields['flavor']]
        texture = row[fields['texture']]
        viscosity = row[fields['viscosity']]
        fats = row[fields['fats']]
        proteins = row[fields['proteins']]
        quality_effect_1 = row[fields['quality_effect_1']]
        quality_effect_2 = row[fields['quality_effect_2']]
        quality_effect_3 = row[fields['quality_effect_3']]
        quality_effect_4 = row[fields['quality_effect_4']]

        if study not in study_done_list: study_done_list.append(study)
        else: continue

        if treatment_type.strip() != 'ozono': continue

        template = 'non ha effetti collaterali '
        quality_list = []
        if color.strip() != '': 
            if color.strip() == 'NE': quality_list.append(f'{template} sul colore')
            else: quality_list.append(f'{color} il colore')
        if odor.strip() != '': 
            if odor.strip() == 'NE': quality_list.append(f'{template} sull\'odore')
            else: quality_list.append(f'{odor} l\'odore')
        if flavor.strip() != '': 
            if flavor.strip() == 'NE': quality_list.append(f'{template} sul gusto')
            else: quality_list.append(f'{flavor} il gusto')
        if texture.strip() != '': 
            if texture.strip() == 'NE': quality_list.append(f'{template} sulla consistenza')
            else: quality_list.append(f'{texture} la consistenza')
        if viscosity.strip() != '': 
            if viscosity.strip() == 'NE': quality_list.append(f'{template} sulla viscosità')
            else: quality_list.append(f'{viscosity} la viscosità')
        if fats.strip() != '': 
            if fats.strip() == 'NE': quality_list.append(f'{template} sui grassi')
            else: quality_list.append(f'{fats} i grassi')
        if proteins.strip() != '': quality_list.append(proteins)
        if quality_effect_1.strip() != '': quality_list.append(quality_effect_1)
        if quality_effect_2.strip() != '': quality_list.append(quality_effect_2)
        if quality_effect_3.strip() != '': quality_list.append(quality_effect_3)
        if quality_effect_4.strip() != '': quality_list.append(quality_effect_4)

        if not quality_list: continue

        if len(quality_list) == 0: quality_formatted = 'non causa variazioni nella qualità'
        elif len(quality_list) == 1: quality_formatted = quality_list[0]
        else: quality_formatted = ', '.join(quality_list[:-1]) + f' e {quality_list[-1]}'
        
        if product not in product_list: product_list.append(product)
        product_ad = get_ad(products_rows, products_fields, 'product', product, 'ad_4')
        product_formatted = f'{product_ad}{product}'

        condition_list = []
        if ozone_type.strip() != '': condition_list.append(f'in forma {ozone_type}')
        if o3_concentration.strip() != '': condition_list.append(f'con una concentrazione di {o3_concentration} {o3_concentration_unit}')
        if treatment_time.strip() != '': condition_list.append(f'per un tempo di {treatment_time} {treatment_time_unit}')

        conditions_formatted = ''
        if len(condition_list) != 0:
            conditions_formatted = ', se usato ' + ' '.join(condition_list)

        line = f'''
            {quality_formatted}
            {product_formatted}
            {conditions_formatted}
            ({study}, {study_year})
            .
        '''
        print(line)

        # ({study}, {study_year})

        line = line.replace('\n', '')
        line = re.sub(' +', ' ', line)
        line = line.replace(' ,', ',')
        line = line.replace(' .', '.')
        line = line.replace(' %', '%')
        line = line.strip()
        line = line[0].capitalize() + line[1:]
        line = f'- {line}\n'

        item_list.append(line)
        # print(line)
        # print()

    qualities_products_type.append(product_type)
    qualities_products_intro.append(quality_list)
    qualities_products_list.append(item_list)



# print(qualities_products_intro)
# quit()


text_to_write = ''

industry_ad = get_ad(industries_rows, industries_fields, 'industry', industry, 'ad_4')
text_to_write += f'# Sanificazione ad ozono nell\'industria {industry_ad}{industry}\n\n'

problem_with_ad_list = []
for problem in problem_list:
    problem_ad = get_ad(problems_rows, problems_fields, 'problem', problem, 'ad_3')
    problem_with_ad_list.append(f'{problem_ad}{problem}')
problem_formatted = list_to_text(problem_with_ad_list)

line = f'L\'ozono (O3) è un gas che viene usato nell\'indutria {industry} per ridurre problemi come {problem_formatted}.'
line = format_line(line)
text_to_write += line

industry_ad = get_ad(industries_rows, industries_fields, 'industry', industry, 'ad_4')

line = f'In questo articolo vediamo quali sono le applicazioni dell\'ozono nell\'industria {industry} e quali sono gli effetti di questo gas sulla qualità dei prodotti di questa industria.\n\n'
line = format_line(line)
text_to_write += line

format_line(line)





industry_ad = get_ad(industries_rows, industries_fields, 'industry', industry, 'ad_4')

line = f'## L\'ozono quali applicazioni ha nell\'industria {industry_ad}{industry}?\n\n'
text_to_write += line

problem_list = []
for sublist in applications_intro_problems:
    for item in sublist:
        problem_list.append(item)


problem_with_ad_list = []
for problem in problem_list:
    problem_ad = get_ad(problems_rows, problems_fields, 'problem', problem, 'ad_3')
    problem_with_ad_list.append(f'{problem_ad}{problem}')
problem_formatted = list_to_text(problem_with_ad_list)
industry_ad = get_ad(industries_rows, industries_fields, 'industry', industry, 'ad_4')

line = f'L\'ozono riduce {problem_formatted} dai prodotti dell\'industria {industry_ad}{industry}, se usato a giuste concentazioni e per il giusto tempo.\n\n'
text_to_write += line


product_type_with_ad_list = []
for product_type in applications_products_type:
    product_type_ad = get_ad(products_rows, products_fields, 'product_type', product_type, 'pt_ad_2')
    product_type_with_ad_list.append(f'{product_type_ad}{product_type}')
product_formatted = list_to_text(product_type_with_ad_list)

line = f'Ecco una lista di applicazioni dell\'ozono {product_formatted}.\n\n'
line = format_line(line)
text_to_write += line


for i, lines in enumerate(applications_problems_list):
    product_type = applications_products_type[i]
    text_to_write += f'### {product_type.capitalize()}\n\n'

    # product_list = []
    # for sublist in applications_products:
    #     for item in sublist:
    #         product_list.append(item)

    # PRODUCT --------------------------------------------------------------------------

    # PRODUCT INTRO
    product_list = applications_products[i]
    product_with_ad_list = [] 
    for product in product_list:
        product_ad = get_ad(products_rows, products_fields, 'product', product, 'ad_3')
        product_with_ad_list.append(f'{product_ad}{product}')
    product_formatted = list_to_text(product_with_ad_list)

    problem_list = applications_intro_problems[i]
    problem_with_ad_list = [] 
    for problem in problem_list:
        problem_ad = get_ad(problems_rows, problems_fields, 'problem', problem, 'ad_3')
        problem_with_ad_list.append(f'{problem_ad}{problem}')
    problem_formatted = list_to_text(problem_with_ad_list)

    line = f'L\'ozono viene usato per trattare {product_formatted}, eliminando problemi come {problem_formatted}.\n\n'
    line = format_line(line)
    text_to_write += line
    # TODO: {study_formatted}\n\n'

    # PRODUCT LIST INTO
    product_type_ad = get_ad(products_rows, products_fields, 'product_type', product_type, 'pt_ad_2')
    
    line = f'Ecco elencati alcuni problemi che l\'ozono risolve {product_type_ad}{product_type}.\n\n'
    line = format_line(line)
    text_to_write += line

    # PRODUCT LIST
    for line in lines:
        text_to_write += line
    text_to_write += '\n'







industry_ad = get_ad(industries_rows, industries_fields, 'industry', industry, 'ad_4')

line = f'## L\'ozono quali proprietà sensoriali altera nei prodotti dell\'industria {industry_ad}{industry}?\n\n'
text_to_write += line


line = f'L\'ozono può avere effetti collaterali sulle proprietà sensoriali dei prodotti dell\'industria {industry}, se usato a concentrazioni eccessive e per un tempo prolungato.\n\n'
line = format_line(line)
text_to_write += line


product_type_with_ad_list = []
for i, product_type in enumerate(qualities_products_type):
    quality_list = qualities_products_intro[i]
    if not quality_list: continue
    product_type_ad = get_ad(products_rows, products_fields, 'product_type', product_type, 'pt_ad_2')
    product_type_with_ad_list.append(f'{product_type_ad}{product_type}')
product_formatted = list_to_text(product_type_with_ad_list)


line = f'Ecco una lista di effetti dell\'ozono sulle proprietà sensoriali {product_formatted}.\n\n'
line = format_line(line)
text_to_write += line


for i, lines in enumerate(qualities_products_list):
    quality_list = qualities_products_intro[i]

    if not quality_list: continue

    product_type = applications_products_type[i]

    text_to_write += f'### {product_type.capitalize()}\n\n'

    product_list = applications_products[i]
    product_with_ad_list = [] 
    for product in product_list:
        product_ad = get_ad(products_rows, products_fields, 'product', product, 'ad_3')
        product_with_ad_list.append(f'{product_ad}{product}')
    product_formatted = list_to_text(product_with_ad_list)

    quality_formatted = list_to_text(quality_list)

    # text_to_write += f'L\'ozono viene usato per trattare {product_formatted}, eliminando problemi come {problem_formatted}.\n\n'

    product_type_ad = get_ad(products_rows, products_fields, 'product_type', product_type, 'pt_ad_4')
    
    line = f'L\'ozono {quality_formatted} {product_type_ad}{product_type}. \n\n'
    line = format_line(line)
    text_to_write += line


    product_type_ad = get_ad(products_rows, products_fields, 'product_type', product_type, 'pt_ad_4')
    
    line = f'Ecco elencati alcuni effetti dell\'ozono sulla qualità {product_type_ad}{product_type}.\n\n'
    line = format_line(line)
    text_to_write += line



    for line in lines:
        text_to_write += line
    text_to_write += '\n'

with open('test.md', 'w', encoding='utf-8') as f:
    f.write(text_to_write)