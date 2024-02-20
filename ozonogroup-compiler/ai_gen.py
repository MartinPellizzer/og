from ctransformers import AutoModelForCausalLM

llm = AutoModelForCausalLM.from_pretrained(
    "C:\\Users\\admin\\Desktop\\models\\neural-chat-7b-v3-1.Q8_0.gguf", 
    model_type="mistral", 
    context_length=256, 
    max_new_tokens=512, 
    temperature=1, 
    repetition_penalty=1.5
    )


def generate_reply(prompt):
    print(f"Q: ---")
    print(prompt)
    print()
    print("A: ---")
    reply = ''
    for text in llm(prompt, stream=True):
        reply += text
        print(text, end="", flush=True)
    print()
    print()
    return reply

prompt = f'''
    Write a 5-sentence 60-word paragraph about ozone sanitization in the dairy industry.
'''

reply = generate_reply(prompt)
