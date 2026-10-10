from pathlib import Path
import gzip,hashlib,json,re,subprocess,os
r=Path('runs/20261007-companion-priority/pbps-real-root-unique62');load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()=='9d7f7b640c7cb18fea133ccbd300de129af40b83'
assert load(r/'root.exact-verification62.adoption.json')['native_verified'] and load(r/'visual.inspection.json')['viewed_by_root']
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
plan=load(r/'publication-plan.json');shared=['AutoSamplingTheory/TechnicalLemmas.lean','AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl','runs/substantive_advances.jsonl','docs/module-graph.svg','docs/assets/astis_lean_arsenal_module_graph.svg','research-wiki/sampling-sde-library/lean-leaf-module-graph.md','research-wiki/retrieval-index/astis-lean-arsenal-module-graph.json','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareRootUnique.md','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.ExampleCases.ProximalBPS.RealDefectRootUnique.md']+['research-wiki/frontier-cells/'+x+'.json' for x in plan['active_cells']]
planning_cell='research-wiki/frontier-cells/ASTIS-SW-PBPS-unique-macroscopic-defect-root.json'
assert load(planning_cell)['status']=='claimed'
shared.append(planning_cell)
changed=set(subprocess.check_output(['git','diff','--name-only'],text=True).splitlines());assert changed<=set(shared),changed-set(shared)
for cid in plan['active_cells']:assert load('research-wiki/frontier-cells/'+cid+'.json')['evidence']['serialized_shared_gate']['status']=='PASS'
for label in ['mandatory-astis-check','publication-final-admin','contributor-final-admin-v2','frontier-final-admin-v2','semantic','python-compile','website-ci-build','official-graph-ci-output','official-graph-final-admin','graph-producer','graph-consumer','graph-producer-final-admin','graph-consumer-final-admin','site-check','site-check-final-admin']:assert load(r/'integration62'/label/'receipt.json')['exit_code']==0,label
assert load(r/'integration62/tracked-whitespace/diagnosis.json')['full_tracked_called_PASS']
export=r/'root-integration-executed62';export.mkdir(exist_ok=False)
for name in ['adopt-exact62.py','integrate62.py','integration-gate62.py','preserve-integration-newlines62.py','preserve-generated-context62.py','inspect-cdp62.mjs','record-integration62.py','cache-generated-cards62.py','commit-integration62.py']:(export/name).write_bytes((Path('.astis/pbps-real-root-unique62')/name).read_bytes())
active=Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR']).resolve();assert active.is_relative_to((r/'integration62').resolve())
old=Path('runs/20261007-companion-priority/pbps-real-defect-root61');preold=Path('runs/20261007-companion-priority/pbps-real-defect-root-preproof61');pre=Path('runs/20261007-companion-priority/pbps-real-root-unique-preproof62');pre63=Path('runs/20261007-companion-priority/pbps-macro-root-preproof63');r63=Path('runs/20261007-companion-priority/pbps-macro-root63');excluded=[(old/'next-macro-source62').resolve()]
paths=list(dict.fromkeys(shared+[p.as_posix() for folder in [r,pre,old,preold,pre63] for p in folder.rglob('*') if p.is_file() and not p.resolve().is_relative_to(active) and not any(p.resolve().is_relative_to(x) for x in excluded)]))
planning63=['claim.json','preproof-admission.json','ledger.before63.exactraw.snapshot','ledger-history.json','conceptual-mirror-audit63.json','cell.before-conceptual-audit63.exactraw.snapshot.json']
paths+= [(r63/p).as_posix() for p in planning63]
assert all(Path(p).stat().st_size<100*1024*1024 for p in paths)
def stage(ps):subprocess.run(['git','-c','core.autocrlf=false','add','-f','--pathspec-from-file=-','--pathspec-file-nul'],input=('\0'.join(ps)+'\0').encode(),check=True)
stage(paths);q=subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'],capture_output=True);d=r/'integration62/staging-whitespace';d.mkdir(exist_ok=False)
if q.returncode:
 assert q.returncode==2;txt=q.stdout.decode('utf-8');hits=re.findall(r'^(runs/.+):(\d+): (trailing whitespace\.|new blank line at EOF\.)$',txt,re.M);assert sum(2 if k=='trailing whitespace.' else 1 for _,_,k in hits)==len(txt.splitlines()),txt[-2000:];bad=sorted({p for p,n,k in hits})
 for p in bad:
  assert p.startswith(tuple(f.as_posix()+'/' for f in [r,pre,old,preold,pre63,r63])) and p.endswith(('.log','.snapshot','.snapshot.json','.snapshot.jsonl','.snapshot.lean','.raw','.lf','.py','.mjs','.exactraw.snapshot','.txt','.lean')),p
 (d/'full-staged-immutable-negative.raw.gz').write_bytes(gzip.compress(q.stdout,mtime=0));authored=[p for p in paths if p not in set(bad)];commands=[]
 for i in range(0,len(authored),64):
  cmd=['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check','--']+authored[i:i+64];x=subprocess.run(cmd,capture_output=True);assert x.returncode==0,x.stdout;commands.append(cmd)
 data=dict(full_staged_exit=2,full_staged_called_PASS=False,exact_immutable_raw_paths=bad,findings=[dict(path=p,line=int(n),kind=k) for p,n,k in hits],negative_raw_sha256=sha(q.stdout),authored_complement_exit=0,authored_commands=commands,no_folder_exclusion=True)
else:
 assert q.returncode==0;data=dict(full_staged_exit=0,full_staged_called_PASS=True,exact_immutable_raw_paths=[],authored_complement_exit=0)
(d/'diagnosis.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');stage([p.as_posix() for p in d.iterdir() if p.is_file()]);subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check','--',d.as_posix()],check=True)
actual=set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines());assert actual<=set(paths)|{p.as_posix() for p in d.iterdir() if p.is_file()};assert set(shared)<=actual;assert not any(Path(p).resolve().is_relative_to(active) or any(Path(p).resolve().is_relative_to(x) for x in excluded) for p in actual)
subprocess.run(['git','commit','-q','-m','Integrate verified PBPS scalar root uniqueness and seal next macro target'],check=True)
print(json.dumps(dict(integration_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),staged_files=len(actual),immutable_native_whitespace_findings=len(data.get('findings',[])),authored_whitespace_PASS=True,full_paper=False,macro63_planning_only=True,active_macro_proof_staged=False)))
