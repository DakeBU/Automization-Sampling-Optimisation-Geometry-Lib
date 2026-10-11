from pathlib import Path
import hashlib,json
root=Path('E:/Samplinglib');out=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def write(n,o):
 p=out/n;assert not p.exists(),p;p.write_bytes((json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode())
checks=json.loads((out/'exact-region-checks96.native.json').read_bytes())
for i in checks['inputs']:
 assert sha((root/i['snapshot']).read_bytes())==i['raw_sha256']
decision={
 'kind':'independent-authored-mathematical-exposition-review',
 'reviewer':'/root/independent_whole_math93',
 'decision':'ACCEPT_MATHEMATICAL_STATEMENT_AND_SEVEN_PROOF_EXPLANATIONS',
 'scope':'Exact snapshotted authored mathematics and Lean-region consistency only. Reuses unchanged accepted whole mathematics/kernel proof. No rendered/visual acceptance, source-fidelity verdict, publication admission or VERIFIED transition.',
 'inputs':checks['inputs'],
 'statement_review':{
  'complete_statements_identical':True,
  'findings':['All six original analytic hypotheses appear with the same domains and everywhere Hessian quantifiers. Finite-dimensional real Borel Hilbert E includes rank zero.',
   'All eight literal definitions match, including actual sqrt(eta) scaling, canonical product volume and totalized zero-normal reflection.',
   'Joint Borel scope, all real u, every y/r/z, three volume-preserving maps, both flow inverses, both involutions, all three reversal/rate identities and real-integrable A6 conclusion cover the thirteen conjuncts.',
   'Integrable real F remains local to the final test corollary. No arbitrary supplied volume law, inverse law, measurability, density or other provider is substituted for the proved maps.',
   'The stated boundary correctly excludes prescribed-path reversal, invariance, semigroup, whole-paper/composition results.']},
 'step_review':[
  {'step':1,'finding':'Correct lower/upper shear definitions, fixed-position momentum translation, swap conjugation and product-negation volume argument.'},
  {'step':2,'finding':'B(n,p) is the reflection in span(n) orthogonal complement. At n=0 this is the identity; joint state-dependent Borel measurability is explicitly separated from fiberwise isometry.'},
  {'step':3,'finding':'Private conditions a^2-bc=1 and 1+a!=0 are explicit in prose. k=b/(1+a), ck=a-1 and k(1+a)=b give the correct composition U_k L_c U_k. The upper-right coefficient 2k+k^2 c and other coefficients are correct.'},
  {'step':4,'finding':'Exact harmonic coefficients use sqrt(eta), not unit scaling. eta>0 gives the nonzero denominator. cos=-1 entails sin=0 and simultaneous negation. Position translations before/after the linear map restore the actual center in the correct order.'},
  {'step':5,'finding':'The two actual parent theorems supply the named Borel and involution/inverse facts. The position-fixed fiber argument yields bounce preservation, and product negation/affine helper yield the remaining maps.'},
  {'step':6,'finding':'Momentum negation conjugates harmonic flow to negative time and commutes with reflection. The reflected inner-product sign flip followed by negation restores the exact positive-part rate, including zero normal.'},
  {'step':7,'finding':'Real F integrability is explicit. Measure-preserving pullback gives integrability, and the measurable involution provides the measurable equivalence used for the integral change of variables. No extra everywhere-measurability assumption needed.'}],
 'regions':checks['seven_regions'],
 'region_verification':'Seven inclusive line slices are byte-identical to their embedded UTF-8 Lean code and exact_code_raw_sha256, all source RAW pins equal the unchanged accepted production. No newline normalization was needed for these slices.',
 'dependency_review':'Two ASTIS direct parents match actual consumption. Listed Mathlib operations occur in the proof; no producer is made a public assumption. The eight private mathematical helpers remain consumed in the accepted proof.',
 'required_mathematical_repairs':[],
 'separate_metadata_observation':{
  'path':'website/content/publications/pbps-actual-phase-reversal-volume.json',
  'field':'items[0].source_proof_coverage.coverage_status',
  'snapshot_value':checks['publication_source_coverage_status'],
  'issue':'The phrase proof not yet implemented is stale relative to the compiled and independently kernel-reviewed production. Prospective source review itself must not be promoted to completed source review.',
  'minimal_correction':'Update the status to distinguish the implemented compiled proof from pending completed source review, or replace the coverage pointer/status when that independent review is completed.',
  'reported_to_owner':True,
  'effect_on_this_verdict':'No mathematical or Lean-region correction needed; this is not blanket acceptance of all publication metadata.'},
 'immutable_prior_review_preserved':True,
 'no_production_or_public_writes':True}
write('exposition-decision96.native.json',decision)
entries=[]
for p in sorted(out.rglob('*')):
 if p.is_file():
  b=p.read_bytes();entries.append({'path':p.relative_to(root).as_posix(),'raw_sha256':sha(b),'bytes':len(b)})
write('closed-RAW-manifest-exposition96.native.json',{'kind':'closed-raw-manifest','reviewer':'/root/independent_whole_math93','self_excluded':True,'closure':'All files in this bounded exposition96 supplement; earlier closed whole-math manifest remains unchanged.','files':entries})
for n in ['exposition-decision96.native.json','closed-RAW-manifest-exposition96.native.json']:
 b=(out/n).read_bytes();print(n,sha(b),len(b))
