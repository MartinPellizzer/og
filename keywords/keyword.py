with open('keywords_todo.txt') as f:
    content = f.read()
new_lines = content.split('\n')

with open('_master.txt') as f:
    content = f.read()
old_lines = content.split('\n')

# quit()

filtered_lines = []
for i, new_line in enumerate(new_lines):
    if new_line not in old_lines:
        filtered_lines.append(new_line)
        # print(new_line)

print(len(new_lines))
print(len(filtered_lines))

with open('keywords_todo_filtered.txt', 'w') as f:
    for line in filtered_lines:
        f.write(f'{line}\n')