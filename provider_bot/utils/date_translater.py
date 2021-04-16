import re

datedict = {}

with open('./provider_bot/utils/datedict.txt') as f:
    for l in f.readlines():
        k, v = l.split(' ')
        datedict[k.strip()] = v.strip()

def translate_dates(txt: str):
    for k, v in datedict.items():
        r = re.compile(re.escape(k), re.IGNORECASE)
        txt = r.sub(v, txt)
    return txt

