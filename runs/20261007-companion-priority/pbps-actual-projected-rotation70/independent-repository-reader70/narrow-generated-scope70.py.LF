from pathlib import Path
import hashlib, json, os, subprocess
r = Path('runs/20261007-companion-priority/pbps-actual-projected-rotation70')
load = lambda p: json.loads(Path(p).read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
baseline = load(r/'resume-state70/receipt.json')
assert set(line[3:] for line in baseline['tracked_status'].splitlines()) == {'website/scripts/check_cross_domain_browser.py','website/scripts/inline_lean.py'}
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip() == 'c46af8a55e89419109f654c4553cf527993cbeed'
assert subprocess.check_output(['git','rev-parse','HEAD^'],text=True).strip() == baseline['head']
label_commit_paths = subprocess.check_output(['git','diff-tree','--no-commit-id','--name-only','-r','HEAD'],text=True).splitlines()
assert all(p == 'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-projected-rotation.json' or p.startswith(r.as_posix()+'/search-label-repair70/') for p in label_commit_paths)
keep = {'AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl','runs/substantive_advances.jsonl','docs/module-graph.svg','docs/assets/astis_lean_arsenal_module_graph.svg','research-wiki/sampling-sde-library/lean-leaf-module-graph.md','research-wiki/retrieval-index/astis-lean-arsenal-module-graph.json','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.ExampleCases.ProximalBPS.ActualProjectedRotation.md','website/scripts/inline_lean.py','website/scripts/check_cross_domain_browser.py','conversion-windows/ASTIS-SW-PBPS-2026.md'}
keep.update('research-wiki/frontier-cells/'+cid+'.json' for cid in load(r/'publication-plan.json')['active_cells'])
changed = set(subprocess.check_output(['git','-c','core.autocrlf=false','diff','--name-only'],text=True).splitlines())
extras = sorted(changed - keep)
assert extras and all(p == 'MANIFEST.md' or p.startswith(('agent-briefs/log_concave_sampling_6h_execution_pack.md','docs/assets/','research-wiki/external-lean-libraries/','research-wiki/lemma-dags/','research-wiki/retrieval-index/','research-wiki/sampling-sde-library/')) for p in extras)
newcards = subprocess.check_output(['git','ls-files','--others','--exclude-standard','research-wiki/sampling-sde-library/cards'],text=True).splitlines()
newcards = sorted(p for p in newcards if p not in keep)
generated_log = (r/'integration70/module-graph-refresh/stdout.log').read_text(encoding='utf8').replace('\\','/')
assert all(p in generated_log for p in newcards)
dest = r/'integration70/generator-sideeffects'; dest.mkdir(exist_ok=False)
rows = []
for i,p in enumerate(extras):
    raw = Path(p).read_bytes(); base = subprocess.check_output(['git','show','HEAD:'+p])
    q = dest/f'{i:04d}.generated.exactraw.snapshot'; q.write_bytes(raw)
    h = dest/f'{i:04d}.HEAD.exactraw.snapshot'; h.write_bytes(base)
    assert Path(p).read_bytes() == raw
    Path(p).write_bytes(base)
    rows.append(dict(path=p,action='RESTORED_CLEAN_BASELINE_AFTER_EXACT_GENERATED_BACKUP',generated_backup=q.as_posix(),generated_RAW_sha256=sha(raw),HEAD_backup=h.as_posix(),HEAD_RAW_sha256=sha(base)))
for i,p in enumerate(newcards,len(extras)):
    raw = Path(p).read_bytes(); q = dest/f'{i:04d}.generated-new-card.exactraw.snapshot'
    source = Path(p).resolve(); target = q.resolve(); workspace = Path.cwd().resolve()
    assert source.is_relative_to(workspace) and target.is_relative_to(workspace)
    source.rename(target)
    rows.append(dict(path=p,action='MOVED_UNUSED_TOOL_GENERATED_NEW_CARD_TO_EXACT_BACKUP',generated_backup=q.as_posix(),generated_RAW_sha256=sha(raw)))
handoff = Path('docs/companion-papers-handoff.md'); b = handoff.read_bytes()
(dest/'handoff.before-wording.exactraw.snapshot').write_bytes(b)
old = b'repair is a separate reviewed code change with fresh current browser checks due.'
assert b.count(old) == 1
handoff.write_bytes(b.replace(old,b'repair is a separate reviewed code change; fresh local browser checks passed. Remote70 CI remains pending.'))
payload = dict(status='BOUNDED70_GENERATED_SCOPE_WITH_EXACT_BACKUPS',actual_PID=os.getpid(),baseline_receipt=(r/'resume-state70/receipt.json').as_posix(),tracked_generated_restored=len(extras),unused_new_generated_cards_preserved=len(newcards),rows=rows,canonical_proof_source_review_cell_unchanged=True,shared_relevant_graph_and70_card_retained=True,old_frontiers_and_reader_content_preserved=True)
(dest/'receipt.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
assert set(subprocess.check_output(['git','-c','core.autocrlf=false','diff','--name-only'],text=True).splitlines()) <= keep
print(json.dumps({k:v for k,v in payload.items() if k!='rows'}))
