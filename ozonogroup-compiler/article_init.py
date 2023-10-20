import os 
import sys 

print(len(sys.argv))
if len(sys.argv) != 2:
    print('ERR: missing INDUSTRY')
    quit()

industry = sys.argv[1]

# industry = 'viticoltura'

try: os.makedirs(f'database/tables/{industry}')
except: pass

try: os.makedirs(f'database/tables/{industry}/acqua-processo')
except: pass
try: os.makedirs(f'database/tables/{industry}/acque-reflue')
except: pass
try: os.makedirs(f'database/tables/{industry}/aria-ambienti')
except: pass
try: os.makedirs(f'database/tables/{industry}/patogeni')
except: pass
try: os.makedirs(f'database/tables/{industry}/superfici-lavoro')
except: pass

with open(f'database/tables/{industry}/acqua-processo/acqua-processo.csv', 'a') as f: pass
with open(f'database/tables/{industry}/acque-reflue/acque-reflue.csv', 'a') as f: pass
with open(f'database/tables/{industry}/aria-ambienti/aria-ambienti.csv', 'a') as f: pass
with open(f'database/tables/{industry}/patogeni/patogeni.csv', 'a') as f: pass
with open(f'database/tables/{industry}/superfici-lavoro/superfici-lavoro.csv', 'a') as f: pass

