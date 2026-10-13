from pathlib import Path
import json,hashlib,gzip,subprocess,datetime,sys
R=Path('E:/Samplinglib');root=Path(__file__).parent;r=root/'ci-reader-order-repair86';sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'raw_sha256':sha(b),'bytes':len(b)}
def new(p,x):
 assert not p.exists(),p;p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
labels=['contributor-regressions','site-regressions','canonical','publication','contributor-after-exploration-metadata-audit','semantic','frontier','graph','python-compile','site-check']
for label in labels:
 d=json.loads((r/label/'receipt.json').read_bytes());assert d['exit_code']==0 and d['terminal_closed'],label
assert sha((R/'tools/tests/test_astis_publication.py').read_bytes())=='a40f288d05d1e63ca8b75f95e1ebf96f19d182adff1aaebcdbc7e87a3c7a2d73'
assert sha((R/'website/scripts/declaration_lessons.py').read_bytes())=='671dc0d177856b9c0f91f8acc6922f1e0e0cf57de5656b44cf8dbdea51cb9cdc'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()=='f62dca7500b1fa035ef7b377ac55e182ea3fd057'
assert not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=R,text=True).strip()
saved=json.loads((root.parent/'pbps-clock-tail-preread87/pre-fetch87.workspace-RAW.json').read_bytes())['tracked_modified'];assert len(saved)==21
for p,h in saved.items():assert sha((R/p).read_bytes())==h
p=root/'integration.notes.json';notes=json.loads(p.read_bytes())
notes['remote_ci_reader_test_repair86']={'original_integration_commit':'f62dca7500b1fa035ef7b377ac55e182ea3fd057','old_remote_workflows':'All three failed the same stale reader-order regression before Lean/site completion. No remote PASS claim.','exact_reviewed_test_sha256':'a40f288d05d1e63ca8b75f95e1ebf96f19d182adff1aaebcdbc7e87a3c7a2d73','independent_review':pin(r/'independent-review/independent-ci-review86.decision.json'),'local_gate_receipts':[pin(r/l/'receipt.json') for l in labels],'renderer_mathematics_source_audits_unchanged':True,'remote_rerun':'Pending new commit and push; terminal success not yet observed.'}
p.write_text(json.dumps(notes,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
doc=R/'docs/companion-papers-handoff.md';raw=doc.read_bytes();nl=b'\r\n' if b'\r\n' in raw else b'\n'
addition=('\nReader CI follow-up86: remote checks on f62dca7 exposed one stale test expecting\nLean statements after the mathematical proof. An independently reviewed exact\ntest repair restores statement adjacency coverage and adds actual86 full-Prop /\nproof-helper / folded-step regression. Local contributor regressions64, website\nregressions225, root Lean/Tests/ASTIS and current publication/semantic/frontier/\ngraph/site checks pass. Native failed remote logs and exact review are retained\nin86 ci-reader-order-repair86; rerun remote CI is pending the repair push.\nThis test-only repair changes no mathematics, source audit or completion status.\n').encode().replace(b'\n',nl)
assert b'Reader CI follow-up86:' not in raw;doc.write_bytes(raw+addition)
archives=[]
for p in sorted(r.rglob('*')):
 if p.is_file() and p.suffix in {'.log','.snapshot'}:
  a=Path(str(p)+'.gz');assert not a.exists();a.write_bytes(gzip.compress(p.read_bytes(),mtime=0));assert gzip.decompress(a.read_bytes())==p.read_bytes();archives.append({'native':pin(p),'archive':pin(a)})
new(r/'native-RAW-archives86.json',{'files':archives,'preservation':'Lossless gzip; native log/snapshot originals remain local; restore original named paths by decompression for RAW-manifest reproduction.'})
paths=['tools/tests/test_astis_publication.py','docs/companion-papers-handoff.md',(root/'integration.notes.json').relative_to(R).as_posix()]
for p in r.rglob('*'):
 if p.is_file() and '__pycache__' not in p.parts and p.suffix not in {'.log','.snapshot','.pyc'}:paths.append(p.relative_to(R).as_posix())
for name in ['propose_ci_reader_test86.py','apply_ci_reader_test86.py','check_ci_reader_repair86.py','commit_ci_reader_repair86.py']:paths.append((root/name).relative_to(R).as_posix())
paths=sorted(set(paths));assert not set(paths).intersection(saved);assert not any('tail-law87' in p or 'preread87' in p or p=='runs/substantive_advances.jsonl' for p in paths)
for i in range(0,len(paths),25):subprocess.run(['git','-c','core.autocrlf=false','add','--',*paths[i:i+25]],cwd=R,check=True)
actual=subprocess.check_output(['git','diff','--cached','--name-only'],cwd=R,text=True).splitlines();assert set(actual).issubset(paths)
for label,args in [('staged-diff-check',['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check']),('working-diff-check',['git','diff','--check'])]:
 q=subprocess.run(args,cwd=R,capture_output=True);assert q.returncode==0,(label,q.stdout)
 new(r/(label+'.receipt.json'),{'argv':args,'exit_code':q.returncode,'terminal_closed':True})
new(r/'staged-scope86.json',{'paths':actual,'collaborator_RAW21_preserved':True,'SAU87_exploration_excluded':True,'existing_single_stabilization_lane':True})
subprocess.run(['git','-c','core.autocrlf=false','add','--',*[str((r/n).relative_to(R)) for n in ['staged-diff-check.receipt.json','working-diff-check.receipt.json','staged-scope86.json']]],cwd=R,check=True)
subprocess.run(['git','commit','-q','-m','Align reader regression with adjacent Lean statements'],cwd=R,check=True)
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
assert subprocess.check_output(['git','show','HEAD:tools/tests/test_astis_publication.py'],cwd=R)==(R/'tools/tests/test_astis_publication.py').read_bytes()
for p,h in saved.items():assert sha((R/p).read_bytes())==h
q=subprocess.run(['git','push','origin','HEAD:codex/sphmc-standardized-rgo'],cwd=R,capture_output=True)
(r/'push-repair86.stdout.log').write_bytes(q.stdout);(r/'push-repair86.stderr.log').write_bytes(q.stderr)
new(r/'push-repair86.receipt.json',{'commit':commit,'exit_code':q.returncode,'terminal_closed':True,'remote_branch':'codex/sphmc-standardized-rgo'});assert q.returncode==0,q.stderr.decode(errors='replace')
q=subprocess.run(['git','ls-remote','origin','refs/heads/codex/sphmc-standardized-rgo'],cwd=R,capture_output=True)
(r/'push-repair86.remote-raw.log').write_bytes(q.stdout);assert q.returncode==0 and q.stdout.decode().split()[0]==commit
print('Exact reviewed CI repair committed and pushed:',commit,'; new remote CI terminal result pending; SAU87 remains separate exploring.')
