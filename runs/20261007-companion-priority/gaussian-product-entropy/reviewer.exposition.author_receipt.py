from pathlib import Path
import json,hashlib,re,subprocess
from html.parser import HTMLParser
from datetime import datetime,timezone
R=Path('E:/Samplinglib');B='runs/20261007-companion-priority/gaussian-product-entropy/';O=R/B
COMMIT='7e02d986a20af81d3c9ea027b3dcded6a8c25ffa';ACTOR='gaussian_domain_preproof_reviewer_29'
PROD='AutoSamplingTheory/TechnicalLemmas/InformationTheory/ProductEntropy.lean';TEST='Tests/ProductEntropy.lean'
SLUG='bounded-product-entropy';DECL='AutoSamplingTheory.TechnicalLemmas.InformationTheory.ProductEntropy.bounded_product_entropy_subadditivity'
COMP='_site/example-cases/samplewiki/companions/smoothed-picard-hmc.html';MOD='_site/modules/autosamplingtheory-technicallemmas-informationtheory-productentropy.html';TP='_site/modules/tests-productentropy.html';GRAPH='_site/data/underlying-lean-graph.json'
paths=[PROD,TEST,'AutoSamplingTheory/TechnicalLemmas/Analysis/Calculus/Cutoff.lean',
 'website/content/declaration_lessons/'+SLUG+'.json','website/content/publications/'+SLUG+'.json',
 'research-wiki/frontier-cells/ASTIS-SW-SPHMC-bounded-product-entropy.json',
 'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261007-BoundedProductEntropy.json',
 B+'publication-plan.json',B+'math-freeze.json',
 'runs/20261007-companion-priority/gaussian-product-entropy-preproof/signature.prospective.txt',
 'runs/20261007-companion-priority/gaussian-product-entropy-preproof/statement-seals.accepted.json',
 B+'integration.json',B+'verified.json',B+'whole-proof-review/math.review.json',B+'source.0.review.json',
 'runs/20261007-companion-priority/gaussian-product-entropy-source-graph-review/source-topology-review.repaired.json',
 B+'graph.0.json',COMP,MOD,TP,GRAPH]
def lf(b):return b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
H=lambda b:hashlib.sha256(b).hexdigest()
def enc(o):return (json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
def put(n,b):
 if not isinstance(b,bytes):b=enc(b)
 with (O/n).open('xb') as f:f.write(b)
 return H(b)
def git(*args):return subprocess.run(['git',*args],cwd=R,capture_output=True)
def load(p):return json.loads((R/p).read_bytes())
assert git('rev-parse','HEAD').stdout.decode().strip()==COMMIT
pins=[];data={p:(R/p).read_bytes() for p in paths}
for i,p in enumerate(paths):
 b=data[p];g=git('show',COMMIT+':'+p)
 rec={'path':p,'raw_sha256':H(b),'lf_sha256':H(lf(b)),'bytes':len(b),'raw_snapshot':f'reviewer.exposition.input.{i:03d}.raw.snapshot','lf_snapshot':f'reviewer.exposition.input.{i:03d}.lf.snapshot','tracked':g.returncode==0}
 if g.returncode==0:
  rec.update({'Git_commit':COMMIT,'Git_raw_sha256':H(g.stdout),'Git_lf_sha256':H(lf(g.stdout)),'working_equals_Git_LF':lf(b)==lf(g.stdout)})
  assert rec['working_equals_Git_LF'],p
 else:rec['untracked_boundary']='Current generated static bytes hash-bound only; no Git/browser/rendered/live delivery inferred.'
 pins.append(rec)
by={p['path']:p for p in pins};freeze=load(B+'math-freeze.json')
for p in [PROD,TEST,paths[9]]:
 a=next(x for x in freeze['inputs'] if x['path']==p);assert a['raw_sha256']==by[p]['raw_sha256'] and a['lf_sha256']==by[p]['lf_sha256']
prod=lf(data[PROD]).decode();test=lf(data[TEST]).decode();suffix=prod[prod.index('theorem bounded_product_entropy_subadditivity'):]
header=suffix.split(' := by',1)[0]+'\n';assert header.encode()==data[paths[9]] and len(header.encode())==1029
u=load(paths[3])['units'][0];pub=load(paths[4])['items'][0]
assert u['declaration']==DECL and u['astis_dependencies']==[] and len(u['steps'])==6
imports=[x for x in prod.splitlines() if x.startswith('import ')];assert not any('AutoSamplingTheory' in x for x in imports)
providers=re.findall(r'^private (?:def|theorem) (\w+)',prod,re.M);assert len(providers)==15
assert all(x in prod for x in ['hF.stronglyMeasurable.integral_prod_right\'','hF.stronglyMeasurable.integral_prod_left\'','(iA.mul_prod iB).div_const m','integral_prod_mul','scalar_logsum','tendsto_integral_of_dominated_convergence','le_of_tendsto_of_tendsto'])
class Extract(HTMLParser):
 def __init__(self):super().__init__();self.codes=[];self.cur=[];self.pre=False;self.text=[];self.links=[];self.details=[]
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='pre':self.pre=True;self.cur=[]
  if t=='a':self.links.append(d.get('href'))
  if t=='details':self.details.append(d)
 def handle_endtag(self,t):
  if t=='pre':self.codes.append(''.join(self.cur));self.pre=False
 def handle_data(self,d):
  self.text.append(d)
  if self.pre:self.cur.append(d)
s=lf(data[COMP]).decode();start=s.index('<section id="'+SLUG+'"');depth=0
for m in re.finditer(r'</?section\b[^>]*>',s[start:]):
 depth+=-1 if m.group().startswith('</') else 1
 if depth==0:end=start+m.end();break
sec=s[start:end];h=Extract();h.feed(sec);text=''.join(h.text)
assert len(h.codes)==2 and h.codes[0].strip()==header.strip() and h.codes[1].strip()==suffix.strip()
assert all('open' not in d for d in h.details)
steps=[]
for st in u['steps']:
 assert st['title'] in text and st['text'] in text and st['formula'] in text
 steps.append({'title':st['title'],'formula':st['formula']})
for phrase in ['every fixed-coordinate slice','Zero mass and zero fibers are included','not a printed SPHMC result','Finite iteration, Gaussian tensorization/Hilbert law/Parseval','Cross-log terms are never sent through a zero-fiber limit']:
 assert phrase in text,phrase
assert any('modules/autosamplingtheory-technicallemmas-informationtheory-productentropy.html#complete-module-source' in (x or '') for x in h.links)
assert not any('tests-productentropy' in (x or '') for x in h.links)
modules={}
for page,code in [(MOD,prod),(TP,test)]:
 q=Extract();q.feed(lf(data[page]).decode());c=max(q.codes,key=len);assert lf(c.encode()).decode()==code,page
 modules[page]={'complete_actual_source_exact_LF':True,'source_sha256':H(code.encode()),'bytes':len(code.encode())}
assert all(x in test for x in ['zero_product_entropy','actual_compact_product_entropy','compact_zero_fiber','actual_probe_signed','actual_probe_C2_compact','smoothUnitCutoff_hasCompactSupport','sq_nonneg (signedProbe z)'])
assert test.count('#print axioms ')==3
v=load(B+'verified.json');assert v['verified_commit']=='913438726472dcac2483cefbe6b4b2f4746cbe74'
audit=load(paths[6]);assert audit['publication_context']['file']==H(prod.encode()) and audit['publication_context']['current_lean_module']==prod
assert load(B+'source.0.review.json')['verdict']=='equivalent-after-elaboration'
integ=load(B+'integration.json');graph=json.loads(data[GRAPH]);module='module:'+DECL.rsplit('.',1)[0];decl='decl:'+DECL
edges=[e for e in graph['edges'] if module in [e['source'],e['target']] or decl in [e['source'],e['target']] or 'module:Tests.ProductEntropy' in [e['source'],e['target']]]
nodeids={module,decl,'module:Tests.ProductEntropy','semantic-audit:ASTIS-RT-20261007-BoundedProductEntropy'}
nodes=[n for n in graph['nodes'] if n['id'] in nodeids]
assert any(e['source']==module and e['target']==decl and e['relation']=='declares' for e in edges)
assert any(e['source']==decl and e['relation']=='source correspondence; not a Lean dependency' for e in edges)
assert not any(e['target']==module and e['relation']=='imports' and e['source'].startswith('module:AutoSamplingTheory') for e in edges)
assert any(e['source']=='module:AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff' and e['target']=='module:Tests.ProductEntropy' for e in edges)
checks={'schema_version':1,'checked_commit':COMMIT,'six_steps_formula_and_natural_language_match_actual_code':True,
 'generic_arbitrary_probability_binary_product_only':True,'pointwise_nonnegative_globally_bounded_measurable_F_scope':True,
 'coefficient_one_exact_joint_plus_mass_Phi_vs_both_marginal_Phi':True,'actual_Bochner_A_B_m_no_conditional_RN_representative':True,
 'all_x_and_all_y_slice_L1_including_zero_fibers_are_outputs':True,'joint_marginal_and_Phi_true_L1_internal':True,
 'positive_R_AB_over_m_true_mass_identity_and_weighted_log_Fubini':True,
 'scalar_logsum_orientation_actual_u_minus1_le_u_logu':True,'epsilon_1_over_nplus1_true_probability_integral_shifts':True,
 'bounded_continuous_tlogt_DCT_only_entropy_terms_no_zero_crosslog_limit':True,'zero_mass_no_positive_mass_normalization_or_inequality_binder':True,
 'actual_ASTIS_production_parents':[],'direct_Mathlib_imports':imports,'private_provider_count':len(providers),'private_provider_names':providers,
 'sealed_header_exact_bytes':{'bytes':len(header.encode()),'sha256':H(header.encode())},'production_Test_signature_math_freeze_raw_LF_unchanged':True,
 'complete_folded_actual_header_and_proof_suffix':True,'folded_details_closed':True,'complete_source_and_Test_pages':modules,
 'actual_signed_nonseparable_C2_compact_squared_observer_and_zero_Tests_visible':True,
 'Tests_cutoff_parent_is_test_only_not_production_formal_parent':True,'companion_Test_page_link':False,
 'no_fullFin_Gaussian_Hilbert_noncompact_LSI_T2_PBPS_SPHMC_main_cost_or_live_claim':True,
 'J_notation':'J_F,J_A,J_B denote the displayed actual Phi integrals; no normalized KL interpretation.',
 'canonical_mutations':False,'compiler_started':False,'blockers':[]}
branch={'schema_version':1,'checked_commit':COMMIT,'consumer':DECL,'actual_direct_ASTIS_formal_parents':[],
 'production_Mathlib_imports':imports,'test_only_ASTIS_parent':'AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff',
 'generated_graph_raw_sha256':by[GRAPH]['raw_sha256'],'affected_nodes':nodes,'affected_edges':edges,
 'integration_structural_branch':integ['structural_branch'],'source_correspondence_is_not_Lean_dependency':True,
 'source_topology_boundary':'This reviewer authored39 preproof graph; distinct phase repaired review bound only as provenance, never selfvalidated.'}
provpaths={'source_topology_review':paths[15],'actual_source_review':B+'source.0.review.json','wholeproof_review':B+'whole-proof-review/math.review.json','exact_proof_verified':B+'verified.json'}
seal={'schema_version':1,'verdict':'ACCEPTED_SCOPED_EXPOSITION_SEAL','status':'accepted-scoped','reviewer':ACTOR,'checked_commit':COMMIT,
 'scope':'Bounded STATIC six-formula39 root-authored lesson/generated companion, folded actual public Lean, complete production/Test pages and affected graph branch. No compiler/site rerender/canonical writes/browser/live certification.',
 'independent_from_prose_author':True,'source_graph_author_history':'Reviewer authored39 sourcegraph and earlier statement review; phase source/topology and picard wholemath/exact provenance are separate and not selfvalidated here.',
 'mathematical_declaration':DECL,'mathematical_exposition':'Actual arbitrary probability binary product, bounded pointwise nonnegative measurable F, every fixed slice/joint/marginal true L1, marginal Phi sum <=joint Phi+Phi(actualmass). Internally positive logsum/Fubini comparison, probability regularization and continuous entropy DCT include zero fibers/mass.',
 'formula_proof_steps':steps,'checks':'reviewer.exposition.checks.json','graph_branch':'reviewer.exposition.branch.json','blockers':[],
 'mathematical_and_source_provenance':{k:by[p] for k,p in provpaths.items()},
 'verified_proof_commit':v['verified_commit'],'current_repository_ProofSeal_boundary':'Picard repository check/compiler is exclusive and separate; static seal does not replace mandatory repository gate or exactcommit verification.',
 'FULL_READER_DELIVERY_GAP':{'status':'OPEN','items':['Actual Test tails are not inline in companion39; complete Test module page exists but this section has no Test-page link','CopyLean/source-download behavior not independently executed','Paper/book/chapter bundles not delivered or checked','Browser/device rendering and fold/copy/download interactions not tested','Own39 main merge/deploy/live verification not inferred','Postmerge PURIFIED and human-facing completeness remain open']},
 'remaining_mathematical_boundary':['finite entropy iteration and full Fin product GaussianLSI','Euclidean coordinate/Hilbert law and Parseval transport','noncompact actual32/33 cutoff/W12 GaussianLSI','GaussianT2 and SPHMC FIRST4.6','PBPS/SPHMC main/work/cost/composition'],
 'input_bindings':'reviewer.exposition.inputs.json','static_only':True,'PURIFIED':False,'human_facing_complete':False,'compiler_started':False,
 'leases':{'read':'CLOSED','write':'CLOSED','Python':'CLOSED','compiler':'CLOSED'}}
for pin in pins:put(pin['raw_snapshot'],data[pin['path']]);put(pin['lf_snapshot'],lf(data[pin['path']]))
put('reviewer.exposition.companion-section.raw.snapshot.html',sec.encode());put('reviewer.exposition.folded-proof.raw.snapshot.lean',h.codes[1].encode())
outs={}
for name,obj in [('reviewer.exposition.inputs.json',{'schema_version':1,'checked_commit':COMMIT,'inputs':pins}),('reviewer.exposition.checks.json',checks),('reviewer.exposition.branch.json',branch),('ExpositionSeal.json',seal)]:outs[name]=put(name,obj)
run={'schema_version':1,'actor':ACTOR,'checked_commit':COMMIT,'inputs':[{'path':p['path'],'raw_sha256':p['raw_sha256'],'lf_sha256':p['lf_sha256']} for p in pins],'outputs':outs,'canonical_mutations':False,'compiler_started':False};run['run_sha256']=H(enc(run));put('reviewer.exposition.run.json',run)
for p in pins:assert H((R/p['path']).read_bytes())==p['raw_sha256']
lease=load(B+'reviewer.exposition.lease.json');lease.update({'status':'CLOSED','read_lease':'CLOSED','write_lease':'CLOSED','Python_lease':'CLOSED','compiler_lease':'CLOSED','compiler_status':'NEVER_STARTED','closed_utc':datetime.now(timezone.utc).isoformat(),'seal_raw_sha256':outs['ExpositionSeal.json'],'run_sha256':run['run_sha256'],'input_count':len(pins),'verdict':seal['verdict']});(O/'reviewer.exposition.lease.json').write_bytes(enc(lease))
print(json.dumps({'verdict':seal['verdict'],'checked_commit':COMMIT,'seal_raw_sha256':outs['ExpositionSeal.json'],'run_sha256':run['run_sha256'],'inputs':len(pins),'leases':'CLOSED','delivery_gap':'OPEN'}))
