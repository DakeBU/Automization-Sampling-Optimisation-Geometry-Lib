from pathlib import Path
import hashlib,json,re
root=Path('E:/Samplinglib');out=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def write(n,o):
 p=out/n;assert not p.exists(),p
 p.write_bytes((json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode())
prepared=json.loads((out/'prepared-inputs96.native.json').read_bytes())
receipt=json.loads((out/'fresh-kernel-receipt96.native.json').read_bytes())
assert receipt['exit_code']==0 and receipt['source_rehashed_unchanged'] and receipt['manifest_rehashed_unchanged']
for entry in prepared['inputs']:
 assert sha((root/entry['path']).read_bytes())==entry['raw_sha256'],entry
 assert sha((root/entry['snapshot']).read_bytes())==entry['raw_sha256'],entry
log=(out/'fresh-kernel.stdout.log').read_text(encoding='utf-8')
ax=re.findall(r"depends on axioms:\s*\[([^\]]+)\]",log)
assert len(ax)==2 and all({x.strip() for x in a.split(',')}=={'propext','Classical.choice','Quot.sound'} for a in ax)
assert not (out/'fresh-kernel.stderr.log').read_bytes()
src=(root/prepared['inputs'][0]['path']).read_text(encoding='utf-8')
helpers=re.findall(r'^private theorem (\w+)',src,re.M)
assert len(helpers)==8
decision={
 'kind':'independent-whole-mathematics-and-kernel-review',
 'reviewer':'/root/independent_whole_math93',
 'decision':'ACCEPT_EXACT_PRODUCTION_AND_SEALED_STATEMENT',
 'target':'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseReversalVolume.actual_phase_reversal_volume_laws',
 'production':prepared['inputs'][0],
 'header':prepared['inputs'][1],
 'statement_seal':prepared['inputs'][2],
 'commit_context':{'observed_head':prepared['observed_repository_head'],'scope':'Exact worktree RAW reviewed; not an exact science-commit verification or VERIFIED transition.'},
 'statement_binding':{
  'literal_comparison':'Production private full Prop, original Header96 candidate and expanded_literal_Prop in frozen seal agree textually after newline decoding and removal of outer whitespace/declaration name only. No binder, definition or conclusion changed.',
  'kernel_witness':'FreshExactSourceAndHeader96.lean starts with every exact production byte, appends the original Header96 body (only imports omitted), then proves that candidate directly with the newly elaborated public theorem. No import of the target production olean is used.',
  'six_analytic_assumptions':['hα:alpha>0','hαβ:alpha<=beta','hV:ContDiff real 2 V','hH:everywhere two-sided Hessian quadratic-form bounds','hη:eta>0','hβη:beta*eta<=1'],
  'eight_literal_lets':['c','h','B','S','R','Phi','rate','ell'],
  'outer_conjuncts':13,
  'no_added_provider':'No volume-preservation, density, joint-measurability, inverse, reflection law or external closure supplied as public hypothesis. Integrable F belongs only to the quantified real-test corollary.'},
 'kernel':{
  'receipt':'fresh-kernel-receipt96.native.json','exit_code':0,
  'fresh_full_source_elaboration':True,'exact_header_witness':True,
  'axioms_public_and_witness':['propext','Classical.choice','Quot.sound'],
  'warnings':'Unused named proof binders in Prop definitions only; these preserve the original source hypotheses. No error or stderr.',
  'toolchain':'Pinned lake/Lean4.33.0 with ELAN_TOOLCHAIN removed; fixed manifest RAW unchanged.',
  'mathlib_commit':prepared['mathlib_commit']},
 'helper_audit':[
  {'name':'lower_shear','reason':'For fixed position x, p maps to p+a*x, a canonical-volume-preserving translation. Joint measurability plus MeasurePreserving.skew_product establishes product preservation without a determinant or finite-mass premise.','consumers':['upper_shear','area_matrix']},
  {'name':'upper_shear','reason':'Coordinate swap conjugates the lower shear to position translation by momentum. Both product factors are the same canonical volume.','consumers':['area_matrix']},
  {'name':'negate_phase','reason':'Product of two real linear-isometry negations preserves the explicit product volume.','consumers':['harmonic_linear']},
  {'name':'reflect_fiber','reason':'The literal zero-safe B(n,p) is identified with reflection in the orthogonal complement of span(n). reflection_singleton_apply and reflection_orthogonal_apply have no n!=0 premise. Finite-dimensional completeness is derived internally; LinearIsometryEquiv.measurePreserving applies to canonical E-volume.','consumers':['public hSmp']},
  {'name':'area_matrix','reason':'For a*a-b*c=1 and 1+a!=0, k=b/(1+a) satisfies c*k=a-1 and k*(1+a)=b. The checked equality M=U(k) composed L(c) composed U(k) has diagonal 1+c*k=a, lower c and upper k*(1+a)=b. Each actual factor preserves volume. These determinant/denominator premises are private and discharged by harmonic coefficients.','consumers':['harmonic_linear']},
  {'name':'harmonic_linear','reason':'eta>0 gives sqrt(eta)!=0. Coefficients are exactly a=cos u,b=sqrt(eta)*sin u,c=-sin u/sqrt(eta); field simplification and sin^2+cos^2=1 discharge area_matrix. If 1+cos u=0, cos u=-1 forces sin u=0 and the actual map equals negate_phase. No exceptional duration is dropped; no unscaled isometry claim.','consumers':['harmonic_affine']},
  {'name':'translate_position','reason':'Position translation product momentum identity, each canonical-volume-preserving.','consumers':['harmonic_affine']},
  {'name':'harmonic_affine','reason':'Exact conjugation T(d) composed harmonic_linear composed T(-d), with d=c(y,r). The centered shift cancels by module algebra and no assumption on d is supplied.','consumers':['public flow-volume conclusion']}],
 'public_conjunct_audit':[
  {'indices':[1,2,3,7,8],'finding':'ActualHarmonicFlow.actual_harmonic_flow_laws supplies joint flow measurability and both inverse identities; ActualBounceRate.actual_bounce_rate_energy_laws supplies joint S/rate measurability and S involution. Exact literal definitions and all six source assumptions match the existing declarations. Projections select the intended facts.'},
  {'indices':[4],'finding':'harmonic_affine specializes to the literal center c(y,r), for every y,r and every real u.'},
  {'indices':[5],'finding':'hSmp fixes the position coordinate and applies reflect_fiber at h(r,x) for every x. Measurability of the momentum fiber map follows from the inherited joint S map with r fixed and second projection. The proof meets the sigma-finite product hypotheses by finite-dimensional volume instances.'},
  {'indices':[6,9],'finding':'R is identity times momentum negation; measure preservation is a product construction and double negation proves involution.'},
  {'indices':[10],'finding':'Coordinate algebra, cos(-u)=cos u and sin(-u)=-sin u prove R Phi(u) R=Phi(-u) for every state. Center remains fixed.'},
  {'indices':[11],'finding':'Reflection is linear/odd in momentum for the same position-dependent normal, so R commutes with S including normal zero.'},
  {'indices':[12],'finding':'The inherited exact inner-product flip gives <B(n,p),n>=-<p,n>. Momentum negation restores the argument to max(0,.) and hence the actual sqrt(eta)-scaled rate for every state.'},
  {'indices':[13],'finding':'Measure-preserving pullback gives integrability for real integrable F. The involution plus measurability yields a MeasurableEquiv and thus MeasurableEmbedding, meeting the actual Bochner integral_comp API. The integral equality is not inferred from an absent everywhere-measurability premise.'}],
 'instances_and_degenerate_cases':[
  'ell is explicitly volume(E).prod(volume(E)); there is no inferred arbitrary Haar normalization or reliance on a norm-induced volume on the standard product E x E.',
  'Finite-dimensional Borel E supplies the locally compact/second-countable/sigma-finite volume structure needed by translation and product lemmas. No extra instance binder is hidden in the public theorem.',
  'No Nontrivial E or finrank>0 premise; rank zero gives singleton volume one and all maps identity.',
  'When h(r,x)=0, span(0) orthogonal complement is the whole space, its reflection is identity, literal B(0,p)=p and rate=0.',
  'All real durations, including 0 and odd-pi exceptional cos=-1, are covered. eta=0 remains correctly excluded by the original eta>0 binder.',
  'No horizon/count indices or AE intersections are introduced. Identities hold at every stated parameter/state; joint Borel maps are on finite-dimensional product spaces.',
  'A bounded real test need not be volume-integrable in positive dimension; the theorem correctly assumes Integrable F only for its real integral statement.'],
 'closure_audit':{'source_scan':prepared['fake_closure_scan'],'private_helpers':helpers,'private_helpers_all_consumed':True,'one_private_literal_Prop':True,'one_public_theorem':True,'kernel_axioms_cover_transitive_dependencies':True,'fake_closure_found':False},
 'scope_boundary':'Accepted bounded mathematical edge: actual affine harmonic flow, bounce and momentum reversal preserve phase product volume with exact measurability/inverse/reversal/rate laws and bounce integral change of variables. No finite-simplex reversal, Gibbs cocycle, skew detailed balance, invariance, semigroup, full paper/composition/Goal credit; publication and independent source review remain separate.',
 'required_repairs':[],
 'all_inputs_rehashed_before_closure':True,
 'inputs':prepared['inputs']}
write('whole-math-decision96.native.json',decision)
entries=[]
for p in sorted(out.rglob('*')):
 if p.is_file():
  b=p.read_bytes();entries.append({'path':p.relative_to(root).as_posix(),'raw_sha256':sha(b),'bytes':len(b)})
write('closed-RAW-manifest96.native.json',{'kind':'closed-raw-manifest','reviewer':'/root/independent_whole_math93','self_excluded':True,'closure':'All exact input snapshots, generation/check scripts, fresh kernel input, stdout/stderr, receipt and decision in this owned directory. No primary-source extract copied.','files':entries})
for n in ['whole-math-decision96.native.json','closed-RAW-manifest96.native.json']:
 b=(out/n).read_bytes();print(n,sha(b),len(b))
