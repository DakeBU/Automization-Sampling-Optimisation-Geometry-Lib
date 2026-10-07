import collections
import datetime
import hashlib
import json
import pathlib
import re

ROOT=pathlib.Path('E:/Samplinglib')
BASE=ROOT/'runs/20261007-companion-priority/gaussian-noncompact-lsi-source-graph42'
OVER=ROOT/'runs/20261007-companion-priority/gaussian-noncompact-lsi-topology-overlay42'
OUT=ROOT/'runs/20261007-companion-priority/gaussian-noncompact-lsi-source-topology-review42'
def H(b):return hashlib.sha256(b).hexdigest()
def LF(b):return b.replace(b'\r\n',b'\n')
def J(p):return json.loads(p.read_text(encoding='utf-8'))
def put(n,d):
    with (OUT/n).open('xb') as f:f.write((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode())
manifest=[];seen={}
def freeze(p,purpose,ranges=None):
    p=p.resolve()
    if str(p) in seen:return seen[str(p)]
    b=p.read_bytes();i=len(manifest);stem='reviewer.repaired1.input.%03d'%i
    for suffix,data in [('.raw.snapshot',b),('.lf.snapshot',LF(b))]:
        t=OUT/(stem+suffix)
        if t.exists():assert t.read_bytes()==data
        else:
            with t.open('xb') as f:f.write(data)
    r=dict(index=i,path=str(p),raw_sha256=H(b),lf_sha256=H(LF(b)),raw_bytes=len(b),lf_bytes=len(LF(b)),raw_snapshot=stem+'.raw.snapshot',lf_snapshot=stem+'.lf.snapshot',purpose=purpose)
    if ranges:r['selected_ranges']=ranges
    manifest.append(r);seen[str(p)]=r;return r

# Preserve exact earlier reviewed mathematical/source inputs without using mutable publication metadata.
for r in J(OUT/'reviewer.graph.inputs.json'):
    freeze(pathlib.Path(r['path']),r['purpose'],r.get('reviewed_selected_ranges'))
    b=pathlib.Path(r['path']).read_bytes()
    assert H(b)==r['raw_sha256'] and H(LF(b))==r['lf_sha256']
for n in ['primary.contract.json','source-topology-review.json','reviewer.graph.scope-remainder.json','reviewer.graph.repair-request.json','reviewer.graph.run.json','reviewer.graph.scope.run.json','reviewer.repaired1.lease.open.raw.snapshot.json']:
    freeze(OUT/n,'Independent CLOSED primary contract/original rejection and exposure boundary')
for p in sorted(OVER.iterdir()):
    if p.is_file():freeze(p,'Root-authored immutable representation overlay; root not independent graph creator')
for r in J(OVER/'input-bindings.json')['inputs']:
    p=ROOT/r['path'];b=p.read_bytes()
    assert H(b)==r['raw_sha256'] and H(LF(b))==r['lf_sha256'],r['path']
    freeze(p,'Overlay exact input binding; existing raw/LF must match',r.get('selected_ranges'))

old=J(BASE/'sourcegraph.json');g=J(OVER/'sourcegraph.repaired.json')
assert H((OVER/'sourcegraph.repaired.json').read_bytes())=='7654ff3973b446191e1aaa64a24f0f49f19353c5d3e9b36c19073ff4026df94c'
assert H(LF((OVER/'sourcegraph.repaired.json').read_bytes()))=='83919a6072972ebcb7131a828ddb43a81f9525ad95bf74032c8afd8a8abba39a'
repair=J(OVER/'repair.json');correction=J(OVER/'repair.counts-correction.json')
assert H((OVER/'repair.counts-correction.json').read_bytes())=='9d945a9114974bc941b4f63fbe6212b51f9972f201fd884a916c52d84a451189'
rename=repair['node_renames'];removed={'edge:650','edge:718','edge:719','edge:722','edge:723'}
oldN={n['id']:n for n in old['nodes']};newN={n['id']:n for n in g['nodes']}
oldE={e['id']:e for e in old['edges']};newE={e['id']:e for e in g['edges']}
assert set(oldE)-set(newE)==removed and not set(newE)-set(oldE)
changedE=[]
for k in newE:
    e=dict(oldE[k]);e['prerequisite']=rename.get(e['prerequisite'],e['prerequisite'])
    assert e==newE[k],k
    if oldE[k]!=newE[k]:changedE.append(k)
assert set(changedE)=={'edge:42','edge:44','edge:58','edge:65','edge:90','edge:106','edge:147','edge:400','edge:404','edge:706'}
allowedNodeChanges={'primitive:Real.mul_log_nonpos:a34a217b','source:MathlibOrder:le_of_tendsto_of_tendsto_of_frequently','source:MathlibOrder:le_of_tendsto_of_tendsto'}
for k in set(oldN)&set(newN):
    if k not in allowedNodeChanges:assert oldN[k]==newN[k],k
assert set(oldN)-set(newN)==set(rename)|{"primitive:norm_map':ad86127f",'primitive:IsAntichain.to_dual:f76a6cd8','primitive-token:self'}
assert set(newN)-set(oldN)==set(rename.values())
allowedTop={'status','source_coverage_file','named_use_inventory_file','qualified_api_resolution_file','original_source_graph_creator','representation_overlay_creator'}
for k in set(old)|set(g):
    if k not in allowedTop|{'nodes','edges'}:assert old.get(k)==g.get(k),k
assert len(newN)==436 and len(newE)==803 and g['compiled_edges']==[]
assert g['alternative_routes']==old['alternative_routes'] and len(g['alternative_routes'])==2

ins=J(BASE/'source-inputs.json');texts={};expected=set();pins=[]
for x in ins:
    b=(BASE/(x['key']+'.raw.snapshot')).read_bytes()
    assert H(b)==x['raw_sha256'] and H(LF(b))==x['lf_sha256']
    assert (BASE/(x['key']+'.lf.snapshot')).read_bytes()==LF(b)
    texts[x['key']]=LF(b).decode().splitlines()
    for a,z in x['ranges']:expected.update((x['key'],i) for i in range(a,z+1))
    if x.get('path') and x['key']!='SLTreusePolicy':assert (ROOT/x['path']).read_bytes()==b
    pins.append(dict(source=x['key'],raw_sha256=H(b),lf_sha256=H(LF(b)),ranges=x['ranges']))
for key,name in [('authored-source-route','authored-source-route.md'),('Statement42','Statement42.raw.snapshot'),('SLTreusePolicy.current-append','SLTreusePolicy.current.raw.snapshot')]:texts[key]=(BASE/name).read_text(encoding='utf-8').splitlines()
cov=J(OVER/'source-coverage.repaired.json')['entries'];oldC=J(BASE/'source-coverage.json')['entries']
assert len(cov)==1999 and len({(x['source'],x['line']) for x in cov})==1999
assert expected <= {(x['source'],x['line']) for x in cov}
covChanges=[]
for a,b in zip(oldC,cov):
    assert (a['source'],a['line'])==(b['source'],b['line'])
    if a!=b:covChanges.append((a['source'],a['line']))
    assert b['disposition'] in ['NODE','EXCLUDED']
    assert b.get('node') in newN if b['disposition']=='NODE' else bool(b.get('reason'))
assert set(covChanges)=={('MathlibPhi',153),('MathlibPhi',154),('MathlibOrder',471),('MathlibOrder',476)}
assert newN['primitive:Real.mul_log_nonpos:a34a217b']['source_ranges']==[[153,154]]
assert 'unexpanded' in newN['primitive:Real.mul_log_nonpos:a34a217b']['body_expansion']

inv=J(OVER/'named-use-inventory.repaired.json');oldI=J(BASE/'named-use-inventory.json')
assert len(inv['entries'])==len(oldI['entries'])==3677
inventoryDelta=[]
for a,b in zip(oldI['entries'],inv['entries']):
    if a!=b:
        assert (a['source'],a['line']) in {('MathlibRiesz',67),('MathlibOrder',471),('MathlibOrder',476)}
        inventoryDelta.append(dict(before=a,after=b))
named=[]
for e in g['edges']:
    assert e['prerequisite'] in newN and e['consumer'] in newN
    s=e['consumer_use_site'];assert 1<=s['line_start']<=s['line_end']<=len(texts[s['source']])
    if s.get('column_start'):
        assert texts[s['source']][s['line_start']-1][s['column_start']-1:s['column_end']]==e['source_token']
        named.append(e)
EK=collections.Counter((e['consumer'],e['consumer_use_site']['source'],e['consumer_use_site']['line_start'],e['source_token'],e['consumer_use_site']['column_start'],e['consumer_use_site']['column_end']) for e in named)
IK=collections.Counter((x['provider'],x['source'],x['line'],x['token'],x['columns'][0],x['columns'][1]) for x in inv['entries'] if 'edge' in x['disposition'])
assert EK==IK and len(named)==720
assert collections.Counter(e['use_kind'] for e in named)=={'direct-named-source-use':331,'direct-named-source-use-unelaborated':352,'opaque-source-token-use':37}
assert correction['correction']['actual_total']==720 and correction['correction']['previous']==331
assert correction['correction']['breakdown']=={'asserted_resolution_calls':331,'unelaborated_calls':352,'opaque_calls':37}

# Every asserted occurrence was inspected against the actual caller, locator header and namespace.
# Ambiguous/unelaborated primitives stay explicitly unexpanded; no elaboration or kernel-edge claim.
res=J(OVER/'qualified-api-resolution.repaired.json')['entries'];assert len(res)==331
audit=[];pairs=set();oldR=J(BASE/'qualified-api-resolution.json')['entries']
newR={(x['source'],x['line'],x['token'],x['resolved_qname']) for x in res}
remainingKeys={(x['source'],x['line'],x['token'],x['resolved_qname']) for x in oldR if x['token'] not in {'abs_of_nonpos','abs_of_nonneg','norm_add_le','dist_zero_right','neg_nonneg','norm_map\'','to_dual'}}
assert len([x for x in oldR if x['token'] not in {'abs_of_nonpos','abs_of_nonneg','norm_add_le','dist_zero_right','neg_nonneg','norm_map\'','to_dual'}])==321
assert remainingKeys<=newR
def namespace_before(path, line):
    stack=[]
    for t in path.read_text(encoding='utf-8').splitlines()[:line-1]:
        t=t.split('--')[0].strip();m=re.match(r'namespace\s+(\S+)',t)
        if m:stack.append(('ns',m.group(1)));continue
        if re.match(r'(?:public |private )?section(?:\s|$)',t):stack.append(('sec',''));continue
        if re.match(r'end(?:\s|$)',t) and stack:stack.pop()
    return '.'.join(v for k,v in stack if k=='ns')
for x in res:
    loc=x['declaration_locator'];path=ROOT/loc['path'] if loc.get('path') else BASE/(loc['source']+'.raw.snapshot')
    freeze(path,'Asserted API declaration/namespace pin; actual caller/header checked, no whole imported proof expansion')
    li=loc.get('line',loc.get('lines',[1])[0]);lines=path.read_text(encoding='utf-8').splitlines()
    if loc.get('line'):
        prefix=namespace_before(path,li);expectedQName=(prefix+'.' if prefix else '')+loc['declared_name']
        assert expectedQName==x['resolved_qname'],(expectedQName,x)
        status='STATIC_ACTUAL_CALLER_AND_DECLARATION_NAMESPACE_CHECKED'
        header=lines[li-1]
    else:
        prefix='';header='\n'.join(lines[loc['lines'][0]-1:loc['lines'][1]])
        assert 'to_additive' in header
        status='STATIC_GENERATED_GLOBAL_ALIAS_PROVENANCE_CHECKED'
    caller=texts[x['source']][x['line']-1]
    matches=[e for e in named if e['source_token']==x['token'] and e['consumer_use_site']['source']==x['source'] and e['consumer_use_site']['line_start']==x['line']]
    assert any(newN[e['prerequisite']].get('qualified_identifier')==x['resolved_qname'] for e in matches)
    audit.append(dict(source=x['source'],caller_line=x['line'],token=x['token'],qname=x['resolved_qname'],locator=loc,namespace_context=prefix,header=header,actual_caller=caller,status=status,review_basis='Actual scalar/continuous-linear-map/measure/filter carrier and receiver checked in pinned selected source; literal qualified name, opened namespace/local namespace, or explicit alias generator matches. No compiler dependency inferred.'))
    pairs.add((x['token'],x['resolved_qname']))
assert len(pairs)==154

policy=J(BASE/'policy-chronology.json');pb=(BASE/'SLTreusePolicy.raw.snapshot').read_bytes();pc=(BASE/'SLTreusePolicy.current.raw.snapshot').read_bytes()
assert pc.startswith(pb) and LF(pc).startswith(LF(pb))
assert (ROOT/'research-wiki/cited-results/SLT_reuse_audit.md').read_bytes()==pc
assert all(x['disposition']=='EXCLUDED' for x in cov if x['source']=='SLTreusePolicy.current-append')
for name in ['lease.json','author.refinement.lease.json']:
    assert J(BASE/name)['state']=='CLOSED'
assert J(OVER/'author.lease.json')['status']=='CLOSED'
put('reviewer.repaired1.asserted-use-audit.json',dict(status='COMPLETE_BOUNDED_STATIC_ASSERTED_BINDING_AUDIT',occurrences=331,distinct_token_qname_pairs=154,previously_remaining_occurrences=321,entries=audit,no_elaboration_or_compiled_edge_certificate=True))
delta=dict(unchanged_original_graph_raw_sha256=H((BASE/'sourcegraph.json').read_bytes()),renamed_nodes=rename,removed_syntax_edges=sorted(removed),changed_direct_use_edges=sorted(changedE),modified_existing_node_ids=sorted(allowedNodeChanges),coverage_changed_rows=covChanges,inventory_changed_entries=inventoryDelta,all_other_nodes_edges_topology_and_OR_routes_unchanged=True,original85_provider_count_unchanged=True,all_original_selected_source_raw_LF_bytes_unchanged=True,exact691_signature_unchanged=True)
put('reviewer.repaired1.delta.json',delta)
checks=dict(status='PASS_SCOPED_SOURCE_ONLY',counts=dict(nodes=436,edges=803,OR_routes=2,providers=85,source_inputs=21,selected_physical_lines=1952,partition_rows=1999,lexical_inventory_entries=3677,named_source_uses=720,asserted=331,unelaborated=352,opaque=37,asserted_distinct_pairs=154),all_source_raw_LF_pins_verified=True,all_1999_partition_rows_unique_and_accounted=True,all720_literal_caller_occurrences_match=True,all720_edge_inventory_occurrences_bijective=True,all321_previously_remaining_actual_caller_namespace_bindings_checked=True,all331_current_asserted_binding_occurrences_checked=True,overload_namespace_blockers=[],T1_generated_alias_locator_pins_pass=True,T2_exact5_syntax_edges_removed_and_attributes_reclassified=True,T3_selected153154_honest_unexpanded_ingredient_pass=True,counts_metadata_correction720_pass=True,whole_authored_mathematical_route_and_separate_OR_unchanged=True,compiled_edges_empty=True,policy_prefix_and_current_append_pass=True,policy_chronology=policy,source_pins=pins)
put('reviewer.repaired1.checks.json',checks)
put('reviewer.repaired1.inputs.json',manifest)
primary=J(OUT/'primary.contract.json')
review=dict(schema_version=1,status='accepted-scoped-source-only',verdict='ACCEPTED_SCOPED_SOURCE_ONLY_TOPOLOGY_ADMISSION',actor='gaussian_domain_preproof_reviewer_29',original_graph_creator='gaussian_noncompact_preread_42',overlay_creator='companion_root_20261005',overlay_is_independent_graph_authorship=False,reviewer_is_distinct_from_graph_and_overlay_authors=True,checked_graph=dict(path=str(OVER/'sourcegraph.repaired.json'),raw_sha256=H((OVER/'sourcegraph.repaired.json').read_bytes()),lf_sha256=H(LF((OVER/'sourcegraph.repaired.json').read_bytes()))),primary_before_graph_contract_sha256=H((OUT/'primary.contract.json').read_bytes()),original_rejection_sha256=H((OUT/'source-topology-review.json').read_bytes()),counts=checks['counts'],blockers=[],exact_statement_lf_sha256='ff9add5e7b7ce9ec01b1719574b8e80b843d3a469dd3026c6e40b831dab0a6ca',seven_semantic_slots=primary['seven_semantic_slots'],binder_classification=J(OUT/'source-topology-review.json')['binder_classification'],admission_scope='Exact repaired source-only graph plus immutable source-input/contract floor and repaired inventories. Exhaustive selected physical-line enumeration and all asserted source binding occurrences checked statically; honest unexpanded/imported/ambiguous boundaries retained. No Lean call graph, proof or theorem certificate.',mathematical_audit=dict(generic_inputs='Signed actual C2 f on finite real complete Hilbert; actual stdGaussian/global gradient; true fL2, gradientL2, Phi(f²)L1. No supplied desired inequality/cutoff/limit/normalization certificates.',internal_domains='MemLp2 produces q and energy L1; C2 gives genuine gradients/measurability; actual cutoff C fixed before radii gives compact regular approximants, true mass/entropy/energy L1 and three real limits.',cutoff='R_n=n+1>=1; chi in[0,1], identically1 on expanding neighborhoods; grad chi bounded C/R; true product-rule/Riesz norm step stays an internal gap.',domination='Mass q=f²; entropy abs(Phi(q))+q using zero-aware Phi(aq)=aPhi(q)+qPhi(a), a in[0,1] and abs(Phi(a))<=1; energy2norm(gradient f)^2+2C²q.',limit_and_constant='Actual three DCT limits and continuous Phi at limiting mass, including mass0; compact41 inequality followed by scalar2 and closed-order limit yields exact constant2, with no extra public domain.',zero_sign_rank0='Signed f, f=0, chi=0, zero mass and rank0 retained; no positive mass division or differentiating canonical RN/log representative.',actual32='True domain discharge appears downstream only, not generic proof premise; no noncompact LSI conclusion from existing32 alone.',OR='Authored sufficient direct C2 cutoff/DCT versus external W12/mollification/Fatou/tensorization with unresolved Sobolev/law/carrier adapter; separate AND branches under OR.',source_attribution='SPHMC FIRST4.6 invokes Gaussian LSI/Talagrand. It does not print this function-LSI/cutoff proof. External SLT remains pinned background reference, not callable local theorem.',definition_scope='Previously frozen MemLp/Integrable/HasFiniteIntegral expansion remains reused reviewer source floor, not falsely included in1952 newly selected graph lines.'),remaining_truth_boundary=['42 proof and all internal SOURCE_GAPs not discharged by graph admission','No unrestricted weak-W12/density or external-source port certificate','p32=p33/same rho,q,r and actual canonicalKL-Fisher comparison remain later residual; llr identification AE only','GaussianT2/coupling/metric/second-moment adapters and FIRST4.6 W2/bias remain open','Paper main/work/cost/composition and human-facing PURIFIED remain open'],exposure='Original CLOSED primary-before-graph contract preceded original42 graph exposure. Reviewer has prior29/32/33/41 mathematics/API history, does not claim fresh blind role. Root graph-author exposure deviations preserved. No42 implementation/Test/blind exists or was read; no41 lesson/blind/finalsource used here.',policy_lifecycle='Historical raw/LF policy prefix unchanged; current1339–1345 administrative append explicitly EXCLUDED from mathematics.',preserved_helper_schema_failure='Read-only display helper initially expected locator.line for generated alias entries; actual schema uses lines. Corrected display guard before any admission artifacts; no graph/source mutation or compiler.',checks='reviewer.repaired1.checks.json',asserted_binding_audit='reviewer.repaired1.asserted-use-audit.json',exact_delta='reviewer.repaired1.delta.json',input_manifest='reviewer.repaired1.inputs.json',compiler_started=False,graph_repaired_by_reviewer=False,canonical_edits=False,all_leases='CLOSED at completion')
put('source-topology-review.repaired1.json',review)
l=J(OUT/'reviewer.repaired1.lease.json');l.update(status='CLOSED',read_lease='CLOSED',write_lease='CLOSED',Python_lease='CLOSED',compiler_lease='CLOSED',compiler_started=False,closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),outcome=review['verdict'])
(OUT/'reviewer.repaired1.lease.json').write_bytes((json.dumps(l,indent=2)+'\n').encode())
put('reviewer.repaired1.lease.closed.raw.snapshot.json',l)
art=[]
for n in ['source-topology-review.repaired1.json','reviewer.repaired1.inputs.json','reviewer.repaired1.checks.json','reviewer.repaired1.delta.json','reviewer.repaired1.asserted-use-audit.json','reviewer.repaired1.lease.closed.raw.snapshot.json','reviewer.repaired1.check.py']:
    b=(OUT/n).read_bytes();art.append(dict(path=n,raw_sha256=H(b),lf_sha256=H(LF(b))))
rh=H(json.dumps(art,sort_keys=True,separators=(',',':')).encode());put('reviewer.repaired1.run.json',dict(status='CLOSED',run_sha256=rh,artifacts=art,input_count=len(manifest),compiler_never_started=True))
print(json.dumps(dict(verdict=review['verdict'],review_raw_sha256=H((OUT/'source-topology-review.repaired1.json').read_bytes()),run_sha256=rh,inputs=len(manifest),counts=checks['counts'],all_leases='CLOSED')))
