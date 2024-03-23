
def generate_table_problems():
    pass
    # article_html += f'<p>La seguente tabella elenca i nomi di alcuni problemi di contaminazione che l\'ozono elimina {application_a_1}{application}, divisi per categoria.</p>'
        # batteri = ', '.join(data['problemi_batteri'][:5])
        # virus = ', '.join(data['problemi_virus'][:5])
        # muffe = ', '.join(data['problemi_muffe'][:5])
        # insetti = ', '.join(data['problemi_insetti'][:5])
        # odori = ', '.join(data['problemi_odori'][:5])
        # article_html += f'''
        #     <table>
        #         <tr>
        #             <th>Categoria</th>
        #             <th>Nomi</th>
        #         </tr>
        #         <tr>
        #             <td>Batteri</td>
        #             <td>{batteri}</td>
        #         </tr>
        #         <tr>
        #             <td>Virus</td>
        #             <td>{virus}</td>
        #         </tr>
        #         <tr>
        #             <td>Muffe</td>
        #             <td>{muffe}</td>
        #         </tr>
        #         <tr>
        #             <td>Insetti</td>
        #             <td>{insetti}</td>
        #         </tr>
        #         <tr>
        #             <td>Odori</td>
        #             <td>{odori}</td>
        #         </tr>
        #     </table>
        # '''


def generate_manual_article_html():
    folder = pathlib.Path("articles")

    w, h = 768, 432
    util_img.gen_plain(
        'assets/images/featured/ozono-chimica.jpg', 
        w, h,
        'public/assets/images/ozono-chimica.jpg',
    )
    util_img.gen_plain(
        'assets/images/featured/ozono-stratosferico.jpg', 
        w, h, 
        'public/assets/images/ozono-stratosferico.jpg', 
    )
    util_img.gen_plain(
        'assets/images/featured/ozono-troposferico.jpg', 
        w, h, 
        'public/assets/images/ozono-troposferico.jpg', 
    )
    util_img.gen_plain(
        'assets/images/featured/ozono-effetti.jpg', 
        w, h, 
        'public/assets/images/ozono-effetti.jpg', 
    )
    util_img.gen_plain(
        'assets/images/featured/ozono-benefici.jpg', 
        w, h, 
        'public/assets/images/ozono-benefici.jpg', 
    )
    util_img.gen_plain(
        'assets/images/featured/ozono-sanificazione.jpg', 
        w, h, 
        'public/assets/images/ozono-sanificazione.jpg', 
    )
    util_img.gen_plain(
        'assets/images/featured/ozono-sanificazione-benefici.jpg', 
        w, h, 
        'public/assets/images/ozono-sanificazione-benefici.jpg', 
    )

    for filepath in folder.rglob("*.md"):
        filepath = str(filepath)
        
        with open(filepath, encoding='utf-8') as f:
            content = f.read()

        content_html = markdown.markdown(content, extensions=['markdown.extensions.tables', 'meta'])

        md = markdown.Markdown(extensions=['meta'])
        md.convert(content)

        title = ''
        try: title = md.Meta['title'][0]
        except: pass
        print(title)

        lines = '\n'.join(md.lines)

        content_html = markdown.markdown(lines, extensions=['markdown.extensions.tables'])

        # BREADCRUMBS  ---------------------------------------------
        breadcrumbs = generate_breadcrumbs(filepath)

        # READING TIME  --------------------------------------------
        reading_time = len(content.split(' ')) // 200

        # PUBLICATION DATE  ----------------------------------------
        publishing_date = ''
        try: publishing_date = md.Meta['publishing_date'][0]
        except: pass

        # AUTHOR ----------------------------------------
        author = 'Ozonogroup Staff'
        try: author = md.Meta['author'][0]
        except: pass

        last_update_date = ''
        try: last_update_date = md.Meta['last_update_date'][0]
        except: pass

        # GENERATE TABLE OF CONTENTS ----------------------------------------
        toc_html = generate_toc(content_html)
        
        
        with open('components/header.html', encoding='utf-8') as f:
            header_html = f.read()
                

                
        html = f'''
            <!DOCTYPE html>
            <html lang="en">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link rel="stylesheet" href="/style-blog.css">
                <link rel="stylesheet" href="/util.css">
                <title>{title}</title>
                {GOOGLE_TAG}
            </head>

            <body>
                <section class="header-section">
                    <div class="container-xl h-full">
                        {header_html}
                    </div>
                </section>

                <section class="breadcrumbs-section">
                    <div class="container-xl h-full">
                        <a href="/index.html">Home</a>{''.join(breadcrumbs)}
                    </div>
                </section>

                <section class="meta-section mt-48">
                    <div class="container-md h-full">
                        <div class="flex justify-between mb-8">
                            <span>by {author} • {publishing_date}</span>
                            <span>Tempo Lettura: {reading_time} min</span>
                        </div>
                    </div>
                </section>

                <section class="container-md">
                    {toc_html}
                </section>

                <section class="footer-section">
                    <div class="container-xl h-full">
                        <footer class="flex items-center justify-center">
                            <span class="text-white">Ozonogroup s.r.l. | Tutti i diritti riservati</span>
                        </footer>
                    </div>
                </section>
            </body>

            </html>
        '''

        filepath_out_dir = '/'.join(filepath_chunks[1:-1])
        filepath_out = '/'.join(filepath_chunks[1:]).replace('.md', '.html')
        # print(filepath_out)

        if not os.path.exists(filepath_out_dir):
            os.makedirs(filepath_out_dir)

        util.file_write(filepath_out, html)

    
    # IMAGES
    industries = [
        'lattiero-casearia',
        'salumiera',
        'ittica',
        'cerealicola',
        'ortofrutticola',
        'vinicola',
        'acqua-minerale',
        'birraria',
        'lavorazione-carni',
        'automobili',
        'ospedali',
        'ambulanze',
        'case-di-riposo',
        'cliniche-dentistiche',
        'cliniche-veterinarie',
        'scuole',
        'asili',
        'bagni-pubblici',
        'cinema',
        'teatri',
        'alberghi',
        'bed-and-breakfast',
    ]
    articles_folder = 'articles/public/ozono/sanificazione/applicazioni'
    for article_filename in os.listdir(articles_folder):
        article_filename_no_ext = article_filename.replace('.md', '')
        print(article_filename)
        if article_filename_no_ext in industries:
            print('ok')
            article_filepath = f'{article_filename}/{article_filename}'
            images_articles_folder = f'C:/og-assets/images/articles'
            images_article_folder = f'{images_articles_folder}/{article_filename_no_ext}'
            images_filepath = [f'{images_article_folder}/{filepath}' for filepath in os.listdir(images_article_folder)]

            image_filepath = images_filepath.pop(0)
            util_img.resize(
                image_filepath, 
                f'public/assets/images/ozono-sanificazione-{article_filename_no_ext}.jpg'
            )

            image_filepath = images_filepath.pop(0)
            util_img.resize(
                image_filepath, 
                f'public/assets/images/ozono-sanificazione-{article_filename_no_ext}-definizione.jpg'
            )

            image_filepath = images_filepath.pop(0)
            util_img.resize(
                image_filepath, 
                f'public/assets/images/ozono-sanificazione-{article_filename_no_ext}-problemi.jpg'
            )

            image_filepath = images_filepath.pop(0)
            util_img.resize(
                image_filepath, 
                f'public/assets/images/ozono-sanificazione-{article_filename_no_ext}-benefici.jpg'
            )

            image_filepath = images_filepath.pop(0)
            util_img.resize(
                image_filepath, 
                f'public/assets/images/ozono-sanificazione-{article_filename_no_ext}-applicazioni.jpg'
            )
        

def copy_images():
    # articles_images_path = 'assets/images/articles/'
    # for f in os.listdir(articles_images_path):
    #     shutil.copy2(f'{articles_images_path}{f}', f'public/assets/images/{f}')
        
    articles_images_path = 'assets/images/home/'
    for f in os.listdir(articles_images_path):
        shutil.copy2(f'{articles_images_path}{f}', f'public/assets/images/{f}')
        
    articles_images_path = 'assets/images/static/'
    for f in os.listdir(articles_images_path):
        shutil.copy2(f'{articles_images_path}{f}', f'public/assets/images/{f}')


def generate_article_html(date, attribute, article, title):
    with open(f'articles/public/ozono/sanificazione/{attribute}.md', 'w', encoding='utf-8') as f:
        f.write(article)

    with open(f'articles/public/ozono/sanificazione/{attribute}.md', encoding='utf-8') as f:
        article_md = f.read()

    word_count = len(article_md.split(' '))
    reading_time = str(word_count // 200) + ' minuti'
    # word_count_html = str(word_count) + ' words'

    # article_html = markdown.markdown(article_md)
    article_html = markdown.markdown(article_md, extensions=['markdown.extensions.tables'])


    # GENERATE TABLE OF CONTENTS ----------------------------------------
    article_html = generate_toc(article_html)

    with open('components/header.html', encoding='utf-8') as f:
            header_html = f.read()

    author = 'Ozonogroup'

    html = f'''
        <!DOCTYPE html>
        <html lang="en">

        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="/style-blog.css">
            <title>{title}</title>
            {GOOGLE_TAG}
        </head>

        <body>
            <section class="header-section">
                <div class="container-xl">
                    {header_html}
                </div>
            </section>

            <section class="meta-section mt-48">
                <div class="container-md px-16">
                    <div class="flex justify-between mb-8">
                        <span>by {author} • {date}</span>
                        <span>Tempo Lettura: {reading_time}</span>
                    </div>
                </div>
            </section>

            <section class="mb-96">
                <div class="container-md px-16">
                    {article_html}
                </div>
            </section>
            
            <section class="footer-section">
                <div class="container-xl h-full">
                    <footer class="flex items-center justify-center">
                        <span class="text-white">Ozonogroup s.r.l. | Tutti i diritti riservati</span>
                    </footer>
                </div>
            </section>

        </body>

        </html>
    '''

    with open(f'public/ozono/sanificazione/{attribute}.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
