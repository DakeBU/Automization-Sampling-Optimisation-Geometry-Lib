from pathlib import Path
import base64,hashlib,json,os,subprocess,sys
r=Path('runs/20261007-companion-priority/pbps-clock-preproof75');o=r/'independent-header-source75';out=r/'root-source-adoption75';out.mkdir(exist_ok=False)
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def check(z):
 b=Path(z['path']).read_bytes();assert len(b)==z['RAW_bytes'] and sha(b)==z['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==z['LF_sha256'],z['path'];return b
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
def write(p,x):
 p=Path(p);assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
lp=o/'lease.final.json';assert sha(lp.read_bytes())=='097275eafecd32d40da05160d25de30e1ca606fe725b4e3ec38bbb353fb44198'
l=load(lp);rows=l['all_owned_outputs_except_only_self'];assert l['status']=='CLOSED_LAST' and l['owned_count']==len(rows)+1==35 and l['all_sessions_closed'] and not l['postclose_owned_writes']
assert {p.resolve() for p in o.rglob('*') if p.is_file()}=={Path(z['path']).resolve() for z in rows}|{lp.resolve()}
for z in rows:check(z);assert Path(z['path']).stat().st_mtime_ns<=lp.stat().st_mtime_ns
run=load(o/'run75.json');h=sha(can({k:v for k,v in run.items() if k!='run_sha256'}));assert h==run['run_sha256']==l['whole_logical_run_sha256']=='2a5e8e3ce15414148047fb8d893d4e91192b0f911a6df11e0c52e342d2d157c0'
payload=load(l['complete_named_RAW_payload']['path']);check(l['complete_named_RAW_payload']);assert l['complete_named_RAW_payload']['RAW_sha256']=='299d5d8ad194fdfa738ee12f8421fec8df5bf7e69423811ffa8066de557a1482'
assert len(payload['named_payloads'])==5
for z in payload['named_payloads']:assert check(z['pin'])==base64.b64decode(z['complete_RAW_base64'],validate=True)
im=load(run['input_manifest']['path']);check(run['input_manifest']);assert im['current_input_count']==len(im['current_inputs'])==26 and im['reused_StageA_input_count']==len(im['reused_StageA_inputs'])==22
for z in im['current_inputs']+im['reused_StageA_inputs']:
 check(z)
 if 'snapshot' in z:assert check(z)==check(z['snapshot'])
d=load(o/'decision75.json');assert d['blocking_count']==0 and not d['required_repairs'] and d['prospective_only'] and len(d['semantic_slots'])==7 and len(d['deltas'])==6
admission=load(o/'admission-fields75.json');assert sha((o/'admission-fields75.json').read_bytes())=='034b9248dfc15a76a598ede004124e625bdfcc8260ca5d4a1698217a3343b610'
header=admission['candidate_header'];assert check(header)==(r/'header75.v2.proposed.lean').read_bytes()
api=admission['exact_API_overlay_admission'];assert api['all_other_bytes_identical'] and api['allowed_occurrences']==1 and not api['additional_changes_authorized']
before=check(api['before_header']);assert before.count(api['allowed_exact_old'].encode())==1 and before.replace(api['allowed_exact_old'].encode(),api['allowed_exact_new'].encode())==check(header)
math=load(r/'root.math75.adoption.json');baseline=load(r/'root.source-baseline75.adoption.json');assert math['native_files']==51 and baseline['native_files']==53 and check(math['proposed_header'])==check(header)
for z in [math['native_lease'],baseline['native_lease']]:check(z)
with (out/'native-readonly.stdout.log').open('wb') as s,(out/'native-readonly.stderr.log').open('wb') as e:
 p=subprocess.Popen([sys.executable,'-B','-X','utf8',str(o/'check_header75.py')],stdout=s,stderr=e);code=p.wait()
assert code==0
record=dict(status='ACCEPTED_CLOSED_PROSPECTIVE_SOURCE_HEADER75_AND_EXACT_API_OVERLAY_ONLY',actual_root_PID=os.getpid(),native_lease=pin(lp),native_files=35,current_input_entries=26,reused_stageA_inputs=22,native_run_sha256=h,native_complete_named=l['complete_named_RAW_payload'],native_readonly_PID=p.pid,native_readonly_EXIT=code,admission_fields=pin(o/'admission-fields75.json'),candidate=pin(r/'header75.v2.proposed.lean'),blocking_deltas=0,mathematical_source_repairs=[],exact_API_overlay_accepted=True,actual_theorem_proved=False,new_SAU=False,Goal_complete=False)
write(r/'root.source-header75.adoption.json',record)
write(r/'root.header-reviews75.adoption.json',dict(status='PREPROOF_HEADER75_ACCEPTED_PENDING_CLAIM_AND_PROOF',actual_root_PID=os.getpid(),reviews=[baseline,math,record],no_mathematical_repairs=True,exact_API_repair_independently_accepted=True,no_theorem_proof=True,header=pin(r/'header75.v2.proposed.lean'),source_coverage=admission['prospective_source_proof_coverage'],source_admission=admission['source_header_admission'],Goal_complete=False))
assert not Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHazardClock.lean').exists()
write(r/'root.statement-seal75.json',dict(status='SEALED_V2_BEFORE_PROOF_SEARCH_AFTER_DISTINCT_HEADER_MATH_AND_SOURCE',actual_root_PID=os.getpid(),header=pin(r/'header75.v2.proposed.lean'),statement_version=2,source_anchors=['arXiv2609.06905v1 Algorithm1/Proposition3.1','AppendixA.1 equation(A.1), A.2 recursive consumer remains open'],source_plan=pin(r.parent/'pbps-clock-construction-preread75/selected.contract.json'),source_graph=pin(r/'independent-source-baseline75/source-proof-graph75.json'),source_inventory=pin(r/'independent-source-baseline75/source-coverage-inventory75.json'),header_reviews=pin(r/'root.header-reviews75.adoption.json'),original_six_callers=True,definitions=8,conclusion_groups=10,private_literal_is_specification_not_provider=True,typecheck_predicate_Lean_PID=17148,typecheck_full_telescope_Lean_PID=28408,original_unknown_identifier_negative_preserved=True,exact_API_overlay=pin(r/'exact-API-overlay75.source-review-proposal.json'),Lean_toolchain=pin('lean-toolchain'),Mathlib_manifest=pin('lake-manifest.json'),truth_boundary='Prospective statement only. No actual theorem proof, clock/path/nonexplosion/Markov/invariance/kernel/main/cost/composition/Exposition/PURIFIED/live/Goal completion credit. Claim/proof wait for parent74 serialized integration.',proof_search=False,new_SAU=False,Goal_complete=False))
write(out/'receipt.json',dict(status='CLOSED35_SOURCE_ADOPTED_AND_V2_STATEMENT_SEALED_ONLY',actual_root_PID=os.getpid(),native_readonly_PID=p.pid,native_readonly_EXIT=code,Goal_complete=False))
print('PASS75 exact API overlay and full prospective source header adopted; v2 sealed before any proof search; no SAU/theorem proof credit.')
