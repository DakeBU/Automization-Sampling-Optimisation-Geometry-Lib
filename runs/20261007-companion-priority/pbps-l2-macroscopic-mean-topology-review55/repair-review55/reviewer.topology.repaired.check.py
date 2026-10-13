import json, hashlib, bisect
from pathlib import Path

ROOT = Path('E:/Samplinglib')
BASE = ROOT/'runs/20261007-companion-priority/pbps-l2-macroscopic-mean-sourcegraph55'
SRC = BASE/'repair-overlay55'
OUT = ROOT/'runs/20261007-companion-priority/pbps-l2-macroscopic-mean-topology-review55/repair-review55'
def h(b): return hashlib.sha256(b).hexdigest()
def logical(x,key): return h(json.dumps({k:v for k,v in x.items() if k != key},ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode())
def read(name):
    if name in ['source-proof-graph.json','selected-providers.json','caller-inventory.json','source-coverage.json','lexical-inventory.json']: name=name.replace('.json','.after.json')
    return json.loads((SRC/name).read_text(encoding='utf8'))
cache={}
def data(p):
    p=str(p)
    if p not in cache: cache[p]=Path(p).read_bytes()
    return cache[p]
def pin(p):
    b=data(p); lf=b.replace(b'\r\n',b'\n')
    assert b'\r' not in lf,p
    return dict(path=str(p),raw_bytes=len(b),lf_bytes=len(lf),raw_sha256=h(b),lf_sha256=h(lf))
errors=[]
def ck(test,label):
    if not test: errors.append(label)
run=read('run.json'); g=read('source-proof-graph.json'); ps=read('selected-providers.json'); cs=read('caller-inventory.json'); cov=read('source-coverage.json'); lex=read('lexical-inventory.json')
ck(logical(run,'run_sha256')==run['run_sha256'],'creator logical run')
original=json.loads((BASE/'run.json').read_text(encoding='utf8'))
bind=json.loads((SRC/'input-bindings.json').read_text(encoding='utf8'))
ck(bind['inherited_original_inputs']==original['inputs'],'exact inherited87 descriptor list')
ck(bind['inherited_original_outputs']==original['outputs'],'exact inherited1389 descriptor list')
ck(bind['inherited_actual_CLOSED_lease']==original['actual_closed_lease'],'exact inherited creator lease')
descriptors=run['inputs']+run['outputs']+[run['actual_closed_lease']]+original['inputs']+original['outputs']+[original['actual_closed_lease']]
for i,d in enumerate(descriptors):
    got=pin(d['path'])
    for k in ['raw_bytes','lf_bytes','raw_sha256','lf_sha256']:
        ck(got[k]==d[k],f'pin {i} {k}: {d["path"]}')
nodeids={n['id'] for n in g['nodes']}; pmap={p['id']:p for p in ps}
for p in ps:
    b=data(p['path']);frag=b[p['start_utf8_byte0']:p['end_utf8_byte0_exclusive']]
    ck(h(b)==p['whole_raw_sha256'],p['id']+' whole raw')
    ck(h(b.replace(b'\r\n',b'\n'))==p['whole_lf_sha256'],p['id']+' whole LF')
    ck(h(frag)==p['fragment_raw_sha256'],p['id']+' fragment raw')
    ck(h(frag.replace(b'\r\n',b'\n'))==p['fragment_lf_sha256'],p['id']+' fragment LF')
    for key,expected in [('fragment_raw_path',frag),('fragment_lf_path',frag.replace(b'\r\n',b'\n'))]:
        if key in p: ck(data(p[key])==expected,p['id']+' saved '+key)
    ck(p['node'] in nodeids,p['id']+' graph node')
def check_pos(x,token=False):
    p=pmap[x['provider']];b=data(p['path']);a=x['utf8_byte_start0'];z=x['utf8_byte_end0_exclusive'];fragment=b[a:z]
    ck(p['start_utf8_byte0']<=a<=z<=p['end_utf8_byte0_exclusive'],f'containment {x["provider"]}:{x.get("index0",x["physical_line1"])}')
    starts=[0]+[i+1 for i,c in enumerate(b) if c==10]
    line=bisect.bisect_right(starts,a)-1
    ck(line==x['physical_line0'] and line+1==x['physical_line1'],'line '+str(x.get('index0',x['provider'])))
    ck(a-starts[line]==x['utf8_column_start0'] and z-starts[line]==x['utf8_column_end0_exclusive'],'column '+str(x.get('index0',x['provider'])))
    if token: ck(fragment.decode('utf8')==x['token'],'token '+str(x['index0']))
    else: ck(h(fragment)==x['raw_sha256'],'row '+str(x['physical_line1']))
for x in cov:
    check_pos(x)
    ck(x['classification'] in ['NODE','EXCLUDED'],'coverage classification')
    ck(x['node'] in nodeids if x['classification']=='NODE' else x['node'] is None,'coverage node '+str(x['node']))
for p in ps:
    rows=sorted((x['utf8_byte_start0'],x['utf8_byte_end0_exclusive']) for x in cov if x['provider']==p['id'])
    b=data(p['path']);cursor=p['start_utf8_byte0']
    for a,z in rows:
        ck(a>=cursor and b[cursor:a].strip(b'\r\n')==b'',p['id']+' uncovered non-line-ending bytes')
        cursor=z
    ck(bool(rows) and b[cursor:p['end_utf8_byte0_exclusive']].strip(b'\r\n')==b'',p['id']+' tail coverage')
for x in cs:
    check_pos(x,True)
    ck(x['resolution'] in nodeids,'caller resolution '+str(x['index0']))
    ck(any(e.get('caller_index0')==x['index0'] and e['ingredient']==x['resolution'] and e['consumer']==x['consumer'] for e in g['edges']),'caller edge '+str(x['index0']))
for x in lex: check_pos(x,True)
for e in g['edges']:
    ck(e['ingredient'] in nodeids and e['consumer'] in nodeids,'edge endpoints '+e['id'])
    ck(e.get('compiled55call') is False,'false compiled edge '+e['id'])
ck(g['compiled_graph_created'] is False and g['implementation55_seen'] is False,'no implementation claim')
ck(g['candidate_LF_sha256']=='0c4a69c99eb2dc8572af054133619442ccaf8e2e91ca19e130f4b1b5fc4cee3f','exact statement')
before={name:json.loads((BASE/name).read_text(encoding='utf8')) for name in ['source-proof-graph.json','selected-providers.json','source-coverage.json','caller-inventory.json','lexical-inventory.json']}
ops=json.loads((SRC/'operations.json').read_text(encoding='utf8'))
og=before['source-proof-graph.json'];op=before['selected-providers.json']
ck(len(g['nodes'])==182 and g['nodes'][:181]==og['nodes'],'181node exact prefix plus1')
ck(len(g['edges'])==678 and g['edges'][:668]==og['edges'],'668edge exact prefix plus10')
ck({k:v for k,v in g.items() if k not in ['nodes','edges']}=={k:v for k,v in og.items() if k not in ['nodes','edges']},'all non-node/edge graph fields unchanged')
ck(len(ps)==147 and all(ps[i]==op[i] for i in range(146) if i not in [64,68]),'only64/68 providers change plus1')
ck(ops[0]['before']==op[68] and ops[0]['after']==ps[68],'T55-1 actual before/after not wrong-before')
ck(ops[1]['field_before']==op[64] and ops[1]['field_after']==ps[64] and ops[1]['carrier_provider']==ps[146],'T55-2 actual before/after not wrong-before')
ck({k:v for k,v in ps[64].items() if k not in ['generated_field_carrier_provider','generated_field_carrier_node']}==op[64],'domain field only two provenance keys')
for name,after,n in [('source-coverage.json',cov,590),('caller-inventory.json',cs,593),('lexical-inventory.json',lex,2891)]: ck(after[:n]==before[name],name+' exact full old prefix')
ck(json.loads((SRC/'selected-token-inventory.after.json').read_text(encoding='utf8'))==lex,'selected-token exact lexical copy')
ck(ps[68]['physical_lines1']==[75,77] and ps[146]['physical_lines1']==[41,42],'exact two source line scopes')
expected=['MeasurableSpace','StandardBorelSpace','Nonempty','Ring','Ring','AddCommGroup','Module','AddCommGroup','Module']
ck([x['token'] for x in cs[593:]]==expected,'nine exact appended type callers')
ck([x['consumer'] for x in cs[593:]]==['D55.MeasureTheory_Measure_condKernel']*3+['D55.LinearPMap']*6,'exact correct repaired type consumers')
ck(g['edges'][-1]==ops[1]['generated_provenance_edge'],'exact generated field provenance edge')
ck(g['edges'][-1]['ingredient']=='D55.LinearPMap' and g['edges'][-1]['consumer']=='D55.LinearPMap_domain','carrier to actual domain field')
lease=json.loads((SRC/'lease.json').read_text(encoding='utf8'))
ck(all(lease[k]=='CLOSED' for k in ['read','write','python']) and lease['compiler']=='NOT_STARTED_CLOSED','actual creator final roles')
ck(run['source_or_topology_admission'] is False and lease['creator_admission'] is False,'no creator self admission')
result={'status':'PASSED_BYTE_STRUCTURAL_AND_EXACT_OVERLAY_CHECKS' if not errors else 'BYTE_STRUCTURAL_CHECK_FAILURE','errors':errors,'counts':{'native_inputs':len(run['inputs']),'native_outputs':len(run['outputs']),'inherited_original_inputs':87,'inherited_original_outputs':1389,'closed_leases':2,'providers':len(ps),'coverage':len(cov),'NODE':sum(x['classification']=='NODE' for x in cov),'EXCLUDED':sum(x['classification']=='EXCLUDED' for x in cov),'callers':len(cs),'lexemes':len(lex),'nodes':len(g['nodes']),'edges':len(g['edges'])},'creator_run_logical_recomputed':logical(run,'run_sha256'),'verified_descriptors':descriptors,'check_boundary':'Exact raw/LF and all successor fragment/token geometry; original prefixes, actual operations before/after, affected provider/type edges and final closed roles. Reuses unchanged original selected source semantics; no future proof admission.'}
(OUT/'reviewer.topology.byte-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({k:v for k,v in result.items() if k!='verified_descriptors'},ensure_ascii=False))
