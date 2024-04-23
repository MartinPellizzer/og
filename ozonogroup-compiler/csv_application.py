import time

import g
import util
import util_ai

applications_rows = util.csv_get_rows(g.CSV_APPLICATIONS_FILEPATH)
applications_cols = util.csv_get_cols(applications_rows)

equipment_rows = util.csv_get_rows(g.CSV_EQUIPMENT_FILEPATH)
equipment_cols = util.csv_get_cols(equipment_rows)

for application_row in applications_rows[1:]:
    application_id = application_row[applications_cols['application_id']].strip()
    application_sector_id = application_row[applications_cols['application_sector_id']].strip()
    to_process = application_row[applications_cols['to_process']].strip()

    if to_process == '': continue
    if application_sector_id != '9': continue

    equipment_row = []
    for equipment_row_tmp in equipment_rows[1:]:
        equipment_application_id_tmp = equipment_row_tmp[equipment_cols['equipment_application_id']].strip()
        if equipment_application_id_tmp == application_id:
            equipment_row = equipment_row_tmp
            break
    
    if equipment_row == []:
        items_num = 10
        application_a_1 = application_row[applications_cols['application_a_1']].lower()
        application_name = application_row[applications_cols['application_name']].strip().lower()
        application_slug = application_row[applications_cols['application_slug']].strip().lower()
        prompt = f'''
            Scrivi in Italiano una lista numerata di {items_num} attrezzature {application_a_1}{application_name} l'ozono può sanificare.
            Scrivi solo il nome delle attrezzature, no le descrizioni.
        '''
        reply = util_ai.gen_reply(prompt).strip()

        lines = reply.split('\n')
        list_items = []
        for line in lines:
            line = line.strip()
            if line == '': continue

            if not line[0].isdigit(): continue
            line = '.'.join(line.split('.')[1:])
            line = line.replace('*', '')

            line = line.strip()
            if line == '': continue
            list_items.append([
                application_id,
                application_name,
                application_slug,
                line,
            ])
        
        print(len(list_items))
        if len(list_items) == items_num:
            print('*****************************************')
            for item in list_items: print(item)
            print('*****************************************')
            util.csv_add_rows(g.CSV_EQUIPMENT_FILEPATH, list_items)
            time.sleep(g.PROMPT_DELAY_TIME)
        # quit()




