from pathlib import Path
import hashlib,json,os,subprocess
r=Path('runs/20261007-companion-priority/pbps-actual-bounce-rate74/integration74');load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
b=load(r/'before-generator-state.json');assert b['head']==subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
failed=load(r/'narrow-generated-scope/receipt.json');assert failed['exit_code']==1 and not (r/'generator-sideeffects').exists()
row=json.loads((r/'narrow-generated-scope/stdout.log').read_text(encoding='utf8').splitlines()[0]);paths=row['unsupported'];assert len(paths)==10
log=(r/'module-graph-refresh/stdout.log').read_text(encoding='utf8').replace('\\','/')
out=r/'generator-line-ending-diagnosis';out.mkdir(exist_ok=False);(out/'failed-scope-helper.exactraw.py').write_bytes(Path('.astis/pbps-bounce74/narrow-generated-scope74.py').read_bytes())
rows=[]
for i,p in enumerate(paths):
 assert p not in b['preexisting_tracked_changes'] and p not in b['keep'] and p in log,p
 current=Path(p).read_bytes();old=subprocess.check_output(['git','show',b['head']+':'+p]);assert current!=old and current.replace(b'\r\n',b'\n')==old.replace(b'\r\n',b'\n'),p
 a=out/f'{i}.generated.exactraw.snapshot';c=out/f'{i}.HEAD.exactraw.snapshot';a.write_bytes(current);c.write_bytes(old)
 rows.append(dict(path=p,generated_RAW_sha256=sha(current),HEAD_RAW_sha256=sha(old),common_LF_sha256=sha(old.replace(b'\r\n',b'\n')),generated_backup=a.as_posix(),HEAD_backup=c.as_posix(),in_explicit_generator_stdout=True,preexisting_tracked_change=False,only_CRLF_pairs_differ=True))
for z in rows:
 p=Path(z['path']);assert sha(p.read_bytes())==z['generated_RAW_sha256'];p.write_bytes(Path(z['HEAD_backup']).read_bytes())
(out/'diagnosis.json').write_text(json.dumps(dict(status='EXACT_TEN_GENERATOR_CRLF_ONLY_SIDE_EFFECTS_RESTORED_WITH_RAW_BACKUPS',actual_PID=os.getpid(),negative_PID=failed['actual_foreground_PID'],negative_EXIT=1,rows=rows,broad_allowlist_changed=False,scope_helper_unchanged=True,canonical_Lean_source_metadata_reviews_unchanged=True,collaborator_files_preserved=True,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS74 ten explicit generator-only CRLF differences diagnosed and exact clean HEAD restored; failed scope helper unchanged.')
