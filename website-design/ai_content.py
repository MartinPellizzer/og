import time

import util
import util_ai

SLEEP_TIME = 30

content_rows = util.csv_get_rows('content/master-sheet.csv')
content_cols = util.csv_get_cols(content_rows)
content_rows = content_rows[1:]

for content_row in content_rows:
    sub_section = content_row[content_cols['sub_section']]
    sub_section_slug = sub_section.replace(' ', '-').strip().lower()

    filepath = f'content/{sub_section_slug}.txt'

    util.file_append(filepath, '')
    content = util.file_read(filepath)
    
    if content.strip() == '':
        prompt =  content_row[content_cols['prompt']].strip()
        
        if prompt.strip() != '':
            
        reply = util_ai.gen_reply(prompt)

        util.file_write(filepath, reply)

        time.sleep(SLEEP_TIME)
