from tkinter import *
from tkinter import ttk, filedialog
from datetime import datetime, timedelta
import sqlite3
import csv
import os

import subprocess
from fpdf import FPDF


text_size = 12

class PDF(FPDF):
	def header(self):
		self.image('logo.jpg', 10, 8, 50)
		self.set_font('helvetica', 'B', text_size)

		self.cell(130, 10)
		self.cell(0, 10, 'Offerta #M11-23', ln=1)

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
    pdf = PDF('P', 'mm', 'Letter')
    pdf.add_font("Arial", "", "./fonts/arial.ttf", uni=True)
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_page()


    cell_height = 6
    pdf.set_font('helvetica', '', text_size)
    pdf.set_fill_color(255, 255, 255)

    pdf.cell(0, cell_height, 'Ozonogroup s.r.l.', fill=True, ln=1)
    pdf.cell(0, cell_height, 'Via dell\'Artigianato, 23 - 31011 Asolo (TV) Italia', fill=True, ln=1)
    pdf.cell(0, cell_height, 'P.IVA/C.F.: 86334519757', fill=True, ln=1)
    pdf.ln(5)

    pdf.cell(100, cell_height, 'Cliente:', border='B', fill=True, ln=1)
    pdf.ln(2)
    business_name = entries[10].get()
    business_address = entries[11].get()
    pdf.cell(0, cell_height, business_name, fill=True, ln=1)
    pdf.cell(0, cell_height, business_address, fill=True, ln=1)
    pdf.cell(0, cell_height, 'P.IVA/C.F.: 86334519757', fill=True, ln=1)
    pdf.ln(10)

    cell_height = 8
    pdf.set_font('helvetica', 'B', text_size)
    pdf.set_fill_color(229, 229, 229)

    cell_width_numdoc = 25
    cell_width_data = 25

    cell_height = 8
    pdf.set_font('helvetica', 'B', text_size)
    pdf.set_fill_color(229, 229, 229)

    cell_width_codice = 20
    cell_width_description = 80
    cell_width_um = 15
    cell_width_qta = 15
    cell_width_valuta = 20
    cell_width_valunit = 15
    cell_width_prezzo = 30
    cell_width_sconti = 20
    cell_width_totale = 30

    pdf.cell(cell_width_qta, cell_height, 'Q.tà', border=1, fill=True)
    pdf.cell(cell_width_codice, cell_height, 'Codice', border=1, fill=True)
    pdf.cell(cell_width_description, cell_height, 'Descrizione', border=1, fill=True)
    pdf.cell(cell_width_prezzo, cell_height, 'Prezzo', border=1, fill=True)
    pdf.cell(cell_width_sconti, cell_height, 'Sconto', border=1, fill=True)
    pdf.cell(cell_width_totale, cell_height, 'Subtotale', border=1, fill=True)
    pdf.ln()

    pdf.set_font('helvetica', '', text_size)
    pdf.set_fill_color(255, 255, 255)

    price_num = 24810
    discount_num = 15
    subtotal_num = price_num - price_num * (discount_num/100)

    price_str = '€ ' + str(price_num)
    discount_str = str(discount_num) + "%"
    subtotal_str = '€ ' + str(subtotal_num)

    pdf.cell(cell_width_qta, cell_height, '1', border=1, fill=True)
    pdf.cell(cell_width_codice, cell_height, '0001', border=1, fill=True)
    pdf.cell(cell_width_description, cell_height, 'GreenOzone V2 15/30', border=1, fill=True)
    pdf.cell(cell_width_prezzo, cell_height, price_str, border=1, fill=True)
    pdf.cell(cell_width_sconti, cell_height, discount_str, border=1, fill=True)
    pdf.cell(cell_width_totale, cell_height, subtotal_str, border=1, fill=True)
    pdf.ln(cell_height)


    price_num = 120
    discount_num = 100
    subtotal_num = price_num - price_num * (discount_num/100)

    price_str = '€ ' + str(price_num)
    discount_str = str(discount_num) + "%"
    if subtotal_num == 0: subtotal_str = 'gratis'
    else: subtotal_str = '€ ' + str(subtotal_num)

    pdf.cell(cell_width_qta, cell_height, '1', border=1, fill=True)
    pdf.cell(cell_width_codice, cell_height, '0002', border=1, fill=True)
    pdf.cell(cell_width_description, cell_height, 'Trasporto', border=1, fill=True)
    pdf.cell(cell_width_prezzo, cell_height, price_str, border=1, fill=True)
    pdf.cell(cell_width_sconti, cell_height, discount_str, border=1, fill=True)
    pdf.cell(cell_width_totale, cell_height, subtotal_str, border=1, fill=True)
    pdf.ln(cell_height)


    price_num = 480
    discount_num = 100
    subtotal_num = price_num - price_num * (discount_num/100)

    price_str = '€ ' + str(price_num)
    discount_str = str(discount_num) + "%"
    if subtotal_num == 0: subtotal_str = 'gratis'
    else: subtotal_str = '€ ' + str(subtotal_num)

    pdf.cell(cell_width_qta, cell_height, '1', border=1, fill=True)
    pdf.cell(cell_width_codice, cell_height, '0003', border=1, fill=True)
    pdf.cell(cell_width_description, cell_height, 'Installazione', border=1, fill=True)
    pdf.cell(cell_width_prezzo, cell_height, price_str, border=1, fill=True)
    pdf.cell(cell_width_sconti, cell_height, discount_str, border=1, fill=True)
    pdf.cell(cell_width_totale, cell_height, subtotal_str, border=1, fill=True)
    pdf.ln(cell_height + 3)

    price_num = 24810
    discount_num = 15
    subtotal_num = price_num - price_num * (discount_num/100)
    print(subtotal_num)

    price_str = '€ ' + str(price_num)
    discount_str = str(discount_num) + "%"
    if subtotal_num == 0: subtotal_str = 'gratis'
    else: subtotal_str = '€ ' + str(subtotal_num)

    pdf.cell(140, cell_height, '')
    pdf.set_font('helvetica', 'B', text_size)
    pdf.cell(25, cell_height, 'Subtotale: ', align='R')
    pdf.set_font('helvetica', '', text_size)
    pdf.cell(25, cell_height, subtotal_str)
    pdf.ln(cell_height)

    iva_perc = 22
    iva_num = price_num * (22/100)
    iva_str = '€ ' + str(iva_num) + f' ({iva_perc}%)'

    pdf.cell(140, cell_height, '')
    pdf.set_font('helvetica', 'B', text_size)
    pdf.cell(25, cell_height, 'IVA: ', align='R')
    pdf.set_font('helvetica', '', text_size)
    pdf.cell(25, cell_height, iva_str)
    pdf.ln(cell_height)


    totale_str = '€ ' + str(iva_num + subtotal_num)

    pdf.cell(140, cell_height, '')
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
    pdf.cell(100, cell_height, 'Merce: disponibile in 40/60gg lavorativi', ln=1)
    pdf.cell(100, cell_height, 'Garanzia: 12 mesi', ln=1)
    pdf.cell(100, cell_height, "Pagamento: 50% all'ordine, 50% alla consegna", ln=1)


    pdf.ln(10)

    pdf.set_font('helvetica', '', 10)
    cell_height = 5
    privacy = 'Privacy L. 675 del 31.12.96 : Si informa che i dati a voi relativi e riportati nel presente documento vengono trattati in base alle esigenze contrattuali ed i conseguenti adempimenti degli obblighi fiscali e contabili. Con tale avviso ci riteniamo esonerati da eventuali responsabilità.'

    pdf.multi_cell(0, cell_height, privacy)


    pdf.output('report.pdf')

    subprocess.Popen('report.pdf', shell=True)


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

database_name = 'database.db'


def tk_clients_tree_refresh(rows):
	tree.delete(*tree.get_children())
	for index, row in enumerate(rows):
		tree.insert(parent='', index=index, iid=index, text='', values=row, tags=(row[1],))

root = Tk()
root.title('Ozonogroup CRM')
root.iconbitmap('logo.ico')
root.geometry('800x600')
root.state('zoomed')

# CREATE FIELDS
frame_fields = LabelFrame(root, text='Client Info', padx=20, pady=10)
frame_fields.pack(side=LEFT, fill=Y)

labels = []
entries = []

i = 0
# client_info_title_label = Label(frame_fields, text="Client Info")
# client_info_title_label.grid(row=i, column=0, sticky=W)
# i += 1
for field in clients_fields:
    labels.append(Label(frame_fields, text=field).grid(row=i, column=0, sticky=W))
    tmp_entry = Entry(frame_fields, width=50)
    if field == 'id':
        tmp_entry.insert(0, '-')
        tmp_entry.config(state='readonly')
    tmp_entry.grid(row=i, column=1, sticky=W)
    entries.append(tmp_entry)
    i += 1
pdf_button = Button(frame_fields, text='Generate PDF', command=generate_pdf)
pdf_button.grid(row=i, column=1, sticky=W)
i += 1

def db_client_get_by_business_name(business_name):
	conn = sqlite3.connect(database_name)
	c = conn.cursor()
	c.execute(f'select * from clients where business_name="{business_name}"')
	records = c.fetchall()[0]
	conn.commit()
	conn.close()
	return records

row = db_client_get_by_business_name('San Nicola Prosciuttificio del Sole S.p.A.')
print(row)

for k, entry in enumerate(entries):
    entry.delete(0, END)
    entry.insert(0, row[k])


# SIZING
frame_sizing = LabelFrame(root, text='Sizing', padx=20, pady=10)
frame_sizing.pack(side=LEFT, fill=Y)

m3_var = StringVar()
m3_var.trace("w", lambda name, index, mode, var=m3_var: calc_command())
ppm_var = StringVar()
ppm_var.trace("w", lambda name, index, mode, var=ppm_var: calc_command())

i = 0
m3_label = Label(frame_sizing, text='cubic meters   ')
m3_label.grid(row=i, column=0, sticky=W)
m3_entry = Entry(frame_sizing, width=50, textvariable=m3_var)
m3_entry.grid(row=i, column=1, sticky=W)
i += 1
# mg_label = Label(frame_sizing, text='ozone mg   ')
# mg_label.grid(row=i, column=0, sticky=W)
# mg_entry = Entry(frame_sizing, width=50)
# mg_entry.grid(row=i, column=1, sticky=W)
# i += 1
# minutes_label = Label(frame_sizing, text='tempo accensione (minuti)   ')
# minutes_label.grid(row=i, column=0, sticky=W)
# minutes_entry = Entry(frame_sizing, width=50)
# minutes_entry.grid(row=i, column=1, sticky=W)
# i += 1
ppm_label = Label(frame_sizing, text='ppm   ')
ppm_label.grid(row=i, column=0, sticky=W)
ppm_entry = Entry(frame_sizing, width=50, textvariable=ppm_var)
ppm_entry.grid(row=i, column=1, sticky=W)
i += 1
res_label = Label(frame_sizing, text='res (mg)   ')
res_label.grid(row=i, column=0, sticky=W)
res_entry = Entry(frame_sizing, width=50)
res_entry.grid(row=i, column=1, sticky=W)
i += 1


def callback():
   content = var.get()
   print(content)
#    Label(win, text=content).pack()




def calc_command():
    m3 = int(m3_entry.get())
    ppm = int(ppm_entry.get())
    # mg = int(mg_entry.get())
    # minutes = int(minutes_entry.get())

    # ppm = mg / m3

    mg = 2.14 * m3 * ppm

    res_entry.delete(0, END)
    res_entry.insert(0, mg)


# calc_button = Button(frame_sizing, text='Calc', command=calc_command)
# calc_button.grid(row=i, column=1, sticky=W)
# i += 1

root.mainloop()
