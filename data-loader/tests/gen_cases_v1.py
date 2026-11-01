# gen_cases_v1.py -- 20,014 numbers as text, each with hp-prime-kit's 8-byte encoding of it: cases_v1.json,
# which test_core_v1.js compares with the page's encoder.  Needs hp-prime-kit ($HPKIT).
# Run: HPKIT=PATH python3 gen_cases_v1.py
import random, json, sys, os
sys.path.insert(0, os.environ.get('HPKIT', '/tmp/kit/hp-prime-kit-HEAD'))
from hpkit.numbers import encode
rng=random.Random(31)
cases=[]
def fmt(v): return v
for i in range(20000):
    nd=rng.randint(1,12)
    digits=str(rng.randint(10**(nd-1), 10**nd-1))
    e=rng.randint(-300,300)
    style=i%4
    sign='-' if rng.random()<0.4 else ''
    if style==0: s=sign+digits[0]+('.'+digits[1:] if len(digits)>1 else '')+'E'+str(e)
    elif style==1:
        # plain decimal with a point somewhere
        p=rng.randint(0,len(digits)); s=sign+(digits[:p] or '0')+'.'+digits[p:]+'0'*rng.randint(0,3)
    elif style==2: s=sign+digits
    else: s=sign+'0.'+'0'*rng.randint(0,8)+digits
    cases.append([s, encode(float(s)).hex()])
for s in ['0','-0','0.0','1','-1','0.1','52','45.85','1E499','9.99999999999E499','1E-499','123456789012','-7.6E1','0.0006']:
    # 1E-499 is below a double: float() makes it 0, so the kit's encoding of the float is not comparable
    if float(s) == 0 and any(ch in '123456789' for ch in s.split('E')[0]):
        cases.append([s, 'ERR']); continue
    try: cases.append([s, encode(float(s)).hex()])
    except Exception as ex: cases.append([s, 'ERR'])
json.dump(cases, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cases_v1.json'),'w'))
print(len(cases))
