import tkinter as tk
from tkinter import ttk

import util


products_rows = util.csv_get_rows('products.csv')
products_cols = util.csv_get_cols(products_rows)
products_rows = products_rows[1:]

def func(value):
    product_row = util.csv_get_rows_by_col_val('products.csv', products_cols['name'], value)[0]
    product_quantity = product_row[products_cols['quantity']]
    quantity_label['text'] = f'Quantity: {product_quantity}'
    print(product_row)


products_names = [row[products_cols['name']] for row in products_rows]

window = tk.Tk()
window.title('Ozonogroup Store')
window.geometry('600x800')

choices = ('network one', 'network two', 'network three')
var = tk.StringVar(window)
var.set("Select an Option") 
network_select = tk.OptionMenu(window, var, *products_names, command=func)
network_select.pack()   

quantity_label = tk.Label(window, text="Quantity: ")
quantity_label.pack()
# var.trace("w", callback)

window.mainloop()