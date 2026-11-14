from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,shutil

ROOT=Path('/Users/zhouhuanjian/ASTIS-GC')
OUT=ROOT/'.astis/semantic-neutral-20261108/src_4e8f6a/phase2'
INPUT=ROOT/'.astis/semantic-neutral-20261108/src_4e8f6a/phase2-selective-input.json'
PHASE1='cf4dd57dc05d19cb3ca6938032a7730d402aba6220a200ae4a3afe2aca721fac'
EXPECTED_INPUT='eff8df755f5b59f14529de5308cb722d8ef539f2bf1c24c980b089044084b6a2'
H=lambda data:hashlib.sha256(data).hexdigest()
canonical=lambda obj:json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def dump(name,obj):
    p=OUT/name
    with p.open('x') as f:
        f.write(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

raw=INPUT.read_bytes()
assert H(raw)==EXPECTED_INPUT
obj=json.loads(raw)
packet=obj['anonymous_decoder_packet']
lean=packet['lean']
recon=obj['blind_reconstruction']
packet_without_self=dict(packet)
packet_without_self.pop('packet_sha256')
assert H(lean['statement'].encode())==lean['statement_sha256']
assert H(recon['reconstructed_theorem_text'].encode())==recon['reconstructed_text_sha256']
assert H(canonical(packet_without_self))==packet['packet_sha256']
assert H(canonical(packet))==obj['provenance']['whole_JSON_canonical_sha256']
assert packet['packet_sha256']==recon['packet_sha256']
assert obj['provenance']['own_source_phase1_freeze_manifest_raw_sha256']==PHASE1
with (OUT/'inputs/phase2-selective-input.json').open('xb') as f:
    f.write(raw)
dump('input_hash_receipt.json',{
 'input_original_path':str(INPUT),'input_snapshot':'inputs/phase2-selective-input.json',
 'input_raw_bytes':len(raw),'input_raw_sha256':H(raw),
 'statement_utf8_sha256':H(lean['statement'].encode()),
 'reconstructed_text_utf8_sha256':H(recon['reconstructed_theorem_text'].encode()),
 'canonical_rule':'UTF-8, ensure_ascii=false, sort_keys=true, compact separators comma/colon',
 'anonymous_packet_canonical_excluding_packet_sha256':H(canonical(packet_without_self)),
 'anonymous_packet_canonical_including_packet_sha256':H(canonical(packet)),
 'hash_distinction':'The self-field packet hash excludes its own hash field; whole-JSON canonical hash includes that field. Both match their distinct recorded values. This is not an error or a provenance discrepancy.',
 'phase1_freeze_reference_sha256':PHASE1,
 'decoder_run_raw_sha256_reported':recon['decoder_run_sha256'],
 'decoder_original_manifest_raw_sha256_reported':recon['original_manifest_sha256'],
 'verification_limit':'Text and packet hashes were computed from the only permitted new input. Original decoder files named in provenance were not opened or independently re-audited. The compiled=true field is reported metadata, not fresh Lean evidence from this reviewer.'
})

counterparts=[
 {'source_claim_id':'H4-02','anchors':['S4.SS1.p1','S4.E11'],
  'role':'exact-local-definition-counterpart',
  'instantiation':'For i∈Fin d put j=i.val+1. The source angle ((j−1/2)π/d) becomes ((i.val+1/2)π/d); λ_j and OΛOᵀ then equal the anonymous local definitions in coordinates.',
  'scope':'d≥2, κ≥2, every full real orthogonal O; no random draw is needed for this pointwise component.',
  'limits':'The source prior also draws O Haar independently of the seed. That prior is not asserted or needed by this deterministic pointwise proposition.'},
 {'source_claim_id':'P2-04','anchors':['S2.SS0.SSS0.Px1.p1','S2.E1'],
  'role':'primary-mathematical-counterpart-as-a-family-instance',
  'instantiation':'Take source A equal to the H4-02 constructor. Identify EuclideanSpace and WithLp coordinates with R^d. The pair (f_A(x),∇f_A(x))=(⟨x,Ax⟩/2,Ax) becomes exactly the second conjunct.',
  'scope':'A restricted fixed-spectrum instance of the general exact first-order formula.',
  'limits':'The general source formula covers every A∈A_(d,κ), d≥1, κ≥1. Anonymous A is a local let, not an arbitrary precision matrix. Its membership in the source precision class is a separate constructed-family fact.'},
 {'source_claim_id':'C4-02','anchors':['A3.SS4.p2'],
  'role':'calculus-support-and-partial-conclusion-counterpart',
  'instantiation':'The source quadratic V_A=f_A is C∞ with Hessian A. The anonymous genuine HasGradientAt conjunct makes differentiability, implicit in the source gradient notation and smoothness assertion, explicit at every x.',
  'scope':'Same local family and Euclidean quadratic.',
  'limits':'C∞ and Hessian=A are not explicit conclusions of the anonymous proposition. The first-derivative identity is a local calculus component, not a lossless restatement of all C4-02.'},
 {'source_claim_id':'P2-05','anchors':['S2.SS0.SSS0.Px1.p2'],
  'role':'algebraic-oracle-information-subcomponent',
  'instantiation':'The explicit Ax query and pair identity substantiate the algebraic fact that a matrix–vector reply determines this quadratic value and gradient.',
  'scope':'Pointwise response interpretation, restricted to the constructed family.',
  'limits':'No transformation of adaptive Borel algorithms, reverse simulation theorem, cost equality or uniform query-complexity result is stated. The entire P2-05 assertion is broader.'},
 {'source_claim_id':'P2-01','anchors':['S2.p1'],
  'role':'standard-notation-definition-bridge',
  'instantiation':'Ordinary finite real matrix multiplication, dot product, inner product and Euclidean coordinates.',
  'scope':'Typing and representation, using the approved standard definition context.',
  'limits':'No new project-owned semantic adapter or fallback is authorized.'},
 {'source_claim_id':'P2-02','anchors':['S2.p2'],
  'role':'partial-standard-orthogonal-group-definition-bridge',
  'instantiation':'The anonymous orthogonalGroup permits OᵀO=OOᵀ=I and both determinant signs, matching the full source O(d).',
  'scope':'Deterministic universal group carrier.',
  'limits':'Haar probability and determinant-conditioned μ_(d,b) are not assertions of the candidate.'},
 {'source_claim_id':'H4-16','anchors':['S4.Thmtheorem6'],
  'role':'source-class-instantiation-proof-ingredient-not-candidate-conclusion',
  'instantiation':'Lemma 4.6 supplies the Loewner bounds for the constructor when interpreting P2-04 on its source input class; real diagonal orthogonal conjugation also supplies symmetry.',
  'scope':'Local d≥2, κ≥2 and every O.',
  'limits':'The anonymous statement contains no Loewner conclusion. It cannot stand in for the printed admissibility theorem. Direct quadratic differentiation needs symmetry, not the spectral bounds.'},
 {'source_claim_id':'C4-01','anchors':['A3.SS4.p1'],
  'role':'supporting-source-proof-component-not-candidate-conclusion',
  'instantiation':'Angle/cosine/eigenvalue bounds explain the admissibility ingredient for source-class instantiation.',
  'scope':'Local construction only.',
  'limits':'Strict eigenvalue inequalities and Loewner bounds are absent from the anonymous conclusions and must not be counted as proved by this comparison.'}
]
dump('selected_source_counterparts.json',{
 'phase1_manifest_sha256':PHASE1,
 'selection_basis':'Independent selection from the 50 frozen source clauses after reading the anonymous proposition; no target/module/author/verdict context.',
 'primary_counterpart':'P2-04 instantiated by H4-02; with explicit genuine differentiability justified by the source calculus context and ordinary quadratic-gradient meaning.',
 'counterparts':counterparts,
 'non_equivalence_warning':'This local first-order component is not the entire global §2 oracle-complexity claim, Lemma 4.6, C.4, Theorem 4.1, or a normalizer/affine-comparison theorem.'
})

slots=[
 {'slot':'objects',
  'source':'H4-02 defines θ,λ,Λ,A; P2-04 defines f_A and FO_A; C4-02 uses the same quadratic under V_A notation.',
  'anonymous':'Local θ,A,f,query where query(x)=Ax in coordinates; HasGradientAt and the value/gradient ordered pair.',
  'reconstruction_check':'Decoder retains every local let and identifies ordinary quadratic/matrix–vector meanings, without turning A,θ,f,query into independent quantified inputs.',
  'classification':['same-under-standard-coordinate-identification','restricted-source-instance','broader-source-objects-omitted'],
  'reason':'The constructed precision is exactly the source family. No target Gaussian, covariance matrix as a queried object, Z, A_2, algorithm, seed or query budget occurs in the proposition.',
  'local_component_blocking_delta_found':False,
  'broader_scope_boundary':'Do not import target-law, normalizer, affine, admissibility or algorithmic objects as additional candidate conclusions.'},
 {'slot':'quantifiers',
  'source':'Local H4-02: d≥2,κ≥2, all family indices; H4-16/C4 pointwise conclusions hold for every O; P2-04 first-order formula holds for all x on the admissible class.',
  'anonymous':'For all natural d with hd:2≤d, real κ with hκ:2≤κ, full orthogonal O, then local lets, then every Euclidean x; two conjuncts at that x.',
  'reconstruction_check':'Decoder accurately retains order, implicit d/κ universality, explicit proof arguments, full-O universality and all-x conjunction.',
  'classification':['same-local-quantifiers','narrower-than-global-P2-04','no-added-probabilistic-quantifier'],
  'reason':'The all-O deterministic component matches. d≥2 and κ≥2 are source local-family bounds; relative to §2 alone these omit d=1,κ∈[1,2) and arbitrary admissible matrices.',
  'local_component_blocking_delta_found':False,
  'broader_scope_boundary':'No δ,d₀,q,n,ε,cap or seed is needed for this local component. Their absence does not weaken a local calculus statement, but prevents claiming the full lower bound.'},
 {'slot':'domain',
  'source':'Real R^d, one-based i=1,…,d cosine nodes and full real O(d); pointwise quadratic calculus.',
  'anonymous':'EuclideanSpace R (Fin d), Fin values 0,…,d−1; real matrices, ordinary real trigonometric/division operations and full orthogonalGroup.',
  'reconstruction_check':'Decoder explicitly handles zero-based indexing, coordinate-preserving WithLp maps and both determinant signs.',
  'classification':['representational-same','requires-index-and-coordinate-bridges'],
  'reason':'j=i.val+1 exactly converts θ_j=(j−1/2)π/d into the anonymous angle. Coordinate maps preserve the vector, multiplication and Euclidean inner product.',
  'local_component_blocking_delta_found':False,
  'broader_scope_boundary':'This is neither a complex/vector-space variant nor a restriction to determinant +1. No off-source fallback is introduced by WithLp in the supplied context.'},
 {'slot':'assumptions',
  'source':'Local family requires d≥2,κ≥2,O orthogonal. The source precision interpretation additionally uses derived symmetry and I⪯A⪯κI; source calculus has the explicit symmetric quadratic.',
  'anonymous':'Exactly hd,hκ and O membership; A,f,query fixed by lets. No gradient-existence, C∞, Hessian, Loewner, normalizer, query-correctness or probability premise is added.',
  'reconstruction_check':'Decoder does not add symmetry, positivity, regularity or derivative existence as hypotheses; genuine derivative existence is the conclusion.',
  'classification':['same-local-source-assumptions','typing-representation-only-adapters','independent-proof-ingredients-not-binders'],
  'reason':'Symmetry follows from O diag(λ) Oᵀ and must be discharged in a proof; local spectral bounds can justify instantiation of the global source class. They are not arbitrary extra binders. Family restrictions need not be logically minimal for quadratic differentiation to remain source-faithful local restrictions.',
  'local_component_blocking_delta_found':False,
  'broader_scope_boundary':'No claim is made that orthogonality or κ≥2 is mathematically necessary for the bare derivative identity. Removing them would be a separate generalization, not a source repair forced by this comparison.'},
 {'slot':'conclusion',
  'source':'P2-04: gradient Ax and FO_A(x)=(xᵀAx/2,Ax). C4-02: the family quadratic is genuinely smooth, with Hessian A.',
  'anonymous':'Every x has HasGradientAt f (query x) x and (f x,gradient f x)=(inner x (query x)/2,query x).',
  'reconstruction_check':'Decoder keeps both conjuncts and the Riesz derivative meaning; it distinguishes actual HasGradientAt from the fallback of the totalized gradient.',
  'classification':['same-local-first-order-formula','source-implicit-differentiability-made-explicit','full-C4-conclusions-not-restated'],
  'reason':'With query=Ax and standard coordinates, the pair matches the source formula. The differentiability conjunct gives the genuine mathematical meaning of ∇f instead of allowing a fallback value to stand alone. It is not a strengthened premise.',
  'local_component_blocking_delta_found':False,
  'broader_scope_boundary':'No explicit C∞, Hessian=A, strong convexity, smoothness bound, minimizer, Loewner bound, normalizer, covariance or complexity conclusion. Such facts can be separate mathematical consequences of the construction, but are not credited by this statement-level comparison.'},
 {'slot':'use',
  'source':'P2-04/P2-05 identify exact matrix–vector information with the quadratic value and gradient; C4 calculus supports the Gaussian hard instance in a smooth-potential setting.',
  'anonymous':'A local pointwise oracle/calculus interface for the constructed family.',
  'reconstruction_check':'The reconstruction describes the proposition without inventing a downstream use or theorem identity.',
  'classification':['same-algebraic-oracle-use','partial-component-of-broader-simulation'],
  'reason':'The response pair can be interpreted as exact first-order information. The statement itself does not provide a sampler, adaptive simulation, reverse simulation, or equality of query complexities.',
  'local_component_blocking_delta_found':False,
  'broader_scope_boundary':'No whole-result completion, algorithmic lower bound, general-potential lower bound or normalizer result follows as a publication credit from this comparison alone.'},
 {'slot':'failure_boundary',
  'source':'Frozen source differentiates local parameters from the main theorem; full O from same-O affine pairing; queried precision from covariance; deterministic cap from expected cost; and standard bridges from finished proof.',
  'anonymous':'Local all-O exact derivative/pair assertion only, with no random experiment, second matrix, sampling law, costs or asymptotic constants.',
  'reconstruction_check':'Decoder makes no claims of a target distribution, normalizer, affine pairing, Haar independence, cap, expected cost, or extension to smaller d/κ.',
  'classification':['same-local-boundary','broader-source-coverage-explicitly-limited','proof-validation-deferred'],
  'reason':'There is no constant-dependence drift: only d,κ and the exact coefficient 1/2 appear. The true differentiability conjunct blocks semantic reliance on total-gradient fallback at nonexistent derivatives.',
  'local_component_blocking_delta_found':False,
  'broader_scope_boundary':'Conditional statement-level match only under supplied standard definitions. Whole-module/elaboration/proof/publication/reader context and fresh Lean remain uninspected and cannot be presumed clean.'}
]
bridges=[
 {'id':'B01','kind':'standard-definition/indexing',
  'statement':'j=i.val+1 is a bijection between Fin d coordinates and source indices 1,…,d; (j−1/2)=(i.val+1/2) after real casts.',
  'scope':'Exact source-family formula, not a changed node grid or reordered spectrum.',
  'status':'Definition-level same; a formal implementation must justify cast/arithmetic identities.'},
 {'id':'B02','kind':'standard-definition/coordinate-carrier',
  'statement':'WithLp.ofLp and WithLp.toLp 2 preserve the same coordinates; dot product/mulVec give xᵀAx and Ax; real Euclidean inner agrees with dot product.',
  'scope':'Approved standard context only.',
  'status':'No project-owned meaning change or invented fallback is supplied.'},
 {'id':'B03','kind':'standard-definition/orthogonal-group',
  'statement':'Full real orthogonalGroup has transpose inverse in both orders, permits determinant ±1 and matches source O(d).',
  'scope':'Pointwise ∀O, without Haar randomness.',
  'status':'Same carrier; a same-O affine comparison is not present.'},
 {'id':'B04','kind':'independent-proof-ingredient/symmetry',
  'statement':'For real diagonal Λ, (OΛOᵀ)ᵀ=OΛOᵀ, so A is symmetric.',
  'scope':'Needed for the usual quadratic-gradient identity; no new symmetry premise is licensed.',
  'status':'Mathematical bridge, not a definition and not proof-checked in this phase.'},
 {'id':'B05','kind':'independent-proof-ingredient/quadratic-differentiability',
  'statement':'A symmetric real quadratic x↦xᵀAx/2 has genuine Frechet derivative h↦⟨Ax,h⟩ at every x.',
  'scope':'The source ∇f_A formula and C∞ calculus context.',
  'status':'Standard mathematical fact; proof of the actual candidate is reserved for the later whole-module/fresh-Lean stage.'},
 {'id':'B06','kind':'standard-definition-plus-proof-ingredient/gradient',
  'statement':'HasGradientAt f (query x) x supplies the derivative whose inverse Riesz image is gradient f x, so the total-fderiv zero fallback is irrelevant at this x.',
  'scope':'Uses the genuine differentiability conjunct, not an assumption added outside the theorem.',
  'status':'Standard context explains semantics; actual use in proof uninspected.'},
 {'id':'B07','kind':'definition-and-algebra/value-identity',
  'statement':'Coordinate preservation gives f x=inner R x (query x)/2.',
  'scope':'The first component of the ordered pair.',
  'status':'Representational/algebraic identity; no normalizer or target distribution involved.'},
 {'id':'B08','kind':'source-instantiation-proof-ingredient/admissibility',
  'statement':'To invoke the general §2 formula with this A as a precision-class member, establish symmetry and I⪯A⪯κI from the family, using H4-16/C4-01.',
  'scope':'Required for identifying the input as a source admissible precision. The bare symmetric quadratic derivative can instead be established directly without spectral bounds.',
  'status':'Separate source proof ingredient. Anonymous proposition does not conclude admissibility and this comparison does not award it.'}
]
dump('seven_slot_comparison.json',{
 'stage':'PHASE2_SELECTIVE_ANONYMOUS_COMPARISON',
 'phase1_manifest_sha256':PHASE1,'phase2_input_raw_sha256':H(raw),
 'statement_sha256':lean['statement_sha256'],
 'reconstruction_sha256':recon['reconstructed_text_sha256'],
 'source_selection':'P2-04 restricted via H4-02, with ordinary source calculus/gradient semantics; additional supporting and limited counterparts separately typed.',
 'seven_slots':slots,'necessary_definition_and_mathematical_bridges':bridges,
 'provisional_semantic_conclusion':{
  'type':'STATEMENT_LEVEL_MATCH_FOR_SELECTED_LOCAL_FIRST_ORDER_COMPONENT',
  'qualification':'Restricted family instance of the global §2 exact first-order formula, with source-implicit genuine differentiability explicit as a conclusion.',
  'blocking_semantic_delta_found_for_selected_local_component':False,
  'blind_reconstruction_statement_mismatch_found':False,
  'full_source_result_equivalence':False,
  'final_acceptance':False,'source_admission':False,'fresh_lean_verified':False,
  'scope':'Provisional only; relies on the supplied anonymous statement and approved standard definition meanings, not unseen current module/proof/author intent.'
 }
})

all_ids=([f'P2-{i:02d}' for i in range(1,10)]+[f'H4-{i:02d}' for i in range(0,17)]
         +[f'C4-{i:02d}' for i in range(1,8)]+[f'T4-{i:02d}' for i in range(1,11)]
         +[f'L4-{i:02d}' for i in range(1,6)]+['CTX-01','CTX-02'])
assert len(all_ids)==50 and len(set(all_ids))==50
chosen={c['source_claim_id']:c for c in counterparts}
accounting=[]
for cid in all_ids:
    if cid in chosen:
        disposition=chosen[cid]['role']
        reason=chosen[cid]['limits']
    elif cid=='P2-03':
        disposition='global-source-class-context-not-a-candidate-conclusion'
        reason='Precision-class domain helps interpret P2-04 but the candidate only defines one constructor family and asserts no Loewner or class-membership conclusion.'
    elif cid in ['H4-03','C4-05','C4-06','C4-07']:
        disposition='outside-selected-local-conclusion-normalizer-or-public-spectrum'
        reason='No Z, determinant identity, normalizing integral, target law or public-spectrum complexity assertion is in the anonymous conclusion.'
    elif cid=='H4-04':
        disposition='outside-selected-local-conclusion-affine-pairing'
        reason='There is only one constructed matrix and no κ=2 matched matrix, affine comparison or bidirectional query simulation.'
    elif cid in ['C4-03','C4-04']:
        disposition='outside-selected-local-conclusion-additional-calculus-or-minimizer'
        reason='No explicit strong-convexity/smoothness bound, minimizer or quadratic growth conclusion; do not infer source credit from a shared construction.'
    elif cid in ['P2-06','P2-07','P2-08','P2-09','H4-00','H4-01','CTX-01','CTX-02'] or cid.startswith('T4-'):
        disposition='outside-selected-local-conclusion-algorithm-or-full-result'
        reason='No algorithm, input/output law, TV, deterministic cap, expected cost, uniform lower bound, general-potential transfer or its probability/asymptotic argument is asserted.'
    elif cid.startswith('L4-'):
        disposition='outside-selected-local-conclusion-method-limitation-or-open-boundary'
        reason='No Krylov dimension or test limitation statement; full source analysis remains separate and its open boundaries unchanged.'
    else:
        disposition='outside-selected-local-conclusion-krylov-target-moments-or-roadmap'
        reason='No output representation, Gaussian starts, uniform Krylov bound, target moments, Chebyshev test or probabilistic transport is asserted.'
    accounting.append({'source_claim_id':cid,'disposition':disposition,'reason':reason})
dump('source_scope_accounting.json',{
 'phase1_manifest_sha256':PHASE1,
 'inventory_basis':'All 50 IDs were carried forward from this reviewer’s already-read frozen Phase 1 inventory; no new source or repository file was opened for Phase 2.',
 'claim_count':50,'clauses':accounting,
 'omission_meaning':'Outside selected local conclusion means absent as an asserted theorem conclusion relative to the broader source. It is not a blocking omission for the identified local first-order component, a statement of logical non-derivability from explicit definitions, or a judgment that the larger source claim is false.'
})

dump('phase2_ambient_exposure_record.json',{
 'reviewer':'src_4e8f6a','ambient_exposure_nonzero':True,
 'phase1_freeze_sha256':PHASE1,
 'phase1_exposure_carried_forward':'The frozen nonzero ambient exposure record remains applicable; Phase 1 is unchanged.',
 'only_new_external_file_opened':str(INPUT),
 'actual_input_raw_sha256':H(raw),
 'newly_visible_material':[
  'Anonymous Lean proposition, statement hash, five approved standard definition-context strings and compiled metadata.',
  'Actual independent reconstructed text, its text/run/manifest hashes, decoder role identity and detailed honest ambient-exposure report.',
  'Packet identifier, hash fields, original neutral input/run paths and the source-reviewer Phase 1 binding hash.',
  'Root instruction that this is selective comparison before whole-module/reader context, with no desired verdict supplied.'
 ],
 'source_visibility':'Source text was read by this reviewer in Phase 1, as required for a source reviewer. This reviewer is not a blind decoder.',
 'decoder_visibility_scope':'The independent decoder reports source_text_visible=false while expressly recording nonzero ambient cues. That distinction is preserved; no global zero-exposure or global cue-free claim is made.',
 'named_original_decoder_files_opened':False,
 'candidate_declaration_or_module_identity_supplied':False,
 'current_target_inferred_from_ambient_labels':False,
 'mathematical_basis':'Frozen 50 source clauses plus the permitted anonymous proposition, standard definitions and reconstruction. No root acceptance state, current target identity or author prose was used.',
 'not_performed':[
  'No current module/Test/authored lesson/publication/control-plane item or old sourcegraph/sourceaudit/repair file opened.',
  'No implementation proof, Lean API, declaration identity search or fresh Lean run.',
  'No sourceV/source admission/final acceptance, shared ledger/frontier/README/site/remote/model write.',
  'No edit to Phase 1, no .atlas-upstream access, no new Goal/background process or spawned subagent.'
 ],
 'output_scope':str(OUT),
 'next_phase_boundary':'Await separately authorized whole-module/reader/fresh-Lean inputs only after this second freeze.'
})

(OUT/'provisional_comparison.md').write_text(r"""# Phase 2 selective comparison — provisional

The anonymous proposition matches a **local first-order oracle/calculus
component** of the frozen source, subject to the supplied standard definition
context. Its primary counterpart is P2-04 (§2 Eq. (1)) instantiated by H4-02
(§4.1 Eq. (11)). Genuine differentiability is made explicit, consistently with
the source gradient notation and C4-02 calculus context. No blocking semantic
delta was found for that selected local component. This is not final
acceptance, source admission, proof validation or equivalence to an entire
source result.

The actual independent reconstruction retains the proposition's quantifiers,
local lets, coordinates, both determinant signs, two conclusions, and genuine
derivative versus total-gradient distinction. No statement/reconstruction
mismatch was found under the approved meanings. The decoder's
source_text_visible=false report is preserved together with its nonzero ambient
exposure; its original private run files were not opened.

## The selected source instance

For a zero-based coordinate i in Fin d, set j=i.val+1. Then the source angle
(j−1/2)π/d is exactly the anonymous angle (i.val+1/2)π/d. The diagonal
eigenvalues and OΛOᵀ construction match. The bounds d≥2, κ≥2 and universal
full real orthogonal O are the source local-family setting.

With coordinate-preserving WithLp maps, f(x)=xᵀAx/2 and query(x)=Ax.
The second conjunct is precisely the local value-and-gradient pair
(f(x),∇f(x))=(⟨x,Ax⟩/2,Ax). HasGradientAt in the first conjunct means actual
Frechet differentiability with derivative h↦⟨Ax,h⟩. It is a conclusion, not a
new hypothesis. It prevents a total gradient's zero fallback at a nonexistent
derivative from substituting for the intended mathematical gradient.

The source §2 formula is broader: every admissible symmetric precision A,
d≥1 and κ≥1. The candidate fixes A by the family constructor. Its comparison
is therefore an instantiated component, not an equivalent universal
restatement of the global formula. The local bounds need not be logically
minimal for differentiating a quadratic to remain faithful family restrictions.

## Seven-slot result

| Slot | Provisional comparison |
|---|---|
| Objects | Same θ/eigenvalue/precision constructor, quadratic and Ax reply after indexing and coordinate identification. No target law or normalizer is introduced. |
| Quantifiers | Same local d≥2, κ≥2, every full-O matrix and every x. Narrower than the global arbitrary-A formula; no random or algorithmic quantifiers are invented. |
| Domain | Fin d with Euclidean coordinates is the source real R^d after an explicit index shift. Both determinant signs remain allowed. |
| Assumptions | Local family bounds and orthogonal membership match. Symmetry/differentiability are not smuggled as new binders. Symmetry is a construction-derived proof ingredient. |
| Conclusion | Same local value/gradient identity; source-implicit genuine derivative existence is explicit. C∞, Hessian, Loewner bounds, convexity/smoothness, minimizer and normalizer are not explicit conclusions. |
| Use | Supplies the algebraic response component behind exact matrix–vector versus first-order information. It states no adaptive algorithm simulation or equality of complexities. |
| Failure boundary | No δ,q,ε,TV,seed,cap,expected cost, second matrix, target covariance or asymptotic constant claim. Full-module and proof semantics remain uninspected. |

The structured seven_slot_comparison.json records all slot details and bridge
classifications. source_scope_accounting.json explicitly accounts for all 50
frozen source clauses; unselected broader clauses are not silently treated as
proved or rejected.

## Necessary bridges, without implementation assumptions

The finite-index shift and coordinate/inner-product adapters are standard
definition bridges. Symmetry of O diag(λ) Oᵀ and the genuine quadratic
derivative are mathematical proof ingredients. The connection from
HasGradientAt to the value of the totalized gradient uses the supplied standard
Riesz/fderiv meaning. These ingredients cannot become public convenience
premises in a faithful theorem.

To interpret the constructor as a member of the global source precision
class, Lemma 4.6/C4-01 supplies admissibility, with symmetry derived by algebra.
The anonymous proposition itself has no spectral-order conclusion. Direct
quadratic differentiation needs symmetry rather than the spectral bounds.

## Broader source scope is separate

The candidate does not restate printed Lemma 4.6, the full C.4 paragraph,
normalizer invariance, same-O affine comparison, the entire §2 oracle
complexity equivalence, Theorem 4.1 or its analysis limitations. Further facts
may follow from the explicit construction through separate proofs; this
comparison awards no such proof or source-completion credit.

In particular, full-O universality is present, while no matched κ=2 matrix
appears, so same-O affine comparison is absent. The query is the precision
matrix product Ax, with no inverse-covariance oracle confusion. No budget
model occurs here, so neither deterministic-cap nor expected-cost complexity
is proved.

## Provenance and next gate

The input raw SHA-256, statement text hash and reconstructed-text hash were
recomputed successfully. Canonical packet hashing excludes its self-hash
field, while the recorded whole-JSON canonical hash includes it; both match
their respective values. This distinction is correct.

The supplied compiled=true flag is metadata, not a fresh compiler check by
this reviewer. Actual current module/import/scoped-variable/definition/proof
content, authored exposition, publication bindings, reader context and fresh
Lean remain unopened. This provisional conclusion is conditional on the
anonymous statement and approved standard meanings. The phase stops at its
second freeze and awaits separately supplied later-stage inputs.
""")

dump('validation_receipt.json',{
 'checked_utc':datetime.now(timezone.utc).isoformat(),
 'checks':[
  'Permitted new input raw SHA-256 matched eff8df755f5b59f14529de5308cb722d8ef539f2bf1c24c980b089044084b6a2.',
  'Anonymous statement text and actual reconstruction text matched their recorded SHA-256 values.',
  'Anonymous packet self-field-excluding canonical SHA and self-field-including whole-JSON canonical SHA both matched.',
  'Packet hash is consistent between the anonymous packet and independent reconstruction.',
  'Input Phase 1 reference matches the reviewer’s already-frozen Phase 1 manifest hash.',
  'All seven requested slots are compared and all 50 frozen source clause IDs are accounted for.',
  'All eight source counterparts are typed as primary/partial/definition/supporting roles with explicit scope limits.'
 ],
 'source_proof_check':False,'whole_module_check':False,'fresh_lean_check':False,
 'source_admission':False,'final_acceptance':False
})

artifacts=[]
for path in sorted(OUT.rglob('*')):
    if path.is_file() and path.name not in {'freeze_manifest.json','freeze_manifest.sha256'}:
        data=path.read_bytes()
        artifacts.append({'path':path.relative_to(OUT).as_posix(),'bytes':len(data),'sha256':H(data)})
dump('freeze_manifest.json',{
 'schema':'phase2-selective-comparison-freeze-v1',
 'reviewer':'src_4e8f6a','phase':'PHASE2_SELECTIVE_ANONYMOUS_COMPARISON',
 'status':'FROZEN_PROVISIONAL_AWAITING_SEPARATE_FULL_CONTEXT',
 'frozen_utc':datetime.now(timezone.utc).isoformat(),
 'phase1_manifest_sha256':PHASE1,
 'phase2_input_raw_sha256':H(raw),
 'statement_sha256':lean['statement_sha256'],
 'independent_reconstruction_text_sha256':recon['reconstructed_text_sha256'],
 'provisional_conclusion':'Statement-level match for selected local first-order component, a restricted source-family instance. No blocking semantic delta found at this scope; no whole-source equivalence or final acceptance.',
 'scope_accounting':'source_scope_accounting.json',
 'comparison':'seven_slot_comparison.json',
 'selected_counterparts':'selected_source_counterparts.json',
 'summary':'provisional_comparison.md',
 'exposure':'phase2_ambient_exposure_record.json; nonzero exposure recorded',
 'hash_provenance':'input_hash_receipt.json',
 'source_admission':False,'final_acceptance':False,
 'whole_module_or_reader_opened':False,'fresh_lean_or_API_inspected':False,
 'phase1_modified':False,
 'next_phase_gate':'Await separately authorized whole-module/reader/fresh-Lean inputs. Do not infer the actual candidate identity or desired verdict.',
 'artifacts':artifacts
})
manifest_raw=(OUT/'freeze_manifest.json').read_bytes()
with (OUT/'freeze_manifest.sha256').open('x') as f:
    f.write(H(manifest_raw)+'  freeze_manifest.json\n')
print(json.dumps({'status':'FROZEN_PROVISIONAL_AWAITING_SEPARATE_FULL_CONTEXT',
 'freeze_manifest_sha256':H(manifest_raw),'artifact_count':len(artifacts),
 'source_clauses_accounted':len(accounting),'slots':len(slots),
 'statement_level_local_match':True,'final_acceptance':False,'source_admission':False},indent=2))
