from tkinter import *
from tkinter import ttk
from datetime import datetime
import sqlite3


##############################################################
# DATA
##############################################################
fields = [
	'id',
	'status',
	'date_first_added',
	'date_last_updated',
	'first_name',
	'last_name',
	'email',
	'phone',
	'business_name',
	'business_address',
	'website',
	'sector',
	'gil',
	'salesman',
]


##############################################################
# DATABASE
##############################################################
database_name = 'database.db'
table_clients = 'clients'


def db_create_table(table):
	conn = sqlite3.connect(database_name)
	c = conn.cursor()
	c.execute(f'''
		create table if not exists {table} (
			status text,
			date_first_added text,
			date_last_updated text,
			first_name text,
			last_name text,
			email text,
			phone text,
			business_name text,
			business_address text,
			website text,
			sector text,
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
		status = ?,
		date_first_added = ?,
		date_last_updated = ?,
		first_name = ?,
		last_name = ?,
		email = ?,
		phone = ?,
		business_name = ?,
		business_address = ?,
		website = ?,
		sector = ?,
		gil = ?,
		salesman = ?

		where oid = ?'''
	c.execute(sql, data)
	conn.commit()
	conn.close()


def db_delete_row():
	conn = sqlite3.connect('database.db')
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







##############################################################
# TKINTER ADD
##############################################################
def add_client():
	add_window = Toplevel(root)
	add_window.title('Treeview demo')
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
		
		c.execute('insert into clients values (:status, :date_first_added, :date_last_updated, :first_name, :last_name, :email, :phone, :business_name, :business_address, :website, :sector, :gil, :salesman)',
			{
				'status': entries_vals[1],
				'date_first_added': entries_vals[2],
				'date_last_updated': entries_vals[3],
				'first_name': entries_vals[4],
				'last_name': entries_vals[5],
				'email': entries_vals[6],
				'phone': entries_vals[7],
				'business_name': entries_vals[8],
				'business_address': entries_vals[9],
				'website': entries_vals[10],
				'sector': entries_vals[11],
				'gil': entries_vals[12],
				'salesman': entries_vals[13],
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
frame_fields = LabelFrame(root, text='Fields', padx=20, pady=10)
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


# CREATE VIEWER
frame_tree = LabelFrame(root, text='Viewer')
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
# KEY BINDING
##############################################################
tree.bind('<ButtonRelease-1>', tk_select_record)


##############################################################
# INIT
##############################################################
db_create_table(table_clients)
tk_refresh_tree(db_get_all_rows())


root.mainloop()

