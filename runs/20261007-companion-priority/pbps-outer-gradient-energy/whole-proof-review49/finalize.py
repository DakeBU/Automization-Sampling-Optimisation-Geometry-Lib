# -*- coding: utf-8 -*-
from pathlib import Path
import json,hashlib,re,datetime,sys
sys.stdout.reconfigure(encoding='utf-8');R=Path('E:/Samplinglib');D=R/'runs/20261007-companion-priority/pbps-outer-gradient-energy';O=D/'whole-proof-review49'
def sha(b):return hashlib.sha256(b).hexdigest()
def lf(b):return b.replace(b'\r\n',b'\n')
def dump(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def read(n):return json.loads((O/n).read_text(encoding='utf-8'))
# Before sealing, pin and resolve the actual global gradient/Riesz definition names.
calls=read('direct-mathematical-call-review.json');corrections=[]
for e in calls['calls']:
 if e['declaration']=='InnerProductSpace.gradient':
  corrections.append(dict(field='direct-mathematical-call-review.json /calls declaration',draft='InnerProductSpace.gradient',resolved='gradient',reason='Exact Mathlib Gradient.Basic namespace scan confirms global declaration82; draft qualifier corrected before receipt seal.'))
  e['declaration']='gradient'
p=R/'.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Dual.lean';b=p.read_bytes();frag=b''.join(b.splitlines(keepends=True)[134:142]);(O/'api-Riesz-toDual.raw').write_bytes(frag);(O/'api-Riesz-toDual.lf').write_bytes(lf(frag))
calls['calls'].append(dict(declaration='InnerProductSpace.toDual',production_physical_lines1=[154],provider_binding='api-Riesz-toDual',checked_contract='Actual Hilbert Riesz linear isometry equivalence at Dual135; inverse continuous map composed with measurable Frechet derivative, gradient is global declaration82.'))
(O/'direct-mathematical-call-review.json').write_bytes(dump(calls));(O/'preseal-api-resolution.json').write_bytes(dump(dict(corrections=corrections,pinned_Riesz=dict(path=str(p),whole_raw_sha256=sha(b),whole_lf_sha256=sha(lf(b)),physical_lines1=[135,142],raw_fragment_sha256=sha(frag),lf_fragment_sha256=sha(lf(frag))),draft_helper_script_preserved=True,meaning='Corrected API qualification before sealing; no Lean/proof/statement mutation.')))
# Final exact frozen input recheck; root publication may move separately, science may not.
freeze=json.loads((D/'math-freeze.json').read_text(encoding='utf-8'))
for x in freeze['inputs']:
 b=(R/x['path']).read_bytes();assert sha(b)==x['raw_sha256'] and sha(lf(b))==x['lf_sha256'] and len(b)==x['bytes'],x['path']
assert len(freeze['inputs'])==45
for file in ['AutoSamplingTheory/ExampleCases/ProximalBPS/ConditionalGradientEnergy.lean','Tests/ProximalBPSConditionalGradientEnergy.lean']:
 s=(R/file).read_text(encoding='utf-8');assert not re.search(r'\b(sorry|admit|sorryAx)\b|^\s*(?:unsafe\s+)?axiom\s|Prop\s*:=\s*True|:=\s*trivial',s,re.M)
for x in read('unchanged-parent-api-checks.json'):
 b=Path(x['path']).read_bytes();assert sha(b)==x['current_raw_sha256'] and sha(lf(b))==x['current_lf_sha256']
for x in read('astis-import-reachability.json')['modules']:
 b=Path(x['path']).read_bytes();assert sha(b)==x['raw_sha256'] and sha(lf(b))==x['lf_sha256'],x['module']
lease=read('lease.json');assert lease['status']=='OPEN' and all(lease[k]=='OPEN' for k in ['read','write','python']) and lease['compiler']=='CLOSED'
closed=dict(lease);closed.update(status='CLOSED',read='CLOSED',write='CLOSED',python='CLOSED',compiler='CLOSED',compiler_used=False,closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),final_operation='write actual CLOSED leases after all frozen inputs/output fingerprints are complete; no subsequent filesystem operations')
closedbytes=dump(closed)
outputs={}
for f in sorted(O.iterdir(),key=lambda x:x.name):
 if f.is_file() and f.name not in ['run.json','lease.json']:
  b=f.read_bytes();outputs[f.name]=dict(raw_sha256=sha(b),lf_sha256=sha(lf(b)),raw_bytes=len(b),lf_bytes=len(lf(b)))
run=dict(schema_version='wholeproof49-review-run-v1',status='CLOSED_ACCEPT_SCOPED_NO_MATHEMATICAL_BLOCKER',checked_base_commit=freeze['checked_base_commit'],frozen_math_input_count=45,math_freeze_raw_sha256=sha((D/'math-freeze.json').read_bytes()),all_frozen_inputs_matched_at_final_close=True,sourcegraph_creator_role_disclosed=True,source_topology_self_admission=False,freshblind_or_publication_read=False,reviewer_compiler_used=False,reused_root_focused_production_attempt=2,reused_root_focused_tests_attempt=1,focused_tests_jobs=3888,closure_axiom_prints=3,reachable_astis_modules=65,negative_results='No mathematical blocker or fake proof closure found within bounded reviewed scope; raw scan hits only Core marker strings.',output_files=outputs,expected_actual_closed_lease_raw_sha256=sha(closedbytes),hash_recipe=dict(raw='SHA256 exact file bytes',lf='SHA256 bytes with CRLF replaced by LF',outputs='Sorted relative names of every prepared file excluding run.json and mutable lease.json; final lease separately bound',run='SHA256 exact UTF8 LF JSON bytes; no self-digest field'),limits='This is substantive independent wholeproof review of frozen bytes, not an independent compiler rerun/full repository gate, source admission, freshblind receipt, exact-proof-commit verification or VERIFIED transition.')
runbytes=dump(run);(O/'run.json').write_bytes(runbytes)
result=dict(status=run['status'],run_raw_sha256=sha(runbytes),review_raw_sha256=outputs['whole-proof-review.json']['raw_sha256'],capsule_raw_sha256=outputs['capsule.md']['raw_sha256'],lease_raw_sha256=sha(closedbytes),science_raw_sha256=freeze['inputs'][0]['raw_sha256'],all_actual_leases='CLOSED',reviewer_compiler_used=False)
# FINAL filesystem operation. Print only already computed in-memory evidence afterward.
(O/'lease.json').write_bytes(closedbytes)
print(json.dumps(result,indent=2))
