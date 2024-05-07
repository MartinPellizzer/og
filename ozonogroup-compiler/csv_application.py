import time

import g
import util
import util_ai

NUM_APPLICATIONS = 1

applications_rows = util.csv_get_rows(g.CSV_APPLICATIONS_FILEPATH)
applications_cols = util.csv_get_cols(applications_rows)
applications_rows = applications_rows[1:]

equipment_rows = util.csv_get_rows(g.CSV_EQUIPMENT_FILEPATH)
equipment_cols = util.csv_get_cols(equipment_rows)



bacteria_rows = util.csv_get_rows(g.CSV_BACTERIA_FILEPATH)
bacteria_cols = util.csv_get_cols(bacteria_rows)
bacteria_rows = bacteria_rows[1:]
applications_bacteria_rows = util.csv_get_rows(g.CSV_APPLICATIONS_BACTERIA_FILEPATH)
applications_bacteria_cols = util.csv_get_cols(applications_bacteria_rows)
applications_bacteria_rows = applications_bacteria_rows[1:]

virus_rows = util.csv_get_rows(g.CSV_VIRUS_FILEPATH)
virus_cols = util.csv_get_cols(virus_rows)
virus_rows = virus_rows[1:]
applications_virus_rows = util.csv_get_rows(g.CSV_APPLICATIONS_VIRUS_FILEPATH)
applications_virus_cols = util.csv_get_cols(applications_virus_rows)
applications_virus_rows = applications_virus_rows[1:]

molds_rows = util.csv_get_rows(g.CSV_MOLDS_FILEPATH)
molds_cols = util.csv_get_cols(molds_rows)
molds_rows = molds_rows[1:]
applications_molds_rows = util.csv_get_rows(g.CSV_APPLICATIONS_MOLDS_FILEPATH)
applications_molds_cols = util.csv_get_cols(applications_molds_rows)
applications_molds_rows = applications_molds_rows[1:]

insects_rows = util.csv_get_rows(g.CSV_INSECTS_FILEPATH)
insects_cols = util.csv_get_cols(insects_rows)
insects_rows = insects_rows[1:]
applications_insects_rows = util.csv_get_rows(g.CSV_APPLICATIONS_INSECTS_FILEPATH)
applications_insects_cols = util.csv_get_cols(applications_insects_rows)
applications_insects_rows = applications_insects_rows[1:]




# for application_row in applications_rows[1:]:
#     application_id = application_row[applications_cols['application_id']].strip()
#     application_sector_id = application_row[applications_cols['application_sector_id']].strip()
#     to_process = application_row[applications_cols['to_process']].strip()

#     if to_process == '': continue
#     if application_sector_id != '9': continue

#     equipment_row = []
#     for equipment_row_tmp in equipment_rows[1:]:
#         equipment_application_id_tmp = equipment_row_tmp[equipment_cols['equipment_application_id']].strip()
#         if equipment_application_id_tmp == application_id:
#             equipment_row = equipment_row_tmp
#             break
    
#     if equipment_row == []:
#         items_num = 10
#         application_a_1 = application_row[applications_cols['application_a_1']].lower()
#         application_name = application_row[applications_cols['application_name']].strip().lower()
#         application_slug = application_row[applications_cols['application_slug']].strip().lower()
#         prompt = f'''
#             Scrivi in Italiano una lista numerata di {items_num} attrezzature {application_a_1}{application_name} l'ozono può sanificare.
#             Scrivi solo il nome delle attrezzature, no le descrizioni.
#         '''
#         reply = util_ai.gen_reply(prompt).strip()

#         lines = reply.split('\n')
#         list_items = []
#         for line in lines:
#             line = line.strip()
#             if line == '': continue

#             if not line[0].isdigit(): continue
#             line = '.'.join(line.split('.')[1:])
#             line = line.replace('*', '')

#             line = line.strip()
#             if line == '': continue
#             list_items.append([
#                 application_id,
#                 application_name,
#                 application_slug,
#                 line,
#             ])
        
#         print(len(list_items))
#         if len(list_items) == items_num:
#             print('*****************************************')
#             for item in list_items: print(item)
#             print('*****************************************')
#             util.csv_add_rows(g.CSV_EQUIPMENT_FILEPATH, list_items)
#             time.sleep(g.PROMPT_DELAY_TIME)
#         # quit()



def csv_gen_applications_bacteria_by_application(application_id):
    applications_rows = util.csv_get_rows_by_col_val(
        g.CSV_APPLICATIONS_FILEPATH, applications_cols['application_id'], application_id
    )
    if applications_rows != []:
        application_row = applications_rows[0]
        application_name = application_row[applications_cols['application_name']]
        application_a_1 = application_row[applications_cols['application_a_1']]
    else:
        print('MISSING: application in csv_gen_applications_bacteria_by_application() ')
        return

    found = False
    for application_bacteria_row in applications_bacteria_rows:
        application_bacteria_id = application_bacteria_row[applications_bacteria_cols['application_id']]
        if application_bacteria_id == application_id:
            found = True
            break

    if not found:            
        prompt = f'''
            Scrivi in Italiano una lista numerata di nomi scientifici dei batteri più comuni {application_a_1}{application_name}.
            Scrivi solo i nomi scientifici dei batteri, non le descrizioni.
        '''
        reply = util_ai.gen_reply(prompt).strip()

        lines = reply.split('\n')
        list_items = []
        for line in lines:
            line = line.strip()
            if line == '': continue

            if not line[0].isdigit(): continue
            line = '.'.join(line.split('.')[1:])
            line = line.split('(')[0]
            line = line.replace('*', '')

            line = line.strip()
            if line == '': continue

            bacteria_rows_filtered = util.csv_get_rows_by_col_val(
                g.CSV_BACTERIA_FILEPATH, bacteria_cols['bacteria_name'], line
            )

            if bacteria_rows_filtered != []:
                bacteria_row = bacteria_rows_filtered[0]
                bacteria_id = bacteria_row[bacteria_cols['bacteria_id']]
                bacteria_name = bacteria_row[bacteria_cols['bacteria_name']]
            else:
                bacteria_id = ''
                bacteria_name = ''

            list_items.append([application_id, application_name, bacteria_id, line])

        if len(list_items) > 0:
            print('*****************************************')
            print(list_items)
            print('*****************************************')
            util.csv_add_rows(g.CSV_APPLICATIONS_BACTERIA_FILEPATH, list_items)

        time.sleep(g.PROMPT_DELAY_TIME)
        

def csv_gen_applications_virus_by_application(application_id):
    applications_rows = util.csv_get_rows_by_col_val(
        g.CSV_APPLICATIONS_FILEPATH, applications_cols['application_id'], application_id
    )
    if applications_rows != []:
        application_row = applications_rows[0]
        application_name = application_row[applications_cols['application_name']]
        application_a_1 = application_row[applications_cols['application_a_1']]
    else:
        print('MISSING: application in csv_gen_applications_virus_by_application() ')
        return

    found = False
    for application_virus_row in applications_virus_rows:
        application_virus_id = application_virus_row[applications_virus_cols['application_id']]
        if application_virus_id == application_id:
            found = True
            break

    if not found:            
        prompt = f'''
            Scrivi in Italiano una lista numerata di nomi scientifici dei virus più comuni {application_a_1}{application_name}.
            Scrivi solo i nomi scientifici dei virus, non le descrizioni.
        '''
        reply = util_ai.gen_reply(prompt).strip()

        lines = reply.split('\n')
        list_items = []
        for line in lines:
            line = line.strip()
            if line == '': continue

            if not line[0].isdigit(): continue
            line = '.'.join(line.split('.')[1:])
            line = line.split('(')[0]
            line = line.replace('*', '')

            line = line.strip()
            if line == '': continue

            virus_rows_filtered = util.csv_get_rows_by_col_val(
                g.CSV_BACTERIA_FILEPATH, virus_cols['virus_name'], line
            )

            if virus_rows_filtered != []:
                virus_row = virus_rows_filtered[0]
                virus_id = virus_row[virus_cols['virus_id']]
                virus_name = virus_row[virus_cols['virus_name']]
            else:
                virus_id = ''
                virus_name = ''

            list_items.append([application_id, application_name, virus_id, line])

        if len(list_items) > 0:
            print('*****************************************')
            print(list_items)
            print('*****************************************')
            util.csv_add_rows(g.CSV_APPLICATIONS_VIRUS_FILEPATH, list_items)

        time.sleep(g.PROMPT_DELAY_TIME)


def csv_gen_applications_molds_by_application(application_id):
    applications_rows = util.csv_get_rows_by_col_val(
        g.CSV_APPLICATIONS_FILEPATH, applications_cols['application_id'], application_id
    )
    if applications_rows != []:
        application_row = applications_rows[0]
        application_name = application_row[applications_cols['application_name']]
        application_a_1 = application_row[applications_cols['application_a_1']]
    else:
        print('MISSING: application in csv_gen_applications_molds_by_application()')
        return

    found = False
    for application_molds_row in applications_molds_rows:
        application_molds_id = application_molds_row[applications_molds_cols['application_id']]
        if application_molds_id == application_id:
            found = True
            break

    if not found:            
        prompt = f'''
            Scrivi in Italiano una lista numerata di nomi scientifici delle muffe più comuni {application_a_1}{application_name}.
            Scrivi solo i nomi scientifici delle muffe, non le descrizioni.
        '''
        reply = util_ai.gen_reply(prompt).strip()

        lines = reply.split('\n')
        list_items = []
        for line in lines:
            line = line.strip().lower()
            if line == '': continue

            if not line[0].isdigit(): continue
            line = '.'.join(line.split('.')[1:])
            line = line.split('(')[0]
            line = line.replace('*', '')

            line = line.strip()
            if line == '': continue

            molds_rows_filtered = util.csv_get_rows_by_col_val(
                g.CSV_MOLDS_FILEPATH, molds_cols['mold_name'], line
            )

            if molds_rows_filtered != []:
                molds_row = molds_rows_filtered[0]
                mold_id = molds_row[molds_cols['mold_id']]
                mold_name = molds_row[molds_cols['mold_name']]
            else:
                mold_id = ''
                mold_name = ''

            list_items.append([application_id, application_name, mold_id, line])

        if len(list_items) > 0:
            print('*****************************************')
            print(list_items)
            print('*****************************************')
            util.csv_add_rows(g.CSV_APPLICATIONS_MOLDS_FILEPATH, list_items)

        time.sleep(g.PROMPT_DELAY_TIME)


def csv_gen_applications_insects_by_application(application_id):
    applications_rows = util.csv_get_rows_by_col_val(
        g.CSV_APPLICATIONS_FILEPATH, applications_cols['application_id'], application_id
    )
    if applications_rows != []:
        application_row = applications_rows[0]
        application_name = application_row[applications_cols['application_name']]
        application_a_1 = application_row[applications_cols['application_a_1']]
    else:
        print('MISSING: application in csv_gen_applications_insects_by_application()')
        return

    found = False
    for application_insects_row in applications_insects_rows:
        application_insects_id = application_insects_row[applications_insects_cols['application_id']]
        if application_insects_id == application_id:
            found = True
            break

    if not found:            
        prompt = f'''
            Scrivi in Italiano una lista numerata di nomi scientifici degli insetti più comuni {application_a_1}{application_name}.
            Scrivi solo i nomi scientifici degli insetti, non le descrizioni.
        '''
        reply = util_ai.gen_reply(prompt).strip()

        lines = reply.split('\n')
        list_items = []
        for line in lines:
            line = line.strip().lower()
            if line == '': continue

            if not line[0].isdigit(): continue
            line = '.'.join(line.split('.')[1:])
            line = line.split('(')[0]
            line = line.replace('*', '')

            line = line.strip()
            if line == '': continue

            insects_rows_filtered = util.csv_get_rows_by_col_val(
                g.CSV_MOLDS_FILEPATH, insects_cols['insect_name'], line
            )

            if insects_rows_filtered != []:
                insects_row = insects_rows_filtered[0]
                insect_id = insects_row[insects_cols['insect_id']]
                insect_name = insects_row[insects_cols['insect_name']]
            else:
                insect_id = ''
                insect_name = ''

            list_items.append([application_id, application_name, insect_id, line])

        if len(list_items) > 0:
            print('*****************************************')
            print(list_items)
            print('*****************************************')
            util.csv_add_rows(g.CSV_APPLICATIONS_INSECTS_FILEPATH, list_items)

        time.sleep(g.PROMPT_DELAY_TIME)


def csv_applications():
    for application_row in applications_rows[:NUM_APPLICATIONS]:
        application_id = application_row[applications_cols['application_id']]
        application_slug = application_row[applications_cols['application_slug']]
        application_name = application_row[applications_cols['application_name']]
        application_a_1 = application_row[applications_cols['application_a_1']]

        print(application_row)

        if application_id == '': continue
        if application_slug == '': continue
        if application_name == '': continue

        csv_gen_applications_bacteria_by_application(application_id)
        csv_gen_applications_virus_by_application(application_id)
        csv_gen_applications_molds_by_application(application_id)
        csv_gen_applications_insects_by_application(application_id)

        

csv_applications()




