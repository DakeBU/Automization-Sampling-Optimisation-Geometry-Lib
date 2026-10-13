from common import *
INTEGRATION='d1b150d6e59b3a9c398cc41e75a3330ef1915790'; assert git('rev-parse','HEAD').decode().strip()==INTEGRATION
files=[f for f in git('diff-tree','--no-commit-id','--name-only','-r','-z',INTEGRATION).decode().split('\0') if f]; assert len(files)==1386,len(files)
allentries={}
for row in git('ls-tree','-rz',INTEGRATION).split(b'\0'):
 if row:
  meta,name=row.split(b'\t',1); mode,typ,sha=meta.decode().split(); allentries[name.decode()]=(mode,typ,sha)
proc=subprocess.Popen(['git','cat-file','--batch'],cwd=ROOT,stdin=subprocess.PIPE,stdout=subprocess.PIPE); data,_=proc.communicate(('\n'.join(allentries[f][2] for f in files)+'\n').encode()); assert proc.returncode==0
rows=[]; pos=0
for f in files:
 end=data.index(b'\n',pos); header=data[pos:end].split(); size=int(header[2]); raw=data[end+1:end+size+1]; pos=end+size+2; current=pin(ROOT/f)
 assert current['lf_sha256']==H(raw.replace(b'\r\n',b'\n')),(f,current)
 rows.append(dict(repository_path=f,git_mode=allentries[f][0],git_blob=allentries[f][2],git_raw_bytes=len(raw),git_raw_sha256=H(raw),git_lf_sha256=H(raw.replace(b'\r\n',b'\n')),current=current))
W(P/'integration.entries.json',dict(checked_integration_commit=INTEGRATION,science_parent=SCI,count=len(rows),actual_catfile_PID=proc.pid,exit_code=proc.returncode,entries=rows,all_current_git_LF_equal=True))
inventory=[dict(path=f,mode=v[0],git_blob=v[2]) for f,v in allentries.items() if f.startswith('AutoSamplingTheory/') and f.endswith('.lean')]
W(P/'integration.production.inventory.json',dict(checked_commit=INTEGRATION,count=len(inventory),entries=inventory,truth='Exact tracked integration tree only; excludes future untracked/new62 and no whole working-tree inventory'))
metadata=[ROOT/'runs/substantive_advances.jsonl',ROOT/'research-wiki/frontier-cells/ASTIS-SHARED-l2-positive-real-square-root.json',ROOT/'research-wiki/frontier-cells/ASTIS-SW-PBPS-real-defect-root.json',ROOT/'docs/companion-papers-handoff.md',ROOT/'website/content/samplewiki_companion_frontiers.json',ROOT/'_site/data/underlying-lean-graph.json',R/'integration.notes.json',R/'visual.inspection.json']
shared=[ROOT/f for f in files if not f.startswith('runs/') and not f.startswith('research-wiki/frontier-cells/') and not f.endswith('.json')]
receipts=[]
dirs=['mandatory-astis-check','publication','contributor','semantic','frontier','python-compile','website-ci-build','site-check','official-graph-ci-output','graph-producer','graph-consumer','visual-capture61','generated-context-preservation','recordaggregate','publication-final-admin','contributor-final-admin','frontier-final-admin','official-graph-final-admin','graph-producer-final-admin','graph-consumer-final-admin']
for folder in dirs:
 p=R/'integration61'/folder/'receipt.json'
 if p.exists():
  receipts.append(p); q=J(p)
  for k in ['stdout','stderr']:
   v=q.get(k)
   if isinstance(v,dict) and v.get('path'): receipts.append(path(v['path']))
cards=[ROOT/f for f in files if '/cards/' in f and ('l2realsquareroot' in f.lower() or 'realdefectroot' in f.lower())]
chosen=list(dict.fromkeys(metadata+shared+receipts+cards)); snapshots=[snap(p,200+i) for i,p in enumerate(chosen)]
W(P/'phase2.inputs.json',dict(schema='native-repository-exposition61-phase2-inputs-v1',actor=ACTOR,actual_opener_PID=os.getpid(),checked_science_commit=SCI,checked_integration_commit=INTEGRATION,git_entry_count=len(rows),integration_entries=pin(P/'integration.entries.json'),production_inventory=pin(P/'integration.production.inventory.json'),qualified_original_snapshot_pairs=snapshots,count=len(snapshots),capture='Phase1 exact53 inputs/8PNG+DOM retained; current final admin graph separately exact snapshotted',timing='Actual final integration readback before root62 claim/newcanonical/body; all1386 changed entries compared current LF; no live observer inputs'))
print('PHASE2_FROZEN',len(rows),'integration entries',len(snapshots),'additional qualified snapshots',len(inventory),'tracked production files')
