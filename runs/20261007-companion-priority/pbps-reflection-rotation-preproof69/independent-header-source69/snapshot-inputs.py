import datetime,hashlib,json,os,pathlib
out=pathlib.Path(__file__).resolve().parent;run=out.parent;old=run/'independent-primary69';repo=pathlib.Path(r'E:\Samplinglib')
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(name,path,b,role):return dict(name=name,original_path=str(path),RAW_bytes=len(b),RAW_sha256=sha(b),LF_bytes=len(b.replace(b'\r\n',b'\n')),LF_sha256=sha(b.replace(b'\r\n',b'\n')),role=role)
def put(n,d):(out/n).write_text(json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
inputs=[]
def copy(name,path,role):
 b=path.read_bytes();(out/name).write_bytes(b);inputs.append(pin(name,path,b,role));return b
draft=json.loads(copy('candidate.header-draft69.RAW.json',run/'header-draft69.json','current-no-proof-header-metadata'))
assert draft['status']=='UNSEALED_NEXT_STATEMENT_DRAFT_NO_PROOF_SEARCH'
assert draft['SAU_claim'] is False and draft['Statement_Seal'] is False and draft['proof_search'] is False
for name in ['header0-expanded.lean','header0-public.lean','statement0.definition.lean']:
 b=copy('candidate.'+name,run/name,'current-header-or-complete-literal-private-Prop-only-no-body')
 expected=next(x for x in draft['headers'] if x['path'].endswith('/'+name))
 assert len(b)==expected['RAW_bytes'] and sha(b)==expected['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==expected['LF_sha256']
adoption=json.loads(copy('root.primary69.adoption.RAW.json',run/'root.primary69.adoption.json','source-only-adoption-provenance-not-a-candidate-verdict'))
lease_b=copy('prior-primary69.lease.final.RAW.json',old/'lease.final.json','immutable-prior-source-lease-read-only')
assert sha(lease_b)=='2d168d568a260f2cc18fba260a5bd7c1ac45cb41602f6a359df3d16b387aec93'
lease=json.loads(lease_b);assert lease['status']=='CLOSED_LAST' and lease['owned_file_count']==82
manifest_b=copy('prior-primary69.owned-manifest.RAW.json',old/'owned-manifest.json','immutable-prior-closure-manifest-read-only')
assert sha(manifest_b)==lease['manifest_RAW_sha256']=='1c2cb829368b83a04d59aad24859c5c724c381236347d6ae3b07a353173a68e9'
manifest=json.loads(manifest_b);pins={x['name']:x for x in manifest['regular_file_entries']}
for name in ['source-proof-graph.json','source-expectations.json','literal-formulas-and-conditions.json','finite-coverage-manifest.json','source-input-regions.json','source-expectations-frozen.json']:
 b=copy('prior-primary69.'+name,old/name,'frozen-source-first-expectation-evidence-read-only')
 assert sha(b)==pins[name]['RAW_sha256']
for p in sorted(old.glob('source.*.RAW.html')):
 b=copy(p.name,p,'exact-fixed-primary-HTML-source-region')
 assert sha(b)==pins[p.name]['RAW_sha256']
assert len(list(out.glob('source.*.RAW.html')))==7
fm_b=copy('parent67.fragment-map.RAW.json',run/'existing-parent67-statement.fragment-map.json','current-parent-header-only-provenance')
fm=json.loads(fm_b)
fragment=copy('parent67.statement.exact-RAW.fragment.lean',run/'existing-parent67-statement.exactraw.fragment.lean','complete-existing-parent-literal-Prop-no-proof-body')
full_path=repo/fm['parent_path'];full=full_path.read_bytes()
assert sha(full)==fm['parent_RAW_sha256']==draft['existing_verified_parent_RAW_sha256']
a,z=fm['RAW_range_end_exclusive'];assert full[a:z]==fragment
assert len(fragment)==fm['fragment_RAW_bytes'] and sha(fragment)==fm['fragment_RAW_sha256']=='cad04bdb202c104b9821855d0b652790668e50cf0f2550f1e00f044a134da010'
assert fm['no_parent_BODY_in_fragment'] is True
assert len(inputs)==22
for x in inputs:
 b=(out/x['name']).read_bytes();lf=b.replace(b'\r\n',b'\n')
 # A separate exact LF view is always present; no other newline or Unicode transformation.
 (out/(x['name']+'.LF')).write_bytes(lf)
put('current-input-manifest.json',dict(schema='header-source69-complete-finite-current-inputs-v1',count=len(inputs),inputs=inputs,
 LF_transform='only CRLF byte pairs replaced with LF; all other bytes preserved',source_expectations_frozen_before_candidate=True,
 prior_CLOSED82_native_lease_hash=sha(lease_b),prior_CLOSED82_native_manifest_hash=sha(manifest_b),
 prior_CLOSED82_write_performed=False,full_parent_content_opaque_hash_only=True,
 parent_full_RAW_sha256=sha(full),parent_fragment_range=[a,z],parent_full_body_reviewed=False))
put('input-read-process.json',dict(schema='header-source69-input-reader-v1',actual_pid=os.getpid(),read_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 current_candidate_inputs=4,source_regions=7,named_input_count=len(inputs),parent_statement_fragment_only=True,
 no_review68_or_decoder68_or_candidate_BODY_read=True,no_proof_search=True,no_SAU_claim=True))
put('lease.open.json',dict(schema='header-source69-open-lease-v1',owner='/root/independent_primary69',owned_path=str(out),status='OPEN',
 scope='independent source-first header-only admission',prior_CLOSED82_modified=False))
print(json.dumps(dict(actual_pid=os.getpid(),named_inputs=len(inputs),source_regions=7,
 expanded_header_RAW_sha256=next(x['RAW_sha256'] for x in inputs if x['name']=='candidate.header0-expanded.lean'),
 parent_fragment_RAW_sha256=sha(fragment),prior_CLOSED82_unchanged=True),sort_keys=True))
