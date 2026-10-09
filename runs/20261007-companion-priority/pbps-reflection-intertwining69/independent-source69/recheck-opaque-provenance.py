import datetime,hashlib,json,os,pathlib
out=pathlib.Path(__file__).resolve().parent
repo=pathlib.Path(r'E:\Samplinglib')
def sha(b):return hashlib.sha256(b).hexdigest()
def put(n,d):(out/n).write_text(json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
pre=repo/'runs/20261007-companion-priority/pbps-reflection-rotation-preproof69'
checks=[]
for name,expected_lease,expected_manifest,total in [
 ('independent-primary69','2d168d568a260f2cc18fba260a5bd7c1ac45cb41602f6a359df3d16b387aec93','1c2cb829368b83a04d59aad24859c5c724c381236347d6ae3b07a353173a68e9',82),
 ('independent-header-source69','a3b1cfecdc7d0bb7d9a33a8360658ed8ba9f2d8913e857ad0cdada008b28f4ee',None,84)]:
 p=pre/name;lease=(p/'lease.final.json').read_bytes();manifest=(p/'owned-manifest.json').read_bytes()
 assert sha(lease)==expected_lease
 if expected_manifest:assert sha(manifest)==expected_manifest
 m=json.loads(manifest);entries=m.get('regular_file_entries',m.get('entries'))
 assert entries is not None
 verified=[]
 for e in entries:
  b=(p/e['name']).read_bytes()
  assert len(b)==e['RAW_bytes'] and sha(b)==e['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==e['LF_sha256']
  verified.append(dict(name=e['name'],RAW_sha256=sha(b),opaque_hash_only=True))
 assert len(list(p.rglob('*')))==total and len(verified)==total-2
 checks.append(dict(path=str(p),lease_RAW_sha256=sha(lease),manifest_RAW_sha256=sha(manifest),owned_file_count=total,all_regular_hashes_verified=len(verified),old_verdicts_slots_deltas_repair_content_not_read=True,regular_names_and_hashes=verified))
primary=repo/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
b=primary.read_bytes();assert len(b)==1482128 and sha(b)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
r=json.loads((out/'current.focused.receipt.RAW.json').read_bytes());dependency_checks=[]
for e in r['inputs'][:5]:
 p=pathlib.Path(e['path']);b=p.read_bytes()
 assert len(b)==e['bytes'] and sha(b)==e['raw_sha256'] and sha(b.replace(b'\r\n',b'\n'))==e['lf_sha256']
 dependency_checks.append(dict(path=str(p),RAW_sha256=sha(b),opaque_hash_only=('ActualRootCommutation' in p.name or 'ReflectionL2' in p.name)))
put('opaque-prior-closure-and-compiler-provenance-recheck.json',dict(schema='source69-opaque-provenance-recheck-v1',actual_pid=os.getpid(),utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),old_closed_bundles=checks,primary=dict(path=str(primary),RAW_bytes=1482128,RAW_sha256='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'),focused_current_dependency_pins=dependency_checks,old_closed_bundles_unchanged=True,current_compilation_dependency_pins_match=True))
print(json.dumps(dict(actual_pid=os.getpid(),prior_owned_counts=[x['owned_file_count'] for x in checks],all_prior_regular_file_hashes_verified=sum(x['all_regular_hashes_verified'] for x in checks),current_compiler_dependency_count=len(dependency_checks),primary_RAW_sha256=sha(primary.read_bytes())),sort_keys=True))
