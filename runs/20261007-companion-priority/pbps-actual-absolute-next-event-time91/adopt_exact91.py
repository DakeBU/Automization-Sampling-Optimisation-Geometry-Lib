from pathlib import Path
import hashlib,json,subprocess,datetime
R=Path('E:/Samplinglib');r=Path(__file__).parent
v=r/'exact-commit-verification91'; sha=lambda b:hashlib.sha256(b).hexdigest()
science='d62f7b2c89e749953a36d8922124865a4651e55e'
expected={'verified.json':'55d4172220ef64fe4d14567d73a322e0daafe711bdbf859fb4efd2a462c0147e','admission91.json':'82b4fe85dd56520b05457ccf36c8146350e873eabf88ec0bc2881ba181732f4e','closed-RAW-manifest91.json':'f141c62418d5f03ca6744f31eb47e3ee4c4a9e680c04b6fbee0bc0f1c3a6b522'}
for n,h in expected.items(): assert sha((v/n).read_bytes())==h,n
m=json.loads((v/'closed-RAW-manifest91.json').read_bytes());a=json.loads((v/'admission91.json').read_bytes())
for d in m['owned_artifacts']+m['preserved_collaborator_inputs']+[a['cell'],a['ledger']]:
 b=(R/d['path']).read_bytes();assert sha(b)==d['raw_sha256'],d['path'];assert len(b)==d['bytes']
tree={}
for line in subprocess.check_output(['git','ls-tree','-rz',science],cwd=R).split(b'\0'):
 if line:
  meta,name=line.split(b'\t',1);tree[name.decode()]=meta.split()[2].decode()
for d in m['checked_science_inputs']:
 if d.get('binding')=='git-blob':
  b=subprocess.check_output(['git','cat-file','blob',tree[d['path']]],cwd=R)
  assert sha(b)==d['git_blob_raw_sha256'],d['path']
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==science
data=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),science_commit=science,status='adopted independent exact-commit verification',native_hashes=expected,owned_artifact_count=len(m['owned_artifacts']),preserved_collaborator_count=len(m['preserved_collaborator_inputs']),checked_science_input_count=len(m['checked_science_inputs']),verified_transition_by=a['verifier_id'],root_did_not_self_verify=True,aggregate='pending',reader_visual='pending',merged=False,purified=False,Goal_complete=False)
(r/'root.exact91.adoption.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8',newline='\n')
out=r/'preintegration-current91';out.mkdir(exist_ok=False)
for label,args in [('status',['status','--porcelain=v1']),('branch',['branch','--show-current']),('head',['rev-parse','HEAD'])]:
 (out/(label+'.txt')).write_bytes(subprocess.check_output(['git',*args],cwd=R))
(out/'frontier.json').write_bytes((R/a['cell']['path']).read_bytes())
q=subprocess.run(['git','fetch','origin'],cwd=R,capture_output=True)
(out/'fetch.stdout.log').write_bytes(q.stdout);(out/'fetch.stderr.log').write_bytes(q.stderr)
assert q.returncode==0
print(json.dumps(data));print('Fetched; no working-branch mutation.')
