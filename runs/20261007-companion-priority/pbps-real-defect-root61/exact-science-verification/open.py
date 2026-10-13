from common import *
assert head()==SCI
freeze=J(R/'math-freeze.json'); verified=[matches(x) for x in freeze['inputs']]; assert len(verified)==27
files=git('diff-tree','--no-commit-id','--name-only','-r','-z',SCI).decode().split('\0'); files=[f for f in files if f]; assert len(files)==691,len(files)
entries=git('ls-tree','-rz',SCI,'--',*[]).split(b'\0'); allentries={}
for row in entries:
 if row:
  meta,name=row.split(b'\t',1); mode,typ,sha=meta.decode().split(); allentries[name.decode()]=(mode,typ,sha)
objs=[allentries[f][2] for f in files]
proc=subprocess.Popen(['git','cat-file','--batch'],cwd=ROOT,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
data,_=proc.communicate(('\n'.join(objs)+'\n').encode()); assert proc.returncode==0
i=0; rows=[]
for f in files:
 end=data.index(b'\n',i); header=data[i:end].split(); size=int(header[2]); blob=data[end+1:end+1+size]; i=end+size+2
 current=pin(ROOT/f); assert current['lf_sha256']==H(blob.replace(b'\r\n',b'\n')),(f,current)
 rows.append(dict(repository_path=f,git_mode=allentries[f][0],git_blob=allentries[f][2],git_bytes=len(blob),git_raw_sha256=H(blob),git_lf_sha256=H(blob.replace(b'\r\n',b'\n')),current=current))
W(P/'science.entries.json',dict(checked_commit=SCI,actual_catfile_PID=proc.pid,exit_code=proc.returncode,count=len(rows),entries=rows,all_current_git_LF_equal=True))
names=['math-freeze.json','proved-local.json','root.math61.adoption.json','root.decoder61.adoption.json','root.source61.adoption.json','publication-plan.json','source-review61/run.json','source-review61/lease.json','source-review61/native.receipt.json','anonymous-decoder/decoder-native-run.json','anonymous-decoder/CLOSED_LAST.json','independent-math61/run.json','independent-math61/lease.json','independent-math61/receipt.json']
W(P/'inputs.before.json',dict(checked_commit=SCI,actual_opener_PID=os.getpid(),freeze=pin(R/'math-freeze.json'),freeze_inputs=verified,native_inputs=[pin(R/n) for n in names],science_entries=pin(P/'science.entries.json'),ledger_before=snapshot(ROOT/'runs/substantive_advances.jsonl','ledger-before'),timing='Actual before independent focused compiler; all27 freeze originals and691 changed Git blobs compared without observer exception'))
W(P/'lease.open.json',dict(status='OPEN',actor=ACTOR,actual_PID=os.getpid(),checked_commit=SCI,compiler='NOT_STARTED',scope='Exact-science61 independent verification; ledger transition sole authorized canonical mutation'))
print('OPEN_PINS_PASS',len(verified),len(rows),SCI)
