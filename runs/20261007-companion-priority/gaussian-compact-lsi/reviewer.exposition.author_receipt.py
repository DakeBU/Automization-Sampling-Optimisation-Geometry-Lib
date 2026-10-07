from pathlib import Path
import json,hashlib,re,subprocess
from html.parser import HTMLParser
from datetime import datetime,timezone
R=Path('E:/Samplinglib');B='runs/20261007-companion-priority/gaussian-compact-lsi/';O=R/B
COMMIT='bc6f5b25bd1f98f32465df60f7eb257ba06e3734';ACTOR='gaussian_domain_preproof_reviewer_29'
P='AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/'
PROD=P+'GaussianCompactLogSobolev.lean';TEST='Tests/GaussianCompactLogSobolev.lean'
SLUG='gaussian-compact-log-sobolev';DECL='AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactLogSobolev.compact_gaussian_logSobolev'
PARENTS=['AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.BernoulliLogSobolev.bernoulli_function_logSobolev','AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactEntropy.compact_count_gaussian_entropy_limits','AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianFlipEnergy.compact_count_gaussian_flip_energy_limit']
COMP='_site/example-cases/samplewiki/companions/smoothed-picard-hmc.html';MOD='_site/modules/autosamplingtheory-technicallemmas-functionalinequalities-gaussiancompactlogsobolev.html';TP='_site/modules/tests-gaussiancompactlogsobolev.html'
paths=[PROD,TEST,P+'BernoulliLogSobolev.lean',P+'GaussianCompactEntropy.lean',P+'GaussianFlipEnergy.lean',
 'website/content/declaration_lessons/'+SLUG+'.json','website/content/publications/'+SLUG+'.json',
 'research-wiki/frontier-cells/ASTIS-SW-SPHMC-gaussian-compact-lsi.json','research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261007-GaussianCompactLogSobolev.json',
 B+'publication-plan.json',B+'math-freeze.json',B+'preproof/signature.prospective.txt',B+'preproof/statement-seals.accepted.json',
 B+'integration.json',B+'verified.json',B+'whole-proof-review/math.review.json',B+'source.0.review.json',
 'runs/20261007-companion-priority/gaussian-compact-lsi-source-graph-review/source-topology-review.json',
 COMP,MOD,TP,'_site/theorems/autosamplingtheory-technicallemmas-functionalinequalities-gaussiancompactlogsobolev-compact-gaussian-logsobolev.html',
 '_site/lessons/autosamplingtheory-technicallemmas-functionalinequalities-gaussiancompactlogsobolev-compact-gaussian-logsobolev-59313e321d2a.html']
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
data={p:(R/p).read_bytes() for p in paths};pins=[]
for i,p in enumerate(paths):
 b=data[p];rec={'path':p,'raw_sha256':H(b),'lf_sha256':H(lf(b)),'bytes':len(b),'raw_snapshot':f'reviewer.exposition.input.{i:03d}.raw.snapshot','lf_snapshot':f'reviewer.exposition.input.{i:03d}.lf.snapshot'}
 g=git('show',COMMIT+':'+p);rec['tracked']=g.returncode==0
 if g.returncode==0:
  rec.update({'Git_commit':COMMIT,'Git_raw_sha256':H(g.stdout),'Git_lf_sha256':H(lf(g.stdout)),'working_equals_Git_LF':lf(b)==lf(g.stdout)})
  assert rec['working_equals_Git_LF'],p
 else:rec['untracked_boundary']='Exact current generated or reviewer receipt bytes bound; no Git-tracked page or rendered/browser/live delivery claim inferred.'
 pins.append(rec)
by={x['path']:x for x in pins}
freeze=load(B+'math-freeze.json')
for p in [PROD,TEST,P+'BernoulliLogSobolev.lean',P+'GaussianCompactEntropy.lean',P+'GaussianFlipEnergy.lean',B+'preproof/signature.prospective.txt']:
 a=next(x for x in freeze['inputs'] if x['path']==p);assert a['raw_sha256']==by[p]['raw_sha256'] and a['lf_sha256']==by[p]['lf_sha256'],p
prod=lf(data[PROD]).decode();test=lf(data[TEST]).decode();suffix=prod[prod.index('theorem compact_gaussian_logSobolev'):]
header=suffix.split(' := by',1)[0]+'\n';assert header.encode()==data[B+'preproof/signature.prospective.txt']
assert len(header.encode())==308
u=load('website/content/declaration_lessons/'+SLUG+'.json')['units'][0];pub=load('website/content/publications/'+SLUG+'.json')['items'][0]
assert u['declaration']==DECL and u['astis_dependencies']==PARENTS and len(u['steps'])==4
imports=[x for x in prod.splitlines() if x.startswith('import ')]
for name in ['BernoulliLogSobolev.bernoulli_function_logSobolev','GaussianCompactEntropy.compact_count_gaussian_entropy_limits','GaussianFlipEnergy.compact_count_gaussian_flip_energy_limit']:assert name in prod
assert [x for x in imports if 'AutoSamplingTheory' in x]==['import '+x.rsplit('.',1)[0] for x in PARENTS]
assert all(x in prod for x in ['sub_sq_comm','tEnergy.const_mul','le_of_tendsto_of_tendsto','Eventually.of_forall'])
assert 'private ' not in prod
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
assert 'f may change sign or vanish identically' in text and 'no mass positivity or normalization is assumed' in text
assert 'finite-Hilbert/noncompact GaussianLSI, Gaussian T2, printed FIRST4.6' in text
for par in PARENTS:
 assert par in u['astis_dependencies']
token_links=['bernoullilogsobolev-bernoulli-function-logsobolev','gaussiancompactentropy-compact-count-gaussian-entropy-limits','gaussianflipenergy-compact-count-gaussian-flip-energy-limit']
for token in token_links:assert any(token in (link or '') for link in h.links)
assert not any('tests-gaussiancompactlogsobolev' in (x or '') for x in h.links)
modules={}
for page,code in [(MOD,prod),(TP,test)]:
 q=Extract();q.feed(lf(data[page]).decode());c=max(q.codes,key=len);assert c==code,page
 modules[page]={'complete_actual_source_exact_LF':True,'source_sha256':H(code.encode()),'bytes':len(code.encode())}
assert 'private def signedProbe' in test and 'zero_observer_entropy_bound' in test and 'actual_signed_compact_entropy_bound' in test and test.count('#print axioms ')==3
cell=load('research-wiki/frontier-cells/ASTIS-SW-SPHMC-gaussian-compact-lsi.json');integ=load(B+'integration.json')
notes=[]
if cell.get('blocked',{}).get('status') is False and 'not yet' in cell.get('blocked',{}).get('reason',''):
 notes.append({'field':'cell.blocked.reason','observation':'Inactive historical not-yet wording; not a mathematical premise or current rendered lesson claim.'})
checks={'schema_version':1,'checked_commit':COMMIT,'four_steps_formula_and_natural_language_match_actual_code':True,'only_f_C2_AND_compact_analytic_scope':True,
 'actual_gaussianReal_mean0_variance1':True,'homogeneous_entropy_not_normalized_KL':True,'signed_f_zero_function_zero_mass_included':True,
 'zero_tlogt_no_positive_mass_or_log_domain_certificate':True,'actual_count_probability_L1_and_parent_limits_internal':True,
 'three_actual_ASTIS_parents_directly_called':PARENTS,'half_full_flip_coefficient_times4_exactly2':True,
 'square_orientation_sub_sq_comm_same_actual_energy_and_integral':True,'successor_indices_no_positive_dimension_binder':True,
 'N0_distinction':'No zero-index limit substitution: proof uses N+1. Parent37 empty zero-index flip energy is distinct from derivative observer at0; Gaussian theorem has no N binder.',
 'real_closed_order_nontrivial_atTop_comparison':True,'no_monotonicity_rate_normalization_or_supplied_LSI_binder':True,
 'source_external_real_product_route_vs_authored_Bool_integration_disclosed':True,'sealed_header_exact_bytes':{'bytes':308,'sha256':H(header.encode())},
 'source_Test_three_parents_math_freeze_raw_LF_unchanged':True,'complete_folded_actual_header_and_proof_suffix':True,'folded_details_closed':True,
 'complete_production_all_imports_namespace_context_and_Test_private_signedProbe_pages':modules,
 'actual_zero_and_constructed_signed_cutoff_Tests_visible':True,'actual_three_parent_links_present':True,'companion_Test_page_link':False,
 'no_noncompact_Hilbert_T2_FIRST_main_cost_or_live_completion_claim':True,'canonical_mutations':False,'compiler_started':False,'nonblocking_notes':notes}
branch={'schema_version':1,'checked_commit':COMMIT,'actual_direct_formal_parents':PARENTS,'consumer':DECL,'imports':imports,
 'evidence':'Production imports and actual named calls independently checked against lesson dependencies and current integration structural branch. No edge is inferred merely from conceptual similarity.',
 'integration_structural_branch':integ.get('structural_branch'),'source_topology':'Distinct phase receipt establishes source topology; reviewer authored38 graph and does not revalidate it.'}
provpaths={'source_topology_review':paths[17],'actual_source_review':B+'source.0.review.json','wholeproof_review':B+'whole-proof-review/math.review.json','exact_proof_verified':B+'verified.json'}
seal={'schema_version':1,'verdict':'ACCEPTED_SCOPED_EXPOSITION_SEAL','status':'accepted-scoped','reviewer':ACTOR,'checked_commit':COMMIT,
 'scope':'Bounded STATIC four-step38 source-adjacent exposition plus exact folded actual Lean and complete production/Test pages; independent of root prose author. No compiler, site rebuild, sourcegraph selfvalidation or browser/live certification.',
 'independent_from_prose_author':True,'source_graph_author_history':'Reviewer authored38 preproof source graph. Only distinct phase source/topology receipts are used as provenance; no selfvalidation.',
 'mathematical_declaration':DECL,'mathematical_exposition':'Only real f/C2/compact; true variance1 Gaussian homogeneous entropy <=2 derivative energy; signed/zero included. Genuine actual34 half finite LSI,36 entropy limit,37 fullenergy4, pointwise sub_sq_comm and closed real order supply result without caller domains/certificates.',
 'formula_proof_steps':steps,'checks':'reviewer.exposition.checks.json','graph_branch':'reviewer.exposition.branch.json','blockers':[],
 'mathematical_and_source_provenance':{k:by[v] for k,v in provpaths.items()},
 'current_repository_ProofSeal_boundary':'Picard owns independent repository gate; no pending mutable repository receipt frozen here. Static ExpositionSeal is independent of that gate and does not replace it.',
 'provenance_boundary':'Prior independent source/wholeproof/exact receipts establish their bounded truth; this receipt independently checks actual formulas/prose/code correspondence. Historical conditional37 sourcegraph provenance is not retroactively edited.',
 'FULL_READER_DELIVERY_GAP':{'status':'OPEN','items':['Actual Test tails not inline in companion38 lesson; complete Test module page exists but this section has no Test-page link','CopyLean/source-download controls and actual copy/download behavior not independently executed','Paper/book/chapter bundles not delivered or checked','Browser/device rendered formulas and fold/copy/download interactions not tested','No38 remote CI/main merge/deploy/live evidence inferred','Postmerge PURIFIED and human-facing completeness remain open']},
 'remaining_mathematical_boundary':['continuous product entropy/finite-coordinate tensorization','compact finite-product/Hilbert Gaussian energy transport','noncompact actual32/33 cutoff/W12 extension','full GaussianLSI/T2/SPHMC FIRST4.6','paper main/work/cost/composition'],
 'input_bindings':'reviewer.exposition.inputs.json','static_only':True,'PURIFIED':False,'human_facing_complete':False,'compiler_started':False,
 'leases':{'read':'CLOSED','write':'CLOSED','Python':'CLOSED','compiler':'CLOSED'}}
for pin in pins:put(pin['raw_snapshot'],data[pin['path']]);put(pin['lf_snapshot'],lf(data[pin['path']]))
put('reviewer.exposition.companion-section.raw.snapshot.html',sec.encode());put('reviewer.exposition.folded-proof.raw.snapshot.lean',h.codes[1].encode())
outs={}
for name,obj in [('reviewer.exposition.inputs.json',{'schema_version':1,'checked_commit':COMMIT,'inputs':pins}),('reviewer.exposition.checks.json',checks),('reviewer.exposition.branch.json',branch),('ExpositionSeal.json',seal)]:outs[name]=put(name,obj)
run={'schema_version':1,'actor':ACTOR,'checked_commit':COMMIT,'inputs':[{'path':p['path'],'raw_sha256':p['raw_sha256'],'lf_sha256':p['lf_sha256']} for p in pins],'outputs':outs,'canonical_mutations':False,'compiler_started':False};run['run_sha256']=H(enc(run));put('reviewer.exposition.run.json',run)
for p in pins:assert H((R/p['path']).read_bytes())==p['raw_sha256']
lease=load(B+'reviewer.exposition.lease.json');lease.update({'status':'CLOSED','read_lease':'CLOSED','write_lease':'CLOSED','Python_lease':'CLOSED','compiler_lease':'CLOSED','closed_utc':datetime.now(timezone.utc).isoformat(),'seal_raw_sha256':outs['ExpositionSeal.json'],'run_sha256':run['run_sha256'],'input_count':len(pins),'verdict':seal['verdict']});(O/'reviewer.exposition.lease.json').write_bytes(enc(lease))
print(json.dumps({'verdict':seal['verdict'],'checked_commit':COMMIT,'seal_raw_sha256':outs['ExpositionSeal.json'],'run_sha256':run['run_sha256'],'inputs':len(pins),'leases':'CLOSED','delivery_gap':'OPEN'}))
