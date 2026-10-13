import sys, json, hashlib, re, copy
from pathlib import Path
from datetime import datetime, timezone

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path('E:/Samplinglib')
BASE = ROOT / 'runs/20261007-companion-priority/pbps-l2-macroscopic-mean-sourcegraph55'
OUT = BASE / 'repair-overlay55'
REVIEW = ROOT / 'runs/20261007-companion-priority/pbps-l2-macroscopic-mean-topology-review55'
def sha(b): return hashlib.sha256(b).hexdigest()
def lf(b):
    result = b.replace(b'\r\n', b'\n')
    assert b'\r' not in result, 'lone CR'
    return result
def rawjson(d): return (json.dumps(d, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
def readj(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def desc(p, b=None):
    if b is None: b = p.read_bytes()
    return dict(path=str(p), raw_bytes=len(b), lf_bytes=len(lf(b)), raw_sha256=sha(b), lf_sha256=sha(lf(b)))
def write(name,d): (OUT / name).write_bytes(rawjson(d))
def check(d):
    actual=desc(Path(d['path']))
    for k in ['raw_bytes','lf_bytes','raw_sha256','lf_sha256']:
        assert actual[k] == d[k], (d['path'],k)

lease=readj(OUT/'lease.json')
assert all(lease[x]=='OPEN' for x in ['read','write','python'])
assert lease['compiler']=='NOT_STARTED_CLOSED'
negative=readj(REVIEW/'source-topology-review.json')
assert negative['status']=='BLOCKED_SCOPED_REPRESENTATION_ONLY'
assert [b['id'] for b in negative['blockers']]==['T55-1','T55-2']
reviewlease=readj(REVIEW/'reviewer.topology.lease.json')
assert all(reviewlease[k]=='CLOSED' for k in ['read','write','Python'])
assert reviewlease['compiler']=='NOT_STARTED_CLOSED'
assert negative['review_run_sha256']==sha(json.dumps({k:v for k,v in negative.items() if k!='review_run_sha256'},ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8'))
originalrun=readj(BASE/'run.json')
assert originalrun['run_sha256']==sha(json.dumps({k:v for k,v in originalrun.items() if k!='run_sha256'},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8'))
for descriptor in originalrun['inputs']+originalrun['outputs']+[originalrun['actual_closed_lease']]: check(descriptor)
for name in ['graph','creator_run','creator_actual_closed_lease']: check(negative[name])
for x in negative['source_context_evidence']:
    check(x['whole']);check(x['fragment'])

names=['source-proof-graph.json','selected-providers.json','source-coverage.json',
       'caller-inventory.json','lexical-inventory.json','selected-token-inventory.json']
before={n:readj(BASE/n) for n in names}
g=copy.deepcopy(before['source-proof-graph.json'])
providers=copy.deepcopy(before['selected-providers.json'])
coverage=copy.deepcopy(before['source-coverage.json'])
callers=copy.deepcopy(before['caller-inventory.json'])
lexemes=copy.deepcopy(before['lexical-inventory.json'])
assert before['selected-token-inventory.json']==lexemes
assert providers[68]['id']=='condKernel-scope'
assert providers[64]['id']=='api-LinearPMap_domain'
assert len(g['nodes'])==181 and len(g['edges'])==668
assert g['candidate_LF_sha256']=='0c4a69c99eb2dc8572af054133619442ccaf8e2e91ca19e130f4b1b5fc4cee3f'
nodes={n['qualified_id']:n['id'] for n in g['nodes'] if n.get('qualified_id')}
assert 'LinearPMap' not in nodes
carrier='D55.LinearPMap'
g['nodes'].append(dict(id=carrier, kind='external-unexpanded-primitive',
    contract='Actual global LinearPMap structure carrier header41-42; implementation and deeper instance hierarchy unexpanded; generated domain field provenance only',
    qualified_id='LinearPMap', compiled55=False, proof_body_expanded=False))
nodes['LinearPMap']=carrier

def edge(ingredient,consumer,kind,reason,**kw):
    x=dict(id='E55.'+str(len(g['edges'])),ingredient=ingredient,consumer=consumer,
           kind=kind,reason=reason,compiled55call=False)
    x.update(kw);g['edges'].append(x)

fragments=OUT/'fragments';fragments.mkdir()
def capture(pid,node,path,lo,hi,kind):
    data=path.read_bytes(); lines=data.splitlines(keepends=True)
    start=sum(len(b) for b in lines[:lo-1]);end=sum(len(b) for b in lines[:hi])
    b=data[start:end];rawpath=fragments/(pid+'.raw.txt');lfpath=fragments/(pid+'.lf.txt')
    rawpath.write_bytes(b);lfpath.write_bytes(lf(b))
    return dict(id=pid,node=node,kind=kind,path=str(path),physical_lines1=[lo,hi],
                start_utf8_byte0=start,end_utf8_byte0_exclusive=end,
                fragment_raw_sha256=sha(b),fragment_lf_sha256=sha(lf(b)),
                fragment_raw_path=str(rawpath),fragment_lf_path=str(lfpath),
                whole_raw_sha256=sha(data),whole_lf_sha256=sha(lf(data)),
                definition_semantics_selected=False,proof_body_selected=False,body_expansion_boundary=True)

oldscope=copy.deepcopy(providers[68])
providers[68]=capture(oldscope['id'],oldscope['node'],Path(oldscope['path']),75,77,oldscope['kind'])
fieldbefore=copy.deepcopy(providers[64])
providers[64]['generated_field_carrier_provider']='overlay55-LinearPMap-carrier'
providers[64]['generated_field_carrier_node']=carrier
newcarrier=capture('overlay55-LinearPMap-carrier',carrier,Path(fieldbefore['path']),41,42,'public-structure-carrier-header')
providers.append(newcarrier)

rx=re.compile(r'[^\W\d]\w*(?:\.[^\W\d]\w*)*\'?')
named={'MeasurableSpace':'primitive-public-reference',
       'StandardBorelSpace':'explicit-external-unexpanded-type-hierarchy-boundary',
       'Nonempty':'explicit-external-unexpanded-type-hierarchy-boundary',
       'Ring':'explicit-external-unexpanded-type-hierarchy-boundary',
       'AddCommGroup':'explicit-external-unexpanded-type-hierarchy-boundary',
       'Module':'primitive-public-reference'}
allowed={'structure','LinearPMap','R','S','Type','σ','E','F','where','mΩ','Ω'}
def append_rows(pr,physicalrows):
    data=Path(pr['path']).read_bytes();lines=data.splitlines(keepends=True)
    for line in physicalrows:
        start=sum(len(b) for b in lines[:line-1]);body=lines[line-1].rstrip(b'\r\n');text=body.decode('utf-8')
        assert not any(r['provider']==pr['id'] and r['physical_line1']==line for r in coverage)
        coverage.append(dict(provider=pr['id'],path=pr['path'],physical_line1=line,physical_line0=line-1,
            utf8_byte_start0=start,utf8_byte_end0_exclusive=start+len(body),
            utf8_column_start0=0,utf8_column_end0_exclusive=len(body),classification='NODE',node=pr['node'],
            reason='T55 bounded actual inherited class/structure carrier context; no implementation body',raw_sha256=sha(body)))
        for match in rx.finditer(text):
            token=match.group();at=start+len(text[:match.start()].encode('utf-8'));end=start+len(text[:match.end()].encode('utf-8'))
            if token=='LinearPMap':cl='declaration-name-binding';resolution=None
            elif token in named:cl=named[token];resolution=nodes[token]
            else:
                assert token in allowed, ('unexpected context token',token)
                cl='bound-identifier-or-syntax';resolution=None
            item=dict(index0=len(lexemes),provider=pr['id'],consumer=pr['node'],token=token,
                physical_line1=line,physical_line0=line-1,utf8_byte_start0=at,utf8_byte_end0_exclusive=end,
                utf8_column_start0=at-start,utf8_column_end0_exclusive=end-start,
                classification=cl,resolution=resolution,composite_projections=[])
            lexemes.append(item)
            if resolution:
                caller=dict(item);caller['index0']=len(callers);callers.append(caller)
                edge(resolution,pr['node'],'public-header-or-context-reference' if cl=='primitive-public-reference' else 'explicit-external-type-slot',
                     'T55 exact named inherited context/carrier slot; not implementation call',caller_index0=caller['index0'])

append_rows(providers[68],[77])
append_rows(newcarrier,[41,42])
edge(carrier,fieldbefore['node'],'generated-field-provenance',
     'T55-2 actual LinearPMap structure carrier41-42 generates domain field44; ring/semilinear/module contexts are inherited typing obligations',
     carrier_provider_id=newcarrier['id'],field_provider_id=fieldbefore['id'])

assert g['nodes'][:181]==before['source-proof-graph.json']['nodes']
assert g['edges'][:668]==before['source-proof-graph.json']['edges']
assert coverage[:590]==before['source-coverage.json']
assert callers[:593]==before['caller-inventory.json']
assert lexemes[:2891]==before['lexical-inventory.json']
for i in range(146):
    if i not in [64,68]: assert providers[i]==before['selected-providers.json'][i]
for k,v in before['source-proof-graph.json'].items():
    if k not in ['nodes','edges']:assert g[k]==v

providerbyid={p['id']:p for p in providers}
cache={p['path']:Path(p['path']).read_bytes() for p in providers}
for p in providers:
    data=cache[p['path']];fragment=data[p['start_utf8_byte0']:p['end_utf8_byte0_exclusive']]
    assert sha(data)==p['whole_raw_sha256'] and sha(lf(data))==p['whole_lf_sha256']
    assert sha(fragment)==p['fragment_raw_sha256'] and sha(lf(fragment))==p['fragment_lf_sha256']
    if p.get('fragment_raw_path'):assert Path(p['fragment_raw_path']).read_bytes()==fragment
    if p.get('fragment_lf_path'):assert Path(p['fragment_lf_path']).read_bytes()==lf(fragment)
    lines=data.splitlines(keepends=True);offset=0
    rows=[r for r in coverage if r['provider']==p['id']]
    for lineno,line in enumerate(lines,1):
        a=max(offset,p['start_utf8_byte0']);b=min(offset+len(line.rstrip(b'\r\n')),p['end_utf8_byte0_exclusive'])
        if b>a:
            selected=sorted((r['utf8_byte_start0'],r['utf8_byte_end0_exclusive']) for r in rows if r['physical_line1']==lineno)
            assert selected, (p['id'],lineno,'missing coverage')
            cursor=a
            for lo,hi in selected:assert lo==cursor and hi>=lo;cursor=hi
            assert cursor==b,(p['id'],lineno,'coverage mismatch')
        offset+=len(line)
for row in coverage:
    assert row['classification'] in ['NODE','EXCLUDED']
    p=providerbyid[row['provider']];data=cache[p['path']]
    a,b=row['utf8_byte_start0'],row['utf8_byte_end0_exclusive']
    assert sha(data[a:b])==row['raw_sha256']
    if row['classification']=='NODE':assert row['node']==p['node']
    else:assert row['node'] is None
for items in [callers,lexemes]:
    for i,row in enumerate(items):
        assert i==row['index0'];p=providerbyid[row['provider']];data=cache[p['path']]
        a,b=row['utf8_byte_start0'],row['utf8_byte_end0_exclusive']
        assert data[a:b].decode('utf-8')==row['token']
        assert row['physical_line1']==data[:a].count(b'\n')+1
        assert row['physical_line0']==row['physical_line1']-1
        line_start=data.rfind(b'\n',0,a)+1
        assert row['utf8_column_start0']==a-line_start and row['utf8_column_end0_exclusive']==b-line_start
        assert row['consumer']==p['node']
nodeids={n['id'] for n in g['nodes']}
for e in g['edges']:assert e['ingredient'] in nodeids and e['consumer'] in nodeids and e['compiled55call'] is False
for c in callers:
    assert any(e.get('caller_index0')==c['index0'] and e['ingredient']==c['resolution'] and e['consumer']==c['consumer'] for e in g['edges'])
for l in lexemes:
    if l['classification'] in ['primitive-public-reference','explicit-external-unexpanded-type-hierarchy-boundary']:
        assert any(c['provider']==l['provider'] and c['utf8_byte_start0']==l['utf8_byte_start0'] and c['resolution']==l['resolution'] for c in callers)
assert not any(l['classification']=='UNRESOLVED' for l in lexemes)
counts=dict(nodes=len(g['nodes']),edges=len(g['edges']),providers=len(providers),coverage=len(coverage),
            NODE=sum(r['classification']=='NODE' for r in coverage),EXCLUDED=sum(r['classification']=='EXCLUDED' for r in coverage),
            callers=len(callers),lexemes=len(lexemes),unresolved=0)
assert counts['nodes']==182 and counts['edges']==678 and counts['providers']==147
assert counts['coverage']==593 and counts['callers']==602
successors={'source-proof-graph.after.json':g,'selected-providers.after.json':providers,
            'source-coverage.after.json':coverage,'caller-inventory.after.json':callers,
            'lexical-inventory.after.json':lexemes,'selected-token-inventory.after.json':lexemes}
for name,d in successors.items():write(name,d)
operations=[dict(id='T55-1',operation='replace provider68 selected scope75-76 with exact75-77; append line77 coverage/lexical/named slots and consumer edges',
    before=oldscope,after=providers[68],caller_indices0=list(range(593,596))),
    dict(id='T55-2',operation='append exact opaque carrier41-42; annotate provider64 generated carrier provenance and append carrier-to-domain edge',
    field_before=fieldbefore,field_after=providers[64],carrier_provider=newcarrier,
    caller_indices0=list(range(596,602)),generated_provenance_edge=g['edges'][-1])]
write('operations.json',operations)
write('mechanical-checks.json',dict(status='CREATOR_MECHANICAL_ONLY_NOT_TOPOLOGY_ADMISSION',counts=counts,
    original_87_inputs_and_1389_outputs_and_CLOSED_lease_match=True,
    original_negative_and_reviewer_CLOSED=True,all_successor_provider_whole_and_fragments_exact=True,
    all_selected_rows_exhaustive_NODE_or_EXCLUDED=True,all_caller_and_lexeme_byte_coordinates_exact=True,
    named_lexemes_have_callers_and_real_consumer_edges=True,
    prefix_preservation=dict(nodes=181,edges=668,coverage=590,callers=593,lexemes=2891),
    changed_original_provider_indices0=[64,68],signature_or_math_change=False,
    compiler='NOT_STARTED_CLOSED',creator_admission=False))

control=[BASE/n for n in names]+[BASE/'run.json',BASE/'lease.json',BASE/'input-bindings.json',BASE/'source-contract.json',BASE/'hypothesis-contract.json',
    REVIEW/'source-topology-review.json',REVIEW/'reviewer.topology.lease.json',OUT/'lease.open.snapshot.json',
    ROOT/'runs/20261007-companion-priority/pbps-l2-macroscopic-mean-preproof55/prospective-statement.txt',
    ROOT/'runs/20261007-companion-priority/pbps-l2-macroscopic-mean-preproof55/statement-seals.accepted.json']
inputpins=[desc(p) for p in control]
for evidence in negative['source_context_evidence']: inputpins += [desc(Path(evidence['whole']['path'])),desc(Path(evidence['fragment']['path']))]
write('input-bindings.json',dict(native_current_overlay_inputs=inputpins,
    inherited_original_inputs=originalrun['inputs'],inherited_original_outputs=originalrun['outputs'],
    inherited_actual_CLOSED_lease=originalrun['actual_closed_lease'],
    current_actual_OPEN_lease_snapshot=desc(OUT/'lease.open.snapshot.json'),
    inherited_scopes_reopened=False,LF_recipe='CRLF -> LF only; remaining lone CR rejects'))
payload=dict(schema='sourcegraph55-minimal-representation-overlay/v1',status='CREATOR_COMPLETE_PENDING_DISTINCT_REPAIR_REVIEW',
    original_negative=desc(REVIEW/'source-topology-review.json'),original_graph=desc(BASE/'source-proof-graph.json'),
    exact_signature_LF_sha256=g['candidate_LF_sha256'],operations=operations,counts_before=negative['verified_counts'],counts_after=counts,
    successors={n:desc(OUT/n) for n in successors},
    unchanged=['original primary/freezes/negative/lease/header/source formulas/binders','original181 nodes and668 edges prefix','original590 coverage/593 callers/2891 lexical prefix','all other original provider records','all source-contract and hypothesis-contract semantics'],
    exposure='Historical creator/source/API and49/50 body exposures remain disclosed. This task read only exact negative/control metadata and selected77/41-42 public contexts; no55 proof/Test or54 verdict. Initial receipt print was oversized/truncated metadata; next queries narrowed. One console GBK decode failure corrected with explicit UTF8; no data mutation.',
    no_new_math_or_typing_assumption='Nonempty position E follows internally from vector zero; all new references are existing class/structure context obligations, not public theorem premises.',
    external_boundary='LinearPMap carrier implementation and deep instance/type hierarchy remain external-unexpanded. Existing primitive nodes reused; declaration-name binding is not a mathematical call.',
    coordinates='physical lines1-based; inventory rows and UTF8 bytes/columns0-based half-open',
    compiler='NOT_STARTED_CLOSED',source_or_topology_admission=False,proof_or_claim_created=False,canonical_mutation=False)
write('payload.json',payload)
capsule='''Representation-only overlay55 is complete, pending a distinct independent repair review.

T55-1 extends condKernel-scope provider68 from StandardBorel.lean75-76 through77. It adds the actual Omega MeasurableSpace/StandardBorelSpace/Nonempty context, three caller-slot edges to condKernel, and exact raw/LF fragments/coverage.

T55-2 preserves LinearPMap.domain field44 and adds its actual opaque structure carrier41-42: Ring R/S, semilinear sigma, AddCommGroup/Module E/F. Six named type-slot callers feed the carrier; one generated-field provenance edge feeds domain. No declaration self-loop or new public premise.

Successors preserve original181 nodes/668 edges,590 rows,593 callers,2891 lexemes as exact prefixes. Only original providers64(metadata) and68(scope extension) change; one carrier provider/node is appended. Original primary, negative, leases and2526 statement remain immutable. Counts and byte checks are in mechanical-checks.json; creator checks do not admit topology.

The run binds original87 input descriptors,1389 output descriptors and original CLOSED lease, all freshly byte-rechecked; current overlay inputs and new outputs are separate. Raw hashes use exact bytes. LF normalizes CRLF only and rejects lone CR. Run logical hash is SHA256 compact sorted UTF8 JSON of the whole run minus run_sha256, ensure_ascii=False. Coordinates are one-based physical lines and zero-based half-open UTF8 bytes/columns. Final actual read/write/Python CLOSED lease is the last filesystem write after output readbacks; compiler NOT_STARTED_CLOSED.

No proof/Test55 or verdict54 read, compiler, claim, mathematical/signature repair, canonical mutation, or creator source/topology admission. Whole rough B13/H1/Gamma/main/cost boundary remains unchanged. Historical exposure and the oversized initial metadata print/GBK retry are disclosed in payload.json.
'''
(OUT/'capsule.md').write_bytes(capsule.encode('utf-8'))

# Final original and native successor readbacks precede closure.
for descriptor in originalrun['inputs']+originalrun['outputs']+[originalrun['actual_closed_lease']]+inputpins:check(descriptor)
for n,d in successors.items():assert readj(OUT/n)==d
outputs=[desc(p) for p in sorted(OUT.rglob('*')) if p.is_file() and p.name not in ['run.json','lease.json']]
for d in outputs:check(d)
closed=dict(lease);closed.update(read='CLOSED',write='CLOSED',python='CLOSED',compiler='NOT_STARTED_CLOSED',
    closed_utc=datetime.now(timezone.utc).isoformat(),stage='REPRESENTATION_OVERLAY_COMPLETE_PENDING_DISTINCT_REVIEW',
    creator_admission=False,final_operation='actual CLOSED lease write after all output readbacks')
closedbytes=rawjson(closed);closedpin=desc(OUT/'lease.json',closedbytes)
run=dict(schema='sourcegraph55-overlay-native-run/v1',status='CLOSED_SOURCE_ONLY_PENDING_INDEPENDENT_REPAIR_REVIEW',
    created_utc=datetime.now(timezone.utc).isoformat(),inputs=inputpins,outputs=outputs,
    inherited_original_run=desc(BASE/'run.json'),inherited_input_count=len(originalrun['inputs']),inherited_output_count=len(originalrun['outputs']),
    inherited_original_run_logical=originalrun['run_sha256'],payload=desc(OUT/'payload.json'),actual_closed_lease=closedpin,counts=counts,
    LF_recipe='CRLF -> LF only; remaining lone CR rejects',
    logical_hash_recipe='SHA256 UTF8 whole run minus run_sha256, ensure_ascii=False sort_keys=True separators=(comma,colon), no newline',
    compiler='NOT_STARTED_CLOSED',source_or_topology_admission=False)
run['run_sha256']=sha(json.dumps(run,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8'))
runbytes=rawjson(run);(OUT/'run.json').write_bytes(runbytes)
assert (OUT/'run.json').read_bytes()==runbytes
summary=dict(counts=counts,run=desc(OUT/'run.json',runbytes),logical_run_sha256=run['run_sha256'],
    lease=closedpin,payload=desc(OUT/'payload.json'),graph=desc(OUT/'source-proof-graph.after.json'))
# LAST FILESYSTEM OPERATION. No reads, stats, enumeration or subprocesses afterward.
(OUT/'lease.json').write_bytes(closedbytes)
print(json.dumps(summary,ensure_ascii=False,indent=2))
