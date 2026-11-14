from pathlib import Path
import hashlib,json
E=Path('research-wiki/paper-contributions/GaussianComplexity/zero-query-separation-semantic-evidence')
P=Path('AutoSamplingTheory/ExampleCases/GaussianComplexity/ZeroQuerySeparation.lean');T=Path('Tests/GaussianComplexityZeroQuerySeparation.lean')
sha=lambda b:hashlib.sha256(b).hexdigest();rows=[]
def add(i,r,f,a,b,node,claim,body=False,decl=None,provenance=None):
    p=Path(f);raw=p.read_bytes();s=raw.decode();scope=s.index(':= by')+len(':= by') if body else 0
    assert s.count(a,scope)==1,(i,a)
    lo=s.index(a,scope);hi=s.index(b,lo+len(a)) if b else s.index('\n\n',lo)
    z={'id':i,'role':r,'source_anchors':['S2','S3.SS3.SSS0.Px1.p1.1','S3.Ex3'],'source_or_overlay_node':node,'claim':claim,'lean':{'file':str(p),'line':s[:lo].count('\n')+1,'end_line':s[:hi].count('\n')+1,'file_sha256':sha(raw),'start_character_offset':lo,'end_character_offset_exclusive':hi,'exact_start_marker':a,'exact_end_marker_exclusive':b,'exact_locator_block_sha256':sha(s[lo:hi].encode())},'separate_new_Lean_node':False}
    if decl:z['canonical_existing_declaration']=decl
    if provenance:z['source_declaration_provenance']=provenance
    rows.append(z)
for i,r,f,a,b,n,c,body in [
('P-type','public-root',P,'theorem actual_zero_query_gaussian_event_gap',':= by','typed:public-signed-event-gap','Exact signed actual Gaussian event-mass gap, all d>=1,kappa>=4, strict1/8.',False),
('P-objects','definition',P,'  let E','  have hκpos','Z:pair','Literal precisions/inverse covariance measures, first coordinate, scalar intervals and standard Gaussian.',True),
('P-positive-inverse','producer-proof',P,'  have hκpos','  have hp₀','G:normal-law','Internally derive positive diagonal precision and actual inverse; this does not assert the still-separate full source precision-class/algorithm adapter.',True),
('P-marginal-event','producer-proof',P,'  have hp₀','  have hinvpos','G:event-masses','Actual canonical Gaussian coordinate laws and event-mass transport. Direct canonical abs_le matches the closed coordinate slab.',True),
('P-scaling','producer-proof',P,'  have hinvpos','  have hmass','G:event-masses','Internally prove c=sqrt(kappa inverse)<=1/2 and actual scalar Gaussian map; full standard interval is a preimage subset.',True),
('P-mass-monotone','producer-proof',P,'  have hmass','  have hst','G:event-masses','Measurable pushforward and finite real-measure monotonicity give the oriented target probability lower comparison.',True),
('P-band-volume','producer-proof',P,'  have hst','  let a :','G:integral-lower-bound','Exact measurable band difference has finite Lebesgue mass1; closed endpoints retained.',True),
('P-numeric','producer-proof',P,'  let a :','  have haform','G:numerical-comparison','Exact scalar inverse density constant is strictly greater than1/8, using canonical exp/pi inequalities.',True),
('P-density','producer-proof',P,'  have haform','  have hint','G:integral-lower-bound','Pointwise standard Gaussian PDF lower bound over the actual band.',True),
('P-integral','producer-proof',P,'  have hint','  have hdiff','G:integral-lower-bound','Actual integrability/constant set integral and actual Gaussian density formula give the probability-band bound.',True),
('P-gap','producer-proof',P,'  have hdiff','\nend AutoSamplingTheory','typed:public-signed-event-gap','Finite probability difference and true marginal equalities produce the signed gap, not a converse from a TV bound.',True),
('C-type','private-root',T,'private theorem no_common_zero_query_output',':= by','typed:proposed-common-rho-obstruction','Exact arbitrary-common-probability-law obstruction at non-strict1/16, no algorithm model encoded.',False),
('C-objects','definition',T,'  let E','  have hgap','D:TV','Actual target measures, closed coordinate event and literal real measurable-event-supremum TV.',True),
('C-call','consumer-proof',T,'  have hgap','  have hB','typed:public-signed-event-gap','Genuine invocation of the public producer with only source domain bounds.',True),
('C-event','consumer-proof',T,'  have hB','  have hbounded','G:event-measurable','Actual coordinate-event Borelness derived from the concrete Euclidean coordinate.',True),
('C-bounded-sup','consumer-proof',T,'  have hbounded','  have hsup₀','D:TV','Probability masses internally bound the entire event-difference set. No boundedness/TV certificate input.',True),
('C-event-TV','consumer-proof',T,'  have hsup₀','  change ¬','B:TV-triangle','The actual Borel event witnesses both conditional-supremum lower bounds.',True),
('C-contradiction','consumer-proof',T,'  change ¬','\nend AutoSamplingTheory','typed:proposed-common-rho-obstruction','Two non-strict1/16 event differences contradict the genuinely consumed strict1/8 signed gap.',True)
]:add(i,r,f,a,b,n,c,body)
B=Path('.lake/packages/mathlib/Mathlib')
std=[
('Matrix.PosDef.diagonal','LinearAlgebra/Matrix/PosDef.lean','protected theorem diagonal ['),
('Matrix.inv_eq_left_inv','LinearAlgebra/Matrix/NonsingularInverse.lean','theorem inv_eq_left_inv'),
('ProbabilityTheory.measurePreserving_eval_multivariateGaussian','Probability/Distributions/Gaussian/Multivariate.lean','lemma measurePreserving_eval_multivariateGaussian'),
('MeasureTheory.MeasurePreserving.measureReal_preimage','Dynamics/Ergodic/MeasurePreserving.lean','theorem measureReal_preimage {'),
('ProbabilityTheory.gaussianReal_map_const_mul','Probability/Distributions/Gaussian/Real.lean','lemma gaussianReal_map_const_mul ('),
('ProbabilityTheory.gaussianReal_apply_eq_integral','Probability/Distributions/Gaussian/Real.lean','lemma gaussianReal_apply_eq_integral ('),
('ProbabilityTheory.gaussianPDFReal','Probability/Distributions/Gaussian/Real.lean','def gaussianPDFReal ('),
('ProbabilityTheory.integrable_gaussianPDFReal','Probability/Distributions/Gaussian/Real.lean','lemma integrable_gaussianPDFReal ('),
('MeasureTheory.map_measureReal_apply','MeasureTheory/Measure/Real.lean','theorem map_measureReal_apply ['),
('MeasureTheory.measureReal_mono','MeasureTheory/Measure/Real.lean','@[gcongr] theorem measureReal_mono ('),
('MeasureTheory.measureReal_sdiff','MeasureTheory/Measure/Real.lean','theorem measureReal_sdiff ('),
('Real.volume_Icc','MeasureTheory/Measure/Lebesgue/Basic.lean','theorem volume_Icc {'),
('Real.volume_real_Icc','MeasureTheory/Measure/Lebesgue/Basic.lean','theorem volume_real_Icc {'),
('MeasureTheory.setIntegral_const','MeasureTheory/Integral/Bochner/Set.lean','theorem setIntegral_const ['),
('MeasureTheory.setIntegral_mono_on','MeasureTheory/Integral/Bochner/Set.lean','theorem setIntegral_mono_on (hs :'),
('Real.exp_one_lt_three','Analysis/Complex/ExponentialBounds.lean','theorem exp_one_lt_three :'),
('Real.pi_lt_four','Analysis/Real/Pi/Bounds.lean','theorem pi_lt_four :'),
('MeasureTheory.measureReal_le_one','MeasureTheory/Measure/Typeclasses/Probability.lean','lemma measureReal_le_one {'),
('le_csSup','Order/ConditionallyCompleteLattice/Basic.lean','theorem le_csSup ('),
]
for n,f,a in std:add('S-'+n,'canonical-Mathlib-substrate',B/f,a,None,'canonical-library',n+' is an existing canonical dependency, not a new ASTIS node.',decl=n)
add('S-abs_le','canonical-Mathlib-substrate',B/'Algebra/Order/Group/Abs.lean','theorem mabs_le :',None,'canonical-library','Canonical abs_le is reused directly in the producer and consumer, with no new ASTIS equality-conversion alias.',decl='abs_le',provenance='The immediately preceding to_additive attribute generates the existing canonical additive abs_le from this multiplicative mabs_le source theorem. This is Mathlib declaration provenance, not a new ASTIS theorem.')
seal=json.loads((E.parent/'zero-query-separation-statement-seal.json').read_bytes())
for role,i in [('producer','P-type'),('actual_private_consumer','C-type')]:
    z=next(r['lean'] for r in rows if r['id']==i);s=Path(z['file']).read_bytes().decode();assert s[z['start_character_offset']:z['end_character_offset_exclusive']]==seal[role]['signature']
for r in rows:
    z=r['lean'];s=Path(z['file']).read_bytes().decode();assert sha(s[z['start_character_offset']:z['end_character_offset_exclusive']].encode())==z['exact_locator_block_sha256']
x={'schema':2,'locator_convention':'All rows, including roots, use UTF8-decoded Unicode character offsets start-inclusive/end-exclusive with literal LF retained. File SHA256 is raw-byte hash.','producer_sha256':sha(P.read_bytes()),'Test_sha256':sha(T.read_bytes()),'source_graph_base_sha256':'6a04af74551be8374dabd3a9cbd5cbef94f1a92629731c3190c4a4638dbc639b','typed_overlay_sha256':'42462a761b1f2706f0f132c4bf56fb923388c87d505813eec1b40494974a954f','typed_root_map_sha256':'61316ab46089cdf88bcf95881012fe85f2f40e4da752d051d81ca4e77f340d45','derived_separate_integer_branch_scope_label_map_sha256':'e6d1ad7e661fb6aeec27a08eb04d3f5018c67c283f42f53dd22bd0fd72147118','source_relation_boundary':'The selected signed event-mass auxiliary is supported by the actual Gaussian event/integral/numerical path. A TV lower bound alone cannot be reversed into this oriented event gap. Row locators do not certify the whole source node or general background proof. The separate integer branch remains conditional2T+1>d.','actual_owned_declarations':2,'handwritten':2,'generated_auxiliaries':0,'one_canonical_node_per_compiled_declaration':True,'rows':rows,'remaining':['actual Borel seed/stopping/output/deterministic-cap algorithm model and zero-query common-law adapter','full source precision-class membership and uniform-accuracy instantiation','T>=1/Q_G and complete Theorem3.1; disclosed-spectrum/fixed-eigenbasis route','oracle/precision/TV/positive-query-cap/expected-cost adapters','independent full-code/source/native/static acceptance, serialized integration/delivery and purification'],'row_counts_not_math_credit':True}
out=E/'source-to-lean-map-v1.json';assert not out.exists();out.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'rows':len(rows),'map_sha256':sha(out.read_bytes()),'all_exact_locators_and_sealed_types_checked':True}))
