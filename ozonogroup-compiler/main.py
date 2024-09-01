import shutil

from lib import components
from lib import templates

from oliark import file_write

homepage = templates.homepage()

file_write('public/index.html', homepage)
shutil.copy('style.css', 'public/style.css')
