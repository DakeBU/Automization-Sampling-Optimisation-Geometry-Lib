from pathlib import Path
import hashlib,json,os,subprocess,sys
r=Path('runs/20261007-companion-priority/pbps-actual-hazard-clock75');p=Path('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-hazard-clock.json');out=Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR'])
before=p.read_bytes();(out/'cell.before.exactraw.json').write_bytes(before);c=json.loads(before)
old='Source-first CLOSED53 finite retrieval and original CLOSED86 prospective plan; corrected Exp(1) API separately source-reviewed.'
new='Samplinglib source-first CLOSED53 finite retrieval and original CLOSED86 prospective plan; corrected Exp(1) API separately source-reviewed.'
assert c['shared_floor_audit']['searched'][0]==c['reuse_plan']['searched_existing'][0]==old
c['shared_floor_audit']['searched'][0]=c['reuse_plan']['searched_existing'][0]=new
p.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
with (out/'frontier.stdout.log').open('wb') as s,(out/'frontier.stderr.log').open('wb') as e:
 q=subprocess.Popen([sys.executable,'-B','-X','utf8','tools/astis_frontier_cells.py','check'],stdout=s,stderr=e);code=q.wait()
(out/'repair.json').write_text(json.dumps(dict(status='PROCESS_ONLY_RETRIEVAL_LABEL_REPAIR',actual_root_PID=os.getpid(),field_changes=['shared_floor_audit.searched[0]','reuse_plan.searched_existing[0]'],actual_frontier_PID=q.pid,exit_code=code,header_unchanged=True,mathematical_change=False,prior_negative_preserved=True),indent=2)+'\n',encoding='utf8',newline='\n');assert code==0
print('PASS75 exact retrieval-label repair; frontier PASS; sealed statement unchanged.')
