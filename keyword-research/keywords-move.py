seed_keyword = 'ozonoterapia'
output_file = f'clusters/{seed_keyword}.txt'

with open('keywords-master-todo.txt', errors='ignore') as f:
    keywords = f.read()

keywords = keywords.split('\n')

filtered_keywords = []
for k in keywords:
    if seed_keyword in k.split(' '):
        filtered_keywords.append(k)

with open(output_file, 'w', errors='ignore') as f:
    for k in filtered_keywords:
        f.write(k)
        f.write('\n')
