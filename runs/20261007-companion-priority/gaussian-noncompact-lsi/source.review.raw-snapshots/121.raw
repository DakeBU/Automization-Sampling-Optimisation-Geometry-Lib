import collections
import datetime
import hashlib
import json
import pathlib

ROOT = pathlib.Path('E:/Samplinglib')
OUT = ROOT / 'runs/20261007-companion-priority/gaussian-noncompact-lsi-source-topology-review42'
SRC = ROOT / 'runs/20261007-companion-priority/gaussian-noncompact-lsi-source-graph42'
def sha(b): return hashlib.sha256(b).hexdigest()
def lf(b): return b.replace(b'\r\n', b'\n')
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def put(name, value):
    with (OUT / name).open('xb') as f:
        f.write((json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))

g = read(SRC / 'sourcegraph.json')
ins = read(SRC / 'source-inputs.json')
cov = read(SRC / 'source-coverage.json')['entries']
inv = read(SRC / 'named-use-inventory.json')
res = read(SRC / 'qualified-api-resolution.json')['entries']
prim = read(OUT / 'primary.contract.json')
bindings = []
seen = {}
def freeze(path, purpose, selected=None):
    path = path.resolve()
    if str(path) in seen: return seen[str(path)]
    b = path.read_bytes(); i = len(bindings)
    name = 'reviewer.graph.input.%03d' % i
    for suffix, data in [('.raw.snapshot', b), ('.lf.snapshot', lf(b))]:
        target = OUT / (name + suffix)
        if target.exists(): assert target.read_bytes() == data, 'immutable retry snapshot mismatch'
        else:
            with target.open('xb') as f: f.write(data)
    row = dict(index=i, path=str(path), raw_sha256=sha(b), lf_sha256=sha(lf(b)),
               raw_bytes=len(b), lf_bytes=len(lf(b)), purpose=purpose,
               raw_snapshot=name+'.raw.snapshot', lf_snapshot=name+'.lf.snapshot')
    if selected is not None: row['reviewed_selected_ranges'] = selected
    seen[str(path)] = row; bindings.append(row); return row

for name in ['sourcegraph-capsule.md','sourcegraph.json','sourcegraph.base.json',
             'sourcecontract.json','source-inputs.json','current-input-bindings.json',
             'source-coverage.json','named-use-inventory.json','qualified-api-resolution.json',
             'policy-chronology.json','authored-source-route.md','sourcegraph-run.json',
             'structural-check.json','lease.json','author.refinement.lease.json']:
    freeze(SRC/name, 'Actual independent graph-review input; author structural claims are not acceptance evidence')
for name in ['primary.contract.json','reviewer.topology.coverage-expectations.json',
             'reviewer.inputs.json','reviewer.exposure.json','reviewer.policy-lifecycle-delta.json',
             'reviewer.run.json','reviewer.topology.lease.json']:
    freeze(OUT/name, 'Previously CLOSED independent primary-before-graph baseline')

texts = {}; expected = set(); pin_checks = []
for x in ins:
    key = x['key']; row = freeze(SRC/(key+'.raw.snapshot'), 'Frozen source pin; mathematical reading limited to selected spans', x['ranges'])
    b = (SRC/(key+'.raw.snapshot')).read_bytes()
    assert row['raw_sha256'] == x['raw_sha256'] and row['lf_sha256'] == x['lf_sha256'], key
    assert (SRC/(key+'.lf.snapshot')).read_bytes() == lf(b), key
    texts[key] = lf(b).decode('utf-8').splitlines()
    for lo, hi in x['ranges']:
        assert 1 <= lo <= hi <= len(texts[key]), key
        expected.update((key,i) for i in range(lo,hi+1))
    if x.get('path') and key != 'SLTreusePolicy':
        current = (ROOT/x['path']).read_bytes()
        assert current == b, ('current mathematical drift', key)
    pin_checks.append(dict(source=key,raw_sha256=sha(b),lf_sha256=sha(lf(b)),selected_ranges=x['ranges']))
for key, filename in [('authored-source-route','authored-source-route.md'),('Statement42','Statement42.raw.snapshot'),('SLTreusePolicy.current-append','SLTreusePolicy.current.raw.snapshot')]:
    freeze(SRC/filename, 'Route/signature/current policy evidence')
    texts[key] = (SRC/filename).read_text(encoding='utf-8').splitlines()
for name in ['SourceDetail42.raw.snapshot','StatementSeal42.raw.snapshot']:
    if (SRC/name).exists(): freeze(SRC/name,'Historical preread/statement identity only; no proof approval')

assert sha((SRC/'sourcegraph.json').read_bytes()) == 'bd2da75c9ce3444861c512aba0e0859872ca0cd2abcc365d0920e2f76ac4db82'
assert sha((OUT/'primary.contract.json').read_bytes()) == '892427bc157872c9d844195d1b4f62e87f65294f6508ee3ac8c1d3b5779d2a1b'
keys = [(x['source'],x['line']) for x in cov]
assert len(keys)==len(set(keys)) and expected <= set(keys)
nodes = {x['id']:x for x in g['nodes']}
assert len(nodes)==len(g['nodes'])
for x in cov:
    assert x['disposition'] in ['NODE','EXCLUDED']
    assert (x.get('node') in nodes) if x['disposition']=='NODE' else bool(x.get('reason'))
    assert 1<=x['line']<=len(texts[x['source']])
named = []
for e in g['edges']:
    assert e['prerequisite'] in nodes and e['consumer'] in nodes, e['id']
    s=e['consumer_use_site']; t=texts[s['source']]
    assert 1<=s['line_start']<=s['line_end']<=len(t),e['id']
    if s.get('column_start'):
        # Both columns are one-based inclusive; independently inferred and verified for all725.
        assert t[s['line_start']-1][s['column_start']-1:s['column_end']]==e['source_token'],e['id']
        named.append(e)
assert len(named)==725
edge_keys=collections.Counter((e['consumer'],e['consumer_use_site']['source'],e['consumer_use_site']['line_start'],e['source_token'],e['consumer_use_site']['column_start'],e['consumer_use_site']['column_end']) for e in named)
inventory_keys=collections.Counter((x['provider'],x['source'],x['line'],x['token'],x['columns'][0],x['columns'][1]) for x in inv['entries'] if 'edge' in x['disposition'])
assert edge_keys==inventory_keys
assert g['compiled_edges']==[] and len(g['alternative_routes'])==2

# Pin each asserted external locator; inspect declaration headers, not whole imported proof bodies.
locator_evidence=[]
for x in res:
    loc=x['declaration_locator']
    if loc.get('path'):
        row=freeze(ROOT/loc['path'],'Imported locator source pin; only exact declaration header inspected')
        line=(ROOT/loc['path']).read_text(encoding='utf-8').splitlines()[loc['line']-1]
    else:
        line=texts[loc['source']][loc['line']-1]
    locator_evidence.append(dict(token=x['token'],claimed_qname=x['resolved_qname'],caller_source=x['source'],caller_line=x['line'],locator=loc,header=line))

correct = {
 'abs_of_nonpos':dict(qname='abs_of_nonpos',path='.lake/packages/mathlib/Mathlib/Algebra/Order/Group/Unbundled/Abs.lean',lines=[95,96],kind='to_additive generated alias of mabs_of_le_one; no compiler claim'),
 'abs_of_nonneg':dict(qname='abs_of_nonneg',path='.lake/packages/mathlib/Mathlib/Algebra/Order/Group/Unbundled/Abs.lean',lines=[90,91],kind='to_additive generated alias of mabs_of_one_le; no compiler claim'),
 'norm_add_le':dict(qname='norm_add_le',path='.lake/packages/mathlib/Mathlib/Analysis/Normed/Group/Basic.lean',lines=[96,99],kind='explicit to_additive generated alias of norm_mul_le\'; no compiler claim'),
 'dist_zero_right':dict(qname='dist_zero_right',path='.lake/packages/mathlib/Mathlib/Analysis/Normed/Group/Basic.lean',lines=[50,52],kind='to_additive generated alias of dist_one_right; no compiler claim'),
 'neg_nonneg':dict(qname='neg_nonneg',path='.lake/packages/mathlib/Mathlib/Algebra/Order/Group/Unbundled/Basic.lean',lines=[453,455],kind='explicit to_additive alias of one_le_inv\'; no compiler claim')}
for x in correct.values(): freeze(ROOT/x['path'],'Correct generated-global API locator evidence', [x['lines']])
def occurrences(tokens, sources=None):
    out=[]
    for e in named:
        if e['source_token'] in tokens and (sources is None or e['consumer_use_site']['source'] in sources):
            s=e['consumer_use_site'];out.append(dict(edge=e['id'],prerequisite=e['prerequisite'],consumer=e['consumer'],token=e['source_token'],site=s,literal_line=texts[s['source']][s['line_start']-1]))
    return out
wrong=occurrences(set(correct))
syntax=occurrences({'norm_map\'','to_dual','self'},{'MathlibRiesz','MathlibOrder'})
# self in the two to_dual attributes is also syntax, not an unresolved proof ingredient.
syntax=[x for x in syntax if (x['site']['source']=='MathlibRiesz' and x['site']['line_start']==67) or (x['site']['source']=='MathlibOrder' and x['site']['line_start'] in [471,476])]
repairs=[
 dict(id='T1',class_='WRONG_QUALIFIED_API_PROVIDER',occurrences=wrong,correct_source_locators=correct,
      request='Retarget exactly these scalar/Hilbert calls to the actual global generated APIs with explicit generator source pins, or honestly keep imported-unexpanded source tokens with no asserted unrelated QName. Update corresponding nodes/resolution entries; do not invent selected-file declarations.'),
 dict(id='T2',class_='SYNTAX_MISCLASSIFIED_AS_MATHEMATICAL_DEPENDENCY',occurrences=syntax,
      request='Classify to_dual/self attribute tokens as attribute syntax, not proof calls; norm_map\' at Riesz67 is the linear-isometry structure field being assigned, not the global norm_map\' lemma. Remove their fake proof-use edges/locators or represent an explicit structure-field typing boundary without an unrelated theorem provider. Attribute471 belongs to following declaration472; attribute476 belongs to alias477, not previous theorem bodies.'),
 dict(id='T3',class_='INACCURATE_SELECTED_SOURCE_EXCLUSION',occurrences=occurrences({'mul_log_nonpos'}),
      selected_source='MathlibPhi',selected_lines=[153,154],literal_lines=texts['MathlibPhi'][152:154],
      request='Replace the false outside-route EXCLUDED reason on153–154. Either map these selected lines to existing Real.mul_log_nonpos primitive with an explicit unexpanded-body boundary, or expand the genuine provider and its two actual calls mul_nonpos_of_nonneg_of_nonpos/log_nonpos. Do not claim fresh full proof coverage while retaining outside-route exclusion. Other151–152/155–158 may retain accurate tail/trivia/unneeded-lemma exclusions.')]
put('reviewer.graph.repair-request.json',dict(status='BLOCKED_REPRESENTATION_ONLY',repairs=repairs,unchanged_target_lf_sha256=prim['prospective_target_identity']['lf_sha256']))
put('reviewer.graph.locator-evidence.json',locator_evidence)
policy=read(SRC/'policy-chronology.json');old=(SRC/'SLTreusePolicy.raw.snapshot').read_bytes();cur=(SRC/'SLTreusePolicy.current.raw.snapshot').read_bytes()
assert cur.startswith(old) and lf(cur).startswith(lf(old))
assert (ROOT/'research-wiki/cited-results/SLT_reuse_audit.md').read_bytes()==cur
counts=dict(nodes=len(g['nodes']),edges=len(g['edges']),OR_routes=len(g['alternative_routes']),provider_declarations=len(inv['providers']),selected_source_inputs=len(ins),selected_physical_lines=len(expected),coverage_rows=len(cov),named_source_use_occurrences=len(named),asserted_resolution_occurrences=len(res),unelaborated_source_token_boundaries=354,opaque_source_token_boundaries=37)
checks=dict(status='INDEPENDENT_BOUNDED_CHECKS_NOT_MATHEMATICAL_COMPLETION',counts=counts,all21source_raw_LF_pins=True,all_current_mathematical_pins_identical=True,unique_disjoint_selected_line_partition=True,every_selected_line_has_node_or_reason=True,coverage_reason_semantics='BLOCKED T3; enumeration passes',all725inclusive_column_literals_match=True,all725inventory_edge_occurrences_bijective=True,all_node_edge_references_exist=True,qualified_resolution_semantics='BLOCKED T1/T2; lexical declaration existence does not select overloaded actual call',compiled_edges_empty=True,OR_routes_separate=True,policy_original_raw_and_LF_prefix_preserved=True,policy_append_1339_1345_math_excluded=True,policy_chronology=policy,source_pins=pin_checks)
put('reviewer.graph.checks.json',checks)
put('reviewer.graph.inputs.json',bindings)
review=dict(schema_version=1,status='BLOCKED',verdict='BLOCKED_SOURCE_TOPOLOGY_REPRESENTATION_ONLY',actor='gaussian_domain_preproof_reviewer_29',graph_creator='gaussian_noncompact_preread_42',role='Distinct independent source-only topology validator; not graph author/prover',primary_before_graph_contract_sha256=sha((OUT/'primary.contract.json').read_bytes()),checked_graph_raw_sha256=sha((SRC/'sourcegraph.json').read_bytes()),checked_graph_lf_sha256=sha(lf((SRC/'sourcegraph.json').read_bytes())),sourcecontract_raw_sha256=sha((SRC/'sourcecontract.json').read_bytes()),counts=counts,mathematical_contract_verdict='ACCEPTED_SCOPED_SOURCE_ONLY_CONTRACT; no theorem/proof/statement admission',seven_semantic_slots=prim['seven_semantic_slots'],binder_classification=dict(SOURCE='Printed FIRST4.6 Gaussian LSI/Talagrand invocation only; no printed cutoff function theorem',TYPECLASS='Real complete finite Hilbert and Borel carrier structures',DEFINITION='Literal stdGaussian/global gradient/Phi/real Bochner integral; domain predicates retain frozen independent expansion',AUTHORED_DOMAIN='C2, fL2, actual gradient L2, actual Phi(f²)L1; actual32 supplies downstream domains',DERIVED='q and energy L1; chi C/R/support/regularity; all observers/domination; three true real integral limits',EXCESS=[]),mathematical_route_audit=dict(route='chi_(n+1)*f sufficient C2 route, distinct external W12/mollification/Fatou OR',domination='q; abs(Phi(q))+q; 2norm(grad f)^2+2C²q with radius>=1 and C fixed before radii',constant='2 unchanged; future actual32 energy1/4 yields Fisher1/2 only after law/witness coherence',zero_sign_rank0='Included; Phi0=0, no positivity or mass normalization, eventual equality of cutoff on neighborhoods gives true gradients',actual32='Downstream applicability, not generic42 parent',no_public_cutoff_or_limit_or_desired_inequality_certificates=True),blockers=repairs,required_minimal_repair='Preserve original BLOCKED graph/raw source inputs and691 statement. Author distinct immutable representation successor; correct T1/T2 provenance and T3 selected-line reason. Regenerate honest counts/locator inventory only for exact repairs; distinct review before proof search.',source_coverage_boundary='1952 selected physical lines plus27 authored-route,13 signature,7 policy rows enumerated; not whole external project coverage. Prior frozen MemLp/Integrable/HasFiniteIntegral definition floor remains reviewer-owned reused context; no claim these extra definitions were newly covered by graph.',historical_exposure='Previously disclosed29/32/33/41 mathematical/API history and42 pregraph target shape. Original primary-before-graph contract CLOSED before any42 graph exposure. Current graph-author deviations retained from sourcecontract; reviewer is not source-blind decoder. No42 implementation/Test/blind exists or was read; no41 lesson/blind/finalsource read in this task.',policy_delta='Exact historical raw/LF policy prefix preserved;1339–1345 lifecycle append is EXCLUDED mathematics, matches previous primary contract drift receipt.',remaining_truth_boundary=['42 analytic proof remains unproved; source-topology repair admission is not theorem credit','Full weak-W12/density/representative/carrier transport not obtained','p32=p33 and same rho/q/r canonicalKL-Fisher adapter still residual','Gaussian T2, metric/coupling/second-moment adapters and FIRST4.6 W2 remain open','Paper main/bias/work/cost/composition and PURIFIED remain open'],compiler_started=False,no_graph_repairs_or_canonical_writes=True,input_manifest='reviewer.graph.inputs.json',checks='reviewer.graph.checks.json',repair_request='reviewer.graph.repair-request.json',all_leases='CLOSED at completion')
put('source-topology-review.json',review)
lease=read(OUT/'reviewer.graph-review.lease.json');lease.update(status='CLOSED',read_lease='CLOSED',write_lease='CLOSED',Python_lease='CLOSED',compiler_lease='CLOSED',compiler_started=False,closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),outcome='BLOCKED_SOURCE_TOPOLOGY_REPRESENTATION_ONLY')
(OUT/'reviewer.graph-review.lease.json').write_bytes((json.dumps(lease,indent=2)+'\n').encode())
put('reviewer.graph-review.lease.closed.json',lease)
artifacts=[]
for name in ['source-topology-review.json','reviewer.graph.checks.json','reviewer.graph.inputs.json','reviewer.graph.repair-request.json','reviewer.graph.locator-evidence.json','reviewer.graph-review.lease.closed.json','reviewer.graph.check.py']:
    b=(OUT/name).read_bytes();artifacts.append(dict(path=name,raw_sha256=sha(b),lf_sha256=sha(lf(b))))
run_hash=sha(json.dumps(artifacts,sort_keys=True,separators=(',',':')).encode())
put('reviewer.graph.run.json',dict(status='CLOSED',run_sha256=run_hash,artifacts=artifacts,input_count=len(bindings),compiler_never_started=True))
print(json.dumps(dict(verdict=review['verdict'],review_sha256=sha((OUT/'source-topology-review.json').read_bytes()),run_sha256=run_hash,counts=counts,repair_occurrences=[len(wrong),len(syntax),1],inputs=len(bindings),leases='CLOSED')))
