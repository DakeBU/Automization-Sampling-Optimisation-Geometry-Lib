from pathlib import Path
import subprocess,json,re,difflib,hashlib
r=Path('runs/20261007-companion-priority/pbps-countable-endpoint-preread105/upstream-reconciliation105');s=r/'normalized-merge'
ps=['AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests.lean','Tests/Basic.lean','runs/substantive_advances.jsonl','runs/substantive_discoveries.jsonl']
rows=[]
for i,p in enumerate(ps):
 if i<3:
  b=(s/f'{i}.candidate').read_bytes()
  if i==2:
   pattern=rb'<<<<<<<[^\n]*\nexample : TechnicalLemmas.formalizedTechnicalLemmaCount = 555 := by native_decide\n=======\nexample : TechnicalLemmas.formalizedTechnicalLemmaCount = 489 := by native_decide\n>>>>>>>[^\n]*\n'
   b,n=re.subn(pattern,b'example : TechnicalLemmas.formalizedTechnicalLemmaCount = 556 := by native_decide\n',b);assert n==1
 else:
  base,ours,theirs=[(s/f'{i}.stage{n}.raw').read_bytes().replace(b'\r\n',b'\n') for n in (1,2,3)]
  assert theirs.startswith(base)
  assert all(t in ('equal','insert') for t,*_ in difflib.SequenceMatcher(None,base.splitlines(),ours.splitlines(),autojunk=False).get_opcodes())
  tail=theirs[len(base):];assert all(x not in ours.splitlines() for x in tail.splitlines())
  b=ours+tail
  if i==4:
   original_base,original_ours,original_theirs=[(s/f'{i}.stage{n}.raw').read_bytes() for n in (1,2,3)]
   assert original_theirs.startswith(original_base)
   b=original_ours+original_theirs[len(original_base):]
  for x in b.splitlines():json.loads(x)
 assert b'<<<<<<<' not in b and b'>>>>>>>' not in b
 Path(p).write_bytes(b);rows.append({'path':p,'raw_sha256':hashlib.sha256(b).hexdigest()})
subprocess.run(['git','-c','core.autocrlf=false','-c','core.fscache=false','add','--',*ps],check=True)
assert not subprocess.check_output(['git','diff','--name-only','--diff-filter=U']).strip()
(r/'resolution105.json').write_text(json.dumps({'policy':'LF-normalized three-way merge; preserve both independent append tails and all historical events; Registry count 555+1 sphere=556','files':rows},indent=2)+'\n')
print('Five conflicts resolved; upstream sphere and all PBPS contributions retained; merge not committed yet.')
