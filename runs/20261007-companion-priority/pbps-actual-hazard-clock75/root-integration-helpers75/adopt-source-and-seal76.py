from pathlib import Path
import hashlib,json,os,subprocess,sys
pre=Path('runs/20261007-companion-priority/pbps-recursive-preproof76');o=pre/'independent-source76'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def check(z,path=None):
 p=Path(path or z['path']);b=p.read_bytes();assert len(b)==z['RAW_bytes'] and sha(b)==z['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==z['LF_sha256'];return b
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
def new(p,x):
 p=Path(p);assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
lp=o/'lease.final.json';assert sha(lp.read_bytes())=='b7bdca274bbc819b079b15ca600941a03dcae679ce96a40ce7caf5ec79decbc5'
l=load(lp);assert l['status']=='CLOSED_LAST' and l['no_further_writes'] and l['owned_file_count_including_lease']==67
rows=l['files'];assert len(rows)==66
assert {p.resolve() for p in o.rglob('*') if p.is_file()}=={(o/z['owned_relative_path']).resolve() for z in rows}|{lp.resolve()}
for z in rows:check(z,o/z['owned_relative_path']);assert (o/z['owned_relative_path']).stat().st_mtime_ns<=lp.stat().st_mtime_ns
run=load(o/'source.0.run.json');h=sha(can({k:v for k,v in run.items() if k!='run_sha256'}));assert h==run['run_sha256']==l['native_run_sha256']=='dab106a00ace8389a782a96b9ccc9bf556b5483e9ef6e71c5abf45363b51a563'
assert run['no_canonical_files_modified'] and run['no_proof_or_SAU_or_VERIFIED_claim'] and not run['reviewer_is_formalizer']
cp=o/'complete-named-review-decision-input-payload.json';assert sha(cp.read_bytes())==l['complete_five_RAW_payload_sha256']=='025a5492a96239d6ed2e8ff7f2f8df5742c2a824c0b83f1066862f5cf11fcfe5'
payload=load(cp);assert payload['payload_count']==len(payload['named_RAW_payloads'])==5
for z in payload['named_RAW_payloads']:assert check(z,o/z['name'])==z['RAW_payload_utf8'].encode()
for z in load(o/'source.0.input-manifest.json')['candidate_and_parent_full_RAW_snapshots']:assert check(z,z['original_path'])==check(z,z['snapshot_path'])
d=load(o/'source.0.decision.json');admission=load(o/'source.0.admission-fields.json');fields=admission['prospective_statement_seal_fields'];neutral=fields['expanded_binder_audit']
assert d['status']=='ACCEPT_PROSPECTIVE_SOURCE_HEADER_ONLY' and d['ready_for_exact_prospective_header_seal'] and d['blocking_delta_count']==0 and not d['repairs']
assert admission['fresh_postcompile_source_review_required'] and admission['audit_fields'] is None and admission['cell_source_proof_coverage'] is None
def clean(x):
 if isinstance(x,dict):
  assert not set(x)&{'semantic_slots','deltas','verdict','review_run_sha256'}
  for v in x.values():clean(v)
 elif isinstance(x,list):
  for v in x:clean(v)
clean(neutral);assert neutral['counts']==dict(callers=6,typing=5,literal_definitions=11,conclusion_groups=10)
math=load(pre/'root.math-header76.adoption.json');assert check(math['accepted_header'])==check(fields['header'],fields['header']['original_path'])
check(math['native_lease']);assert sha((pre/'header76.v3.proposed.lean').read_bytes())=='996b8a89ffe84cfef8faf75551f962f2378db221841f5e1a38137eb81281d015'
out=Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR'])
with (out/'native-readonly.stdout.log').open('wb') as s,(out/'native-readonly.stderr.log').open('wb') as e:
 p=subprocess.Popen([sys.executable,'-B','-X','utf8',str(o/'verify_closed76.py'),'--observed-close-exit','0'],stdout=s,stderr=e);code=p.wait()
assert code==0
record=dict(status='ACCEPTED_CLOSED_PROSPECTIVE_SOURCE_HEADER76_ONLY',actual_root_PID=os.getpid(),native_lease=pin(lp),native_files=67,native_run_sha256=h,native_complete_five_RAW=pin(cp),native_whole_owned_logical_run_sha256=l['whole_logical_run_sha256'],native_readonly_PID=p.pid,native_readonly_EXIT=code,admission_fields=pin(o/'source.0.admission-fields.json'),candidate=pin(pre/'header76.v3.proposed.lean'),blocking_deltas=0,mathematical_source_repairs=[],actual_theorem_proved=False,new_SAU=False,Goal_complete=False)
new(pre/'root.source-header76.adoption.json',record)
new(pre/'root.header-reviews76.adoption.json',dict(status='PREPROOF_V3_HEADER76_ACCEPTED_PENDING_CLAIM_AND_PROOF',math_review=math,source_review=record,no_mathematical_repairs=True,exact_two_type_coercions_independently_reviewed=True,no_theorem_proof=True,header=pin(pre/'header76.v3.proposed.lean'),neutral_binder_inventory=neutral,source_graph=fields['source_graph'],source_inventory=fields['source_coverage_inventory'],source_first_freeze=fields['source_first_freeze'],prospective_coverage=pin(o/'header76.source-coverage-map.json'),Goal_complete=False))
assert not Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean').exists()
new(pre/'root.statement-seal76.json',dict(status='SEALED_V3_BEFORE_PROOF_SEARCH_AFTER_DISTINCT_HEADER_MATH_AND_SOURCE',actual_root_PID=os.getpid(),header=pin(pre/'header76.v3.proposed.lean'),statement_version=3,source_anchors=['arXiv2609.06905v1 AppendixA.1 equation(A.2), Ex4-8; fixed-reference finite stopped skeleton only'],source_plan=pin(pre.parent/'pbps-recursive-path-preread76/selected.contract.json'),source_graph=fields['source_graph'],source_inventory=fields['source_coverage_inventory'],source_first_freeze=fields['source_first_freeze'],exact_source_formulas=fields['exact_source_formulas'],header_reviews=pin(pre/'root.header-reviews76.adoption.json'),binder_inventory=neutral,original_six_callers=True,definitions=11,conclusion_groups=10,private_literal_is_specification_not_provider=True,typecheck_predicate_Lean_PID=29384,typecheck_full_telescope_Lean_PID=48688,original_and_insufficient_v2_type_negatives_preserved=True,exact_type_ascription_change='Two finite WithTop NNReal waits are explicitly ascribed NNReal before Real coercion. No formula/caller/conclusion change.',Lean_toolchain=pin('lean-toolchain'),Mathlib_manifest=pin('lake-manifest.json'),truth_boundary='Prospective finite stopped recursion only; no current theorem proof. Source graph distinguishes finite/top/zero thresholds, original-energy cap and deterministic wait increment from future iid/positivity/SLLN/nonaccumulation/global path/Markov/invariance/kernel/main/cost/composition. Corrected Davis1984 bibliography is context only, no source theorem text or Lean dependency. Claim/proof wait for parent75 serialized integration and normal push.',proof_search=False,new_SAU=False,Goal_complete=False))
print('PASS76 prospective v3 source/math accepted and Statement Seal frozen before proof search; parent75 integration/claim/proof pending.')
