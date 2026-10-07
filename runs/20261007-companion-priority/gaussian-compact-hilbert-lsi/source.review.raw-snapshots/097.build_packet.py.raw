import hashlib, json, pathlib, datetime, re

ROOT = pathlib.Path('E:/Samplinglib')
BASE = ROOT / 'runs/20261007-companion-priority'
OUT = BASE / 'gaussian-hilbert-lsi-preread'
def sha(b): return hashlib.sha256(b).hexdigest()
def lf(b): return b.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
def canon(x): return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
def save(name, x):
    b = (json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    with (OUT/name).open('xb') as f: f.write(b)
    return sha(b)

specs = [
 ('PRIMARY-E6','runs/20261007-companion-priority/gaussian-clt-entropy-preread/primary.S4.E6.raw.snapshot.html'),
 ('PRIMARY-EXPLANATION','runs/20261007-companion-priority/gaussian-clt-entropy-preread/primary.S4.SS1.p4.3.raw.snapshot.html'),
 ('CLOSED-EXTENSION','runs/20261007-companion-priority/gaussian-lsi-extension-preread/source-detail-packet.json'),
 ('SOURCE40-CONTRACT','runs/20261007-companion-priority/gaussian-compact-product-source-graph/source.contract.json'),
 ('SOURCE40-REPAIR-PROVENANCE','runs/20261007-companion-priority/gaussian-compact-product-source-graph/representation-overlay1/repair.json'),
 ('TARGET40-SEALED-INTERFACE','runs/20261007-companion-priority/gaussian-compact-product-preproof/signature.prospective.txt'),
 ('GENERIC32-INTERFACE','runs/20261007-companion-priority/gaussian-sqrt-density-domain/preproof/generic.signature.txt'),
 ('SOURCE32-INTERFACE','runs/20261007-companion-priority/gaussian-sqrt-density-domain/preproof/source.signature.txt'),
 ('SOURCE33-INTERFACE','runs/20261007-companion-priority/standardized-rgo-relative-entropy/preproof/source.signature.txt'),
 ('VERIFIED32','runs/20261007-companion-priority/gaussian-sqrt-density-domain/verified.json'),
 ('VERIFIED33','runs/20261007-companion-priority/standardized-rgo-relative-entropy/verified.json'),
 ('ASTIS-GAUSSIAN-LAW','AutoSamplingTheory/TechnicalLemmas/Measure/IsotropicGaussianDensity.lean'),
 ('ASTIS-GRADIENT','AutoSamplingTheory/TechnicalLemmas/Analysis/Calculus/Gradient.lean'),
 ('ASTIS-PARSEVAL-USE','AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/WeightedBochner.lean'),
 ('ASTIS-GAUSSIAN-MOMENT','AutoSamplingTheory/TechnicalLemmas/Probability/StdGaussianMoment.lean'),
 ('ASTIS-CUTOFF','AutoSamplingTheory/TechnicalLemmas/Analysis/Calculus/Cutoff.lean'),
 ('ASTIS-LSI-BOOKKEEPING','AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/LogSobolev.lean'),
 ('ASTIS-CANONICAL-LSI-INTERFACE','AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/CanonicalLogSobolev.lean'),
 ('M-GAUSSIAN','.lake/packages/mathlib/Mathlib/Probability/Distributions/Gaussian/Multivariate.lean'),
 ('M-BASIS-CONTINUOUS','.lake/packages/mathlib/Mathlib/Topology/Algebra/Module/FiniteDimension.lean'),
 ('M-BASIS-SUM','.lake/packages/mathlib/Mathlib/LinearAlgebra/Basis/Defs.lean'),
 ('M-PARSEVAL','.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/PiL2.lean'),
 ('M-WITHLP','.lake/packages/mathlib/Mathlib/Analysis/Normed/Lp/PiLp.lean'),
 ('M-GRADIENT','.lake/packages/mathlib/Mathlib/Analysis/Calculus/Gradient/Basic.lean'),
 ('M-C2','.lake/packages/mathlib/Mathlib/Analysis/Calculus/ContDiff/Basic.lean'),
 ('M-CHAIN','.lake/packages/mathlib/Mathlib/Analysis/Calculus/FDeriv/Comp.lean'),
 ('M-LINEAR-DERIV','.lake/packages/mathlib/Mathlib/Analysis/Calculus/FDeriv/Linear.lean'),
 ('M-DERIV-SUPPORT','.lake/packages/mathlib/Mathlib/Analysis/Calculus/FDeriv/Const.lean'),
 ('M-SUPPORT','.lake/packages/mathlib/Mathlib/Topology/Algebra/Support.lean'),
 ('M-MAP-L1','.lake/packages/mathlib/Mathlib/MeasureTheory/Function/L1Space/Integrable.lean'),
 ('M-MAP-INTEGRAL','.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Bochner/Basic.lean'),
 ('M-COMPACT-L1','.lake/packages/mathlib/Mathlib/MeasureTheory/Function/LocallyIntegrable.lean'),
 ('M-PHI','.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/Log/NegMulLog.lean'),
 ('SLT-TENSOR','runs/20261007-companion-priority/gaussian-functional-availability/SLT__GaussianLSI__TensorizedGLSI.lean.raw.snapshot'),
 ('SLT-ENTROPY','runs/20261007-companion-priority/gaussian-functional-availability/SLT__GaussianLSI__Entropy.lean.raw.snapshot'),
 ('SLT-CLOSURE','runs/20261007-companion-priority/gaussian-functional-availability/import-closure-audit.json'),
 ('SLT-LICENSE','runs/20261007-companion-priority/gaussian-functional-availability/LICENSE.raw.snapshot'),
 ('SLT-TOOLCHAIN','runs/20261007-companion-priority/gaussian-functional-availability/lean-toolchain.raw.snapshot'),
 ('SLT-MANIFEST','runs/20261007-companion-priority/gaussian-functional-availability/lake-manifest.json.raw.snapshot'),
 ('LOCAL-TOOLCHAIN','lean-toolchain'), ('LOCAL-MANIFEST','lake-manifest.json')
]
inputs=[]; texts={}
for i,(pid,rel) in enumerate(specs):
    raw=(ROOT/rel).read_bytes(); normalized=lf(raw)
    rn=f'input.{i:03d}.raw.snapshot'; ln=f'input.{i:03d}.LF.snapshot'
    for name,data in [(rn,raw),(ln,normalized)]:
        with (OUT/name).open('xb') as f: f.write(data)
    inputs.append(dict(id=pid,path=rel,raw_sha256=sha(raw),lf_sha256=sha(normalized),bytes=len(raw),raw_snapshot=rn,lf_snapshot=ln))
    texts[pid]=normalized.decode('utf-8')
byid={x['id']:x for x in inputs}
assert byid['CLOSED-EXTENSION']['raw_sha256']=='79268f932bd892c8c077c8b4fed162e291d150cac6cfb68409ad87b53723813c'
assert byid['TARGET40-SEALED-INTERFACE']['raw_sha256']=='fc859f057a9242675d2a769fa3b2dbbd7b66764fdbe429f608decf0018511d50'
assert byid['SOURCE32-INTERFACE']['raw_sha256']=='684d27de9e173512093e55b29535d59ae9de58dd5fa607c472873f4187ee7d17'
assert byid['SOURCE33-INTERFACE']['raw_sha256']=='ceb03a6df9a4c62e2240a27e6d2e16224de1d391ca28724330599a37b7a3de25'
assert json.loads(texts['LOCAL-MANIFEST'])['packages'][0]['rev']=='db584cd6d46c92f209a44c0f1c829460d327499d'
input_hash=save('inputs.json',dict(scope='Bounded API/source and sealed interfaces only; full raw/LF snapshots bind files, semantic reading limited to named regions. No40 proof/Test/blind.',inputs=inputs))

regions=[
 ('PRIMARY-E6',1,8,'FIRST4.6 exact W2/Fisher target'), ('PRIMARY-EXPLANATION',1,5,'Printed GaussianLSI plusTalagrand attribution, no adapter proof'),
 ('ASTIS-GAUSSIAN-LAW',24,56,'Existing actual finiteHilbert basis-law consumer, public isotropic density theorem'),
 ('ASTIS-GRADIENT',114,149,'Public gradient continuity and Riesz derivative APIs'),
 ('ASTIS-PARSEVAL-USE',103,113,'Existing local internal Parseval use, not public reusable adapter'),
 ('ASTIS-GAUSSIAN-MOMENT',21,46,'Public true Gaussian L2 moment and covariance use'),
 ('ASTIS-CUTOFF',155,178,'Actual radial definition and plateau/range'), ('ASTIS-CUTOFF',198,201,'C-infinity radial regularity header'),
 ('ASTIS-CUTOFF',235,237,'Uniform C/R derivative bound header'), ('ASTIS-CUTOFF',324,330,'Compact support in finite dimension'),
 ('ASTIS-CUTOFF',339,345,'Existing second derivative bound header, not required by adapter'), ('ASTIS-CUTOFF',390,397,'Actual cutoff tends to one'),
 ('ASTIS-LSI-BOOKKEEPING',3,30,'Bookkeeping only, not a Gaussian producer'), ('ASTIS-CANONICAL-LSI-INTERFACE',8,17,'Explicit interface boundary'),
 ('ASTIS-CANONICAL-LSI-INTERFACE',44,64,'Public LSI/admissibility/score/pair/gamma premises, not applicable as convenience source inputs'),
 ('M-GAUSSIAN',55,73,'Canonical stdGaussian is exact finite orthonormal basis sum map and probability'),
 ('M-GAUSSIAN',128,153,'Genuine law identification/isometry transport, Euclidean alternative'),
 ('M-BASIS-CONTINUOUS',431,457,'Module.Basis.equivFunL continuous direct carrier equivalence'),
 ('M-BASIS-SUM',239,266,'Basis.equivFun_symm_apply exact sum and basis coordinates'),
 ('M-PARSEVAL',277,279,'EuclideanSpace.equiv alternative'), ('M-PARSEVAL',390,445,'OrthonormalBasis.repr/single identity'),
 ('M-PARSEVAL',492,540,'Finite basis reconstruction and exact real Parseval'), ('M-PARSEVAL',1067,1079,'Canonical finite-index orthonormal basis'),
 ('M-WITHLP',1140,1150,'PiLp.continuousLinearEquiv, not a sup/L2 isometry'),
 ('M-GRADIENT',51,83,'Gradient is actual Riesz inverse of fderiv; CompleteSpace required'), ('M-GRADIENT',122,128,'toDual_gradient'),
 ('M-GRADIENT',281,301,'inner_gradient_left/right'), ('M-C2',415,422,'C2 pullback by continuous linear map'),
 ('M-CHAIN',176,179,'Actual fderiv composition'), ('M-LINEAR-DERIV',43,62,'ContinuousLinearMap actual derivative'),
 ('M-DERIV-SUPPORT',378,394,'Compact support of actual fderiv and evaluations'),
 ('M-SUPPORT',559,566,'HasCompactSupport.comp_homeomorph generated additive API'),
 ('M-MAP-L1',354,363,'True integrable map iff and AE strong measurability'),
 ('M-MAP-INTEGRAL',1032,1069,'Actual Bochner map integral, integrability must be separately established'),
 ('M-COMPACT-L1',621,625,'Continuous compact L1'), ('M-PHI',42,63,'Continuous xlogx including0'),
 ('SLT-TENSOR',34,55,'Actual coordinate partial, gradient-square sum, W12 definitions'),
 ('SLT-TENSOR',459,479,'External unbounded product LSI hypotheses and direct source calls'),
 ('SLT-ENTROPY',34,61,'Homogeneous entropy, totalized log/zero-mass convention')
]
inventory=[]
for i,(pid,a,b,why) in enumerate(regions):
    lines=texts[pid].splitlines(); assert b<=len(lines)
    payload=('\n'.join(lines[a-1:b])+'\n').encode('utf-8')
    name=f'region.{i:03d}.LF.snapshot'
    with (OUT/name).open('xb') as f:f.write(payload)
    inventory.append(dict(id=f'R{i:03d}',pin=pid,start_line=a,end_line=b,line_count=b-a+1,role=why,lf_sha256=sha(payload),snapshot=name))
region_hash=save('source-api-regions.json',dict(scope='Exact selected bounded spans; no exhaustive whole-library or upstream closure claim. Inputs bind full raw files, unrelated regions excluded from this dependency audit.',regions=inventory))

signature='''theorem compact_stdGaussian_logSobolev
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [CompleteSpace E] [FiniteDimensional ℝ E]
    [MeasurableSpace E] [BorelSpace E]
    (f : E → ℝ) (hf : ContDiff ℝ 2 f) (hs : HasCompactSupport f) :
    let γ : Measure E := ProbabilityTheory.stdGaussian E
    Integrable (fun x => (f x)^2) γ ∧
    Integrable (fun x => (f x)^2 * Real.log ((f x)^2)) γ ∧
    Integrable (fun x => ‖gradient f x‖^2) γ ∧
    (∫ x, (f x)^2 * Real.log ((f x)^2) ∂γ) -
      (∫ x, (f x)^2 ∂γ) * Real.log (∫ x, (f x)^2 ∂γ) ≤
      2 * ∫ x, ‖gradient f x‖^2 ∂γ
'''
with (OUT/'candidate.signature.txt').open('xb') as f:f.write(signature.encode('utf-8'))
closure=json.loads(texts['SLT-CLOSURE'])
external_leaves=[x for x in closure['files'] if x['path'] in ['SLT/GaussianLSI/TensorizedGLSI.lean','SLT/GaussianLSI/Entropy.lean']]
packet={
 'schema_version':1, 'actor':'gaussian_domain_preproof_reviewer_29', 'status':'BOUNDED_SOURCE_API_READINESS_ONLY',
 'synthesis':'Shortest meaningful delta: transport the compact finite-Pi coefficient2 theorem to actual stdGaussian E using the canonical basis continuous linear equivalence directly, and derive coordinate energy=actual gradient norm squared internally. Canonical Gaussian law identification is already available; the assembled compact Hilbert producer is not yet implemented or admitted by this audit.',
 'truth_contract':'Source/API readiness and mathematically proposed authored background leaf only, not StatementSeal/type elaboration/proof/sourcegraph validation/SAU/repository verification.',
 'primary':{'source':'arXiv2609.06906v1','full_raw_sha256':'ec485cdad5fe140114be35eef93d19398e0cafcf21abb3fff1bdbbf462e5f94d','anchors':['S4.E6 FIRST','S4.SS1.p4.3'],'printed':'W2(r_y,N(0,I)) <= sqrt(integral ||gradient rho_y||^2 d r_y); Gaussian Talagrand plus Gaussian LSI cited with no Hilbert adapter or cutoff proof.','proposed_leaf_attribution':'ASTIS-authored sufficient compact background, not a separately printed SPHMC theorem.'},
 'pins':{'input_bindings_sha256':input_hash,'region_inventory_sha256':region_hash,'inputs':len(inputs),'selected_regions':len(inventory),'selected_lines':sum(x['line_count'] for x in inventory),'Mathlib':'db584cd6d46c92f209a44c0f1c829460d327499d','Lean':'leanprover/lean4:v4.33.0','SLT':'d0f506f0a695018265dccb33bcb05e2f5ca1c876'},
 'candidate':{'full_name':'AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactHilbertLogSobolev.compact_stdGaussian_logSobolev','proposed_file':'AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/GaussianCompactHilbertLogSobolev.lean','signature_file':'candidate.signature.txt','raw_LF_sha256':sha(signature.encode('utf-8')),'typechecked':False,'implementation_exists_by_this_audit':False,'public_analytic_inputs':['actual signed f','ContDiff ℝ 2 f','HasCompactSupport f'],'produced_outputs':['true f² Gaussian L1','true f²logf² Gaussian L1','true gradient-square Gaussian L1','homogeneous entropy <=2 actual Hilbert gradient-square energy'],'suggested_import_floor':['existing40 GaussianCompactProductLogSobolev, conditional until independently admitted','Mathlib.Probability.Distributions.Gaussian.Multivariate','Mathlib.Topology.Algebra.Module.FiniteDimension','Mathlib.Analysis.Calculus.FDeriv.Comp','Mathlib.Analysis.Calculus.Gradient.Basic','ASTIS Analysis.Calculus.Gradient if its public continuity/Riesz bridges are actually called'],'failure_policy':'If direct equivalence elaboration/API issue appears, retain exact no-certificate mathematical target and diagnose typed adapter failure; Euclidean carrier alternative may be internal, never a supplied law or Parseval binder.'},
 'route_at_most_seven_steps':[
  {'step':1,'action':'Choose n=finrank ℝ E and b=stdOrthonormalBasis ℝ E internally. Let T=(b.toBasis.equivFunL).symm from default Pi(Fin n,ℝ) to E.','api':['Module.Basis.equivFunL: M-BASIS-CONTINUOUS445–452','Basis.equivFun_symm_apply: M-BASIS-SUM243–245','stdOrthonormalBasis: M-PARSEVAL1076–1079'],'output':'T continuous linear homeomorphism; T x=sum_i x_i • b_i, including Fin0.'},
  {'step':2,'action':'Identify gamma=(pi_i gaussianReal0 1).map T from the literal canonical stdGaussian definition; derive probability and Borel measurable transport internally.','api':['ProbabilityTheory.stdGaussian: M-GAUSSIAN66–68','isProbabilityMeasure_stdGaussian: M-GAUSSIAN72–73','stdGaussian_eq_map_pi_orthonormalBasis: M-GAUSSIAN146–153'],'output':'Actual law equality, not just covariance-isotropy or an input assumption.'},
  {'step':3,'action':'Set g=f∘T. Pull C2 and compact support along T using continuous linear composition/homeomorphism. Apply exact40 compact_gaussian_pi_logSobolev interface only after independent admission.','api':['ContDiff.comp_continuousLinearMap: M-C2420–422','HasCompactSupport.comp_homeomorph generated at M-SUPPORT563–566','TARGET40-SEALED-INTERFACE1–12'],'output':'All true product-domain L1 outputs and product entropy bound2. No RMS marginal regularity argument or mass certificate.'},
  {'step':4,'action':'Chain rule gives D_i g(x)=fderiv f(Tx)(T(Pi.single i 1))=fderiv f(Tx)(b_i)=inner ℝ(gradient f(Tx))(b_i).','api':['fderiv_comp: M-CHAIN177–179','ContinuousLinearMap.hasFDerivAt: M-LINEAR-DERIV57–58','Basis.equivFun_self: M-BASIS-SUM265–266, inverse equivalence yields T(single)=b_i','inner_gradient_left: M-GRADIENT291–292','ASTIS fderiv_apply_eq_inner_gradient_of_differentiableAt1144–149 (line144–149, no new certificate)'],'output':'Actual coordinate derivative identity for the same f and pointTx. C2 supplies genuine differentiability.'},
  {'step':5,'action':'Apply b.sum_sq_inner_left to gradient f(Tx), obtaining sum_i(D_i g x)^2=||gradient f(Tx)||² exactly.','api':['OrthonormalBasis.sum_sq_inner_left: M-PARSEVAL537–540'],'output':'No dimensional factor, no sup-norm operator norm substitution, no basis/certificate public premise.'},
  {'step':6,'action':'Use continuity/measurability and integrable_map_measure to transport true product L1 to gamma for all three integrands; map integrals carry both entropy integrals and energy.','api':['ASTIS continuous_gradient_of_contDiff_one: ASTIS-GRADIENT114–119','Real.continuous_mul_log: M-PHI45–63','integrable_map_measure: M-MAP-L1356–360','integral_map: M-MAP-INTEGRAL1043–1045'],'output':'True Hilbert domains and equalities before comparing totalized Bochner integrals. Compact derivative support also supplies an independent local domain route.'},
  {'step':7,'action':'Rewrite exact product inequality by these law and energy equalities to obtain entropy_gamma(f²)<=2 integral||gradientf||²gamma.','api':['TARGET40-SEALED-INTERFACE10–12'],'output':'Compact finite-Hilbert result only, including signedf, zerof, zeromass, E0. No noncompact/T2/paper claim.'}
 ],
 'carrier_route_comparison':{'preferred':'Direct canonical finite Basis.equivFunL.symm; one coordinate continuous linear equivalence and exact stdGaussian defining sum-map.','alternative':'T=b.repr.symm ∘ WithLp.toLp2 via EuclideanSpace.equiv.symm, law from map_pi_eq_stdGaussian and stdGaussian_map. Same genuine mathematics, additional carrier/map composition stage.','warning':'T from default Pi sup norm to E is a continuous linear equivalence, not claimed isometric. OrthonormalBasis.repr is isometric only for EuclideanSpace L2 carrier. Parseval uses real orthonormal directional coefficients, not a Pi operator-norm identity.','availability':'Both actual law routes exist in pinned Mathlib. No typed law-identification obstruction found.'},
 'binder_definition_audit':{
  'E_classes':{'classification':'TYPECLASS','expansion':'Real finite-dimensional complete Hilbert carrier, canonical norm/inner product, compatible given MeasurableSpace/BorelSpace. CompleteSpace retained to match32 and Riesz gradient API; finite dimension already yields completeness as a mathematical consequence.'},
  'f':{'classification':'OBJECT','expansion':'actual signed Real-valued function on E, no positivity or normalization'},
  'C2_compact':{'classification':'AUTHORED_DOMAIN_RESTRICTION','expansion':'Bounded sufficient precursor to source full Gaussian LSI; strictly smaller than actual32 noncompact class, not printed source assumption'},
  'gamma':{'classification':'DEFINITION','expansion':'ProbabilityTheory.stdGaussian E, centered identity covariance in actual Hilbert metric; variance1 scalar product transported by orthonormal basis'},
  'gradient':{'classification':'DEFINITION','expansion':'(InnerProductSpace.toDual ℝ E).symm(fderiv ℝ f x), genuine under C2; no AE RN representative differentiation'},
  'entropy':{'classification':'DEFINITION','expansion':'integral f²logf² - m logm; Real.log0 totalized and continuous xlogx at0; homogeneous, no mass1 required'},
  'law_probability_basis_Parseval_domains_bound':{'classification':'DERIVED_INTERNAL_DEPENDENCIES','expansion':'Derived from actual definitions, finite-dimensional basis, C2/compact and exact40 outputs; never theorem binders'},
  'certificates':{'classification':'EXCESS_IF_PUBLIC','items':['supplied Gaussian law identification','supplied Parseval','supplied L1/probability/normalization','supplied desired HilbertLSI','pointwise smooth canonicalRN/llr representative']}
 },
 'hidden_domains':{'T':'Continuous linear homeomorphism implies Borel measurability; Gaussian map matches the literal law.','g':'C2 and compact support genuinely pulled back along T; no dependence on merely continuous RMS square-root marginal.','integrands':'f² continuous compact; Phi(f²) continuous compact since Phi0=0; gradient continuous from C2 and support controlled by fderiv. Or use true40 transported L1, with AE strong measurability proved before map iff.','map_integrals':'Bochner integral equality alone can hold totalized without L1; public domains must be separately obtained via true40 L1 and integrable_map_measure.','E0':'finrank0 implies singleton carrier; canonical Gaussian mass1, f constant, gradient0, empty Parseval sum0 and homogeneous entropy0. Zero-dimensional compact support includes every function.','E1':'Centered variance1 law, coefficient2 unchanged; orientation of basis sign cancels squared directional energy.','mass0':'No division by integral f²; mlogm uses Real.log0.','signed':'Use actual f²; no abs/sqrt differentiability introduced.'},
 'actual32_33_consumer':{'parents':[{'interface':'SOURCE32-INTERFACE','verified_commit':json.loads(texts['VERIFIED32'])['verified_commit']},{'interface':'SOURCE33-INTERFACE','verified_commit':json.loads(texts['VERIFIED33'])['verified_commit']}],'same_objects':'p,R,r,rho,gamma,Z,q and f=exp(-rho/2)/sqrtZ. Source33 stationary uniqueness matches any separately obtained32 selector; all eta>0 including unrestricted largeeta and E0.','existing32':'C2f; f²=q; positiveZ; integralqgamma=1; f and gradientf MemLp2 gamma; Integrable qlogqgamma; exact energy=Fisher(rho,r)/4.','existing33':'Actual canonical ENNReal KL finite, AE[r]llr=logq, actualKL.toReal=integral qlogqgamma; no pointwise RN derivative conclusion.','next_after_adapter':'Apply compact Hilbert LSI to radial cutoff f_R=radialSmoothCutoff R * f; prove entropy/mass and gradient-energy limits using32 true domains. Derive actualKL.toReal <= (1/2) integral||gradientrho||²r only after that new cutoff proof.','cutoff_details':'Existing actual radialSmoothCutoff APIs supply0<=chi<=1, C-infinity, compact support, chi_R->1 and ||fderiv chi_R||<=C/R. Need genuine product gradient and L2 convergence, plus entropy bound |Phi(chi²q)|<=|Phi(q)|+q/e (0<=chi<=1) for DCT. No f third derivative or normalization of each f_R is needed.','positive_dimension':'Actual32 f is strictly positive everywhere and cannot have compact support on positive-dimensional E. Existing C2/positive normalization is not compact membership.','constants':'compact coefficient2;32 energy1/4 yields KL<=Fisher/2 after cutoff; separate Gaussian T2 W2²<=2KL would then yield FIRST W2<=sqrtFisher. T2 not proved here.'},
 'source_external_audit':{'SLT_revision':closure['revision'],'source_files':external_leaves,'license':'Apache-2.0 exact frozen LICENSE','upstream_toolchain':closure['toolchain'],'upstream_Mathlib':closure['mathlib_revision'],'status':'external-reference only; previous import-closure static receipt retained, no upstream build/evaluation and no bulk port','current_direct_placeholder_scan':{pid:bool(re.search(r'\b(sorry|admit|axiom)\b',texts[pid])) for pid in ['SLT-TENSOR','SLT-ENTROPY']},'dependency_placeholders':'Existing CLOSED static import-closure receipt has [] placeholder hits on the selected leaves; not a fresh whole-upstream closure audit or proof certification.','hypotheses':'External gaussian_logSobolev_W12_pi requires MemW12GaussianPi (MemLp2f and allpartialMemLp2), genuine Differentiable, continuouspartials and Phi(f²)L1. Coordinateenergy is literal finite sum of squared directional derivatives. These are internally supplied by compact40, not imported as convenience public source hypotheses.'},
 'typed_boundaries':[
 {'type':'UNASSEMBLED_LOCAL_ANALYTIC_ADAPTER','first_unmet_edge':'Proposed compact finiteHilbert functionLSI assembly; primitives available, new theorem unimplemented/untyped/uncompiled.'},
 {'type':'CONDITIONAL_FORMAL_PARENT_ADMISSION','edge':'Exact40 678-byte interface is frozen; root reports whole mathematics passed and canonical source admission ongoing. This audit neither reads40body nor promotes that report to VERIFIED.'},
 {'type':'NONCOMPACT_C2_CUTOFF_LIMIT_GAP','edge':'Actual32 f is not compact in positive dimension; entropy/mass/Dirichlet limit proof still needed despite existing cutoff functions.'},
 {'type':'CANONICAL_REPRESENTATIVE_GAP','edge':'AE llr/logq and canonical RN density identities do not authorize arbitrary pointwise derivatives; actualq/f route avoids that unnecessary premise.'},
 {'type':'GAUSSIAN_T2_METRIC_GAP','edge':'A real Gaussian transport-entropy theorem and true HilbertW2 adapters remain absent from this result; named coupling/value definitions do not produce T2.'}
 ],
 'remaining_open':['full noncompact/W12 finiteHilbert GaussianLSI','canonical RN pointwise differentiation if demanded by another interface','Gaussian T2 and FIRST4.6 W2/Fisher consumer','bias/main/work/cost/algorithm/composition','reader/postmerge PURIFIED delivery'],
 'exposure_attestation':{'primary_read_before_new_candidate':True,'root_future_candidate_read':False,'40_implementation_Test_blind_read':False,'32_33_bodies_read':False,'existing_API_context_read':'Only named existing local API regions; WeightedBochner internal Parseval and IsotropicGaussianDensity prior law-use examples are substrates, not inferred40source topology.','sourcegraph_selfvalidation':False,'new_sourcegraph_feature_work':False,'Lean_compiler_started':False,'proof_search':False,'canonical_shared_site_ledger_mutations':False,'history':'Actor authored earlier source40 graph/representation overlay; current audit uses its frozen source contract for coordinate conventions only, no validation of own graph. No candidate implementation is authored.'},
 'compiled_edges':[]
}
# Correct a descriptive API span typo before freezing the packet.
packet['route_at_most_seven_steps'][3]['api'][-1]='ASTIS fderiv_apply_eq_inner_gradient_of_differentiableAt: ASTIS-GRADIENT144–149'
packet_hash=save('source-detail-packet.json',packet)
checks={ 'inputs_stable':[], 'compiler':'NEVER_STARTED','canonical_mutations':False }
for x in inputs:
    raw=(ROOT/x['path']).read_bytes(); assert sha(raw)==x['raw_sha256']; checks['inputs_stable'].append(x['id'])
checks.update(public_input_certificate_count=0,law_API_obstruction_found=False,proof_completion_credit=False,sourcegraph_selfvalidation=False)
checks_hash=save('checks.json',checks)
run_basis={'inputs':[(x['id'],x['raw_sha256'],x['lf_sha256']) for x in inputs],'regions_sha256':region_hash,'packet_sha256':packet_hash,'checks_sha256':checks_hash,'candidate_sha256':sha(signature.encode('utf-8'))}
run_hash=sha(canon(run_basis))
save('run.json',dict(artifact_kind='deterministic-bounded-source-api-preread-run',run_sha256=run_hash,basis=run_basis,not_statement_seal=True,not_proof_or_verification=True))
lease=json.loads((OUT/'lease.json').read_text(encoding='utf-8'))
lease.update(status='CLOSED',read_lease='CLOSED',write_lease='CLOSED',Python_lease='CLOSED',compiler_lease='CLOSED',compiler_started=False,closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),run_sha256=run_hash,packet_sha256=packet_hash)
(OUT/'lease.json').write_bytes((json.dumps(lease,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
save('lease.closed.raw.snapshot.json',lease)
print(json.dumps({'packet_sha256':packet_hash,'run_sha256':run_hash,'input_count':len(inputs),'region_count':len(regions),'selected_lines':sum(x['line_count'] for x in inventory),'candidate_sha256':sha(signature.encode('utf-8')),'leases':'CLOSED','compiler':'NEVER_STARTED'}))
