import datetime,gzip,hashlib,json,os,pathlib,subprocess,sys
out=pathlib.Path(__file__).resolve().parent
repo=out.parents[3]
transport=out.parent/'integration69'/'native-transport69'
native=out.parent/'independent-repository-reader69'
cache=repo/'.astis'/'reader69-transport-validation'
dst=cache/'complete-named-review-decision-input-payload.exactraw.json'
sha=lambda b:hashlib.sha256(b).hexdigest()
def filehash(p):
    h=hashlib.sha256();size=0
    with p.open('rb') as f:
        for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b);size+=len(b)
    return size,h.hexdigest()
def native_state():
    lease_raw=(native/'lease.final.json').read_bytes();manifest_raw=(native/'manifest.final.json').read_bytes()
    assert sha(lease_raw)=='9526ce7abb2b52e5a090dc33f60a8236bf1ad648d49f204b56bee746242184de'
    assert sha(manifest_raw)=='7f983589f3edaf4a148fcd456aa44c76b959f46eb474e143b609dd3e2cc05dff'
    lease=json.loads(lease_raw);manifest=json.loads(manifest_raw);assert lease['status']=='CLOSED_LAST'
    stats={}
    for e in manifest['entries']:
        p=native/e['name'];size,digest=filehash(p)
        assert size==e['RAW_bytes'] and digest==e['RAW_sha256'],e['name']
        st=p.stat();stats[e['name']]=dict(size=size,RAW_sha256=digest,mtime_ns=st.st_mtime_ns)
    assert len(stats)==333
    actual={p.relative_to(native).as_posix() for p in native.rglob('*') if p.is_file()}
    assert actual==set(stats)|{'manifest.final.json','lease.final.json'}
    for name in ['manifest.final.json','lease.final.json']:
        st=(native/name).stat();stats[name]=dict(size=st.st_size,RAW_sha256=sha((native/name).read_bytes()),mtime_ns=st.st_mtime_ns)
    return stats
assert not (out/'lease.final.json').exists()
before=native_state()
small_inputs=[]
for name in ['manifest.json','materialize-outside-native-tree.py','README.md']:
    b=(transport/name).read_bytes();(out/('input.'+name)).write_bytes(b)
    small_inputs.append(dict(path=(transport/name).as_posix(),snapshot='input.'+name,RAW_bytes=len(b),RAW_sha256=sha(b)))
m=json.loads((out/'input.manifest.json').read_bytes())
original=repo/m['original_path'];compressed=repo/m['transport_path']
assert original.resolve()==(native/'complete-named-review-decision-input-payload.json').resolve()
assert m['original_RAW_bytes']==167233478 and m['original_RAW_sha256']=='87b24e44b44993928d6ce9c511036e98d53ecbbbd5da126408362cb9af873605'
size,digest=filehash(compressed);assert size==m['transport_bytes']==51224320 and digest==m['transport_RAW_sha256']
h=hashlib.sha256();decoded_size=0
with gzip.open(compressed,'rb') as f:
    for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b);decoded_size+=len(b)
assert decoded_size==m['original_RAW_bytes'] and h.hexdigest()==m['original_RAW_sha256']
assert filehash(original)==(decoded_size,h.hexdigest())
assert decoded_size>100*1024*1024 and size<50*1024*1024
assert not dst.exists() and dst.resolve().is_relative_to(cache.resolve()) and not dst.resolve().is_relative_to(native.resolve())
ignored=subprocess.run(['git','check-ignore','--',dst.relative_to(repo).as_posix()],cwd=str(repo),capture_output=True)
(out/'git-check-ignore.stdout.log').write_bytes(ignored.stdout);(out/'git-check-ignore.stderr.log').write_bytes(ignored.stderr)
assert ignored.returncode==0,ignored.stderr.decode('utf-8',errors='replace')
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
p=subprocess.Popen([sys.executable,str(transport/'materialize-outside-native-tree.py'),str(dst)],cwd=str(repo),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
stdout,stderr=p.communicate()
(out/'materializer.stdout.log').write_bytes(stdout);(out/'materializer.stderr.log').write_bytes(stderr)
receipt=dict(schema='native-transport69-actual-materializer-terminal-v1',actual_pid=p.pid,actual_exit=p.returncode,
    foreground=True,completed=True,start_utc=start,end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    interpreter=sys.executable,python_version=sys.version,script=(transport/'materialize-outside-native-tree.py').as_posix(),
    output_path=dst.as_posix(),output_is_ignored_cache=True)
(out/'materializer.receipt.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n',encoding='utf-8')
assert p.returncode==0,stderr.decode('utf-8',errors='replace')
assert filehash(dst)==(decoded_size,h.hexdigest())
after=native_state();assert before==after
state_hash=sha(json.dumps(before,sort_keys=True,separators=(',',':')).encode('utf-8'))
decision=dict(schema='astis-independent-native-transport69-decision-v1',owner='/root/independent_primary69',
    verdict='ACCEPT_EXACT_GZIP_TRANSPORT_ONLY',actual_audit_pid=os.getpid(),
    original_RAW_bytes=decoded_size,original_RAW_sha256=h.hexdigest(),transport_RAW_bytes=size,transport_RAW_sha256=digest,
    original_native_lease_RAW_sha256=m['native_CLOSED_lease_RAW_sha256'],original_native_manifest_RAW_sha256=sha((native/'manifest.final.json').read_bytes()),
    old_native_count=335,old_native_all_RAW_hashes_verified_before_and_after=True,old_native_paths_sizes_hashes_mtimes_unchanged=True,
    native_pre_post_state_sha256=state_hash,small_named_inputs=small_inputs,
    independent_stream_decompression_compares_original=True,actual_materializer_receipt=receipt,
    materialized_RAW_path=dst.as_posix(),materialized_RAW_bytes=decoded_size,materialized_RAW_sha256=h.hexdigest(),
    materialized_only_under_ignored_astis_cache=True,no_large_payload_copy_in_owned_or_runs=True,
    GitHub_limit=dict(source='https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github',
        checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),hard_limit_bytes=104857600,warning_threshold_bytes=52428800,
        original_exceeds_hard_limit=True,gzip_below_warning_threshold=True),
    materializer_review='Resolves supplied fresh destination, rejects existing files and any destination inside original CLOSED native tree; Python3.12.14 satisfies Path.is_relative_to API. Actual run used the explicit ignored cache path.',
    exact_Git_exclusion_path=m['original_path'],exclusion_not_applied_by_this_reviewer=True,
    Git_RAW_object_identity_for_oversized_file=False,transport_representation_only=True,
    original_close_chronology_replayed=False,new_math_or_source_admission=False,canonical_old_native_Git_ledger_Goal_writes=False,
    remaining_truth_boundary='Transport integrity and ignored-cache materialization only. No Git commit/push, original Git RAW object, chronology replay or new mathematical/source/reader acceptance.')
(out/'decision.json').write_text(json.dumps(decision,sort_keys=True,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(actual_audit_pid=os.getpid(),verdict=decision['verdict'],materializer_actual_pid=p.pid,materializer_actual_exit=p.returncode,
    original_RAW_bytes=decoded_size,original_RAW_sha256=h.hexdigest(),transport_RAW_bytes=size,transport_RAW_sha256=digest,
    old_native_count=335,old_native_unchanged=True,output=dst.as_posix()),sort_keys=True))
