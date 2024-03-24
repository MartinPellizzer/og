from groq import Groq

client = Groq(
    api_key='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',
)


def prompt_normalize(prompt):
    return '\n'.join([line.strip() for line in prompt.split('\n') if line.strip() != ''])


def gen_reply(prompt):
    prompt_normalized = prompt_normalize(prompt)

    completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt_normalized,
            }
        ],
        model="mixtral-8x7b-32768",
    )

    reply = completion.choices[0].message.content
    print()
    print()
    print()
    print("Q:")
    print()
    print(prompt)
    print()
    print("A:")
    print()
    print(reply)
    print()
    return reply


def list_to_paragraph(reply):
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




