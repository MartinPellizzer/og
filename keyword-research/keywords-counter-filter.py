from tkinter import *  
  
root = Tk()  
  
root.geometry("800x600")  
  
listbox1 = Listbox(root, width=32)
listbox1.pack(side='left', fill='y', padx=32, pady=32)

listbox2 = Listbox(root, width=32)
listbox2.pack(side='left', fill='y', padx=32, pady=32)

listbox3 = Listbox(root, width=32)
listbox3.pack(side='left', fill='y', padx=32, pady=32)


# FILTERED
with open('keyword-filtered-list.txt') as f:
    filtered_lines = f.readlines()

filtered_keywords = []
for filtered_line in filtered_lines:
    if not filtered_line: continue
    keyword = filtered_line.split(',')[0]
    filtered_keywords.append(keyword)
    
for line in filtered_keywords:
    listbox2.insert(END, line)


# BLACKLISTED
with open('keyword-blacklisted-list.txt') as f:
    blacklisted_lines = f.readlines()

blacklisted_keywords = []
for line in blacklisted_lines:
    if not line: continue
    keyword = line.split(',')[0]
    blacklisted_keywords.append(line)

for line in blacklisted_keywords:
    listbox3.insert(END, line)

with open('out.csv', encoding="utf-8") as f:
    lines = f.readlines()


# for i, line in enumerate(lines):
#     if i > 100: break
#     print(line)


# lines = [ x for x in lines if "ozone" not in x.split(',') ]




for filtered_keyword in filtered_keywords:
    lines = [ x for x in lines if filtered_keyword not in x.split(',') ]

for i, line in enumerate(lines):
    listbox1.insert(i, line)






def filter_item(e):
    item_index = listbox1.curselection()
    selected_item = listbox1.get(item_index)
    listbox2.insert(END, selected_item)
    listbox1.delete(item_index)
    listbox1.selection_set(item_index)

    with open('keyword-filtered-list.txt', 'a', encoding='utf-8') as f:
        f.write(selected_item)


def blacklist_item(e):
    item_index = listbox2.curselection()
    selected_item = listbox2.get(item_index)
    listbox3.insert(END, selected_item)
    listbox2.delete(item_index)
    listbox2.selection_set(item_index)

    with open('keyword-blacklisted-list.txt', 'a', encoding='utf-8') as f:
        f.write(selected_item)

    filtered_keywords.remove(selected_item)

    with open('keyword-filtered-list.txt', 'w', encoding='utf-8') as f:
        for k in filtered_keywords:
            f.write(k)


listbox1.bind('f', filter_item) 
listbox2.bind('b', blacklist_item) 

root.mainloop()