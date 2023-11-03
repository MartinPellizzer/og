import shutil
# shutil.copy2('/style.css', '/')

import markdown
import pathlib
import os

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from PIL import ImageColor 

import random
import re
import csv

encoding = 'utf-8'

# DB TO ARTICLE ----------------------------------------------------




w, h = 800, 600
generate_image_plain('assets/images/home/pasta-raw.jpg', w, h, 'assets/images/home/pasta.jpg')
generate_image_plain('assets/images/home/clinica-raw.jpg', w, h, 'assets/images/home/clinica.jpg')
generate_image_plain('assets/images/home/trasporti-raw.jpg', w, h, 'assets/images/home/trasporti.jpg')













shutil.copy2('index.html', 'public/index.html')

shutil.copy2('style.css', 'public/style.css')
shutil.copy2('style-blog.css', 'public/style-blog.css')
shutil.copy2('util.css', 'public/util.css')
shutil.copy2('img.css', 'public/img.css')
shutil.copy2('logo.ico', 'public/logo.ico')
shutil.copy2('CNAME', 'public/CNAME')



