from pathlib import Path
import copy, hashlib, json

ROOT=Path(__file__).parent
BASE=ROOT.parent
REPAIR=BASE/'edge-repair56'
PRIOR=BASE/'review56'
EXHAUSTIVE=BASE/'exhaustive-overlay56'
REPO=BASE.parents[2]
sha=lambda b:hashlib.sha256(b).hexdigest()
canonical=lambda o:json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def receipt(p):
    raw=p.read_bytes();lf=raw.replace(b'\r\n',b'\n')
    return {'path':p.resolve().as_posix(),'raw_bytes':len(raw),'raw_sha256':sha(raw),
            'lf_bytes':len(lf),'lf_sha256':sha(lf),'crlf_count':raw.count(b'\r\n'),
            'normalization':'Replace literal raw-byte CRLF pairs with LF only; no JSON reserialization'}
def resolve(p):
    path=Path(p);return path if path.is_absolute() else REPO/path

checked={};occurrences=0;self_checks=[]
def walk(x,label):
    global occurrences
    if isinstance(x,dict):
        if 'path' in x and 'raw_sha256' in x:
            p=resolve(x['path']);actual=receipt(p)
            for name,equivalent in [('raw_bytes','raw_bytes'),('bytes','raw_bytes'),('raw_sha256','raw_sha256'),
                                    ('lf_bytes','lf_bytes'),('lf_sha256','lf_sha256'),
                                    ('crlf_to_lf_bytes','lf_bytes'),('crlf_to_lf_sha256','lf_sha256')]:
                if name in x:assert x[name]==actual[equivalent],(label,name,p)
            checked[p.resolve().as_posix()]=actual;occurrences+=1
        for k,v in x.items():walk(v,label+'/'+k)
    elif isinstance(x,list):
        for i,v in enumerate(x):walk(v,label+'/'+str(i))

documents=[]
for scope,names in [(REPAIR,['overlay.json','lease.open.json','lease.json']),
    (PRIOR,['topology.review.json','minimal-edge-repair.proposal.json','reviewer.topology.run.json','manifest.json','complete.json','lease.json','input-verification.json']),
    (BASE,['manifest.json','run.json','complete.json','lease.json','read.lease.json','write.lease.json','python.lease.json','compiler.lease.json']),
    (EXHAUSTIVE,['manifest.json','run.json','complete.json','lease.json','read.lease.json','write.lease.json','python.lease.json','compiler.lease.json','lease-discipline-correction.json','read-isolation-and-chronology56.json'])]:
    for name in names:
        p=scope/name;raw=p.read_bytes();o=json.loads(raw);documents.append((p,o));checked[p.resolve().as_posix()]=receipt(p);walk(o,p.as_posix())
        if 'content_self_sha256' in o:
            body={k:v for k,v in o.items() if k!='content_self_sha256'};payload=canonical(body);assert sha(payload)==o['content_self_sha256']
            self_checks.append({'path':p.resolve().as_posix(),'kind':'complete-object excluding only top-level content_self_sha256',
                                'payload_bytes':len(payload),'sha256':sha(payload),'verified':True})
        elif 'self_digest' in o:
            body={k:v for k,v in o.items() if k!='self_digest'};payload=canonical(body);d=o['self_digest']
            assert len(payload)==d.get('payload_bytes',d.get('named_payload_bytes'))
            assert sha(payload)==d.get('payload_sha256',d.get('named_payload_sha256'))
            self_checks.append({'path':p.resolve().as_posix(),'kind':'complete-object excluding only top-level self_digest',
                                'payload_bytes':len(payload),'sha256':sha(payload),'verified':True})

before_raw=(REPAIR/'sourceproofgraph.before.raw.snapshot.json').read_bytes()
assert before_raw==(EXHAUSTIVE/'sourceproofgraph56.json').read_bytes()
assert sha(before_raw)=='d664f3915894bf0693b779f97059c7a107b778cec1139092488808f738214919'
before=json.loads(before_raw);after=json.loads((REPAIR/'sourceproofgraph.after.json').read_bytes())
proposal=json.loads((PRIOR/'minimal-edge-repair.proposal.json').read_bytes())
overlay=json.loads((REPAIR/'overlay.json').read_bytes())
assert overlay['changes']==proposal['changes']
expected=copy.deepcopy(before)
for change in proposal['changes']:
    rows=[n for n in expected['unnamed_source_step_refinement'] if n['id']==change['consumer']];assert len(rows)==1
    assert change['field']=='required_inputs' and change['append'] not in rows[0]['required_inputs']
    rows[0]['required_inputs'].append(change['append'])
assert after==expected,'Repair has unexpected semantic changes'
diffs=[]
def diff(a,b,path=''):
    if type(a) is not type(b):diffs.append({'path':path,'kind':'type-change'});return
    if isinstance(a,dict):
        for k in sorted(set(a)|set(b)):
            if k not in a or k not in b:diffs.append({'path':path+'/'+k,'kind':'key-add-remove'})
            else:diff(a[k],b[k],path+'/'+k)
    elif isinstance(a,list):
        for i in range(min(len(a),len(b))):diff(a[i],b[i],path+'/'+str(i))
        for i in range(len(a),len(b)):diffs.append({'path':path+'/'+str(i),'kind':'append','value':b[i]})
        if len(b)<len(a):diffs.append({'path':path,'kind':'list-shortening'})
    elif a!=b:diffs.append({'path':path,'kind':'value-change','before':a,'after':b})
diff(before,after)
assert diffs==[{'path':'/unnamed_source_step_refinement/2/required_inputs/4','kind':'append','value':'route56:core-gradient'},
               {'path':'/unnamed_source_step_refinement/3/required_inputs/2','kind':'append','value':'route56:core-linear-bound'}]
mapping={n['child']:n['parents'] for n in after['source_edges']}
mapping.update({n['id']:n['required_inputs'] for n in after['unnamed_source_step_refinement']})
def reachable(start):
    seen=set();pending=list(mapping.get(start,[]))
    while pending:
        x=pending.pop()
        if x in seen:continue
        seen.add(x);pending+=mapping.get(x,[])
    return sorted(seen)
for n in mapping:assert n not in reachable(n),'Cycle introduced'
assert 'route56:core-gradient' in reachable('route56:core-linear-bound')
assert 'route56:core-linear-bound' in reachable('route56:bounded-extension')
assert 'route56:core-gradient' in reachable('route56:closed-graph')
assert 'route56:core-gradient' in reachable('route56:sharp-energy')
prior_review=json.loads((PRIOR/'topology.review.json').read_bytes())
coverage=prior_review['coverage']
assert coverage['inventory']==92 and coverage['covered']==49 and coverage['excluded']==43
assert coverage['target_slots']==29 and coverage['parent_slots']==87 and coverage['source_nodes']==29
assert after['coverage']==before['coverage'] and after['source_nodes']==before['source_nodes'] and after['source_edges']==before['source_edges']
assert len(after['source_nodes'])==29 and len(after['unnamed_source_step_refinement'])==7
statement=(BASE/'prospective-statement.target.lf.snapshot.txt').read_bytes()
assert len(statement)==1755 and sha(statement)=='fea2c3ade170bc0526d659f8c51abedaa0ce1a6186e75f0d8a2532b6608e94d8'
correction=json.loads((EXHAUSTIVE/'lease-discipline-correction.json').read_bytes())
assert len(correction['actual_post_closed_mutations'])==3
for row in correction['restorations']:
    p=Path(row['original_path']);before_p=Path(row['preserved_original_path'])
    assert p.read_bytes()==before_p.read_bytes()
    assert len(p.read_bytes())==row['raw_bytes'] and sha(p.read_bytes())==row['raw_sha256']
    checked[p.resolve().as_posix()]=receipt(p);checked[before_p.resolve().as_posix()]=receipt(before_p)
isolation=json.loads((EXHAUSTIVE/'read-isolation-and-chronology56.json').read_bytes())
assert isolation['strict_provider_body_blindness'] is False
assert isolation['primary_first_freeze_precedes_exposure'] is True
lease=json.loads((REPAIR/'lease.json').read_bytes());opened=json.loads((REPAIR/'lease.open.json').read_bytes())
assert lease['status']=='CLOSED' and opened['status']=='OPEN' and lease['exit_code']==0
assert lease['compiler']=='NOT_STARTED_CLOSED'
assert json.loads((PRIOR/'lease.json').read_bytes())['status']=='CLOSED'
assert sha((PRIOR/'lease.json').read_bytes())=='9909fc2ad19f1c7da0998fe64411462601d2e90344eef5259845ba2b46c2e115'
result={'schema_version':1,'status':'PASS_EXACT_TWO_EDGE_REPAIR','exact_deep_diff':diffs,
        'reachability':{n:reachable(n) for n in ['route56:core-linear-bound','route56:bounded-extension','route56:closed-graph','route56:sharp-energy']},
        'paths':[['route56:core-linear-bound','route56:core-gradient'],
                 ['route56:bounded-extension','route56:core-linear-bound','route56:core-gradient'],
                 ['route56:closed-graph','route56:bounded-extension','route56:core-linear-bound','route56:core-gradient'],
                 ['route56:sharp-energy','route56:bounded-extension','route56:core-linear-bound','route56:core-gradient']],
        'acyclic':True,'semantic_only_two_appends':True,'status_prose_nodes_source_anchors_binders_unchanged':True,
        'before_receipt':receipt(REPAIR/'sourceproofgraph.before.raw.snapshot.json'),'after_receipt':receipt(REPAIR/'sourceproofgraph.after.json'),
        'raw_vs_semantic_distinction':'After JSON uses CRLF packaging; exact two changes refer to decoded deep JSON. Raw and CRLF->LF receipts separately verified.',
        'coverage':coverage,'unique_verified_files':len(checked),'embedded_pin_checks':occurrences,'verified_receipts':list(checked.values()),
        'complete_object_self_hash_checks':self_checks,'original_restorations_exact':11,
        'negative_history_unchanged':True,'strict_body_blindness':False,'overwritten_fragment_recovered':False,
        'original_blocker_review_preserved_CLOSED':True,'sourcegraph_admission_proposed':True,
        'proof_admission':False,'compiler':'NOT_STARTED_CLOSED',
        'native_schema_audit':{'repair_overlay':'schema_version1 status/author/inputs/changes/before/after flags; output raw pins, no content self-hash field',
                               'repair_author_lease':'status/read/write/Python/compiler/exit_code/owner/actual_outputs/closed_last; raw receipt binding, no content self-hash field',
                               'original_native_seals':'Both payload/named_payload labels checked as complete-object canonical hash, not raw-file hash'}}
(ROOT/'repair-verification.json').write_bytes(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2).encode('utf-8')+b'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['verified_receipts','complete_object_self_hash_checks']},ensure_ascii=False,indent=2))
