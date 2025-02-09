import os
import json
import random

import chromadb
from chromadb.utils import embedding_functions

from oliark_io import json_read, json_write
from oliark_llm import llm_reply

vault_tmp = '/home/ubuntu/vault-tmp'
collection_name = 'listeria'

vertices_filepath = f'vertices.json'
vertices = json_read(vertices_filepath)

model = f'{vault_tmp}/llms/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf'
model_validator_filepath = f'{vault_tmp}/llms/Llama-3-Partonus-Lynx-8B-Intstruct-Q4_K_M.gguf'

'''
vertex_new = {
    'entity_type': 'contamination',
    'entity_category': 'bacteria',
    'entity_slug': 'listeria-monocytogenes',
    'entity_name_scientific': 'listeria monocytogenes',
    'entity_name_common': 'listeria',
}
'''

'''
vertices_slugs = [vertex['entity_slug'] for vertex in vertices]
if vertex_new['entity_slug'] not in vertices_slugs:
    vertices.append(vertex_new)
    # json_write('vertices.json', vertices)
    j = json.dumps(vertices, indent=4)
    with open('vertices.json', 'w') as f:
        print(j, file=f)

prompt = f'''
    
'''

'''

for vertex in vertices:
    contamination_slug = vertex['contamination_slug']
    contamination_name_scientific = vertex['contamination_name_scientific']
    key = 'foods'
    if key not in vertex: vertex[key] = []
    vertex[key] = []
    if vertex[key] == []:
        outputs = []
        tries_num = 100
        for i in range(tries_num):
            print(f'{i}/{tries_num}')
            rand_list_items = random.randint(7, 13)
            prompt = f'''
                Write a list of the {rand_list_items} foods names that are at most risk to be contaminate with {contamination_name_scientific}.
                Write each list item using only 1 word.
                Also, write a confidence score from 1 to 10 for each list item, indicating how much you believe that answer is correct.
                Use as few words as possible.
                Reply with the following JSON format:
                [
                    {{"name": "write name 1 here", "score": 10}},
                    {{"name": "write name 2 here", "score": 5}},
                    {{"name": "write name 3 here", "score": 7}}
                ]
                Reply only with the JSON.
                Reply in Italian.
            '''
            reply = llm_reply(prompt)
            try: json_reply = json.loads(reply)
            except: json_reply = {}
            if json_reply != {}:
                for item_reply in json_reply:
                    try: name = item_reply['name'].strip().lower()
                    except: continue
                    try: score = int(item_reply['score'])
                    except: continue
                    found = False
                    for output in outputs:
                        if output['name'] == name:
                            output['score'] += score
                            output['mentions'] += 1
                            output['score_tot'] = output['score'] * output['mentions']
                            found = True
                            break
                    if not found:
                        outputs.append({
                            'name': name, 
                            'score': score, 
                            'mentions': 1,
                            'score_tot': score / 1,
                        })
        outputs = sorted(outputs, key=lambda x: x['score_tot'], reverse=True)
        for output in outputs:
            print(output)
        for output in outputs[:]:
            vertex[key] = outputs
            j = json.dumps(vertices, indent=4)
            with open(vertices_filepath, 'w') as f:
                print(j, file=f)
        quit()

quit()
db_path = f'{vault_tmp}/og/chroma'
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name='all-mpnet-base-v2', 
    device='cuda',
)
chroma_client = chromadb.PersistentClient(path=db_path)

def retrieve_docs(query):
    collection = chroma_client.get_or_create_collection(
        name=collection_name, 
        embedding_function=sentence_transformer_ef,
    )
    n_results = 100
    results = collection.query(query_texts=[query], n_results=n_results)
    documents = results['documents'][0]
    metadatas = results['metadatas'][0]
    return documents, metadatas

def llm_validate(question, context, answer):
    prompt = f'''
    Given the following QUESTION, DOCUMENT and ANSWER you must analyze the provided answer and determine whether it is faithful to the contents of the DOCUMENT. The ANSWER must not offer new information beyond the context provided in the DOCUMENT. The ANSWER also must not contradict information provided in the DOCUMENT. Output your final verdict by strictly following this format: "PASS" if the answer is faithful to the DOCUMENT and "FAIL" if the answer is not faithful to the DOCUMENT. Show your reasoning.

    --
    QUESTION (THIS DOES NOT COUNT AS BACKGROUND INFORMATION):
    {question}

    --
    DOCUMENT:
    {context}

    --
    ANSWER:
    {answer}

    --

    Your output should be in JSON FORMAT with the keys "REASONING" and "SCORE":
    {{"REASONING": <your reasoning as bullet points>, "SCORE": <your final score>}}
    '''
    reply = llm_reply(prompt, model_validator_filepath, max_tokens=512)
    return reply

prompt = f''
reply = llm_reply(prompt, model, max_tokens=256)

def gen_vertex_attr_lst_from_studies(key, query, question, prompt_var):
    outputs = []
    documents, metadatas = retrieve_docs(query)
    for document in documents[:100]:
        for i in range(10):
            prompt = prompt_var
            prompt += f'''
                Use as few words as possible.
                Reply in numbered list format.
                Don't hallucinate.
                DOCUMENT: {document}
            '''
            print(document)
            print(prompt)
            reply = llm_reply(prompt, model, max_tokens=256)
            validator_reply = llm_validate(question, document, reply)
            try: validator_obj = json.loads(validator_reply)
            except: 
                print('*******************************')
                print('*** bad json or "not available" answer')
                print('*******************************')
                continue
            score = validator_obj['SCORE']
            if score == 'PASS':
                if 'none' in reply.lower():
                    print('*******************************')
                    print('*** pass but none')
                    print('*******************************')
                    continue
                lines = []
                for line in reply.split('\n'):
                    line = line.strip()
                    if line == '': continue
                    if not line[0].isdigit(): continue
                    if '. ' not in line: continue
                    line = '. '.join(line.split('. ')[1:])
                    line = line.strip()
                    if line == '': continue
                    lines.append(line)
                for line in lines:
                    line = line.lower().strip()
                    found = False
                    for output in outputs:
                        if line in output['name']: 
                            output['mentions'] += 1
                            found = True
                            break
                    if not found:
                        outputs.append({
                            'name': line, 
                            'mentions': 1, 
                        })
                break
            elif score == 'FAIL':
                print('*******************************')
                print('*** fail score')
                print('*******************************')
                continue
            else: 
                print('*******************************')
                print('*** bad something')
                print('*******************************')
                continue
            break
    outputs = sorted(outputs, key=lambda x: x['mentions'], reverse=True)
    print('***********************')
    print('***********************')
    print('***********************')
    for output in outputs:
        print(output)
    outputs_filtered = [output for output in outputs if output['mentions'] >= 3]
    print('***********************')
    print('***********************')
    print('***********************')
    vertex[key] = outputs_filtered[:20]
    j = json.dumps(vertices, indent=4)
    with open('vertices.json', 'w') as f:
        print(j, file=f)

def gen_vertex_attr_lst():
    pass

for vertex in vertices:
    entity_type = vertex['entity_type']
    entity_category = vertex['entity_category']
    entity_slug = vertex['entity_slug']
    entity_name_scientific = vertex['entity_name_scientific']
    entity_name_common = vertex['entity_name_common']
    
    if 0:
        # symtoms
        if 'symptoms' not in vertex: vertex['symptoms'] = []
        # vertex['symptoms'] = []
        if vertex['symptoms'] == []:
            outputs = []
            query = f'{entity_name_scientific} symptoms'
            question = f'what are the symptoms of {entity_name_scientific}?'
            documents, metadatas = retrieve_docs(query)
            for document in documents[:100]:
                for i in range(10):
                    prompt = f'''
                        Write all the names of the symptoms that are caused by {entity_name_scientific} mentioned in the following DOCUMENT. 
                        If the document doesn't mention symptoms caused by {entity_name_scientific}, reply only with: "not available".
                        Reply with only the names of the symptoms.
                        Use as few words as possible.
                        Reply in numbered list format.
                        Don't hallucinate.
                        DOCUMENT: {document}
                    '''
                    print(prompt)
                    reply = llm_reply(prompt, model, max_tokens=256)
                    validator_reply = llm_validate(question, document, reply)
                    try: validator_obj = json.loads(validator_reply)
                    except: 
                        print('*******************************')
                        print('*** bad json or "not available" answer')
                        print('*******************************')
                        continue
                    score = validator_obj['SCORE']
                    if score == 'PASS':
                        if 'none mentioned' in reply:
                            print('*******************************')
                            print('*** pass but none')
                            print('*******************************')
                            continue
                        lines = []
                        for line in reply.split('\n'):
                            line = line.strip()
                            if line == '': continue
                            if not line[0].isdigit(): continue
                            if '. ' not in line: continue
                            line = '. '.join(line.split('. ')[1:])
                            line = line.strip()
                            if line == '': continue
                            lines.append(line)
                        for line in lines:
                            line = line.lower().strip()
                            found = False
                            for output in outputs:
                                if line in output['name']: 
                                    output['mentions'] += 1
                                    found = True
                                    break
                            if not found:
                                outputs.append({
                                    'name': line, 
                                    'mentions': 1, 
                                })
                        break
                    elif score == 'FAIL':
                        print('*******************************')
                        print('*** fail score')
                        print('*******************************')
                        continue
                    else: 
                        print('*******************************')
                        print('*** bad something')
                        print('*******************************')
                        continue
                    break
            outputs = sorted(outputs, key=lambda x: x['mentions'], reverse=True)
            print('***********************')
            print('***********************')
            print('***********************')
            for output in outputs:
                print(output)
            outputs_filtered = [output for output in outputs if output['mentions'] >= 3]
            print('***********************')
            print('***********************')
            print('***********************')
            vertex['symptoms'] = outputs_filtered[:20]
            j = json.dumps(vertices, indent=4)
            with open('vertices.json', 'w') as f:
                print(j, file=f)

    if 0:
        key = 'foods'
        query = f'{entity_name_scientific} foods'
        question = f'in what foods you can find {entity_name_scientific}?'
        gen_vertex_attr_lst_from_studies(
            key, 
            query, 
            question,
            prompt_var = f'''
                Write all the names of the foods with {entity_name_scientific} mentioned in the following DOCUMENT. 
                If the document doesn't mention foods with {entity_name_scientific}, reply only with: "none".
                Reply with only the names of the foods.
            '''
            )

    key = 'treatments'
    if key not in vertex: vertex[key] = []
    # vertex[key] = []
    if vertex[key] == []:
        outputs = []
        for _ in range(100):
            lst_num_rnd = random.randint(7, 13)
            prompt = f'''
                Write a list of the {lst_num_rnd} most used treatments for {entity_name_scientific} in the food processing industry.
                Write each list item in 1 or 2 words.
                Also, write a confidence score from 1 to 10 for each list item, indicating how sure you are about the answer.
                Reply using the structure of the followng JSON:
                [
                    {{"name": "<write name 1 here>", "confidence_score": 10}},
                    {{"name": "<write name 2 here>", "confidence_score": 5}},
                    {{"name": "<write name 3 here>", "confidence_score": 7}}
                ]
                Write only the JSON.
            '''
            reply = llm_reply(prompt)
            try: json_reply = json.loads(reply)
            except: json_reply = {}    
            if json_reply != {}:
                for json_reply_item in json_reply:
                    try: name = json_reply_item['name'].strip().lower()
                    except: continue
                    try: confidence_score = json_reply_item['confidence_score']
                    except: continue
                    found = False
                    for output in outputs:
                        if name == output['name']:
                            found = True
                            output['mentions'] += 1
                            output['confidence_score'] += confidence_score
                            output['total_score'] = output['confidence_score'] * output['mentions']
                    if not found:
                        outputs.append({
                            'name': name,
                            'confidence_score': confidence_score,
                            'mentions': 1,
                            'total_score': confidence_score * 1,
                        })
        outputs = sorted(outputs, key=lambda x: x['total_score'], reverse=True)
        for output in outputs:
            print(output)
        vertex['treatments'] = outputs[:20]
        j = json.dumps(vertices, indent=4)
        with open('vertices.json', 'w') as f:
            print(j, file=f)

    key = 'foods'
    if key not in vertex: vertex[key] = []
    vertex[key] = []
    if vertex[key] == []:
        outputs = []
        for _ in range(100):
            lst_num_rnd = random.randint(7, 13)
            prompt = f'''
                Write a list of the {lst_num_rnd} most common foods names where you find {entity_name_scientific} in the food processing industry.
                Write each list item using only 1 words.
                Also, write a confidence score from 1 to 10 for each list item, indicating how sure you are about the answer.
                Reply using the structure of the followng JSON:
                [
                    {{"name": "<write name 1 here>", "confidence_score": 10}},
                    {{"name": "<write name 2 here>", "confidence_score": 5}},
                    {{"name": "<write name 3 here>", "confidence_score": 7}}
                ]
                Write only the JSON.
                Write te names of foods in italian.
            '''
            reply = llm_reply(prompt)
            try: json_reply = json.loads(reply)
            except: json_reply = {}    
            if json_reply != {}:
                for json_reply_item in json_reply:
                    try: name = json_reply_item['name'].strip().lower()
                    except: continue
                    try: confidence_score = json_reply_item['confidence_score']
                    except: continue
                    found = False
                    for output in outputs:
                        if name == output['name']:
                            found = True
                            output['mentions'] += 1
                            output['confidence_score'] += confidence_score
                            output['total_score'] = output['confidence_score'] * output['mentions']
                    if not found:
                        outputs.append({
                            'name': name,
                            'confidence_score': confidence_score,
                            'mentions': 1,
                            'total_score': confidence_score * 1,
                        })
        outputs = sorted(outputs, key=lambda x: x['total_score'], reverse=True)
        for output in outputs:
            print(output)
        vertex[key] = outputs[:20]
        j = json.dumps(vertices, indent=4)
        with open('vertices.json', 'w') as f:
            print(j, file=f)



