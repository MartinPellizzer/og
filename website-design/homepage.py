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
    _template_0005 = layouts_og.template_0005()
    _template_0006 = layouts_og.template_0006()
    _template_0007 = layouts_og.template_0007()

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
                {_template_0003}
                {_template_0004}
                {_template_0005}
                {_template_0006}
                {_template_0007}
                {_template_0006}

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<p>I. Introduction</p>
<p>* A. Engaging headline highlighting the benefits of ozone generation for sanitization</p>
<p>* B. Brief overview of your brand and its mission</p>
<p>* C. Call to action to explore the website and learn more about your products</p>
<p>II. About Ozone Generation</p>
<p>* A. Explanation of what ozone generation is and how it works</p>
<p>* B. Comparison of ozone generation to other sanitization methods</p>
<p>* C. List of common applications for ozone generation</p>
<p>III. Products</p>
<p>* A. Overview of your product line, including different models and sizes</p>
<p>* B. Description of key features and benefits of your ozone generators</p>
<p>* C. Call to action to learn more about each product and purchase</p>
<p>IV. Resources</p>
<p>* A. FAQ section addressing common questions about ozone generation</p>
<p>* B. Blog or news section featuring articles and updates related to ozone and sanitization</p>
<p>* C. Testimonials or case studies showcasing the success of your products</p>
<p>V. Contact</p>
<p>* A. Contact information for customer service and support</p>
<p>* B. Form for inquiries or requests for more information</p>
<p>* C. Social media links for staying connected and engaged.</p>
            </main>
            <footer></footer>
        </body>
        </html>
    '''

    with open('homepage.html', 'w') as f:
        f.write(html)

homepage()