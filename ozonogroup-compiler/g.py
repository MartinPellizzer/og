
GOOGLE_TAG = '''
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-TV11JVJVKC"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', 'G-TV11JVJVKC');
    </script>
'''

PROMPT_DELAY_TIME = 30

ARTICLES_AUTHOR = 'Ozonogroup Staff'


CSV_SECTORS_FILEPATH = 'database/csv/sectors.csv'
CSV_APPLICATIONS_FILEPATH = 'database/csv/applications.csv'
CSV_EQUIPMENT_FILEPATH = 'database/csv/applications_equipment.csv'


# MAIN CSVS
CSV_BACTERIA_FILEPATH ='database/csv/bacteria.csv'
CSV_VIRUS_FILEPATH ='database/csv/virus.csv'

# JUNCTIONS CSVS
CSV_APPLICATIONS_STUDIES_FILEPATH = 'database/csv/applications_studies.csv'
CSV_APPLICATIONS_BACTERIA_FILEPATH = 'database/csv/junctions/applications_bacteria.csv'
CSV_APPLICATIONS_VIRUS_FILEPATH = 'database/csv/junctions/applications_virus.csv'
