import os
import sys

def keywords_remove_blacklist():
    with open('keywords-master-todo.txt', errors='ignore') as f:
        keywords_new = f.readlines()

    with open('keyword-blacklisted-list.txt', errors='ignore') as f:
        keywords_old = f.readlines()

    keywords_new_filtered = [k for k in keywords_new if k not in keywords_old]

    print(len(keywords_new))
    print(len(keywords_old))
    print(len(keywords_new_filtered))

    return
    with open('keywords-master.txt', 'a', errors='ignore') as f:
        for k in keywords_new_filtered:
            f.write(k)

    with open('keywords-master-todo.txt', 'a', errors='ignore') as f:
        for k in keywords_new_filtered:
            f.write(k)


def keywords_to_master():
    with open('keywords-to-master.txt', errors='ignore') as f:
        keywords_new = f.readlines()

    with open('keywords-master.txt', errors='ignore') as f:
        keywords_old = f.readlines()

    keywords_new_filtered = [k for k in keywords_new if k not in keywords_old]

    print(len(keywords_new))
    print(len(keywords_new_filtered))

    with open('keywords-master.txt', 'a', errors='ignore') as f:
        for k in keywords_new_filtered:
            f.write(k)

    with open('keywords-master-todo.txt', 'a', errors='ignore') as f:
        for k in keywords_new_filtered:
            f.write(k)



def keywords_to_cluster(keyword):
    filepath = f'clusters/new.txt'

    with open('keywords-master-todo.txt', errors='ignore') as f:
        keywords_new = f.readlines()

    if not os.path.exists(filepath): 
        with open(filepath, 'w') as f: pass

    with open(filepath, errors='ignore') as f:
        keywords_old = f.readlines()

    keywords_new_filtered = [k for k in keywords_new if keyword in k]
    keywords_new_filtered = [k for k in keywords_new_filtered if k not in keywords_old]
    keywords_old_filtered = [k for k in keywords_new if k not in keywords_new_filtered]

    print(len(keywords_new))
    print(len(keywords_new_filtered))
    print(len(keywords_old_filtered))

    with open(filepath, 'a', errors='ignore') as f:
        for k in keywords_new_filtered:
            f.write(k)

    with open('keywords-master-todo.txt', 'w', errors='ignore') as f:
        for k in keywords_old_filtered:
            f.write(k)
            
# keywords_remove_blacklist()
# keywords_to_master()
keywords_to_cluster(sys.argv[1])