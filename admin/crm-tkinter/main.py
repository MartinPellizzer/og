from tkinter import *
from tkinter import ttk
from datetime import datetime
import sqlite3

database_name = 'database.db'


root = Tk()
root.title('Ozonogroup CRM')
root.geometry('800x600')

data = [
	(
	'0',
	'0',
	'2023-05-19',
	'2023-05-19',
	'Martin',
	'Pellizzer',
	'martinpellizeer@gmail.com',
	'3209624740',
	'MP',
	'Via Cornere, 13',
	'martinpellizzer.com',
	'Ozono',
	'0',
	'Luca',
	),
	(
	'1',
	'0',
	'2023-05-20',
	'2023-05-20',
	'Elena',
	'Ceccato',
	'elenaceccato@gmail.com',
	'Unknown',
	'EC',
	'Unknown',
	'elenaceccato.com',
	'Ozono',
	'1000',
	'Ettore',
	),

]




conn = sqlite3.connect(database_name)
c = conn.cursor()

c.execute('''
	create table if not exists clients (
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

# DEMO ADD FAKE DATA
# for record in data:
# 	c.execute('insert into clients values (:status, :date_first_added, :date_last_updated, :first_name, :last_name, :email, :phone, :business_name, :business_address, :website, :sector, :gil, :salesman)',
# 		{
# 			'status': record[1],
# 			'date_first_added': record[2],
# 			'date_last_updated': record[3],
# 			'first_name': record[4],
# 			'last_name': record[5],
# 			'email': record[6],
# 			'phone': record[7],
# 			'business_name': record[8],
# 			'business_address': record[9],
# 			'website': record[10],
# 			'sector': record[11],
# 			'gil': record[12],
# 			'salesman': record[13],
# 		}
# 	)

conn.commit()
conn.close()



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

frame_fields = LabelFrame(root, text='Fields', padx=20, pady=10)
frame_fields.pack(side=LEFT, fill=Y)

labels = []
entries = []
for i, field in enumerate(fields):
	labels.append(Label(frame_fields, text=field).grid(row=i, column=0, sticky=W))
	tmp_entry = Entry(frame_fields)
	tmp_entry.grid(row=i, column=1, sticky=W)
	entries.append(tmp_entry)
i += 1

def select_record(e):
	selected = tree.focus()
	values = tree.item(selected, 'values')

	for k, entry in enumerate(entries):
		entry.delete(0, END)
		entry.insert(0, values[k])

def clear_entries():
	for i, entry in enumerate(entries[1:]):
		entry.delete(0, END)

def remove_one():
	x = tree.selection()[0]
	tree.delete(x)

	conn = sqlite3.connect('database.db')
	c = conn.cursor()

	id = entries[0].get()

	c.execute(f'delete from clients where oid={id}')
	
	conn.commit()
	conn.close()


def update_record():
	entries_vals = [entry.get() for entry in entries]

	selected = tree.focus()
	tree.item(selected, text='', values=entries_vals)

	for i, entry in enumerate(entries[1:]):
		entry.delete(0, END)

	conn = sqlite3.connect(database_name)
	c = conn.cursor()

	data = entries_vals[1:]
	data.append(entries_vals[0])

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



clear_button = Button(frame_fields, text='Clear', command=clear_entries)
clear_button.grid(row=i, column=0, sticky=W)
i += 1

remove_button = Button(frame_fields, text='Remove', command=remove_one)
remove_button.grid(row=i, column=0, sticky=W)
i += 1

update_button = Button(frame_fields, text='Update', command=update_record)
update_button.grid(row=i, column=0, sticky=W)
i += 1



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

# tree.column('First Name', width=80, anchor=W)
# tree.column('Last Name', width=80, anchor=W)
# tree.column('Email', width=80, anchor=W)

# tree.heading('First Name', text='First Name', anchor=W)
# tree.heading('Last Name',  text='Last Name', anchor=W)
# tree.heading('Email', text='Email', anchor=W)

# for index, record in enumerate(data):
# 	tree.insert(parent='', index=index, iid=index, text='', values=record)



def query_database():
	conn = sqlite3.connect(database_name)
	c = conn.cursor()

	c.execute('select rowid, * from clients')
	records = c.fetchall()
	for record in records:
		print(record)
	
	for index, record in enumerate(records):
		tree.insert(parent='', index=index, iid=index, text='', values=record)

	conn.commit()
	conn.close()

query_database()


tree.bind('<ButtonRelease-1>', select_record)







# ADD
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

		for i, entry in enumerate(add_entries):
			entry.delete(0, END)

		tree.delete(*tree.get_children())
		query_database()

	curr_add_button = Button(add_frame, text='Add', command=add_client_db)
	curr_add_button.grid(row=i, column=0, sticky=W)



add_button = Button(frame_fields, text='Add', command=add_client)
add_button.grid(row=i, column=0, sticky=W)
i += 1


root.mainloop()

