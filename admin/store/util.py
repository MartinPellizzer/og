import csv


def csv_get_rows(filepath, delimiter='\\'):
    rows = []
    with open(filepath, encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f, delimiter=delimiter)
        for i, line in enumerate(reader):
            if line != []:
                rows.append(line)
    return rows


def csv_add_rows(filepath, rows, delimiter='\\'):
    with open(filepath, 'a', encoding='utf-8', errors='ignore', newline='') as f:
        writer = csv.writer(f, delimiter=delimiter)
        writer.writerows(rows)


def csv_set_rows(filepath, rows, delimiter='\\'):
    with open(filepath, 'w', encoding='utf-8', errors='ignore', newline='') as f:
        writer = csv.writer(f, delimiter=delimiter)
        writer.writerows(rows)
        

def csv_get_cols(rows):
    cols = {}
    i = 0
    for col_name in rows[0]:
        cols[col_name] = i
        i += 1
    return cols



def csv_get_rows_by_col_val(filepath, col_index, cell_val, delimiter='\\', ):
    rows = []
    with open(filepath, encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f, delimiter=delimiter)
        for i, line in enumerate(reader):
            if line != []:
                if line[col_index].lower().strip().replace(' ', '-').replace("'", '-') == cell_val.lower().strip().replace(' ', '-').replace("'", '-'):
                    rows.append(line)
    return rows

