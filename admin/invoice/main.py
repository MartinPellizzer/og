from tkinter import *
from tkinter import ttk, filedialog
from datetime import datetime, timedelta
import csv

import subprocess
from fpdf import FPDF
import locale

from pdf2image import convert_from_path
from PIL import ImageTk, Image




locale.setlocale( locale.LC_ALL, '' )

db_clients_fields = {
	'invoice_number': "text",
	'business_name': "text",
	'business_address_1': "text",
	'business_address_2': "text",
	'business_iva': "text",
}

clients_fields = [f'{f}' for f in db_clients_fields]

def get_products():
    with open('products.csv', "r") as f:
        reader = csv.reader(f, delimiter=",")
        products = [product for product in reader]
        products = products[1:]
    return products

text_size = 12


class PDF(FPDF):
    def header(self):
        invoice_number = invoice_client_entries[0].get()
        self.image('logo.jpg', 10, 8, 50)
        self.set_font('helvetica', 'B', text_size)

        self.cell(130, 10)
        self.cell(0, 10, f'Offerta #{invoice_number}', ln=1)

        self.set_font('helvetica', '', text_size)
        self.cell(130, 10)
        day = datetime.now().day
        if day < 10: day = '0' + str(day)
        month = datetime.now().month
        if month < 10: month = '0' + str(month)
        year = datetime.now().year
        self.cell(0, 6, f'Data: {day}/{month}/{year}', border=0, ln=1)
        self.cell(130, 10)
        end_date = datetime.now().date() + timedelta(days=30)
        
        day = end_date.day
        if day < 10: day = '0' + str(day)
        month = end_date.month
        if month < 10: month = '0' + str(month)
        year = end_date.year

        self.cell(0, 6, f'Valido fino a: {day}/{month}/{year}', border=0, ln=1)
        self.ln(15)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 10)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')


def generate_pdf():
    rows = []
    for child in invoice_tree.get_children():
        rows.append(invoice_tree.item(child)["values"])
        print(invoice_tree.item(child)["values"])

    business_name = invoice_client_entries[1].get()
    business_address_1 = invoice_client_entries[2].get()
    business_address_2 = invoice_client_entries[3].get()
    business_iva = invoice_client_entries[4].get()

    pdf = PDF('P', 'mm', 'Letter')
    pdf.add_font("Arial", "", "./fonts/arial.ttf", uni=True)
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_page()

    cell_height = 6
    cell_width = 90
    cell_width_divider = 10

    pdf.set_font('helvetica', '', text_size)
    pdf.set_fill_color(255, 255, 255)

    pdf.cell(cell_width, cell_height, 'Fornitore:', border='B', fill=True)
    pdf.cell(cell_width_divider, cell_height, '', fill=True)
    pdf.cell(cell_width, cell_height, 'Cliente:', border='B', fill=True, ln=1)
    pdf.ln(2)

    pdf.cell(cell_width, cell_height, 'Ozonogroup s.r.l.', fill=True)
    pdf.cell(cell_width_divider, cell_height, '', fill=True)
    pdf.cell(cell_width, cell_height, business_name, fill=True, ln=1)

    # address = business_address.split(',')
    # address_1 = address[:2]
    # address_2 = address[2:]

    pdf.cell(cell_width, cell_height, 'Via dell\'Artigianato, 23', fill=True)
    pdf.cell(cell_width_divider, cell_height, '', fill=True)
    pdf.cell(cell_width, cell_height, business_address_1, fill=True, ln=1)

    pdf.cell(cell_width, cell_height, '31011 Asolo TV', fill=True)
    pdf.cell(cell_width_divider, cell_height, '', fill=True)
    pdf.cell(cell_width, cell_height, business_address_2, fill=True, ln=1)
    
    pdf.cell(cell_width, cell_height, 'P.IVA/C.F.: 86334519757', fill=True)
    pdf.cell(cell_width_divider, cell_height, '', fill=True)
    pdf.cell(cell_width, cell_height, f'P.IVA/C.F.: {business_iva}', fill=True, ln=1)
    pdf.ln(10)

    cell_height = 8
    pdf.set_font('helvetica', 'B', text_size)
    pdf.set_fill_color(229, 229, 229)

    cell_width_numdoc = 25
    cell_width_data = 25

    cell_height = 8
    pdf.set_font('helvetica', 'B', text_size)
    pdf.set_fill_color(229, 229, 229)

    cell_width_codice = 35
    cell_width_description = 60
    cell_width_um = 15
    cell_width_qta = 15
    cell_width_valuta = 20
    cell_width_valunit = 15
    cell_width_prezzo = 30
    cell_width_sconti = 20
    cell_width_totale = 35

    pdf.cell(cell_width_qta, cell_height, 'Q.tà', border=1, fill=True)
    pdf.cell(cell_width_codice, cell_height, 'Codice', border=1, fill=True)
    pdf.cell(cell_width_description, cell_height, 'Descrizione', border=1, fill=True)
    pdf.cell(cell_width_prezzo, cell_height, 'Prezzo', border=1, fill=True)
    pdf.cell(cell_width_sconti, cell_height, 'Sconto', border=1, fill=True)
    pdf.cell(cell_width_totale, cell_height, 'Subtotale', border=1, fill=True)
    pdf.ln()

    pdf.set_font('helvetica', '', text_size)
    pdf.set_fill_color(255, 255, 255)

    price_total_num = 0
    discount_total_num = 0

    for row in rows:
        row_code_str = str(row[0])
        row_desc_str = str(row[1])
        price_num = row[2]
        discount_num = row[3]
        subtotal_num = price_num - price_num * (discount_num/100)

        price_total_num += price_num
        discount_total_num += price_num * (discount_num/100)

        # price_str = '€ ' + str(price_num)
        discount_str = str(discount_num) + "%"
        if discount_num == 100:
            subtotal_str = 'gratis'
        else:
            subtotal_str = locale.currency(subtotal_num, grouping=True)

        price_str = locale.currency(price_num, grouping=True)

        pdf.cell(cell_width_qta, cell_height, '1', border=1, fill=True)
        pdf.cell(cell_width_codice, cell_height, row_code_str, border=1, fill=True)
        pdf.cell(cell_width_description, cell_height, row_desc_str, border=1, fill=True)
        pdf.cell(cell_width_prezzo, cell_height, price_str, border=1, fill=True)
        pdf.cell(cell_width_sconti, cell_height, discount_str, border=1, fill=True)
        pdf.cell(cell_width_totale, cell_height, subtotal_str, border=1, fill=True)
        pdf.ln(cell_height)

    pdf.ln(3)
    
    subtotal_str = locale.currency(price_total_num, grouping=True)

    margin_left = 135

    pdf.cell(margin_left, cell_height, '')
    pdf.set_font('helvetica', 'B', text_size)
    pdf.cell(25, cell_height, 'Totale Prezzo: ', align='R')
    pdf.set_font('helvetica', '', text_size)
    pdf.cell(25, cell_height, subtotal_str)
    pdf.ln(cell_height)

    discount_total_str = locale.currency(discount_total_num, grouping=True)

    pdf.cell(margin_left, cell_height, '')
    pdf.set_font('helvetica', 'B', text_size)
    pdf.cell(25, cell_height, 'Totale Sconto: ', align='R')
    pdf.set_font('helvetica', '', text_size)
    pdf.cell(25, cell_height, discount_total_str)
    pdf.ln(cell_height)

    iva_perc = 22
    iva_num = (price_total_num - discount_total_num) * (22/100)
    iva_str = locale.currency(iva_num, grouping=True) + f' ({iva_perc}%)'

    pdf.cell(margin_left, cell_height, '')
    pdf.set_font('helvetica', 'B', text_size)
    pdf.cell(25, cell_height, 'IVA: ', align='R')
    pdf.set_font('helvetica', '', text_size)
    pdf.cell(25, cell_height, iva_str)
    pdf.ln(cell_height)

    totale_str = locale.currency(iva_num + price_total_num - discount_total_num, grouping=True)

    pdf.cell(margin_left, cell_height, '')
    pdf.set_font('helvetica', 'B', text_size)
    pdf.cell(25, cell_height, 'Totale: ', align='R')
    pdf.set_font('helvetica', '', text_size)
    pdf.cell(25, cell_height, totale_str)
    pdf.ln(cell_height)
    pdf.ln(10)

    cell_height = 6

    pdf.set_font('helvetica', 'B', text_size)
    pdf.cell(130, cell_height, 'Condizioni di fornitura')
    pdf.cell(100, cell_height, 'Timbro e firma per accettazione', ln=1)
    pdf.set_font('helvetica', '', text_size)
    pdf.cell(100, cell_height, 'Merce: da pronta a 40gg lavorativi', ln=1)
    pdf.cell(100, cell_height, 'Garanzia: 12 mesi', ln=1)
    pdf.cell(100, cell_height, "Pagamento: 50% all'ordine, 50% alla consegna", ln=1)

    pdf.ln(20)

    pdf.set_font('helvetica', '', 10)
    cell_height = 5
    privacy = 'Privacy L. 675 del 31.12.96 : Si informa che i dati a voi relativi e riportati nel presente documento vengono trattati in base alle esigenze contrattuali ed i conseguenti adempimenti degli obblighi fiscali e contabili. Con tale avviso ci riteniamo esonerati da eventuali responsabilità.'

    pdf.multi_cell(0, cell_height, privacy)

    pdf.output('report.pdf')


invoice_window = Tk()
invoice_window.title('Ozonogroup CRM')
invoice_window.iconbitmap('logo.ico')
invoice_window.geometry('1700x600')
invoice_window.grab_set()
invoice_window.state('zoomed')

# MAIN FRAME

invoice_data_frame = LabelFrame(invoice_window, text='Data', padx=20, pady=10)
invoice_data_frame.pack(side=LEFT, fill=Y)

tree_frame = LabelFrame(invoice_window, text='Add Service', padx=20, pady=20)
tree_frame.pack(side=LEFT, fill=BOTH, expand=True)

invoice_pdf_frame = LabelFrame(invoice_window, text='Pdf', padx=20, pady=10)
invoice_pdf_frame.pack(side=LEFT, fill=Y)



# PREVIEW FRAME
preview_width = int(210*3)
preview_height = int(297*3)


invoice_preview_frame = Frame(invoice_pdf_frame)
invoice_preview_frame.pack(side=TOP, fill=Y)

image = Image.open("report.png")
image = image.resize((preview_width, preview_height), Image.ANTIALIAS)
my_image = ImageTk.PhotoImage(image)

invoice_preview_label = Label(invoice_preview_frame, text="label1", image=my_image)
invoice_preview_label.pack()

pages = convert_from_path('report.pdf')
for page in pages:
    page.save("report.png")

image = Image.open("report.png")
image = image.resize((preview_width, preview_height), Image.ANTIALIAS)
my_image = ImageTk.PhotoImage(image)

invoice_preview_label.config(image=my_image)

invoice_preview_actions_frame = Frame(invoice_pdf_frame, padx=20, pady=10)
invoice_preview_actions_frame.pack(side=TOP, fill=Y)




def preview_command():
    generate_pdf()
    
    pages = convert_from_path('report.pdf')
    for page in pages:
        page.save("report.png")

    image = Image.open("report.png")
    image = image.resize((preview_width, preview_height), Image.ANTIALIAS)
    my_image = ImageTk.PhotoImage(image)

    invoice_preview_label.config(image=my_image)


def view_command():
    preview_command()
    subprocess.Popen('report.pdf', shell=True)


preview_button = Button(invoice_preview_actions_frame, text='Preview', command=preview_command)
preview_button.pack(side=LEFT, fill=Y)

view_button = Button(invoice_preview_actions_frame, text='View', command=view_command)
view_button.pack(side=LEFT, fill=Y)


# DATA FRAME -------------------------------------------------------


frame_fields = LabelFrame(invoice_data_frame, text='Client Info', padx=20, pady=10)
frame_fields.pack(side=TOP, fill=Y)


# CLIENT FIELDS
entry_width = 40
invoice_client_labels = []
invoice_client_entries = []
i = 0
for field in clients_fields:
    invoice_client_labels.append(Label(frame_fields, text=field).grid(row=i, column=0, sticky=W))
    tmp_entry = Entry(frame_fields, width=entry_width)
    tmp_entry.grid(row=i, column=1, sticky=W)
    invoice_client_entries.append(tmp_entry)
    i += 1





# # CALCULATOR FRAME
# frame_sizing = LabelFrame(invoice_window, text='Sizing', padx=20, pady=10)
# frame_sizing.pack(side=LEFT, fill=Y)

# # CALCULATOR FIELDS
# m3_var = StringVar()
# m3_var.trace("w", lambda name, index, mode, var=m3_var: calc_command())
# ppm_var = StringVar()
# ppm_var.trace("w", lambda name, index, mode, var=ppm_var: calc_command())
# oxy_var = StringVar()
# oxy_var.trace("w", lambda name, index, mode, var=oxy_var: calc_command())
# mul_var = StringVar()
# mul_var.trace("w", lambda name, index, mode, var=mul_var: calc_command())

# entry_width = 20 

# i = 0
# m3_label = Label(frame_sizing, text='cubic meters   ')
# m3_label.grid(row=i, column=0, sticky=W)
# m3_entry = Entry(frame_sizing, width=entry_width, textvariable=m3_var)
# m3_entry.grid(row=i, column=1, sticky=W)
# i += 1
# ppm_label = Label(frame_sizing, text='ppm target  ')
# ppm_label.grid(row=i, column=0, sticky=W)
# ppm_entry = Entry(frame_sizing, width=entry_width, textvariable=ppm_var)
# ppm_entry.grid(row=i, column=1, sticky=W)
# i += 1
# oxy_label = Label(frame_sizing, text='feeding oxygen %   ')
# oxy_label.grid(row=i, column=0, sticky=W)
# oxy_entry = Entry(frame_sizing, width=entry_width, textvariable=oxy_var)
# oxy_entry.grid(row=i, column=1, sticky=W)
# i += 1
# mul_label = Label(frame_sizing, text='adjusting multiplier   ')
# mul_label.grid(row=i, column=0, sticky=W)
# mul_entry = Entry(frame_sizing, width=entry_width, textvariable=mul_var)
# mul_entry.grid(row=i, column=1, sticky=W)
# i += 1
# res_label = Label(frame_sizing, text='result (mg)   ')
# res_label.grid(row=i, column=0, sticky=W)
# res_entry = Entry(frame_sizing, width=entry_width)
# res_entry.grid(row=i, column=1, sticky=W)
# i += 1

# def calc_mg():
#     m3 = int(m3_entry.get())
#     ppm = int(ppm_entry.get())
#     oxy = int(oxy_entry.get())
#     mul = int(mul_entry.get())
#     mg = 2.14 * m3 * ppm / (oxy / 100) * mul
#     res_entry.delete(0, END)
#     res_entry.insert(0, mg)

# calc_mg_button = Button(frame_sizing, text='Calc (MG)', command=calc_mg)
# calc_mg_button.grid(row=i, column=1, sticky=W)
# i += 1

# MAIN FRAME ADD ------------------------------------------------
# invoice_product_frame = Frame(invoice_window)
# invoice_product_frame.pack(side=LEFT, fill=Y)


# ADD PRODUCT FRAME ---------------------------------------------
invoice_main_product_frame = LabelFrame(invoice_data_frame, text='Add Product', padx=20, pady=10)
invoice_main_product_frame.pack(side=TOP, fill=BOTH)

product_list = [item for item in get_products() if (item[1] == 'Generator')]

def selected_optionmenu(product_var):
    print(product_var)
    product_desc = product_var
    for prod in product_list:
        if product_desc == prod[2]:
            curr_prod = prod

    product_code_entry.delete(0, END)
    product_code_entry.insert(0, curr_prod[0])
    product_desc_entry.delete(0, END)
    product_desc_entry.insert(0, curr_prod[2])
    product_price_entry.delete(0, END)
    product_price_entry.insert(0, curr_prod[3])
    product_discount_entry.delete(0, END)
    product_discount_entry.insert(0, 0)

i = 0

product_list_for_menu = [item[2] for item in product_list]
product_var = StringVar()
product_option = OptionMenu(invoice_main_product_frame, product_var, *product_list_for_menu, command=selected_optionmenu)
product_option.grid(row=i, column=0, sticky=W)
i += 1

product_code_label = Label(invoice_main_product_frame, text='product code   ')
product_code_label.grid(row=i, column=0, sticky=W)
product_code_entry = Entry(invoice_main_product_frame, width=20)
product_code_entry.grid(row=i, column=1, sticky=W)
i += 1

product_desc_label = Label(invoice_main_product_frame, text='product description   ')
product_desc_label.grid(row=i, column=0, sticky=W)
product_desc_entry = Entry(invoice_main_product_frame, width=20)
product_desc_entry.grid(row=i, column=1, sticky=W)
i += 1

product_price_label = Label(invoice_main_product_frame, text='price   ')
product_price_label.grid(row=i, column=0, sticky=W)
product_price_entry = Entry(invoice_main_product_frame, width=20)
product_price_entry.grid(row=i, column=1, sticky=W)
i += 1

product_discount_label = Label(invoice_main_product_frame, text='discount   ')
product_discount_label.grid(row=i, column=0, sticky=W)
product_discount_entry = Entry(invoice_main_product_frame, width=20)
product_discount_entry.grid(row=i, column=1, sticky=W)
i += 1

def tree_add_product():
    product_code = product_code_entry.get()
    product_desc = product_desc_entry.get()
    product_price = product_price_entry.get()
    product_discount = product_discount_entry.get()
    values = [product_code, product_desc, product_price, product_discount]
    invoice_tree.insert(parent='', index='end', text='', values=values)

add_prod_button = Button(invoice_main_product_frame, text='Add Product', command=tree_add_product)
add_prod_button.grid(row=i, column=1, sticky=W)
i += 1


# ADD ACCESSORY FRAME ---------------------------------------------
invoice_accessory_frame = LabelFrame(invoice_data_frame, text='Add Accessory', padx=20, pady=10)
invoice_accessory_frame.pack(side=TOP, fill=BOTH)

accessory_list = [accessory for accessory in get_products() if accessory[1] == 'Accessory']

def accessory_select(accessory_var):
    for row in accessory_list:
        if accessory_var == row[2]:
            accessory_selected = row
            break

    accessory_code_entry.delete(0, END)
    accessory_code_entry.insert(0, accessory_selected[0])
    accessory_desc_entry.delete(0, END)
    accessory_desc_entry.insert(0, accessory_selected[2])
    accessory_price_entry.delete(0, END)
    accessory_price_entry.insert(0, accessory_selected[3])
    accessory_discount_entry.delete(0, END)
    accessory_discount_entry.insert(0, 0)

i = 0
    
accessory_list_for_menu = [accessory[2] for accessory in accessory_list]
accessory_var = StringVar()
accessory_option = OptionMenu(invoice_accessory_frame, accessory_var, *accessory_list_for_menu, command=accessory_select)
accessory_option.grid(row=i, column=0, sticky=W)
i += 1

accessory_code_label = Label(invoice_accessory_frame, text='product code   ')
accessory_code_label.grid(row=i, column=0, sticky=W)
accessory_code_entry = Entry(invoice_accessory_frame, width=20)
accessory_code_entry.grid(row=i, column=1, sticky=W)
i += 1

accessory_desc_label = Label(invoice_accessory_frame, text='product description   ')
accessory_desc_label.grid(row=i, column=0, sticky=W)
accessory_desc_entry = Entry(invoice_accessory_frame, width=20)
accessory_desc_entry.grid(row=i, column=1, sticky=W)
i += 1

accessory_price_label = Label(invoice_accessory_frame, text='price   ')
accessory_price_label.grid(row=i, column=0, sticky=W)
accessory_price_entry = Entry(invoice_accessory_frame, width=20)
accessory_price_entry.grid(row=i, column=1, sticky=W)
i += 1

accessory_discount_label = Label(invoice_accessory_frame, text='discount   ')
accessory_discount_label.grid(row=i, column=0, sticky=W)
accessory_discount_entry = Entry(invoice_accessory_frame, width=20)
accessory_discount_entry.grid(row=i, column=1, sticky=W)
i += 1

def tree_add_accessory():
    item_code = accessory_code_entry.get()
    item_desc = accessory_desc_entry.get()
    item_price = accessory_price_entry.get()
    item_discount = accessory_discount_entry.get()
    values = [item_code, item_desc, item_price, item_discount]
    invoice_tree.insert(parent='', index='end', text='', values=values)

accessory_add_button = Button(invoice_accessory_frame, text='Add Accessory', command=tree_add_accessory)
accessory_add_button.grid(row=i, column=1, sticky=W)
i += 1


# ADD SERVICE FRAME ---------------------------------------------
invoice_service_frame = LabelFrame(invoice_data_frame, text='Add Service', padx=20, pady=10)
invoice_service_frame.pack(side=TOP, fill=BOTH)

service_list = [service for service in get_products() if service[1] == 'Service']

def service_select(service_var):
    for row in service_list:
        if service_var == row[2]:
            service_selected = row
            break

    service_code_entry.delete(0, END)
    service_code_entry.insert(0, service_selected[0])
    service_desc_entry.delete(0, END)
    service_desc_entry.insert(0, service_selected[2])
    service_price_entry.delete(0, END)
    service_price_entry.insert(0, service_selected[3])
    service_discount_entry.delete(0, END)
    service_discount_entry.insert(0, 100)

i = 0
    
service_list_for_menu = [service[2] for service in service_list]
service_var = StringVar()
service_option = OptionMenu(invoice_service_frame, service_var, *service_list_for_menu, command=service_select)
service_option.grid(row=i, column=0, sticky=W)
i += 1

service_code_label = Label(invoice_service_frame, text='product code   ')
service_code_label.grid(row=i, column=0, sticky=W)
service_code_entry = Entry(invoice_service_frame, width=20)
service_code_entry.grid(row=i, column=1, sticky=W)
i += 1

service_desc_label = Label(invoice_service_frame, text='product description   ')
service_desc_label.grid(row=i, column=0, sticky=W)
service_desc_entry = Entry(invoice_service_frame, width=20)
service_desc_entry.grid(row=i, column=1, sticky=W)
i += 1

service_price_label = Label(invoice_service_frame, text='price   ')
service_price_label.grid(row=i, column=0, sticky=W)
service_price_entry = Entry(invoice_service_frame, width=20)
service_price_entry.grid(row=i, column=1, sticky=W)
i += 1

service_discount_label = Label(invoice_service_frame, text='discount   ')
service_discount_label.grid(row=i, column=0, sticky=W)
service_discount_entry = Entry(invoice_service_frame, width=20)
service_discount_entry.grid(row=i, column=1, sticky=W)
i += 1

def tree_add_service():
    item_code = service_code_entry.get()
    item_desc = service_desc_entry.get()
    item_price = service_price_entry.get()
    item_discount = service_discount_entry.get()
    values = [item_code, item_desc, item_price, item_discount]
    invoice_tree.insert(parent='', index='end', text='', values=values)

service_add_button = Button(invoice_service_frame, text='Add Service', command=tree_add_service)
service_add_button.grid(row=i, column=1, sticky=W)
i += 1




# TREE
invoice_tree = ttk.Treeview(tree_frame)
invoice_tree.pack(expand=True, fill=BOTH)
tree_fields = ['product code', 'product description', 'price', 'discount']
invoice_tree['columns'] = tree_fields
invoice_tree.column('#0', width=0, stretch=NO)
invoice_tree.heading('#0', text='', anchor=W)
for field in tree_fields:
    invoice_tree.column(field, width=160, anchor=W)
    invoice_tree.heading(field, text=field, anchor=W)

def invoice_tree_del_row(e):
    selected_items = invoice_tree.selection()        
    for selected_item in selected_items:          
        invoice_tree.delete(selected_item)
    
invoice_tree.bind('x', invoice_tree_del_row)


preview_command()

invoice_window.mainloop()
