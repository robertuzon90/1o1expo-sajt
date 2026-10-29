import sys,json;sys.path.insert(0,'/home/claude/de-build')
from units import *
SITE='/home/claude/1o1expo-sajt/'
PAGES=['about.html','legal.html','privacy.html','404.html','review.html','review-thanks.html','guides/index.html','guides/stand-types/index.html','guides/stand-brief/index.html','guides/stand-cost/index.html','guides/trade-fair-timeline/index.html','guides/trade-fair-calendar-2027/index.html','fairs/index.html']+[f'fairs/{s}/index.html' for s in ['ambiente-frankfurt','mwc-barcelona','hannover-messe','intersolar-europe','eurobike-frankfurt','gamescom-cologne','ifa-berlin','sbc-summit-lisbon','reneo-budapest','cphi-frankfurt']]
if __name__=='__main__':
    keys={}
    for p in PAGES:
        s=open(SITE+p).read();body=s[s.find('<body'):]
        parts,rs=runs(body)
        for r in rs:
            k,t,_,_=key_of(r)
            keys.setdefault(k,p)
    have={}
    import os
    if os.path.exists('/home/claude/de-build/tr.json'): have=json.load(open('/home/claude/de-build/tr.json'))
    todo=[k for k in sorted(keys) if k not in have]
    open('/home/claude/de-build/todo.txt','w').write('\n'.join(f'{i}\t{k}' for i,k in enumerate(todo)))
    json.dump(todo,open('/home/claude/de-build/todo.json','w'),ensure_ascii=False)
    print(len(keys),'todo',len(todo))
