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
    _spacer_lg = layouts_og.spacer_lg()
    _spacer_xl = layouts_og.spacer_xl()

    header = layouts_og.header_0000()
    _template_0000 = layouts_og.template_0000()
    _template_0001 = layouts_og.template_0001()
    _template_0004 = layouts_og.template_0004()
    _template_0005 = layouts_og.template_0005()
    

    _footer_0000 = layouts_og.footer_0000()

    _section_our_work = layouts_og.template_content_image_ext(theme='dark')

    _benefit_1 = layouts_og.template_content_image_ext(theme='dark')
    _benefit_2 = layouts_og.template_image_content_ext(theme='dark')
    _benefit_3 = layouts_og.template_content_image_ext(theme='dark')

    _images_1_ext = layouts_og.images_x2_ext()
    _images_2_ext = layouts_og.images_x3_ext()
    _images_3_ext = layouts_og.images_x4_ext()
    _images_4_ext = layouts_og.images_x5_ext()
    _images_5_ext = layouts_og.images_x6_ext()

    _images_1 = layouts_og.images_x2()
    _images_2 = layouts_og.images_x3()
    _images_3 = layouts_og.images_x4()
    _images_4 = layouts_og.images_x5()
    _images_5 = layouts_og.images_x6()

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
                {_section_our_work}
                {_template_0004}
                {_template_0005}

                {_spacer_lg}

                {_benefit_1}
                {_benefit_2}
                {_benefit_3}

                {_spacer_xl}

                {_images_1_ext}
                {_images_2_ext}
                {_images_3_ext}
                {_images_4_ext}
                {_images_5_ext}

                {_spacer_lg}

                {_images_1}
                {_images_2}
                {_images_3}
                {_images_4}
                {_images_5}
            </main>
            {_footer_0000}

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
        </body>
        </html>
    '''

    with open('homepage.html', 'w') as f:
        f.write(html)

homepage()