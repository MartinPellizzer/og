import csv
import re


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



experiments_quality_rows = csv_get_rows('experiments-quality')
experiments_quality_fields = fields_to_dict(experiments_quality_rows[0])
experiments_quality_rows = experiments_quality_rows[1:]

products_rows = csv_get_rows('products')
products_fields = fields_to_dict(products_rows[0])
products_rows = products_rows[1:]







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

        study = experiments_quality_row[experiments_quality_fields['study']]
        study_year = experiments_quality_row[experiments_quality_fields['study_year']]

        study_list.append(f'{study} del {study_year}')

    quality_list = list(dict.fromkeys(quality_list))
    if len(quality_list) == 0: quality_formatted = 'non causa variazioni nella qualità'
    elif len(quality_list) == 1: quality_formatted = quality_list[0]
    elif len(quality_list) == 2: ' e '.join(quality_list[:2])
    else: quality_formatted = ', '.join(quality_list[:2]) + f' e {quality_list[2]}'

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
    line = f'Ecco elencati alcuni effetti dell\'ozono sulla qualità del {product_type}.\n\n'
    print(line)
    return line


def generate_product_list_quality(rows):
    return_text = ''

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
        return_text += f'- {line}\n\n'

    return return_text



industry = 'lattiero-casearia'

industry_rows = []
for row in experiments_quality_rows:
    if row[experiments_quality_fields['industry']] == industry:
        industry_rows.append(row)

product_types = []
for row in industry_rows:
    product_type = row[experiments_quality_fields['product_type']]
    if product_type not in product_types:
        product_types.append(product_type)

# print(product_types)
# quit()

text_to_write = ''

for product_type in product_types:
    milk_rows = [row for row in industry_rows if row[experiments_quality_fields['product_type']] == product_type]

    # text_to_write += generate_intro_quality()

    text_to_write += f'# {product_type}\n\n'
    text_to_write += generate_product_intro_quality(milk_rows)
    text_to_write += generate_product_list_intro_quality(product_type)
    text_to_write += generate_product_list_quality(milk_rows)



with open('test.md', 'w', encoding='utf-8') as f:
    f.write(text_to_write)