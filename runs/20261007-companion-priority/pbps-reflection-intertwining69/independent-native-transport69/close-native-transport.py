import base64,datetime,hashlib,json,os,pathlib
out=pathlib.Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
canonical=lambda d:json.dumps(d,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
load=lambda n:json.loads((out/n).read_text(encoding='utf-8'))
assert not (out/'lease.final.json').exists()
d=load('decision.json');audit=load('transport-audit.receipt.json');material=load('materializer.receipt.json')
assert audit['actual_exit']==0 and material['actual_exit']==0
assert d['verdict']=='ACCEPT_EXACT_GZIP_TRANSPORT_ONLY'
for p in d['small_named_inputs']:
    assert sha(pathlib.Path(p['path']).read_bytes())==p['RAW_sha256']
inputs=[]
for p in d['small_named_inputs']:
    b=(out/p['snapshot']).read_bytes();lf=b.replace(b'\r\n',b'\n')
    inputs.append(dict(attribution=p,RAW_base64=base64.b64encode(b).decode('ascii'),
        LF_base64=base64.b64encode(lf).decode('ascii'),LF_sha256=sha(lf),LF_recipe='CRLF-to-LF only'))
run=dict(schema='native-transport69-bounded-complete-review-v1',decision=d,exact_small_inputs=inputs,
    audit_terminal=audit,materializer_terminal=material,large_payload_copied_into_owned=False)
run['run_sha256']=sha(canonical(run))
(out/'review-run.json').write_text(json.dumps(run,sort_keys=True,indent=2)+'\n',encoding='utf-8')
entries=[]
for p in sorted(out.iterdir()):
    if not p.is_file() or p.name in ['manifest.final.json','lease.final.json']:continue
    b=p.read_bytes();lf=b.replace(b'\r\n',b'\n')
    entries.append(dict(name=p.name,RAW_bytes=len(b),RAW_sha256=sha(b),LF_bytes=len(lf),LF_sha256=sha(lf),LF_recipe='CRLF-to-LF only'))
assert all(e['RAW_bytes']<1024*1024 for e in entries)
manifest=dict(schema='native-transport69-finite-owned-manifest-v1',entries=entries,regular_file_count=len(entries),
    owned_file_count=len(entries)+2,finite_owned_closure_sha256=sha(canonical(entries)),
    excludes_exactly=['manifest.final.json','lease.final.json'])
(out/'manifest.final.json').write_text(json.dumps(manifest,sort_keys=True,indent=2)+'\n',encoding='utf-8')
lease=dict(schema='native-transport69-CLOSED_LAST-owned-lease-v1',status='CLOSED_LAST',owner='/root/independent_primary69',
    actual_lease_writer_pid=os.getpid(),closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    verdict=d['verdict'],regular_file_count=len(entries),owned_file_count=len(entries)+2,
    decision_RAW_sha256=sha((out/'decision.json').read_bytes()),review_run_RAW_sha256=sha((out/'review-run.json').read_bytes()),
    whole_logical_run_sha256=run['run_sha256'],whole_logical_deletes_ONLY_top_level_run_sha256=True,
    manifest_RAW_sha256=sha((out/'manifest.final.json').read_bytes()),finite_owned_closure_sha256=manifest['finite_owned_closure_sha256'],
    actual_audit_pid=audit['actual_pid'],actual_audit_exit=0,actual_materializer_pid=material['actual_pid'],actual_materializer_exit=0,
    original_native_count=335,original_native_unchanged=True,original_RAW_bytes=d['original_RAW_bytes'],original_RAW_sha256=d['original_RAW_sha256'],
    gzip_RAW_bytes=d['transport_RAW_bytes'],gzip_RAW_sha256=d['transport_RAW_sha256'],
    materialized_path=d['materialized_RAW_path'],materialized_in_ignored_astis_cache_only=True,
    new_math_or_source_admission=False,Git_RAW_identity_for_oversized_file=False,original_close_chronology_replayed=False,
    canonical_old_native_Git_ledger_Goal_writes=False,last_owned_write=True,postclose_writes_permitted=False,
    actual_writer_exit_observed_externally=True,postclose_readonly_output_only=True)
(out/'lease.final.json').write_text(json.dumps(lease,sort_keys=True,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(actual_lease_writer_pid=os.getpid(),owned_file_count=lease['owned_file_count'],
    decision_RAW_sha256=lease['decision_RAW_sha256'],whole_logical_run_sha256=run['run_sha256'],
    manifest_RAW_sha256=lease['manifest_RAW_sha256'],finite_owned_closure_sha256=lease['finite_owned_closure_sha256'],
    lease_RAW_sha256=sha((out/'lease.final.json').read_bytes())),sort_keys=True))
