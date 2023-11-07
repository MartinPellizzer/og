from googlesearch import search
import requests
from bs4 import BeautifulSoup

results = search("sanificazione ozono benefici", lang='it')

# for result in results:
#     print(result)

urls = [x for x in results]

for i, url in enumerate(urls):
    # url = urls[0]
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    title = soup.find_all("h1")
    paragraphs = soup.find_all("p")

    # print(soup.prettify())
    # print(title)
    # for p in paragraphs:
    #     print(p.text)
    #     print()

    # print(soup.text)
    print(f'{i+1}/{len(urls)}: {title}')

    with open(f'scraped/scraped-{i+1}.txt', 'w', encoding='utf-8') as f:
        f.write(f'dato il seguente testo, dammi una lista completa dei benefici e vantaggi della sanificazione ad ozono:\n')
        f.write(soup.text)