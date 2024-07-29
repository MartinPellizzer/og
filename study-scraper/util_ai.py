import json

from llama_cpp import Llama

llm = None
llm_loaded = False

# model_path = '/home/ubuntu/vault/llms/llama3-8b-instruct.q8_0.gguf'
mp = '/home/ubuntu/vault/llms/Meta-Llama-3-8B-Instruct.Q4_0.gguf'
# model_path = '/home/ubuntu/vault/llms/Mistral-Nemo-Instruct-2407.Q4_0.gguf'
# model_path = '/home/ubuntu/vault/llms/Mistral-Nemo-Instruct-2407.Q8_0.gguf'

#######################
# ;util
#######################

def gen_reply(prompt, model_path=mp):
    print(model_path)
    global llm
    global llm_loaded
    if not llm_loaded:
        llm = Llama(
            model_path = model_path,
            n_gpu_layers=-1,
            n_ctx = 8192,
        )
        llm_loaded = True
    stream = llm.create_chat_completion(
        messages = [
            {
                'role': 'user', 
                'content': prompt,
            },
        ],
        stream = True,
        temperature = 1.0,
    )
    reply = ''
    for piece in stream:
        if 'content' in piece['choices'][0]['delta'].keys():
            response_piece = piece['choices'][0]['delta']['content']
            reply += response_piece
            print(response_piece, end="", flush=True)
    return reply


def json_read(filepath):
    with open(filepath) as f:
        data = json.load(f)
    return data

