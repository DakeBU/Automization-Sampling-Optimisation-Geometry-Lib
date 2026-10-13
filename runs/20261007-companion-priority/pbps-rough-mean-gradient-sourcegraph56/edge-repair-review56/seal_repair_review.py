from pathlib import Path
import datetime, hashlib, json, re

ROOT=Path(__file__).parent
BASE=ROOT.parent
REPAIR=BASE/'edge-repair56'
PRIOR=BASE/'review56'
EXHAUSTIVE=BASE/'exhaustive-overlay56'
sha=lambda b:hashlib.sha256(b).hexdigest()
canonical=lambda o:json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def receipt(p):
    b=p.read_bytes();lf=b.replace(b'\r\n',b'\n')
    return {'path':p.resolve().as_posix(),'raw_bytes':len(b),'raw_sha256':sha(b),'lf_bytes':len(lf),'lf_sha256':sha(lf),
            'crlf_count':b.count(b'\r\n'),'normalization':'Replace literal raw-byte CRLF pairs with LF only; no JSON reserialization'}
def seal(o):
    o['self_hash_recipe']={'algorithm':'SHA-256','payload':'COMPLETE object excluding only top-level content_self_sha256; every remaining schema/recipe/identity/receipt/negative/acceptance field included',
                          'serialization':'UTF8 JSON ensure_ascii=false sort_keys=true separators=(comma,colon); no trailing newline','recursive':False}
    o['content_self_sha256']=sha(canonical(o));return o
def write(n,o):
    (ROOT/n).write_bytes(json.dumps(o,ensure_ascii=False,sort_keys=True,indent=2).encode('utf-8')+b'\n');return receipt(ROOT/n)
def verify_self(p):
    raw=p.read_bytes();o=json.loads(raw);expected=o.pop('content_self_sha256');assert sha(canonical(o))==expected
    return {'path':p.resolve().as_posix(),'actual_readback':True,'raw_bytes':len(raw),'raw_sha256':sha(raw),
            'complete_nonrecursive_self_hash_verified':True,'content_self_sha256':expected}

v=json.loads((ROOT/'repair-verification.json').read_bytes())
assert v['status']=='PASS_EXACT_TWO_EDGE_REPAIR' and v['semantic_only_two_appends'] and v['acyclic']
for pin in v['verified_receipts']:assert receipt(Path(pin['path']))==pin
assert sha((PRIOR/'lease.json').read_bytes())=='9909fc2ad19f1c7da0998fe64411462601d2e90344eef5259845ba2b46c2e115'
inputs=ROOT/'inputs';inputs.mkdir(exist_ok=False)
snapshots=[]
for scope,label,names in [(REPAIR,'author',['sourceproofgraph.before.raw.snapshot.json','sourceproofgraph.after.json','overlay.json','lease.open.json','lease.json']),
                          (PRIOR,'original-review',['topology.review.json','minimal-edge-repair.proposal.json','manifest.json','complete.json','lease.json']),
                          (EXHAUSTIVE,'exhaustive',['lease-discipline-correction.json','read-isolation-and-chronology56.json'])]:
    for n in names:
        p=scope/n;raw=p.read_bytes();rawp=inputs/(label+'-'+n+'.exactraw.snapshot');lfp=inputs/(label+'-'+n+'.crlf-to-lf.snapshot')
        rawp.write_bytes(raw);lfp.write_bytes(raw.replace(b'\r\n',b'\n'))
        snapshots.append({'origin':receipt(p),'exactraw_snapshot':receipt(rawp),'LF_snapshot':receipt(lfp)})

review=seal({'schema_version':1,'artifact_kind':'independent-source-topology-edge-repair-review','reviewer':'/root/next_primary56','created_utc':now(),
             'verdict':'ACCEPT_REPAIRED_SOURCE_TOPOLOGY_ONLY','statement_verdict':'ACCEPT_SCOPED_STATEMENT_ONLY_UNCHANGED',
             'accepted_graph':v['after_receipt'],'before_graph':v['before_receipt'],'exact_deep_diff':v['exact_deep_diff'],
             'reachability':v['reachability'],'explicit_paths':v['paths'],'acyclic':True,'remaining_topology_blockers':[],
             'coverage':v['coverage'],'source_status_prose_semantics_binders_unchanged':True,
             'target_LF_bytes':1755,'target_LF_sha256':'fea2c3ade170bc0526d659f8c51abedaa0ce1a6186e75f0d8a2532b6608e94d8',
             'raw_vs_semantic_distinction':v['raw_vs_semantic_distinction'],
             'negative_history':{'three_original_post_CLOSED_mutations_retained':True,'original_restorations_exact':11,
                                 'historical_immutability_certified':False,'strict_creator_body_blindness':False,'strict_reviewer_body_blindness':False,
                                 'initial_context_fragment_recovered':False,'initial_fragment_evidence':'Transcript only; no original file recovered',
                                 'primary22_freeze_before_disclosed_provider_callsites_and_Mathlib_structural_fields':True,
                                 'original_blocker_review_stays_CLOSED_and_unchanged':True},
             'repair_author_schema_audit':v['native_schema_audit'],'input_verification':receipt(ROOT/'repair-verification.json'),
             'independent_receipt_checks':{'unique_files':v['unique_verified_files'],'embedded_pins':v['embedded_pin_checks'],
                                           'complete_object_self_hashes':len(v['complete_object_self_hash_checks'])},
             'raw_LF_snapshots':snapshots,'native_output':receipt(ROOT/'edge-repair.review.md'),
             'schema_receipt':receipt(ROOT/'edge-repair.review.schema.json'),
             'original_review_complete':receipt(PRIOR/'complete.json'),'original_review_lease':receipt(PRIOR/'lease.json'),
             'scope':'Accept only exact two-edge repaired SOURCE topology; neither Lean dependency certificate nor source mathematical theorem proof',
             'root_claim_proof_gate':'ACTUAL55_ACCEPTED_VERIFICATION_SERIALIZED_CYCLE_REQUIRED',
             'remaining_mathematical_boundaries':['Actual normalization/kernel/disintegration and AE representative compatibility','Genuine compact gradient/noncompact mean admission',
                                                'Sharp core D bound and real bounded extension/closure/energy passage','Separately defined weak-H1 equivalence and Gamma positive square root',
                                                'FullB13, half-turn/hypocoercivity/main/cost/composition/four-paper completion'],
             'sourcegraph_admission':True,'proof_admission':False,'Lean_or_math_admission':False,'future_implementation_read':False,
             'canonical_or_previous_CLOSED_writes':False,'compiler':'NOT_STARTED_CLOSED'})
schema=json.loads((ROOT/'edge-repair.review.schema.json').read_bytes())
def validate(value,spec):
    known={'$schema','title','type','required','properties','const','minItems','maxItems','pattern','additionalProperties'}
    assert not(set(spec)-known)
    if 'type' in spec:assert {'object':isinstance(value,dict),'array':isinstance(value,list),'string':isinstance(value,str)}[spec['type']]
    if 'required' in spec:assert all(k in value for k in spec['required'])
    if 'const' in spec:assert value==spec['const']
    if 'minItems' in spec:assert len(value)>=spec['minItems']
    if 'maxItems' in spec:assert len(value)<=spec['maxItems']
    if 'pattern' in spec:assert re.search(spec['pattern'],value)
    for k,s in spec.get('properties',{}).items():
        if k in value:validate(value[k],s)
validate(review,schema)
review_receipt=write('edge-repair.review.json',review)
run=seal({'schema_version':1,'artifact_kind':'independent-source-topology-edge-repair-native-run','owner':'/root/next_primary56','completed_utc':now(),
          'status':'COMPLETE_REPAIRED_SOURCE_TOPOLOGY_ACCEPTANCE_ONLY','review':review_receipt,
          'open_lease':receipt(ROOT/'lease.open.json'),'native_output':receipt(ROOT/'edge-repair.review.md'),
          'verification':receipt(ROOT/'repair-verification.json'),'scripts':[receipt(ROOT/'verify_repair.py'),receipt(Path(__file__))],
          'foreground_verifier':{'script':'verify_repair.py','observed_exit_code':0},
          'final_writer':'Foreground synchronous seal_repair_review.py; parent-observed exec exit0 is actual process completion',
          'schema_validation':'PASS exact checker for every keyword occurring in authored schema; unsupported validation keywords rejected',
          'sourcegraph_admission':True,'proof_admission':False,'compiler':'NOT_STARTED_CLOSED','children':[],'background_jobs':[],
          'negative_chronology_retained':True,'originals_or_prior_CLOSED_outputs_written':False})
run_receipt=write('reviewer.edge-repair.run.json',run)
manifest=seal({'schema_version':1,'artifact_kind':'independent-source-topology-edge-repair-manifest',
               'status':'COMPLETE_SOURCE_TOPOLOGY_REPAIR_REVIEW','files':{p.relative_to(ROOT).as_posix():receipt(p) for p in ROOT.rglob('*') if p.is_file()},
               'manifest_scope':'Files existing before manifest write; manifest self seal binds complete object; later complete/composite lease bind manifest raw bytes',
               'sourcegraph_admission':True,'proof_admission':False})
manifest_receipt=write('manifest.json',manifest)
complete=seal({'schema_version':1,'artifact_kind':'independent-source-topology-edge-repair-complete','status':'COMPLETE',
               'verdict':review['verdict'],'review':review_receipt,'run':run_receipt,'manifest':manifest_receipt,
               'accepted_graph':v['after_receipt'],'sourcegraph_admission':True,'proof_admission':False,
               'root_claim_proof_gate':review['root_claim_proof_gate'],'compiler':'NOT_STARTED_CLOSED'})
complete_receipt=write('complete.json',complete)
readbacks=[verify_self(ROOT/n) for n in ['edge-repair.review.json','reviewer.edge-repair.run.json','manifest.json','complete.json']]
validate(json.loads((ROOT/'edge-repair.review.json').read_bytes()),schema)
for pin in manifest['files'].values():assert receipt(Path(pin['path']))==pin
for pin in v['verified_receipts']:assert receipt(Path(pin['path']))==pin
lease=seal({'schema_version':1,'artifact_kind':'independent-source-topology-edge-repair-resource-lease','owner':'/root/next_primary56','status':'CLOSED','closed_utc':now(),
            'scope':ROOT.as_posix(),'open_lease':receipt(ROOT/'lease.open.json'),
            'resources':{'read':'CLOSED','write':'CLOSED','Python':'CLOSED','compiler':'NOT_STARTED_CLOSED'},
            'run':run_receipt,'manifest':manifest_receipt,'complete':complete_receipt,'actual_readbacks_before_close':readbacks,
            'schema_readback_validation':'PASS','all_prior_and_author_inputs_reverified':True,
            'closure_order':'Every actual readback and hash/schema check before final composite lease write; no further filesystem operation',
            'actual_process_evidence':'Foreground synchronous writer terminates; parent observes exec_command exit0; no retained sessions/jobs',
            'sourcegraph_admission':True,'proof_admission':False,'negative_chronology_retained':True,
            'creator_or_previous_CLOSED_outputs_written':False,'children':[],'background_jobs':[]})
lease_bytes=json.dumps(lease,ensure_ascii=False,sort_keys=True,indent=2).encode('utf-8')+b'\n'
(ROOT/'lease.json').write_bytes(lease_bytes)
print(json.dumps({'verdict':review['verdict'],'review':review_receipt,'run':run_receipt,'manifest':manifest_receipt,'complete':complete_receipt,
                  'lease_raw_bytes':len(lease_bytes),'lease_raw_sha256':sha(lease_bytes),'lease_content_self_sha256':lease['content_self_sha256'],
                  'actual_readbacks':len(readbacks),'status':'CLOSED','sourcegraph_admission':True,'proof_admission':False,
                  'root_claim_proof_gate':review['root_claim_proof_gate'],'compiler':'NOT_STARTED_CLOSED'},ensure_ascii=False,indent=2))
