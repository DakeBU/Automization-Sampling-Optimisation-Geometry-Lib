from pathlib import Path
import hashlib, json, subprocess, os, gzip, re
root=Path.cwd();r=Path('runs/20261007-companion-priority/pbps-macro-root63')
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()=='4d02622332d02d0bd6c977d3cee48fd535ebf203'
assert load(r/'root.exact-verification63.adoption.json')['native_verified']
assert load(r/'visual.inspection.json')['viewed_by_root']
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
for label in ['mandatory-astis-check-final','publication-final-admin-v2','frontier-final-admin-v3','contributor-final-admin-v2','semantic','python-regression-suite','local-site-check','cell-graph-check','reader-copy-download-v2']:
 x=load(r/'integration63'/label/'receipt.json');assert x['terminal_closed'] and x['exit_code']==0,label
shared=['AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl','runs/substantive_advances.jsonl','docs/module-graph.svg','docs/assets/astis_lean_arsenal_module_graph.svg','research-wiki/sampling-sde-library/lean-leaf-module-graph.md','research-wiki/retrieval-index/astis-lean-arsenal-module-graph.json','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicDefectRoot.md','research-wiki/frontier-cells/ASTIS-SW-PBPS-unique-macroscopic-defect-root.json']
changed=set(subprocess.check_output(['git','-c','core.autocrlf=false','diff','--name-only'],text=True).splitlines())
assert changed<=set(shared),changed-set(shared)
active=Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR']).resolve();assert active.is_relative_to((r/'integration63').resolve())
export=r/'root-integration-executed63';export.mkdir(exist_ok=False)
for name in ['adopt-exact63.py','repair-frontier-process63.py','integrate63.py','integration-gate63.py','preserve-integration-newlines63.py','preserve-generated-context63.py','inspect-cdp63.mjs','inspect-copy63.mjs','inspect-copy63-v2.mjs','record-integration63.py','cache-generated-cards63.py','commit-integration63.py']:
 (export/name).write_bytes((Path('.astis/pbps-macro-root63')/name).read_bytes())
pre=Path('runs/20261007-companion-priority/pbps-macro-root-preproof63')
r62=Path('runs/20261007-companion-priority/pbps-real-root-unique62')
assert load(r62/'root.repository-exposition62.adoption.json')['status']
paths=list(dict.fromkeys([p for p in shared if p!='runs/substantive_advances.jsonl']+[p.as_posix() for folder in [r,pre,r62] for p in folder.rglob('*') if p.is_file() and not p.resolve().is_relative_to(active)]))
assert all(Path(p).stat().st_size<100*1024*1024 for p in paths)
assert not any('pbps-centered-root64' in p or 'pbps-centered-root-preproof64' in p for p in paths)
def stage(ps):
 subprocess.run(['git','-c','core.autocrlf=false','add','-f','--pathspec-from-file=-','--pathspec-file-nul'],input=('\0'.join(ps)+'\0').encode(),check=True)
stage(paths)
# Stage only the immutable exact prefix ending at native VERIFIED63. Keep the
# newer claimed64 ledger tail in the working file; do not overwrite or stash it.
prefix=Path('runs/20261007-companion-priority/pbps-centered-root64/ledger.before64.exactraw.snapshot').read_bytes()
working=Path('runs/substantive_advances.jsonl').read_bytes();assert working.startswith(prefix) and len(working)>len(prefix)
events=[json.loads(s) for s in prefix.splitlines() if s.strip()]
assert any(x.get('advance_id')=='ASTIS-SA-20261009-PBPSUniqueMacroscopicDefectRoot' and x.get('status',x.get('state',x.get('to_state')))=='VERIFIED' for x in events), 'prefix missing native verified63 event'
assert b'ASTIS-SA-20261009-PBPSCenteredRootOrderInverse' not in prefix
blob=subprocess.check_output(['git','hash-object','-w','--stdin'],input=prefix).decode().strip()
subprocess.run(['git','update-index','--cacheinfo','100644',blob,'runs/substantive_advances.jsonl'],check=True)
paths.append('runs/substantive_advances.jsonl')
d=r/'integration63/staging-whitespace';d.mkdir(exist_ok=False)
q=subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'],capture_output=True)
if q.returncode:
 assert q.returncode==2
 text=q.stdout.decode('utf-8');hits=re.findall(r'^(.+):(\d+): (trailing whitespace\.|new blank line at EOF\.)$',text,re.M)
 assert sum(2 if k=='trailing whitespace.' else 1 for _,_,k in hits)==len(text.splitlines()),text[-1500:]
 bad=sorted({p for p,n,k in hits})
 for p in bad:assert p.startswith(tuple(f.as_posix()+'/' for f in [r,pre,r62])),p
 (d/'full-staged-immutable-negative.raw.gz').write_bytes(gzip.compress(q.stdout,mtime=0))
 authored=[p for p in paths if p not in set(bad)];commands=[]
 for i in range(0,len(authored),64):
  cmd=['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check','--']+authored[i:i+64]
  x=subprocess.run(cmd,capture_output=True);assert x.returncode==0,x.stdout
  commands.append(cmd)
 data=dict(full_staged_exit=2,full_staged_called_PASS=False,exact_immutable_raw_paths=bad,findings=[dict(path=p,line=int(n),kind=k) for p,n,k in hits],negative_raw_sha256=sha(q.stdout),authored_complement_exit=0,authored_commands=commands,no_folder_exclusion=True)
else:
 assert q.returncode==0;data=dict(full_staged_exit=0,full_staged_called_PASS=True,exact_immutable_raw_paths=[],authored_complement_exit=0)
(d/'diagnosis.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
pres=dict(staged63_ledger_exact_prefix_RAW_sha256=sha(prefix),working64_ledger_tail_RAW_sha256=sha(working[len(prefix):]),working_file_not_overwritten=True,claim64_or_proof64_staged=False)
(d/'ledger-prefix-preservation.json').write_text(json.dumps(pres,indent=2)+'\n',encoding='utf-8',newline='\n')
stage([p.as_posix() for p in d.iterdir() if p.is_file()])
actual=set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines())
assert actual<=set(paths)|{p.as_posix() for p in d.iterdir() if p.is_file()}
assert not any(Path(p).resolve().is_relative_to(active) or 'pbps-centered-root64' in p or 'pbps-centered-root-preproof64' in p for p in actual)
assert Path('runs/substantive_advances.jsonl').read_bytes()==working
subprocess.run(['git','commit','-q','-m','Integrate verified PBPS macroscopic defect root and Gram identity'],check=True)
print(json.dumps(dict(integration_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),staged_files=len(actual),immutable_native_whitespace_findings=len(data.get('findings',[])),authored_whitespace_PASS=True,full_staged_whitespace_PASS=data['full_staged_called_PASS'],claim64_working_tail_preserved=True,actual64_proof_staged=False,full_paper=False)))
