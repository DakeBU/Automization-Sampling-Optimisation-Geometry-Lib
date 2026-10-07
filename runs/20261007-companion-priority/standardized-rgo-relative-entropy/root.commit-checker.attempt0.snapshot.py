from pathlib import Path
import subprocess,json
run=Path('runs/20261007-companion-priority/standardized-rgo-relative-entropy')
read=lambda p:json.loads(Path(p).read_text(encoding='utf-8'))
assert (run/'proved-local.json').exists()
assert read(run/'source.review.lease.json')['write_lease']=='CLOSED'
assert read(run/'reviewer.math.lease.json')['write_lease']=='CLOSED'
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()=='1e0818f1dc2d954a6355f4df1312f645f9e12494'
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
plan=read(run/'publication-plan.json');claim=read(run/'claim.json')
paths=list(claim['proposal']['proposed_files'])
paths += ['research-wiki/frontier-cells/'+x+'.json'for x in plan['active_cells']]
paths += ['research-wiki/semantic-roundtrip/audits/'+x+'.json'for x in plan['audit_ids']]
paths += ['website/content/'+folder+'/'+x+'.json'for folder in ['publications','declaration_lessons']for x in plan['slugs']]
paths += ['runs/substantive_advances.jsonl','proof-blueprints/standardized-rgo-relative-entropy.md']
paths += [p.as_posix()for p in run.rglob('*')if p.is_file()]
for name in ['gaussian-relative-entropy-preread','gaussian-lsi-t2-readiness']:
 other=run.parent/name
 assert json.loads((other/'lease.json').read_text(encoding='utf-8-sig'))['status']=='CLOSED'
 paths += [p.as_posix()for p in other.rglob('*')if p.is_file()]
paths += [p.as_posix()for p in run.parent.joinpath('gaussian-sqrt-density-domain').glob('remote-ci.1e0818f1*.json')]
paths=list(dict.fromkeys(paths));assert all(Path(p).is_file()for p in paths)
subprocess.run(['git','-c','core.autocrlf=false','add','-f','--pathspec-from-file=-','--pathspec-file-nul'],input=('\0'.join(paths)+'\0').encode(),check=True)
subprocess.run(['git','commit','-q','-m','Prove unique proximal witness and finite canonical entropy for the actual SPHMC RGO'],check=True)
print(subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip())
