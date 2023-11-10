from PIL import Image, ImageFont, ImageDraw, ImageColor


def resize_image(in_path, out_path, w, h):
    img = Image.open(in_path)

    start_size = img.size
    end_size = (w, h)

    if start_size[0] / end_size [0] < start_size[1] / end_size [1]:
        ratio = start_size[0] / end_size[0]
        new_end_size = (end_size[0], int(start_size[1] / ratio))
    else:
        ratio = start_size[1] / end_size[1]
        new_end_size = (int(start_size[0] / ratio), end_size[1])

    img = img.resize(new_end_size)

    w_crop = new_end_size[0] - end_size[0]
    h_crop = new_end_size[1] - end_size[1]
    
    area = (
        w_crop // 2, 
        h_crop // 2,
        new_end_size[0] - w_crop // 2,
        new_end_size[1] - h_crop // 2
    )
    img = img.crop(area)

    img.save(out_path, format='JPEG', subsampling=0, quality=100)


# def generate_image_template_1(image_path, out_image_path, title, subtitle, lst):
#     # create canvas 
#     img_w = 1024
#     img_h = 768
#     img = Image.new(mode="RGB", size=(img_w, img_h), color='#fafafa')
#     draw = ImageDraw.Draw(img)

#     # open background image
#     img_background = Image.open(image_path)
#     img_background_w = 576
#     img_background_h = 768
#     img_background = resize_image(img_background, image_path, img_background_w, img_background_h)
#     img.paste(img_background, (img_w - img_background_w, 0))

#     xy = [
#         (0, 0,),
#         (img_background_w, 0,),
#         (img_w - img_background_w, img_h,),
#         (0, img_h,),
#     ]
#     draw.polygon(xy, fill ="#1d4ed8") 

#     font_size = 48
#     line_spacing = 1.3
#     font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
#     line = title
#     line_w = font.getbbox(line)[2]
#     line_h = font.getbbox(line)[3]
#     draw.text((50, 50), line, '#ffffff', font=font)
    
#     font_size = 24
#     font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
#     line = subtitle
#     draw.text((50, 50 + line_h * line_spacing), line, '#ffffff', font=font)
    
#     line_spacing = 1.5
#     lst_line_height = 40
#     line_h = font.getbbox(lst[0])[3]
#     for i, line in enumerate(lst):
#         draw.text((50, 50 + line_h * line_spacing + 100 + lst_line_height * i), line, '#ffffff', font=font)

#     draw.text((50, img_h - 50 - line_h), '© Ozonogroup.it', '#ffffff', font=font)
    
#     img.save(out_image_path, format='JPEG', subsampling=0, quality=100)
    
#     if image_path == 'assets/images/resized/ozono-sanificazione-benefici-efficace.jpg':
#         img.show()
#         quit()

#     # img.show()

#     # return filepath
    
    
def generate_image_template_1_new(in_path, out_path, title, subtitle, lst):
    # create canvas 
    img_w = 1024
    img_h = 768
    img = Image.new(mode="RGB", size=(img_w, img_h), color='#fafafa')
    draw = ImageDraw.Draw(img)

    # open background image
    img_background = Image.open(in_path)
    img_background_w = 576
    img_background_h = 768
    img.paste(img_background, (img_w - img_background_w, 0))

    xy = [
        (0, 0,),
        (img_background_w, 0,),
        (img_w - img_background_w, img_h,),
        (0, img_h,),
    ]
    draw.polygon(xy, fill ="#1d4ed8") 

    font_size = 48
    line_spacing = 1.3
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = title
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((50, 50), line, '#ffffff', font=font)
    
    font_size = 24
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = subtitle
    draw.text((50, 50 + line_h * line_spacing), line, '#ffffff', font=font)
    
    line_spacing = 1.5
    lst_line_height = 40
    line_h = font.getbbox(lst[0])[3]
    for i, line in enumerate(lst):
        draw.text((50, 50 + line_h * line_spacing + 100 + lst_line_height * i), line, '#ffffff', font=font)

    draw.text((50, img_h - 50 - line_h), '© Ozonogroup.it', '#ffffff', font=font)
    
    img.save(out_path, format='JPEG', subsampling=0, quality=100)
    print(out_path)





# in_folder = 'assets/images/resized'
# out_folder = 'assets/images/articles'

# # sanificazioni
# generate_image_template_1(
#     f'{in_folder}/ozono-sanificazione-cosa-serve.jpg', 
#     f'{out_folder}/ozono-sanificazione-cosa-serve.jpg', 
#     'Sanificazione Ozono',
#     'A COSA SERVE',
#     [
#         "Pulisce l'aria",
#         "Disinfetta le superfici",
#         "Depura l'acqua",
#     ]
# )

# generate_image_template_1(
#     f'{in_folder}/ozono-sanificazione-perché-funziona.jpg', 
#     f'{out_folder}/ozono-sanificazione-perché-funziona.jpg', 
#     'Sanificazione Ozono',
#     'PERCHÉ FUNZIONA',
#     [
#         "Ossida i costituenti cellulari",
#         "Inattiva il DNA/RNA",
#         "Reagisce con proteine e enzimi",
#     ]
# )

# generate_image_template_1(
#     f'{in_folder}/ozono-sanificazione-aria.jpg', 
#     f'{out_folder}/ozono-sanificazione-aria.jpg', 
#     'Sanificazione Ozono',
#     'ARIA',
#     [
#         "Acquista un generatore di ozono",
#         "Sgombera l'ambiente da persone/animali",
#         "Imposta il generatore di ozono",
#         "Avvia il generatore di ozono",
#         "Esci dall'ambiente",
#         "Chiudi e sigilla l'ambiente",
#         "Arieggia l'ambiente finito il trattamento",
#     ]
# )

# generate_image_template_1(
#     f'{in_folder}/ozono-sanificazione-acqua.jpg', 
#     f'{out_folder}/ozono-sanificazione-acqua.jpg', 
#     'Sanificazione Ozono',
#     'ACQUA',
#     [
#         "Acquista un generatore di ozono",
#         "Imposta il generatore di ozono",
#         "Avvia il generatore di ozono",
#         "Miscela l'ozono accuratamente",
#         "Genera l'ozono per il tempo necessario",
#         "Non respirare l'ozono prodotto",
#         "Aspetta 20-30 minuti prima dell'utilizzo",
#     ]
# )

# generate_image_template_1(
#     f'{in_folder}/ozono-sanificazione-vantaggi.jpg', 
#     f'{out_folder}/ozono-sanificazione-vantaggi.jpg', 
#     'Sanificazione Ozono',
#     'VANTAGGI',
#     [
#         "Ha un ampio spettro di disinfezione",
#         "Elimina gli odori",
#         "Ha un'ampia copertura",
#         "Risparmia tempo",
#         "Consuma meno energia",
#         "Non lascia residui chimici",
#         "Rispetta l'ambiente",
#     ]
# )

# generate_image_template_1(
#     f'{in_folder}/ozono-sanificazione-svantaggi.jpg', 
#     f'{out_folder}/ozono-sanificazione-svantaggi.jpg', 
#     'Sanificazione Ozono',
#     'SVANTAGGI',
#     [
#         "È tossico se respirato",
#         "Richiede attrezzature specializzate",
#         "Deteriora alcuni materiali",
#     ]
# )

# generate_image_template_1(
#     f'{in_folder}/ozono-sanificazione-applicazioni.jpg', 
#     f'{out_folder}/ozono-sanificazione-applicazioni.jpg', 
#     'Sanificazione Ozono',
#     'APPLICAZIONI',
#     [
#         "Sanifica la casa",
#         "Disinfetta l'auto",
#         "Disinfetta gli ospedali",
#         "Sanitizza le lavanderie",
#         "Sanifica le piscine",
#         "Sanitizza l'industria alimentare",
#         "Sanifica l'industria agricoltura",
#     ]
# )


# sanificazione benefici

raw_image_filepath = 'C:\\Users\\Utente 01\\Desktop\\resize_images\\in\\ozono-sanificazione-benefici-penetrante.jpg'
resized_image_filepath = 'assets/images/resized/ozono-sanificazione-benefici-penetrante.jpg'
generated_image_filepath = 'assets/images/articles/ozono-sanificazione-benefici-penetrante.jpg'

resize_image(raw_image_filepath, resized_image_filepath, 576, 768)

# image_filename = 'ozono-sanificazione-benefici-efficace.jpg'
# generate_image_template_1_new(
#     image_filename,
#     f'{in_folder}', 
#     f'{out_folder}', 
#     'Sanificazione Ozono Benefici',
#     'EFFICACE',
#     [  
#         'Inattiva i batteri.',
#         'Neutralizza i virus.',
#         'Elimina i funghi.',
#         'Distruzione di protozoi.',
#         'Abbattere le spore fungine.',
#         'Disgregare le alghe.',
#         'Inibisce i parassiti.',
#         'Sterilizza gli acari.',
#         'Spezza i biofilm batterici.',
#         'Disinfetta i prioni.',
#     ]
# )



image_filename = 'ozono-sanificazione-benefici-penetrante.jpg'
generate_image_template_1_new(
    resized_image_filepath, 
    generated_image_filepath, 
    'Sanificazione Ozono Benefici',
    'PENETRANTE',
    [   
        "Condotti dell'aria",
        "Superfici irregolari",
        "Sistemi di ventilazione",
        "Spazi angusti",
        "Superfici porose",
        "Ambiti ospedalieri",
        "Apparecchiature elettroniche",
        "Sistemi di climatizzazione",
        "Superfici verticali",
        "Ambienti industriali",
    ]
)


raw_image_filepath = 'C:\\Users\\Utente 01\\Desktop\\resize_images\\in\\ozono-sanificazione-benefici-rapida.jpg'
resized_image_filepath = 'assets/images/resized/ozono-sanificazione-benefici-rapida.jpg'
generated_image_filepath = 'assets/images/articles/ozono-sanificazione-benefici-rapida.jpg'

resize_image(raw_image_filepath, resized_image_filepath, 576, 768)

image_filename = 'ozono-sanificazione-benefici-rapida.jpg'
generate_image_template_1_new(
    resized_image_filepath, 
    generated_image_filepath, 
    'Sanificazione Ozono Benefici',
    'RAPIDA',
    [   
        "Inattiva batteri e virus rapidamente.",
        "Elimina odori persistenti rapidamente.",
        "Velocizza la rioccupazione degli ambienti.",
        "Ottimizza la disinfezione di grandi spazi.",
        "Riduce il tempo di lavorazione manuale.",
        "Evita di disassemblare attrezzature.",
        "Riduce i risciacqui post trattamento.",
        "Viene generato in loco.",
        "Cancella tempi di gestione inventario.",
        "Migliora l'efficienza operativa.",
    ]
)