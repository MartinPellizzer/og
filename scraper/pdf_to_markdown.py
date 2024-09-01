import os
import pdfplumber

pdf_file = '36847.pdf'
pdfs_folderpath = f'/home/ubuntu/vault/ozonogroup/studies/pubmed/ozone/pdfs-done'
markdowns_folderpath = f'/home/ubuntu/vault/ozonogroup/studies/pubmed/ozone/markdowns'
pdfs_filenames = os.listdir(pdfs_folderpath)
for i, pdf_filename in enumerate(pdfs_filenames):
    print(f'{i}/{len(pdfs_filenames)}')
    pdf_filepath = f'{pdfs_folderpath}/{pdf_filename}'
    markdown_filename = pdf_filename.replace('.pdf', '.md')
    markdown_filepath = f'{markdowns_folderpath}/{markdown_filename}'
    if os.path.exists(markdown_filepath): continue

    with pdfplumber.open(pdf_filepath) as pdf:
        markdown_text = ''
        for page in pdf.pages:
            markdown_text += page.extract_text()

    with open(markdown_filepath, 'w') as file:
        file.write(markdown_text)
