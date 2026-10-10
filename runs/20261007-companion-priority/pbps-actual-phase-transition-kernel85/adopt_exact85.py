from pathlib import Path
import gzip,hashlib,json,subprocess
r=Path(__file__).parent;d=r/'exact-commit-verification85';load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha((d/'verified.json').read_bytes())=='6244ceea9cff19ff39bde8bfa7bd80a99b1a4354fc90b59446782750add9bfd9'
assert sha((d/'closed-RAW-manifest85.json').read_bytes())=='586d12d9d284cb6f2ba1c499736dab935113655b24d76f10c0375a6a7f608d35'
m=load(d/'closed-RAW-manifest85.json');v=load(d/'verified.json');C='6d7d42f996a4fbb159c518623fd35c1ac7717fe9'
assert m['status']=='CLOSED_RAW_NONCIRCULAR' and m['verified_commit']==v['verified_commit']==C
assert v['status']=='PASS_INDEPENDENT_EXACT_COMMIT_VERIFICATION' and v['verifier_id']=='/root/exact_verify77'
changes={'runs/substantive_advances.jsonl','research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-phase-transition-kernel.json'}
for x in m['checked_science_inputs']:
 b=subprocess.check_output(['git','show',C+':'+(x.get('lossless_archive') or x['path'])])
 if x.get('lossless_archive'):b=gzip.decompress(b)
 assert sha(b)==x['git_blob_RAW_sha256'],x['path']
 if x['path'] not in changes:assert sha(Path(x['path']).read_bytes())==x['RAW_sha256'],x['path']
for group in ['nested_pinned_mathlib','local_fixed_primary','local_compiled_artifacts','owned_artifacts']:
 for x in m[group]:assert sha(Path(x['path']).read_bytes())==x['RAW_sha256'],x['path']
assert load(d/'admission85.json')['state']=='VERIFIED'
assert load(d/'post-admission-frontier.receipt.json')['exit_code']==0
p=r/'root.exact85.adoption.json';assert not p.exists();p.write_text(json.dumps(dict(status='INDEPENDENT_EXACT_COMMIT_VERIFIED_EVIDENCE_ADOPTED',verified_commit=C,native_verified_RAW_sha256=sha((d/'verified.json').read_bytes()),native_closed_manifest_RAW_sha256=sha((d/'closed-RAW-manifest85.json').read_bytes()),science_inputs_rebound_to_exact_Git=True,admission_cell_ledger_changes_explicit=True,source_statement_BODY_lesson_unchanged=True,aggregate='pending',Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
print('Exact independent VERIFIED evidence rehashed and adopted; sole-lane aggregation now eligible')
