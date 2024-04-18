import shutil

import util
import util_img
import g

products_csv_filepath = 'database/csv/products.csv'
products_rows = util.csv_get_rows(products_csv_filepath)
products_cols = util.csv_get_cols(products_rows)

for product_row in products_rows[1:]:
    print(product_row)


html_header = util.component_header_no_logo()
html_header = f'''
    <section class="header-section mb-96">
        <div class="container-xl h-full">
            {html_header}
        </div>
    </section>
'''

img_in_filepath = 'C:/og-assets/images/prodotti/omega-o3-plus/0000.jpg'
img_out_filepath = 'public/assets/images/ozonogroup-prodotti-omega-o3-plus.jpg'
img_web_filepath = 'assets/images/ozonogroup-prodotti-omega-o3-plus.jpg'
img_alt = 'ozonogroup prodotti omega o3 plus'
img_omega_plus = f'<img src="{img_web_filepath}" alt="{img_alt}">'
util_img.resize(img_in_filepath, img_out_filepath, rotate=180, quality=70)

html = f'''
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="/style.css">
        <link rel="stylesheet" href="/util.css">
        <link rel="stylesheet" href="/img.css">
        <title>Ozonogroup | Prodotti</title>
        {g.GOOGLE_TAG}
    </head>

    <body>
        {html_header}

        <section>
            <div class="container-xl h-full">

                <div class="grid-2 items-center mb-96">
                    <div class="grid-col-1">
                        {img_omega_plus}
                    </div>
                    <div class="grid-col-2">
                        <h2 class="mb-16">Omega O3</h2>
                        <p>L'Omega O3 viene utilizzata per sanificare ambienti di piccole e medie dimensioni.</p>
                        <p>
                            Quest'apparecchiatura genera ozono in forma gassosa e ha una ventola che distribuisce questo gas nell'ambiente.
                        </p>
                        <p>Il sopralluogo sarà fatto solo se Ozonogroup lo riterrà utile e, in tal caso, sarà totalmente
                            gratuito.</p>
                    </div>
                </div>

                <div class="grid-2 items-center reverse mb-96">
                    <div class="grid-col-1">
                        <h2 class="mb-16">Big Power</h2>
                        <p>A seguito dell'incontro di consulenza e di un'eventuale sopralluogo, andremo a fare uno studio di
                            fattibilità per verificare se la sanificazione ad ozono sia implementabile nella tua specifica
                            situaztione.
                        </p>
                        <p>Nel caso in cui lo sia, andremo a identificare il sistema di sanificazione che meglio soddisfa la
                            tua esigenza. Valuteremo se hai bisogno di un sistema progettato su misura o se una soluzione
                            standard è sufficiente.
                        </p>
                        <p>In entrambi i casi, faremo anche un'analisi costi/benefici per capire con te se questo sistema è
                            vantaggioso da un punto di vista economico o se non è conveniente implementarlo. </p>
                    </div>
                    <div class="grid-col-2"><img src="assets/images/ozonogroup-servizi-studio-fattibilità.jpg" alt=""></div>
                </div>
            </div>
        </section>

        <section class="footer-section">
            <div class="container-xl h-full">
                <footer class="flex">
                    <span class="text-white">Ozonogroup s.r.l. | Tutti i diritti riservati</span>
                </footer>
            </div>
        </section>

    </body>

    </html>
    '''

util.file_write('public/prodotti.html', html)

shutil.copy2('style.css', 'public/style.css')