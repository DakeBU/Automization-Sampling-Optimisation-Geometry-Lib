import hashlib, json, re, subprocess
from pathlib import Path
from html.parser import HTMLParser
from datetime import datetime, timezone

ROOT = Path('E:/Samplinglib')
OUT = ROOT / 'runs/20261007-companion-priority/gaussian-flip-energy'
COMMIT = '7e293eb0470ea6f97368bbdc539e70609cbb3598'
ACTOR = 'gaussian_domain_preproof_reviewer_29'
BASE = 'runs/20261007-companion-priority/gaussian-flip-energy/'
PROD = 'AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/GaussianFlipEnergy.lean'
TEST = 'Tests/GaussianFlipEnergy.lean'
PARENT = 'AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/GaussianCompactEntropy.lean'
SLUG = 'gaussian-compact-full-flip-energy'
DECL = 'AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianFlipEnergy.compact_count_gaussian_flip_energy_limit'
PARENTDECL = 'AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactEntropy.compact_count_gaussian_entropy_limits'
COMPANION = '_site/example-cases/samplewiki/companions/smoothed-picard-hmc.html'
MODULE = '_site/modules/autosamplingtheory-technicallemmas-functionalinequalities-gaussianflipenergy.html'
TESTPAGE = '_site/modules/tests-gaussianflipenergy.html'
paths = [PROD, TEST, PARENT,
 'website/content/declaration_lessons/'+SLUG+'.json',
 'website/content/publications/'+SLUG+'.json',
 'research-wiki/frontier-cells/ASTIS-SW-SPHMC-gaussian-flip-energy.json',
 'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261007-GaussianFlipEnergy.json',
 BASE+'publication-plan.json', BASE+'math-freeze.json',
 BASE+'preproof/statement-seals.accepted.json', BASE+'preproof/signature.prospective.txt',
 BASE+'integration.json', BASE+'verified.json', BASE+'whole-proof-review/math.review.json',
 BASE+'source.0.review.overlay1.json', BASE+'dependency-metadata-overlay1/overlay1.review.json',
 'runs/20261007-companion-priority/gaussian-flip-energy-source-graph-review/source-topology-review.repaired.json',
 BASE+'reviewer.repository.ProofSeal.json',
 COMPANION, MODULE, TESTPAGE,
 '_site/theorems/autosamplingtheory-technicallemmas-functionalinequalities-gaussianflipenergy-compact-count-gaussian-flip-energy-limit.html',
 '_site/lessons/autosamplingtheory-technicallemmas-functionalinequalities-gaussianflipenergy-compact-count-gaussian-flip-energy-limit-d4acf9cf0395.html']

def lf(b): return b.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
def sha(b): return hashlib.sha256(b).hexdigest()
def encode(obj): return (json.dumps(obj, ensure_ascii=False, indent=2)+'\n').encode('utf8')
def create(name, b):
 with (OUT/name).open('xb') as h: h.write(b)
def load(path): return json.loads((ROOT/path).read_text(encoding='utf8'))
def git(*args): return subprocess.run(['git', *args], cwd=ROOT, capture_output=True)

assert git('rev-parse', 'HEAD').stdout.decode().strip() == COMMIT
data = {p:(ROOT/p).read_bytes() for p in paths}
bindings = []
for i,p in enumerate(paths):
 b=data[p]; rec={'path':p,'raw_sha256':sha(b),'lf_sha256':sha(lf(b)),'bytes':len(b),
 'raw_snapshot':f'reviewer.exposition.input.{i:03d}.raw.snapshot',
 'lf_snapshot':f'reviewer.exposition.input.{i:03d}.lf.snapshot'}
 g=git('show', COMMIT+':'+p)
 rec['tracked']=g.returncode==0
 if g.returncode==0:
  rec.update({'Git_commit':COMMIT,'Git_raw_sha256':sha(g.stdout),'Git_lf_sha256':sha(lf(g.stdout)),
    'working_equals_Git_LF':lf(b)==lf(g.stdout)})
  assert rec['working_equals_Git_LF'], p
 bindings.append(rec)
by_path={r['path']:r for r in bindings}
freeze=load(BASE+'math-freeze.json')
for p in [PROD,TEST,PARENT,BASE+'preproof/signature.prospective.txt']:
 original=next(x for x in freeze['inputs'] if x['path']==p)
 assert original['raw_sha256']==by_path[p]['raw_sha256'],p
 assert original['lf_sha256']==by_path[p]['lf_sha256'],p
lesson=load('website/content/declaration_lessons/'+SLUG+'.json')['units'][0]
assert lesson['declaration']==DECL
assert len(lesson['steps'])==5
prod=lf(data[PROD]).decode(); test=lf(data[TEST]).decode()
header=prod[prod.index('theorem compact_count_gaussian_flip_energy_limit'):].split(' := by',1)[0]+'\n'
assert header.encode()==data[BASE+'preproof/signature.prospective.txt']
assert lesson['astis_dependencies'][0]==PARENTDECL
assert len(lesson['astis_dependencies'])==1
assert 'GaussianCompactEntropy.compact_count_gaussian_entropy_limits f hf hs' in prod
imports=[l for l in prod.splitlines() if l.startswith('import ')]
assert [l for l in imports if 'AutoSamplingTheory' in l]==['import '+PARENT[:-5].replace('/','.')]

class Extract(HTMLParser):
 def __init__(self):
  super().__init__();self.codes=[];self.cur=[];self.pre=False;self.links=[];self.text=[];self.details=[]
 def handle_starttag(self,t,a):
  attrs=dict(a)
  if t=='pre':self.pre=True;self.cur=[]
  if t=='a':self.links.append(attrs.get('href'))
  if t=='details':self.details.append(attrs)
 def handle_endtag(self,t):
  if t=='pre':self.codes.append(''.join(self.cur));self.pre=False
 def handle_data(self,d):
  self.text.append(d)
  if self.pre:self.cur.append(d)

s=lf(data[COMPANION]).decode();start=s.index('<section id="'+SLUG+'"');depth=0
for m in re.finditer(r'</?section\b[^>]*>',s[start:]):
 depth += -1 if m.group().startswith('</') else 1
 if depth==0: end=start+m.end();break
section=s[start:end]; h=Extract();h.feed(section)
assert len(h.codes)==2
assert h.codes[-1].strip()==prod[prod.index('theorem compact_count_gaussian_flip_energy_limit'):].strip()
assert h.codes[0].strip()==header.strip()
assert h.details and all('open' not in d for d in h.details)
step_records=[]
for step in lesson['steps']:
 assert step['title'] in ''.join(h.text)
 assert step['formula'] in ''.join(h.text)
 step_records.append({'title':step['title'],'formula':step['formula']})
modules={}
for page,source in [(MODULE,prod),(TESTPAGE,test)]:
 q=Extract();q.feed(lf(data[page]).decode()); code=max(q.codes,key=len)
 assert code==source,page
 modules[page]={'complete_source_exact_LF':True,'source_sha256':sha(source.encode()),'code_bytes':len(code.encode())}
text=''.join(h.text)
assert '16BK/sqrt(N)' in text and 'N0 fullflip energy is an empty sum equal0' in text
assert 'derivative observer fprime(0)^2 may be nonzero' in text
assert 'Compact GaussianLSI, finite-Hilbert/noncompact extension, T2, main results and expected costs remain open' in text
assert not any('tests-gaussianflipenergy' in (x or '') for x in h.links)
proofseal=load(BASE+'reviewer.repository.ProofSeal.json')
assert proofseal['checked_commit']==COMMIT and proofseal['status']=='accepted-scoped'
cell=load('research-wiki/frontier-cells/ASTIS-SW-SPHMC-gaussian-flip-energy.json')
assert cell['parents']==['ASTIS-SW-SPHMC-gaussian-compact-entropy']
assert cell['blocked']['status'] is False
integration=load(BASE+'integration.json')
checks={'schema_version':1,'checked_commit':COMMIT,'scope':'Independent bounded static reader/formula/source correspondence only',
 'five_formula_steps_present_and_mathematically_correspond':True,
 'C2_AND_compact_support_only_analytic_binders':True,
 'signed_zero_function_zero_mass_included':True,
 'literal_count_card_normalization_probability_and_true_L1_produced_internally':True,
 'actual_bool_true_1_false_minus1_and_update_flip':True,
 'positive_N_displacement_2_over_sqrt_N_and_N_delta_squared_4':True,
 'secant_squared_error_2BK_cubic_and_summed_16BK_over_sqrt_N':True,
 'successor_factor4_limit_correct':True,
 'N0_full_energy_zero_distinct_from_derivative_observer_at_zero':True,
 'sealed_public_header_exact_bytes':{'sha256':sha(header.encode()),'bytes':len(header.encode())},
 'production_Test_parent_raw_LF_equal_math_freeze':True,
 'folded_public_theorem_exact_source_suffix_ignoring_terminal_newline':True,
 'folded_statement_exact_sealed_header':True,
 'Lean_details_closed_by_default':True,
 'complete_module_and_Test_pages':modules,
 'module_all_10_private_providers_and_all_imports_visible':True,
 'complete_actual_N0_N1_Tests_and_3_axiom_prints_visible':True,
 'actual_ASTIS_parent_only_36':True,
 'no_Bernoulli_formal_parent_fabricated':True,
 'source_external_route_and_authored_route_distinct':True,
 'no_full_LSI_T2_FIRST_main_cost_live_or_PURIFIED_claim_in37_lesson':True,
 'complete_module_source_link_present':True,'Test_page_link_in_companion37_section':False,
 'nonblocking_notes':[{'path':'research-wiki/frontier-cells/ASTIS-SW-SPHMC-gaussian-flip-energy.json',
  'field':'blocked.reason','observation':'Inactive blocked.status=false retains historical "Actual proof not yet implemented" wording; not rendered in37 lesson and not a premise of this seal.'},
  {'observation':'Displayed sign sigma is shorthand; exact folded statement explicitly fixes true to1 and false to-1. Inverse sqrt display is read at positive successor indices; N0 is explicitly handled separately.'}],
 'receipt_preflight_diagnoses':['First preflight treated astis_dependencies string as a declaration object; schema inspection corrected receipt code only, no snapshots had been emitted.', 'Second preflight compared rendered actual Lean header to lean_statement natural-language metadata; exact diff showed rendered statement is the canonical sealed header. Receipt now compares that header directly. No mathematical/canonical input changed.'],
 'browser_rendering_or_interaction_executed':False,'compiler_started':False,'canonical_mutations':False}
branch={'schema_version':1,'checked_commit':COMMIT,'true_ASTIS_formal_parent':PARENTDECL,
 'consumer':DECL,'evidence':['actual production import','actual parent theorem call','lesson astis_dependencies','cell parents'],
 'imports':imports,'integration_structural_branch':integration.get('structural_branch'),
 'boundary':'Source graphs authored by reviewer are not revalidated. Distinct phase topology/source receipts reused only for provenance. Source correspondence edges are not Lean implications. No Bernoulli->37 proof edge.'}
provenance_paths={'source_topology_review':paths[16], 'actual_source_review':BASE+'source.0.review.overlay1.json',
 'metadata_overlay_review':BASE+'dependency-metadata-overlay1/overlay1.review.json',
 'wholeproof_review':BASE+'whole-proof-review/math.review.json','exact_proof_verified':BASE+'verified.json',
 'current_repository_ProofSeal':BASE+'reviewer.repository.ProofSeal.json'}
seal={'schema_version':1,'verdict':'ACCEPTED_SCOPED_EXPOSITION_SEAL','status':'accepted-scoped',
 'reviewer':ACTOR,'checked_commit':COMMIT,
 'scope':'Static source-adjacent37 mathematical reader and complete production/Test module pages; independent of root prose author. No compiler, sourcegraph selfvalidation or remote/live certification.',
 'independent_from_prose_author':True,
 'source_graph_author_history':'Reviewer authored37 source graph; topology/source truth comes only from distinct phase receipts. This check does not validate that graph.',
 'mathematical_declaration':DECL,
 'mathematical_exposition':'Actual card-normalized count law and Boolean sign sum; C2 AND compact support; internally produced bounds/L1/probability; full integral-of-sum energy, successor Gaussian variance1 limit4. Secant cubic error2BK and full error16BK/sqrtN; N0 empty energy0 differs from derivative observer fprime(0)^2.',
 'formula_proof_steps':step_records,'checks':'reviewer.exposition.checks.json','graph_branch':'reviewer.exposition.branch.json',
 'blockers':[],
 'mathematical_and_source_provenance':{k:by_path[v] for k,v in provenance_paths.items()},
 'provenance_boundary':'Accepted independent source/wholemath/exact/repository receipts establish their own scope; none replaces this independent exposition/code check.',
 'FULL_READER_DELIVERY_GAP':{'status':'OPEN','items':[
 'Actual Test tails not inline in companion37 lesson; complete Test page exists but this section has no Test-page link',
 'CopyLean/source-download controls and actual copy/download behavior not independently executed',
 'Paper/book/chapter bundles not delivered or checked in this bounded review',
 'Rendered browser/device formulas and fold/copy/download interaction not tested',
 'No37 remote CI, main merge, deployment/live credit inferred from historical receipts',
 'Postmerge PURIFIED and human-facing completeness remain open']},
 'remaining_mathematical_boundary':['compact scalar GaussianLSI final comparison','finite-Hilbert/noncompact sqrt-RN/cutoff/W12 extension','full GaussianLSI/T2/SPHMC FIRST4.6','paper main/work/cost/composition'],
 'input_bindings':'reviewer.exposition.inputs.json','static_only':True,'PURIFIED':False,
 'human_facing_complete':False,'compiler_started':False,'leases':{'read':'CLOSED','write':'CLOSED','Python':'CLOSED','compiler':'CLOSED'}}
# Freeze only after every semantic and exact-source assertion passes.
for r in bindings:
 create(r['raw_snapshot'],data[r['path']]);create(r['lf_snapshot'],lf(data[r['path']]))
create('reviewer.exposition.companion-section.raw.snapshot.html',section.encode())
create('reviewer.exposition.folded-proof.raw.snapshot.lean',h.codes[-1].encode())
create('reviewer.exposition.module-source.raw.snapshot.lean',prod.encode())
create('reviewer.exposition.Test-source.raw.snapshot.lean',test.encode())
payloads={'reviewer.exposition.inputs.json':{'schema_version':1,'checked_commit':COMMIT,'inputs':bindings},
 'reviewer.exposition.checks.json':checks,'reviewer.exposition.branch.json':branch,'ExpositionSeal.json':seal}
for name,obj in payloads.items():create(name,encode(obj))
run={'schema_version':1,'checked_commit':COMMIT,'actor':ACTOR,'input_count':len(bindings),
 'inputs':[{'path':r['path'],'raw_sha256':r['raw_sha256'],'lf_sha256':r['lf_sha256']} for r in bindings],
 'outputs':[{'path':n,'raw_sha256':sha(encode(o)),'lf_sha256':sha(encode(o))} for n,o in payloads.items()],
 'compiler_started':False,'canonical_mutations':False}
run['run_sha256']=sha(encode(run));create('reviewer.exposition.run.json',encode(run))
lease=load(BASE+'reviewer.exposition.lease.json')
lease.update({'status':'CLOSED','read_lease':'CLOSED','write_lease':'CLOSED','Python_lease':'CLOSED','compiler_lease':'CLOSED',
 'completed_utc':datetime.now(timezone.utc).isoformat(),'verdict':seal['verdict'],
 'seal_raw_sha256':sha(encode(seal)),'run_sha256':run['run_sha256'],'input_count':len(bindings)})
(OUT/'reviewer.exposition.lease.json').write_bytes(encode(lease))
print(json.dumps({'verdict':seal['verdict'],'seal_raw_sha256':sha(encode(seal)),
 'run_sha256':run['run_sha256'],'inputs':len(bindings),'leases':'all CLOSED','delivery_gap':'OPEN'}))
