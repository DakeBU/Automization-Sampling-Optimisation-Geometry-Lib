from pathlib import Path
import hashlib,json,os,subprocess
r=Path('runs/20261007-companion-priority/pbps-b4-corrector-perturbation72/integration72')
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
baseline=load(r/'before-generator-state.json');head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert head==baseline['head']
keep=set(baseline['keep']);changed=set(subprocess.check_output(['git','-c','core.autocrlf=false','diff','--name-only'],text=True).splitlines());extras=sorted(changed-keep)
assert not (set(extras)&set(baseline['preexisting_tracked_changes']))
assert all(p=='MANIFEST.md' or p.startswith(('agent-briefs/log_concave_sampling_6h_execution_pack.md','docs/assets/','research-wiki/external-lean-libraries/','research-wiki/lemma-dags/','research-wiki/retrieval-index/','research-wiki/sampling-sde-library/')) for p in extras)
newcards=sorted(set(subprocess.check_output(['git','ls-files','--others','--exclude-standard','research-wiki/sampling-sde-library/cards'],text=True).splitlines())-set(baseline['untracked_cards'])-keep)
log=(r/'module-graph-refresh/stdout.log').read_text(encoding='utf8').replace('\\','/')
assert all(p in log for p in newcards)
dest=r/'generator-sideeffects';dest.mkdir(exist_ok=False);rows=[]
for i,p in enumerate(extras):
 raw=Path(p).read_bytes();old=subprocess.check_output(['git','show',head+':'+p]);q=dest/f'{i:04d}.generated.exactraw.snapshot';h=dest/f'{i:04d}.HEAD.exactraw.snapshot'
 q.write_bytes(raw);h.write_bytes(old);assert Path(p).read_bytes()==raw;Path(p).write_bytes(old)
 rows.append(dict(path=p,action='RESTORE_PREVIOUSLY_CLEAN_HEAD_AFTER_EXACT_GENERATED_BACKUP',generated_backup=q.as_posix(),generated_RAW_sha256=sha(raw),HEAD_backup=h.as_posix(),HEAD_RAW_sha256=sha(old)))
for i,p in enumerate(newcards,len(rows)):
 source=Path(p).resolve();target=(dest/f'{i:04d}.generated-new-card.exactraw.snapshot').resolve();workspace=Path.cwd().resolve()
 assert source.is_relative_to(workspace) and target.is_relative_to(workspace)
 raw=source.read_bytes();source.rename(target)
 rows.append(dict(path=p,action='PRESERVE_UNUSED_NEW_GENERATED_CARD_IN_EXACT_BACKUP',generated_backup=target.relative_to(workspace).as_posix(),generated_RAW_sha256=sha(raw)))
# Canonical mutable generated views are cleaned before their independent reader seal.
trim=[]
for name in ['docs/module-graph.svg','docs/assets/astis_lean_arsenal_module_graph.svg','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCorrectorPerturbation.md','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.TechnicalLemmas.Analysis.HilbertCorrectorPerturbation.md']:
 p=Path(name);b=p.read_bytes();parts=b.splitlines(keepends=True);clean=b''.join(z.rstrip(b'\r\n').rstrip(b' \t')+(b'\r\n' if z.endswith(b'\r\n') else b'\n' if z.endswith(b'\n') else b'') for z in parts)
 if b!=clean:
  q=dest/('mutable-generated-'+sha(name.encode())+'.before.exactraw.snapshot');q.write_bytes(b);p.write_bytes(clean)
  trim.append(dict(path=name,before_RAW_sha256=sha(b),after_RAW_sha256=sha(clean),backup=q.as_posix(),only_trailing_ASCII_space_tab_removed=True))
out=dict(status='BOUNDED71_GENERATED_SCOPE_WITH_EXACT_BACKUPS',actual_PID=os.getpid(),tracked_generated_restored=len(extras),unused_new_generated_cards_preserved=len(newcards),rows=rows,mutable_generated_ASCII_trims=trim,canonical_Lean_source_review_unchanged=True,old_frontiers_and_untracked_cards_preserved=True)
(dest/'receipt.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
assert set(subprocess.check_output(['git','-c','core.autocrlf=false','diff','--name-only'],text=True).splitlines())<=keep
print('PASS72 generated scope retained exact relevant branch/card; restored',len(extras),'clean generated paths; preserved',len(newcards),'unused new cards; mutable ASCII trims',len(trim))
