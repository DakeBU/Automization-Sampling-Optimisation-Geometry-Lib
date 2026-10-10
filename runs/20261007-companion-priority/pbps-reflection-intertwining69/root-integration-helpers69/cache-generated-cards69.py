from pathlib import Path
import hashlib,json,subprocess,sys
root=Path.cwd().resolve();r=Path('runs/20261007-companion-priority/pbps-reflection-intertwining69');cache=root/'.astis/pbps-sharp-energy68/generated-card-cache69';cache.mkdir(exist_ok=False)
sys.path.insert(0,str(root/'tools'));import astis
records={x['module']:x for x in astis.lean_module_records()};raw=subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z','--','research-wiki/sampling-sde-library/cards']);paths=[x.decode() for x in raw.split(b'\0') if x];moved=[];skipped=[]
sha=lambda b:hashlib.sha256(b).hexdigest()
for name in paths:
 p=(root/name).resolve();assert p.is_relative_to(root) and p.parent==root/'research-wiki/sampling-sde-library/cards';module=p.stem
 if module not in records:skipped.append(name);continue
 data=p.read_bytes();expected=astis.arsenal_module_card_text(records[module]).encode()
 if data.replace(b'\r\n',b'\n')!=expected.replace(b'\r\n',b'\n'):skipped.append(name);continue
 dest=(cache/p.name).resolve();assert dest.is_relative_to(cache.resolve()) and not dest.exists();p.rename(dest);assert dest.read_bytes()==data;moved.append(dict(original=name,cache=dest.as_posix(),raw_sha256=sha(data),bytes=len(data),reason='Exact root-generator output from known current source inventory; original starting tree had no untracked module cards. Reversible cache retention, no deletion.'))
manifest=dict(moved=moved,skipped=skipped,all_targets_resolved_inside_workspace=True,kept_one_enriched69_card=True,no_Git_or_Lean_changes=True)
(cache/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');(r/'integration69/generated-card-cache69.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');print('Retained',len(moved),'exact root-generated untracked cards in reversible ignored cache; skipped',len(skipped),'nonmatching files. Tracked source/canonical cards untouched.')
