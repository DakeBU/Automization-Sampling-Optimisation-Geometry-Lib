from pathlib import Path
import hashlib,json,subprocess,os,gzip,re
root=Path.cwd();r=Path('runs/20261007-companion-priority/pbps-ambient-adjoint66');pre=Path('runs/20261007-companion-priority/pbps-ambient-adjoint-preproof66');load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()=='a115115d42b3fa2b67885d87fe4d5300af36fcd1'
assert load(r/'root.exact-verification66.adoption.json')['native_verified'] and load(r/'visual.inspection.json')['viewed_by_root']
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
for label in ['mandatory-astis-check-final','publication-final-admin','frontier-final-admin','contributor-final-admin','semantic','local-site-check-final','cell-graph-check-actual','reader-copy-download']:
 x=load(r/'integration66'/label/'receipt.json');assert x['terminal_closed'] and x['exit_code']==0,label
plan=load(r/'publication-plan.json')
shared=['AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl','runs/substantive_advances.jsonl','runs/substantive_discoveries.jsonl','docs/module-graph.svg','docs/assets/astis_lean_arsenal_module_graph.svg','research-wiki/sampling-sde-library/lean-leaf-module-graph.md','research-wiki/retrieval-index/astis-lean-arsenal-module-graph.json','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.ExampleCases.ProximalBPS.AmbientAdjointCorrector.md']+['research-wiki/frontier-cells/'+cid+'.json' for cid in plan['active_cells']]
changed=set(subprocess.check_output(['git','-c','core.autocrlf=false','diff','--name-only'],text=True).splitlines());assert changed<=set(shared),changed-set(shared)
active=Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR']).resolve();assert active.is_relative_to((r/'integration66').resolve())
export=r/'root-integration-helpers66';export.mkdir(exist_ok=False)
for p in Path('.astis/pbps-ambient-adjoint66').iterdir():
 if p.is_file() and p.suffix in ['.py','.mjs']:(export/p.name).write_bytes(p.read_bytes())
(export/'source-retention.json').write_text(json.dumps(dict(scope='Helper sources retained; execution separately bound by foreground receipts.',active_observer_excluded=active.as_posix()),indent=2)+'\n',encoding='utf-8',newline='\n')
paths=list(dict.fromkeys(shared+[p.as_posix() for folder in [r,pre] for p in folder.rglob('*') if p.is_file() and not p.resolve().is_relative_to(active)]))
assert all(Path(p).is_file() and Path(p).stat().st_size<100*1024*1024 for p in paths)
assert not any('pbps-first-corrector-energy-preproof67' in p or 'pbps-macro-root63/exact-science-verification/inputs/0446.exactraw.snapshot' in p or Path(p).resolve().is_relative_to(active) for p in paths)
def stage(ps):subprocess.run(['git','-c','core.autocrlf=false','add','-f','--pathspec-from-file=-','--pathspec-file-nul'],input=('\0'.join(ps)+'\0').encode(),check=True)
stage(paths);d=r/'integration66/staging-whitespace';d.mkdir(exist_ok=False)
q=subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'],capture_output=True);raw=q.stdout;hits=[]
for line in raw.decode('utf-8').splitlines():
 m=re.match(r'^(.+?):([0-9]+): (trailing whitespace|new blank line at EOF|space before tab in indent).*$',line)
 if m:hits.append(dict(path=m[1],line=int(m[2]),kind=m[3]))
assert q.returncode in [0,2] and (q.returncode==0 or hits)
bad=sorted({x['path'] for x in hits})
for p in bad:assert p.startswith(tuple(f.as_posix()+'/' for f in [r,pre])),p
authored=[p for p in paths if p not in set(bad)]
for start in range(0,len(authored),64):subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check','--']+authored[start:start+64],check=True)
(d/'full-staged-immutable-negative.raw.gz').write_bytes(gzip.compress(raw,mtime=0));(d/'diagnosis.json').write_text(json.dumps(dict(full_staged_exit=q.returncode,full_staged_called_PASS=q.returncode==0,exact_immutable_raw_paths=[dict(path=p,raw_sha256=sha(Path(p).read_bytes())) for p in bad],findings=hits,negative_RAW_sha256=sha(raw),authored_complement_exit=0,no_folder_exclusion=True,active_observer_excluded=active.as_posix(),future67_not_staged=True),ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
stage([p.as_posix() for p in d.iterdir() if p.is_file()]);actual=set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines());assert actual<=set(paths)|{p.as_posix() for p in d.iterdir() if p.is_file()}
subprocess.run(['git','commit','-q','-m','Integrate verified PBPS ambient adjoint and centered corrector geometry'],check=True)
print(json.dumps(dict(integration_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),staged_files=len(actual),immutable_native_whitespace_findings=len(hits),authored_whitespace_PASS=True,full_staged_whitespace_PASS=q.returncode==0,future67_not_staged=True,full_paper=False)))
