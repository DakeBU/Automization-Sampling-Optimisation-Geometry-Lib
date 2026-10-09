import hashlib
import json
from pathlib import Path

OUT=Path('E:/Samplinglib/.astis/decoder-63/independent')
capture=json.loads((OUT/'capture.json').read_text(encoding='utf-8'))
decoded=(OUT/'decoded.txt').read_bytes()
slots={
 'hypotheses': {
  'reconstruction':'Finite-dimensional real inner-product Borel E; V:E→ℝ; α,β:ℝ≥0; η:ℝ; α>0; α≤β; ContDiff ℝ 2 V; ∀x v lower and upper iterated-Fréchet Hessian quadratic bounds α‖v‖²≤D²V(x)[v,v]≤β‖v‖²; η>0; βη≤1.',
  'reasoning':'Only binders before colon are public inputs. Probability, closedness support, kernel, equivalence, operators and roots occur after colon. No normalization/integrability/energy certificate added; dimension zero and βη=1 admitted.'},
 'definitions': {
  'reconstruction':'μ=normalized volume tilt by −V; J=(μ⊗stdGaussian).map((x,z)↦(x,x+√ηz)); ν=J.snd; Λ=J.map((x,y)↦(y,2x−y)); F(x,y)=(x,2x−y); mY=comap snd; HP=lpMeas mY 2 J; P=inclusion∘condExpL2; hp internally measures snd-preservation; M=canonical snd pullback; A=orthogonalProjectionOnto∘U∘inclusion; B=((I_H−P) U P)∘inclusion; ΓP=eΓe⁻¹.',
  'reasoning':'Literal lets determine constructions. Λ defining map and F differ. Approved context provides normalized tilt, L² class semantics, positivity and conjugation meanings. ΓP is the transported SAME Γ, not a free second root.'},
 'domains': {
  'reconstruction':'H=L²(J) on E×E; K=L²(ν) on E; HP closed mY-measurable subspace of H. inclusion:HP→H; orthogonalProjectionOnto:H→HP; condExpL2:H→HP; P,U:H→H; M:K→H; e:K≃HP; S:Kernel E E; T,Γ:K→K; A,ΓP,G:HP→HP; B:HP→H; B.adjoint:H→HP.',
  'reasoning':'Operator annotations and subtypes prevent conflation. Identities I_H,I_K,I_HP differ; B.adjoint∘B belongs to HP→HP. All operators are real-linear, endomorphisms continuous where →L or associated continuous-linear map appears; U,M are isometries and e an isometric equivalence.'},
 'quantifiers': {
  'reconstruction':'Universal E/input binders and ∀x v Hessian bounds; ∀f:HP fixed-subspace equality; ∃S with ∀y exact density; ∃e with ∀u:K canonical pullback; ∃U with ∀g:H AE_J action, involution and selfadjointness; ∃T with ∀u:K contraction, AE_ν action and integral invariance; ∀f:HP contraction and separately ∀f:HP leakage annihilation; ∃Γ; ∀f:HP both norm/energy equalities; separate ∀G:HP→LHP positivity→same-square→G=ΓP.',
  'reasoning':'Conjunction parsing keeps ∀G outside ∀f. Every positive same-square G is included, without an alternative energy assumption. Per-observable AE need not share one exceptional set; normalized density holds every y.'},
 'scopes': {
  'reconstruction':'Internal lets precede initial conjunctions; existential order S,e,U,T,Γ. A,B are defined under T; ΓP under Γ. Later witnesses can depend on preceding witnesses. IsCondKernel refers to Λ and SAME S; marginals both ν. HP range/fixed-point equalities and canonical e compatibility are outputs.',
  'reasoning':'Fact(comap≤product) is locally constructed with measurable_snd.comap_le and supports closedness; there is no public subtype/comap certificate. The conclusion constructs hp with measurable_snd and rfl, and e compatibility pins canonical pullback rather than arbitrary isomorphism.'},
 'conclusions': {
  'reconstruction':'μ,J,ν probability; HP=range(P) and P fixes HP; every-state normalized Markov S conditionally disintegrates Λ with both marginals ν; canonical e; joint reflection U is involutive/selfadjoint; T selfadjoint contraction with conditional-integral AE action and mean preservation; A=eTe⁻¹ selfadjoint contraction; P(Bf)=0; positive Γ square I_K−T²; positive transported ΓP square I_HP−A²; B*B=ΓP²; every-f equal leakage/root norm and energy defect; unique positive same-square macro operator.',
  'reasoning':'Every conjunct is retained. No pointwise conditional-action promotion, T-positivity, generic kernel-class uniqueness, source verdict or extra Γ-on-K universal uniqueness claim is made.'},
 'invariants': {
  'reconstruction':'Stationary Λ marginals, P fixed macro subspace, canonical pullback compatibility, U²=I_H, selfadjointness of U/T/A, T integral invariance, exact compression conjugacy, ambient leakage annihilation, root transport and composition-square identities, all-macro energy identity, unrestricted-positive-alternative uniqueness.',
  'reasoning':'Exact class/operator equalities differ from representative AE equalities. Positivity is selfadjointness plus nonnegative quadratic form. The normalization expression, η denominator, 1/2 midpoint and 2x−y reflection coefficients are retained exactly.'}
}
payload={
 'schema_version':1,'decoder':'independent anonymous source-blind decoder',
 'packet_raw_sha256':capture['packet_raw_sha256'],
 'statement_sha256':capture['statement_raw_sha256'],
 'statement_declared_sha256':capture['statement_declared_sha256'],
 'context_sha256':capture['context_sha256'],
 'context_declared_sha256':None,
 'context_declared_sha256_status':capture['context_declared_sha256_status'],
 'context_hash_encoding':capture['context_hash_encoding'],
 'reconstructed_theorem_text':decoded.decode('utf-8'),
 'reconstructed_text_sha256':hashlib.sha256(decoded).hexdigest(),
 'slots':slots,'unresolved_syntax':[],
 'unexpanded_approved_semantics':['Λ.IsCondKernel S is decoded as conditional-kernel disintegration without reading its library body.'],
 'source_text_visible':False,'source_identity_visible':False,'compiler_started':False,
 'source_fidelity_verdict':None,'mathematical_proof_correctness_judgement':None,
}
raw=(json.dumps(payload,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
(OUT/'decoded.payload.json').write_bytes(raw)
result={'decoded_payload_raw_sha256':hashlib.sha256(raw).hexdigest(),
        'reconstructed_text_sha256':hashlib.sha256(decoded).hexdigest()}
(OUT/'payload.hashes.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
