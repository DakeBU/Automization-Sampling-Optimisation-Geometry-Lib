from pathlib import Path
import hashlib,json

E=Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-target-law-semantic-evidence')
P=Path('AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumTargetLaw.lean')
T=Path('Tests/GaussianComplexityFixedSpectrumTargetLaw.lean')
sha=lambda b:hashlib.sha256(b).hexdigest()
rows=[]
def add(ident,role,f,start,end,node,claim,body=False):
    p=Path(f);raw=p.read_bytes();s=raw.decode('utf-8')
    scope=s.index(':= by')+len(':= by') if body else 0
    assert s.count(start,scope)==1,(ident,start,scope)
    a=s.index(start,scope)
    b=s.index(end,a+len(start)) if end else s.index('\n\n',a)
    code=s[a:b]
    rows.append({'id':ident,'role':role,'source_anchors':['S4.E11','S4.SS2.SSS0.Px3.p2.1','A3.SS3.p4'],'source_or_overlay_node':node,'claim':claim,'lean':{'file':str(p),'line':s[:a].count('\n')+1,'end_line':s[:b].count('\n')+1,'file_sha256':sha(raw),'start_character_offset':a,'end_character_offset_exclusive':b,'exact_start_marker':start,'exact_end_marker_exclusive':end,'exact_locator_block_sha256':sha(code.encode('utf-8'))},'separate_new_Lean_node':False})

for i,r,f,a,b,n,c,body in [
('P-type','public-root',P,'theorem actual_rotated_gaussian_target',':= by','ov:producer','Full fixed-O actual Gaussian probability-measure identity, d>=2,kappa>=2, both orthogonal determinant signs.',False),
('P-objects','definition',P,'  let E','  have hApos','ov:aux-parameters','Actual precision matrices, inverse-covariance Gaussians and continuous linear orthogonal rotation.',True),
('P-positive','producer-proof',P,'  have hApos','  have hOleft','bg:precision-positive','Internally invoke canonical actual_precision_admissible for O and identity; no positivity certificate binder.',True),
('P-inverse','producer-proof',P,'  have hOleft','  have hstar','br:inverse-precision-conjugation','Both orthogonal equations and actual matrix left inverse establish A inverse = O Lambda inverse O transpose.',True),
('P-operator','producer-proof',P,'  have hstar','  change μ.map T','br:covariance-conjugation','Existing star-algebra equivalence supplies real adjoint and covariance-operator conjugation.',True),
('P-Gaussian-law','producer-proof',P,'  change μ.map T','\nend AutoSamplingTheory','ov:producer','Gaussian linear image, equal means and full covariance bilinear forms imply actual measure equality via canonical IsGaussian.ext.',True),
('C-type','private-root',T,'private theorem actual_target_gaussian_norm_mean',':= by','ov:consumer-root','Actual target L1 and norm-square integral finite inverse-spectrum sum; not full Lemma4.5 or closed M.',False),
('C-objects','definition',T,'  let E','  have hLaw','ov:target-norm','Literal actual diagonal/target Gaussians, rotation and Euclidean norm-square.',True),
('C-canonical-calls','consumer-proof',T,'  have hLaw','  have hR','br:target-norm-mean','Genuinely invoke public new law and canonical diagonal Gaussian moments at internally fixed n=1; no frequency binder or copied proof.',True),
('C-isometry','consumer-proof',T,'  have hR','  have hmapLint','br:norm-invariance','Actual rotation is measurable and unitary CLM preserves norm; g composed R equals g.',True),
('C-transport','consumer-proof',T,'  have hmapLint','\nend AutoSamplingTheory','ov:consumer-root','Actual public law rewrites both conjuncts; integrable_map_measure and integral_map transport canonical L1/mean.',True),
]:add(i,r,f,a,b,n,c,body)

base=Path('.lake/packages/mathlib/Mathlib')
std=[
('Matrix.toEuclideanCLM','Analysis/CStarAlgebra/Matrix.lean','def toEuclideanCLM :'),
('Matrix.inner_toEuclideanCLM','Analysis/CStarAlgebra/Matrix.lean','lemma inner_toEuclideanCLM'),
('Matrix.mem_orthogonalGroup_iff','LinearAlgebra/UnitaryGroup.lean','theorem mem_orthogonalGroup_iff {'),
('Matrix.mem_orthogonalGroup_iff\u2032','LinearAlgebra/UnitaryGroup.lean',"theorem mem_orthogonalGroup_iff' {"),
('Matrix.inv_eq_left_inv','LinearAlgebra/Matrix/NonsingularInverse.lean','theorem inv_eq_left_inv'),
('Matrix.nonsing_inv_mul','LinearAlgebra/Matrix/NonsingularInverse.lean','theorem nonsing_inv_mul ('),
('multivariateGaussian','Probability/Distributions/Gaussian/Multivariate.lean','def multivariateGaussian'),
('integral_id_multivariateGaussian','Probability/Distributions/Gaussian/Multivariate.lean','lemma integral_id_multivariateGaussian :'),
('covarianceBilin_multivariateGaussian','Probability/Distributions/Gaussian/Multivariate.lean','lemma covarianceBilin_multivariateGaussian'),
('covarianceBilin_map','Probability/Moments/CovarianceBilin.lean','lemma covarianceBilin_map {'),
('ContinuousLinearMap.integral_id_map','Probability/Moments/Basic.lean','lemma integral_id_map (h : Integrable id μ)'),
('IsGaussian.ext','Probability/Distributions/Gaussian/CharFun.lean','protected lemma IsGaussian.ext {'),
('Unitary.map_mem','Algebra/Star/Unitary.lean','lemma map_mem'),
('ContinuousLinearMap.norm_map_of_mem_unitary','Analysis/InnerProductSpace/Adjoint.lean','theorem norm_map_of_mem_unitary'),
('integrable_map_measure','MeasureTheory/Function/L1Space/Integrable.lean','theorem integrable_map_measure {'),
('integral_map','MeasureTheory/Integral/Bochner/Basic.lean','theorem integral_map {β}'),
]
for n,f,a in std:add('S-'+n,'canonical-Mathlib-substrate',base/f,a,None,'canonical-library',n+' is reused existing mathematics, not new ASTIS proof credit.')
for n,f in [('actual_precision_admissible','FixedSpectrumAdmissibility.lean'),('actual_diagonal_gaussian_quadratic_means','FixedSpectrumGaussianMoments.lean')]:
    add('A-'+n,'canonical-ASTIS-parent',P.parent/f,'theorem '+n,'\nend AutoSamplingTheory','canonical-compiled-parent',n+' is the existing compiled declaration; this locator is not a duplicate node.')
for row in rows:
    z=row['lean'];s=Path(z['file']).read_bytes().decode('utf-8');assert sha(s[z['start_character_offset']:z['end_character_offset_exclusive']].encode())==z['exact_locator_block_sha256']
for role,p in [('producer',P),('actual_private_consumer',T)]:
    seal=json.loads((E.parent/'fixed-spectrum-target-law-statement-seal.json').read_bytes())[role]
    rr=next(z for z in rows if z['id']==('P-type' if role=='producer' else 'C-type'))['lean']
    assert p.read_text()[rr['start_character_offset']:rr['end_character_offset_exclusive']]==seal['signature']
x={'schema':2,'locator_convention':'UTF-8 decoded Unicode character offsets, start inclusive/end exclusive, literal LF retained, identical for every row including roots. Whole-file SHA256 is over raw bytes.','producer_sha256':sha(P.read_bytes()),'Test_sha256':sha(T.read_bytes()),'source_graph_original_v2_sha256':'a3d876092b9854614c6d09bba8f1fa4add8d772ba030fa2358526b9c55ac6449','source_delta_seven_ops_sha256':'660724759634bdc66d7082815ccaf0e6c139a173000cf64d67c0cd6f41387700','source_typed_overlay_sha256':'991816a8f58b34509474606e48f7cd29751c1248717e51def9847ca47db0be47','corrected_coverage_sha256':'05a21fc721933dc6ab0e5561b8961ce7c6e27e0a32634ef982062deba6265f3b','source_normalizer_boundary':'A3.Ex160 and A3.SS4.p3.2 are normalizer/partition-function sibling context only, NOT this Gaussian-law/norm-mean conclusion. Original TC HOLD and exact source-author two-string successor both retained.','actual_owned_declarations':2,'one_canonical_node_per_compiled_declaration':True,'rows':rows,'remaining':['full Lemma4.5 moments/variance/pass probability','random-basis joint/conditional and adaptive Haar laws','algorithm/oracle/TV/precision/deterministic worst-query cap/expected-cost comparison','main lower bounds and source-background completeness','independent code/native/source/reader acceptance, global integration, delivery and purification']}
out=E/'source-to-lean-map-v1.json';assert not out.exists();out.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'rows':len(rows),'map_sha256':sha(out.read_bytes()),'all_locator_hashes_and_sealed_types_checked':True,'row_count_is_not_math_credit':True}))
