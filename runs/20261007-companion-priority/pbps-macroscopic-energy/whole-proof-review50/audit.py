# coding: utf-8
import pathlib,json,re,hashlib,sys,difflib
sys.stdout.reconfigure(encoding='utf-8');R=pathlib.Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/pbps-macroscopic-energy/whole-proof-review50';RUN=O.parent
def sha(b):return hashlib.sha256(b).hexdigest()
def lf(b):return b.replace(b'\r\n',b'\n')
def dump(name,x):(O/name).write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
def pin(p):b=p.read_bytes();return dict(path=str(p),raw_sha256=sha(b),lf_sha256=sha(lf(b)),raw_bytes=len(b),lf_bytes=len(lf(b)))
target=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicEnergy.lean';test=R/'Tests/ProximalBPSMacroscopicEnergy.lean';raw=target.read_bytes();st=raw.index(b'theorem actual_macroscopic_gradient_energy_blocks');en=raw.index(b':= by',st);header=lf(raw[st:en]).rstrip()+b'\n';expected=lf((R/'runs/20261007-companion-priority/pbps-macroscopic-energy-preproof50/prospective-statement.txt').read_bytes());assert header==expected and len(header)==2907
(O/'actual-public-header.lf').write_bytes(header)
parents=json.loads((R/'runs/20261007-companion-priority/pbps-macroscopic-energy-preproof50/parent-public-contracts.json').read_text(encoding='utf-8-sig'));parents=parents.get('parents',parents.get('contracts'));parentchecks=[]
for p in parents:
 path=R/p['file'];b=path.read_bytes();name=p['declaration'].split('.')[-1];a=b.index(('theorem '+name).encode());z=b.index(b':= by',a);h=lf(b[a:z]).rstrip()+b'\n';assert sha(b)==p['whole_raw_sha256'] and sha(lf(b))==p['whole_lf_sha256'] and sha(h)==p['public_header_lf_sha256'];parentchecks.append(dict(declaration=p['declaration'],current=pin(path),public_header_lf_sha256=sha(h),exact_matches=True,review_scope='Energy49 wholemath reused unchanged after identity; representative and reflection bodies expanded now.'))
dump('parent-identity-reuse.json',parentchecks)
# Recursively pin only actual reachable local ASTIS imports. This is a lexical/import closure audit, not semantic expansion of every parent proof.
queue=['AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicEnergy'];seen=set();nodes=[];edges=[];hits=[];rawmarkers=[];external=set()
def strip_comments_and_strings(s):
 # Preserve line positions while masking nested Lean comments and string contents.
 out=list(s);i=0;depth=0;string=False
 while i<len(s):
  if depth:
   if s.startswith('/-',i):out[i:i+2]=[' ',' '];depth+=1;i+=2;continue
   if s.startswith('-/',i):out[i:i+2]=[' ',' '];depth-=1;i+=2;continue
   if s[i]!='\n':out[i]=' '
   i+=1;continue
  if string:
   if s[i]=='\\' and i+1<len(s):out[i]=' ';out[i+1]=' ';i+=2;continue
   if s[i]=='"':string=False
   if s[i]!='\n':out[i]=' '
   i+=1;continue
  if s.startswith('/-',i):out[i:i+2]=[' ',' '];depth=1;i+=2;continue
  if s.startswith('--',i):
   while i<len(s) and s[i]!='\n':out[i]=' ';i+=1
   continue
  if s[i]=='"':out[i]=' ';string=True
  i+=1
 return ''.join(out)
pattern=re.compile(r'\b(?:sorry|admit)\b|^\s*axiom\s|Prop\s*:=\s*True|:=\s*trivial\b',re.M)
while queue:
 mod=queue.pop()
 if mod in seen:continue
 seen.add(mod);path=R/(mod.replace('.','/')+'.lean');b=path.read_bytes();s=b.decode('utf-8-sig');clean=strip_comments_and_strings(s);imports=re.findall(r'^\s*(?:public\s+)?import\s+([\w.]+)',clean,re.M)
 nodes.append(dict(module=mod,**pin(path),audit_scope='Import topology and lexical fake-closure scan only; body semantics expanded only for named reviewed parents/target'))
 for child in imports:
  edges.append(dict(from_module=child,to_module=mod))
  if child.startswith('AutoSamplingTheory'):queue.append(child)
  else:external.add(child)
 for m in pattern.finditer(clean):hits.append(dict(module=mod,line1=clean.count('\n',0,m.start())+1,token=m.group()))
 for m in pattern.finditer(s):rawmarkers.append(dict(module=mod,line1=s.count('\n',0,m.start())+1,token=m.group(),code_or_masked='code' if pattern.search(clean,m.start(),m.end()) else 'comment/string/nonclosure text'))
dump('reachable-local-import-closure.json',dict(local_modules=nodes,edges=edges,external_imports=sorted(external),full_mathlib_import_or_body_scan=False))
dump('fake-closure-scan.json',dict(status='NO_EXECUTABLE_FAKE_CLOSURE_FOUND' if not hits else 'FLAGGED',code_hits=hits,raw_markers=rawmarkers,masking='Nested comments, line comments and Lean string literals excluded; axioms/sorry/admit/PropTrue/trivial closures checked lexically. Kernel axiom prints provide stronger target reachability evidence.',module_count=len(nodes)))
assert not hits
apis=[('Mathlib/Probability/Kernel/Composition/MeasureCompProd.lean',61,62,'MeasureTheory.Measure.compProd_apply','SFinite first measure and SFinite kernel; both internally supplied by actual probabilities/Markov kernels.'),('Mathlib/MeasureTheory/Measure/Map.lean',161,162,'MeasureTheory.Measure.map_apply','Measurable map and measurable set.'),('Mathlib/MeasureTheory/Measure/Map.lean',203,204,'MeasureTheory.Measure.map_map','Both maps measurable; literal composition.'),('Mathlib/MeasureTheory/Measure/Prod.lean',1133,1134,'MeasureTheory.Measure.fst_map_prodMk','Measurable second component; first marginal is true map of first component.'),('Mathlib/MeasureTheory/Measure/Prod.lean',1209,1209,'MeasureTheory.Measure.fst_map_swap','Actual swap pushforward first marginal equals original second marginal.'),('Mathlib/Probability/Kernel/Disintegration/Basic.lean',53,59,'MeasureTheory.Measure.IsCondKernel','Actual measure equality rho.fst compProd kernel=rho.'),('Mathlib/Probability/Kernel/Disintegration/Basic.lean',63,63,'MeasureTheory.Measure.disintegrate','Projection of genuine class witness, not caller-supplied arbitrary law equality.'),('Mathlib/Probability/Kernel/Disintegration/Unique.lean',32,40,'uniqueness section context','StandardBorel nonempty conditional space; rho finite. Supplied internally by finite Hilbert/Borel/probability.'),('Mathlib/Probability/Kernel/Disintegration/Unique.lean',82,84,'ProbabilityTheory.eq_condKernel_of_measure_eq_compProd','Finite kernel and genuine disintegration; result AE under true first marginal only.'),('Mathlib/MeasureTheory/Measure/Map.lean',248,249,'MeasureTheory.ae_of_ae_map','Actual map and AE predicate under pushed law.'),('Mathlib/MeasureTheory/Function/LpSpace/Basic.lean',146,146,'MeasureTheory.Lp.ext','Genuine Lp quotient elements and AE representative equality.'),('Mathlib/MeasureTheory/Function/L2Space.lean',137,137,'MeasureTheory.L2.inner_def','Actual L2 inner equals real integral of pointwise inner.'),('Mathlib/Analysis/InnerProductSpace/Basic.lean',396,396,'real_inner_self_eq_norm_sq','Real Hilbert squared norm identity.'),('Mathlib/MeasureTheory/Integral/Bochner/Basic.lean',299,299,'MeasureTheory.integral_congr_ae','Actual AE integrands; true domains remain produced by49/Lp.'),('Mathlib/MeasureTheory/Integral/Bochner/Basic.lean',1043,1045,'MeasureTheory.integral_map','AEMeasurable snd and AEStronglyMeasurable continuous square; square-integrability follows from actual Lp/49 outputs.')]
apiout=[];d=O/'selected-apis';d.mkdir(exist_ok=True)
for i,(rel,a,z,q,c) in enumerate(apis):
 path=R/'.lake/packages/mathlib'/rel;b=path.read_bytes();ls=b.splitlines(keepends=True);st=sum(map(len,ls[:a-1]));en=sum(map(len,ls[:z]));frag=b[st:en];label='%02d'%i;(d/(label+'.raw')).write_bytes(frag);(d/(label+'.lf')).write_bytes(lf(frag));apiout.append(dict(qualified_id=q,contract=c,**pin(path),physical_lines1=[a,z],start_utf8_byte0=st,end_utf8_byte0_exclusive=en,fragment_raw_sha256=sha(frag),fragment_lf_sha256=sha(lf(frag)),snapshot='selected-apis/'+label,scope='Exact pinned primitive header/context; no optional Mathlib proof expansion'))
dump('selected-api-bindings.json',apiout)
log=(RUN/'tests.4.log').read_text(encoding='utf-8');prints=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]+)\]",log);assert len(prints)==3
assert all(set(x.strip() for x in ax.split(','))=={'propext','Classical.choice','Quot.sound'} for _,ax in prints)
assert 'Build completed successfully (3891 jobs)' in log
status=json.loads((RUN/'tests.4.status.json').read_text(encoding='utf-8-sig'));assert status['exit_code']==0 and status['source_raw_sha256']==sha(test.read_bytes()) and status['log_raw_sha256']==sha((RUN/'tests.4.log').read_bytes())
prod2=(RUN/'production.2.source.raw.snapshot.lean').read_text(encoding='utf-8');final=target.read_text(encoding='utf-8');diff=''.join(difflib.unified_diff(prod2.splitlines(True),final.splitlines(True),fromfile='production2',tofile='frozen-final'));(O/'production2-final-style-delta.diff').write_bytes(diff.encode())
assert prod2.replace('letI :','let :')==final
dump('focused-evidence-reuse.json',dict(status='FROZEN_ROOT_FOCUSED_EVIDENCE_REUSED_NO_REVIEWER_COMPILER',tests_attempt=4,jobs=3891,exit_code=0,tests_source_raw_sha256=sha(test.read_bytes()),production_source_raw_sha256=sha(raw),production2_final_delta='Only9 proof-irrelevant letI→let local instance style changes; final focused Lake Tests4 imports/checks current target. Earlierproduction2 standalonePASS bound its own historical snapshot, not substituted for final bytes.',axiom_prints=[dict(declaration=d,axioms=[x.strip() for x in a.split(',')]) for d,a in prints],no_sorryAx=True,scope='Mathematical review uses frozen build/kernel axiom evidence; not a new independent compiler/commit/full-root gate or VERIFIED transition.'))
print(json.dumps(dict(header_sha256=sha(header),local_import_modules=len(nodes),lexical_code_hits=len(hits),raw_markers=len(rawmarkers),parent_identity_checks=len(parentchecks),api_headers=len(apiout),axiom_prints=len(prints))))
