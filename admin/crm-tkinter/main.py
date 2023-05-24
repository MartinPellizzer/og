from tkinter import *
from tkinter import ttk, filedialog
from datetime import datetime
import sqlite3
import csv

# TODO: remove id entry, always take id from treeview selected row
# TODO: heavy refactoring before moving on


##############################################################
# DATA
##############################################################
fields = [
	'id',
	'level',
	'exp',
	'date_first_added',
	'date_last_updated',
	'first_name',
	'last_name',
	'email',
	'phone',
	'business_name',
	'business_address',
	'district',
	'website',
	'industry',
	'gil',
	'salesman',
]


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
def db_create_table_clients():
	conn = sqlite3.connect(database_name)
	c = conn.cursor()
	c.execute(f'''
		create table if not exists clients (
			level text,
			exp text,
			date_first_added text,
			date_last_updated text,
			first_name text,
			last_name text,
			email text,
			phone text,
			business_name text,
			business_address text,
			district text,
			website text,
			industry text,
			gil text,
			salesman text
		)
	''')
	conn.commit()
	conn.close()


def db_update_row(values):
	# PUT ID IN LAST POS
	data = values[1:]
	data.append(values[0])

	conn = sqlite3.connect(database_name)
	c = conn.cursor()
	sql = '''update clients set
		level = ?,
		exp = ?,
		date_first_added = ?,
		date_last_updated = ?,
		first_name = ?,
		last_name = ?,
		email = ?,
		phone = ?,
		business_name = ?,
		business_address = ?,
		district = ?,
		website = ?,
		industry = ?,
		gil = ?,
		salesman = ?

		where oid = ?'''
	c.execute(sql, data)
	conn.commit()
	conn.close()


def db_delete_row():
	conn = sqlite3.connect(database_name)
	c = conn.cursor()
	id = entries[0].get()
	c.execute(f'delete from clients where oid={id}')
	conn.commit()
	conn.close()


def db_get_all_rows():
	conn = sqlite3.connect(database_name)
	c = conn.cursor()
	c.execute('select rowid, * from clients')
	records = c.fetchall()	
	conn.commit()
	conn.close()
	return records


def db_insert_rows(rows):
	conn = sqlite3.connect(database_name)
	c = conn.cursor()
	for row in rows:
		c.execute('insert into clients values (:level, :exp, :date_first_added, :date_last_updated, :first_name, :last_name, :email, :phone, :business_name, :business_address, :district, :website, :industry, :gil, :salesman)',
			{
				'level': row[0],
				'exp': row[1],
				'date_first_added': row[2],
				'date_last_updated': row[3],
				'first_name': row[4],
				'last_name': row[5],
				'email': row[6],
				'phone': row[7],
				'business_name': row[8],
				'business_address': row[9],
				'district': row[10],
				'website': row[11],
				'industry': row[12],
				'gil': row[13],
				'salesman': row[14],
			}
		)
	conn.commit()
	conn.close()


# NOTES ####################################################
note_fields = ['business_name', 'note_date', 'note_text']

def db_create_table_notes():
	conn = sqlite3.connect(database_name)
	c = conn.cursor()
	c.execute(f'''
		create table if not exists notes (
			business_name text,
			note_date text,
			note_text text
		)
	''')
	conn.commit()
	conn.close()


def db_insert_note(row):
	conn = sqlite3.connect(database_name)
	c = conn.cursor()
	c.execute('insert into notes values (:business_name, :note_date, :note_text)',
		{
			'business_name': row[0],
			'note_date': row[1],
			'note_text': row[2],
		}
	)
	conn.commit()
	conn.close()


def db_get_all_notes():
	conn = sqlite3.connect(database_name)
	c = conn.cursor()
	c.execute('select rowid, * from notes')
	records = c.fetchall()	
	conn.commit()
	conn.close()
	return records
	

def db_get_business_notes(business_name):
	conn = sqlite3.connect(database_name)
	c = conn.cursor()
	sql = '''select rowid, * from notes 
		where business_name = ?'''
	c.execute(sql, (business_name,))
	records = c.fetchall()	
	conn.commit()
	conn.close()
	return records

	
def db_get_notes_by_id(oid):
	conn = sqlite3.connect(database_name)
	c = conn.cursor()
	sql = '''select rowid, * from notes 
		where oid = ?'''
	c.execute(sql, (oid,))
	records = c.fetchall()
	conn.commit()
	conn.close()
	return records


def db_note_delete(oid):
	conn = sqlite3.connect(database_name)
	c = conn.cursor()
	c.execute(f'delete from notes where oid={oid}')
	conn.commit()
	conn.close()


##############################################################
# TKINTER MAIN
##############################################################
def tk_get_entries_vals():
	return [entry.get() for entry in entries]


def tk_update_record():
	values = tk_get_entries_vals()
	db_update_row(values)
	tree.item(tree.focus(), text='', values=values)


# TODO: CLEAR ALSO ID? 
def tk_clear_entries():
	for i, entry in enumerate(entries[1:]):
		entry.delete(0, END)
		

def tk_delete():
	db_delete_row()
	tk_refresh_tree(db_get_all_rows())
	tk_clear_entries()
	

def tk_select_record(e):
	selected = tree.focus()
	values = tree.item(selected, 'values')

	for k, entry in enumerate(entries):
		if k == 0:
			entry.config(state='normal')
			entry.delete(0, END)
			entry.insert(0, values[k])
			entry.config(state='readonly')
		else:
			entry.delete(0, END)
			entry.insert(0, values[k])


def tk_refresh_tree(rows):
	tree.delete(*tree.get_children())
	for index, row in enumerate(rows):
		tree.insert(parent='', index=index, iid=index, text='', values=row)

# TODO: UPLOAD REAL CSV WITH BROWSE WINDOW
def tk_upload_csv():
	filename = filedialog.askopenfilename(filetypes=(("csv files","*.csv"),("All files","*.*")))
	
	with open(filename, "r") as f:
		reader = csv.reader(f, delimiter="\\")

		# FORMAT CSV ROWS FOR DB
		rows_csv = []
		for row in reader:
			formatted_row = [
				0,
				0,
				datetime.now().date(),
				datetime.now().date(),
				'',
				'',
				row[4],
				row[3],
				row[0],
				row[1],
				row[5],
				row[2],
				'',
				0,
				'',
			]
			rows_csv.append(formatted_row)
			
		rows_db = db_get_all_rows()

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

		db_insert_rows(rows_filtered)
		tk_refresh_tree(db_get_all_rows())






##############################################################
# TKINTER ADD
##############################################################
def add_client():
	add_window = Toplevel(root)
	add_window.title('Add Client')
	add_window.geometry('270x400')
	add_window.grab_set()

	add_frame = LabelFrame(add_window, text='Add Clients', padx=20, pady=10)
	add_frame.pack(side=LEFT, fill=Y)

	add_labels = []
	add_entries = []
	for i, field in enumerate(fields):
		add_labels.append(Label(add_frame, text=field).grid(row=i, column=0, sticky=W))
		tmp_entry = Entry(add_frame)
		tmp_entry.grid(row=i, column=1, sticky=W)
		if field == 'id':
			tmp_entry.insert(0, '-')
			tmp_entry.config(state='disabled')
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
				'level': entries_vals[1],
				'exp': entries_vals[2],
				'date_first_added': entries_vals[3],
				'date_last_updated': entries_vals[4],
				'first_name': entries_vals[5],
				'last_name': entries_vals[6],
				'email': entries_vals[7],
				'phone': entries_vals[8],
				'business_name': entries_vals[9],
				'business_address': entries_vals[10],
				'district': entries_vals[11],
				'website': entries_vals[12],
				'industry': entries_vals[13],
				'gil': entries_vals[14],
				'salesman': entries_vals[15],
			})


		conn.commit()
		conn.close()

		tk_clear_entries()
		tk_refresh_tree(db_get_all_rows())

	curr_add_button = Button(add_frame, text='Add', command=add_client_db)
	curr_add_button.grid(row=i, column=0, sticky=W)



root = Tk()
root.title('Ozonogroup CRM')
root.iconbitmap('logo.ico')
root.geometry('800x600')

# CREATE FIELDS
frame_fields = Frame(root, padx=20, pady=10)
frame_fields.pack(side=LEFT, fill=Y)

labels = []
entries = []
for i, field in enumerate(fields):
	labels.append(Label(frame_fields, text=field).grid(row=i, column=0, sticky=W))
	tmp_entry = Entry(frame_fields)
	if field == 'id':
		tmp_entry.insert(0, '-')
		tmp_entry.config(state='readonly')
	tmp_entry.grid(row=i, column=1, sticky=W)
	entries.append(tmp_entry)
i += 1
clear_button = Button(frame_fields, text='Clear', command=tk_clear_entries)
clear_button.grid(row=i, column=0, sticky=W)
i += 1
remove_button = Button(frame_fields, text='Remove', command=tk_delete)
remove_button.grid(row=i, column=0, sticky=W)
i += 1
update_button = Button(frame_fields, text='Update', command=tk_update_record)
update_button.grid(row=i, column=0, sticky=W)
i += 1
add_button = Button(frame_fields, text='Add', command=add_client)
add_button.grid(row=i, column=0, sticky=W)
i += 1
upload_csv_button = Button(frame_fields, text='Upload CSV', command=tk_upload_csv)
upload_csv_button.grid(row=i, column=0, sticky=W)
i += 1



# CREATE VIEWER
frame_tree = Frame(root)
frame_tree.pack(side=LEFT, expand=True, fill=BOTH)

tree = ttk.Treeview(frame_tree)
tree.pack(expand=True, fill=BOTH)

tree['columns'] = fields

tree.column('#0', width=0, stretch=NO)
tree.heading('#0', text='', anchor=W)
for field in fields:
	tree.column(field, width=80, anchor=W)
	tree.heading(field, text=field, anchor=W)





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
	business_name_curr = values[9]


	def tk_note_refresh_tree():
		rows = db_get_business_notes(business_name_curr)
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
		record = db_get_notes_by_id(values[0])[0]
		note_text.delete('1.0', END)
		note_text.insert(END, record[3])


	def add_note():
		note_date = datetime.now()
		note_content = note_text.get("1.0",END)
		row = [business_name_curr, note_date, note_content]
		db_insert_note(row)
		tk_note_refresh_tree()


	def tk_note_delete():
		note_selected = note_tree.focus()
		values = note_tree.item(note_selected, 'values')
		oid = values[0]

		db_note_delete(oid)
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
	note_fields = ['note_id', 'note_date', 'note_text']
	note_tree['columns'] = note_fields
	note_tree.column('#0', width=0, stretch=NO)
	note_tree.heading('#0', text='', anchor=W)
	for field in note_fields:
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

	note_tree.bind('<ButtonRelease-1>', tk_note_selected)




##############################################################
# KEY BINDING
##############################################################
tree.bind('<ButtonRelease-1>', tk_select_record)
tree.bind("<Double-1>", tk_open_notes)


##############################################################
# INIT
##############################################################
# drop_table(table_clients)
db_create_table_clients()
db_create_table_notes()
tk_refresh_tree(db_get_all_rows())
# print(db_get_all_notes())






root.mainloop()

