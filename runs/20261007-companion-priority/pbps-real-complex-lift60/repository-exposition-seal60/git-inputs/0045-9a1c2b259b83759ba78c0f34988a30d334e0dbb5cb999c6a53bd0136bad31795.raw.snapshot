import pathlib,subprocess,json,hashlib,os
ROOT=pathlib.Path('E:/Samplinglib');D=ROOT/'runs/20261007-companion-priority/pbps-real-complex-lift60/exact-science-verification';SCI='0a77416f5ec38702c46ec1358966b9dd4846c8d3'
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
names=[x.decode() for x in subprocess.check_output(['git','diff-tree','--no-commit-id','--name-only','-r','-z',SCI],cwd=ROOT).split(b'\0') if x]
b=subprocess.check_output(['git','cat-file','--batch'],input=('\n'.join(SCI+':'+x for x in names)+'\n').encode(),cwd=ROOT);offset=0;bad=[]
for i,rel in enumerate(names):
 end=b.index(b'\n',offset);meta=b[offset:end].decode().split();n=int(meta[2]);blob=b[end+1:end+1+n];offset=end+1+n+1;current=(ROOT/rel).read_bytes()
 if sha(blob.replace(b'\r\n',b'\n'))!=sha(current.replace(b'\r\n',b'\n')):
  gp=D/(str(i)+'.science-blob.exactraw.snapshot');cp=D/(str(i)+'.current-runtime.exactraw.snapshot');gp.write_bytes(blob);cp.write_bytes(current)
  bad.append(dict(original_path=(ROOT/rel).as_posix(),git_oid=meta[0],Git_exact_snapshot=pin(gp),current_exact_snapshot=pin(cp)))
q=dict(actual_PID=os.getpid(),science_entries=len(names),exact_mismatches=bad,earlier_exit_tool='ea6d33',no_compiler=True,no_transition=True,inline_shell_parse_negative_tool='8eaa53',inline_shell_parse_exit=1)
(D/'science-git-negative.json').write_bytes((json.dumps(q,indent=2)+'\n').encode());print(json.dumps(q),flush=True)
