import util

def article_init():
    industry = 'ittica'
    sector = 'ittico'
    applications_folder = 'articles/public/ozono/sanificazione/applicazioni'
    
    industry_dash = industry.replace(' ', '-')
    
    filepath = f'{applications_folder}/{industry_dash}.md'
    content = util.file_read(filepath)

    content = content.strip()
    # if content == '':
    content = ''
    content += f"# Sanificazione ad ozono nell'industria {industry}: cos'è, problemi, benefici e applicazioni\n\n"
    content += f"![Ozono Sanificazione Industria {industry.title()}](/assets/images/ozono-sanificazione-industria-{industry_dash}.jpg)\n\n"
    content += f"<!-- content -->\n\n"
    content += f"## Cos'è la sanificazione ad ozono nell'industria {industry} e a cosa serve?\n\n"
    content += f"<!-- content -->\n\n"
    content += f"![Ozono Sanificazione Industria {industry.title()} Definizione](/assets/images/ozono-sanificazione-industria-{industry_dash}-definizione.jpg)\n\n"
    content += f"## Quali problemi risolve la sanificazione ad ozono nel settore {sector}?\n\n"
    content += f"<!-- content -->\n\n"
    content += f"![Ozono Sanificazione Industria {industry.title()} Problemi](/assets/images/ozono-sanificazione-industria-{industry_dash}-problemi.jpg)\n\n"
    content += f"La seguente lista elenca i problemi principali di contaminazione che l'ozono può risolvere nel settore {sector}.\n\n- Batteri\n- Virus\n- Muffe\n- Parassiti\n- Odori\n\n"
    content += f"### Batteri\n\n"
    content += f"<!-- content -->\n\n"
    content += f"I batteri più comuni presenti settore {sector} che si possono eliminare con l'ozono sono elencati nella seguente lista.\n\n"
    content += f"<!-- list -->\n\n"
    content += f"### Virus\n\n"
    content += f"<!-- content -->\n\n"
    content += f"I virus più comuni presenti settore {sector} che si possono inattivare con l'ozono sono elencati nella seguente lista.\n\n"
    content += f"<!-- list -->\n\n"
    content += f"### Muffe\n\n"
    content += f"<!-- content -->\n\n"
    content += f"Le muffe più comuni presenti settore {sector} che si possono ossidare con l'ozono sono elencati nella seguente lista.\n\n"
    content += f"<!-- list -->\n\n"
    content += f"### Parassiti\n\n"
    content += f"<!-- content -->\n\n"
    content += f"I parassiti più comuni presenti settore {sector} che si possono repellere con l'ozono sono elencati nella seguente lista.\n\n"
    content += f"<!-- list -->\n\n"
    content += f"### Odori\n\n"
    content += f"<!-- content -->\n\n"
    content += f"Gli odori più comuni presenti nel settore {sector} che si possono disgregare con l'ozono sono elencati nella seguente lista.\n\n"
    content += f"<!-- list -->\n\n"
    content += f"## Quali sono i benefici della sanificazione ad ozono nell'industria {industry}?\n\n"
    content += f"<!-- content -->\n\n"
    content += f"![Ozono Sanificazione Industria {industry.title()} Benefici](/assets/images/ozono-sanificazione-industria-{industry_dash}-benefici.jpg)\n\n"
    content += f"La seguente lista elenca i principali benefici della sanificazione ad ozono nell'industria {industry}.\n\n"
    content += f"<!-- list -->\n\n"
    content += f"## Quali sono le applicazioni della sanificazione ad ozono nel settore {sector}?\n\n"
    content += f"<!-- content -->\n\n"
    content += f"![Ozono Sanificazione Industria {industry.title()} Applicazioni](/assets/images/ozono-sanificazione-industria-{industry_dash}-applicazioni.jpg)\n\n"
    content += f"Qui sotto trovi una lista dettagliata delle principali applicazioni della sanificazione ad ozono nel settore {sector}.\n\n"
    content += f"<!-- list -->\n\n"
    content += f"\n\n"



    util.file_write(filepath, content)





article_init()

# llm = AutoModelForCausalLM.from_pretrained(
#     "C:\\Users\\admin\\Desktop\\models\\neural-chat-7b-v3-1.Q8_0.gguf", 
#     model_type="mistral", 
#     context_length=256, 
#     max_new_tokens=512, 
#     temperature=1, 
#     repetition_penalty=1.5
#     )

# def generate_reply(prompt):
#     print(f"Q: ---")
#     print(prompt)
#     print()
#     print("A: ---")
#     reply = ''
#     for text in llm(prompt, stream=True):
#         reply += text
#         print(text, end="", flush=True)
#     print()
#     print()
#     return reply

# prompt = f'''
#     Write a 5-sentence 60-word paragraph about ozone sanitization in the dairy industry.
# '''

# reply = generate_reply(prompt)
