"""Issue this independent VERIFIED transition only; no stabilization."""
from pathlib import Path
import copy, datetime, hashlib, json, os, subprocess, sys
ROOT=Path('E:/Samplinglib'); os.chdir(ROOT);sys.path[:0]=[str(ROOT),str(ROOT/'tools')]
from tools.astis_advance import transition_advance, _replay_advances
R=ROOT/'runs/20261007-companion-priority/pbps-actual-nonaccumulation78';P=R/'exact-commit-verification78'
C='bbcad09376c51bbf27c0ed4c16be0dc053bb01c5';ID='ASTIS-SA-20261010-PBPSActualNonaccumulation'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualNonaccumulation.actual_fixed_reference_event_time_nonaccumulation'
CELL=ROOT/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-event-time-nonaccumulation.json'
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def info(p):
 p=Path(p);b=p.read_bytes();return dict(path=str(p),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def save(n,v):
 p=P/n;assert not p.exists(),p;p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def states():return _replay_advances([json.loads(x) for x in (ROOT/'runs/substantive_advances.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()])
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()==C
assert load(P/'checks-complete.json')['status']=='PASS'
module=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualNonaccumulation.lean'
assert module.read_bytes()==subprocess.check_output(['git','show',C+':'+module.relative_to(ROOT).as_posix()])
assert info(module)['RAW_sha256']=='e6d71cb969b30f6ac8e6be65e5cd067166b4f29213d9328ed9edc0971fd026fc'
before=states();assert before[ID]['state']=='PROVED_LOCAL';assert before[ID]['owner_id']=='companion_root_20261005'
lane={k:v for k,v in before.items() if v.get('state')=='STABILIZING'}
assert set(lane)=={'ASTIS-SA-20261005-SPHMCImplementedPhaseKernel'}
cell=load(CELL);assert cell['status']=='proved_locally';save('cell.before-independent-admission.json',cell)
audit=load(ROOT/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualNonaccumulation.json')
assert audit['state']=='accepted' and audit['source_review']['reviewer']=='/root/fresh_source78'
assert audit['publication_binding_sha256']=='f812375b3e96e4b089af570ccd3a0f2f0852e0bd950290f77791b89974fc9069'
decoder=load(R/'anonymous-decoder78/run-manifest.json')
assert decoder['decoder']=='/root/blind_decoder78' and not decoder['source_text_visible'] and not decoder['source_identity_visible'] and not decoder['proof_BODY_visible']
for e in decoder['input_artifacts']+decoder['output_artifacts']:
 assert info(e['path'])['RAW_sha256']==e['raw_sha256']
receipts=[]
for n in ['packet','focused-module','contributor','publication','semantic','frontier']:
 p=P/(n+'.receipt.json');r=load(p);assert r['exit_code']==0 and r['terminal_closed'] and r['checked_commit']==C
 for e in [r['stdout'],r['stderr']]:assert info(e['path'])['RAW_sha256']==e['RAW_sha256']
 receipts.append(info(p))
assert not load(P/'fake-closure-scan.json')['hits']
verdict=dict(status='PASS_INDEPENDENT_EXACT_COMMIT_VERIFICATION',verifier_id='/root/exact_verify77',verified_commit=C,
 created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_admission_helper_PID=os.getpid(),
 lean_module=info(module),gate=receipts,source_audit=dict(state='accepted',reviewer='/root/fresh_source78',
 review_result=info(R/'fresh-source78/source-review.result78.json'),review_run=info(R/'fresh-source78/source-review.run-manifest78.json'),
 reviewer_packet_sha256='5fb176d5c9dbb96a3448593de56df696d6517decc1971bf250dbdffc1007f362'),
 semantic_roundtrip_audit='ASTIS-RT-20261010-PBPSActualNonaccumulation',publication_declarations=[D],
 publication_binding_sha256=audit['publication_binding_sha256'],fake_closure_scan=info(P/'fake-closure-scan.json'),
 unchanged_fresh_full_source_elaboration=info(R/'independent-math78/fresh-whole-module-axioms.receipt.json'),
 fresh_elaboration_reuse='Own complete-source native elaboration and all inputs/logs remain exact; current commit binds module, both parents, seal, full-source probe, pinned toolchain and manifest. Focused build rerun at this exact commit.',
 axioms=['propext','Classical.choice','Quot.sound'],independent_mathematics=info(R/'independent-math78/decision78.json'),
 whole_proof_review=info(R/'independent-math78/whole-proof-mathematics78.json'),exact_definition_review=info(R/'independent-math78/statement-and-definition-audit78.json'),
 blind_decoder=dict(identity='/root/blind_decoder78',manifest=info(R/'anonymous-decoder78/run-manifest.json'),source_text_visible=False),
 exact_input_and_seven_BODY_formula_lesson_freeze=info(P/'input-freeze.json'),
 mathematical_cases=['six sealed source analytic binders and no provider premises','actual literal flow/bounce/hazard/record definitions equal parent','canonical epsilon index matches product',
 'C=0 includes rank0/zero-energy and positive first threshold stops with absorption','C>0 yields S_n/C<=T_n by extended-valued induction including initialization and top',
 'positive finite cap transfers divergent actual sums to every finite horizon escape, including never-stopped paths','finite sublevel index set lies below a natural N and includes initialization index0'],
 lesson_review='Seven exact contiguous BODY regions lines74-184; all formulas/prose independently checked against full proof and native mathematics. No WithTop atTop target substituted.',
 truth_boundary=load(R/'claim.json')['truth_boundary'],
 remaining_acceptance=['canonical aggregate imports/Registry/root Tests and full astis.py check','graph/site generation/check and visual reader acceptance','serialized stabilization in existing sole lane',
 'main merge and remote CI','live validation','Exposition Seal and postmerge purification','full PBPS/global process/main accuracy/query costs/composition and existing four-paper Goal'],
 nonblocking_notes=['Module overview still says Prospective statement only; publication cleanup pending','hcapPos unused; purification pending'],
 production_edits=False,stabilization=False,Goal_complete=False,
 provenance='Exact input hashes and real foreground terminal receipts. No fabricated native reasoning trajectory. Prior verifier procedure failure retained as attempt1-procedure-diagnosis.json.')
save('verified.json',verdict)
e={k:verdict[k] for k in ['verifier_id','verified_commit','source_audit','fake_closure_scan','publication_declarations','semantic_roundtrip_audit']};e['gate']=info(P/'verified.json')
transition_advance(ID,'VERIFIED',worker_id='/root/exact_verify77',evidence=e)
new=copy.deepcopy(cell);new['status']='independently_verified';new['evidence']['independent_verification']=(P/'verified.json').relative_to(ROOT).as_posix()
CELL.write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
after=states();assert after[ID]['state']=='VERIFIED'
assert {k:v for k,v in after.items() if k!=ID}=={k:v for k,v in before.items() if k!=ID}
rest=copy.deepcopy(load(CELL));rest['status']=cell['status']
if 'independent_verification' in cell.get('evidence',{}):rest['evidence']['independent_verification']=cell['evidence']['independent_verification']
else:rest['evidence'].pop('independent_verification')
assert rest==cell
save('admission.json',dict(state='VERIFIED',cell_state='independently_verified',verified_commit=C,verifier_id='/root/exact_verify77',
 verified=info(P/'verified.json'),cell=info(CELL),all_other_cell_metadata_semantically_preserved=True,all_other_advance_records_unchanged=True,
 existing_stabilization_lane_unchanged=list(lane),stabilization=False,Goal_complete=False))
print('VERIFIED',C,info(P/'verified.json')['RAW_sha256'])
