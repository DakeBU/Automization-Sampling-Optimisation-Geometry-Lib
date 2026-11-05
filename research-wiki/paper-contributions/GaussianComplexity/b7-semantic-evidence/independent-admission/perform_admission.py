from pathlib import Path
from datetime import datetime, timezone
import copy, hashlib, json, shutil, subprocess, sys
sys.path.insert(0,str(Path.cwd()))
from tools import astis_advance

ROOT=Path.cwd()
EV=Path('research-wiki/paper-contributions/GaussianComplexity/b7-semantic-evidence')
OUT=EV/'independent-admission'
ADVANCE='ASTIS-SA-20261104-GaussianComplexitySingleBlockSeparation'
VERIFIER='/root/b7_fresh_source_module_review'
CANDIDATE='2418655bc07cbc8798aabc069e8677b95dd6093a'
REVIEW='3ee5691f85b2ad632a824c1dc70612b5600174ce'
HEAD='d925c0c3e16810c0023735b80279ed06ffe92ed6'
OFFICIAL='387ae4e589bb0521789b7a719c9c0d331cc4b92c'
DECL='AutoSamplingTheory.ExampleCases.GaussianComplexity.SingleBlockSeparation.single_block_separation'
CELL=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-single-block-separation.json')
AUDIT=Path('research-wiki/semantic-roundtrip/audits/huanjian-single-block-separation.json')
LEDGER=Path('runs/substantive_advances.jsonl')
DISCOVERIES=Path('runs/substantive_discoveries.jsonl')
sha_bytes=lambda b:hashlib.sha256(b).hexdigest()
sha=lambda p:sha_bytes(Path(p).read_bytes())
canonical_sha=lambda x:sha_bytes(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())
git=lambda *args:subprocess.check_output(['git',*args])
gitbytes=lambda commit,p:git('show',commit+':'+str(p))
load=lambda p:json.loads(Path(p).read_text())
dump=lambda p,x:Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
assert git('rev-parse','HEAD').decode().strip()==HEAD
assert git('status','--porcelain').decode().strip()=='?? .atlas-upstream/'
for older,newer in [(CANDIDATE,REVIEW),(REVIEW,HEAD)]:
    subprocess.check_call(['git','merge-base','--is-ancestor',older,newer])

review_names=set(git('diff','--name-only',CANDIDATE,REVIEW).decode().splitlines())
review_expected={str(EV/p) for p in [
 'authored-reader-review.json','fake-closure-scan.json','independent-raw-source-extract.txt',
 'independent-review-build/.gitattributes',
 'independent-review-build/20261105T060454273650Z-b7-independent-review-build.log',
 'independent-review-build/20261105T060454273650Z-b7-independent-review-build.receipt.json',
 'independent-review-manifest.json','latest-main-queue-observation-20261105.json','local-proof-seal-spine-candidate.json',
 'source-code-correspondence-check.json','source-review-audit-update.json','source-review-result.json',
 'source-review-run.json','source-review-validation.json','whole-module-review.json']}
review_expected.add(str(AUDIT))
assert review_names==review_expected, (review_names-review_expected,review_expected-review_names)
gate_names=set(git('diff','--name-only',REVIEW,HEAD).decode().splitlines())
gate_expected={str(EV/'reviewed-local-gates.json'),'research-wiki/paper-contributions/GaussianComplexity/b7-integration-notes.json'}
gate_stems=['20261105T061324835876Z-b7-contributor-reviewed','20261105T061324835878Z-b7-frontier-reviewed','20261105T061324835879Z-b7-publication-reviewed','20261105T061324835879Z-b7-semantic-reviewed']
gate_expected|={str(EV/(stem+ext)) for stem in gate_stems for ext in ['.log','.receipt.json']}
assert gate_names==gate_expected,(gate_names-gate_expected,gate_expected-gate_names)

manifest_path=EV/'independent-review-manifest.json'
assert sha(manifest_path)=='f136d69cecee863bc9bcdfa4af8023a7629fcb445a6f1d382616a532f98fb1c2'
manifest=load(manifest_path)
for path,expected in manifest['outputs'].items():
    assert sha(path)==expected, path
    assert Path(path).read_bytes()==gitbytes(HEAD,path),path
run=load(EV/'source-review-run.json')
result=load(EV/'source-review-result.json')
assert result['verdict']=='equivalent-after-elaboration' and not result['repairs']
assert not any(d['blocking'] for d in result['deltas'])
assert result['reviewer']==VERIFIER
assert sha(EV/'source-review-run.json')==result['review_run_sha256']
assert load(EV/'whole-module-review.json')['verdict']=='accepted'
assert load(EV/'authored-reader-review.json')['verdict']=='accepted-content-only'
assert load(EV/'fake-closure-scan.json')['accepted']

protected=[]
for item in run['reviewed_files']:
    path=item['path']
    assert sha(path)==item['sha256'],path
    record={'path':path,'sha256':sha(path),'matches_frozen_review':True}
    if not path.startswith('.lake/'):
        assert Path(path).read_bytes()==gitbytes(CANDIDATE,path)==gitbytes(REVIEW,path)==gitbytes(HEAD,path),path
        record['candidate_review_descendant_byte_identity']=True
    protected.append(record)
extra=['website/content/declaration_lessons/huanjian-single-block-separation.json','website/content/publications/huanjian-single-block-separation.json','lean-toolchain','lake-manifest.json',str(EV/'decoder-packet.json'),str(EV/'decoder-result.json'),str(EV/'source-reviewer-packet.json')]
for path in extra:
    assert Path(path).read_bytes()==gitbytes(CANDIDATE,path)==gitbytes(REVIEW,path)==gitbytes(HEAD,path),path
    protected.append({'path':path,'sha256':sha(path),'candidate_review_descendant_byte_identity':True})
assert sha(run['raw_source'])==run['raw_source_sha256']=='6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915'
packet=load(EV/'source-reviewer-packet.json')
assert sha('lean-toolchain')==packet['candidate_publication_context']['toolchain']
assert sha('lake-manifest.json')==packet['candidate_publication_context']['dependencies']
candidate_audit=json.loads(gitbytes(CANDIDATE,AUDIT))
head_audit=load(AUDIT)
allowed_audit={'state','semantic_slots','deltas','verdict','source_review'}
assert all(candidate_audit.get(k)==head_audit.get(k) for k in set(candidate_audit)|set(head_audit) if k not in allowed_audit)
assert head_audit['state']=='source-reviewed' and head_audit['source_review']['state']=='accepted'
assert head_audit['reconstruction']==candidate_audit['reconstruction']

raw_pairs=[]
focused=manifest['build']
for key in ['log','receipt']:
    p=Path(focused[key]); expected=focused[key+'_sha256']
    assert sha(p)==expected and p.read_bytes()==gitbytes(HEAD,p)
receipt=load(focused['receipt'])
assert receipt['command']==['lake','build','Tests.GaussianComplexitySingleBlockSeparation']
assert receipt['head_before']==receipt['head_after']==CANDIDATE and receipt['exit_code']==0
assert receipt['log_sha256']==sha(focused['log'])
raw_pairs.append({'kind':'focused-Lean-build','head':CANDIDATE,'receipt':focused['receipt'],'receipt_sha256':sha(focused['receipt']),'log':focused['log'],'log_sha256':sha(focused['log']),'exact_HEAD_blob_bytes':True})
gates=load(EV/'reviewed-local-gates.json')
for check in gates['checks']:
    rp=Path(check['receipt']['path']); lp=Path(check['log']['path'])
    assert sha(rp)==check['receipt']['sha256'] and rp.read_bytes()==gitbytes(HEAD,rp)
    assert sha(lp)==check['log']['sha256'] and lp.read_bytes()==gitbytes(HEAD,lp)
    r=load(rp)
    assert r['command']==check['command'] and r['head_before']==r['head_after']==REVIEW and r['exit_code']==0
    assert r['log_sha256']==sha(lp)
    assert check['head_before']==check['head_after']==REVIEW and check['exit_code']==0
    raw_pairs.append({'kind':r['command'][1],'head':REVIEW,'receipt':str(rp),'receipt_sha256':sha(rp),'log':str(lp),'log_sha256':sha(lp),'exact_HEAD_blob_bytes':True})

ledger_before=LEDGER.read_bytes()
assert ledger_before==gitbytes(HEAD,LEDGER)==gitbytes(REVIEW,LEDGER)==gitbytes(CANDIDATE,LEDGER)
assert ledger_before.endswith(b'\n')
before=astis_advance._replay_advances([json.loads(line) for line in ledger_before.splitlines() if line.strip()])
assert before[ADVANCE]['state']=='PROVED_LOCAL'
assert before[ADVANCE]['owner_id']=='huanjian_gc_20261104_b7' and before[ADVANCE]['owner_id']!=VERIFIER
assert before[ADVANCE]['publication_declarations']==[DECL]
discovery_before=DISCOVERIES.read_bytes()
official_ledger=gitbytes(OFFICIAL,LEDGER)
official_state=astis_advance._replay_advances([json.loads(line) for line in official_ledger.splitlines() if line.strip()])
foreign=official_state['ASTIS-SA-20261104-BoundedPerturbationLaw']
assert foreign['state']=='STABILIZING'
assert foreign['latest_evidence']['integration_owner']=='agent-task:/root'
official_foreign={'observed_official_commit':OFFICIAL,'advance_id':foreign['advance_id'],'state':foreign['state'],'integration_owner':foreign['latest_evidence']['integration_owner'],'mutated':False}
cell_before=load(CELL)
assert CELL.read_bytes()==gitbytes(HEAD,CELL) and cell_before['status']=='proved_locally'
assert cell_before['owner_id']=='huanjian_gc_20261104_b7'
assert cell_before['learning_contract']['reader_backpressure']['purification_status']=='pending'
assert cell_before['learning_contract']['reader_backpressure']['exposition_seal_status']=='pending'

OUT.mkdir(exist_ok=True)
(OUT/'.gitattributes').write_text('* -text -diff\n')
shutil.copyfile(__file__,OUT/'perform_admission.py')
boundary=('Independently verified local source Proposition B.7 Eq19 only: every natural n>=3 and real kappa>=4, including endpoints and both parities, actual twice-restricted full-Haar inverse-precision Gaussian bind mixtures, normalized event TV >= q^n/D >= (1/2) exp(-5n/s). No n=2 extension. Browser/desktop/mobile/adjacent-Lean/source-index/graph acceptance, root aggregate ASTIS/Tests/site build, Registry/imports/root integration, current-main stabilization/merge and postmerge purification/Exposition Seal remain pending. Product amplification, both main lower bounds, oracle/transcript, deterministic caps, TV precision, expected-cost/dimension adapters and hidden-eigenbasis are outside this admission; the whole Goal is not complete. Preserve foreign BoundedPerturbationLaw stabilization and other chats/PBPS/SPHMC state.')
evidence={
 'verifier_id':VERIFIER,'verified_commit':HEAD,'publication_declarations':[DECL],
 'gate':{'focused_Lean_build':focused,'focused_build_reused_from_commit':CANDIDATE,'protected_context_unchanged':True,
   'local_metadata_gates':{'path':str(EV/'reviewed-local-gates.json'),'sha256':sha(EV/'reviewed-local-gates.json'),'actual_run_commit':REVIEW,'evidence_commit':HEAD,'all_exit_codes':0},
   'scope':'Focused Lean plus publication/contributor/semantic/frontier gates. This is not a root aggregate or browser acceptance.'},
 'source_audit':{'result':str(EV/'source-review-result.json'),'result_sha256':sha(EV/'source-review-result.json'),'run':str(EV/'source-review-run.json'),'run_sha256':sha(EV/'source-review-run.json'),'verdict':'equivalent-after-elaboration','blocking_deltas':0,'repairs':[],
   'whole_module':str(EV/'whole-module-review.json'),'whole_module_sha256':sha(EV/'whole-module-review.json'),'authored_reader_content':str(EV/'authored-reader-review.json'),'authored_reader_content_sha256':sha(EV/'authored-reader-review.json')},
 'semantic_roundtrip_audit':{'path':str(AUDIT),'sha256':sha(AUDIT),'state':'source-reviewed','verdict':'equivalent-after-elaboration'},
 'fake_closure_scan':{'path':str(EV/'fake-closure-scan.json'),'sha256':sha(EV/'fake-closure-scan.json'),'hits':[],'compiled_axioms':['propext','Classical.choice','Quot.sound']},
 'immutable_descendant_check':{'candidate_commit':CANDIDATE,'review_evidence_commit':REVIEW,'verified_commit':HEAD,'permitted_diff_only':True,'unchanged_protected_context':True},
 'truth_boundary':boundary,'integration_notes':'research-wiki/paper-contributions/GaussianComplexity/b7-integration-notes.json'}

# This is the only lifecycle mutation: the independent verifier's normal API call.
astis_advance.transition_advance(ADVANCE,'VERIFIED',worker_id=VERIFIER,
 modes=['independent-source-review','immutable-descendant-admission'],evidence=evidence)

ledger_after=LEDGER.read_bytes()
assert ledger_after.startswith(ledger_before)
suffix=ledger_after[len(ledger_before):]
assert len(suffix.splitlines())==1 and suffix.endswith(b'\n')
event=json.loads(suffix)
assert event['advance_id']==ADVANCE and event['from_state']=='PROVED_LOCAL' and event['to_state']=='VERIFIED'
assert event['worker_id']==VERIFIER and event['evidence']['verifier_id']==VERIFIER
assert event['evidence']['verified_commit']==HEAD
after=astis_advance._replay_advances([json.loads(line) for line in ledger_after.splitlines() if line.strip()])
other_before={k:v for k,v in before.items() if k!=ADVANCE}
other_after={k:v for k,v in after.items() if k!=ADVANCE}
assert other_before==other_after
assert DISCOVERIES.read_bytes()==discovery_before
assert git('rev-parse','HEAD').decode().strip()==HEAD
event_path=OUT/'transition-event.jsonl'
event_path.write_bytes(suffix)

cell_after=copy.deepcopy(cell_before)
cell_after['status']='independently_verified'
cell_after['evidence']['independent_verification']=VERIFIER+' verified immutable descendant '+HEAD+' using frozen source/whole-module/authored-content review, protected-context equality, pinned focused build and real local metadata gates; see '+str(EV/'independent-verified-admission.json')+'. No browser/root aggregate/integration/purification acceptance.'
cell_after['evidence']['immutable_descendant_verification']={
 'verifier_id':VERIFIER,'verified_commit':HEAD,'reviewed_candidate_commit':CANDIDATE,
 'review_evidence_commit':REVIEW,'event_artifact':str(event_path),'event_sha256':sha(event_path),
 'source_review_result':str(EV/'source-review-result.json'),'whole_module_review':str(EV/'whole-module-review.json'),
 'authored_reader_content_review':str(EV/'authored-reader-review.json'),'fake_closure_scan':str(EV/'fake-closure-scan.json'),
 'gate_evidence':str(EV/'reviewed-local-gates.json'),'truth_boundary':boundary}
assert all(cell_after[k]==cell_before[k] for k in cell_before if k not in {'status','evidence'})
dump(CELL,cell_after)

admission={
 'schema_version':1,'kind':'independent-immutable-descendant-VERIFIED-admission','verifier_id':VERIFIER,
 'advance_id':ADVANCE,'verified_commit':HEAD,'candidate_commit':CANDIDATE,'review_evidence_commit':REVIEW,
 'recorded_utc':datetime.now(timezone.utc).isoformat(),'accepted':True,
 'ancestry':{'candidate_is_ancestor_of_review':True,'review_is_ancestor_of_verified':True},
 'descendant_changes':{'candidate_to_review':sorted(review_names),'review_to_verified':sorted(gate_names),'only_permitted_evidence_and_own_semantic_audit_changes':True},
 'frozen_manifest':{'path':str(manifest_path),'sha256':sha(manifest_path),'all_output_hashes_match':True,'all_output_bytes_match_Git_HEAD':True},
 'protected_inputs':protected,
 'raw_source':{'path':run['raw_source'],'sha256':sha(run['raw_source']),'matches_frozen_source':True,'tracked_in_repo':False},
 'audit_field_changes_limited_to':sorted(allowed_audit),'reconstruction_and_definition_context_unchanged':True,
 'raw_log_receipt_pairs':raw_pairs,
 'reused_build_reason':'All production code, test, meaning-carrying providers, pinned Mathlib source hashes, blind artifacts, source, authored prose, toolchain and manifest are identical to the independently compiled candidate. Descendants add review/gate evidence only; no identical Lean rebuild was run.',
 'ledger':{'path':str(LEDGER),'before_sha256':sha_bytes(ledger_before),'before_bytes':len(ledger_before),'after_sha256':sha_bytes(ledger_after),'after_bytes':len(ledger_after),
  'exact_prior_raw_prefix_unchanged':True,'appended_event_count':1,'appended_event_artifact':str(event_path),'appended_event_sha256':sha(event_path),
  'from_state':'PROVED_LOCAL','to_state':'VERIFIED','worker_id':VERIFIER,
  'all_other_advances_count':len(other_before),'all_other_replayed_records_unchanged':True,'other_records_before_sha256':canonical_sha(other_before),'other_records_after_sha256':canonical_sha(other_after),
  'discovery_ledger_unchanged':True,'discovery_ledger_sha256':sha_bytes(discovery_before)},
 'frontier':{'path':str(CELL),'before_sha256':sha_bytes(gitbytes(HEAD,CELL)),'after_sha256':sha(CELL),'status':'independently_verified','only_status_and_evidence_changed':True,'reader_backpressure_unchanged':True},
 'foreign_stabilization_preserved':official_foreign,
 'no_fake_closure_or_reader_boundary_upgrade':True,'truth_boundary':boundary,
 'normal_transition_API':'tools.astis_advance.transition_advance',
 'transition_evidence':evidence,
 'performing_script':{'path':str(OUT/'perform_admission.py'),'sha256':sha(OUT/'perform_admission.py')},
 'commit_or_merge_performed':False,'STABILIZING_transition_performed':False,
 'post_transition_working_tree_scope':'Only own SAU append event, own B7 frontier status/evidence and own admission evidence; pre-existing .atlas-upstream remains untouched.'}
admission_path=EV/'independent-verified-admission.json'
dump(admission_path,admission)
print(json.dumps({'accepted':True,'verified_commit':HEAD,'new_state':after[ADVANCE]['state'],
 'admission':str(admission_path),'admission_sha256':sha(admission_path),'raw_event':str(event_path),'raw_event_sha256':sha(event_path),
 'ledger_before_sha256':sha_bytes(ledger_before),'ledger_after_sha256':sha_bytes(ledger_after),
 'frontier_sha256':sha(CELL),'other_advances_preserved':len(other_before)},indent=2))
