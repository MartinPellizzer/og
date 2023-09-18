import sqlite3
from tkinter import *


database_name = 'ozone_it.db'

db_experiments_fields = {
	'study': "text",
	'study_year': "text",
	'product_family': "text",
	'product': "text",
	'problem': "text",
	'treatment_type': "text",
	'treatment': "text",
	'w_pressure': "text",
	'o3_concentration': "text",
	'pathogen_reduction': "text",
}
							



db_pathogens_fields = {
	'name': "text",
}



def db_ozone_create_database():
    conn = sqlite3.connect(database_name)
    conn.close()
    
def db_show_tables():
    con = sqlite3.connect(database_name)
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cursor.fetchall())

def db_table_show_fields(name):
	conn = sqlite3.connect(database_name)
	c = conn.cursor()
	c.execute(f'select * from {name}')
	print(list(map(lambda x: x[0], c.description)))
	conn.commit()
	conn.close()



def db_experiments_create_table():
    fields_list = [f'{f} {db_experiments_fields[f]}' for f in db_experiments_fields]
    fields = ', '.join(fields_list)

    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute(f'''create table if not exists experiments ({fields})''')
    conn.commit()
    conn.close()


def db_experiments_get_rows():
	conn = sqlite3.connect(database_name)
	c = conn.cursor()
	c.execute('select * from experiments')
	records = c.fetchall()	
	conn.commit()
	conn.close()
	return records

def db_experiments_insert_row():
    fields_lst = [f'{f}' for f in db_experiments_fields]
    fields = ':' + ', :'.join(fields_lst)

    fields_dict = {}
    for i, key in enumerate(db_experiments_fields):
        fields_dict[key] = 'test'

    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    sql = f'insert into experiments values ({fields})', fields_dict
    print(sql)
    c.execute(f'insert into experiments values ({fields})', fields_dict)
    conn.commit()
    conn.close()


# ----------------------------------------------------------------------
# TABLE PATHOGENS
# ----------------------------------------------------------------------
def db_table_create(name, db_fields):
    fields_list = [f'{f} {db_fields[f]}' for f in db_fields]
    fields = ', '.join(fields_list)

    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute(f'''create table if not exists {name} ({fields})''')
    conn.commit()
    conn.close()
    

def db_table_get_rows(name):
	conn = sqlite3.connect(database_name)
	c = conn.cursor()
	c.execute(f'select * from {name}')
	records = c.fetchall()	
	conn.commit()
	conn.close()
	return records

    
def db_table_insert_row(name, db_fields, values):
    fields_lst = [f'{f}' for f in db_fields]
    fields = ':' + ', :'.join(fields_lst)

    print(len(db_fields))
    print(len(values))

    fields_dict = {}
    for i, key in enumerate(db_fields):
        fields_dict[key] = values[i]

    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute(f'insert into {name} values ({fields})', fields_dict)
    conn.commit()
    conn.close()



db_table_create('experiments', db_experiments_fields)
db_show_tables()
# db_table_show_fields('pathogens')
# db_table_insert_row('pathogens', db_pathogens_fields)
# rows = db_table_get_rows('pathogens')

# print(rows)



def tk_add_pathogen_db():
    entry_val = tmp_entry.get()
    db_table_insert_row('pathogens', db_pathogens_fields, [entry_val])
    rows = db_table_get_rows('pathogens')
    print(rows)
    
def tk_add_experiment_db():
    entries_vals = [entry.get() for entry in entries]
    print(entries_vals)
    # return ''
    db_table_insert_row('experiments', db_experiments_fields, entries_vals)
    rows = db_table_get_rows('experiments')
    print(rows)



##############################################################
# TKINTER MAIN
##############################################################
root = Tk()
root.title('Ozone DB')
root.geometry('800x600')

# CREATE FIELDS
frame_fields = Frame(root, padx=20, pady=10)
frame_fields.pack(side=LEFT, fill=Y)

labels = []
entries = []
for i, field in enumerate(db_experiments_fields):
	tmp_label = Label(frame_fields, text=field)
	tmp_label.grid(row=i, column=0, sticky=W)
	labels.append(tmp_label)

	tmp_entry = Entry(frame_fields)
	tmp_entry.grid(row=i, column=1, sticky=W)
	entries.append(tmp_entry)

i += 1
add_button = Button(frame_fields, text='Add', command=tk_add_experiment_db)
add_button.grid(row=i, column=0, sticky=W)
i += 1


root.mainloop()