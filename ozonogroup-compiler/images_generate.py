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

image_filename = 'ozono-sanificazione-benefici-efficace.jpg'

raw_image_filepath = f'C:\\Users\\Utente 01\\Desktop\\resize_images\\in\\{image_filename}'
resized_image_filepath = f'assets/images/resized/{image_filename}'
generated_image_filepath = f'assets/images/articles/{image_filename}'

# resize_image(raw_image_filepath, resized_image_filepath, 576, 768)

generate_image_template_1_new(
    resized_image_filepath,
    generated_image_filepath,
    'Sanificazione Ozono',
    'EFFICACE',
    [  
        'Inattiva i batteri',
        'Neutralizza i virus',
        'Elimina i funghi',
        'Distruzione di protozoi',
        'Abbattere le spore fungine',
        'Disgregare le alghe',
        'Inibisce i parassiti',
        'Sterilizza gli acari',
        'Spezza i biofilm batterici',
        'Disinfetta i prioni',
    ]
)



image_filename = 'ozono-sanificazione-benefici-penetrante.jpg'

raw_image_filepath = f'C:\\Users\\Utente 01\\Desktop\\resize_images\\in\\{image_filename}'
resized_image_filepath = f'assets/images/resized/{image_filename}'
generated_image_filepath = f'assets/images/articles/{image_filename}'

# resize_image(raw_image_filepath, resized_image_filepath, 576, 768)

generate_image_template_1_new(
    resized_image_filepath, 
    generated_image_filepath, 
    'Sanificazione Ozono',
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

# resize_image(raw_image_filepath, resized_image_filepath, 576, 768)
image_filename = 'ozono-sanificazione-benefici-rapida.jpg'
generate_image_template_1_new(
    resized_image_filepath, 
    generated_image_filepath, 
    'Sanificazione Ozono',
    'RAPIDA',
    [   
        "Inattiva batteri e virus rapidamente",
        "Elimina odori persistenti rapidamente",
        "Velocizza la rioccupazione degli ambienti",
        "Ottimizza la disinfezione di grandi spazi",
        "Riduce il tempo di lavorazione manuale",
        "Evita di disassemblare attrezzature",
        "Riduce i risciacqui post trattamento",
        "Viene generato in loco",
        "Cancella tempi di gestione inventario",
        "Migliora l'efficienza operativa",
    ]
)


image_filename = 'ozono-sanificazione-benefici-ecologica.jpg'

raw_image_filepath = f'C:\\Users\\Utente 01\\Desktop\\resize_images\\in\\{image_filename}'
resized_image_filepath = f'assets/images/resized/{image_filename}'
generated_image_filepath = f'assets/images/articles/{image_filename}'

# resize_image(raw_image_filepath, resized_image_filepath, 576, 768)
generate_image_template_1_new(
    resized_image_filepath, 
    generated_image_filepath, 
    'Sanificazione Ozono',
    'ECOLOGICA',
    [   
        "Riduce inquinanti atmosferici",
        "Non richiede disinfettanti chimici",
        "Non lascia residui tossici",
        "Non crea sottoprodotti dannosi",
        "Risparmia acqua",
        "Risparmia energia",
        "Minimizza la produzione di CO",
        "Si riconverte velocemente in ossigeno",
        "Non necessita di essere smaltito",
        "Preserva la biodiversità",
        "Rispetta normative ambientali",
    ]
)



image_filename = 'ozono-sanificazione-benefici-sicura.jpg'

raw_image_filepath = f'C:\\Users\\Utente 01\\Desktop\\resize_images\\in\\{image_filename}'
resized_image_filepath = f'assets/images/resized/{image_filename}'
generated_image_filepath = f'assets/images/articles/{image_filename}'

resize_image(raw_image_filepath, resized_image_filepath, 576, 768)

generate_image_template_1_new(
    resized_image_filepath, 
    generated_image_filepath, 
    'Sanificazione Ozono',
    'SICURA',
    [   
        "Rapida dissipazione",
        "Non lascia residui chimici",
        "Eliminia allergeni nell'aria",
        "Migliora la qualità dell'aria",
        "Vantaggioso per persone con asma",
        "Bassa probabilità di irritazione",
        "Non aggressivo a contatto con la pelle",
        "Evita di maneggiare prodotti chimici",
        "Non richiede manutenzione frequente",
        "Facile da usare e controllare",
        "Presenti procedure definite e sicure",
    ]
)



image_filename = 'ozono-sanificazione-benefici-versatile.jpg'

raw_image_filepath = f'C:\\Users\\Utente 01\\Desktop\\resize_images\\in\\{image_filename}'
resized_image_filepath = f'assets/images/resized/{image_filename}'
generated_image_filepath = f'assets/images/articles/{image_filename}'

resize_image(raw_image_filepath, resized_image_filepath, 576, 768)

generate_image_template_1_new(
    resized_image_filepath, 
    generated_image_filepath, 
    'Sanificazione Ozono',
    'VERSATILE',
    [   
        "Sanificazione degli ambienti domestici",
        "Settore ospedaliero e sanitario",
        "Industria alimentare",
        "Trasporti pubblici e privati",
        "Hotel e strutture ricettive",
        "Settore dell'istruzione e scuole",
        "Uffici e spazi commerciali",
        "Ambiti industriali e manifatturieri",
        "Settore degli impianti sportivi",
        "Trattamento delle acque e depurazione",
    ]
)




image_filename = 'ozono-sanificazione-benefici-economica.jpg'

raw_image_filepath = f'C:\\Users\\Utente 01\\Desktop\\resize_images\\in\\{image_filename}'
resized_image_filepath = f'assets/images/resized/{image_filename}'
generated_image_filepath = f'assets/images/articles/{image_filename}'

resize_image(raw_image_filepath, resized_image_filepath, 576, 768)

generate_image_template_1_new(
    resized_image_filepath, 
    generated_image_filepath, 
    'Sanificazione Ozono',
    'ECONOMICA',
    [   
        "Riduce spese acquisto disinfettanti",
        "Riduce spese stoccaggio disinfettanti",
        "Riduce spese applicazione disinfettanti",
        "Basso consumo energetico",
        "Minimizza il tempo di inattività",
        "Aumento della produttività",
        "Lunga durata dell'efficacia",
        "Riduzione dei costi di manutenzione",
        "Abbassa i costi di manodopera",
        "Minimizza i rischi per la salute",
    ]
)



image_filename = 'ozono-sanificazione-benefici-riconosciuta.jpg'

raw_image_filepath = f'C:\\Users\\Utente 01\\Desktop\\resize_images\\in\\{image_filename}'
resized_image_filepath = f'assets/images/resized/{image_filename}'
generated_image_filepath = f'assets/images/articles/{image_filename}'

resize_image(raw_image_filepath, resized_image_filepath, 576, 768)

generate_image_template_1_new(
    resized_image_filepath, 
    generated_image_filepath, 
    'Sanificazione Ozono',
    'RICONOSCIUTA',
    [   
        "Italia",
        "Stati Uniti",
        "Germania",
        "Francia",
        "Regno Unito",
        "Canada",
        "Australia",
        "Cina",
        "Giappone",
        "Spagna",
    ]
)



image_filename = 'ozono-sanificazione-benefici-personalizzabile.jpg'

raw_image_filepath = f'C:\\Users\\Utente 01\\Desktop\\resize_images\\in\\{image_filename}'
resized_image_filepath = f'assets/images/resized/{image_filename}'
generated_image_filepath = f'assets/images/articles/{image_filename}'

resize_image(raw_image_filepath, resized_image_filepath, 576, 768)

generate_image_template_1_new(
    resized_image_filepath, 
    generated_image_filepath, 
    'Sanificazione Ozono',
    'PERSONALIZZABILE',
    [   
        "Ampia disponibilità nel meracto",
        "Ozonizzatori standard per ogni esigenza",
        "Sanificazione multifunzionale",
        "Tecnologia solida e consolidata",
        "Sistema semplice da personalizzare",
        "Livelli di ozono impostabili",
        "Facile da automatizzare",
        "Semplica da controllare",
        "Possibile integrazione con altri sistemi",
        "Utilizzabile con industria 4.0",
    ]
)



image_filename = 'ozono-sanificazione-benefici-apprezzata.jpg'

raw_image_filepath = f'C:\\Users\\Utente 01\\Desktop\\resize_images\\in\\{image_filename}'
resized_image_filepath = f'assets/images/resized/{image_filename}'
generated_image_filepath = f'assets/images/articles/{image_filename}'

resize_image(raw_image_filepath, resized_image_filepath, 576, 768)

generate_image_template_1_new(
    resized_image_filepath, 
    generated_image_filepath, 
    'Sanificazione Ozono',
    'APPREZZATA',
    [   
        "Soddisfa il cliente",
        "Aumenta i feedback positivi",
        "Diminuisce le lamentele",
        "Maggiore percezione di igiene",
        "Apprezzata come metodo naturale",
        "Migliora reputazione azziendale",
        "Evita casi di infezioni",
        "Maggiure quota di mercato",
        "Crescente domanda di ozono",
        "Offre una soluzione completa",
        "Posizione l'azienda come leader",
    ]
)