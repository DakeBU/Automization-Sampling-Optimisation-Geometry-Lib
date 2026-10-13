from pathlib import Path
from html.parser import HTMLParser
import collections, hashlib, json

ROOT = Path(__file__).parent
BASE = ROOT.parent
OVERLAY = BASE / 'exhaustive-overlay56'
REPO = BASE.parents[2]
sha = lambda b: hashlib.sha256(b).hexdigest()
canon = lambda x: json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
def resolve(p):
    path = Path(p)
    return path if path.is_absolute() else REPO / path

def receipt(p):
    b = p.read_bytes(); lf = b.replace(b'\r\n', b'\n')
    return {'path': p.resolve().as_posix(), 'raw_bytes': len(b), 'raw_sha256': sha(b),
            'lf_bytes': len(lf), 'lf_sha256': sha(lf), 'crlf_count': b.count(b'\r\n'),
            'normalization': 'literal raw-byte CRLF->LF only; no JSON reserialization'}

checked = {}; self_checks = []; embedded_count = 0
def check_pin(pin, location, implied=None):
    global embedded_count
    p = resolve(pin['path']) if 'path' in pin else implied
    assert p is not None, location
    r = receipt(p)
    mappings = {'raw_bytes': 'raw_bytes', 'bytes': 'raw_bytes', 'raw_sha256': 'raw_sha256',
                'lf_bytes': 'lf_bytes', 'lf_sha256': 'lf_sha256',
                'crlf_to_lf_bytes': 'lf_bytes', 'crlf_to_lf_sha256': 'lf_sha256'}
    for field, actual in mappings.items():
        if field in pin: assert pin[field] == r[actual], (location, field, pin[field], r[actual])
    checked[r['path']] = r
    embedded_count += 1

def walk(x, location):
    if isinstance(x, dict):
        if 'path' in x and 'raw_sha256' in x:
            check_pin(x, location)
        for k,v in x.items(): walk(v, location + '/' + k)
    elif isinstance(x, list):
        for i,v in enumerate(x): walk(v, location + '/' + str(i))

json_names = ['manifest.json','run.json','complete.json','lease.json','read.lease.json','write.lease.json',
              'python.lease.json','compiler.lease.json','sourceproofgraph56.json','creator-complete56.json',
              'read-isolation-and-chronology56.json','target-binder-semantic-expansion56.json',
              'opaque-provider-semantic-expansion56.json','provider-contract-snapshots.json',
              'provider-physical-context-receipts56.json']
docs = {}
for scope in [BASE, OVERLAY]:
    names = json_names + (['lease.open.json','lease-discipline-correction.json','exhaustive-parent-contract-coverage56.json','operations-readback56.json'] if scope==OVERLAY else ['primary-before-signature.freeze.json','source-first-proof-graph.json','primary-source-anchor-inventory.json','external-semantic-context-snapshots.json'])
    for name in names:
        p=scope/name
        if not p.exists(): continue
        d=json.loads(p.read_bytes()); docs[p.as_posix()]=d; checked[p.resolve().as_posix()]=receipt(p)
        walk(d,p.as_posix())
        if isinstance(d,dict) and 'self_digest' in d:
            digest=d['self_digest']; body={k:v for k,v in d.items() if k!='self_digest'}; payload=canon(body)
            size=digest.get('payload_bytes',digest.get('named_payload_bytes'))
            hash_value=digest.get('payload_sha256',digest.get('named_payload_sha256'))
            assert size==len(payload) and hash_value==sha(payload),(p,'self_digest')
            self_checks.append({'file':p.resolve().as_posix(),'recipe':'Remove only entire top-level self_digest; canonical UTF8 sorted compact JSON of complete remaining object; no newline',
                                'payload_bytes':len(payload),'payload_sha256':sha(payload),'verified':True})

freeze=json.loads((BASE/'primary-before-signature.freeze.json').read_bytes())
for name,pin in freeze['first_stage_artifacts'].items():check_pin(pin,'freeze/'+name,BASE/name)
source=(BASE/'primary-pbps.raw.snapshot.html').read_bytes()
assert sha(source)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
assert source==(REPO/'runs/20261007-companion-priority/phase-pbps-primary-preread56/primary-pbps.raw.snapshot.html').read_bytes()

class Parser(HTMLParser):
    def __init__(self,text):
        super().__init__(); self.stack=[];self.nodes=[];self.offsets=[];pos=0
        for line in text.splitlines(keepends=True):self.offsets.append(pos);pos+=len(line)
    def handle_starttag(self,t,a):
        attrs=dict(a);n={'tag':t,'attrs':attrs,'start':self.offsets[self.getpos()[0]-1]+self.getpos()[1],
                        'ancestors':[v['attrs'].get('id','') for v in self.stack],'children':[]}
        if self.stack:self.stack[-1]['children'].append(n)
        self.nodes.append(n)
        if t not in ['area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr']:self.stack.append(n)
    def handle_endtag(self,t):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i]['tag']==t:
                self.stack[i]['end']=self.offsets[self.getpos()[0]-1]+self.getpos()[1]+len('</'+t+'>');self.stack=self.stack[:i];break
    def handle_data(self,x):
        if self.stack:self.stack[-1]['children'].append(x)
def text(n):
    if isinstance(n,str):return n
    if n['tag']=='math':return n['attrs'].get('alttext','[NO_ALTTEXT]')
    return ' '.join(text(c) for c in n['children'])
s=source.decode('utf-8'); parser=Parser(s);parser.feed(s)
nodes={n['attrs']['id']:n for n in parser.nodes if n['attrs'].get('id')}
inventory=json.loads((BASE/'primary-source-anchor-inventory.json').read_bytes())['inventory']
assert len(inventory)==92 and len({r['anchor'] for r in inventory})==92
for row in inventory:
    n=nodes[row['anchor']];raw=s[n['start']:n['end']].encode('utf-8')
    assert raw==source[row['byte_start']:row['byte_end']]
    assert sha(raw)==row['raw_sha256']
    assert raw==(BASE/row['balanced_fragment']).read_bytes()
    checked[(BASE/row['balanced_fragment']).resolve().as_posix()]=receipt(BASE/row['balanced_fragment'])
c1_independent={n['attrs'].get('id') for n in parser.nodes if 'A3.SS1' in n['ancestors']
    and (n['tag']=='p' and 'ltx_p' in n['attrs'].get('class','').split() or n['tag']=='table' and 'ltx_eqn_table' in n['attrs'].get('class','').split())}
c1_recorded={r['anchor'] for r in inventory if r['anchor'] in c1_independent}
assert c1_recorded==c1_independent,(c1_independent-c1_recorded,c1_recorded-c1_independent)
for ident in ['A3.SS1','A2.SS1','A2.SS2','S2.SS2','S1.p1','A4.SS2']:
    n=nodes[ident];(ROOT/(ident+'.independent-source.txt')).write_text(' '.join(text(n).split())+'\n',encoding='utf-8',newline='\n')

provider_physical=json.loads((BASE/'provider-physical-context-receipts56.json').read_bytes())
print('provider physical shape',type(provider_physical).__name__)
if isinstance(provider_physical,list): physical_rows=provider_physical
else: physical_rows=provider_physical.get('rows',provider_physical.get('providers',[]))
# These full-file byte reads verify physical provenance only; source/contract semantics are read from preserved headers.
for table in [json.loads((BASE/'provider-contract-snapshots.json').read_bytes()),json.loads((BASE/'external-semantic-context-snapshots.json').read_bytes())]:
    for row in table:
        physical=Path(row['physical_path']);raw=physical.read_bytes();lf=raw.replace(b'\r\n',b'\n')
        for field,value in [('whole_file_raw_sha256',sha(raw)),('whole_file_raw_bytes',len(raw)),('whole_file_lf_sha256',sha(lf)),('whole_file_lf_bytes',len(lf))]:
            if field in row:assert row[field]==value,(physical,field)
        for rr in row.get('ranges',[]):check_pin(rr,'external/'+row['label'],BASE/rr['snapshot'])
        if 'header_raw_sha256' in row:
            p=BASE/(row['declaration']+'.raw.contract.lean');pin={k.replace('header_',''):v for k,v in row.items() if k.startswith('header_')};check_pin(pin,'provider/'+row['declaration'],p)

correction=json.loads((OVERLAY/'lease-discipline-correction.json').read_bytes())
assert len(correction['actual_post_closed_mutations'])==3
for row in correction['restorations']:
    original=Path(row['original_path']);before=Path(row['preserved_original_path'])
    assert original.read_bytes()==before.read_bytes()
    assert len(original.read_bytes())==row['raw_bytes'] and sha(original.read_bytes())==row['raw_sha256']
    checked[original.resolve().as_posix()]=receipt(original);checked[before.resolve().as_posix()]=receipt(before)
isolation=json.loads((OVERLAY/'read-isolation-and-chronology56.json').read_bytes())
assert isolation['strict_provider_body_blindness'] is False
assert isolation['primary_first_freeze_precedes_exposure'] is True

base_graph=json.loads((BASE/'sourceproofgraph56.json').read_bytes())
graph=json.loads((OVERLAY/'sourceproofgraph56.json').read_bytes())
assert len(graph['source_nodes'])==29
assert graph['source_edges']==base_graph['source_edges']
assert graph['unnamed_source_step_refinement']==base_graph['unnamed_source_step_refinement']
parents=json.loads((OVERLAY/'exhaustive-parent-contract-coverage56.json').read_bytes())
assert len(parents['rows'])==87
target=json.loads((OVERLAY/'target-binder-semantic-expansion56.json').read_bytes())
assert len(target['rows'])==29
assert len(graph['unnamed_source_step_refinement'])==7
routes={x['id']:x['required_inputs'] for x in graph['unnamed_source_step_refinement']}
edges={x['child']:x['parents'] for x in graph['source_edges']}
assert not (set(edges)&set(routes))
edges.update(routes)
def reachable(node):
    seen=set();pending=list(edges.get(node,[]))
    while pending:
        v=pending.pop()
        if v in seen:continue
        seen.add(v);pending+=edges.get(v,[])
    return sorted(seen)
assert 'route56:core-gradient' not in reachable('route56:core-linear-bound')
assert 'route56:core-linear-bound' not in reachable('route56:bounded-extension')
assert 'route56:core-gradient' not in reachable('route56:closed-graph')
source_counts=dict(collections.Counter(r['disposition'] for r in inventory))
assert source_counts=={'NODE':49,'EXCLUDED':43}
results={'schema_version':1,'status':'VERIFIED_INPUT_BINDINGS_TOPOLOGY_EDGE_BLOCKER',
    'unique_verified_files':len(checked),'embedded_receipt_checks':embedded_count,'verified_receipts':list(checked.values()),
    'self_digest_checks':self_checks,'coverage':{'inventory':92,'covered':49,'excluded':43,'C1_independent_atomic_regions':len(c1_independent),'target_slots':29,'parent_slots':87,'source_nodes':29,'step_refinements':7},
    'restored_originals':len(correction['restorations']),'post_closed_mutations_retained':3,
    'strict_creator_body_blindness':False,'initial_fragment_recovered':False,
    'route_dependencies':routes,'reachability':{n:reachable(n) for n in ['route56:core-linear-bound','route56:bounded-extension','route56:closed-graph','route56:sharp-energy']},
    'independent_source_snapshot':receipt(BASE/'primary-pbps.raw.snapshot.html'),
    'original_schema_shapes':{p:{'top_level_type':type(d).__name__,'schema_version':d.get('schema_version') if isinstance(d,dict) else None,'kind':d.get('kind') if isinstance(d,dict) else None,'keys':list(d) if isinstance(d,dict) else ['LIST']} for p,d in docs.items()},
    'no_compile_started':True,'no_original_mutations':True}
(ROOT/'input-verification.json').write_bytes(json.dumps(results,ensure_ascii=False,sort_keys=True,indent=2).encode('utf-8')+b'\n')
print(json.dumps({k:v for k,v in results.items() if k not in ['verified_receipts','original_schema_shapes']},ensure_ascii=False,indent=2))
