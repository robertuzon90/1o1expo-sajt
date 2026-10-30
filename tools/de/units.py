import re
TOK=re.compile(r'(<script\b.*?</script>|<style\b.*?</style>|<!--.*?-->|<[^>]+>)',re.S|re.I)
INLINE=re.compile(r'^</?(a|b|strong|em|br|sup|sub|i)\b',re.I)
def split(s):
    return [p for p in TOK.split(s) if p!='']
def runs(s):
    """yield (start_index, end_index, parts) runs of text+inline tags in token list"""
    parts=split(s); out=[]; cur=[]
    def flush():
        if cur and any((not p.startswith('<')) and re.search(r'[A-Za-z]',p) for _,p in cur): out.append(list(cur))
        cur.clear()
    for i,p in enumerate(parts):
        if p.startswith('<'):
            low=p[:8].lower()
            if low.startswith('<script') or low.startswith('<style') or p.startswith('<!--'): flush(); continue
            if INLINE.match(p): cur.append((i,p)); continue
            flush()
        else: cur.append((i,p))
    flush()
    return parts,out
def key_of(run):
    # strip leading/trailing tags-only and whitespace; return key with {n} placeholders, tags list, lead, trail
    toks=[p for _,p in run]
    # trim leading/trailing pure tags that are unbalanced? keep all, simple
    tags=[];k=''
    for p in toks:
        if p.startswith('<'): k+='{%d}'%len(tags); tags.append(p)
        else: k+=p
    lead=re.match(r'^\s*',k).group(0); trail=re.search(r'\s*$',k).group(0)
    return k.strip(),tags,lead,trail
