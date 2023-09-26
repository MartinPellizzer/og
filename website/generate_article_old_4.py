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


industry_rows = get_rows_by_field_value(experiments_rows, experiments_fields, 'industry', industry)
product_types = get_product_types(industry_rows, experiments_fields, 'product_type')

applications_intro_problems = []
applications_problems_list = []
for product_type in product_types:
    experiments_rows_filtered = [row for row in industry_rows if row[experiments_fields['product_type']] == product_type]

    rows = experiments_rows_filtered
    fields = experiments_fields

    item_list = []
    study_done_list = []
    problem_list = []
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

    applications_products_type.append(product_type)
    applications_intro_problems.append(problem_list)
    applications_problems_list.append(item_list)





text_to_write = ''

print(applications_intro_problems)

for line in applications_problems_list:
    applications_products_type.append(product_type)

    text_to_write += line
