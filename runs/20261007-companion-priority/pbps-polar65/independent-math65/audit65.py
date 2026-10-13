import collections,html,json,os,pathlib,re,sys
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from math65 import R,O,D,P,BASE,ACTOR,read,write,pin,sha,inputs_current,now,TARGETS
inputs_current()
inv=read(P/'independent-primary65/source-coverage-inventory.json')
src=read(P/'independent-primary65/source-inputs.json')
full=pathlib.Path(src['primary_path']).read_bytes();regions=src['named_raw_input_payload']['segment_map']
actual=[]
for reg in regions:
    a,z=reg['source_byte_range']
    for m in re.finditer(rb'<math\b.*?</math>',full[a:z],re.S):
        actual.append((reg['name'],a+m.start(),a+m.end(),sha(m.group(0))))
listed=[(x['region'],x['raw_byte_start'],x['raw_byte_end_exclusive'],x['raw_math_sha256']) for x in inv['math_items']]
assert actual==listed and len(actual)==inv['math_count']==280
assert all(x['annotation_present'] and x['alttext_present'] and x['annotation_exactly_matches_alttext'] and x['annotation_tex']==x['alttext'] for x in inv['math_items'])
assert sum(inv['classification_counts'].values())==280
prod=(R/TARGETS[0]).read_text(encoding='utf-8');test=(R/TARGETS[1]).read_text(encoding='utf-8')
parent=(R/'AutoSamplingTheory/ExampleCases/ProximalBPS/CenteredRootOrderInverse.lean').read_text(encoding='utf-8')
def binders(s):return s[s.index('    {E : Type*}'):s.index('    let μ :=')]
assert binders(prod)==binders(test)==binders(parent)
parent_name='AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredRootOrderInverse.actual_centered_root_order_inverse'
assert prod.count(parent_name)==1
assert test.count('have hBase := AutoSamplingTheory.ExampleCases.ProximalBPS.PolarIsometry.actual_centered_polar_isometry')==1
body0=prod[prod.index(':= by')+len(':= by'):];body1=test[test.index(':= by')+len(':= by'):]
api_specs=[
 ('Topology/Algebra/Module/ContinuousLinearMap/Restrict.lean',107,124,'codRestrict','B0 codomain restriction','codRestrict'),
 ('Topology/Algebra/Module/ContinuousLinearMap/Basic.lean',669,671,'isClosed_ker','HP0 and Hperp internally complete closed kernels','isClosed_ker'),
 ('Analysis/InnerProductSpace/Adjoint.lean',97,158,'adjoint; adjoint_comp; apply_norm_sq_eq_inner_adjoint_right','real complete Hilbert adjoint, Gram norm identity and adjoint of composition','apply_norm_sq_eq_inner_adjoint_right'),
 ('Analysis/InnerProductSpace/Adjoint.lean',842,852,'norm_map_iff_adjoint_comp_self','norm preservation gives V0*V0=I','norm_map_iff_adjoint_comp_self'),
 ('Analysis/Normed/Operator/Basic.lean',198,201,'opNorm_le_bound','bound1 from all-vector norm equality without Nontrivial','opNorm_le_bound')]
apis=[]
for path,a,z,n,use,token in api_specs:
    p=R/'.lake/packages/mathlib/Mathlib'/path;b=p.read_bytes();span=b''.join(b.splitlines(keepends=True)[a-1:z])
    assert token in span.decode('utf-8') and token in body0+body1
    apis.append({'path':p.as_posix(),'whole_source_RAW':pin(p),'start_line':a,'end_line':z,'literal_API_span_RAW_sha256':sha(span),'literal_API_span_RAW_bytes':len(span),'API':n,'actual_use':use,'no_L2_finite_dimension_or_Nontrivial_premise':True})
mirror=read(D/'conceptual-mirror-audit65.json');assert mirror['status']=='none-found' and mirror['discovery_ids']==[]
notes={
 'schema':'independent-math65-reviewed-mathematical-capsule-v1',
 'actor':ACTOR,'actual_author_pid':os.getpid(),'authored_utc':now(),
 'verdict':'ACCEPT_BOUNDED_PRECOMMIT_MATHEMATICS_AND_LITERAL_PRESENTATION',
 'checked_BASE_commit':BASE,'checked_SCI65_commit':None,'uncommitted_candidate_limitation':True,
 'candidate_exact_RAW':[pin(R/f) for f in TARGETS],
 'mathematical_blockers':[],'source_region_blockers':[],'explanatory_overclaims_found':[],
 'seven_slot_review':{
  'domain':'Finite-dimensional real Hilbert Borel E with canonical volume; real scalar L2 of the produced laws. No finite-dimensional L2 or Nontrivial binder. Explicit rank-zero extension is retained.',
  'source_inputs':'The only original hypotheses are C2 V, NNReal curvature storage 0<alpha<=beta, both global quadratic-form Hessian bounds, eta>0 and beta eta<=1. Candidate, original-input Test and accepted64 parent public binder bytes match. Alpha eta=1 is legal.',
  'objects_and_definitions':'The actual Gibbs mu, joint J, marginal nu, normalized S, pullback e, actual reflection U, macro T, constant q, positive root Gamma and transported GammaP, centered restriction GammaP0 and bounded two-sided Inv are the SAME existential witnesses extracted once from actual64. HP0=ker innerSL(e q), Hperp=ker actual P. Hperp means conditional mean zero given Y and is not replaced by all globally centered joint L2.',
  'conclusion':'Produced typed B0:HP0->ker P, ambient inclusion B0=B i0; V0=B0 Inv; B0=V0 GammaP0; V0*V0=I_HP0; every-vector norm preservation. Genuine original-input Test produces B0*g=GammaP0(V0*g), adjoint contraction and V0*(g-V0(V0*g))=0 for every g:ker P.',
  'dependencies':'One genuine actual ASTIS production parent actual_centered_root_order_inverse, reused by exact current/base Git RAW equality and closed independent64 capsule pins. Probability/range/Gram/root/centering/order/unit/inverse are inherited conclusions, never caller certificates. New facts use closed-kernel subtype Hilbert structures and standard Mathlib bounded-linear adjoint APIs. Source Proof Graph remains distinct from this Lean dependency edge.',
  'proof_recipe':'codRestrict B i0 using inherited PB=0; define V0=B0 Inv. SAME ambient Gram B*B=GammaP^2 and GammaP selfadjointness give equal squared norms. Restriction equality and right inverse GammaP0 Inv=I give norm preservation. Left inverse Inv GammaP0=I separately gives factorization. Real Hilbert norm-preservation/adjoint API gives V0*V0=I. Adjoint composition plus GammaP0 positivity gives the Test factorization; norm of adjoint equals norm of V0; V0*V0 at V0*g annihilates the residual.',
  'truth_boundary':'This is B16 typed polar isometry/factorization plus the first centered adjoint consumer. It does not prove V0 onto ker P, V0 V0*=I on ker P, norm equality for V0* on all ker P, full ambient B* transport, or the whole modified corrector/Lyapunov contraction. No B13/H1, B14 lower floor, B17 small-step condition or additional root/gap/unit/onto/cost premise is introduced.'},
 'independent_proof_checks':[
  {'stage':'typed_closed_spaces_and_B0','accepted':True,'reason':'Closed kernels of actual bounded maps inherit complete Hilbert structures. codRestrict only uses PB=0 inherited for all HP; hB0 is definitional. The inclusion is into joint L2 and the domain inclusion is into HP.'},
  {'stage':'SAME_Gram_and_normalization','accepted':True,'reason':'For g=Inv f, ambient squared norm identity with B*B=GammaP GammaP matches the identity for selfadjoint GammaP. Nonnegative norms permit sq_eq_sq elimination. hGammaP0 g transports to the inherited subtype norm; hRight evaluates to GammaP0 g=f. No closed range or inverse on full HP is used.'},
  {'stage':'factorization_and_left_inverse','accepted':True,'reason':'At each f, V0 GammaP0 f=B0 Inv GammaP0 f=B0 f by hLeft. This cancellation is distinct from the right inverse used for norm preservation.'},
  {'stage':'VstarV','accepted':True,'reason':'The Mathlib equivalence for a bounded map between complete inner product spaces converts every-vector norm equality into V0.adjoint composed V0=identity. It does not assume or conclude onto.'},
  {'stage':'genuine_Test_adjoint_factorization','accepted':True,'reason':'The Test starts from exactly original potential/curvature/step inputs and extracts the actual producer witnesses. Taking adjoints of factorization reverses composition; positivity makes GammaP0 selfadjoint.'},
  {'stage':'adjoint_contraction_and_residual','accepted':True,'reason':'opNorm_le_bound with 1 is valid even on the zero subspace; adjoint is a norm isometry. Evaluating V0*V0=I at V0*g and linearity yields the annihilated residual, not a zero residual or coisometry.'},
  {'stage':'legal_degenerate_endpoints','accepted':True,'reason':'No new Nontrivial/positive-rank instance, no finite-dimensional L2 and no strict alpha eta<1 condition. Kernel completeness, opNorm upper bound and the adjoint equivalence all permit zero spaces. Gamma inverse remains the inherited original-input centered conclusion.'}],
 'source_first_inventory_check':{'all280_literal_math_tags_reenumerated':True,'exact_item_source_byte_spans_and_RAW_sha256':True,'regions':len(regions),'classification_counts':inv['classification_counts'],'all_annotations_and_alttext_match':True,'coverage_scope':inv['coverage_scope'],'scope':'Source-first initial65 inventory and literal primary regions only; no consumption of post-proof independent-source65 or decoder65 verdicts.'},
 'source_to_delta':{'B11':'SAME ambient Gram used literally for norm equality; no new variance premise','B15':'Exact centered order/inverse inherited from accepted actual64, not reproved or enlarged here','B16':'Exact typed polar factorization/isometry and V*V identity produced','B3_first_consumer':'Exact centered B0 adjoint action, contraction and residual annihilation produced; full ambient adjoint-transport adapter remains separate','excluded':'B13/H1, B14 floor, B17 quantitative half-turn, B18-B20/full Lyapunov and later source equations have no completion credit'},
 'actual_used_APIs':apis,
 'minimal_import_reuse':{'production_imports':['AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredRootOrderInverse'],'Test_imports':['AutoSamplingTheory.ExampleCases.ProximalBPS.PolarIsometry'],'genuine_actual64_parent_count':1,'no_duplicate_probability_root_or_inverse_provider':True,'private_providers':0,'each_new_file_has_one_theorem':True},
 'conceptual_mirror_audit':{'status':'none-found','independently_mathematically_accepted':True,'reason':'This delta is direct polar and adjoint implication on the SAME actual Hilbert model and inherited Gram/root/inverse. No independently sourced pair of different domains, hypothesis transport or cross-domain mechanism was introduced. These are compiled formal edges; labeling the same-space identities a new conceptual bridge would not add a source-backed correspondence.','discovery_ids':[]},
 'literal_exposition':'All5 steps are exact complete BODY line spans and full source RAW bindings, after theorem proof delimiter; mathematical prose/formula claims match those bounded steps. Orthogonal-residual terminology is justified by ker V* but the Lean output is explicitly annihilation, not an asserted projection theorem. Full attributed inherited statement remains original-input; no onto claim.',
 'initial_seals':'Both exact initially sealed theorem headers are unchanged, modulo only trailing delimiter-adjacent whitespace; no binder/definition/quantifier repair. Accepted initial primary/header native closures were hash-checked, not promoted into post-proof source acceptance.',
 'retained_negative_routes':'Root focused v1-v5 actual receipt/log pins and four diagnoses are preserved without proof credit. Our first compiler observer failed on multiline axiom parsing after printed3945 success and had not persisted its compiler exit; its exact script/log/prepin/failure bytes are retained. A second nonforced focused build supplies actual PID23980 EXIT0. Two schema parser diagnostics for native closure-manifest keys are retained and resolved by exact finite schema fields, without changing any native artifact.',
 'required_followups':['Separate anti-anchored source review and blind decoder admission, including any separately reviewed overlay','Later exact SCI65 commit verification and proper non-owner VERIFIED transition','Serialized shared imports/Registry/Tests and repository/publication/reader admission','If downstream full-joint corrector needs it, explicit centered-to-full adjoint transport and global centered decomposition compatibility','B17/H1/remaining operator estimates, event dynamics, invariance/nonexplosion, hypocoercivity/main result, errors, expected query cost, actual-input PBPS/SPHMC composition'],
 'claims_not_made':['Exact SCI65 commit review','VERIFIED ledger transition','Full ambient adjoint transport or onto/completed coisometry','Full paper or actual-input composition','Full repository aggregate gate','Exposition Seal or PURIFIED','Main/live/remote delivery or whole Goal completion'],
 'canonical_Lean_Git_ledger_writes':False}
write('mathematical-review.json',notes)
print(json.dumps({'status':notes['verdict'],'actual_pid':os.getpid(),'inventory_math_items':len(actual),'API_spans':len(apis),'mathematical_blockers':0,'source_region_blockers':0}),flush=True)
