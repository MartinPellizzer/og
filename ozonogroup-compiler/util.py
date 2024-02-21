import os


def file_write(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)