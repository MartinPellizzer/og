import requests
import os
import sys

import util

if sys.argv[1] != '': query = sys.argv[1]

ACCESS_KEY = util.file_read('api.txt')
print(ACCESS_KEY)

def folder_create(filepath):
    chunks = filepath.split('/')[:-1]
    chunk_curr = ''
    for chunk in chunks:
        chunk_curr += f'{chunk}/'
        try: os.makedirs(chunk_curr)
        except: pass


url = f'https://api.unsplash.com/search/photos?page=1&query={query}&client_id={ACCESS_KEY}'
print(url)

response = requests.get(url)
print(response)

data = response.json()
results = data['results']
for i, result in enumerate(results):
    url = result['urls']['regular']
    filename = f'{i+10}.jpg'
    image_response = requests.get(url, stream=True)
    print(image_response)
    if image_response.status_code == 200:
        filepath = f'C:/og-assets/images/articles-auto/{query}/{filename}'
        folder_create(filepath)

        with open(filepath, 'wb') as image_file:
            for chunck in image_response:
                image_file.write(chunck)
    print(url)