from pathlib import Path
import datetime, hashlib, json, re

ROOT = Path(__file__).parent
BASE = ROOT.parent
OVERLAY = BASE / 'exhaustive-overlay56'
REPO = BASE.parents[2]
sha = lambda b: hashlib.sha256(b).hexdigest()
canonical = lambda o: json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
now = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()

def receipt(p):
    b=p.read_bytes();lf=b.replace(b'\r\n',b'\n')
    return {'path':p.resolve().as_posix(),'raw_bytes':len(b),'raw_sha256':sha(b),
            'lf_bytes':len(lf),'lf_sha256':sha(lf),'crlf_count':b.count(b'\r\n'),
            'normalization':'literal raw-byte CRLF->LF only; no JSON reserialization'}

def seal(o):
    o['self_hash_recipe']={'algorithm':'SHA-256','payload':'Complete object excluding ONLY top-level content_self_sha256; includes recipe/schema/metadata/receipts/negative findings',
                          'serialization':'UTF8 JSON ensure_ascii=false sort_keys=true separators=(comma,colon), no newline','recursive':False}
    o['content_self_sha256']=sha(canonical(o));return o

def write(n,o):
    (ROOT/n).write_bytes(json.dumps(o,ensure_ascii=False,sort_keys=True,indent=2).encode('utf-8')+b'\n')
    return receipt(ROOT/n)

def verify_self(p):
    raw=p.read_bytes();o=json.loads(raw);expected=o.pop('content_self_sha256');actual=sha(canonical(o));assert actual==expected
    return {'path':p.resolve().as_posix(),'actual_readback':True,'raw_bytes':len(raw),'raw_sha256':sha(raw),
            'content_self_sha256':expected,'complete_nonrecursive_self_hash_verified':True}

v=json.loads((ROOT/'input-verification.json').read_bytes())
assert v['coverage']=={'inventory':92,'covered':49,'excluded':43,'C1_independent_atomic_regions':63,'target_slots':29,'parent_slots':87,'source_nodes':29,'step_refinements':7}
for pin in v['verified_receipts']:assert receipt(Path(pin['path']))==pin
assert len(v['self_digest_checks'])==16

physical_checks=[]
for d in json.loads((BASE/'provider-contract-snapshots.json').read_bytes()):
    p=Path(d['physical_path']);raw=p.read_bytes();segment=b''.join(raw.splitlines(keepends=True)[d['line_start']-1:d['line_end']])
    header=(BASE/(d['declaration']+'.raw.contract.lean')).read_bytes()
    assert segment.split(b':= by',1)[0].rstrip()==header
    physical_checks.append({'declaration':d['declaration'],'physical_path':p.as_posix(),
                           'line_start':d['line_start'],'line_end':d['line_end'],
                           'recipe':'Exact raw source lines, stop before first actual proof delimiter := by, strip only trailing whitespace',
                           'header_receipt':receipt(BASE/(d['declaration']+'.raw.contract.lean')),'verified':True})
parent=json.loads((OVERLAY/'exhaustive-parent-contract-coverage56.json').read_bytes())
line_checks=0
for row in parent['rows']:
    for p in row['physical_header_rows']:
        actual=Path(p['physical_path']).read_text(encoding='utf-8').splitlines()[p['line_start']-1]
        assert actual==p['literal_header_line'];line_checks+=1
assert line_checks==91
physical_receipt=write('physical-header-verification.json',{'schema_version':1,'status':'PASS','header_checks':physical_checks,'exact_literal_header_line_checks':line_checks,'project_proof_bodies_semantically_inspected':False})

inputs=ROOT/'inputs';inputs.mkdir(exist_ok=False)
snapshots=[]
selected_base=['sourceproofgraph56.json','source-first-proof-graph.json','primary-before-signature.freeze.json',
               'primary-source-anchor-inventory.json','provider-contract-snapshots.json','provider-physical-context-receipts56.json',
               'manifest.json','complete.json','run.json','lease.json','read-isolation-and-chronology56.json',
               'prospective-statement.target.raw.snapshot.txt','primary-pbps.raw.snapshot.html']
selected_overlay=['sourceproofgraph56.json','exhaustive-parent-contract-coverage56.json','target-binder-semantic-expansion56.json',
                  'opaque-provider-semantic-expansion56.json','lease-discipline-correction.json','read-isolation-and-chronology56.json',
                  'manifest.json','complete.json','run.json','lease.open.json','lease.json']
for label,scope,names in [('base',BASE,selected_base),('overlay',OVERLAY,selected_overlay)]:
    for name in names:
        origin=scope/name;raw=origin.read_bytes();lf=raw.replace(b'\r\n',b'\n')
        rawpath=inputs/(label+'-'+name+'.exactraw.snapshot');lfpath=inputs/(label+'-'+name+'.crlf-to-lf.snapshot')
        rawpath.write_bytes(raw);lfpath.write_bytes(lf)
        snapshots.append({'origin':receipt(origin),'exactraw_snapshot':receipt(rawpath),'lf_snapshot':receipt(lfpath),
                          'recipe':'Exact raw bytes copied; LF partner replaces only literal CRLF pairs'})
statement=(BASE/'prospective-statement.target.lf.snapshot.txt').read_bytes()
assert len(statement)==1755 and sha(statement)=='fea2c3ade170bc0526d659f8c51abedaa0ce1a6186e75f0d8a2532b6608e94d8'
graph=json.loads((OVERLAY/'sourceproofgraph56.json').read_bytes())
routes={x['id']:list(x['required_inputs']) for x in graph['unnamed_source_step_refinement']}
edges={x['child']:x['parents'] for x in graph['source_edges']};edges.update(routes)
def reachable(start,mapping):
    pending=list(mapping.get(start,[]));seen=set()
    while pending:
        x=pending.pop()
        if x in seen:continue
        seen.add(x);pending+=mapping.get(x,[])
    return sorted(seen)
deltas=[{'consumer':'route56:core-linear-bound','field':'required_inputs','append':'route56:core-gradient',
         'source_use_site':'A3.SS1.p1.1 / A3.EGx25','issue':'Core D construction needs actual mean gradient/core agreement, not bare graph algebra'},
        {'consumer':'route56:bounded-extension','field':'required_inputs','append':'route56:core-linear-bound',
         'source_use_site':'A3.SS1.p1.1','issue':'Bounded extension consumes actual core-linear D and its norm bound'}]
proposed={k:list(vals) for k,vals in edges.items()}
for d in deltas:
    assert d['append'] not in proposed[d['consumer']];proposed[d['consumer']].append(d['append'])
assert 'route56:core-gradient' in reachable('route56:closed-graph',proposed)
assert 'route56:core-linear-bound' in reachable('route56:bounded-extension',proposed)
repair=seal({'schema_version':1,'artifact_kind':'reviewer-minimal-topology-edge-repair-proposal','status':'RECOMMENDATION_ONLY_NOT_APPLIED_NOT_ACCEPTED',
             'exact_input_graph':receipt(OVERLAY/'sourceproofgraph56.json'),'changes':deltas,
             'permitted_mutation':'ONLY two required_inputs appends in a DISTINCT author repair overlay',
             'no_statement_node_formula_scope_status_mutation':True,'proof_admission':False,
             'before_reachability':v['reachability'],
             'proposed_reachability':{n:reachable(n,proposed) for n in v['reachability']},
             'fresh_independent_review_required':True})
repair_receipt=write('minimal-edge-repair.proposal.json',repair)

previous_receipts=[]
for p,expected in [(REPO/'runs/20261007-companion-priority/phase-pbps-primary-preread56/lease.json','d1e3545eaf1028260a57c79a66e75b0c98557459b0fd116cae89c0796a8d7135'),
                   (REPO/'runs/20261007-companion-priority/pbps-rough-mean-gradient-preproof-review56/lease.json','c2770e3482065b6fa05312de77063a470a8dc6da2979e7d6c7e7a63e6659ae29')]:
    assert sha(p.read_bytes())==expected;assert json.loads(p.read_bytes())['status']=='CLOSED';previous_receipts.append(receipt(p))
negative={'correction_verdict':'ACCEPT_TRUTHFUL_RESTORATION_CORRECTION_WITH_NEGATIVE_RETAINED',
          'historically_modified_after_CLOSED':['sourceproofgraph56.json','creator-complete56.json','read-isolation-and-chronology56.json'],
          'restored_originals_verified_exact':11,'original_historically_unmodified':False,
          'distinct_overlay_OPEN_to_CLOSED_verified':True,
          'strict_creator_provider_body_blindness':False,'strict_reviewer_provider_body_blindness':False,
          'exposed_callsite_locations':['L2MacroscopicMean.lean:62','SourceMeanGradientDomain.lean:66'],
          'exposed_mathlib_structural_fields':['zero_mem','add_mem'],
          'source_only_22_node_freeze_precedes_exposure':True,
          'earliest_overwritten_context_recovered':False,'earliest_context_evidence':'Transcript only, not claimed independently recovered as file',
          'historical_evidence_origin':'Creator correction record and explicit parent observations; present exact restorations independently byte-verified',
          'candidate56_implementation_inspected':False,'canonical_mutation':False}
review=seal({'schema_version':1,'artifact_kind':'independent-source-topology-review','reviewer':'/root/next_primary56','created_utc':now(),
             'verdict':'SOURCE_TOPOLOGY_BLOCKED_MISSING_INPUT_EDGES','statement_verdict':'ACCEPT_SCOPED_STATEMENT_ONLY_UNCHANGED',
             'schema_receipt':receipt(ROOT/'topology.review.schema.json'),
             'target_LF_bytes':len(statement),'target_LF_sha256':sha(statement),
             'coverage':v['coverage'],'coverage_verdict':'SOURCE_COVERAGE_AND_SCOPED_EXCLUSIONS_ACCEPTABLE; NOT_DEPENDENCY_ADMISSION',
             'binder_parent_semantics_verdict':'29 target slots and87 parent slots classified; no new public premises; providers opaque',
             'deep_residuals':['AE/carrier/completeness','actual normalization/kernel/disintegration','normalized compact differentiation/Poincare/covariance','bounded extension/core equality/closure passage'],
             'blockers':deltas,'graph_path_evidence':v['reachability'],'minimal_edge_repair':repair_receipt,
             'negative_chronology':negative,'input_verification':receipt(ROOT/'input-verification.json'),
             'physical_header_verification':physical_receipt,'input_snapshots':snapshots,
             'native_output':receipt(ROOT/'topology.review.md'),'previous_CLOSED_stages_preserved':previous_receipts,
             'original_native_schema_audit':'Actual schema_version1 objects, manifest maps and complete/run/composite/named lease shapes recorded in input-verification.json; no fabricated universal native JSON schema',
             'original_self_hash_audit':'16 creator complete-object canonical self digests verified; top-level self_digest excluded only. payload/named_payload byte labels differ, hashed complete remaining object does not.',
             'remaining_boundaries':['Exact two-edge topology repair and fresh independent admission','Preceding55 exact verification/serialized cycle',
                                     'All target56 mathematical proof and Lean verification','Separately defined weak-H1 equivalence; Gamma; fullB13',
                                     'Half-turn/hypocoercivity/main/cost/composition/four-paper completion'],
             'sourcegraph_admission':False,'proof_admission':False,'compiler':'NOT_STARTED_CLOSED',
             'source_topology_not_Lean_dependency_graph':True,'future_implementation_not_read':True})
schema=json.loads((ROOT/'topology.review.schema.json').read_bytes())
def validate(value,spec):
    known={'$schema','title','type','required','properties','const','minItems','maxItems','pattern','additionalProperties'}
    assert not(set(spec)-known)
    if 'type' in spec:assert {'object':isinstance(value,dict),'array':isinstance(value,list),'string':isinstance(value,str)}[spec['type']]
    if 'required' in spec:assert all(k in value for k in spec['required'])
    if 'const' in spec:assert value==spec['const']
    if 'minItems' in spec:assert len(value)>=spec['minItems']
    if 'maxItems' in spec:assert len(value)<=spec['maxItems']
    if 'pattern' in spec:assert re.search(spec['pattern'],value)
    for k,child in spec.get('properties',{}).items():
        if k in value:validate(value[k],child)
validate(review,schema)
review_receipt=write('topology.review.json',review)
run=seal({'schema_version':1,'artifact_kind':'independent-source-topology-native-run','reviewer':'/root/next_primary56','completed_utc':now(),
          'status':'COMPLETE_TYPED_TOPOLOGY_BLOCKER','review':review_receipt,'proposal':repair_receipt,
          'native_output':receipt(ROOT/'topology.review.md'),'input_verification':receipt(ROOT/'input-verification.json'),
          'physical_header_verification':physical_receipt,'open_lease':receipt(ROOT/'lease.open.json'),
          'foreground_operations':[{'script':'verify_inputs.py','observed_exit_code':0},
                                   {'script':'physical header direct check','observed_exit_code':0}],
          'final_writer':'Synchronous seal_topology_review.py; parent-observed tool exit0 supplies actual process termination',
          'schema_validation':'PASS exact checker evaluates every validation keyword in authored schema and rejects unsupported ones',
          'scripts':[receipt(ROOT/'verify_inputs.py'),receipt(Path(__file__))],
          'sourcegraph_admission':False,'proof_admission':False,'compiler':'NOT_STARTED_CLOSED',
          'negative_chronology_retained':True,'creator_or_previous_CLOSED_writes':False,'background_jobs':[],'children':[]})
run_receipt=write('reviewer.topology.run.json',run)
own_files=[p for p in ROOT.rglob('*') if p.is_file()]
manifest=seal({'schema_version':1,'artifact_kind':'independent-source-topology-review-manifest','status':'COMPLETE_WITH_TYPED_TOPOLOGY_BLOCKER',
               'files':{p.relative_to(ROOT).as_posix():receipt(p) for p in own_files},
               'creator_inputs_still_verified':{'unique_files':v['unique_verified_files'],'embedded_pin_checks':v['embedded_receipt_checks'],'self_digests':16},
               'scope':'Only new review56; all original creator and previous CLOSED reviewer files immutable in this review'})
manifest_receipt=write('manifest.json',manifest)
complete=seal({'schema_version':1,'artifact_kind':'independent-source-topology-review-complete','status':'COMPLETE_TYPED_TOPOLOGY_BLOCKER',
               'verdict':review['verdict'],'review':review_receipt,'run':run_receipt,'manifest':manifest_receipt,'repair_proposal':repair_receipt,
               'sourcegraph_admission':False,'proof_admission':False,'compiler':'NOT_STARTED_CLOSED','negative_chronology_retained':True})
complete_receipt=write('complete.json',complete)
readbacks=[verify_self(ROOT/n) for n in ['minimal-edge-repair.proposal.json','topology.review.json','reviewer.topology.run.json','manifest.json','complete.json']]
validate(json.loads((ROOT/'topology.review.json').read_bytes()),schema)
for pin in manifest['files'].values():assert receipt(Path(pin['path']))==pin
for pin in v['verified_receipts']:assert receipt(Path(pin['path']))==pin
for pin in previous_receipts:assert receipt(Path(pin['path']))==pin
lease=seal({'schema_version':1,'artifact_kind':'independent-source-topology-review-resource-lease','owner':'/root/next_primary56',
            'status':'CLOSED','closed_utc':now(),'scope':ROOT.as_posix(),'open_lease':receipt(ROOT/'lease.open.json'),
            'resources':{'read':'CLOSED','write':'CLOSED','Python':'CLOSED','compiler':'NOT_STARTED_CLOSED'},
            'run':run_receipt,'manifest':manifest_receipt,'complete':complete_receipt,'readback_before_close':readbacks,
            'all_input_and_prior_CLOSED_receipts_reverified':True,'schema_readback':'PASS',
            'closure_order':'All actual readbacks completed before final composite lease write; no filesystem operation after final lease',
            'actual_process_evidence':'Synchronous foreground writer returns exit0; parent observes tool exit. No persistent sessions or background jobs.',
            'sourcegraph_admission':False,'proof_admission':False,'negative_chronology_retained':True,
            'creator_originals_mutated':False,'prior_review_outputs_mutated':False,'background_jobs':[],'children':[]})
lease_bytes=json.dumps(lease,ensure_ascii=False,sort_keys=True,indent=2).encode('utf-8')+b'\n'
(ROOT/'lease.json').write_bytes(lease_bytes)
print(json.dumps({'verdict':review['verdict'],'review':review_receipt,'run':run_receipt,'manifest':manifest_receipt,'complete':complete_receipt,
                  'lease_raw_bytes':len(lease_bytes),'lease_raw_sha256':sha(lease_bytes),'lease_content_self_sha256':lease['content_self_sha256'],
                  'actual_readback_count':len(readbacks),'status':'CLOSED','compiler':'NOT_STARTED_CLOSED'},ensure_ascii=False,indent=2))
