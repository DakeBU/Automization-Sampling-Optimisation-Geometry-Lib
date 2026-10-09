import json,re,hashlib
from pathlib import Path
O=Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-polar-preproof65/independent-primary65')
def load(n):return json.loads((O/n).read_text(encoding='utf-8'))
def write(n,v):(O/n).write_bytes((json.dumps(v,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode())
for tail in ['stdout.txt','stderr.txt','receipt.json']:
 p=O/('foreground-finalizer.'+tail);(O/('initial-finalizer.'+tail)).write_bytes(p.read_bytes())
i=load('source-inputs.json');c=load('source-coverage-inventory.json')
r=next(x for x in i['regions'] if x['name']=='spectral-background-D1');b=(O/'spectral-background-D1.raw.html').read_bytes();m=re.search(rb'<[^>]*id="([^"]+)"[^>]*>\s*(?:<[^>]*>\s*)*Definition.*?D\.2',b,re.S)
# The exact source definition anchor is obtained from the literal heading context.
k=b.find(b'Definition D.2');
if k<0:
 k=b.find(b'Definition</span> <span class="ltx_tag ltx_tag_theorem">D.2')
# LatexHTML supplies a theorem division containing the printed D.2 heading.
heads=list(re.finditer(rb'<div\b[^>]*class="[^"]*ltx_theorem[^>]*>',b))
print('D1 theorem div anchors',[(x.start(),x.group().decode()) for x in heads])
# Stable literal id for Definition D.2 follows the unique-root paragraph.
cut=None
for x in heads:
 if b'D.2' in b[x.start():x.start()+900]:cut=r['source_raw_byte_range'][0]+x.start();break
assert cut is not None
for x in c['math_items']:
 if x['region']=='spectral-background-D1':x['classification']='real-L2-bounded-operator-adjoint-Loewner-spectral-conventions' if x['raw_byte_start']<cut else 'Markov-constants-center-context-not-process-result'
c['classification_counts']={v:sum(x['classification']==v for x in c['math_items']) for v in sorted({x['classification'] for x in c['math_items']})};write('source-coverage-inventory.json',c)
p=load('primary-only-review.json');p['source_coverage_summary']['classification_counts']=c['classification_counts'];write('primary-only-review.json',p)
write('finite-inventory-refinement.json',{'schema':'primary65-finite-inventory-refinement-v1','scope':'D1 paragraph classification boundary only','reason':'Unique-root spectral-calculus paragraph belongs to D1 Hilbert notation before Definition D2; initial equation-D3 cutoff was too early.','definition_D2_raw_byte_start':cut,'mathematical_statement_changed':False,'source_inputs_changed':False,'initial_foreground_finalizer_retained':['initial-finalizer.stdout.txt','initial-finalizer.stderr.txt','initial-finalizer.receipt.json'],'requires_new_complete_logical_finalization':True})
s=(O/'native-finalizer.py').read_text(encoding='utf-8-sig');s=s.replace("x.name not in ['review-run.json','raw-review-binding.json']","x.name not in ['review-run.json','raw-review-binding.json'] and not x.name.startswith('foreground-')")
s=s.replace("'tool-negatives.json']","'tool-negatives.json','finite-inventory-refinement.json']")
(O/'native-finalizer.py').write_bytes(s.encode())
