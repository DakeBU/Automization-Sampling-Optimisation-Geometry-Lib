from pathlib import Path
import hashlib,json
r=Path(__file__).parent;old=r.parent/'pbps-actual-conditional-next-wait-survival88'
changes=[]
for name in ['commit_science','push_science']:
 source=old/(name+'88.py');p=r/(name+'89.py');assert not p.exists()
 s=source.read_text(encoding='utf8')
 for a,b in [('local88','local89'),('checks88','checks89'),('source88','source89'),('math88','math89'),('local88','local89'),('science88','science89'),('archives88','archives89'),('exclusions88','exclusions89'),('staging88','staging89'),('whitespace88','whitespace89'),('new88','new89'),('SCIENCE88','SCIENCE89'),('conditional-next-wait-preread88','conditional-next-wait-density-preread89'),('pre-fetch88','pre-fetch89'),('ActualConditionalNextWaitSurvival','ActualConditionalNextWaitDensity'),('actual-conditional-next-wait-survival','actual-conditional-next-wait-density'),('2f509ce49343d349f7a9fb21d2f7b1697c1a6de942353f6cd8ff16d522911569','36813b659cbdbb4b31c6300abd1300858d42afe683046b8c06ff9c22806e8e37'),('history-dependent conditional next-wait survival','conditional finite next-wait density')]:
  s=s.replace(a,b)
 if name=='commit_science':
  s=s.replace(",'runs/20261007-companion-priority/pbps-actual-finite-history-tail-law87/preread88.py'",'')
  s=s.replace("private_paths=[p.as_posix() for folder in [r,pre]", "folders=[r,pre,Path('runs/semantic-decoder-inputs/round89'),Path('runs/semantic-decoder-outputs/round89')]\nprivate_paths=[p.as_posix() for folder in folders")
  s=s.replace('for folder in [r,pre]:','for folder in folders:')
 p.write_text(s,encoding='utf8',newline='\n')
 changes.append(dict(path=p.as_posix(),template=source.as_posix(),template_RAW_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),status='PREPARED_NOT_EXECUTED_REQUIRES_NATIVE_ADMISSION_AND_GATES'))
(r/'commit-helper89-provenance.json').write_text(json.dumps(changes,indent=2)+'\n',encoding='utf8',newline='\n')
print('Prepared bounded owned-file commit/push helpers; not executed.')
