from pathlib import Path
import subprocess,json,hashlib,datetime,re,gzip,runpy
r=Path('runs/20261007-companion-priority/pbps-rough-mean-gradient56')
j=lambda p:json.loads(Path(p).read_text(encoding='utf-8'));sha=lambda b:hashlib.sha256(b).hexdigest()
def bind(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),bytes=len(b),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')))
def w(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert j(r/'root.integration.0.lease.json')['status']=='CLOSED' and j(r/'root.integration.0.lease.json')['exit_code']==0
v=runpy.run_path('.astis/pbps-marginal-gradient51/require-verification56.py')['require_verified']();head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert head==v['verified_commit'];assert j(r/'exact-verification56/lease.json')['status']=='CLOSED'
sync=j(r/'sync-before-integration56.json');assert subprocess.check_output(['git','rev-parse','origin/main'],text=True).strip()==sync['main_after']
labels=['tests','mandatory','pycompile','whitespace','publication','semantic','frontier','contributor','site-build','official-graph','graph','site-check'];bindings=[]
for label in labels:
 p=r/('integration.0.'+label+'.status.json');assert j(p)['exit_code']==0;bindings += [bind(p),bind(r/('integration.0.'+label+'.log'))]
plan=j(r/'publication-plan.json')
science=['AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','research-wiki/cited-results/SLT_reuse_audit.md','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl','runs/substantive_advances.jsonl','website/content/samplewiki_companion_frontiers.json']+['research-wiki/frontier-cells/'+x+'.json' for x in plan['active_cells']]
assert len(plan['active_cells'])==1 and plan['active_cells'][0]=='ASTIS-SW-PBPS-l2-macroscopic-mean'
assert j(science[-1])['evidence']['serialized_shared_gate']['status']=='PASS'
assert (r/'visual.inspection.json').exists();note=r/'integration.notes.json';assert not note.exists()
jobs=[int(x) for x in re.findall(r'Build completed successfully \((\d+) jobs\)',(r/'integration.0.mandatory.log').read_text(encoding='utf-8'))];assert len(jobs)>=2
w(note,dict(status='SERIALIZED_SHARED_AGGREGATE_PASS_NOT_MAIN_NOT_PURIFIED',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),proof_commit=head,verified_commit=head,registry_count=497,root_jobs=jobs[0],test_jobs=jobs[1],checks=bindings,graph_delta='One actual all-L2 source-specific rough mean-gradient declaration joins the three actual law/mean/compact-energy parents. Exact1755 fixed statement, genuine dense closable compact core, one bounded T/K before all rough inputs, actual graph image, sharp c and source4eta defects; SAME-T real BMu difference and alphaeta1 K=0 consumers compile. Existing companion six-formula lesson and exact declaration graph regenerated, module/import semantics kept; no new conceptual certificates or full weakH1/B13/Gamma/main/cost claims.',visual_inspection=j(r/'visual.inspection.json'),remaining='Separate weak-H1/full B13/actual defect-root Gamma and meanzero inverse-domain; four full papers, expected costs and actual-input composition; full-reader/main/live/PURIFIED separate.',sole_stabilization_owner='ASTIS-SA-20261005-SPHMCImplementedPhaseKernel',sync=sync,shared_files=[bind(q) for q in science]))
paths=list(dict.fromkeys(science+[p.as_posix() for p in r.rglob('*') if p.is_file() and not any(x in ['repository-seal56','exposition-seal56','root-seal-followup56'] for x in p.parts)]))
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip();assert all(Path(p).stat().st_size<100*1024*1024 for p in paths)
def stage(ps):subprocess.run(['git','-c','core.autocrlf=false','add','-f','--pathspec-from-file=-','--pathspec-file-nul'],input=('\0'.join(ps)+'\0').encode(),check=True)
stage(paths)
check=subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
if check.returncode:
 assert check.returncode==2;raw=check.stdout;txt=raw.decode('utf-8');hits=re.findall(r'^(runs/.+):(\d+): (trailing whitespace\.|new blank line at EOF\.)$',txt,re.M)
 assert sum(2 if k=='trailing whitespace.' else 1 for _,_,k in hits)==len(txt.splitlines());rawpaths=sorted(set(p for p,_,_ in hits))
 q=r/'integration-whitespace56';q.mkdir(exist_ok=False);(q/'staged.raw-whitespace.negative.log.gz').write_bytes(gzip.compress(raw,mtime=0))
 for p in rawpaths:assert p.startswith(r.as_posix()+'/') and p.endswith(('.log','.raw','.lf','.snapshot')),p
 authored_paths=[p for p in paths if p not in set(rawpaths)]
 args=[['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check','--']+authored_paths[i:i+64] for i in range(0,len(authored_paths),64)]
 outputs=[]
 for command in args:
  result=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);assert result.returncode==0,result.stdout;outputs.append(result.stdout)
 class Checked:
  returncode=0
  stdout=b''.join(outputs)
 authored=Checked()
 (q/'staged.authored-whitespace.log').write_bytes(authored.stdout)
 w(q/'diagnosis.json',dict(scope='Exact immutable emitted gate/compiler/API snapshot artifacts preserved without folder exclusions. Current authored shared files and notes pass; full staged whitespace not called PASS.',full_staged_exit=2,full_negative_raw_sha256=sha(raw),full_negative_raw_bytes=len(raw),gzip=bind(q/'staged.raw-whitespace.negative.log.gz'),gzip_mtime=0,findings=[dict(path=p,line=int(n),diagnosis=k) for p,n,k in hits],immutable_raw_artifacts=[bind(p) for p in rawpaths],authored_command=args,authored_exit=0,authored_log=bind(q/'staged.authored-whitespace.log')))
 stage([p.as_posix() for p in q.iterdir() if p.is_file()])
 for command in args:subprocess.run(command,check=True)
 subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check','--']+[p.as_posix() for p in q.iterdir() if p.is_file()],check=True)
 print('56 immutable raw whitespace:',len(hits),'findings',len(rawpaths),'exact paths; authored staged PASS')
else:assert check.returncode==0
actual=set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines());assert actual<=set(paths+[p.as_posix() for p in (r/'integration-whitespace56').glob('*') if p.is_file()]);assert all(p in actual for p in science),set(science)-actual
subprocess.run(['git','commit','-q','-m','Integrate verified actual PBPS rough mean closed gradient and sharp defect'],check=True)
print('56 serialized integration',subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip())
