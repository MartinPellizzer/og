from tkinter import *
from tkinter import ttk
from datetime import datetime

root = Tk()
root.title('Treeview demo')
root.geometry('800x600')

fields = [
	'status',
	'date_first_added',
	'data_last_updated',
	'first_name',
	'last_name',
	'email',
	'phone',
	'business_name',
	'business_address',
	'website',
	'sector',
	'gil',
]

frame_fields = LabelFrame(root, text='Fields', padx=20, pady=10)
frame_fields.pack(side=LEFT, fill=Y)

labels = []
entries = []
for i, field in enumerate(fields):
	labels.append(Label(frame_fields, text=field).grid(row=i, column=0, sticky=W))
	tmp_entry = Entry(frame_fields)
	tmp_entry.grid(row=i, column=1, sticky=W)
	if field == 'date_first_added':
		tmp_entry.insert(0, datetime.now().date())
	entries.append(tmp_entry)
i += 1

def get_list_item():
	selected = tree.focus()
	values = tree.item(selected, 'values')

	for i, entry in enumerate(entries):
		entry.delete(0, END)
		entry.insert(0, values[i])

btn = Button(frame_fields, text='Get', command=get_list_item)
btn.grid(row=i, column=0, sticky=W)





data = [
	('0',
	'2023/05/19',
	'2023/05/19',
	'Martin',
	'Pellizzer',
	'martinpellizeer@gmail.com',
	'3209624740',
	'MP',
	'Via Cornere, 13',
	'martinpellizzer.com',
	'Ozono',
	'0',),
	('1',
	'2023/05/20',
	'2023/05/20',
	'Elena',
	'Ceccato',
	'elenaceccato@gmail.com',
	'Unknown',
	'EC',
	'Unknown',
	'elenaceccato.com',
	'Ozono',
	'1000',),

]

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

tree.insert(parent='', index='0', iid=0, text='', values=data[0])
tree.insert(parent='', index='1', iid=1, text='', values=data[1])






root.mainloop()

