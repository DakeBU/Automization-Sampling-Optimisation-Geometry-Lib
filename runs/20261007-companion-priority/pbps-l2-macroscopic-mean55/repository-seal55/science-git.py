from common import *
entries=load(B/'exact-verification55/committed-inputs.json')['bindings'];assert len(entries)==1821
cp=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE);raw,_=cp.communicate(''.join(SCI+':'+e['path']+'\n' for e in entries).encode());assert cp.returncode==0;pos=0;checked=[]
for e in entries:
 end=raw.index(b'\n',pos);h=raw[pos:end].decode().split();size=int(h[2]);b=raw[end+1:end+1+size];pos=end+size+2
 assert h[0]==e['git_blob'] and size==e['git_bytes'] and sha(b)==e['git_raw_sha256'] and sha(b.replace(b'\r\n',b'\n'))==e['git_lf_sha256']
 checked.append(dict(path=e['path'],Git_blob=h[0],Git_raw_sha256=sha(b),Git_LF_sha256=sha(b.replace(b'\r\n',b'\n')),bytes=size))
assert pos==len(raw)
sync=load(B/'sync-before-integration55.json');assert sync['main_after']==git('rev-parse','origin/main')=='c05de12e6a8ca7af8ce2df8608836f8d4e90f617'
dump('science-git.json',dict(status='PASS',science_commit=SCI,integration_commit=HEAD,all1821_real_Git_blob_bindings=checked,count=1821,bindings_sha256=logical(checked),safe_fetch_native=pin(B/'sync-before-integration55.fetch.json'),sync_native=pin(B/'sync-before-integration55.json'),origin_main_unchanged=sync['main_after'],new_integration_CI_claim=False,prior54_CI_not_applied_to55=True))
print(json.dumps(dict(status='PASS',actual_science_Git_blobs=1821,origin_main=sync['main_after'],new55_CI_claim=False)))
