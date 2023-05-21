from tkinter import *
from PIL import ImageTk, Image
import sqlite3
import csv

root = Tk()
root.title("Ozonogroup CRM")
root.iconbitmap('./logo.ico')
root.geometry('400x400')

# DROP TABLE "DEBUG"
# conn = sqlite3.connect('database.db')
# c = conn.cursor()
# c.execute('DROP TABLE if exists clients')
# conn.commit()
# conn.close()

# CREATE TABLE
conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''
	create table if not exists clients (
		status text,
		date_first_added text,
		date_last_updated text,
		first_name text,
		last_name text,
		business_name text,
		business_address text,
		website text,
		phone text,
		email text,
		munny integer,
		sector text
	)''')
conn.commit()
conn.close()

# SHOW TABLES
conn = sqlite3.connect('database.db')
c  = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(c.fetchall())
conn.commit()
conn.close()

# ALTER TABLE
# conn = sqlite3.connect('database.db')
# c  = conn.cursor()
# c.execute('''ALTER TABLE clients ADD sector text''')
# conn.commit()
# conn.close()


title_label = Label(root, text='customer database', font=('Helvetica', 16))
title_label.grid(row=0, column=0, columnspan=2, pady=10)

first_name_label = Label(root, text='First Name').grid(row=1, column=0, sticky=W, padx=10)
last_name_label = Label(root, text='Last Name').grid(row=2, column=0, sticky=W, padx=10)

first_name_box = Entry(root)
first_name_box.grid(row=1, column=1)
last_name_box = Entry(root)
last_name_box.grid(row=2, column=1)

def add_customer():	
	conn = sqlite3.connect('database.db')
	c  = conn.cursor()
	c.execute('insert into clients values (:status, :date_first_added, :date_last_updated, :first_name, :last_name, :business_name, :business_address, :website, :phone, :email, :munny, :sector)',
		{
			'status': 'gray',
			'date_first_added': '2022/09/11', 
			'date_last_updated': '2022/11/15', 
			'first_name': first_name_box.get(), 
			'last_name': last_name_box.get(), 
			'business_name': '', 
			'business_address': '',
			'website': '',
			'phone': '',
			'email': '',
			'munny': 0,
			'sector': '',
		}
	)
	conn.commit()
	conn.close()

	clear_fields()
	
	conn = sqlite3.connect('database.db')
	c  = conn.cursor()
	c.execute('''select * from clients''')
	for x in c.fetchall():
		print(x)
	conn.commit()
	conn.close()

def clear_fields():
	first_name_box.delete(0, END)
	last_name_box.delete(0, END)

def list_customers():
	list_customers_query = Tk()
	list_customers_query.title('List All Customers')
	list_customers_query.iconbitmap('./logo.ico')
	list_customers_query.geometry('800x600')

	conn = sqlite3.connect('database.db')
	c  = conn.cursor()
	c.execute('''select * from clients''')
	result = c.fetchall()
	for i, x in enumerate(result):
		for k, y in enumerate(x):
			lookup_label = Label(list_customers_query, text=y)
			lookup_label.grid(row=i, column=k)
	conn.commit()
	conn.close()

	csv_button = Button(list_customers_query, text="save to excel", command=lambda: write_to_csv(result))
	csv_button.grid(row=i+1, column=0)

def write_to_csv(result):
		with open('costomers.csv', 'a') as f:
			w = csv.writer(f)
			w.writerow(result)

def cmd_search():
	name = search_entry.get()
	conn = sqlite3.connect('database.db')
	c  = conn.cursor()
	c.execute("SELECT * FROM clients WHERE first_name=?", (name,))
	results = c.fetchall()
	print(results)
	conn.commit()
	conn.close()


add_customer_button = Button(root, text='Add Customer', command=add_customer)
add_customer_button.grid(row=3, column=0, padx=10, pady=10)
clear_customer_button = Button(root, text='Clear Fields', command=clear_fields)
clear_customer_button.grid(row=3, column=1, padx=10, pady=10)

list_customers_button = Button(root, text='List Customers', command=list_customers)
list_customers_button.grid(row=15, column=0, sticky=W, padx=10)

search_label = Label(root, text='Search Name')
search_label.grid(row=16, column=0, padx=10, pady=10)
search_entry = Entry(root)
search_entry.grid(row=16, column=1, padx=10, pady=10)
search_button = Button(root, text='Search', command=cmd_search)
search_button.grid(row=17, column=0, sticky=W, padx=10)


root.mainloop()