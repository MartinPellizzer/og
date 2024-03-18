from googlesearch import search
import requests
from bs4 import BeautifulSoup

results = search("sanificazione ozono applicazioni", lang='it')

# for result in results:
#     print(result)

urls = [x for x in results]

for i, url in enumerate(urls):
    # url = urls[0]
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    h1 = soup.find_all("h1")
    h2 = soup.find_all("h2")
    h3 = soup.find_all("h3")
    h4 = soup.find_all("h4")
    h5 = soup.find_all("h5")
    h6 = soup.find_all("h6")
    paragraphs = soup.find_all("p")

    # print(soup.prettify())
    # print(title)
    # for p in paragraphs:
    #     print(p.text)
    #     print()

    # print(soup.text)
    print(f'------------------------------------------')
    print(f'{i+1}/{len(urls)}')
    print(f'------------------------------------------')
    for e in h1: print(e.text)
    for e in h2: print(e.text)
    for e in h3: print(e.text)
    for e in h4: print(e.text)
    for e in h5: print(e.text)
    for e in h6: print(e.text)

    with open(f'scraped/scraped-{i+1}.txt', 'w', encoding='utf-8') as f:
        f.write(f'dato il seguente testo, dammi una lista completa dei benefici e vantaggi della sanificazione ad ozono:\n')
        f.write(soup.text)