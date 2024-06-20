from groq import Groq


import util

# api_key = util.file_read('C:/api/groq.txt')

# client = Groq(
#     api_key=api_key,
# )



MODELS = [
    'C:\\Users\\admin\\Desktop\\models\\mistral-7b-instruct-v0.2.Q8_0.gguf',
]
MODEL = MODELS[0]



# def gen_reply_api(prompt):
#     prompt_normalized = prompt_normalize(prompt)

#     completion = client.chat.completions.create(
#         messages=[
#             {
#                 "role": "user",
#                 "content": prompt_normalized,
#             }
#         ],
#         model="mixtral-8x7b-32768",
#         # model="llama3-70b-8192",
#         temperature=1,
#         max_tokens=2048,
#     )

#     reply = completion.choices[0].message.content
#     print()
#     print()
#     print()
#     print("Q:")
#     print()
#     print(prompt)
#     print()
#     print("A:")
#     print()
#     print(reply)
#     print()
#     return reply


def gen_reply_local(prompt):
    from ctransformers import AutoModelForCausalLM
    
    llm = AutoModelForCausalLM.from_pretrained(
        MODEL,
        model_type="mistral", 
        context_length=2048, 
        max_new_tokens=2048,
        )

    print()
    print("Q:")
    print()
    print(prompt)
    print()
    print("A:")
    print()
    reply = ''
    for text in llm(prompt, stream=True):
        reply += text
        print(text, end="", flush=True)
    print()
    print()
    return reply


def gen_reply(prompt):
    reply = ''
    # try: reply = gen_reply_api(prompt)
    # except: 
    #     print(
    #         '''
    #         ********************************************************************
    #         ERROR API: WAITING FOR SOME MINUTES... THEN RETRY...
    #         ********************************************************************
    #         '''
    #     )
        # time.sleep(600)
    reply = gen_reply_local(prompt)

    return reply


def prompt_normalize(prompt):
    return '\n'.join([line.strip() for line in prompt.split('\n') if line.strip() != ''])



def reply_list_to_paragraph(reply):
    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue

        if not line[0].isdigit(): continue
        if '. ' not in line: continue
        else: line = '. '.join(line.split('. ')[1:]).strip()
        
        reply_formatted.append(line)

    return ' '.join(reply_formatted)


def text_to_paragraph(reply):
    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue

        if line[0].isdigit(): 
            if '. ' in line: 
                line = '. '.join(line.split('. ')[1:]).strip()
        
        reply_formatted.append(line.strip())

    return ' '.join(reply_formatted)




