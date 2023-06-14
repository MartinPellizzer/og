from tkinter import *
from tkinter import ttk, filedialog
from datetime import datetime, timedelta
import sqlite3
import csv
import os

# TODO: heavy refactoring before moving on


##############################################################
# DATA
##############################################################
db_notes_fields = {
	'business_name': "text", 
	'note_date': "text", 
	'note_text': "text",
}

db_clients_fields = {
	'gil': "text",
	'level': "text",
	'attempt': "text",
	'date_first_added': "text",
	'date_last_action': "text",
	'date_next_action': "text",
	'first_name': "text",
	'last_name': "text",
	'email': "text",
	'phone': "text",
	'business_name': "text",
	'business_address': "text",
	'district': "text",
	'website': "text",
	'industry': "text",
	'salesman': "text",
}

clients_fields = [f'{f}' for f in db_clients_fields]


##############################################################
# DATABASE
##############################################################
database_name = 'database.db'

def drop_table(table):
	conn = sqlite3.connect(database_name)
	c = conn.cursor()
	c.execute(f'drop table {table}')
	conn.commit()
	conn.close()


# CLIENTS ####################################################
def db_pragma_table_clients():
	conn = sqlite3.connect(database_name)
	c = conn.cursor()
	c.execute('select * from clients')
	print(list(map(lambda x: x[0], c.description)))
	conn.commit()
	conn.close()


def db_clients_create_table():
	fields_lst = [f'{f} {db_clients_fields[f]}' for f in db_clients_fields]
	fields = ', '.join(fields_lst)
	conn = sqlite3.connect(database_name)
	c = conn.cursor()
	c.execute(f'''create table if not exists clients ({fields})''')
	conn.commit()
	conn.close()


def db_clients_update_by_business_name(values):
	values.append(values[10])
	fields = ' = ?, '.join(db_clients_fields) + ' = ?'
	conn = sqlite3.connect(database_name)
	c = conn.cursor()
	sql = f'''update clients set {fields} where business_name = ?'''
	c.execute(sql, values)
	conn.commit()
	conn.close()


# def db_clients_delete_selected_row():
# 	conn = sqlite3.connect(database_name)
# 	c = conn.cursor()
# 	selected = tree.focus()
# 	values = tree.item(selected, 'values')
# 	c.execute(f'delete from clients where oid={values[0]}')
# 	conn.commit()
# 	conn.close()


def db_clients_get_rows():
	conn = sqlite3.connect(database_name)
	c = conn.cursor()
	c.execute('select * from clients')
	records = c.fetchall()	
	conn.commit()
	conn.close()
	return records


def db_clients_get_by_level(level):
	conn = sqlite3.connect(database_name)
	c = conn.cursor()
	c.execute(f'select * from clients where level={level}')
	records = c.fetchall()	
	conn.commit()
	conn.close()
	return records


def db_clients_get_by_date_next_action(date):
	conn = sqlite3.connect(database_name)
	c = conn.cursor()
	c.execute(f'select * from clients')
	records = c.fetchall()	
	records_filtered = [record for record in records if record[5] == str(date).strip()]
	conn.commit()
	conn.close()
	return records_filtered


def db_clients_insert_rows(rows):
	fields_lst = [f'{f}' for f in db_clients_fields]
	fields = ':' + ', :'.join(fields_lst)

	conn = sqlite3.connect(database_name)
	c = conn.cursor()
	for row in rows:
		fields_dict = {}
		for i, key in enumerate(db_clients_fields):
			fields_dict[key] = row[i]
		c.execute(f'insert into clients values ({fields})', fields_dict)
	conn.commit()
	conn.close()


# NOTES ####################################################

def db_notes_create_table():
	fields_lst = [f'{f} {db_notes_fields[f]}' for f in db_notes_fields]
	fields = ', '.join(fields_lst)
	conn = sqlite3.connect(database_name)
	c = conn.cursor()
	c.execute(f'''create table if not exists notes ({fields})''')


def db_notes_insert_row(row):
	fields_lst = [f'{f}' for f in db_notes_fields]
	fields = ':' + ', :'.join(fields_lst)

	fields_dict = {}
	for i, key in enumerate(db_notes_fields):
		fields_dict[key] = row[i]

	conn = sqlite3.connect(database_name)
	c = conn.cursor()
	c.execute(f'insert into notes values ({fields})', fields_dict)
	conn.commit()
	conn.close()


def db_notes_get_rows():
	conn = sqlite3.connect(database_name)
	c = conn.cursor()
	c.execute('select rowid, * from notes')
	records = c.fetchall()	
	conn.commit()
	conn.close()
	return records
	

def db_notes_get_by_business_name(business_name):
	conn = sqlite3.connect(database_name)
	c = conn.cursor()
	sql = '''select rowid, * from notes 
		where business_name = ?'''
	c.execute(sql, (business_name,))
	records = c.fetchall()	
	conn.commit()
	conn.close()
	return records

	
def db_notes_get_by_oid(oid):
	conn = sqlite3.connect(database_name)
	c = conn.cursor()
	sql = '''select rowid, * from notes 
		where oid = ?'''
	c.execute(sql, (oid,))
	records = c.fetchall()
	conn.commit()
	conn.close()
	return records


def db_notes_delete_by_oid(oid):
	conn = sqlite3.connect(database_name)
	c = conn.cursor()
	c.execute(f'delete from notes where oid={oid}')
	conn.commit()
	conn.close()


##############################################################
# TKINTER CLIENTS
##############################################################
def tk_clients_entries_refresh():
	selected = tree.focus()
	values = tree.item(selected, 'values')
	for k, entry in enumerate(entries):
		entry.delete(0, END)
		entry.insert(0, values[k])


def tk_clients_entries_get_vals():
	return [entry.get() for entry in entries]


def tk_clients_entries_update_row():
	values = tk_clients_entries_get_vals()
	db_clients_update_by_business_name(values)
	tree.item(tree.focus(), text='', values=values)


def tk_clients_tree_refresh(rows):
	tree.delete(*tree.get_children())
	for index, row in enumerate(rows):
		tree.insert(parent='', index=index, iid=index, text='', values=row, tags=(row[1],))
	

def tk_clients_tree_color():
	tree.tag_configure(-1, background='red')
	tree.tag_configure(1, background='yellow')
	tree.tag_configure(2, background='yellow')
	tree.tag_configure(3, background='yellow')
	tree.tag_configure(4, background='yellow')
	tree.tag_configure(5, background='yellow')
	tree.tag_configure(6, background='green')


def tk_clients_tree_upload_csv():
	filename = filedialog.askopenfilename(filetypes=(("csv files","*.csv"),("All files","*.*")))
	
	with open(filename, "r") as f:
		reader = csv.reader(f, delimiter="\\")

		# FORMAT CSV ROWS FOR DB
		rows_csv = []
		for row in reader:
			curr_gil = 0
			curr_level = 0
			curr_attempt = 0
			curr_date_first_added = datetime.now().date()
			curr_date_last_action = datetime.now().date()
			curr_date_next_action = datetime.now().date()
			curr_first_name = ''
			curr_last_name = ''
			curr_email = row[4]
			curr_phone = row[3]
			curr_business_name = row[0]
			curr_business_address = row[1]
			curr_district = row[5]
			curr_website = row[2]
			curr_industry = ''
			curr_salesman = ''

			formatted_row = [
				curr_gil,
				curr_level,
				curr_attempt,
				curr_date_first_added,
				curr_date_last_action,
				curr_date_next_action,
				curr_first_name,
				curr_last_name,
				curr_email,
				curr_phone,
				curr_business_name,
				curr_business_address,
				curr_district,
				curr_website,
				curr_industry,
				curr_salesman,
			]
			rows_csv.append(formatted_row)
			
		rows_db = db_clients_get_rows()

		# FILTER ROWS THAT WITH SAME BUSINESS NAME IN DB
		rows_filtered = []
		for row_csv in rows_csv:
			found = False
			for row_db in rows_db:
				if row_csv[8] == row_db[9]:
					found = True
					break
			if not found:
				rows_filtered.append(row_csv)

		db_clients_insert_rows(rows_filtered)
		tk_clients_tree_refresh(db_clients_get_rows())


def tk_clients_procedure_refresh():
	selected = tree.focus()
	values = tree.item(selected, 'values')
	if not values: return

	file_path = f'procedures/procedure_{values[1]}.txt'
	if not os.path.exists(file_path): return

	with open(file_path) as f:
		content = f.read()
		procedure_text.configure(state='normal')
		procedure_text.delete('1.0', END)
		procedure_text.insert('end', content)
		procedure_text.configure(state='disabled')


def tk_clients_tree_level_up_row_selected(e):
	iid = tree.focus()
	values = list(tree.item(iid, 'values'))

	level_curr = int(values[1])
	level_next = int(values[1]) + 1

	values[1] = level_next
	values[4] = datetime.now().date()

	if level_curr == 0:
		values[5] = datetime.now().date() + timedelta(days=30)	
	elif level_curr == 1:
		values[5] = datetime.now().date() + timedelta(days=7)
	elif level_curr == 2:
		values[5] = datetime.now().date()
	
	db_clients_update_by_business_name(values)
	tk_clients_tree_refresh(db_clients_get_rows())
	tree.focus(iid)
	tree.selection_set(iid)
	tk_clients_entries_refresh()
	tk_clients_procedure_refresh()


def tk_clients_tree_level_down_row_selected(e):
	iid = tree.focus()
	values = list(tree.item(iid, 'values'))
	values[1] = int(values[1]) - 1
	db_clients_update_by_business_name(values)
	tk_clients_tree_refresh(db_clients_get_rows())
	tree.focus(iid)
	tree.selection_set(iid)
	tk_clients_entries_refresh()
	tk_clients_procedure_refresh()


def tk_clients_tree_get_by_priority(e):
	rows = db_clients_get_by_level(3) # Call
	rows += db_clients_get_by_level(4) # Inspection
	rows += db_clients_get_by_level(5) # Inspection Follow up
	rows += db_clients_get_by_level(2) # Email more info
	rows += db_clients_get_by_level(1) # Email again
	rows += db_clients_get_by_level(0) # Email first time
	tk_clients_tree_refresh(rows)
	tree.focus(0)
	tree.selection_set(0)
	

def tk_clients_tree_get_by_level(e):
	rows = db_clients_get_by_level(e.char)
	tk_clients_tree_refresh(rows)
	if not rows: return
	tree.focus(0)
	tree.selection_set(0)


def tk_clients_tree_get_all(e):
	tk_clients_tree_refresh(db_clients_get_rows())
	tree.focus(0)
	tree.selection_set(0)


def tk_clients_tree_move_down(e):
	try:
		next_row = int(tree.focus()) + 1
		tree.focus(next_row)
		tree.selection_set(next_row)
	except: return

	tk_clients_entries_refresh()
	tk_clients_procedure_refresh()
	return "break"


def tk_clients_tree_move_up(e):
	try:
		next_row = int(tree.focus()) - 1
		tree.focus(next_row)
		tree.selection_set(next_row)
	except: return

	tk_clients_entries_refresh()
	tk_clients_procedure_refresh()
	return "break"


def tk_clients_tree_move_j(e):
	try:
		next_row = int(tree.focus()) + 1
		tree.focus(next_row)
		tree.selection_set(next_row)
	except: return
	
	tk_clients_entries_refresh()
	tk_clients_procedure_refresh()


def tk_clients_tree_move_k(e):
	try:
		next_row = int(tree.focus()) - 1
		tree.focus(next_row)
		tree.selection_set(next_row)
	except: return

	tk_clients_entries_refresh()
	tk_clients_procedure_refresh()


def tk_clients_tree_get_rows_today(e):
	today_date = datetime.now().date()
	rows = db_clients_get_by_date_next_action(today_date)
	rows_prioritized = []
	rows_prioritized += [row for row in rows if row[1] == '3']
	rows_prioritized += [row for row in rows if row[1] == '4']
	rows_prioritized += [row for row in rows if row[1] == '5']
	rows_prioritized += [row for row in rows if row[1] == '2']
	rows_prioritized += [row for row in rows if row[1] == '1']
	rows_prioritized += [row for row in rows if row[1] == '6']
	rows_prioritized += [row for row in rows if row[1] == '0']
	tk_clients_tree_refresh(rows_prioritized)
	tree.focus(0)
	tree.selection_set(0)

	
def tk_clients_tree_refresh_entries_procedure(e):
	tk_clients_entries_refresh()
	tk_clients_procedure_refresh()


##############################################################
# TKINTER ADD
##############################################################
# TODO: keep it or delete it?
def add_client():
	add_window = Toplevel(root)
	add_window.title('Add Client')
	add_window.geometry('270x400')
	add_window.grab_set()

	add_frame = LabelFrame(add_window, text='Add Clients', padx=20, pady=10)
	add_frame.pack(side=LEFT, fill=Y)

	add_labels = []
	add_entries = []
	for i, field in enumerate(clients_fields):
		add_labels.append(Label(add_frame, text=field).grid(row=i, column=0, sticky=W))
		tmp_entry = Entry(add_frame)
		tmp_entry.grid(row=i, column=1, sticky=W)
		if field == 'id':
			continue
		elif field == 'status':
			tmp_entry.insert(0, 0)
		elif field == 'date_first_added':
			tmp_entry.insert(0, datetime.now().date())
		elif field == 'date_last_updated':
			tmp_entry.insert(0, datetime.now().date())
		add_entries.append(tmp_entry)
	i += 1

	def add_client_db():
		conn = sqlite3.connect(database_name)
		c = conn.cursor()

		entries_vals = [entry.get() for entry in add_entries]
		
		c.execute('insert into clients values (:level, :exp, :date_first_added, :date_last_updated, :first_name, :last_name, :email, :phone, :business_name, :business_address, :district, :website, :industry, :gil, :salesman)',
			{
				'level': entries_vals[0],
				'exp': entries_vals[1],
				'date_first_added': entries_vals[2],
				'date_last_updated': entries_vals[3],
				'first_name': entries_vals[4],
				'last_name': entries_vals[5],
				'email': entries_vals[6],
				'phone': entries_vals[7],
				'business_name': entries_vals[8],
				'business_address': entries_vals[9],
				'district': entries_vals[10],
				'website': entries_vals[11],
				'industry': entries_vals[12],
				'gil': entries_vals[13],
				'salesman': entries_vals[14],
			})


		conn.commit()
		conn.close()

		tk_entries_clear()
		tk_clients_tree_refresh(db_clients_get_rows())

	curr_add_button = Button(add_frame, text='Add', command=add_client_db)
	curr_add_button.grid(row=i, column=0, sticky=W)


##############################################################
# TKINTER NOTES
##############################################################
def tk_open_notes(e):
	note_window = Toplevel(root)
	note_window.title('Add Note')
	note_window.geometry('800x600')
	note_window.grab_set()
	
	selected = tree.focus()
	values = tree.item(selected, 'values')
	business_name_curr = values[10]


	def tk_note_refresh_tree():
		rows = db_notes_get_by_business_name(business_name_curr)
		note_tree.delete(*note_tree.get_children())
		for index, row in enumerate(rows):
			note_id_tmp = row[0]
			note_date_tmp = row[2]
			note_text_tmp = row[3].replace('\n', ' ')[:40] + '...'
			note_temp = [note_id_tmp, note_date_tmp, note_text_tmp]
			note_tree.insert(parent='', index=index, iid=index, text='', values=note_temp)


	def tk_note_selected(e):
		note_selected = note_tree.focus()
		values = note_tree.item(note_selected, 'values')
		record = db_notes_get_by_oid(values[0])[0]
		note_text.delete('1.0', END)
		note_text.insert(END, record[3])


	def add_note():
		note_date = datetime.now()
		note_content = note_text.get("1.0",END)
		row = [business_name_curr, note_date, note_content]

		iid = tree.focus()
		values = list(tree.item(iid, 'values'))
		data = note_data_entry.get()
		if data != '':
			values[5] = note_data_entry.get()

		db_notes_insert_row(row)
		db_clients_update_by_business_name(values)
		tk_note_refresh_tree()
		tk_clients_tree_refresh(db_clients_get_rows())
		tree.focus(iid)
		tree.selection_set(iid)


	def tk_note_delete():
		note_selected = note_tree.focus()
		values = note_tree.item(note_selected, 'values')
		oid = values[0]

		db_notes_delete_by_oid(oid)
		tk_note_refresh_tree()
		note_text.delete('1.0', END)


	note_frame_row_1 = Frame(note_window)
	note_frame_row_1.pack()
	note_frame_row_2 = Frame(note_window)
	note_frame_row_2.pack(expand=True, fill=BOTH)

	note_label = Label(note_frame_row_1, text=business_name_curr, font=('Arial', 32))
	note_label.pack()
	
	# TREEVIEW
	note_frame_tree = Frame(note_frame_row_2)
	note_frame_tree.pack(side=LEFT, fill=BOTH)
	note_tree = ttk.Treeview(note_frame_tree)
	note_tree.pack(expand=True, fill=BOTH)
	tw_note_fields = ['note_id', 'note_date', 'note_text']
	note_tree['columns'] = tw_note_fields
	note_tree.column('#0', width=0, stretch=NO)
	note_tree.heading('#0', text='', anchor=W)
	for field in tw_note_fields:
		note_tree.column(field, width=160, anchor=W)
		note_tree.heading(field, text=field, anchor=W)

	tk_note_refresh_tree()
		
	# TEXTAREA
	note_frame_text = Frame(note_frame_row_2)
	note_frame_text.pack(side=LEFT, expand=True, fill=BOTH)
	note_text = Text(note_frame_text)
	note_text.pack(expand=True, fill=BOTH)
	note_add = Button(note_frame_text, text='Add Note', command=add_note)
	note_add.pack()
	note_delete = Button(note_frame_text, text='Delete Note', command=tk_note_delete)
	note_delete.pack()

	note_data_label = Label(note_frame_text, text='Next Action Data: (1991-09-27)')
	note_data_label.pack()
	note_data_entry = Entry(note_frame_text)
	note_data_entry.pack()

	note_tree.bind('<ButtonRelease-1>', tk_note_selected)

	




##############################################################
# TKINTER MAIN
##############################################################

root = Tk()
root.title('Ozonogroup CRM')
root.iconbitmap('logo.ico')
root.geometry('800x600')
# root.state('zoomed')

# CREATE FIELDS
frame_fields = Frame(root, padx=20, pady=10)
frame_fields.pack(side=LEFT, fill=Y)

labels = []
entries = []
for i, field in enumerate(clients_fields):
	labels.append(Label(frame_fields, text=field).grid(row=i, column=0, sticky=W))
	tmp_entry = Entry(frame_fields)
	if field == 'id':
		tmp_entry.insert(0, '-')
		tmp_entry.config(state='readonly')
	tmp_entry.grid(row=i, column=1, sticky=W)
	entries.append(tmp_entry)
i += 1
update_button = Button(frame_fields, text='Update', command=tk_clients_entries_update_row)
update_button.grid(row=i, column=0, sticky=W)
i += 1

# CREATE VIEWER
frame_main = Frame(root)
frame_main.pack(side=LEFT, expand=True, fill=BOTH)

frame_tree = Frame(frame_main)
frame_tree.pack(side=TOP, expand=True, fill=BOTH)

tree = ttk.Treeview(frame_tree)
tree.pack(expand=True, fill=BOTH)

tree['columns'] = clients_fields

tree.column('#0', width=0, stretch=NO)
tree.heading('#0', text='', anchor=W)
for field in clients_fields:
	tree.column(field, width=80, anchor=W)
	tree.heading(field, text=field, anchor=W)

frame_upload_csv= Frame(frame_main, padx=10, pady=10)
frame_upload_csv.pack(side=TOP, fill=X)

upload_csv_button = Button(frame_upload_csv, text='Upload CSV', command=tk_clients_tree_upload_csv)
upload_csv_button.pack(side=RIGHT)

# VIEW PROCEDURE
procedure_frame = Frame(root)
procedure_frame.pack(side=LEFT, fill=Y)

procedure_text = Text(procedure_frame, padx=20, pady=10)
procedure_text.pack(expand=True, fill=BOTH)


##############################################################
# KEY BINDING
##############################################################
tree.bind('<ButtonRelease-1>', tk_clients_tree_refresh_entries_procedure)
tree.bind("<Double-1>", tk_open_notes)
tree.bind("<space>", tk_open_notes)
tree.bind("+", tk_clients_tree_level_up_row_selected)
tree.bind("-", tk_clients_tree_level_down_row_selected)
tree.bind("p", tk_clients_tree_get_by_priority)
tree.bind("t", tk_clients_tree_get_rows_today)
tree.bind(".", tk_clients_tree_get_all)
tree.bind("0", tk_clients_tree_get_by_level)
tree.bind("1", tk_clients_tree_get_by_level)
tree.bind("2", tk_clients_tree_get_by_level)
tree.bind("3", tk_clients_tree_get_by_level)
tree.bind("4", tk_clients_tree_get_by_level)
tree.bind("5", tk_clients_tree_get_by_level)
tree.bind("6", tk_clients_tree_get_by_level)
tree.bind("7", tk_clients_tree_get_by_level)
tree.bind("8", tk_clients_tree_get_by_level)
tree.bind("9", tk_clients_tree_get_by_level)


tree.bind('j', tk_clients_tree_move_j)
tree.bind('k', tk_clients_tree_move_k)

tree.bind('<Up>', tk_clients_tree_move_up)
tree.bind('<Down>', tk_clients_tree_move_down)


##############################################################
# INIT
##############################################################
# drop_table('clients')
db_clients_create_table()
db_notes_create_table()

tk_clients_tree_refresh(db_clients_get_rows())
tk_clients_tree_color()
tree.focus_set()

try: 
	tree.focus(0)
	tree.selection_set(0)
except:
	pass


selected = tree.focus()
values = tree.item(selected, 'values')

try: tk_clients_entries_refresh()
except: pass
tk_clients_procedure_refresh()

# print(db_notes_get_rows())

# db_pragma_table_clients()



root.mainloop()

