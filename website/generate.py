import os
import json

import chromadb
from chromadb.utils import embedding_functions

from oliark_io import json_read, json_write
from oliark_llm import llm_reply

AUTHOR_NAME = 'Martin Pellizzer'

proj = 'ozonogroup'
pathogen_name = 'listeria'
query = 'what illnesses listeria causes?'
collection_name = 'listeria'
vault = '/home/ubuntu/vault'
vault_tmp = '/home/ubuntu/vault-tmp'

model = f'{vault_tmp}/llms/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf'
model_validator_filepath = f'{vault_tmp}/llms/Llama-3-Partonus-Lynx-8B-Intstruct-Q4_K_M.gguf'

db_path = f'{vault_tmp}/terrawhisper/chroma'
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

if 0:


    documents, metadatas = retrieve_docs(query)
    outputs = []
    documents = documents[:100]
    for document in documents:
        for i in range(10):
            question = f'''
                Write all the names of the illnesses that are caused by {pathogen_name} mentioned in the following DOCUMENT. 
                Reply with only the names of the illnesses.
                If the study doesn't mention illnesses caused by {pathogen_name}, reply only with: "None mentioned".
            '''
            prompt = f'''
                {question}
                Reply in numbered list format.
                Don't hallucinate.
                DOCUMENT: {document}
            '''
            reply = llm_reply(prompt, model, max_tokens=256)

            validator_reply = llm_validate(question, document, reply)
            try: validator_obj = json.loads(validator_reply)
            except: 
                print('bad json')
                continue
            score = validator_obj['SCORE']
            if score == 'PASS':
                if 'none mentioned' in reply:
                    print('pass but none')
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
                print('fail score')
                continue
            else: 
                print('bad something')
                continue
            break

    outputs = sorted(outputs, key=lambda x: x['mentions'], reverse=True)
    print('***********************')
    print('***********************')
    print('***********************')
    for output in outputs:
        print(output)
    print('***********************')
    print('***********************')
    print('***********************')
    '''
    data[key] = output_plants
    json_write(f'{jsons_folderpath}/{ailment_slug}.json', data)
    '''

def head_html_generate(title, css_filepath):
    head_html = f'''
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="author" content="{AUTHOR_NAME}">
            <link rel="stylesheet" href="{css_filepath}">
            <title>{title}</title>
        </head>
    '''
    return head_html

def a_contamination(entity_slug):
    entity_name = entity_slug.replace('-', ' ')

    json_data_filepath = f'library/json-data/{entity_slug}.json'
    json_data = json_read(json_data_filepath, create=True)
    json_data['entity_slug'] = entity_slug
    json_data['entity_name'] = entity_name
    json_write(json_data_filepath, json_data)

    key = 'entity_category'
    if key not in json_data: json_data[key] = []
    # json_data[key] = []
    if json_data[key] == []:
        outputs = []
        for i in range(20):
            prompt = f'''
                Write which type of contamination is {entity_name}.
                Examples of types of contaminations are: bacteria, virus, etc.
                Also, tell give a confidence score from 1 to 10, indicating how sure you are about your answer.
                Use as few words as possible.
                Don't write fluff, only proven facts.
                Don't allucinate.
                Reply in the following JSON format: 
                [
                    {{"type": <write the type of contamination here>, "confidence_score": 8}} 
                ]
                Only reply with the JSON, don't add additional info.
                Don't include notes, reply ONLY with the JSON.
            '''
            reply = llm_reply(prompt, model).strip()
            reply_data = {}
            try: reply_data = json.loads(reply)
            except: pass 
            if reply_data != {}:
                _objs = []
                for item in reply_data:
                    try: val = item['type']
                    except: 
                        print('FAILEDE: name ********************')
                        continue
                    try: score = item['confidence_score']
                    except: 
                        print('FAILEDE: score ********************')
                        continue
                    _objs.append({
                        "val": val, 
                        "score": score,
                    })
                for _obj in _objs:
                    val = _obj['val']
                    score = _obj['score']
                    found = False
                    for output in outputs:
                        # print(output)
                        # print(val, '->', output['constituent_name'])
                        if val in output['val']: 
                            output['mentions'] += 1
                            output['confidence_score'] += int(score)
                            found = True
                            break
                    if not found:
                        outputs.append({
                            'val': val, 
                            'mentions': 1, 
                            'confidence_score': int(score), 
                        })
        outputs_final = []
        for output in outputs:
            outputs_final.append({
                'val': output['val'],
                'mentions': int(output['mentions']),
                'confidence_score': int(output['confidence_score']),
                'total_score': int(output['mentions']) * int(output['confidence_score']),
            })
        outputs_final = sorted(outputs_final, key=lambda x: x['confidence_score'], reverse=True)
        print('***********************')
        print('***********************')
        print('***********************')
        for output in outputs_final:
            print(output)
        print('***********************')
        print('***********************')
        print('***********************')
        json_data[key] = outputs_final[0]
        json_write(json_data_filepath, json_data)

    key = 'entity_symptoms'
    if key not in json_data: json_data[key] = []
    # if key in json_data: json_data[key] = []
    if json_data[key] == []:
        outputs = []
        query = f'{entity_name} symptoms'
        question = f'what are the symptoms of {entity_name}?'
        documents, metadatas = retrieve_docs(query)
        for document in documents[:100]:
            for i in range(10):
                prompt = f'''
                    Write all the names of the symptoms that are caused by {entity_name} mentioned in the following DOCUMENT. 
                    If the document doesn't mention symptoms caused by {entity_name}, reply only with: "not available".
                    Reply with only the names of the symptoms.
                    Use as few words as possible.
                    Reply in numbered list format.
                    Don't hallucinate.
                    DOCUMENT: {document}
                '''
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
        print('***********************')
        print('***********************')
        print('***********************')
        json_data[key] = outputs[:20]
        json_write(json_data_filepath, json_data)

    key = 'entity_foods'
    if key not in json_data: json_data[key] = []
    if key in json_data: json_data[key] = []
    if json_data[key] == []:
        outputs = []
        query = f'{entity_name} foods'
        question = f'In which foods {entity_name} is found?'
        documents, metadatas = retrieve_docs(query)
        for document in documents[:100]:
            for i in range(10):
                prompt = f'''
                    Write all the names of the foods where you find {entity_name} mentioned in the following DOCUMENT. 
                    If the document doesn't mention foods where you find {entity_name}, reply only with: "not available".
                    Reply with only the names of the foods.
                    Use as few words as possible.
                    Reply in numbered list format.
                    Don't hallucinate.
                    DOCUMENT: {document}
                '''
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
        print('***********************')
        print('***********************')
        print('***********************')
        json_data[key] = outputs[:20]
        json_write(json_data_filepath, json_data)



a_contamination('listeria-monocytogenes')
