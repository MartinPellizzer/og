import csv
import re
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



def generate_product_intro_application(rows):
    
    application_list = []
    study_list = []
    for experiments_quality_row in rows:
        # GET VALUES FOR ROW
        treatment_type = experiments_quality_row[experiments_application_fields['treatment_type']]

        problem = experiments_quality_row[experiments_application_fields['problem']]

        pathogen_reduction_number = experiments_quality_row[experiments_application_fields['pathogen_reduction_number']]
        pathogen_reduction_number_unit = experiments_quality_row[experiments_application_fields['pathogen_reduction_number_unit']]
        pathogen_reduction_text = experiments_quality_row[experiments_application_fields['pathogen_reduction_text']]

        o3_concentration = experiments_quality_row[experiments_application_fields['o3_concentration']]
        o3_concentration_unit = experiments_quality_row[experiments_application_fields['o3_concentration_unit']]
        treatment_time = experiments_quality_row[experiments_application_fields['treatment_time']]
        treatment_time_unit = experiments_quality_row[experiments_application_fields['treatment_time_unit']]

        if treatment_type.strip() != 'ozono':
            continue

            
        tmp_list = []
        if problem.strip() != '': tmp_list.append(problem)
        application_list.append(tmp_list)

        study = experiments_quality_row[experiments_quality_fields['study']]
        study_year = experiments_quality_row[experiments_quality_fields['study_year']]

        study_list.append(f'{study} del {study_year}')

    print(application_list)

    application_list_filtered = []
    for x in application_list:
        if x:
            random.shuffle(x)
            application_list_filtered.append(x[0])
    random.shuffle(application_list_filtered)
    
    print(application_list_filtered)
    # quit()

    application_list_filtered = list(dict.fromkeys(application_list_filtered))
    if len(application_list_filtered) == 0: application_formatted = 'non causa variazioni nella qualità'
    elif len(application_list_filtered) == 1: application_formatted = application_list_filtered[0]
    elif len(application_list_filtered) == 2: application_formatted = ' e '.join(application_list_filtered[:2])
    else: application_formatted = ', '.join(application_list_filtered[:2]) + f' e {application_list_filtered[2]}'
    
    print(application_formatted)
    # quit()

    study_list = list(dict.fromkeys(study_list))
    if len(study_list) != 0: study_formatted = 'Questo è dimostrato da vari studi, come '
    if len(study_list) == 0: study_formatted = ''
    elif len(study_list) == 1: study_formatted += study_list[0]
    else: study_formatted += ' e '.join(study_list[:2])
    if len(study_list) != 0: study_formatted +=  '.'

    product = experiments_quality_row[experiments_quality_fields['product_type']]
    product_ad = ''
    for product_row in products_rows:
        product_tmp = product_row[products_fields['product_type']]
        if product_tmp.strip().lower() == product.strip().lower():
            product_ad = product_row[products_fields['product_ad_3']]
            break
    product_formatted = f'{product_ad}{product}'

    line = f'L\'ozono viene usato per trattare {product_formatted}, eliminando problemi come {application_formatted}. {study_formatted}\n\n'
    print(line)

    line = line.replace('\n', '')
    line = re.sub(' +', ' ', line)
    line = line.replace(' ,', ',')
    line = line.replace(' .', '.')
    line = line.strip()
    line = line[0].capitalize() + line[1:]

    return f'{line}\n\n'


def generate_product_list_intro_application(product_type):
    product = product_type
    product_ad = ''
    for product_row in products_rows:
        product_tmp = product_row[products_fields['product_type']]
        if product_tmp.strip().lower() == product.strip().lower():
            product_ad = product_row[products_fields['product_ad_2']]
            break
    product_formatted = f'{product_ad}{product}'

    line = f'Ecco una lista di alcune applicazioni dell\'ozono {product_formatted}.\n\n'
    print(line)
    return line


def generate_product_list_application(rows):
    lines = []
    study_done_list = []

    for experiments_quality_row in rows:

        # GET VALUES FOR ROW
        study = experiments_quality_row[experiments_application_fields['study']]
        study_year = experiments_quality_row[experiments_application_fields['study_year']]

        product = experiments_quality_row[experiments_application_fields['product']]
        treatment_type = experiments_quality_row[experiments_application_fields['treatment_type']]
        
        problem = experiments_quality_row[experiments_application_fields['problem']]

        pathogen_reduction_number = experiments_quality_row[experiments_application_fields['pathogen_reduction_number']]
        pathogen_reduction_number_unit = experiments_quality_row[experiments_application_fields['pathogen_reduction_number_unit']]
        pathogen_reduction_text = experiments_quality_row[experiments_application_fields['pathogen_reduction_text']]

        o3_concentration = experiments_quality_row[experiments_application_fields['o3_concentration']]
        o3_concentration_unit = experiments_quality_row[experiments_application_fields['o3_concentration_unit']]
        treatment_time = experiments_quality_row[experiments_application_fields['treatment_time']]
        treatment_time_unit = experiments_quality_row[experiments_application_fields['treatment_time_unit']]

        if study not in study_done_list: study_done_list.append(study)
        else: continue

        if treatment_type.strip() != 'ozono':
            continue

        # PRODUCT
        product_ad_4 = ''
        for product_row in products_rows:
            product_tmp = product_row[products_fields['product']]
            if product_tmp.strip().lower() == product.strip().lower():
                product_ad_4 = product_row[products_fields['product_ad_4']]
                break

        product_formatted = f'{product_ad_4}{product}'

        # CONDITIONS
        condition_list = []
        if treatment_type.strip() != '': condition_list.append(f'in forma {treatment_type}')
        if o3_concentration.strip() != '': condition_list.append(f'con una concentrazione di {o3_concentration} {o3_concentration_unit}')
        if treatment_time.strip() != '': condition_list.append(f'per un tempo di {treatment_time} {treatment_time_unit}')

        conditions_formatted = ''
        if len(condition_list) != 0:
            conditions_formatted = ', se usato ' + ' '.join(condition_list)

        # continue

        pathogen_reduction_formatted = f'{pathogen_reduction_number} {pathogen_reduction_number_unit} {pathogen_reduction_text}'

        # FILL TEMPLATE
        line = f'''
            Riduce il livello di 
            {problem}
            {pathogen_reduction_formatted}
            {conditions_formatted}
            ({study}, {study_year})
            .
        '''

        # FORMAT LINE
        line = line.replace('\n', '')
        line = re.sub(' +', ' ', line)
        line = line.replace(' ,', ',')
        line = line.replace(' .', '.')
        line = line.replace(' %', '%')
        line = line.strip()
        line = line[0].capitalize() + line[1:]
        
        print(f'- {line}\n')
        print()
        lines.append(f'- {line}\n')

    return_text = ''
    for line in lines:
        return_text += line

    return f'{return_text}\n'
    





def generate_intro_quality(rows):
    industry = rows[0][experiments_quality_fields['industry']]

    quality_list = []
    for experiments_quality_row in rows:
        odor = experiments_quality_row[experiments_quality_fields['odor']]
        color = experiments_quality_row[experiments_quality_fields['color']]
        flavor = experiments_quality_row[experiments_quality_fields['flavor']]
        texture = experiments_quality_row[experiments_quality_fields['texture']]
        viscosity = experiments_quality_row[experiments_quality_fields['viscosity']]
        fats = experiments_quality_row[experiments_quality_fields['fats']]
        proteins = experiments_quality_row[experiments_quality_fields['proteins']]
        quality_effect_1 = experiments_quality_row[experiments_quality_fields['quality_effect_1']]
        quality_effect_2 = experiments_quality_row[experiments_quality_fields['quality_effect_2']]
        quality_effect_3 = experiments_quality_row[experiments_quality_fields['quality_effect_3']]
        quality_effect_4 = experiments_quality_row[experiments_quality_fields['quality_effect_4']]
        
        if odor.strip() != '': quality_list.append(odor)
        if color.strip() != '': quality_list.append(color)
        if flavor.strip() != '': quality_list.append(flavor)
        if texture.strip() != '': quality_list.append(texture)
        if viscosity.strip() != '': quality_list.append(viscosity)
        if fats.strip() != '': quality_list.append(fats)
        if proteins.strip() != '': quality_list.append(proteins)
        if quality_effect_1.strip() != '': quality_list.append(quality_effect_1)
        if quality_effect_2.strip() != '': quality_list.append(quality_effect_2)
        if quality_effect_3.strip() != '': quality_list.append(quality_effect_3)
        if quality_effect_4.strip() != '': quality_list.append(quality_effect_4)

    random.shuffle(quality_list)

    quality_list = list(dict.fromkeys(quality_list))

    for quality in quality_list:
        print(quality)

    if len(quality_list) == 0: quality_formatted = 'non causa variazioni nella qualità'
    elif len(quality_list) == 1: quality_formatted = quality_list[0]
    elif len(quality_list) == 2: quality_formatted = ' e '.join(quality_list[:2])
    else: quality_formatted = ', '.join(quality_list[:2]) + f' e {quality_list[2]}'

    product_types = []
    for row in rows:
        product_type = row[experiments_quality_fields['product_type']]
        if product_type not in product_types:
            product_types.append(product_type)
    
    line = ''
    line += f'L\'ozono {quality_formatted} dei prodotti dell\'industria {industry}, se usato a concentrazioni eccessive e per un tempo prolungato.\n\n'
    

    line = line.replace('\n', '')
    line = re.sub(' +', ' ', line)
    line = line.replace(' ,', ',')
    line = line.replace(' .', '.')
    line = line.strip()
    line = line[0].capitalize() + line[1:]

    return f'{line}\n\n'

    
def generate_intro_list_quality(product_types):
    products_formatted_list = []
    for product_type in product_types:
        product_ad = ''
        for product_row in products_rows:
            product_type_tmp = product_row[products_fields['product_type']]
            if product_type_tmp.strip().lower() == product_type.strip().lower():
                product_ad = product_row[products_fields['product_ad_4']]
                break
        product_formatted = f'{product_ad}{product_type}'
        products_formatted_list.append(product_formatted)

    if len(products_formatted_list) == 0: products_formatted = ''
    elif len(products_formatted_list) == 1: products_formatted = products_formatted_list[0]
    elif len(products_formatted_list) == 2: products_formatted = ' e '.join(products_formatted_list[:2])
    else: products_formatted = ', '.join(products_formatted_list[:-1]) + f' e {products_formatted_list[-1]}'

    line = ''
    line += f'Ecco una lista di effetti dell\'ozono sulle proprietà sensoriali {products_formatted}.\n\n'
    print(line)
    return line


def generate_product_intro_quality(rows):
    quality_list = []
    study_list = []
    for experiments_quality_row in rows:
        odor = experiments_quality_row[experiments_quality_fields['odor']]
        color = experiments_quality_row[experiments_quality_fields['color']]
        flavor = experiments_quality_row[experiments_quality_fields['flavor']]
        texture = experiments_quality_row[experiments_quality_fields['texture']]
        viscosity = experiments_quality_row[experiments_quality_fields['viscosity']]
        fats = experiments_quality_row[experiments_quality_fields['fats']]
        proteins = experiments_quality_row[experiments_quality_fields['proteins']]
        quality_effect_1 = experiments_quality_row[experiments_quality_fields['quality_effect_1']]
        quality_effect_2 = experiments_quality_row[experiments_quality_fields['quality_effect_2']]
        quality_effect_3 = experiments_quality_row[experiments_quality_fields['quality_effect_3']]
        quality_effect_4 = experiments_quality_row[experiments_quality_fields['quality_effect_4']]
        
        tmp_list = []
        if odor.strip() != '': tmp_list.append(odor)
        if color.strip() != '': tmp_list.append(color)
        if flavor.strip() != '': tmp_list.append(flavor)
        if texture.strip() != '': tmp_list.append(texture)
        if viscosity.strip() != '': tmp_list.append(viscosity)
        if fats.strip() != '': tmp_list.append(fats)
        if proteins.strip() != '': tmp_list.append(proteins)
        if quality_effect_1.strip() != '': tmp_list.append(quality_effect_1)
        if quality_effect_2.strip() != '': tmp_list.append(quality_effect_2)
        if quality_effect_3.strip() != '': tmp_list.append(quality_effect_3)
        if quality_effect_4.strip() != '': tmp_list.append(quality_effect_4)

        quality_list.append(tmp_list)

        study = experiments_quality_row[experiments_quality_fields['study']]
        study_year = experiments_quality_row[experiments_quality_fields['study_year']]

        study_list.append(f'{study} del {study_year}')

    # print(quality_list)

    quality_list_filtered = []
    for x in quality_list:
        if x:
            random.shuffle(x)
            quality_list_filtered.append(x[0])

    # quality_list_filtered = [] # [item for sublist in study_list for item in sublist]
    # for sublist in quality_list:
    #     for item in sublist:
    #         if item:
    #             quality_list_filtered.append(item)
    #     # print(sublist)

    random.shuffle(quality_list_filtered)
    # # quit()

    quality_list_filtered = list(dict.fromkeys(quality_list_filtered))
    if len(quality_list_filtered) == 0: quality_formatted = 'non causa variazioni nella qualità'
    elif len(quality_list_filtered) == 1: quality_formatted = quality_list_filtered[0]
    elif len(quality_list_filtered) == 2: quality_formatted = ' e '.join(quality_list_filtered[:2])
    else: quality_formatted = ', '.join(quality_list_filtered[:2]) + f' e {quality_list_filtered[2]}'

    study_list = list(dict.fromkeys(study_list))
    if len(study_list) != 0: study_formatted = 'Questo è dimostrato da vari studi, come '
    if len(study_list) == 0: study_formatted = ''
    elif len(study_list) == 1: study_formatted += study_list[0]
    else: study_formatted += ' e '.join(study_list[:2])
    if len(study_list) != 0: study_formatted +=  '.'

    product = experiments_quality_row[experiments_quality_fields['product_type']]
    product_ad_4 = ''
    for product_row in products_rows:
        product_tmp = product_row[products_fields['product_type']]
        if product_tmp.strip().lower() == product.strip().lower():
            product_ad_4 = product_row[products_fields['product_ad_4']]
            break
    product_formatted = f'{product_ad_4}{product}'

    line = f'L\'ozono {quality_formatted} {product_formatted}. {study_formatted}\n\n'
    print(line)

    line = line.replace('\n', '')
    line = re.sub(' +', ' ', line)
    line = line.replace(' ,', ',')
    line = line.replace(' .', '.')
    line = line.strip()
    line = line[0].capitalize() + line[1:]

    return f'{line}\n\n'


def generate_product_list_intro_quality(product_type):
    product = product_type
    product_ad = ''
    for product_row in products_rows:
        product_tmp = product_row[products_fields['product_type']]
        if product_tmp.strip().lower() == product.strip().lower():
            product_ad = product_row[products_fields['product_ad_4']]
            break
    product_formatted = f'{product_ad}{product}'

    line = f'Ecco elencati alcuni effetti dell\'ozono sulla qualità {product_ad} {product_type}.\n\n'
    print(line)
    return line


def generate_product_list_quality(rows):
    lines = []
    study_done_list = []

    for experiments_quality_row in rows:

        # GET VALUES FOR ROW
        study = experiments_quality_row[experiments_quality_fields['study']]
        study_year = experiments_quality_row[experiments_quality_fields['study_year']]
        product = experiments_quality_row[experiments_quality_fields['product']]
        treatment_type = experiments_quality_row[experiments_quality_fields['treatment_type']]
        o3_concentration = experiments_quality_row[experiments_quality_fields['o3_concentration']]
        o3_concentration_unit = experiments_quality_row[experiments_quality_fields['o3_concentration_unit']]
        treatment_time = experiments_quality_row[experiments_quality_fields['treatment_time']]
        treatment_time_unit = experiments_quality_row[experiments_quality_fields['treatment_time_unit']]

        odor = experiments_quality_row[experiments_quality_fields['odor']]
        color = experiments_quality_row[experiments_quality_fields['color']]
        flavor = experiments_quality_row[experiments_quality_fields['flavor']]
        texture = experiments_quality_row[experiments_quality_fields['texture']]
        viscosity = experiments_quality_row[experiments_quality_fields['viscosity']]
        fats = experiments_quality_row[experiments_quality_fields['fats']]
        proteins = experiments_quality_row[experiments_quality_fields['proteins']]
        quality_effect_1 = experiments_quality_row[experiments_quality_fields['quality_effect_1']]
        quality_effect_2 = experiments_quality_row[experiments_quality_fields['quality_effect_2']]
        quality_effect_3 = experiments_quality_row[experiments_quality_fields['quality_effect_3']]
        quality_effect_4 = experiments_quality_row[experiments_quality_fields['quality_effect_4']]

        if study not in study_done_list: study_done_list.append(study)
        else: continue

        # QUALITIES
        quality_list = []
        if odor.strip() != '': quality_list.append(odor)
        if color.strip() != '': quality_list.append(color)
        if flavor.strip() != '': quality_list.append(flavor)
        if texture.strip() != '': quality_list.append(texture)
        if viscosity.strip() != '': quality_list.append(viscosity)
        if fats.strip() != '': quality_list.append(fats)
        if proteins.strip() != '': quality_list.append(proteins)
        if quality_effect_1.strip() != '': quality_list.append(quality_effect_1)
        if quality_effect_2.strip() != '': quality_list.append(quality_effect_2)
        if quality_effect_3.strip() != '': quality_list.append(quality_effect_3)
        if quality_effect_4.strip() != '': quality_list.append(quality_effect_4)

        if len(quality_list) == 0: quality_formatted = 'non causa variazioni nella qualità'
        elif len(quality_list) == 1: quality_formatted = quality_list[0]
        else: quality_formatted = ', '.join(quality_list[:-1]) + f' e {quality_list[-1]}'

        # PRODUCT
        product_ad_4 = ''
        for product_row in products_rows:
            product_tmp = product_row[products_fields['product']]
            if product_tmp.strip().lower() == product.strip().lower():
                product_ad_4 = product_row[products_fields['product_ad_4']]
                break

        product_formatted = f'{product_ad_4}{product}'

        # CONDITIONS
        condition_list = []
        if treatment_type.strip() != '': condition_list.append(f'in forma {treatment_type}')
        if o3_concentration.strip() != '': condition_list.append(f'con una concentrazione di {o3_concentration} {o3_concentration_unit}')
        if treatment_time.strip() != '': condition_list.append(f'per un tempo di {treatment_time} {treatment_time_unit}')

        conditions_formatted = ''
        if len(condition_list) != 0:
            conditions_formatted = ', se usato ' + ' '.join(condition_list)

        # continue

        # FILL TEMPLATE
        line = f'''
            {quality_formatted}
            {product_formatted}
            {conditions_formatted}
            ({study}, {study_year})
            .
        '''

        # FORMAT LINE
        line = line.replace('\n', '')
        line = re.sub(' +', ' ', line)
        line = line.replace(' ,', ',')
        line = line.replace(' .', '.')
        line = line.strip()
        line = line[0].capitalize() + line[1:]
        
        print(f'- {line}\n')
        print()
        lines.append(f'- {line}\n')

    return_text = ''
    for line in lines:
        return_text += line

    return f'{return_text}\n'


experiments_application_rows = csv_get_rows('experiments-reduction')
experiments_application_fields = fields_to_dict(experiments_application_rows[0])
experiments_application_rows = experiments_application_rows[1:]

experiments_quality_rows = csv_get_rows('experiments-quality')
experiments_quality_fields = fields_to_dict(experiments_quality_rows[0])
experiments_quality_rows = experiments_quality_rows[1:]

products_rows = csv_get_rows('products')
products_fields = fields_to_dict(products_rows[0])
products_rows = products_rows[1:]



industry = 'lattiero-casearia'

# print(product_types)
# quit()

text_to_write = ''



industry_rows = []
for row in experiments_application_rows:
    if row[experiments_application_fields['industry']] == industry:
        industry_rows.append(row)

product_types = []
for row in industry_rows:
    product_type = row[experiments_application_fields['product_type']]
    if product_type not in product_types:
        product_types.append(product_type)

text_to_write += f'## L\'ozono quali proprietà sensoriali altera nei prodotti dell\'industria {industry}?\n\n'


for product_type in product_types:
    rows = [row for row in industry_rows if row[experiments_application_fields['product_type']] == product_type]

    text_to_write += f'### {product_type.capitalize()}\n\n'
    text_to_write += generate_product_intro_application(rows)
    text_to_write += generate_product_list_intro_application(product_type)
    text_to_write += generate_product_list_application(rows)

with open('test.md', 'w', encoding='utf-8') as f:
    f.write(text_to_write)

quit()




industry_rows = []
for row in experiments_quality_rows:
    if row[experiments_quality_fields['industry']] == industry:
        industry_rows.append(row)

product_types = []
for row in industry_rows:
    product_type = row[experiments_quality_fields['product_type']]
    if product_type not in product_types:
        product_types.append(product_type)

text_to_write += f'## L\'ozono quali proprietà sensoriali altera nei prodotti dell\'industria {industry}?\n\n'

text_to_write += generate_intro_quality(industry_rows)
text_to_write += generate_intro_list_quality(product_types)

for product_type in product_types:

    rows = [row for row in industry_rows if row[experiments_quality_fields['product_type']] == product_type]

    text_to_write += f'### {product_type.capitalize()}\n\n'
    text_to_write += generate_product_intro_quality(rows)
    text_to_write += generate_product_list_intro_quality(product_type)
    text_to_write += generate_product_list_quality(rows)



# with open('test.md', 'w', encoding='utf-8') as f:
#     f.write(text_to_write)