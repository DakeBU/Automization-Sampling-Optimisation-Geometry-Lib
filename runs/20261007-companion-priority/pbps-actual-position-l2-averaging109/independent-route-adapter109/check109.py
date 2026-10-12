import gzip, hashlib, json, re
from pathlib import Path
from collections import Counter, defaultdict, deque
ROOT=Path('E:/Samplinglib')
OUT=Path(__file__).resolve().parent
SRC=OUT.parent/'route-adapter109'
def sha(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads(p.read_bytes().decode('utf-8-sig'))
def bind(r):
    b=(ROOT/r['path']).read_bytes()
    return dict(path=r['path'],actual_raw_sha256=sha(b),hash_ok=sha(b)==r['raw_sha256'],bytes_ok=len(b)==r['bytes'])
def diff(a,b,p=''):
    if isinstance(a,dict) and isinstance(b,dict):
        result=[]
        for k in sorted(set(a)|set(b)):
            if k not in a or k not in b:
                result.append(dict(path=p+'/'+k,before=a.get(k),after=b.get(k)))
            else: result+=diff(a[k],b[k],p+'/'+k)
        return result
    if isinstance(a,list) and isinstance(b,list):
        result=[]
        for i in range(max(len(a),len(b))):
            if i>=len(a) or i>=len(b): result.append(dict(path=p+'/'+str(i),before=a[i] if i<len(a) else None,after=b[i] if i<len(b) else None))
            else: result+=diff(a[i],b[i],p+'/'+str(i))
        return result
    return [] if a==b else [dict(path=p,before=a,after=b)]
prop=load(SRC/'route-adapter-proposal109.native.json')
g=load(ROOT/prop['proposed_graph']['path'])
old=load(ROOT/prop['original_graph']['path'])
coverage=load(ROOT/prop['coverage_overlay']['path'])
oldcov=load((ROOT/prop['original_graph']['path']).parent/'source-coverage109.native.json')
retrieval=load(ROOT/prop['proposed_retrieval']['path'])
oldretrieval=load(ROOT/prop['original_retrieval']['path'])
evidence=load(ROOT/prop['pinned_API_evidence']['path'])
primary=load(ROOT/prop['primary_first']['path'])
oldprimary=load((ROOT/prop['original_graph']['path']).parent/'primary-first109.native.json')
closure=load(SRC/'closed-RAW-route-adapter109.native.json')
ids=[n['id'] for n in g['nodes']]
edges=[(e['source'],e['target']) for e in g['edges']]
es=set(edges)
norm=lambda s:s.replace('MeasureTheory.ae_ae_of_ae_prod','MeasureTheory.Measure.ae_ae_of_ae_prod')
oldes={(norm(e['source']),norm(e['target'])) for e in old['edges']}
oldids={norm(n['id']) for n in old['nodes']}
indeg=dict.fromkeys(ids,0); adj=defaultdict(list)
for a,b in edges: indeg[b]+=1; adj[a].append(b)
q=deque(k for k,v in indeg.items() if not v); order=[]
while q:
    a=q.popleft();order.append(a)
    for b in adj[a]:
        indeg[b]-=1
        if not indeg[b]: q.append(b)
groups=[]
for r in g['new_AND_groups']:
    groups.append(dict(target=r['target'],self_required=r['target'] in r['parents'],missing_edges=[a for a in r['parents'] if (a,r['target']) not in es]))
conditional=g['conditional_route_groups109'][0]
sel=next(a for a in conditional['alternatives'] if a['id']==conditional['selected'])
alt=next(a for a in conditional['alternatives'] if a['id']!=conditional['selected'])
mandatory=next(a for a in g['new_AND_groups'] if a['target']==conditional['target'])
bindings=[]
for key in ('primary_first','original_graph','proposed_graph','original_retrieval','proposed_retrieval','coverage_overlay','pinned_API_evidence','production','sealed_header_unchanged'):
    bindings.append(bind(prop[key]))
for r in closure.get('inputs',[]): bindings.append(bind(r))
spans=[]
def inspect_spans(obj,path=''):
    if isinstance(obj,dict):
        if all(k in obj for k in ('file','start','end','raw_sha256','text')):
            raw=(ROOT/obj['file']['path']).read_bytes()
            span=b''.join(raw.splitlines(keepends=True)[obj['start']-1:obj['end']])
            spans.append(dict(evidence_path=path,file=bind(obj['file']),hash_ok=sha(span)==obj['raw_sha256'],text_ok=span.decode('utf-8')==obj['text']))
        for k,v in obj.items(): inspect_spans(v,path+'/'+k)
    elif isinstance(obj,list):
        for i,v in enumerate(obj): inspect_spans(v,path+'/'+str(i))
inspect_spans(evidence)
raw=(ROOT/primary['primary']['path']).read_bytes()
source_checks=[]
for s in primary['regions']:
    b=raw[s['byte_start']:s['byte_end_exclusive']]
    source_checks.append(dict(id=s['id'],hash_ok=sha(b)==s['raw_sha256'],line_byte_equal=b==b''.join(raw.splitlines(keepends=True)[s['line_start']-1:s['line_end']])))
prod=(ROOT/prop['production']['path']).read_bytes().decode('utf-8')
header=(ROOT/prop['sealed_header_unchanged']['path']).read_bytes().decode('utf-8')
pat=r'    \{E : Type\*\}.*?∃ hk : MemLp kTf 2 mu, Kpos T \(hf.toLp f\) = hk.toLp kTf\)'
prodstatement=re.search(pat,prod,re.S).group()
headerstatement=re.search(pat,header,re.S).group()
archives=[]
for a in closure.get('archives',[]):
    archive=a['archive']; original=a['original']
    b=(ROOT/archive['path']).read_bytes()
    dec=gzip.decompress(b)
    archives.append(dict(path=archive['path'],hash_ok=sha(b)==archive['raw_sha256'],exact_roundtrip=dec==(ROOT/original['path']).read_bytes()))
actualdiff=diff(old,g)
checks=dict(kind='independent exact route-adapter109 evidence and topology',reviewer='/root/blind_decoder106',
 proposal_raw_sha256=sha((SRC/'route-adapter-proposal109.native.json').read_bytes()),
 graph_raw_sha256=sha((ROOT/prop['proposed_graph']['path']).read_bytes()),
 author_closure_raw_sha256=sha((SRC/'closed-RAW-route-adapter109.native.json').read_bytes()),
 exact_graph_diff_matches_proposal=actualdiff==prop['exact_graph_diff'],independent_exact_graph_diff=actualdiff,
 nodes=len(ids),distinct_nodes=len(set(ids)),edges=len(edges),distinct_edges=len(es),acyclic=len(order)==len(ids),topological_order=order,
 namespace_normalized_old_nodes_preserved=oldids<=set(ids),namespace_normalized_old_edges_preserved=oldes<=es,
 added_nodes=sorted(set(ids)-oldids),added_edges=sorted(es-oldes),removed_nodes=sorted(oldids-set(ids)),removed_edges=sorted(oldes-es),
 corrected_effective_identity_only='MeasureTheory.ae_ae_of_ae_prod' not in json.dumps(g),
 AND_groups=groups,conditional_selected_AND_exact=mandatory['parents']==sel['AND'],
 selected_excludes_L2_integrable_inner='MeasureTheory.L2.integrable_inner' not in sel['AND'],
 alternative_retains_L2_integrable_inner='MeasureTheory.L2.integrable_inner' in alt['AND'],
 selected_requires_indicator='MeasureTheory.Integrable.indicator' in sel['AND'],
 conditional_target_not_own_parent=all(conditional['target'] not in a['AND'] for a in conditional['alternatives']),
 conditional_alternatives_edges_present=all((a,conditional['target']) in es for r in conditional['alternatives'] for a in r['AND']),
 final_OR_unchanged=g['OR_route_policy']==old['OR_route_policy'],
 selected_unselected_edge_metadata=[e for e in g['edges'] if e['target']=='MOMENTUM-L1-FUBINI109' and e['source'] in ('MeasureTheory.Integrable.indicator','MeasureTheory.L2.integrable_inner')],
 coverage_nodes_exact=Counter(x['id'] for x in coverage['node_dispositions'])==Counter(ids),
 coverage_edges_exact=Counter((x['source'],x['target']) for x in coverage['edge_dispositions'])==Counter(edges),
 source24_regions_unchanged=primary['regions']==oldprimary['regions'],
 coverage_source24_regions_unchanged=coverage['regions']==oldcov['regions'],
 source_region_checks=source_checks,
 retrieval_exact_diff=diff(oldretrieval,retrieval),
 same_header_full_statement_exact=prodstatement==headerstatement,
 same_header_full_statement_LF_normalized=prodstatement.replace('\r\n','\n')==headerstatement.replace('\r\n','\n'),
 direct_havg_L2_integrable_inner_call='L2.integrable_inner' in '\n'.join(prod.splitlines()[235:284]),
 direct_Integrable_indicator_call='hprod.indicator (hs.preimage measurable_fst)' in prod,
 direct_Measure_ae_ae_of_ae_prod_call='Measure.ae_ae_of_ae_prod hsec' in prod,
 file_bindings=bindings,pinned_API_and_proof_spans=spans,archives=archives,
 no_Lean_typecheck_reperformed=True)
(OUT/'checks109.native.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
small={k:checks[k] for k in ('proposal_raw_sha256','graph_raw_sha256','author_closure_raw_sha256','exact_graph_diff_matches_proposal','nodes','distinct_nodes','edges','distinct_edges','acyclic','added_nodes','added_edges','removed_nodes','removed_edges','corrected_effective_identity_only','conditional_selected_AND_exact','selected_excludes_L2_integrable_inner','alternative_retains_L2_integrable_inner','selected_requires_indicator','conditional_target_not_own_parent','conditional_alternatives_edges_present','final_OR_unchanged','coverage_nodes_exact','coverage_edges_exact','source24_regions_unchanged','coverage_source24_regions_unchanged','same_header_full_statement_exact','same_header_full_statement_LF_normalized','direct_havg_L2_integrable_inner_call','direct_Integrable_indicator_call','direct_Measure_ae_ae_of_ae_prod_call')}
small['bad_bindings']=[x for x in bindings if not x['hash_ok'] or not x['bytes_ok']]
small['bad_spans']=[x for x in spans if not x['file']['hash_ok'] or not x['hash_ok'] or not x['text_ok']]
small['bad_source']=[x for x in source_checks if not x['hash_ok'] or not x['line_byte_equal']]
small['bad_archives']=[x for x in archives if not x['hash_ok'] or not x['exact_roundtrip']]
small['AND_failures']=[x for x in groups if x['self_required'] or x['missing_edges']]
print(json.dumps(small,indent=2))
