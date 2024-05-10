import tkinter as tk
# from tkinter import ttk
import ttkbootstrap as ttk

def calc_ppm():
    mg_x_1ppm_x_1m3 = 2.14
    length = length_entry_val.get()
    depth = depth_entry_val.get()
    height = height_entry_val.get()
    ppm = ppm_entry_val.get()
    minutes = time_entry_val.get()
    oxy_val = oxy_var.get()
    adjuster_val = adjuster_entry_val.get()
    if oxy_val == 0: oxy_mul = 5
    else: oxy_mul = 1

    volume = length * depth * height
    mg = mg_x_1ppm_x_1m3 * volume
    mg = mg * ppm
    mg = mg * (60 / minutes)
    mg = mg * oxy_mul
    mg = mg * adjuster_val
        
    output_string.set(f'Ozono: {mg:.2f} mg')


window = ttk.Window(themename='darkly')
window.title('O3 Calculator')
window.geometry('400x600')

title_label = ttk.Label(master=window, text='O3 CALCULATOR', font='Calibri 24 bold')
title_label.pack()

length_frame = ttk.Frame(master=window)
length_frame.pack(pady=5)
length_label = ttk.Label(master=length_frame, text='Larghezza (m)')
length_label.pack(side='top')
length_entry_val = tk.DoubleVar(value=1.0)
length_entry = ttk.Entry(master=length_frame, textvariable=length_entry_val)
length_entry.pack(side='top', padx=10)

depth_frame = ttk.Frame(master=window)
depth_frame.pack(pady=5)
depth_label = ttk.Label(master=depth_frame, text='Profondità (m)')
depth_label.pack(side='top')
depth_entry_val = tk.DoubleVar(value=1.0)
depth_entry = ttk.Entry(master=depth_frame, textvariable=depth_entry_val)
depth_entry.pack(side='top', padx=10)

height_frame = ttk.Frame(master=window)
height_frame.pack(pady=5)
height_label = ttk.Label(master=height_frame, text='Altezza (m)')
height_label.pack(side='top')
height_entry_val = tk.DoubleVar(value=1.0)
height_entry = ttk.Entry(master=height_frame, textvariable=height_entry_val)
height_entry.pack(side='top', padx=10)

ppm_frame = ttk.Frame(master=window)
ppm_frame.pack(pady=5)
ppm_label = ttk.Label(master=ppm_frame, text='PPM da Raggiungere')
ppm_label.pack(side='top')
ppm_entry_val = tk.DoubleVar(value=1.0)
ppm_entry = ttk.Entry(master=ppm_frame, textvariable=ppm_entry_val)
ppm_entry.pack(side='top', padx=10)

time_frame = ttk.Frame(master=window)
time_frame.pack(pady=5)
time_label = ttk.Label(master=time_frame, text='Minuti Ozono x Ora')
time_label.pack(side='top')
time_entry_val = tk.IntVar(value=60)
time_entry = ttk.Entry(master=time_frame, textvariable=time_entry_val)
time_entry.pack(side='top', padx=10)

adjuster_frame = ttk.Frame(master=window)
adjuster_frame.pack(pady=5)
adjuster_label = ttk.Label(master=adjuster_frame, text='Valore Aggiustamento')
adjuster_label.pack(side='top')
adjuster_entry_val = tk.DoubleVar(value=1.0)
adjuster_entry = ttk.Entry(master=adjuster_frame, textvariable=adjuster_entry_val)
adjuster_entry.pack(side='top', padx=10)

oxy_frame = ttk.Frame(master=window)
oxy_frame.pack(pady=5)
oxy_var = tk.IntVar(value=0)
oxy_checkbox = ttk.Checkbutton(oxy_frame, text='Ossigenatore', command=calc_ppm, variable=oxy_var)
oxy_checkbox.pack()

input_frame = ttk.Frame(master=window)
input_frame.pack(pady=10)

button = ttk.Button(master=input_frame, text='calc mg ozone', command=calc_ppm)
button.pack(side='left')

output_string = tk.StringVar()
output_label = ttk.Label(master=window, text='output', font='Calibri 24', textvariable=output_string)
output_label.pack(pady=5)

title_label = ttk.Label(master=window, text='(1 PPM = 2.14 mg O3 / 1 m3)')
title_label.pack()

calc_ppm()

window.mainloop()