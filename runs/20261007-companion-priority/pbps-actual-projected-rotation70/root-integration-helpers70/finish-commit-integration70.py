from pathlib import Path
import gzip,hashlib,json,os,re,subprocess
r=Path('runs/20261007-companion-priority/pbps-actual-projected-rotation70');load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()=='c46af8a55e89419109f654c4553cf527993cbeed'
assert load(r/'root.repository70.adoption.json')['accepted_scoped_aggregate']
assert load(r/'root.generated-whitespace70.adoption.json')['accepted_finite_overlay']
plan=load(r/'publication-plan.json')
shared=['AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl','runs/substantive_advances.jsonl','docs/module-graph.svg','docs/assets/astis_lean_arsenal_module_graph.svg','research-wiki/sampling-sde-library/lean-leaf-module-graph.md','research-wiki/retrieval-index/astis-lean-arsenal-module-graph.json','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.ExampleCases.ProximalBPS.ActualProjectedRotation.md','website/scripts/inline_lean.py','website/scripts/check_cross_domain_browser.py','conversion-windows/ASTIS-SW-PBPS-2026.md']
shared+=['research-wiki/frontier-cells/'+cid+'.json' for cid in plan['active_cells']]
existing=set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines())
assert existing and all(p in shared or p.startswith(r.as_posix()+'/') for p in existing)
assert set(subprocess.check_output(['git','-c','core.autocrlf=false','diff','--name-only'],text=True).splitlines())<=set(shared)
for label in ['mandatory-astis-check-final','scope-graph-check-final','scope-site-check-final','scope-publication-final','scope-frontier-final','scope-contributor-final','scope-semantic-final','browser-full-current','python-regression-suite']:
 z=load(r/'integration70'/label/'receipt.json');assert z['terminal_closed'] and z['exit_code']==0,label
active=Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR']).resolve();assert active.is_relative_to((r/'integration70').resolve())
export=r/'root-integration-helpers70'
for name in ['finish-commit-integration70.py','trim-generated-whitespace70.py','adopt-generated-whitespace70.py']:
 p=Path('.astis/pbps-actual-rotation70')/name;q=export/name;assert p.is_file() and not q.exists();q.write_bytes(p.read_bytes())
paths=list(dict.fromkeys(shared+[p.as_posix() for p in r.rglob('*') if p.is_file() and not p.resolve().is_relative_to(active)]))
assert all(Path(p).stat().st_size<100*1024*1024 for p in paths)
assert not any('pbps-corrector-change-preproof71' in p or 'pbps-macro-root63' in p or 'independent-repository-reader69' in p for p in paths)
def stage(ps):subprocess.run(['git','-c','core.autocrlf=false','add','-f','--pathspec-from-file=-','--pathspec-file-nul'],input=('\0'.join(ps)+'\0').encode(),check=True)
stage(paths)
d=r/'integration70/final-staging-whitespace';d.mkdir(exist_ok=False)
q=subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'],capture_output=True);raw=q.stdout
hits=[dict(path=m[1],line=int(m[2]),kind=m[3]) for line in raw.decode('utf8').splitlines() if (m:=re.match(r'^(.+?):([0-9]+): (trailing whitespace|new blank line at EOF|space before tab in indent).*$',line))]
assert q.returncode in [0,2] and (q.returncode==0 or hits)
bad=sorted({h['path'] for h in hits});assert all(p.startswith(r.as_posix()+'/') for p in bad),bad
authored=[p for p in paths if p not in set(bad)]
for start in range(0,len(authored),64):subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check','--']+authored[start:start+64],check=True)
(d/'full-staged-immutable-negative.raw.gz').write_bytes(gzip.compress(raw,mtime=0))
(d/'diagnosis.json').write_text(json.dumps(dict(full_staged_exit=q.returncode,full_staged_whitespace_PASS=q.returncode==0,authored_complement_PASS=True,generated_assets_after_independent_whitespace_overlay_PASS=True,exact_immutable_raw_paths=[dict(path=p,RAW_sha256=sha(Path(p).read_bytes())) for p in bad],findings=hits,negative_RAW_sha256=sha(raw),prior_failed_preflight_preserved=True,active_observer_excluded=active.as_posix(),future71_not_staged=True),ensure_ascii=False,indent=2)+'\n',encoding='utf8')
stage([p.as_posix() for p in d.iterdir() if p.is_file()])
actual=set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines())
assert actual<=set(paths)|{p.as_posix() for p in d.iterdir() if p.is_file()}
subprocess.run(['git','commit','-q','-m','Integrate actual PBPS projected rotation and reviewed reader helpers'],check=True)
print(json.dumps(dict(integration_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),staged_files=len(actual),immutable_whitespace_findings=len(hits),full_staged_whitespace_PASS=q.returncode==0,authored_whitespace_PASS=True,full_paper=False)))
