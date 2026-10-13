import json, re, html, hashlib, os
from pathlib import Path
from html.parser import HTMLParser
B=Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-macro-range-preproof-review58')
C=Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-macro-range-sourcegraph58')
P=Path('E:/Samplinglib/runs/20261007-companion-priority/phase-pbps-gamma-preread57')
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def h(b):return hashlib.sha256(b).hexdigest()
primary=(B/'primary.exactraw.snapshot.html').read_bytes()
coverage=load(C/'source-coverage.json')
class Parse(HTMLParser):
    def __init__(self,s):
        super().__init__(convert_charrefs=False);self.s=s;self.stack=[];self.records=[]
        self.lines=[0]
        for m in re.finditer('\n',s):self.lines.append(m.end())
    def pos(self):
        line,col=self.getpos();return self.lines[line-1]+col
    def handle_starttag(self,t,attrs):
        a=dict(attrs);cls=a.get('class','').split();p=self.pos()
        selected=(t=='p' and 'ltx_p' in cls) or any(c in cls for c in ['ltx_equation','ltx_theorem','ltx_proof','ltx_cite']) or t=='math'
        r=dict(tag=t,id=a.get('id'),classes=cls,start=p,selected=selected)
        if t not in ['br','wbr','hr','img','meta','link','input','source','area','col','embed','param']:
            self.stack.append(r)
    def handle_endtag(self,t):
        end=self.s.find('>',self.pos())+1
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i]['tag']==t:
                removed=self.stack[i:];self.stack=self.stack[:i]
                for r in removed:
                    if r['selected']:
                        r['end']=end;r['byte_start']=len(self.s[:r['start']].encode('utf-8'));r['byte_end']=len(self.s[:end].encode('utf-8'));self.records.append(r)
                break
results=[]
for filename in sorted({r['source_file'] for r in coverage['regions']}):
    raw=(P/filename).read_bytes();assert raw in primary,filename
    (B/filename).write_bytes(raw)
    parser=Parse(raw.decode('utf-8'));parser.feed(parser.s)
    expected={(r['source_span_byte_start'],r['source_span_byte_end']):r for r in coverage['regions'] if r['source_file']==filename}
    own={(r['byte_start'],r['byte_end']):r for r in parser.records}
    for key,r in expected.items():
        assert h(raw[key[0]:key[1]])==r['source_span_raw_sha256'],r['region_id']
        assert r['disposition'] in ['NODE','EXCLUDED'] and r['reason']
        if r['disposition']=='NODE':assert r['nodes']
    results.append(dict(filename=filename,creator_count=len(expected),independent_count=len(own),creator_missing_from_parser=[expected[k]['region_id'] for k in expected.keys()-own.keys()],independent_extra=[own[k] for k in own.keys()-expected.keys()]))
i=load(C/'inherited-source606-inventory.json');f=load(C/'inherited57.source-only-freeze.exactraw.snapshot.json');cs=load(C/'inherited57.coverage.citation-supplement.exactraw.snapshot.json')
assert i['coverage']==f['coverage']
for r in i['coverage']:
    assert h(primary[r['primary_start_utf8_byte']:r['primary_end_utf8_byte_exclusive']])==r['raw_sha256'],r['region_id']
for r in i['citation_coverage']:
    print('citation keys' ,list(r)) if r==i['citation_coverage'][0] else None
out=dict(actor='/root/statement_topology58',pid=os.getpid(),independent_parser_results=results,creator_counts=coverage['counts'],all365_creator_span_hashes_match=True,inherited596_exact_field_equality=True,inherited596_primary_byte_hashes_match=True,inherited10_citation_exact= i['citation_coverage']==cs.get('citation_coverage',cs.get('coverage')),inherited596_dispositions={k:sum(r['disposition']==k for r in i['coverage']) for k in ['NODE','EXCLUDED']},inherited10_dispositions={k:sum(r['disposition']==k for r in i['citation_coverage']) for k in ['NODE','EXCLUDED']})
(B/'coverage-validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,ensure_ascii=False))
