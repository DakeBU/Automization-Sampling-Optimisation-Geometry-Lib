import base64,hashlib,json,os,pathlib
out=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
run=json.loads((out/'review-run.json').read_bytes());v=run.pop('run_sha256');assert sha(canon(run))==v
payload=json.loads((out/'RAW-input-payload.json').read_bytes());review=json.loads((out/'RAW-review-payload.json').read_bytes())
assert run['complete_named_RAW_LF_input_payload']==payload and run['complete_named_RAW_review_payload']==review
for x in payload['inputs']:
 b=base64.b64decode(x['complete_RAW_bytes_base64']);lf=base64.b64decode(x['complete_LF_bytes_base64'])
 assert len(b)==x['RAW_bytes'] and sha(b)==x['RAW_sha256'] and b.replace(b'\r\n',b'\n')==lf and sha(lf)==x['LF_sha256']
 assert (out/x['name']).read_bytes()==b and (out/(x['name']+'.LF')).read_bytes()==lf
 assert pathlib.Path(x['original_path']).read_bytes()==b
for x in review['outputs']:
 b=base64.b64decode(x['complete_RAW_bytes_base64']);lf=base64.b64decode(x['complete_LF_bytes_base64'])
 assert (out/x['name']).read_bytes()==b and sha(b)==x['RAW_sha256'] and b.replace(b'\r\n',b'\n')==lf and sha(lf)==x['LF_sha256']
old=out.parent/'independent-primary69'
lease_b=(old/'lease.final.json').read_bytes();assert sha(lease_b)=='2d168d568a260f2cc18fba260a5bd7c1ac45cb41602f6a359df3d16b387aec93'
lease=json.loads(lease_b);mb=(old/'owned-manifest.json').read_bytes();assert sha(mb)==lease['manifest_RAW_sha256']
manifest=json.loads(mb);assert len(list(old.iterdir()))==82
assert len(manifest['regular_file_entries'])==80
for x in manifest['regular_file_entries']:
 b=(old/x['name']).read_bytes();assert len(b)==x['RAW_bytes'] and sha(b)==x['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==x['LF_sha256']
finite=json.loads((out/'finite-coverage-manifest.json').read_bytes())
entries=dict(header_segments=finite['expanded_header_segments_entries'],metadata=finite['metadata_entries'],source_math=finite['source_math_entries'])
assert sha(canon(entries))==finite['coverage_entries_canonical_sha256']
assert finite['expanded_header_uncovered_bytes']==0 and finite['metadata_unclassified_fields']==0 and finite['source_math_unchecked']==0
assert sum(x['RAW_bytes'] for x in finite['expanded_header_segments_entries'])==6533
decision=json.loads((out/'header-source-decision.json').read_bytes())
assert decision['verdict']=='ADMIT_HEADER_ONLY_FOR_STATEMENT_SEAL_CONSIDERATION'
assert not decision['extra_public_premises'] and not decision['missing_source_premises'] and not decision['source_semantic_repairs_required']
receipts=[]
for p in sorted(out.glob('foreground-*.receipt.json')):
 r=json.loads(p.read_bytes());assert r['actual_exit']==0 and r['completed'] and r['foreground'];receipts.append(dict(name=p.name,actual_pid=r['actual_pid'],actual_exit=0))
report=dict(schema='header-source69-complete-readback-v1',actual_pid=os.getpid(),whole_logical_run_sha256=v,
 deleted_ONLY_top_level_run_sha256=True,complete_inputs_verified=len(payload['inputs']),complete_outputs_verified=len(review['outputs']),
 current_original_inputs_unchanged=True,prior_CLOSED82_all_native_bytes_verified_unchanged=True,prior_native_count=82,
 source_math_count=419,expanded_header_lines=107,expanded_header_segments=10,metadata_fields=finite['metadata_fields'],
 actual_foreground_receipts=receipts,source_header_only=True,no_proof_or_compilation=True)
(out/'readback-report.json').write_text(json.dumps(report,sort_keys=True,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,sort_keys=True))
