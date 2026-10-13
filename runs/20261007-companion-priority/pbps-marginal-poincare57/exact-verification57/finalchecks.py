from common import *
import gzip
assert git('rev-parse','HEAD')==BASE
assert load(O/'gates.json')['status']=='PASS'
math=load(B/'whole-math57/receipt.json');scans=[]
def strip(s):
 out=[];i=0;depth=0
 while i<len(s):
  if s[i:i+2]=='/-':depth+=1;i+=2;continue
  if depth and s[i:i+2]=='-/':depth-=1;i+=2;continue
  if depth:i+=1;continue
  if s[i:i+2]=='--':
   j=s.find('\n',i);i=len(s) if j<0 else j;continue
  out.append(s[i]);i+=1
 assert depth==0
 return ''.join(out)
for row in math['fake_closure_scan']:
 assert equal(row['input']);p=path(row['input']['path']);code=strip(p.read_text(encoding='utf-8'))
 hits=re.findall(r'\b(?:axiom|sorry|admit)\b|Prop\s*:=\s*True|:=\s*trivial\b',code)
 assert not hits;scans.append(dict(input=pin(p),authored_fake_closure_hits=hits))
assert len(scans)==10
sig=(B/'whole-math57/exact-statement.lf.txt').read_bytes()
prod=path('AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/GaussianMarginalPoincare.lean').read_bytes().replace(b'\r\n',b'\n')
start=prod.index(b'theorem actual_gaussian_marginal_centered_poincare');actual=prod[start:prod.index(b' := by',start)]+b'\n'
assert actual==sig and len(sig)==1244
log=(O/'focused.log').read_text(encoding='utf-8');axioms=[]
for name,ax in re.findall(r"'([^']+)' depends on axioms: \[([^\]]+)\]",log,re.S):
 a=[x.strip() for x in ax.replace('\n',' ').split(',')];assert set(a)=={'propext','Classical.choice','Quot.sound'};axioms.append(dict(declaration=name,axioms=a))
assert len(axioms)==2 and 'Build completed successfully (3904 jobs).' in log
diag=load(B/'whitespace-diagnosis57/diagnosis.json');gz=path(diag['gzip']['path']).read_bytes();raw=gzip.decompress(gz)
assert sha(gz)==diag['gzip']['raw_sha256'] and sha(raw)==diag['full_negative_raw_sha256']
assert int.from_bytes(gz[4:8],'little')==0 and diag['findings']==3809 and len(diag['immutable_raw_artifacts'])==309 and diag['full_staged_exit']==2
assert sum(len(e['findings']) for e in diag['immutable_raw_artifacts'])==3809
excluded={e['path'] for e in diag['immutable_raw_artifacts']};assert len(excluded)==309
for e in diag['immutable_raw_artifacts']:assert equal(e)
science=load(O/'science.gitbindings.json')['entries'];owned={e['path'] for e in science};assert excluded<=owned
authored=sorted(owned-excluded);records=[]
for i in range(0,len(authored),64):
 cmd=['git','-c','core.whitespace=cr-at-eol','diff',BASE+'^',BASE,'--check','--']+authored[i:i+64]
 p=subprocess.Popen(cmd,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);out,_=p.communicate();assert p.returncode==0,(i,out)
 records.append(dict(batch=i//64,actual_PID=p.pid,exit_code=p.returncode,paths=authored[i:i+64],command=cmd,resource='CLOSED',output_raw_sha256=sha(out),output_bytes=len(out)))
dump('whitespace.authored.actual.json',dict(status='PASS_AUTHORED_COMPLEMENT_ONLY',checked_commit=BASE,owned_entry_count=1923,excluded_exact_immutable_paths=sorted(excluded),excluded_path_count=309,preserved_full_negative_findings=3809,preserved_full_negative_exit_code=2,native_gzip=pin(diag['gzip']['path']),native_negative_lossless_sha256=sha(raw),gzip_mtime=0,authored_path_count=len(authored),batch_limit=64,batches=records,full_staged_whitespace_PASS=False,no_blanket_folder_exclusion=True))
strict('inputs.pre-transition.json')
before=load(O/'before-transition.mappings.json')['exact_verified_admin_before_mappings']
for m in before:assert equal(m['original']) and equal(m['original'],m['exactraw_snapshot']['path'])
for e in science:assert equal(e['current']),e['path']
for e in load(O/'input.manifest.native.json')['inputs']:assert equal(e),e['path']
paths={path(e['current']['path']).as_posix():e['current'] for e in science}
for e in load(O/'input.manifest.native.json')['inputs']:paths[path(e['path']).as_posix()]=e
for p in ['tools/astis_advance.py','tools/astis_publication.py','tools/astis_semantic_roundtrip.py','tools/astis_frontier_cells.py','tools/astis_contributor_contract.py']:
 paths[path(p).as_posix()]=pin(p)
dump('inputs.science-complete.json',dict(checked_commit=BASE,science_entries=1923,math_originals=602,source_originals=614,distinct_actual_input_count=len(paths),inputs=list(paths.values()),before_transition='ALL exact current raw/LF entries bound before any canonical mutation. Posttransition cell/ledger require distinct exact before mappings and explicit authorized deltas.'))
dump('final.checks.json',dict(status='PASS_BEFORE_TRANSITION',checked_commit=BASE,source_gate=pin(O/'native.checks.json'),science_git_gate=pin(O/'science.gitbindings.json'),noncompiler_gates=pin(O/'gates.json'),fake_closure_scan=scans,axiom_closures=axioms,exact1244_sha256=sha(sig),compiler_status=pin(O/'focused.status.json'),compiler_lease=pin(O/'compiler.lease.json'),cache_observation='Exactly one actual invocation; production and Test were Replayed from unchanged cached artifacts. No forced rebuild or fresh-elaboration claim.',authored_whitespace=pin(O/'whitespace.authored.actual.json'),inputs=pin(O/'inputs.science-complete.json'),mathematical_reuse=pin(B/'whole-math57/mathematical-reasons.json'),before_admin_mappings=pin(O/'before-transition.mappings.json'),source_review_repairs=0,all_before_transition_bindings=True,remaining='Full weakH1/macro-range/fullB13/Gamma/halfturn/dynamics/main/errors/cost/composition/full-reader/live/PURIFIED OPEN. Full shared aggregate is later serialized integration, not current evidence.'))
print(json.dumps(dict(status='PASS_BEFORE_TRANSITION',distinct_inputs=len(paths),science_entries=1923,source_inputs614=614,math_inputs602=602,fake_scan_rows=10,axiom_closures=axioms,authored_paths=len(authored),whitespace_batches=len(records),immutable_whitespace_findings=3809,immutable_paths=309)))
