from pathlib import Path
import re,json,hashlib,datetime
root=Path('E:/Samplinglib'); out=root/'runs/20261007-companion-priority/balanced-rademacher-clt/whole-proof-review'
actor='gaussian_domain_preproof_reviewer_29'
def h(b):return hashlib.sha256(b).hexdigest()
def lf(b):return b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def put(name,data):
 b=(json.dumps(data,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
 with (out/name).open('xb') as f:f.write(b)
 return {'path':str((out/name).relative_to(root)).replace('\\','/'),'bytes':len(b),'raw_sha256':h(b),'lf_sha256':h(lf(b))}
manifest=json.loads((out/'input-bindings.initial.json').read_bytes())['inputs']
paths={x['path'] for x in manifest}
parents={
 'Mathlib/Algebra/BigOperators/Ring/Finset.lean':[('Fintype.sum_pow',292,296)],
 'Mathlib/MeasureTheory/Measure/Count.lean':[('actual finite count and singleton values',29,33),('count_apply_finite',43,61),('count_real_singleton',120,135),('finite count instance',157,167)],
 'Mathlib/MeasureTheory/Integral/Bochner/SumMeasure.lean':[('genuine finite Bochner sum',175,177),('integral_fintype',210,218)],
 'Mathlib/MeasureTheory/Integral/Bochner/Basic.lean':[('integral_smul_measure',1013,1025),('integral_map',1032,1053)],
 'Mathlib/MeasureTheory/Function/L1Space/Integrable.lean':[('Integrable.of_finite',166,169)],
 'Mathlib/MeasureTheory/Measure/ProbabilityMeasure.lean':[('actual measure subtype',101,120),('weak topology',286,290)],
 'Mathlib/MeasureTheory/Measure/CharacteristicFunction/Basic.lean':[('charFun actual integral',127,133),('charFun_map_mul_comp',205,218)],
 'Mathlib/Probability/CentralLimitTheorem.lean':[('actual scalar CLT standing scope and public leaf',41,72)],
 'Mathlib/MeasureTheory/Measure/LevyConvergence.lean':[('canonical Real standing classes',40,41),('actual weak/CF equivalence',198,221)],
 'Mathlib/Probability/Distributions/Gaussian/Real.lean':[('mean and NNReal variance definition',219,233),('exact Gaussian CF',486,491)],
 'Mathlib/MeasureTheory/MeasurableSpace/Basic.lean':[('actual finite/countable measurability',287,289)],
 'Mathlib/MeasureTheory/Measure/Typeclasses/Probability.lean':[('actual probability map premise',116,126)],
 'Mathlib/MeasureTheory/Measure/Dirac.lean':[('actual massone constant pushforward',90,101)],
 'Mathlib/Order/Filter/AtTopBot/Basic.lean':[('actual successor atTop map',331,332)],
 'Mathlib/Analysis/Complex/Exponential.lean':[('Complex.exp_sum',145,147)],
 'Mathlib/Data/Fintype/BigOperators.lean':[('Fintype.card_fun',197,201)],
 'Mathlib/Data/Fintype/Card.lean':[('Bool cardinality',181,183),('Fin cardinality',494,498)],
 'Mathlib/MeasureTheory/Measure/CharacteristicFunction/TaylorExpansion.lean':[('true nonzero second integral -> square L1 -> CF expansion',140,159)],
 'Mathlib/Analysis/SpecialFunctions/Complex/LogBounds.lean':[('actual power asymptotics',358,381)]}
apiregions=[]
for f,regions in parents.items():
 p='.lake/packages/mathlib/'+f;b=(root/p).read_bytes()
 if p not in paths:
  i=len(manifest);rn=f'input.{i:03d}.raw.snapshot';ln=f'input.{i:03d}.lf.snapshot'
  with (out/rn).open('xb') as w:w.write(b)
  with (out/ln).open('xb') as w:w.write(lf(b))
  manifest.append({'path':p,'raw_sha256':h(b),'lf_sha256':h(lf(b)),'bytes':len(b),'raw_snapshot':rn,'lf_snapshot':ln,'role':'actual bounded canonical parent API inspected','freeze_pin_matches':None});paths.add(p)
 lines=b.splitlines(keepends=True)
 for label,lo,hi in regions:
  rb=b''.join(lines[lo-1:hi]); name=f'parent-region.{len(apiregions):03d}.raw.snapshot'
  with (out/name).open('xb') as w:w.write(rb)
  apiregions.append({'api':label,'path':p,'lines':[lo,hi],'raw_sha256':h(rb),'lf_sha256':h(lf(rb)),'snapshot':name,'source_file_raw_sha256':h(b)})

source='AutoSamplingTheory/TechnicalLemmas/Probability/BalancedRademacherCLT.lean';test='Tests/BalancedRademacherCLT.lean'
src=lf((root/source).read_bytes()).decode(); t=lf((root/test).read_bytes()).decode()
seals=json.loads((root/'runs/20261007-companion-priority/balanced-rademacher-clt/preproof/statement-seals.accepted.json').read_bytes())
sealed=seals['signatures'][0]['signature_text'].encode()
start=src.index('theorem balanced_count_sum_tendsto_gaussian :'); stop=src.index(' := by',start)
extracted=(src[start:stop]+'\n').encode()
assert extracted==sealed and len(extracted)==573 and h(extracted)=='271595fa838cf28466cf90591d2c6aaa1024b42a1af73d85eee25cfc32e04777'
with (out/'exact-sealed-header.lf.snapshot').open('xb') as w:w.write(extracted)

def strip(s):
 # Nested Lean comments, retaining line numbers. Strings ignored for token scan below.
 ans=[];i=0;depth=0
 while i<len(s):
  if s[i:i+2]=='/-':depth+=1;ans.extend('  ');i+=2
  elif depth and s[i:i+2]=='-/':depth-=1;ans.extend('  ');i+=2
  elif depth:ans.append('\n' if s[i]=='\n' else ' ');i+=1
  elif s[i:i+2]=='--':
   j=s.find('\n',i);j=len(s) if j<0 else j;ans.extend(' '*(j-i));i=j
  else:ans.append(s[i]);i+=1
 return ''.join(ans)
scans=[];imports={}
for p,s in [(source,src),(test,t)]:
 code=strip(s);im=re.findall(r'^[ \t]*import[ \t]+([^\n]+)',code,re.M);imports[p]=im
 patterns={'axiom_sorry_admit':r'\b(?:axiom|sorry|admit)\b','True_closure':r'Prop[ \t\n]*:=[ \t\n]*True|:=[ \t\n]*trivial','unsafe_implemented_by':r'\b(?:unsafe|implemented_by|extern)\b'}
 hits={name:[{'line':code[:m.start()].count('\n')+1,'text':m.group()} for m in re.finditer(pat,code)] for name,pat in patterns.items()}
 assert not any(hits.values()),p
 scans.append({'path':p,'patterns':hits,'fake_closure_hits':0})
assert not any(i.startswith('AutoSamplingTheory.') for i in imports[source])
private=re.findall(r'^[ \t]*private[ \t]+(?:def|theorem|instance)[ \t]+([A-Za-z_][A-Za-z_0-9]*)',strip(src),re.M)
assert len(private)==14,private
provider_deps={
 'countLaw':[], 'countLaw_probability':['countLaw'], 'countLaw_integral':['countLaw'], 'sign':[],
 'sign_mean':['countLaw_integral','sign'], 'sign_second_moment':['countLaw_integral','sign'],
 'coordinateLaw':['countLaw','sign'], 'coordinate_charFun':['coordinateLaw','countLaw_integral','sign'],
 'unscaled_charFun':['countLaw_integral','coordinate_charFun','sign'], 'normalizedSum':['sign'],
 'actualLaw':['countLaw','countLaw_probability','normalizedSum'], 'actualLaw_zero':['actualLaw','normalizedSum','countLaw_probability'],
 'normalized_charFun':['actualLaw','normalizedSum','unscaled_charFun'],
 'actualLaw_tendsto':['actualLaw','normalized_charFun','coordinateLaw','countLaw_probability','sign','sign_mean','sign_second_moment'],
 'balanced_count_sum_tendsto_gaussian':['actualLaw','actualLaw_zero','actualLaw_tendsto']}
reachable=set()
def reach(x):
 if x in reachable:return
 reachable.add(x)
 for p in provider_deps[x]:reach(p)
reach('balanced_count_sum_tendsto_gaussian')
assert set(private)<=reachable
fresh=[]
expected=['AutoSamplingTheory.TechnicalLemmas.Probability.BalancedRademacherCLT.balanced_count_sum_tendsto_gaussian','Tests.BalancedRademacherCLT.actual_first_moments_and_limit','Tests.BalancedRademacherCLT.actual_zero_second_moment']
for name in ['focused','direct-test-axioms']:
 st=json.loads((out/(name+'.status.json')).read_bytes());b=(out/(name+'.log')).read_bytes();assert st['exit_code']==0 and h(b)==st['log_raw_sha256']
 reports=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",b.decode(),re.S)
 assert [x[0] for x in reports]==expected,(name,reports)
 assert all(set(v.strip() for v in ax.replace('\n',' ').split(','))=={'propext','Classical.choice','Quot.sound'} for _,ax in reports)
 fresh.append({'name':name,'status':st,'axiom_reports':[{'declaration':d,'axioms':['propext','Classical.choice','Quot.sound']} for d,_ in reports]})

api=put('parent-api-review.json',{'actor':actor,'regions':apiregions,'scope':'actual bounded canonical direct parent definitions and scalarCLT analytic dependency premises; trusted existing Mathlib, no broad external closure proof claim'})
closure=put('reachability-fake-closure.json',{'actor':actor,'production_imports':imports[source],'test_imports':imports[test],
 'ASTIS_recursive_production_closure':[source],'ASTIS_existing_parent_modules':[],
 'all_private_providers':private,'reachable_ASTIS_private_and_public_declarations':sorted(reachable),'private_provider_edges':provider_deps,
 'implicit_instance_edges_explicit':['actualLaw and scalarCLT countLaw Bool use countLaw_probability; actual finite Fin n→Bool and Bool are inhabited and have canonical measurable singletons'],
 'unused_private_provider_count':0,'fake_closure_scan':scans,'fake_closure_hits':0,'public_output_wrapper':False,
 'why_substantive':'The only public theorem constructs the actual law family and proves its real count CF factorization and weak limit through internal producers; no supplied limit/law/moment premise is restated.',
 'scope':'complete reachable ASTIS source closure consists exactly of the new production module; tests import only it. Existing Mathlib kernel/API accepted as library background; no whole-project scan inferred.'})
body_audit=[
 {'component':'countLaw / probability','verdict':'sound','reason':'Inverse ENNReal cardinal times true count. Nonempty assumption private to generic probability provider ensures card>0; all actual Bool/function carriers inhabited for every N. Card cast finite gives inv_mul_cancel, actual massone.'},
 {'component':'countLaw_integral','verdict':'sound','reason':'True finite count measure supplies genuine Integrable.of_finite before integral_fintype; singleton masses1 and scalar toReal inverse give actual average. Generic empty-carrier case harmless integral0/empty sum0, never falsely probability.'},
 {'component':'sign_mean / sign_second_moment','verdict':'sound','reason':'Exact true1/false-1 under actual countLaw Bool, two points each1/2; actual mean0 and secondmoment1 are proved, not supplied.'},
 {'component':'coordinateLaw / coordinate_charFun','verdict':'sound','reason':'Actual measurable sign pushforward. Continuous complex exponential is AEstronglymeasurable; integral_map matches same actual law and finite integral gives 1/2 times genuine two-point characteristic sum.'},
 {'component':'unscaled_charFun','verdict':'sound','reason':'Complex.exp_sum converts true sign sum exponential into product over coordinates. Fintype.sum_pow is exact finite configuration identity. Card2^n and Complex cast/inverse/mul_pow yield 2^-n*(sum two exponentials)^n=(one-coordinate CF)^n. n0 empty product gives1, no fake product law assumption.'},
 {'component':'normalizedSum / actualLaw / normalized_charFun','verdict':'sound','reason':'Same inverse sqrt(n) times actual sign sum; finite countability gives measurable map; genuine probability provider yields actual ProbabilityMeasure. charFun_map_mul_comp supplies exact scale sqrt(n)^-1*t, no Fourier normalization change.'},
 {'component':'actualLaw_zero','verdict':'sound','reason':'Fin0 sum is empty, so S0 identically0. True massone constant map is dirac0. Function carrier atn0 singleton, not empty, and totalized inverse sqrt0 does not introduce arbitrary Gaussian law.'},
 {'component':'actualLaw_tendsto','verdict':'sound','reason':'Mathlib scalar CF leaf applied only to actual countLaw Bool/sign with internally derived AEMeasurability, mean0 and moment2=1. P.map sign is exactly coordinateLaw. Target CF matches actual gaussianReal(mean0,varianceNNReal1)=exp(-t²/2). Levy uses canonical finite-dimensional Real Borel structure to prove weak ProbabilityMeasure convergence.'},
 {'component':'public assembly','verdict':'sound','reason':'One actualLaw family witnesses all map identities by definitional equality, zero branch and successor-composed weak limit. Exact573-byte LF header matches original seal; no public hypotheses.'},
 {'component':'Tests','verdict':'meaningful','reason':'First test forces same law atN1 through public actual hmap, genuine two equally weighted count configurations, mean0 and secondmoment1 with the same limit. Second forces true N0 dirac and secondmoment0. Genuine finite/Dirac L1 prevents totalized-integral counterfeit; three fresh axiom reports standard3.'}]

# All initially frozen mathematical inputs and newly inspected parents must still match at close.
for x in manifest:
 b=(root/x['path']).read_bytes();assert h(b)==x['raw_sha256'] and h(lf(b))==x['lf_sha256'],x['path']
for name in ['focused.log','focused.status.json','direct-test-axioms.log','direct-test-axioms.status.json']:
 p=out/name;b=p.read_bytes();manifest.append({'path':str(p.relative_to(root)).replace('\\','/'),'raw_sha256':h(b),'lf_sha256':h(lf(b)),'bytes':len(b),'role':'fresh independent foreground compilation evidence'})
bindings=put('input-bindings.final.json',{'actor':actor,'input_count':len(manifest),'inputs':manifest,'all_original_math_freeze_14_input_pins_match':True,
 'source_graph_inventory':'raw/LF binding only; author did NOT issue source topology verdict','mutable_root_metadata_blind_source_reviews_read':False,'all_input_hashes_rechecked_unchanged':True})
review=put('math.review.json',{'actor':actor,'verdict':'ACCEPTED_SCOPED_WHOLE_MATHEMATICAL_PROOF','blockers':[],
 'advance_id':'ASTIS-SA-20261007-BalancedRademacherCLT','reviewed_base_commit_context':'6d5df34cdb124e28022f16f566ff549145eb7e65','checked_identity':'exact frozen worktree mathematical files and raw/LF parent bindings, not an exactcommit VERIFIED transition',
 'exact_statement':{'declaration':expected[0],'sealed_LF_bytes':573,'sealed_raw_original_sha256':h(sealed),'production_extracted_LF_sha256':h(extracted),'matches_sealed_bytes':True,'public_mathematical_binders':[]},
 'mathematical_file_pins':[x for x in manifest if x['path'] in [source,test]],'input_bindings':bindings,'actual_parent_API_review':api,
 'all_private_providers_reviewed':14,'body_mathematical_audit':body_audit,'reachability_fake_closure':closure,'fresh_checks':fresh,
 'actual_definition_semantics':{'measure':'actual inverse-card count law, cardinal2^N on FinN→Bool','sign':'true1,false-1','normalized_sum':'sqrt(N:Real)^-1 times finite real sign sum','zero':'actualN0 Dirac0, secondmoment0','positive_single_coordinate':'actualBool mean0 secondmoment1, notN0 variance1','limit':'actual gaussianReal0 varianceNNReal1 ProbabilityMeasure weak topology','centering':'actual single-coordinate sign expectation0, no supplied abstract law or moments'},
 'hidden_domain_audit':{'all_finite_measures_genuine':True,'genuine_finite_Bochner_L1':True,'actual_AEmeasurable_maps':True,'complex_exponential_integrands':'continuous bounded on real target and finite/countable source; no false integral-undef closure','private_generic_empty_carrier':'countLaw_integral valid; probability provider correctly requires Nonempty internally','no_caller_certificates':['probability','moment','actual law/map','independence','CLT','CF factorization','weak limit']},
 'conceptual_mirror_audit':{'status':'none-found','reason':'This delta proves exact formal finite-algebra/characteristic-law implication for the same probability family and canonical Real weak topology. Existing normalized-count substrate recurs without a new weaker cross-domain hypothesis/conclusion transport; no candidate conceptual bridge discovered.'},
 'role_boundary':{'root_created_proof':True,'source_graph_authored_by_reviewer':True,'source_graph_self_validation':False,'blind_decoder_or_source_verdict_read':False,'new_production_or_shared_metadata_writes':False,'self_VERIFIED':False},
 'remaining_truth_boundary':['No Gaussian entropy or flip-energy limit','No compact Gaussian functionLSI or noncompact sqrt-density domain extension','No finite-Hilbert Gaussian tensorization or T2','No FIRST SPHMC4.6 / bias / main / work / composition completion','Source-fidelity/source-topology and exactcommit/contributor/publication/aggregate admission remain distinct'],
 'compiler':'fresh exclusive foreground lake build3160 PASS plus direct Test Lean PASS; each of3 axiom sets exactly propext/Classical.choice/Quot.sound; compiler CLOSED'})
material={'actor':actor,'review':review,'bindings':bindings,'parent_API':api,'reachability_scan':closure,
 'verdict':'ACCEPTED_SCOPED_WHOLE_MATHEMATICAL_PROOF','self_source_validation':False,'compiler_terminal':True}
runhash=h(json.dumps(material,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
run=put('run.json',dict(material,deterministic_run_sha256=runhash,status='CLOSED'))
p=out/'lease.json';lease=json.loads(p.read_bytes());assert lease['compiler_lease']=='CLOSED'
lease.update(status='CLOSED',read_lease='CLOSED',write_lease='CLOSED',compiler_lease='CLOSED',closed_utc=datetime.datetime.utcnow().isoformat()+'Z',
 verdict='ACCEPTED_SCOPED_WHOLE_MATHEMATICAL_PROOF',run=run,deterministic_run_sha256=runhash)
p.write_text(json.dumps(lease,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'review':review,'run':run,'runhash':runhash,'all_leases':'CLOSED','input_count':len(manifest),'private_providers':14,'fake_closure_hits':0,'fresh_checks':'focused3160 and direct3standard3 PASS'},indent=2))
