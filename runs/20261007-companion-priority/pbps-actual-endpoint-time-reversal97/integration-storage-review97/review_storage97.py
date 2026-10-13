from pathlib import Path
import hashlib,json,gzip,subprocess
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;B=O.parent;I=B/'integration97';V=B/'exact-commit-verification97'
C='49fdfd309151b30f6371767dd74d698d440a8974';BASE='7089dfb0698c50d3ffd0180fb58d06bb32e5d7dd'
sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda p:json.loads(p.read_bytes())
def rel(p):return str(p).replace('\\','/').removeprefix('E:/Samplinglib/')
def info(p):
 p=R/rel(p);b=p.read_bytes();return dict(path=rel(p),raw_sha256=sha(b),bytes=len(b))
def write(n,v):
 p=O/n;assert not p.exists();p.write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
assert git('rev-parse','HEAD').decode().strip()==C and git('rev-parse',C+'^').decode().strip()==BASE
tree={s.split('\t',1)[1]:s.split()[2] for s in git('ls-tree','-r',C).decode().splitlines()};cache={}
def blob(p):
 p=rel(p)
 if p not in cache:cache[p]=git('cat-file','blob',tree[p])
 return cache[p]
correction=load(I/'raw-storage-correction97.json');rawpath=correction['raw_path'];rb=(R/rawpath).read_bytes()
assert sha(rb)==correction['raw_sha256']=='a40f16802817ecd8c6cf82dfcc6303d2fb5597a1a6b0e73482801ebe9568ef23'
assert rawpath not in tree
old=git('show',BASE+':'+rawpath);assert sha(old)==correction['archives'][0]['public_text_sha256']=='e53b0cc1e86b9cab444036f10771307d680a739c75b8b3f82f87f3eba4a49f52'
normal=b'\n'.join(x.rstrip(b' \t') for x in rb.replace(b'\r\n',b'\n').split(b'\n')).rstrip(b'\n')+b'\n';assert old==normal and old!=rb
z=correction['archives'][0];ab=blob(z['archive']);assert ab==git('show',BASE+':'+z['archive']) and sha(ab)==z['archive_sha256'] and gzip.decompress(ab)==rb
assert blob(I/'raw-storage-correction97.json')==(I/'raw-storage-correction97.json').read_bytes()
arch=load(I/'immutable-integration-RAW-archives97.json');assert blob(I/'immutable-integration-RAW-archives97.json')==(I/'immutable-integration-RAW-archives97.json').read_bytes()
byhash={};archive_rows=[]
for x in arch['files']:
 ab=blob(x['archive']);bb=gzip.decompress(ab)
 assert sha(ab)==x['archive_raw_sha256'] and sha(bb)==x['raw_sha256'] and bb==(R/x['raw_path']).read_bytes(),x['raw_path']
 if x['public_text_raw_sha256'] is not None:assert sha(blob(x['raw_path']))==x['public_text_raw_sha256']
 byhash[sha(bb)]=dict(archive=x['archive'],archive_raw_sha256=sha(ab));archive_rows.append(x)
# Build a hash-to-location index only over the committed evidence scopes already bound by97.
st=load(B/'science-staging97.json');scope=set(st['files'])|{p for p in tree if p.startswith(rel(V)+'/')}
for p in scope:
 if p not in tree:continue
 bb=blob(p)
 if p.endswith('.gz'):byhash.setdefault(sha(gzip.decompress(bb)),dict(archive=p,archive_raw_sha256=sha(bb)))
 else:byhash.setdefault(sha(bb),dict(snapshot=p))
closed=load(V/'closed-RAW-manifest97.json');assert info(V/'closed-RAW-manifest97.json')['raw_sha256']=='77d27a8543e5f86dcff9ae1344f14c9806ec9c457bb108d0212a592bb5059bd0'
resolved=[]
for x in closed['owned_artifacts']:
 assert info(x['path'])['raw_sha256']==x['raw_sha256'],('immutable verifier artifact changed',x['path'])
 assert x['raw_sha256'] in byhash,('verifier artifact not preserved in current commit',x['path'])
 resolved.append(dict(path=x['path'],raw_sha256=x['raw_sha256'],location=byhash[x['raw_sha256']]))
freeze=load(V/'current-input-freeze97.json');input_resolutions=[]
for x in freeze['exact_commit_matches']:
 p=x['path'];h=x['raw_sha256']
 if h in byhash:loc=byhash[h]
 elif x.get('archive'):
  ab=blob(x['archive']);assert sha(gzip.decompress(ab))==h;loc=dict(archive=x['archive'],archive_raw_sha256=sha(ab))
 elif x.get('snapshot'):
  assert sha(blob(x['snapshot']))==h;loc=dict(snapshot=x['snapshot'])
 elif p in tree and sha(blob(p))==h:loc=dict(snapshot=p)
 else:raise AssertionError(('science RAW not preserved in integration tree',x))
 input_resolutions.append(dict(path=p,raw_sha256=h,location=loc))
for x in freeze['local_pinned_or_excluded_inputs']:assert info(x['path'])['raw_sha256']==x['raw_sha256'],x['path']
collab=closed['preserved_collaborator_inputs'];assert len(collab)==21
for x in collab:assert info(x['path'])['raw_sha256']==x['raw_sha256'],x['path']
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualEndpointTimeReversal.lean';H=B.parent/'pbps-endpoint-time-reversal-preread97/Header97.lean';H98=B.parent/'pbps-prescribed-gibbs-survival-preread98/Header98.lean'
assert info(M)['raw_sha256']=='01816c27c8371ba9f81e24217ef7732b6c541066cb0b0f37e6494ffd8c58d27a' and blob(M)==git('show',BASE+':'+rel(M))==M.read_bytes()
assert info(H)['raw_sha256']=='2f27a049026ab398bfc85cecf1b2a450e8fef17c45e3a79e8b492c731343800b' and info(H98)['raw_sha256']=='50c6999fe069f4cf648832a804b71bb8e447b7a3aea0f0c42a836f81650c6ad0'
assert not git('diff','--name-only',BASE,C,'--',rel(H),rel(H)+'.gz',rel(H98),rel(H98)+'.gz').strip()
stage=load(I/'staged-scope97.json');assert rawpath in stage['paths'] and stage['sole_lane']=='ASTIS-SA-20261011-PBPSActualPrescribedPathDensity'
changes=git('diff','--name-status',BASE,C,'--',rawpath,z['archive']).decode().splitlines();assert changes==['D\t'+rawpath]
sn=O/'inputs';sn.mkdir();inputs=[]
for i,p in enumerate([I/'raw-storage-correction97.json',I/'immutable-integration-RAW-archives97.json',I/'staged-scope97.json',V/'closed-RAW-manifest97.json',V/'current-input-freeze97.json']):
 q=sn/(str(i).zfill(2)+'.'+p.name+'.exactraw');q.write_bytes(p.read_bytes());inputs.append(dict(**info(p),snapshot=rel(q)))
write('storage-review97.native.json',dict(kind='independent-bounded-integration-RAW-storage-review',reviewer='/root/exact_verifier96',decision='PASS_EXACT_INTEGRATION_STORAGE_PRESERVATION',checked_commit=C,science_commit=BASE,correction=info(I/'raw-storage-correction97.json'),removed_plain_blob=dict(path=rawpath,sha256=sha(old),was_normalized_not_original_RAW=True),original_working_RAW=info(rawpath),unchanged_committed_lossless_archive=dict(path=z['archive'],sha256=sha(ab) if False else sha(blob(z['archive']))),integration_archives_verified=len(archive_rows),exact_verifier_artifacts_preserved=resolved,science_input_RAW_resolutions=input_resolutions,all21collaborator_RAWs_preserved=True,production=info(M),Header97=info(H),prospectiveHeader98=info(H98),production_and_headers_unchanged=True,sole_stabilization_lane=stage['sole_lane'],no_science_audit_replay=True,no_VERIFIED_transition=True,no_shared_edits=True,scope='Storage-only acceptance at exact integration commit. Aggregate gate results, reader delivery, PR/push, merge, purification and whole-paper status are not newly certified by this storage audit.',inputs=inputs))
assert git('rev-parse','HEAD').decode().strip()==C
write('closed-RAW-storage-review97.native.json',dict(kind='closed-independent-integration-storage-review97',hash_recipe='SHA256 of exact bytes, without newline normalization',self_hash_omitted=True,checked_commit=C,files=[info(p) for p in sorted(O.rglob('*')) if p.is_file()]))
for n in ['storage-review97.native.json','closed-RAW-storage-review97.native.json']:print(json.dumps(info(O/n)))
