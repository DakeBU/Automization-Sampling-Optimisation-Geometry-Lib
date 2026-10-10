from pathlib import Path
import copy,datetime,hashlib,json,os,re,subprocess,sys
R=Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-outer-bounded-l2-continuity84';O=Path(__file__).parent;C='5186f92607df617c4e4a8a90d0c5e6b5fc611090'
def info(p):
 p=Path(p);p=p if p.is_absolute() else R/p;b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),RAW_sha256=hashlib.sha256(b).hexdigest(),RAW_bytes=len(b))
def load(p):return json.loads(Path(p).read_bytes())
def save(n,d):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
def gitblob(p):return subprocess.check_output(['git','show',C+':'+Path(p).relative_to(R).as_posix()],cwd=R)
def norm(b):return b.replace(b'\r\n',b'\n')
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==C
cell=R/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-outer-bounded-l2-continuity.json';cur=load(cell);remote=json.loads(gitblob(cell));ad=load(B/'exact-commit-verification84/admission84.json');snap=B/'integration84/cell.before-final-admin84.snapshot.json'
assert info(cell)['RAW_sha256']=='d2fefdde6795303e706cfe687e2806dcc39304558a1ff6bf1f0cba0d49d0d493'==load(B/'integration84/final-admin.json')['cell_RAW_sha256']
assert remote['status']=='proved_locally' and cur['status']=='independently_verified' and info(snap)['RAW_sha256']==ad['cell']['RAW_sha256']
assert load(snap)['status']=='independently_verified' and load(snap)['evidence']['independent_verification']==cur['evidence']['independent_verification']
new=copy.deepcopy(cur);old=load(snap)
for k in ['blocked','evidence','graph_contribution']:new[k]=old[k]
assert new==old
unchanged=[]
for p in [R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualOuterBoundedL2Continuity.lean',R/'AutoSamplingTheory/ExampleCases.lean',R/'AutoSamplingTheory/TechnicalLemmas/Registry.lean',R/'Tests/Basic.lean',R/'Tests.lean',R/'lean-toolchain',R/'lake-manifest.json',R/'website/content/declaration_lessons/pbps-actual-outer-bounded-l2-continuity.json',R/'website/content/publications/pbps-actual-outer-bounded-l2-continuity.json',R/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualOuterBoundedL2Continuity.json',R/'runs/substantive_advances.jsonl']:
 raw=p.read_bytes();blob=gitblob(p);assert norm(raw)==norm(blob);unchanged.append(dict(**info(p),checked_git_blob_RAW_sha256=hashlib.sha256(blob).hexdigest(),exact_or_newline_only_equal=True))
assert unchanged[0]['RAW_sha256']=='8fd35db26717f46313fc53dd90691828b11c9d78cdcc4a62f68c8d59273cc2bd'
helpers=[]
for name,oldtoken,newtoken in [('commit_integration84.py',b'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-bounded-test-continuity.json',b'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-outer-bounded-l2-continuity.json'),('run_gates84.py',b'ASTIS-SW-PBPS-actual-bounded-test-continuity',b'ASTIS-SW-PBPS-actual-outer-bounded-l2-continuity')]:
 p=B/name;blob=norm(gitblob(p));raw=norm(p.read_bytes());assert blob.count(oldtoken)==1 and raw==blob.replace(oldtoken,newtoken,1);helpers.append(info(p))
p=R/'docs/companion-papers-handoff.md';blob=norm(gitblob(p));raw=norm(p.read_bytes());oldtoken=b'/graph checks are bound in84 integration.notes.json.';newtoken=b'/graph checks are bound in84 integration.corrected.notes.json.';assert blob.count(oldtoken)==1 and raw==blob.replace(oldtoken,newtoken,1)
notes=load(B/'integration.notes.json');correct=load(B/'integration.corrected.notes.json');assert info(B/'integration.notes.json')['RAW_sha256']==correct['prior_integration_note']['RAW_sha256']
checks=[]
for e in notes['checks']:
 p=Path(e['receipt']['path']);r=load(p);assert r['exit_code']==0 and r['terminal_closed'] and info(p)['RAW_sha256']==e['receipt']['RAW_sha256']
 for k in ['stdout','stderr']:
  f=r[k];q=Path(f['path']);q=q if q.is_absolute() else R/q;assert info(q)['RAW_sha256']==f['RAW_sha256']
 checks.append(dict(label=e['label'],receipt=info(p)))
correction_receipts=[]
for label in ['correct-cell-graph','metadata-publication','metadata-contributor','frontier','semantic']:
 p=B/'integration84/cell-admission-correction'/(label+'.receipt.json');r=load(p);assert r['exit_code']==0 and r['terminal_closed']
 for k in ['stdout','stderr']:assert info(r[k]['path'])['RAW_sha256']==r[k]['RAW_sha256']
 if label=='correct-cell-graph':assert r['command'][-1]=='ASTIS-SW-PBPS-actual-outer-bounded-l2-continuity'
 if label.startswith('metadata-'):assert r['command'][-2:]==['--base',C]
 correction_receipts.append(info(p))
wrong=B/'integration84/graph-check/receipt.json';assert load(wrong)['command'][-1]=='ASTIS-SW-PBPS-actual-bounded-test-continuity' and norm(wrong.read_bytes())==norm(gitblob(wrong))
assert norm((B/'integration84/graph-check/stdout.log').read_bytes())==norm(__import__('gzip').decompress(gitblob(B/'integration84/graph-check/stdout.log.gz')))
sys.path[:0]=[str(R/'tools'),str(R/'website/scripts')];import astis_site,publication_reader
source_digest=astis_site.source_digest();gate=load(R/'.astis/site-lean-gate.json');assert gate['passed'] and source_digest==gate['source_digest']==notes['lean_source_digest']
graph=load(R/'_site/data/underlying-lean-graph.json');graphdigest=publication_reader.graph_input_digest();assert graphdigest==graph['publication_inputs_sha256']==notes['publication_inputs_sha256'];assert info(R/'_site/data/underlying-lean-graph.json')['RAW_sha256']==notes['current_graph']['RAW_sha256']
page=R/'_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html';offline=load(B/'integration84/offline-reader.json');assert info(page)['RAW_sha256']==offline['page_RAW_sha256'] and offline['exact_step_Lean_regions']==8
log=(B/'integration84/canonical-lean-gate/stdout.log').read_text(encoding='utf8');assert re.findall(r'Build completed successfully \((\d+) jobs\)',log)==['9195','9495'] and 'ASTIS check passed' in log
math=load(B/'independent-math84/closed-raw-manifest84.json')
for e in math['frozen_inputs']+math['owned_artifacts']:assert info(e['path'])['RAW_sha256']==e['RAW_sha256']
verified=load(B/'exact-commit-verification84/verified.json');assert verified['verified_commit']=='dd3a23011b91569acbcd591ccd7b06301147d339'
assert info(B/'exact-commit-verification84/verified.json')['RAW_sha256']=='127e27ba9605502d6a25015fec5ec721f66d218af97697b25f72efa937e40a1a'
for key in ['review_result','review_run','native_manifest']:
 e=verified['source_audit'][key];assert info(e['path'])['RAW_sha256']==e['RAW_sha256']
source=load(R/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualOuterBoundedL2Continuity.json');assert source['state']=='accepted' and source['publication_binding_sha256']==verified['publication_binding_sha256']
for p,h in load(R/'runs/20261007-companion-priority/pbps-outer-bounded-l2-preread84/pre-fetch84.workspace-RAW.json')['tracked_modified'].items():assert info(p)['RAW_sha256']==h
save('bounded-repair-evidence.json',dict(status='CONTROL_PLANE_RESTORE_CHECKS_PASS_GRAPH_CERTIFICATION_LIMITATION_RETAINED',reviewer_id='/root/exact_verify77',checked_integration_commit=C,current_proposed_cell=info(cell),remote_cell_status=remote['status'],actual_local_cell_status=cur['status'],already_admitted_independent_cell=info(snap),verified_admission=info(B/'exact-commit-verification84/verified.json'),exact_two_one_token_helper_corrections=helpers,handoff_pointer_only=info(R/'docs/companion-papers-handoff.md'),corrected_note=info(B/'integration.corrected.notes.json'),source_theorem_publication_tests_toolchain_ledger_unchanged=unchanged,original_retained_receipts=checks,new_correction_receipts=correction_receipts,old_wrong_target_receipt=info(wrong),source_digest=source_digest,graph_input_digest=graphdigest,current_graph=info(R/'_site/data/underlying-lean-graph.json'),same_original_generated_graph=True,page=info(page),same_original_generated_page=True,root_jobs=9195,test_jobs=9495,registry_count=533,real_Lean_or_source_reproof_rerun=False,old_full_gate_source_digest_matches_current=True,cell_metadata_note='Canonical Lean gate binds Lean/test/toolchain source digest; cell before final admin exactly equals independently admitted cell, current final-admin metadata is the same data used by retained publication/site graph receipts. No new independent verification or source promotion.',graph_limitation=info(O/'graph-evidence-mismatch.diagnosis.json'),all21collaborator_RAWs_preserved=True,original_wrong_receipts_unchanged=True,proving_owner_self_verification=False,production_shared_or_state_edits=False))
print('BOUNDED REPAIR EVIDENCE CLOSED',info(O/'bounded-repair-evidence.json')['RAW_sha256'])
