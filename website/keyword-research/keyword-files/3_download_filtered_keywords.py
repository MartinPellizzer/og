with open('keyword-filtered-list.txt') as f:
    filtered_lines = f.readlines()

filtered_keywords = []
for filtered_line in filtered_lines:
    if not filtered_line: continue
    keyword = filtered_line.split(',')[0]
    filtered_keywords.append(keyword)


with open('out.csv', encoding="utf-8") as f:
    lines = f.readlines()

for filtered_keyword in filtered_keywords:
    lines = [ x for x in lines if filtered_keyword not in x.split(',') ]


with open('out-filtered.csv', 'w', encoding="utf-8") as f:
    for line in lines:
        f.write(line)

# print(lines)