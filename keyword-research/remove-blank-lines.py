with open('keyword-filtered-list.txt') as f:
    lines = f.readlines()

filtered_keywords = [x for x in lines if x != '\n']

with open('keyword-filtered-list.txt', 'w', encoding='utf-8') as f:
        for k in filtered_keywords:
            f.write(k)