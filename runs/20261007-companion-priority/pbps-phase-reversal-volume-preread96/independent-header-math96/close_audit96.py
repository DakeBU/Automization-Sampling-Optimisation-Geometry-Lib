from pathlib import Path
import hashlib, json, subprocess

root = Path('E:/Samplinglib')
out = Path(__file__).resolve().parent
def sha(b): return hashlib.sha256(b).hexdigest()
def write(name, value):
    p = out / name
    assert not p.exists(), p
    p.write_bytes((json.dumps(value, ensure_ascii=False, indent=2)+'\n').encode('utf-8'))
header = 'runs/20261007-companion-priority/pbps-phase-reversal-volume-preread96/Header96.lean'
expected = '7a3d1929ccc6f1ae01ac3187040ad032515df7af0d627636d646d7f4df382a91'
assert sha((root/header).read_bytes()) == expected
paths = [header,
'runs/20261007-companion-priority/pbps-phase-reversal-volume-preread96/type-only2-bochner-scope/receipt.json',
'runs/20261007-companion-priority/pbps-actual-bounded-path-expansion95/next-primary96/scope96/proposed-mathematical-statement96.native.json',
'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean',
'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBounceRate.lean',
'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Prod.lean',
'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Haar/InnerProductSpace.lean',
'lean-toolchain', 'lake-manifest.json']
inputs = []
(out/'inputs').mkdir(exist_ok=False)
for i, path in enumerate(paths):
    b = (root/path).read_bytes()
    snap = out/'inputs'/f'{i:02d}.{Path(path).name}.exactraw'
    snap.write_bytes(b)
    inputs.append({'path':path,'raw_sha256':sha(b),'bytes':len(b),'snapshot':snap.relative_to(root).as_posix()})
receipt = json.loads((root/paths[1]).read_bytes())
assert receipt['exit_code']==0 and receipt['raw_sha256']==expected and receipt['type_only'] and not receipt['proved']
decision = {
 'kind':'independent-preproof-mathematical-header-audit',
 'reviewer':'/root/independent_whole_math93',
 'decision':'ACCEPT_EXACT_HEADER_NO_REQUIRED_MATHEMATICAL_REPAIR',
 'header':inputs[0],
 'observed_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
 'scope':'Mathematical truth, literal definitions, quantifiers, measure and degenerate cases. No Lean implementation, theorem proof, Statement Seal, source-fidelity acceptance, SAU or VERIFIED transition.',
 'type_formation':'Reviewed root type-only receipt matches exact header and reports EXIT0. This audit does not treat type checking a Prop definition as proving it; no independent theorem compile claimed.',
 'assumptions':{
  'ambient':'Finite-dimensional real inner-product space with its Borel measurable structure; no Nontrivial or positive-dimension requirement.',
  'six_original':['alpha>0','alpha<=beta','V is C2','two-sided Hessian quadratic-form bounds everywhere','eta>0','beta*eta<=1'],
  'provider_binders':'None. Actual gradient, center, reflection, flow, rate and explicit phase product volume are literal lets. Test integrability is local to the final integral conclusion, not a supplied dynamics/volume/density fact.',
  'strength':'Curvature bounds and eta upper bound are stronger than needed for the elementary volume core but remain unchanged on the source-facing candidate.'},
 'mathematical_checks':[
  {'conjuncts':'1-3','finding':'C2 gives continuous gradient, hence joint continuous flow/rate and Borel reflection. Division by zero is the specified zero-safe real division; reflection is Borel even at vanishing normal. No joint continuity of reflection asserted.'},
  {'conjunct':'4','finding':'For fixed center, each coordinate harmonic block is [[cos u,sqrt(eta)*sin u],[-sin u/sqrt(eta),cos u]], determinant cos(u)^2+sin(u)^2=1 because eta>0. In dimension d its determinant is 1^d, and translation preserves canonical volume. Explicit product volume matches orthonormal coordinate Lebesgue volume. All real u covered.'},
  {'conjunct':'5','finding':'For fixed x, the momentum map is an orthogonal reflection when the normal is nonzero and identity when it is zero. Each fiber preserves canonical momentum volume. Joint Borel measurability and sigma-finiteness of finite-dimensional volume give preservation of position-times-momentum product measure. State dependence requires no differentiability or nonvanishing-normal assumption.'},
  {'conjunct':'6','finding':'Position identity times momentum negation preserves the explicit product measure.'},
  {'conjuncts':'7-11','finding':'Flow inverse follows the harmonic group algebra; reflection squares to identity including zero normal; momentum negation is involutive. Negating momentum conjugates u-flow to (-u)-flow and commutes with the linear reflection at the unchanged position.'},
  {'conjunct':'12','finding':'For every normal n and momentum p, <B(n,p),n>=-<p,n>, including n=0. Therefore <-B(n,p),n>=<p,n> and the same sqrt(eta)*positive-part rate is retained under R after S. No positive-rate or nonzero-normal premise is needed.'},
  {'conjunct':'13','finding':'Measure-preserving pullback preserves AE strong measurability, integrability and the signed real integral. Integrable F is sufficient without a separate everywhere-measurable F binder. Boundedness alone would be insufficient on infinite phase volume; the header uses the correct hypothesis.'}],
 'edge_cases':[
  'Zero normal: B(0,p)=p and rate=0; the map laws and volume claim remain valid.',
  'Rank zero: E and phase are singletons, canonical volume has mass one and all maps are identity.',
  'u=0 gives identity; arbitrary positive/negative u and arbitrary centers are valid.',
  'eta=0 is excluded and must remain excluded for flow inverse/volume; no limiting eta=0 claim.',
  'No horizon/count indices or AE parameter intersections occur. All map identities quantify pointwise over every displayed parameter/state.',
  'No function-space sigma algebra or measurable map into a transformation space is silently assumed. Joint measurability concerns the displayed finite-dimensional product domains.'],
 'reusable_interfaces':[
  {'path':paths[3],'declaration':'actual_harmonic_flow_laws','use':'Exact same literal harmonic formula, joint measurability and inverse laws. Existing zero/group identities may be reused but are not additional new credit.'},
  {'path':paths[4],'declaration':'actual_bounce_rate_energy_laws','use':'Same zero-safe reflection and gradient rate; supplies joint Borel bounce, rate regularity, reflection algebra and zero-normal behavior.'},
  {'path':paths[5],'declaration':'MeasureTheory.MeasurePreserving.skew_product','use':'Inspected signature requires measurable uncurry fiber map and AE fiber pushforward equality; pointwise preservation of all reflection fibers is stronger, with SFinite factors derived here.'},
  {'path':paths[6],'declaration':'LinearIsometryEquiv.measurePreserving','use':'Canonical Hilbert-volume preservation for each orthogonal reflection/negation. Orthonormal and WithLp product volume interfaces explicitly mediate phase norm conventions.'}],
 'implementation_cautions_not_statement_defects':[
  'The harmonic flow is generally not an isometry for the unscaled standard phase inner product when eta differs from 1. Use determinant one or justify conjugating scales and cancellation.',
  'Do not infer global smoothness/continuity of S at zero normal or use an unjustified full-state Jacobian.',
  'Do not change ell to an unspecified phase volume without checking the product normalization.'],
 'source_scope_comparison':'Literal definitions, six hypotheses, measure convention and elementary map conclusions agree with the independently proposed scope. Optional flow group/zero and other integral corollaries mentioned there are existing or derived additions, not falsely claimed as explicit conjuncts here. This is mathematical consistency review only; source reviewer retains source-fidelity authority.',
 'remaining_boundary':[
  'Actual Lean proofs of the new harmonic and state-dependent reflection volume preservation remain required.',
  'No finite-simplex joint reversal theorem, density/Gibbs cocycle, detailed balance, stationarity, Markov property or semigroup result follows as an already proved declaration from this header.',
  'Future finite-jump consumer must check joint Borel dependence and finite recursion; path reversal at internal event times requires correct incoming/left-limit convention.'],
 'required_repairs':[], 'counterexamples_to_exact_header_found':[],
 'inputs':inputs}
write('header-math-decision96.native.json',decision)
entries=[]
for p in sorted(out.rglob('*')):
    if p.is_file():
        b=p.read_bytes();entries.append({'path':p.relative_to(root).as_posix(),'raw_sha256':sha(b),'bytes':len(b)})
write('closed-RAW-manifest96.native.json',{'kind':'closed-raw-manifest','reviewer':'/root/independent_whole_math93','closure':'All owned audit files and exact input snapshots except this self-excluding manifest. Original source input hashes separately recorded in decision; no full primary copied.','files':entries})
for name in ['header-math-decision96.native.json','closed-RAW-manifest96.native.json']:
 b=(out/name).read_bytes();print(name,sha(b),len(b))
