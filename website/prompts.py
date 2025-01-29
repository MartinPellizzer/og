from oliark_llm import llm_reply

prompt = f'''
    here's one important factor about food safety in the food processing industry: contaminated surfaces where food comes in contact with. I have to explain the following about the above mentioned factor:
    - what (what it is, what's involved, what's at stake)
    - why (why it's important, why you're limited, why it works)
    - how (to do it - step by step of "factors to consider")
    - tie down (commitment, exclamation mark comment, conclusion, challenge)
'''
reply = llm_reply(prompt)
