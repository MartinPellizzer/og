import os


def file_read(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def file_write(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)