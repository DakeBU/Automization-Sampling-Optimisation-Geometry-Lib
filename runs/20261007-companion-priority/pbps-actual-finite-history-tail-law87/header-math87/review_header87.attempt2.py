from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,sys
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent
H=B/'header87.proposed.lean';P=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean';U=R/'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def read(p):return json.loads(p.read_text('utf8'))
def put(n,x):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(x,f,ensure_ascii=False,indent=2);f.write('\n')
hraw=H.read_bytes();hs=hraw.decode('utf8').replace('\r\n','\n');ps=P.read_text('utf8').replace('\r\n','\n');us=U.read_text('utf8').replace('\r\n','\n')
def sig(s):return s[s.index('    {E : Type*}'):s.index(' : Prop :=')]
assert sig(hs)==sig(ps)
def definitions(s):
 starts=list(re.finditer(r'^    let ([^\s:]+).*',s,re.M));out={}
 for j,m in enumerate(starts):
  end=starts[j+1].start() if j+1<len(starts) else len(s)
  out[m.group(1)]=s[m.start():end].rstrip()
 return out
hprop=hs[hs.index('private def '):hs.index('\n#check')]
pprop=ps[ps.index('private def '):ps.index('\nset_option maxHeartbeats')]
hd=definitions(hprop);pd=definitions(pprop)
actual=['c','Φ','S','rate','Λ','τ','next','record']
for n in actual:assert hd[n]==pd[n],n
assert len(hd)==13 and set(hd)==set(actual+['P','ε','history','tail','past'])
assert hd['P'].strip() in us
assert 'fun w k => Real.toNNReal (w k)' in hd['ε']
assert 'Fin (n + 1)' in hd['history'] and 'j.val' in hd['history']
assert 'fun n w k => w (n + k)' in hd['tail']
assert '⨆ k ∈ Set.Iio n' in hd['past']
assert not re.search(r'\b(sorry|axiom|admit)\b',hs)
with (O/'header87.exactraw.snapshot.lean').open('xb') as f:f.write(hraw)
api='''import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteJumpRecursion
import AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct
#check @AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteJumpRecursion.actual_fixed_reference_finite_jump_recursion
#check @AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws
#check ProbabilityTheory.iIndepFun.precomp
#check ProbabilityTheory.iIndepFun.map_fun_eq_infinitePi_map
#check ProbabilityTheory.indep_iSup_of_disjoint
#check ProbabilityTheory.IndepFun.map_prod_eq_prod_map_map
#check ProbabilityTheory.IndepFun.measure_inter_preimage_eq_mul
#check Measurable.iSup'
#check MeasurableSpace.comap_iSup
'''
with (O/'ParentAndGenericAPI87.lean').open('x',encoding='utf8',newline='\n') as f:f.write(api)
inputs=[H,P,U,R/'lean-toolchain',R/'lake-manifest.json',R/'.lake/packages/mathlib/Mathlib/Probability/Independence/Basic.lean',R/'.lake/packages/mathlib/Mathlib/Probability/Independence/InfinitePi.lean',R/'.lake/packages/mathlib/Mathlib/Probability/Independence/Process/Basic.lean',R/'.lake/packages/mathlib/Mathlib/MeasureTheory/MeasurableSpace/Basic.lean',R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Constructions/Pi.lean']
base=R/'runs/20261007-companion-priority/pbps-path-law-preread86/pre-fetch86.workspace-RAW.json';prior=read(base)['tracked_modified'];assert len(prior)==21
for p,v in prior.items():assert pin(R/p)['raw_sha256']==v
put('collaborator-preservation87.json',dict(baseline=pin(base),count=21,RAWs=[pin(R/p) for p in prior]))
assert pin(R/'lean-toolchain')['raw_sha256']=='b2b5068d5a4835675e651ce83b29c0ddb308d28b80076e7c007aef4630af0477'
assert pin(R/'lake-manifest.json')['raw_sha256']=='b1f16b43aaf4a886cfe0382d5e3ae63d6904281c00afd8f35af20f0270a747e2'
assert subprocess.check_output(['git','-C',str(R/'.lake/packages/mathlib'),'rev-parse','HEAD'],text=True).strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
put('input-freeze87.json',dict(created_utc=now(),reviewer_id='/root/exact_verify77',observed_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),actual_inputs=[pin(p) for p in inputs],parent_read_scope='ActualFiniteJumpRecursion lines1-135 included complete private Prop/public signature and initial proof definitions; UnitExponentialProduct lines1-35 complete private Prop/public signature. No candidate87 proof exists or is authored. Generic Mathlib declaration retrieval/read only; not source-blind topology or final source review.',source_scope='G86-11 deterministic finite-depth unused-tail independence substrate; no new primary-source topology reconstruction or final source verdict asserted.'))
put('definition-readback87.json',dict(status='EXACT_ACTUAL_PARENT_SEMANTICS_PRESERVED',six_analytic_binders=['hα','hαβ','hV','hH','hη','hβη'],binder_block_identical_to_parent=True,all_literal_definition_names=list(hd),literal_definition_count=13,parent_byte_identical_after_CRLF_LF_read_normalization=actual,per_definition_raw_text_hashes={n:hashlib.sha256(v.encode()).hexdigest() for n,v in hd.items()},P_identity='Same actual infinitePi Exp1 law as UnitExponentialProduct. epsilon(w,k) is parent epsilon(k,w), a definitional argument-order adapter.',history='All records j=0,...,n. record j uses e0,...,e(j-1); Fin(n+1) therefore consumes only coordinates strictly below n.',tail='Complete raw real product function k↦w(n+k), not NNReal converted tail or a finite vector.',past='Join of coordinate-comap sigma algebras for k<n. For n0 this is bottom; no completed filtration or conditional probability version supplied.'))
env=dict(os.environ,PYTHONUTF8='1');env.pop('ELAN_TOOLCHAIN',None)
lake=R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe';lean=R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe'
def compile(n,p):
 cmd=[str(lake),'env',str(lean),str(p)];start=now()
 proc=subprocess.Popen(cmd,cwd=R,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=proc.communicate()
 for suffix,data in [('stdout.log',out),('stderr.log',err)]:
  with (O/(n+'.'+suffix)).open('xb') as f:f.write(data)
 put(n+'.receipt.json',dict(command=cmd,cwd=str(R),actual_foreground_PID=proc.pid,started_utc=start,finished_utc=now(),exit_code=proc.returncode,terminal_closed=True,source=pin(p),stdout=pin(O/(n+'.stdout.log')),stderr=pin(O/(n+'.stderr.log')),toolchain=pin(R/'lean-toolchain'),lake_manifest=pin(R/'lake-manifest.json'),proof_credit=False))
 print(n,'TERMINAL_EXIT',proc.returncode,flush=True);assert proc.returncode==0
compile('whole-header-typecheck87',O/'header87.exactraw.snapshot.lean')
compile('parent-api-check87',O/'ParentAndGenericAPI87.lean')
put('mathematical-review87.json',dict(status='ACCEPTED_PROSPECTIVE_MATHEMATICS_ONLY',reviewer_id='/root/exact_verify77',created_utc=now(),header=pin(H),derivation_audit=[dict(step=1,claim='Actual parent76 supplies joint Borel next and every finite record, internally from the six analytic source assumptions. Parent77 supplies probability, measurable coordinate marginals Exp1 and full iid input family. No such ingredient is a public provider binder.'),dict(step=2,claim='Deterministic induction in j establishes prefix causality: record0 is constant; record(j+1) consumes recordj and threshold e j only. For each j< n+1, j<=n, so history depends only w k for k<n. Sum.inr absorbs independently of future thresholds.'),dict(step=3,claim='For fixed n, each coordinate k<n is measurable from past n by comap inclusion. Compose Real.toNNReal and measurable next, inductively build records j<=n, then finite Pi history. This proves past measurability directly; bare set-theoretic causality alone would not justify measurable factorization in arbitrary spaces.'),dict(step=4,claim='Every raw tail coordinate is measurable. Injection k↦n+k preserves the iid family and each marginal is Exp1. The actual countable-product joint-law theorem identifies the ENTIRE tail law with P; coordinate marginal equality or pairwise independence alone is insufficient.'),dict(step=5,claim='Disjoint index sets {k<n} and {k>=n} generate independent sigma algebras under full iid P. history is measurable in the first; all infinitely many tail coordinates are measurable in the second. Independence of the full two random objects follows, including the countable tail sigma algebra.'),dict(step=6,claim='The two-object IndepFun pushforward theorem gives joint law=history law×tail law; substitute tail law=P. Product association is exactly ordered (history,tail), with history in Fin(n+1)→record and tail in Nat→Real.'),dict(step=7,claim='For Borel history event A and Borel tail event B, evaluate the restricted-tail map: P({history∈A}∩{tail∈B})=P(history∈A)P(tail∈B)=P(history∈A)P(B). Measure extensionality gives P(A-history)•P. No division or P(A)>0 is needed.')],counterexample_and_boundary_audit=[dict(case='n0',result='History has exactly the deterministic initial record, past0=bottom, tail0=id. Joint law is Dirac(initial history)×P; event mass0 or1, and restricted identity holds.'),dict(case='zero-probability A',result='Restricted source measure and ENNReal0 scalar probability measure both zero. No regular conditional probability version or normalization is asserted.'),dict(case='stopped/infinite wait',result='Once Sum.inr, later records remain stopped and contain no phase at infinity; history still finite-prefix measurable, and unused raw clocks retain their unconditional independent tail law. No conditional event density for the stopped phase is asserted.'),dict(case='negative/zero raw coordinates',result='Real.toNNReal is total and measurable; deterministic causality holds for every w,wprime, including exceptional nonpositive coordinates. Strict positivity is not a new premise and not needed for this independence substrate.'),dict(case='rank0/zero-normal/flat hazard',result='Degenerate dynamics may stop or leave identity reflection. No nondegeneracy, strictly increasing hazard, finite next wait or positive cap appears in probability statement.'),dict(case='off-by-one challenge',result='Fin(n+1) records are indexed0..n; recordn uses clocks0..n-1. An additional recordn+1 or tail starting before n would overlap used coordinates. Exact candidate avoids that overlap.'),dict(case='hidden assumptions',result='No supplied measurable recursion, iid family, probability P, conditional distribution, transition kernel, path-space law or nonexplosion premise. Existing source hypotheses are stronger than generic independence needs but preserved exactly.'),dict(case='scope',result='Fixed deterministic n and fixed y/ref/z0; no random stopping, physical-time residual threshold, memoryless restart/CK, conditional next-event density, full A7 or parameter-uniform AE claim.')],required_repairs=[],proof_implementation=False,final_source_verdict=False))
assert H.read_bytes()==hraw
for p in inputs:assert pin(p) in read(O/'input-freeze87.json')['actual_inputs']
for p,v in prior.items():assert pin(R/p)['raw_sha256']==v
put('lookup-diagnosis87.json',dict(status='CORRECTED_PARENT_FILENAME_LOOKUP_ONLY',initial_tool_chunk='548718',initial_lookup='AutoSamplingTheory/ExampleCases/ProximalBPS/FiniteJumpRecursion.lean',native_result='rg reported path missing; actual imported file is ActualFiniteJumpRecursion.lean and was then read directly.',source_or_mathematical_repair=False))
put('decision87.json',dict(status='ACCEPTED_WHOLE_HEADER_MATHEMATICS_AND_TYPE_ONLY',reviewer_id='/root/exact_verify77',created_utc=now(),header=pin(H),whole_header_typecheck=pin(O/'whole-header-typecheck87.receipt.json'),parent_API_check=pin(O/'parent-api-check87.receipt.json'),definition_readback=pin(O/'definition-readback87.json'),mathematical_review=pin(O/'mathematical-review87.json'),required_repairs=[],six_original_analytic_binders_preserved=True,complete_private_Prop_typechecked=True,all21collaborator_RAWs_preserved=True,StatementSeal=False,PROVED=False,VERIFIED=False,remaining='Root may seal exact header only after its independent source-scope review; future BODY requires separate full mathematics/blind/source/exact-commit admission. G86-11 independence substrate only; all global path/restart/A7/operator results remain OPEN.'))
put('run-manifest87.json',dict(status='CLOSED',created_utc=now(),reviewer_id='/root/exact_verify77',actual_inputs=read(O/'input-freeze87.json')['actual_inputs'],terminal_receipts=[pin(O/'whole-header-typecheck87.receipt.json'),pin(O/'parent-api-check87.receipt.json')],decision=pin(O/'decision87.json'),proof_credit=False,production_or_shared_mutation=False,native_reasoning_trajectory_claimed=False))
artifacts=[pin(p) for p in sorted(O.iterdir()) if p.is_file() and p.name!='closed-RAW-manifest87.json']
put('closed-RAW-manifest87.json',dict(status='CLOSED_RAW_NONCIRCULAR',created_utc=now(),reviewer_id='/root/exact_verify77',frozen_current_inputs=read(O/'input-freeze87.json')['actual_inputs'],owned_artifacts=artifacts,self_hash_intentionally_omitted=True,all21collaborator_RAWs_preserved=True,header_only=True))
for e in artifacts:assert pin(R/e['path'])['raw_sha256']==e['raw_sha256']
print(json.dumps(dict(status='ACCEPTED_HEADER_ONLY_NATIVE_CLOSED_REHASH_PASS',header=pin(H),decision=pin(O/'decision87.json'),manifest=pin(O/'closed-RAW-manifest87.json'),whole_header_receipt=pin(O/'whole-header-typecheck87.receipt.json'),parent_API_receipt=pin(O/'parent-api-check87.receipt.json'))),flush=True)
