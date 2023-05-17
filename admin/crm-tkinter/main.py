from tkinter import *
from PIL import ImageTk, Image
import sqlite3

root = Tk()
root.title("Ozonogroup CRM")
root.iconbitmap('./logo.ico')
root.geometry('400x400')

# DROP TABLE "DEBUG"
conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('DROP TABLE if exists clients')
conn.commit()
conn.close()

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
		munny integer
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

quit()

root.mainloop()