import numpy as np
import pandas as pd

with open('keywords-master.txt', encoding='utf-8') as f:
    content = f.read()

words = content.replace('\n', ' ').split()

with open('blacklist.md', encoding='utf-8') as f:
    content = f.read()

words_blacklist = content.split(',')

# for word_blacklist in words_blacklist:
#     word_blacklist = word_blacklist.strip()
#     if not word_blacklist: continue
    # words = [ x for x in words if word_blacklist not in x.split() ]

# for word in words:
    # print(words)


# words = ['hello', 'goodbye', 'howdy', 'hello', 'hello', 'hi', 'bye']

df = pd.value_counts(np.array(words))
df.to_csv('out.csv')

# with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#     print(df)