from PIL import Image, ImageFont, ImageDraw, ImageColor

def generate_image_template_1(image_path, out_image_path, title, subtitle, lst):
    img_w = 1024
    img_h = 768
    img = Image.new(mode="RGB", size=(img_w, img_h), color='#fafafa')
    draw = ImageDraw.Draw(img)

    img_background = Image.open(image_path)
    img_background_w = 576
    img_background_h = 768
    img_background.thumbnail((img_background_w, img_background_h), Image.Resampling.LANCZOS)
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
    
    img.save(out_image_path, format='JPEG', subsampling=0, quality=100)

    # img.show()

    # return filepath

in_folder = 'assets/images/resized'
out_folder = 'assets/images/articles'

generate_image_template_1(
    f'{in_folder}/ozono-sanificazione-cosa-serve.jpg', 
    f'{out_folder}/ozono-sanificazione-cosa-serve.jpg', 
    'Sanificazione Ozono',
    'A COSA SERVE',
    [
        "Pulisce l'aria",
        "Disinfetta le superfici",
        "Depura l'acqua",
    ]
)

generate_image_template_1(
    f'{in_folder}/ozono-sanificazione-perché-funziona.jpg', 
    f'{out_folder}/ozono-sanificazione-perché-funziona.jpg', 
    'Sanificazione Ozono',
    'PERCHÉ FUNZIONA',
    [
        "Ossida i costituenti cellulari",
        "Inattiva il DNA/RNA",
        "Reagisce con proteine e enzimi",
    ]
)

generate_image_template_1(
    f'{in_folder}/ozono-sanificazione-aria.jpg', 
    f'{out_folder}/ozono-sanificazione-aria.jpg', 
    'Sanificazione Ozono',
    'ARIA',
    [
        "Acquista un generatore di ozono",
        "Sgombera l'ambiente da persone/animali",
        "Imposta il generatore di ozono",
        "Avvia il generatore di ozono",
        "Esci dall'ambiente",
        "Chiudi e sigilla l'ambiente",
        "Arieggia l'ambiente finito il trattamento",
    ]
)

generate_image_template_1(
    f'{in_folder}/ozono-sanificazione-acqua.jpg', 
    f'{out_folder}/ozono-sanificazione-acqua.jpg', 
    'Sanificazione Ozono',
    'ACQUA',
    [
        "Acquista un generatore di ozono",
        "Imposta il generatore di ozono",
        "Avvia il generatore di ozono",
        "Miscela l'ozono accuratamente",
        "Genera l'ozono per il tempo necessario",
        "Non respirare l'ozono prodotto",
        "Aspetta 20-30 minuti prima dell'utilizzo",
    ]
)

generate_image_template_1(
    f'{in_folder}/ozono-sanificazione-vantaggi.jpg', 
    f'{out_folder}/ozono-sanificazione-vantaggi.jpg', 
    'Sanificazione Ozono',
    'VANTAGGI',
    [
        "Ha un ampio spettro di disinfezione",
        "Elimina gli odori",
        "Ha un'ampia copertura",
        "Risparmia tempo",
        "Consuma meno energia",
        "Non lascia residui chimici",
        "Rispetta l'ambiente",
    ]
)

generate_image_template_1(
    f'{in_folder}/ozono-sanificazione-svantaggi.jpg', 
    f'{out_folder}/ozono-sanificazione-svantaggi.jpg', 
    'Sanificazione Ozono',
    'SVANTAGGI',
    [
        "È tossico se respirato",
        "Richiede attrezzature specializzate",
        "Deteriora alcuni materiali",
    ]
)

generate_image_template_1(
    f'{in_folder}/ozono-sanificazione-applicazioni.jpg', 
    f'{out_folder}/ozono-sanificazione-applicazioni.jpg', 
    'Sanificazione Ozono',
    'APPLICAZIONI',
    [
        "Sanifica la casa",
        "Disinfetta l'auto",
        "Disinfetta gli ospedali",
        "Sanitizza le lavanderie",
        "Sanifica le piscine",
        "Sanitizza l'industria alimentare",
        "Sanifica l'industria agricoltura",
    ]
)



