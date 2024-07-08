import random
import json

import util

def stefan_hooks():
    with open('assets/prompts/stefan/hooks-0001-big-premise.txt') as f: 
        hooks_0001 = [line.strip() for line in f.read().strip().split('\n') if line.strip() != '']
    random.shuffle(hooks_0001)
    hooks = hooks_0001[:40]
    hooks = '\n'.join(hooks)

    prompt = f'''
        # HOOKS GENERATION
        Write a numbered list of 40 "hook" ideas using the following TEMPLATES and TOPIC.
        I want you to adapt the TOPIC to the TEMPLATES.
        
        # TEMPLATES
        {hooks}

        # TOPIC
        ecological sanitization in the food processing industry
    '''

    print(prompt)
    reply = util.gen_reply(prompt)


def ship30_ideas():
    with open(f'assets/prompts/ship30/approaches.txt') as f:
        approaches_list = [line for line in f.read().strip().split('\n') if line.strip() != '']
    random.shuffle(approaches_list)
    approaches = ', '.join(approaches_list[:30])

    prompt = f'''
        # IDEA GENERATION
        Write a numbered list of 30 headline ideas using the TOPIC, OUTCOME, and APPROACHES below.

        # TOPIC
        ecological sanitization in the food processing industry
        
        # OUTCOME
        to be compliant with regulations

        # APPROACHES
        {approaches}
    '''
    print(prompt)
    reply = util.gen_reply(prompt)

def ship30_headlines():
    topic = 'ecological sanitization'
    sector = 'food processing industry'
    sector_slug = sector.strip().lower().replace(' ', '-')

    with open(f'ozonogroup/data/sector/{sector_slug}/job-titles.txt') as f:
        audience_list = [line for line in f.read().strip().split('\n') if line.strip() != '']
    random.shuffle(audience_list)
    audiences = ', '.join(audience_list[:3])
    audience = random.choice(audience_list)

    with open(f'ozonogroup/data/sector/{sector_slug}/outcomes.txt') as f:
        outcome_list = [line for line in f.read().strip().split('\n') if line.strip() != '']
    random.shuffle(outcome_list)
    outcomes = ', '.join(outcome_list[:3])
    outcome = random.choice(outcome_list)

    with open(f'assets/prompts/ship30/approaches.txt') as f:
        approaches_list = [line for line in f.read().strip().split('\n') if line.strip() != '']
    random.shuffle(approaches_list)
    approaches = ', '.join(approaches_list[:3])

    prompt = f'''
        # HEADLINES GENERATOR
        Write 40 headlines by using random combinations of the TOPICS, AUDIENCES, SECTORS, and OUTCOMES below.
        The headlines must always include all the 5 components listed in the IRRESISTIBLE HEADLINE section below.
        Also follow the rules in the GUIDELINES section below.

        ## IRRESISTIBLE HEADLINE
        - how many (a number): 3, 5, 7, ect.
        - the who (an audience): {audiences}, etc.
        - the what (a noun): {approaches}, etc.
        - the why (a reason/outcome): {outcomes}, etc.
        - "twist the knife" (2-3 additional benefits/outcomes): {outcome_list[0]} and {outcome_list[1]}. 

        ## GUIDELINES
        - reply with only the headlines, don't add additional content

        ## TOPIC
        {topic}

        ## AUDIENCE
        {audience}

        ## SECTOR
        {sector}

        ## OUTCOMES
        {outcome}
    '''

    prompt = f'''
        # HEADLINES GENERATOR
        Write 40 headlines by using the TOPIC and SECTOR below.
        The headlines must include the 5 components listed in the IRRESISTIBLE HEADLINE section below.
        Also follow the rules in the GUIDELINES section below.

        ## IRRESISTIBLE HEADLINE
        - how many (a number): 3, 5, 7, ect.
        - the who (an audience): {audiences}, etc.
        - the what (a noun): {approaches}, etc.
        - the why (a reason/outcome): {outcomes}, etc.
        - "twist the knife" (2-3 additional benefits/outcomes): {outcome_list[0]} and {outcome_list[1]}. 

        ## GUIDELINES
        - reply with only the headlines, don't add additional content

        ## TOPIC
        {topic}

        ## SECTOR
        {sector}

    '''
    print(prompt)
        
    reply = util.gen_reply(prompt)


def gen_tweet(headline):
    prompt = f'''
        Great, I like this headline: {headline}
        Please write a bulleted list tweet based on this headline.
        Here are the rules:
        1. It must be 280 characters or less.
        2. No hashtags
        3. Start with 1 clear, declarative sentence.
        4. 3-5 bulleted list of actionable tips.
    '''
    print(prompt)
    reply = util.gen_reply(prompt)
    with open('ozonogroup/posts/post-0000/tweet.txt', 'w') as f:
        f.write(reply)
    
def gen_thread(headline):
    prompt = f'''
        Rewrite this headline as a Twitter Thread:
        {headline}
        A few rules:
        1. Make each tweet stand alone
        2. No hashtags
        3. Use this format:
        First sentence = name the "tip"
        3-5 bulleted list of how to actionably execute that tip
        If there's room, 1 final sentence encouraging the reader.
    '''
    print(prompt)
    reply = util.gen_reply(prompt)
    with open('ozonogroup/posts/post-0000/thread.txt', 'w') as f:
        f.write(reply)

def gen_linkedin(headline):
    prompt = f'''
        Rewrite this headline as an 800-word LinkedIn post
        {headline}
        A few rules:
        1. Start with a brief introduction of the topic, citing a statistic or data point and crediting the source
        2. Divide the post up into sections/a list
        3. Include at least 1 actionable tip and 1 mistake the reader should avoid in each section
    '''
    print(prompt)
    reply = util.gen_reply(prompt)
    with open('ozonogroup/posts/post-0000/linkedin.txt', 'w') as f:
        f.write(reply)

def gen_atomic_essay(headline):
    prompt = f'''
        Great, now rewrite this headline as an Atomic Essay:
        {headline}
        Atomic Essays are short essays 250 words or less.
        Here are a few guidelines:
        1. The first sentence of the essay must be short, to the point, and clearly tell the reader the "strong opinion" of the essay.
        2. The essay must be structured in a list of 3-7 Main Ideas.
        3. After each main idea must be a short description of that Main Idea. These descriptions should be some combination of the following: Reasons why this main idea is important, Mistakes people make when trying to implement this main idea, Tips to implement this main idea, Examples of this main idea, Stats that prove this main idea, etc. 
        4. Do not use flowery language or vague examples. Be as specific as possible.
    '''
    print(prompt)
    reply = util.gen_reply(prompt)
    with open('ozonogroup/posts/post-0000/atomic_essay.txt', 'w') as f:
        f.write(reply)

def gen_blog_post(headline):
    prompt = f'''
        Great, now create an outline for a long-form blog post with this headline:
        {headline}
        A few rules:
        1. Organize the outline into main points
        2. For each main point, list out 1 actionable tip, 1 mistake, and 1 stat with a source
        3. And for each main point, also list out 2 relevant case studies or well-known stories to reference
    '''
    print(prompt)
    reply = util.gen_reply(prompt)
    with open('ozonogroup/posts/post-0000/blog_post.txt', 'w') as f:
        f.write(reply)

ship30_ideas()
# ship30_headlines()

quit()

gen_tweet(headline)
gen_thread(headline)
gen_linkedin(headline)
gen_atomic_essay(headline)
gen_blog_post(headline)



# TODO: gen the following avatar
def gen_avatar(topic, target):
    '''
        avatar = target + topic
        target: job title in specific industry
        topic: (aka product/service), ecological sanitization? ozone sanitization?
    '''
    with open('assets/prompts/buyer-persona.txt') as f: prompt = f.read()
    prompt = prompt.replace('[Target Market]=', f'[Target Market]={target}')
    prompt = prompt.replace('[Product]=', f'[Product]={topic}')

    reply = util.gen_reply(prompt)
    target_slug = target.strip().lower().replace(' ', '-')
    with open(f'ozonogroup/data/audience/avatar-{target_slug}.txt', 'w') as f: f.write(reply)

'''
gen_avatar(
    target = 'quality assurance managers in the food processing industry',
    topic = 'ecological sanitization'
)
'''

# gen_hooks()
