from pathlib import Path
import json,hashlib
from datetime import datetime,timezone
R=Path('/Users/zhouhuanjian/ASTIS-GC');B=R/'.astis/semantic-neutral-20261112/mv_src_6e28/r9-centered-whole-code-only-v1'
def record(p):
 a=p.read_bytes();return {'path':str(p.relative_to(R)),'bytes':len(a),'sha256':hashlib.sha256(a).hexdigest()}
def write(n,d):
 with (B/n).open('x') as f:f.write(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
files=sorted(p for p in B.rglob('*') if p.is_file());write('artifact-manifest.json',{'phase':'R9 T WHOLE CODE ONLY','files':[record(p) for p in files],'self_hash_external':True})
seal={'schema_version':1,'phase':'R9_CENTERED_WHOLE_CODE_ONLY_FROZEN','frozen_utc':datetime.now(timezone.utc).isoformat(),'reviewer':'/root/mv_fresh_source_6e28','candidate':'6819e686116e6f18df3ef0e638c6ca24bde7dd8d plus untracked exact T bytes; not a commit containing T','T_file_sha256':'c72d3573c6047b75983a958ad8b98de9c399e13277daa852a66c3e5a0820e73b','T_signature_sha256':'95e81a02e5302de9a42e3b60038ffad6195315ac2eca99a4e6abb39978609f7e','result':'No blocking code/source-meaning or provider-applicability gap found by independent whole T code read; not final source-slot or compiler acceptance','new_ASTIS_complete_lines':567,'prior9_ASTIS_950_lines_reused_without_reread_claim':True,'exact_inputs':28,'Mathlib_pinned_source_checks':15,'report':record(B/'REPORT.md'),'exact_input_manifest':record(B/'exact-input-manifest.json'),'actual_read_ranges':record(B/'actual-read-ranges.json'),'provider_contracts':record(B/'provider-applicability-audit.json'),'artifact_manifest':record(B/'artifact-manifest.json'),'compiler_or_strict_results_read':False,'compiler_or_proof_executed':False,'new_T_decoder_lesson_anti_peer_verdict_read':False,'canonical_final_source_verdict_issued':False,'normal_API_calls':0,'ledger_C_registry_or_shared_source_mutations':False,'old_freezes_modified':False,'credit':'Private actual consumer code review only; public normalization/main consumption, final anonymous reconstruction/anti review, native, integration/purification and wholeGoal remain pending. Stop after freeze.','self_hash_external':True}
write('WHOLE-CODE-FROZEN.json',seal)
records=[]
for p in sorted(x for x in B.rglob('*') if x.is_file()):
 x=record(p);records.append({'source_path':x['path'],'destination_path':'research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-semantic-evidence/source-review/mv_src_6e28/r9-centered-whole-code-only-v1/'+str(p.relative_to(B)),'bytes':x['bytes'],'sha256':x['sha256'],'copy_rule':'Exact original bytes only; no canonical source decision implied.'})
write('portable-custody-manifest.json',{'schema_version':1,'records':records,'files':len(records),'total_bytes':sum(x['bytes'] for x in records),'self_hash_external':True,'later_freeze_command_envelope_externally_indexed':True})
for n in ['REPORT.md','exact-input-manifest.json','actual-read-ranges.json','WHOLE-CODE-FROZEN.json','artifact-manifest.json','portable-custody-manifest.json']:
 print(json.dumps(record(B/n)))
