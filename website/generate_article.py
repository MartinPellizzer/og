encoding = 'utf-8'

rows = []
with open("database/dairy.csv", "r", encoding=encoding) as f:
    reader = csv.reader(f, delimiter="\\")
    for i, line in enumerate(reader):
        rows.append(line)