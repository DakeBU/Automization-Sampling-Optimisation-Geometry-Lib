from pathlib import Path
import json, hashlib, datetime
p=Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-reflected-density-sourcegraph53')
q=Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-reflected-density-topology-overlay53')
o=Path(__file__).parent
sha=lambda b:hashlib.sha256(b).hexdigest()
lf=lambda b:b.replace(b'\r\n',b'\n')
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def J(p,f):return json.loads((p/f).read_bytes())
def logical(x,k):
    z=dict(x);z.pop(k,None)
    return sha(json.dumps(z,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode())
def dump(path,x):path.write_bytes((json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode())
def desc(path):
    path=Path(path).absolute();b=path.read_bytes();a=lf(b)
    return dict(path=str(path),raw_bytes=len(b),lf_bytes=len(a),raw_sha256=sha(b),lf_sha256=sha(a))
oldrun=J(p,'run.json');newrun=J(q,'run.json');old=J(o,'source-topology-review.json')
assert desc(o/'source-topology-review.json')['raw_sha256']=='f892e562c4eaafeb49c9c0140a33178b0cbd0ef972702473f6d075b30015ffe0'
assert desc(o/'reviewer.topology.lease.json')['raw_sha256']=='7c62ba657e91de6b1200227521405d31fd1ee907ee7928afdcd97dc365ac60d1'
for x in oldrun['inputs']+oldrun['outputs']+newrun['inputs']+newrun['outputs']:
    d=desc(x['path'])
    for k in ['raw_bytes','lf_bytes','raw_sha256','lf_sha256']:
        if k in x:assert x[k]==d[k],(x['path'],k)
assert desc(q/'source-proof-graph.json')['raw_sha256']=='18805b8c95f5c2b2683a42cd696cfbbece29d5059d047abd8cf9563cccc2572f'
assert desc(q/'overlay-operations.json')['raw_sha256']=='91956ef46a3fae39a54c510e2f53b1df7d52f27baacabd3d553f35feac231f52'
assert desc(q/'run.json')['raw_sha256']=='6300ece8a29f2444b4795620683e06c326939a7a84ee2f4c678b1f28bd13e44f'
assert logical(newrun,'run_sha256')==newrun['run_sha256']=='13135532f19983fe2e4f56b16e07467a17fd92243035eb945f4dc1ca97fafa0c'
assert desc(q/'lease.json')['raw_sha256']=='492fed613ee991859eab1408766246561713d2922efb0031c18128526311a743'
assert all(J(q,'lease.json')[k]=='CLOSED' for k in ['read','write','python'])
a=J(p,'source-proof-graph.json');b=J(q,'source-proof-graph.json')
assert {k:v for k,v in a.items() if k!='edges'}=={k:v for k,v in b.items() if k!='edges'}
assert len(b['edges'])==256
for i,e in enumerate(a['edges']):
    z=dict(b['edges'][i])
    if i in [11,12]:assert z.pop('caller_index0')=={11:202,12:200}[i]
    assert e==z
assert [(e['ingredient'],e['consumer'],e['caller_index0']) for e in b['edges'][254:]]==[('D53.NeZero','P53.volNe0',201),('D53.Set','P53.volNe0',203)]
for f,n,changed in [('selected-providers.json',69,[65]),('source-coverage.json',260,[204]),('caller-inventory.json',204,[]),('lexical-inventory.json',635,[])]:
    x=J(p,f);y=J(q,f);assert len(y)==n
    assert [i for i,z in enumerate(x) if z!=y[i]]==changed
for f in ['source-contract.json','hypothesis-contract.json','primary-formula-inventory.json','parent-status.json','prospective-statement.raw','prospective-statement.lf']:
    assert (p/f).read_bytes()==(q/f).read_bytes()
assert (q/'open-positive-nezero-instance.raw').read_bytes()==b'instance (priority := 100) [Nonempty X] : NeZero \xce\xbc '
assert (q/'open-positive-nezero-context.raw').read_bytes()==b'variable [IsOpenPosMeasure \xce\xbc] {s U F : Set X} {x : X}\r\n'
pr=next(x for x in J(q,'selected-providers.json') if x['id']=='open-positive-nezero-instance')
src=Path(pr['path']).read_bytes();lines=src.splitlines(keepends=True)
assert src[pr['start_utf8_byte0']:pr['end_utf8_byte0_exclusive']]==(q/'open-positive-nezero-instance.raw').read_bytes()
assert lines[49].decode().rstrip()=='instance (priority := 100) [Nonempty X] : NeZero μ :='
assert b'variable [IsOpenPosMeasure \xce\xbc]' in lines[41]
checks=J(o,'reviewer.topology.repaired.byte-checks.json');assert not checks['errors'] and checks['coverage_partition_equal']
opening=(o/'reviewer.topology.repaired.lease.json').read_bytes()
snap=o/'reviewer.topology.repaired.raw-snapshots';snap.mkdir(exist_ok=True)
snapshots=[]
for f in ['capsule.md','source-proof-graph.json','overlay-operations.json','overlay-contract.json','selected-providers.json','source-coverage.json','caller-inventory.json','lexical-inventory.json','primary-formula-inventory.json','run.json','lease.json','open-positive-nezero-instance.raw','open-positive-nezero-context.raw']:
    dest=snap/f;assert not dest.exists();dest.write_bytes((q/f).read_bytes());snapshots.append(dict(original=desc(q/f),snapshot=desc(dest)))
(snap/'reviewer.topology.repaired.opening.lease.raw.snapshot.json').write_bytes(opening)
paths=[]
for x in oldrun['inputs']+oldrun['outputs']+newrun['inputs']+newrun['outputs']+J(q,'selected-providers.json'):
    if str(Path(x['path'])) not in paths:paths.append(str(Path(x['path'])))
for path in [p/'run.json',p/'lease.json',q/'run.json',q/'lease.json',o/'source-topology-review.json',o/'reviewer.topology.lease.json',o/'reviewer.topology.repaired.byte-checks.json']:
    if str(path) not in paths:paths.append(str(path))
inputs=[desc(x) for x in paths]
dump(o/'reviewer.topology.repaired.input-bindings.json',inputs)
dump(o/'reviewer.topology.repaired.snapshot-bindings.json',snapshots)
recipe='SHA256 UTF8 JSON of entire object excluding named self-hash field; ensure_ascii=False,sort_keys=True,separators=(comma,colon),allow_nan=False,no terminal newline.'
review=dict(schema='native-independent-source-topology-review53-repair/v1',reviewer='phase_source_reviewer_20261005',status='ACCEPTED_SCOPED_SOURCE_ONLY',verdict='accepted-scoped',blocking=False,scope='Distinct T53-1 representation repair and renewed source-only topology admission; no implementation/theorem/proof admission',graph=desc(q/'source-proof-graph.json'),repair_operations=desc(q/'overlay-operations.json'),original_negative=desc(o/'source-topology-review.json'),original_closed_reviewer_lease=desc(o/'reviewer.topology.lease.json'),creator_actual_closed_lease=desc(q/'lease.json'),creator_run=desc(q/'run.json'),creator_run_sha256=newrun['run_sha256'],counts=checks,exact_delta=dict(nodes_unchanged=79,original_edges=254,successor_edges=256,existing_edges_changed_only_by_caller_index0={'E53.11':202,'E53.12':200},appended_edges=['D53.NeZero -> P53.volNe0 caller201','D53.Set -> P53.volNe0 caller203'],provider65='Full OpenPos50 instance header before final declaration-level :=, proof not expanded',provider68='Actual inherited OpenPos42 variable context',coverage_original_rows=259,coverage_changed_index0=204,coverage_successor_rows=260,original_callers_exact_prefix=200,new_callers=4,original_lexemes_exact_prefix=621,new_lexemes=14,original_primary_formulae_byte_identical=34),resolved_blockers=['T53-1'],blockers=[],source_excess=[],mathematical_deltas=[],statement_deltas=[],review_evidence='Independently validated the exact operation diff and complete pinned OpenPos50 instance header, inherited OpenPos42 context, Nonempty/NeZero/Set caller spans and their directed ingredient edges. All79 nodes and non-edge graph fields, original254 edges except two caller-index attachments, old200 callers/621 lexemes, source contracts/formulae/exact758/three opaque parent pins remain unchanged. All old and new raw/LF pins rechecked; successor69 provider fragments,260 row partition,204 caller spans/635 lexemes and native creator run hash match. Original negative remains immutable. This accepts source-only topology after the representation repair and supplies no53 mathematical proof credit.',semantic_slots=old['semantic_slots'],semantic_slot_reuse='Original independent primary/signature/full bounded coverage conclusions reused only after strict unchanged-byte checks; the domains slot truncation blocker is resolved by actual selected public header and context.',normalization_boundary=old['normalization_and_boundaries_checked'],typing_precision='[Nonempty X] is an inherited typeclass input of this Mathlib instance; vector zero produces Nonempty E internally. [IsOpenPosMeasure μ] comes from inherited variable42; canonical volume Haar gives open positivity. NeZero μ is this instance output. None becomes a new public target premise.',remaining_boundary=['No53 claim/body/Test/decoder or compiler inspected or admitted','Every-y actual reflected law/mean remains a prospective mathematical obligation','Full rough L2→H1/B13, Γ, halfturn, main/cost/composition remain open','Opaque verified parents and external-unexpanded primitives remain opaque'],independence=dict(distinct_from_creator=True,creator='gaussian_noncompact_preread_42',distinct_from_future_formalizer=True,future_formalizer='root',self_validation=False,exposure='Own53 primary and prospective statement/topology stages plus historical52 source/body exposure disclosed. This phase sees only the representation successor; no historical blind claim and no future53 implementation/Test/decoder/math verdict.',compiler_invocations=0),input_artifacts=inputs,snapshot_bindings=desc(o/'reviewer.topology.repaired.snapshot-bindings.json'),own_primary_contract=old['own_primary_contract'],own_statement_review=old['own_prior_statement_review'],hash_recipe=recipe,completed_utc=now())
review['semantic_slots']['domains']='Finite real Hilbert/Borel including rank0 and signed compact C1 explicitly disclosed extensions. Actual volume NeZero is internally derived; complete anonymous instance header and inherited premise now selected correctly.'
review['review_run_sha256']=logical(review,'review_run_sha256');dump(o/'source-topology-review.repaired.json',review)
run=dict(schema='native-topology53-distinct-repair-review-run/v1',reviewer=review['reviewer'],result='ACCEPTED_SCOPED_SOURCE_ONLY',input_artifacts=inputs,outputs=[desc(o/'source-topology-review.repaired.json'),desc(o/'reviewer.topology.repaired.input-bindings.json'),desc(o/'reviewer.topology.repaired.snapshot-bindings.json'),desc(o/'reviewer.topology.repaired.byte-checks.json'),desc(o/'reviewer.topology.repaired.check.py'),desc(o/'reviewer.topology.repaired.seal.py')],review_run_sha256=review['review_run_sha256'],hash_recipe=recipe,compiler_invocations=0,completed_utc=now())
run['run_sha256']=logical(run,'run_sha256');dump(o/'reviewer.topology.repaired.run.json',run)
lease=json.loads(opening);lease.update(read='CLOSED',write='CLOSED',Python='CLOSED',compiler='NOT_STARTED_CLOSED',status='CLOSED',closed_utc=now(),review=desc(o/'source-topology-review.repaired.json'),run=desc(o/'reviewer.topology.repaired.run.json'),review_run_sha256=review['review_run_sha256'],run_sha256=run['run_sha256'],opening_lease_snapshot=desc(snap/'reviewer.topology.repaired.opening.lease.raw.snapshot.json'),closure_operation='Actual last filesystem write after final input/output sealing; no compiler/canonical/implementation mutation.')
lease['lease_run_sha256']=logical(lease,'lease_run_sha256');lease_bytes=(json.dumps(lease,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
report=dict(verdict=review['verdict'],blocking=False,review_raw_sha256=sha((o/'source-topology-review.repaired.json').read_bytes()),review_run_sha256=review['review_run_sha256'],run_raw_sha256=sha((o/'reviewer.topology.repaired.run.json').read_bytes()),run_sha256=run['run_sha256'],lease_raw_sha256=sha(lease_bytes),lease_run_sha256=lease['lease_run_sha256'],all_roles='CLOSED/compiler NOT_STARTED_CLOSED')
(o/'reviewer.topology.repaired.lease.json').write_bytes(lease_bytes)
print(json.dumps(report,ensure_ascii=False))
