from pathlib import Path
import gzip, hashlib, json, os, subprocess
root=Path.cwd();r=root/'runs/20261007-companion-priority/pbps-centered-root64';d=r/'repository-exposition64'
load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
run,lease,review=[load(d/n) for n in ['run.json','lease.json','review.json']]
assert lease['status']=='CLOSED_LAST'
assert run['checked_commit']==lease['checked_commit']==review['checked_commit']=='0aef19ca2711159eeaec86d42c9be142a94fa402'
assert sha(can({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==lease['whole_logical_run_sha256']=='310311b4b9712e49a31c6cdb86800b2328c954e58c260fecdfd0e214eceaa80c'
assert run['full_review']==review and review['status']=='ACCEPTED_BOUNDED_WITH_READER_AND_STALE_METADATA_DEBT'
raw=(d/'named-reader-review.payload.json').read_bytes()
assert raw==(d/'review.json').read_bytes()
assert sha(raw)==lease['distinct_COMPLETE_named_RAW_review_sha256']=='11ee01a2773e9de054ce6c521fe68a6e91a4e41b072f59cef1db00ff2b3e9cba'
assert sha((d/'lease.json').read_bytes())=='984fea950100f0d99c95333847e89b99340ddba50b2e8a9bff0d31defbdd2d0c'
def check(x):
 b=Path(x['path']).read_bytes();assert sha(b)==x['raw_sha256'],x['path']
 if 'lf_sha256' in x:assert sha(b.replace(b'\r\n',b'\n'))==x['lf_sha256']
 if 'raw_bytes' in x:assert len(b)==x['raw_bytes']
 return b
owned=lease['complete_owned_output_manifest_after_actual_readback']
for x in owned:check(x)
assert {Path(x['path']).resolve() for x in owned}|{(d/'lease.json').resolve()}=={p.resolve() for p in d.rglob('*') if p.is_file()}
assert len(owned)+1==45
for x in load(d/'checker-correction64.json')['finite_exact_own_history_maps']:
 check(x['explicit_lossless_gzip']);h=hashlib.sha256();n=0
 with gzip.open(x['explicit_lossless_gzip']['path'],'rb') as f:
  while True:
   b=f.read(1048576)
   if not b:break
   h.update(b);n+=len(b)
 assert h.hexdigest()==x['original']['raw_sha256'] and n==x['original']['raw_bytes']
 assert not Path(x['original']['path']).exists()
for label in ['independent-check-v4','native-finalizer','native-readback']:
 x=load(d/label/'receipt.json');assert x['exit_code']==0 and x['terminal_closed'];check(x['stdout']);check(x['stderr'])
proc=subprocess.run([os.sys.executable,'-B',str(d/'native64.py'),'postclose'],cwd=root,capture_output=True)
assert proc.returncode==0,proc.stderr.decode(errors='replace')
terminal=json.loads(proc.stdout);assert terminal['owned_files']==45 and terminal['no_postclose_owned_writes']
out=r/'root.repository-exposition64.adoption.json';assert not out.exists()
out.write_text(json.dumps(dict(status=review['status'],actual_adopter_pid=os.getpid(),checked_commit=run['checked_commit'],native_whole_logical_run_sha256=run['run_sha256'],distinct_complete_RAW_review_sha256=sha(raw),native_owned_files=45,root_read_only_postclose=terminal,stale_metadata_debt=lease['stale_metadata_debt'],remaining_reader_debt=review['visual_review']['debts'],VERIFIED_transition=False,full_ExpositionSeal_PURIFIED_main_live_Goal=False),ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS CLOSED_LAST INT64 repository/reader:45 exact owned files, archives streamed, terminal readback, bounded debt retained.')
