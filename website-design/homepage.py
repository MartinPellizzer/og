import os
import time
import json
import random
import requests

import lorem

import util
import util_ai
import layout
import layouts_og
import components

SLEEP_TIME = 30



def homepage():
    header = layouts_og.header_0000()
    _template_0000 = layouts_og.template_0000()
    _template_0001 = layouts_og.template_0001()
    _template_0002 = layouts_og.template_0002()
    _template_0003 = layouts_og.template_0003()
    _template_0004 = layouts_og.template_0004()

    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
            <link rel="stylesheet" href="style-auto.css">
            <link rel="stylesheet" href="tailwind.css">
        </head>
        <body>
            {header}
            <div class="mb-96"></div>
            <main>
                {_template_0000}
                <div class="mb-48"></div>
                {_template_0001}
                {_template_0003}
                {_template_0004}
            </main>
            <footer></footer>
        </body>
        </html>
    '''

    with open('homepage.html', 'w') as f:
        f.write(html)

homepage()