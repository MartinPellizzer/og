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



def get_cell_value(row, fields, col_field):
    return row[fields[col_field]]

for experiments_quality_row in experiments_quality_rows:
    study = get_cell_value(experiments_quality_row, experiments_quality_fields, 'study')
    study_year = get_cell_value(experiments_quality_row, experiments_quality_fields, 'study_year')
    product = get_cell_value(experiments_quality_row, experiments_quality_fields, 'product')

    odor = get_cell_value(experiments_quality_row, experiments_quality_fields, 'odor')
    color = get_cell_value(experiments_quality_row, experiments_quality_fields, 'color')
    flavor = get_cell_value(experiments_quality_row, experiments_quality_fields, 'flavor')
    texture = get_cell_value(experiments_quality_row, experiments_quality_fields, 'texture')
    viscosity = get_cell_value(experiments_quality_row, experiments_quality_fields, 'viscosity')
    fats = get_cell_value(experiments_quality_row, experiments_quality_fields, 'fats')
    proteins = get_cell_value(experiments_quality_row, experiments_quality_fields, 'proteins')
    quality_effect_1 = get_cell_value(experiments_quality_row, experiments_quality_fields, 'quality_effect_1')
    quality_effect_2 = get_cell_value(experiments_quality_row, experiments_quality_fields, 'quality_effect_2')
    quality_effect_3 = get_cell_value(experiments_quality_row, experiments_quality_fields, 'quality_effect_3')
    quality_effect_4 = get_cell_value(experiments_quality_row, experiments_quality_fields, 'quality_effect_4')

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

    product_ad_4 = ''
    for product_row in products_rows:
        product_tmp = get_cell_value(product_row, products_fields, 'product_ad_4')
        if product_tmp == product:
            product_ad_4 = get_cell_value(product_row, products_fields, 'product_ad_4')
            break

    quality_formatted = ', '.join(quality_list)

    line = f'''
        {quality_formatted}
        {product_ad_4}
        {product}
        ({study}, {study_year})
        .
    '''

    print()

    print(line)

    line = line.replace('\n', '')
    line = re.sub(' +', ' ', line)
    line = line.replace(' ,', ',')
    line = line.replace(' .', '.')
    
    print(f'- {line}\n')
    print()