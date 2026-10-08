from pathlib import Path
import json, hashlib, collections
p=Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-reflected-density-sourcegraph53')
o=Path(__file__).parent
sha=lambda b:hashlib.sha256(b).hexdigest()
lf=lambda b:b.replace(b'\r\n',b'\n')
J=lambda f:json.loads((p/f).read_bytes())
r=J('run.json');ps=J('selected-providers.json');g=J('source-proof-graph.json');cv=J('source-coverage.json');cs=J('caller-inventory.json');ls=J('lexical-inventory.json')
errors=[];cache={}
def raw(path):
    k=str(Path(path))
    if k not in cache: cache[k]=Path(path).read_bytes()
    return cache[k]
def ckdesc(x,kind):
    b=raw(x['path']);a=lf(b)
    for f,v in [('raw_sha256',sha(b)),('lf_sha256',sha(a)),('raw_bytes',len(b)),('lf_bytes',len(a))]:
        if f in x and x[f]!=v: errors.append([kind,x['path'],f,x[f],v])
for x in r['inputs']: ckdesc(x,'input')
for x in r['outputs']: ckdesc(x,'output')
for x in ps:
    ckdesc(x,'providerwhole');b=raw(x['path'])[x['start_utf8_byte0']:x['end_utf8_byte0_exclusive']]
    for k,v in [('fragment_raw_sha256',sha(b)),('fragment_lf_sha256',sha(lf(b)))]:
        if x[k]!=v: errors.append(['fragment',x['id'],k])
    for suf,v in [('raw',b),('lf',lf(b))]:
        if (p/(x['id']+'.'+suf)).read_bytes()!=v: errors.append(['savedfragment',x['id'],suf])
prov={x['id']:x for x in ps};ids={n['id'] for n in g['nodes']};expected=set();actual=set()
for x in ps:
    b=raw(x['path']);a=x['start_utf8_byte0'];z=x['end_utf8_byte0_exclusive'];pos=0
    for i,l in enumerate(b.splitlines(keepends=True),1):
        lo=max(pos,a);hi=min(pos+len(l),z)
        if lo<hi: expected.add((x['id'],i,lo,hi))
        pos+=len(l)
for x in cv:
    b=raw(x['path']);lo=x['utf8_byte_start0'];hi=x['utf8_byte_end0_exclusive'];actual.add((x['provider'],x['physical_line1'],lo,hi))
    if 'raw_line_sha256' in x and sha(b[lo:hi])!=x['raw_line_sha256']: errors.append(['coveragehash',x['provider'],x['physical_line1']])
    if x['classification']=='NODE' and x['node'] not in ids: errors.append(['coverage_node',x])
    if not x['reason']: errors.append(['coverage_no_reason',x])
if expected!=actual: errors.append(['coverage_partition',list(expected-actual)[:8],list(actual-expected)[:8]])
for kind,arr in [('callers',cs),('lexemes',ls)]:
    for i,x in enumerate(arr):
        pr=prov[x['provider']];b=raw(pr['path']);lo=x['utf8_byte_start0'];hi=x['utf8_byte_end0_exclusive']
        if x['index0']!=i or b[lo:hi].decode('utf-8')!=x['token']: errors.append([kind,'token',i])
        if not pr['start_utf8_byte0']<=lo<hi<=pr['end_utf8_byte0_exclusive']: errors.append([kind,'range',i])
        if x['resolution'] is not None and x['resolution'] not in ids: errors.append([kind,'resolution',i])
for e in g['edges']:
    if e['ingredient'] not in ids or e['consumer'] not in ids or e['compiled53call']: errors.append(['graph',e])
for x in cs:
    matches=[e for e in g['edges'] if e.get('caller_index0')==x['index0']]
    if len(matches)!=1 or matches[0]['ingredient']!=x['resolution'] or matches[0]['consumer']!=x['consumer']: errors.append(['caller_edge',x['index0']])
z=dict(r);z.pop('run_sha256');logical=sha(json.dumps(z,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode())
if logical!=r['run_sha256']: errors.append(['logicalrun',logical,r['run_sha256']])
checks={'input_count':len(r['inputs']),'output_count':len(r['outputs']),'unique_whole_files_bytechecked':len(cache),'providers':len(ps),'coverage_rows':len(cv),'coverage_partition_equal':expected==actual,'coverage_counts':dict(collections.Counter(x['classification'] for x in cv)),'callers':len(cs),'lexemes':len(ls),'nodes':len(ids),'edges':len(g['edges']),'creator_run_sha256_recomputed':logical,'errors':errors}
(o/'reviewer.topology.byte-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(checks,ensure_ascii=False))
