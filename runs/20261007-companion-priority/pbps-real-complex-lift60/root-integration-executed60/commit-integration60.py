from pathlib import Path
import gzip,hashlib,json,re,subprocess,os
r=Path('runs/20261007-companion-priority/pbps-real-complex-lift60');load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()=='0a77416f5ec38702c46ec1358966b9dd4846c8d3'
assert load(r/'root.exact-verification60.adoption.json')['native_verified'] and load(r/'visual.inspection.json')['viewed_by_root']
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
plan=load(r/'publication-plan.json');shared=['AutoSamplingTheory/TechnicalLemmas.lean','AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.TechnicalLemmas.Measure.L2RealComplexOperator.md','Tests.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl','runs/substantive_advances.jsonl','docs/module-graph.svg','docs/assets/astis_lean_arsenal_module_graph.svg','research-wiki/sampling-sde-library/lean-leaf-module-graph.md','research-wiki/retrieval-index/astis-lean-arsenal-module-graph.json','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.ExampleCases.ProximalBPS.DefectComplexLift.md']+['research-wiki/frontier-cells/'+x+'.json' for x in plan['active_cells']]
changed=set(subprocess.check_output(['git','diff','--name-only'],text=True).splitlines());assert changed<=set(shared)|{'runs/20261007-companion-priority/pbps-real-complex-lift-preproof60/commit-science60/stdout.log'},(changed-set(shared))
for name in plan['active_cells']:assert load('research-wiki/frontier-cells/'+name+'.json')['evidence']['serialized_shared_gate']['status']=='PASS'
for label in ['mandatory-astis-check','publication-final-admin','contributor-final-admin','frontier-final-admin','semantic','python-compile','website-ci-build','official-graph-ci-output','official-graph-final-admin','graph-producer','graph-consumer','site-check','science-push']:assert load(r/'integration60'/label/'receipt.json')['exit_code']==0,label
assert load(r/'integration60/tracked-whitespace-preserved/diagnosis.json')['authored_complement_exit']==0
export=r/'root-integration-executed60';export.mkdir(exist_ok=False)
for name in ['adopt-exact60.py','integrate60.py','integration-gate60.py','preserve-integration-newlines60.py','preserve-generated-context60.py','inspect-cdp60.mjs','record-integration60.py','cache-generated-cards60.py','commit-integration60.py']:(export/name).write_bytes((Path('.astis/pbps-real-complex-lift60')/name).read_bytes())
preproof=Path('runs/20261007-companion-priority/pbps-real-complex-lift-preproof60');active=Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR']).resolve();assert active.is_relative_to(r.resolve())
shared+=['runs/20261007-companion-priority/pbps-real-complex-lift-preproof60/commit-science60/stdout.log']
paths=list(dict.fromkeys(shared+[p.as_posix() for folder in [r,preproof] for p in folder.rglob('*') if p.is_file() and not p.resolve().is_relative_to(active)]))
assert all(Path(p).stat().st_size<100*1024*1024 for p in paths)
def stage(ps):subprocess.run(['git','-c','core.autocrlf=false','add','-f','--pathspec-from-file=-','--pathspec-file-nul'],input=('\0'.join(ps)+'\0').encode(),check=True)
stage(paths)
result=subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'],capture_output=True);diagnosis=r/'integration60/staging-whitespace';diagnosis.mkdir(exist_ok=False)
if result.returncode:
 assert result.returncode==2;raw=result.stdout;txt=raw.decode('utf-8');hits=re.findall(r'^(runs/.+):(\d+): (trailing whitespace\.|new blank line at EOF\.)$',txt,re.M);assert sum(2 if k=='trailing whitespace.' else 1 for _,_,k in hits)==len(txt.splitlines()),txt[-2000:]
 bad=sorted({p for p,n,k in hits})
 for p in bad:
  assert p.startswith((r.as_posix()+'/',preproof.as_posix()+'/')) and p.endswith(('.log','.snapshot','.snapshot.json','.snapshot.jsonl','.snapshot.lean','.raw','.lf','.py','.mjs','.exactraw.snapshot','.txt','.lean')),p
 (diagnosis/'full-staged-immutable-negative.raw.gz').write_bytes(gzip.compress(raw,mtime=0));authored=[p for p in paths if p not in set(bad)];commands=[]
 for i in range(0,len(authored),64):
  command=['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check','--']+authored[i:i+64];p=subprocess.run(command,capture_output=True);assert p.returncode==0,p.stdout;commands.append(command)
 data=dict(full_staged_exit=2,full_staged_called_PASS=False,exact_immutable_raw_paths=bad,findings=[dict(path=p,line=int(n),kind=k) for p,n,k in hits],negative_raw_sha256=sha(raw),negative_gzip_mtime=0,authored_complement_exit=0,authored_commands=commands,no_folder_exclusion=True)
else:
 assert result.returncode==0;data=dict(full_staged_exit=0,full_staged_called_PASS=True,exact_immutable_raw_paths=[],authored_complement_exit=0)
(diagnosis/'diagnosis.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');stage([p.as_posix() for p in diagnosis.iterdir() if p.is_file()]);subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check','--',diagnosis.as_posix()],check=True)
actual=set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines());assert actual<=set(paths)|{p.as_posix() for p in diagnosis.iterdir() if p.is_file()};assert set(shared)<=actual;assert not any(Path(p).resolve().is_relative_to(active) for p in actual)
subprocess.run(['git','commit','-q','-m','Integrate verified actual PBPS positive complex defect lift'],check=True)
print(json.dumps(dict(integration_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),staged_files=len(actual),immutable_native_whitespace_findings=len(data.get('findings',[])),authored_whitespace_PASS=True,full_paper=False)))
