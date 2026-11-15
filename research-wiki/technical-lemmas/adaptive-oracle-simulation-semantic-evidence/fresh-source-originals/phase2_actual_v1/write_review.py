"""Write this reviewer's independently authored, acyclic phase-2 receipts."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

OUT = Path('.astis/semantic-neutral-20261116/adaptive_oracle_fresh_source_r18/phase2_actual_v1')
PACKETS = Path('.astis/huanjian-gc-adaptive-oracle-simulation-20261116/fresh-source-packets.actual-v1')
sha = lambda b: hashlib.sha256(b).hexdigest()
canonical = lambda d: json.dumps(d, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()


def write(name, data):
    p = OUT / name
    assert not p.exists(), 'Do not overwrite a frozen review artifact: ' + str(p)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    return sha(p.read_bytes())


initial = json.loads((OUT / 'input-register.initial.json').read_text())
extra = json.loads((OUT / 'additional-definition-inputs.before-read.json').read_text())
packets = {k: json.loads((PACKETS / (k + '.canonical-fresh-reviewer-packet.json')).read_text()) for k in ['P', 'T']}
reviewer = 'Independent anti-anchored source reviewer; agent=/root/adaptive_oracle_fresh_source_r18; run_id=adaptive_oracle_fresh_source_r18-phase2-actual-v1; no unobserved model-version claim'

run = {
    'schema_version': 1,
    'run_id': 'adaptive_oracle_fresh_source_r18-phase2-actual-v1',
    'reviewer': reviewer,
    'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
    'phase1_receipt_sha256': initial['phase1_receipt_sha256'],
    'source_sha256': initial['source_sha256'],
    'input_register_sha256': sha((OUT / 'input-register.initial.json').read_bytes()),
    'additional_input_register_sha256': sha((OUT / 'additional-definition-inputs.before-read.json').read_bytes()),
    'span_verification_sha256': sha((OUT / 'span-verification.json').read_bytes()),
    'packet_bindings': initial['inputs'],
    'independent_from_formalizer': True,
    'independent_from_decoder': True,
    'prior_verdicts_or_repairs_seen': False,
    'source_graph_or_topology_review_seen': False,
    'native_review_evidence_seen': False,
    'methods': [
        'Preserved the source-first receipt unchanged before reading either reconstruction or target.',
        'Verified the file digests and recomputed both canonical packet hashes after removing packet_sha256, using sorted UTF8 JSON with compact separators and no trailing newline.',
        'Read each canonical statement and its source-blind reconstruction, the declared source contract, all candidate assumptions, the complete shared publication context and every lesson field.',
        'Read all 170 embedded P lines and all 118 embedded T lines; inspected typing/scoped context, private helpers, proof bodies, literal matrix and gradient meanings, and all result conjuncts.',
        'Independently matched every lesson step to its source anchor and Lean span; mechanically verified inclusive line, half-open character and raw UTF8 byte ranges and SHA256 values.',
        'Registered exact run and actual_first_order_query definition file hashes before reading run lines 1-34 and the 92-line producer module. No older audit, native evidence or graph file was consulted.',
        'Checked the seven slots against the declared author-derived finite-fuel contract, while separately preserving the stronger printed source-class complexity boundary.',
        'No proof search, recompilation, Git inspection, API access, browser use, canonical metadata update, or candidate modification was performed.'
    ],
    'compilation_evidence_boundary': 'Both packets carry compiled=true. This run inspected the mathematics and exact text; it neither reran Lean nor treated that flag as evidence of source fidelity.',
    'acyclicity': 'This run record contains input hashes only. Verdict files may hash this record; no verdict, capsule or manifest hash occurs here.'
}
run_sha = write('review-run.json', run)

correspondence = {
    'schema_version': 1,
    'review_run_sha256': run_sha,
    'status': 'accepted-with-explicit-author-derived-boundary',
    'principle': 'Printed source facts, author-derived finite-program consequences and unproved source-class claims are different claims.',
    'rows': [
        {'source': ['S2.E1', 'S2.SS0.SSS0.Px1.p2.1'], 'meaning': 'For the actual ordinary quadratic, FO_A(x)=(x^T A x/2,Ax). One matvec reply plus the known query recovers FO; gradient projection recovers matvec.', 'lean': ['T:42-58', 'T:92-112'], 'disposition': 'literal-specialization-and-internal-discharge', 'evidence': 'The full rotated A appears in f and mv. fo uses gradient f, and hactual is produced internally by actual_first_order_query. P is applied once with the continuous scalar/vector decoder and once with gradient projection.'},
        {'source': ['S2.SS0.SSS0.Px2.p1.1'], 'meaning': 'Borel query, stopping and output decisions use input-independent private randomness and past replies.', 'lean': ['P:94-109', 'T:24-41'], 'disposition': 'author-derived-measurable-state-program-interface', 'evidence': 'next, update and initial have explicit measurability premises. P permits arbitrary measurable carriers. T fixes the literal Borel Euclidean carrier; its common seed law and program data precede every O. No direct O parameter occurs in next/update/initial. Universal representation of every source algorithm is not asserted or supplied.'},
        {'source': ['S2.SS0.SSS0.Px2.p1.1', 'S2.SS0.SSS0.Px4.p1.2'], 'meaning': 'The source query cap is deterministic for every input and seed; it is not an expectation-budget definition.', 'lean': ['run:18-27', 'P:22-51', 'P:115-121', 'P:153-167', 'T:59-70'], 'disposition': 'author-derived-explicit-fuel-and-bounded-cost-consequence', 'evidence': 'A funded request charges one interaction, a halt charges none, and an unfunded request is tagged none. The count cap is pointwise; integrability and the ordinary real expectation bound are proved afterwards.'},
        {'source': ['S2.SS0.SSS0.Px4.p1.1', 'A2.SS1.SSS0.Px4.p4.1', 'A2.SS1.SSS0.Px4.p4.2'], 'meaning': 'Averaging the whole private seed and taking a measurable readout yields an output law; B.1 uses a common seed law in its separate sign experiment.', 'lean': ['P:135-152'], 'disposition': 'context-plus-author-derived-pushforward-result', 'evidence': 'The exact pointwise run equality implies equality of pushforwards under the same mu. These pushforwards concern final state, Option output and actual count. They are not a sign-posterior theorem, a law containing the seed as an explicit coordinate, or a Haar-joint law.'},
        {'source': ['A2.SS1.SSS0.Px3.p6.1', 'A3.SS1.SSS0.Px1.p7.1'], 'meaning': 'B.1 uses absorbing histories; C.1 uses dummy zero queries for a finite proof horizon.', 'lean': ['run:18-27', 'P:22-89'], 'disposition': 'finite-history-context-only', 'evidence': 'The reused interpreter stops immediately and records actual count rather than padding it to fuel. Its tagged exhaustion convention is an explicit author-derived model, not a claim that the paper defines Option-valued samples. No B.1 sign or C.1 Krylov/latent-revelation conclusion is claimed.'},
        {'source': ['S4.E11', 'S4.SS1.p1.2', 'S4.SS1.p2.1'], 'meaning': 'd>=2, kappa>=2, deterministic midpoint-cosine spectrum, full orthogonal conjugation and a possibly public spectrum.', 'lean': ['T:22-51', 'T:80-87'], 'disposition': 'literal-family-pointwise-in-every-O', 'evidence': 'Fin d has values 0,...,d-1, so (i.val+1/2)pi/d equals the paper\'s (i-1/2)pi/d after reindexing 1,...,d. Matrix multiplication is full O*diagonal(lambda)*O.transpose. All full real orthogonal O are quantified. No Haar distribution is asserted.'},
        {'source': ['A3.SS4.p2.1'], 'meaning': 'The potential is the ordinary smooth quadratic with Hessian A.', 'lean': ['T:47-51', 'T:92-101', 'actual_first_order_query:30-44', 'actual_first_order_query:66-90'], 'disposition': 'calculus-context-and-existing-genuine-gradient-producer', 'evidence': 'The producer proves HasGradientAt before identifying gradient, with the literal full matrix quadratic. T adds no genuine-gradient hypothesis. C.4 is not misattributed as the source of the FO/matvec equivalence.'},
        {'source': ['S2.E2', 'S2.SS0.SSS0.Px4.p1.2'], 'meaning': 'Class-uniform successful E-valued sampling and the Q_G query-complexity equivalence.', 'lean': [], 'disposition': 'outside-declared-bridge-and-not-established', 'evidence': 'Neither P nor T provides universal source-policy representation, a proof of some-output at sufficient fuel for all source algorithms, a Gaussian target/TV assertion, or a class-uniform Q_G theorem. This boundary is stated in the source contract, module comments, candidate assumption comparison, and lesson.'}
    ],
    'phase1_hazards': [
        {'id': 'H1', 'result': 'resolved-in-scope', 'evidence': 'T:43-50 uses the full A action and full dot product, including off-diagonal terms.'},
        {'id': 'H2', 'result': 'resolved-in-scope', 'evidence': 'T:41 quantifies every full orthogonal O; no determinant-component or coordinate restriction.'},
        {'id': 'H3', 'result': 'bounded-resolution', 'evidence': 'The same mu and program data are fixed before O in T and used for each compared pair. No random-O joint law or source-class encoding is inferred.'},
        {'id': 'H4', 'result': 'bounded-resolution', 'evidence': 'Programs use next S and update S Q reply; no O argument is exposed to them. Their arbitrary-state representation is explicit and is not claimed to encode all source algorithms.'},
        {'id': 'H5', 'result': 'resolved-in-scope', 'evidence': 'The all-seed count cap precedes its expectation consequence in P:146-167 and T:60,66.'},
        {'id': 'H6', 'result': 'resolved-in-scope', 'evidence': 'run checks halt first and stops; there are no information-bearing queries after a halt.'},
        {'id': 'H7', 'result': 'resolved-in-scope', 'evidence': 'Omega and its sigma algebra are arbitrary; there is no uniform-seed or StandardBorel restriction.'},
        {'id': 'H8', 'result': 'resolved-in-scope', 'evidence': 'T\'s f/mv are literal. The gradient is justified internally. Option none is openly an interpreter exhaustion tag, not an invented value of the source oracle or a successful Euclidean sample.'},
        {'id': 'H9', 'result': 'outside-target-with-correct-boundary', 'evidence': 'No C.1 latent history or auxiliary Gaussian vector is supplied to the program or assumed as a new premise.'},
        {'id': 'H10', 'result': 'resolved-in-scope', 'evidence': 'No B.1 2T<n or C.1 2q+1<d threshold is imposed on P or T; their cited roles are contextual only.'},
        {'id': 'H11', 'result': 'bounded-resolution', 'evidence': 'Only the common-mu execution pushforwards and real count integrals are asserted; no TV supremum or Haar-average interchange is performed.'},
        {'id': 'H12', 'result': 'resolved-in-scope', 'evidence': 'The concrete f and mv depend on A; the theorem is pointwise for each chosen orthogonal representation and asserts no canonical latent quotient.'}
    ],
    'blocking_deltas': [],
    'repairs_proposed': []
}
correspondence_sha = write('source-to-lean-correspondence.json', correspondence)

whole = {
    'schema_version': 1,
    'review_run_sha256': run_sha,
    'whole_module_status': 'accepted-for-the-exact-embedded-P170-and-T118',
    'whole_lesson_status': 'accepted-for-semantics-attribution-and-complete-exact-span-coverage',
    'production_module': {
        'sha256': initial['inputs']['P']['production_module_embedded_sha256'],
        'lines': 170,
        'coverage': [
            {'lines': [1, 21], 'role': 'Imports, author-derived scope comments, open declarations, autoImplicit=false, universe and namespace context.', 'result': 'No hidden mathematical binder or altered oracle definition.'},
            {'lines': [22, 51], 'role': 'Private run_simulation_and_cap.', 'result': 'Direct fuel induction preserves the full state/Option/count tuple and pointwise cap. Uses only exact reply commutation; no theorem-shaped public assumption is smuggled in.'},
            {'lines': [52, 89], 'role': 'Private measurable_run and separation whitespace.', 'result': 'Arbitrary measurable spaces are retained; measurable some is an internal helper premise supplied by the public construction. Halt/request cases use product-sum measurability; recursive counts increment measurably.'},
            {'lines': [90, 121], 'role': 'Public docstring and exact signature.', 'result': 'All carrier/sigma, probability law, next/update/oracle/decode/initial, exact commutation and all-fuel conditions agree with the blind reconstruction. Target measurability is not a separate premise.'},
            {'lines': [122, 152], 'role': 'Local Option sigma instance, measurable some, decoded update, seeded runs, equality and mapped law.', 'result': 'The Option instance is exactly the Unit+X pullback. Target run measurability follows from pointwise equality. The probability claim concerns the mapped execution record; no seed or random input is an added coordinate.'},
            {'lines': [153, 170], 'role': 'Count measurability, bounded integrability, ordinary expected-cost equality and cap; end context.', 'result': 'Natural counts are coerced to real numbers. Integrability is proved from the probability-space constant fuel bound. Both target-count integrability and target-law probability also follow from the established pointwise/law equalities; their explicit base-side presentation hides no premise.'}
        ],
        'private_helpers': ['run_simulation_and_cap', 'measurable_run'],
        'module_level_private_instances': [],
        'placeholder_or_fake_closure_found': False,
        'unreviewed_changed_region': []
    },
    'private_application_module': {
        'sha256': initial['inputs']['P']['private_application_embedded_sha256'],
        'lines': 118,
        'coverage': [
            {'lines': [1, 20], 'role': 'Imports, namespace/universes, explicit exclusions and local elaborator option.', 'result': 'The elaborator option changes proof search transparency, not theorem semantics. No global source hypotheses are introduced.'},
            {'lines': [21, 70], 'role': 'One private theorem signature.', 'result': 'Both explicit Borel instances, input ordering, all fuel values, full orthogonal family, genuine fo and both separate program-specific comparisons are visible.'},
            {'lines': [71, 94], 'role': 'Proof setup and actual oracle identity.', 'result': 'Local Euclidean Borel and Option instances match the signature. mv is a continuous linear map. actual_first_order_query supplies the true gradient identity internally with the same d,kappa,O,x.'},
            {'lines': [95, 112], 'role': 'Decoder/oracle measurability and two calls to P.', 'result': 'Forward simulation reconstructs the scalar and gradient for updateFO. Reverse simulation projects the gradient for updateMV. The proof never identifies arbitrary unrelated update policies.'},
            {'lines': [113, 118], 'role': 'Conjunction assembly and namespace close.', 'result': 'All sixteen result components are retained. No unreviewed declaration or private helper remains.'}
        ],
        'private_theorems': ['actual_fixed_spectrum_first_order_matvec_joint_laws_and_costs'],
        'extra_private_helpers': [],
        'local_instances_reviewed': ['T:24-27', 'T:73-76'],
        'placeholder_or_fake_closure_found': False,
        'unreviewed_changed_region': []
    },
    'lesson_steps': [
        {'step': 1, 'lean_lines': 'P:1-52', 'text_matches_proof': True, 'source_attribution_correct': True, 'explanation': 'Exact commutation identifies the next state; fuel induction preserves the complete returned record and actual count. Eq. (1) motivates reply conversion, while this induction is explicitly author-derived. The absorbing-history link is context only.'},
        {'step': 2, 'lean_lines': 'P:53-134', 'text_matches_proof': True, 'source_attribution_correct': True, 'explanation': 'The displayed pullback sigma algebra and internal measurable-run induction are exact. No StandardBorel assumption is introduced. The source Borel-policy and C.1 finite-horizon anchors are contextual, not printed generic measurability theorems.'},
        {'step': 3, 'lean_lines': 'P:135-152', 'text_matches_proof': True, 'source_attribution_correct': True, 'explanation': 'The common initial map is composed with the run; pointwise equality yields both execution pushforwards and probability. The text expressly distinguishes the tagged execution record from a successful Euclidean sampling law.'},
        {'step': 4, 'lean_lines': 'P:153-170', 'text_matches_proof': True, 'source_attribution_correct': True, 'explanation': 'Measurability plus the pointwise natural-count bound gives real Bochner integrability, then expectation equality and its upper bound. The deterministic source cap remains prior to, and stronger than, this consequence.'},
        {'step': 5, 'lean_lines': 'T:1-118', 'text_matches_proof': True, 'source_attribution_correct': True, 'explanation': 'The whole private module applies P twice on the literal full rotated family. The genuine first-order producer and continuous decoders are actual proof inputs. Eq. (1) supplies the conversion meaning, Eq. (11) the family, and C.4 only ordinary quadratic calculus context.'}
    ],
    'span_verification': 'All five line/character/UTF8-byte spans and hashes were checked. Steps 1-4 concatenate to the exact whole P module; step 5 is the exact whole T module.',
    'reader_conditions_preserved': [
        'The complete P signature is reproduced exactly in lesson.lean_statement; all generic sigma/program conditions appear in the adjacent assumptions.',
        'The lesson separately states T\'s dimensions, spectral grid reindexing, Borel carrier, common-mu/program quantifier order and two distinct policies.',
        'some, none, zero fuel, actual count and ordinary expectation retain their meanings in the statement, assumptions, formulas, five proof steps and exact code.',
        'The generalization and residual source-class/sampling/TV/Q_G boundaries remain visible in the packet statement, comparison assumptions, comments and proof prose.',
        'The exact private application and two P helper proofs have full line coverage; private material receives no extra public proof credit.'
    ],
    'dependency_review_boundary': {
        'visible_calls': ['QuadraticRegularizationOracle.run', 'measurable_simulation_joint_law_and_cost (twice in T)', 'FixedSpectrumFirstOrder.actual_first_order_query'],
        'metadata_observation': 'lesson.astis_dependencies names the public P dependency run. T\'s calls are additionally visible in the exact step-5 code and dependency_notes. This receipt checks that source/proof correspondence; a separately elaborated value/kernel dependency certificate remains pending exactly as the candidate says.',
        'not_inferred': ['Compiler value dependency extraction', 'Kernel axiom closure', 'Browser folding/layout/rendering', 'Current working-tree or Git freshness beyond the exact packet text']
    },
    'blocking_findings': [],
    'repairs_proposed': []
}
whole_sha = write('whole-module-and-lesson-review.json', whole)


def slot(original, reconstructed, relation, evidence):
    return dict(original=original, reconstructed=reconstructed, relation=relation, evidence=evidence)


p_slots = {
    'objects': slot('The declared author-derived bridge uses seeded state programs, exact reply conversion and the complete finite execution record; the printed source supplies exact quadratic replies and Borel adaptive algorithms.', 'Arbitrary measurable S,Q,A,B,X,Omega; next, update, oracle, target, decode, initial; a returned (final state, Option X, natural count).', 'explicit-elaboration', 'P:94-114 and run:18-27 agree with the anonymous reconstruction. The generic state interpreter is explicitly author-derived, not attributed as a printed source definition.'),
    'domains': slot('The bridge abstracts the source Euclidean setting to arbitrary measurable carriers, with an explicit tagged partial-execution result; the concrete application restores the literal Borel Euclidean family.', 'Each carrier has its given sigma algebra. Option X has exactly the pullback sigma algebra under none->inl(), some x->inr x. No StandardBorel assumption is imposed.', 'explicit-elaboration', 'P:94-109,123-134; lesson assumptions 1-4. The arbitrary measurable generalization is deliberate and does not substitute Option X for the paper\'s successful R^d output law.'),
    'quantifiers': slot('A common probability seed law and fixed measurable program data with exact decoder commutation are followed by every finite fuel and every seed realization.', 'For every probability mu and all displayed program data satisfying the displayed conditions, for every natural fuel, both run maps are measurable, equal for every omega and pointwise count bounded.', 'same', 'P:100-121. Every-seed equality is literal, not merely almost sure; fuel includes zero. No source-class representation quantifier has been silently claimed.'),
    'assumptions': slot('Measurable next/update/oracle/decoder/initial, a probability seed law and pointwise exact reply conversion are the declared abstract bridge assumptions.', 'Exactly these hypotheses appear; target measurability, full-run measurability and count integrability are not premises.', 'same', 'P:104-109; internal hcorrected, hb, ht and hint at P:139-161 discharge the required proof ingredients. No EXCESS source-facing condition is added to the declared bridge.'),
    'conclusion': slot('Finite-fuel exact simulation preserves the entire seeded terminal/Option/count record, both execution laws and ordinary expected actual count bounded by fuel.', 'The exact seven combined assertions give two measurable maps; all-seed record equality and count cap; equality of pushforwards; probability; real count integrability; equal real integrals; expected count <= fuel.', 'equivalent', 'P:115-121,146-168. Target count integrability and target-law probability follow from the proven equalities, though explicitly written for the base side. This is the author-derived contract rather than the stronger source-class Q_G assertion.'),
    'scopes': slot('The source uses a deterministic cap; the derived bridge uses partial tagged executions, common-seed pushforwards and an ordinary expected-cost consequence, without success, Haar or TV claims.', 'run inspects halt even at zero fuel, charges one only on a funded request, returns none on an unfunded request and preserves early-halt actual count. The mapped random variable is (S x Option X) x Nat under mu.', 'same', 'run:18-27; P:6-14,111-121; lesson steps 1,3,4. The full joint execution law does not contain Omega as an explicit output coordinate and is not a Haar-joint input law.'),
    'constant_dependencies': slot('Fuel is an arbitrary nonnegative integer and bounds the actual count at every seed before bounding its ordinary expectation; the same mu is used for both executions.', 'For each fuel, count <= fuel and both real integrals are under that one mu; no d,kappa,epsilon or source lower-bound constants occur in P.', 'same', 'P:110-121,153-167. Probability makes the constant bound integrable; there is no expected-budget replacement, positive-fuel restriction or hidden constant.')
}
t_slots = {
    'objects': slot('The actual application uses the Section 4 midpoint-cosine precision A=O Lambda O^T, its ordinary quadratic and genuine first-order oracle, and separately simulates each of two given programs.', 'f is the full coordinate quadratic; mv is full A*x on EuclideanSpace; fo=(f,gradient f); foViaMV is compared to foRun under updateFO, and mvViaFO to mvRun under updateMV.', 'same', 'T:42-58,92-112. The actual producer is read at its registered hash and establishes HasGradientAt before the gradient identity. No diagonal-only surrogate or relation between unrelated policies is used.'),
    'domains': slot('d>=2,kappa>=2; the literal Euclidean Borel carrier and every full real orthogonal O; the Section 4 deterministic midpoint spectrum, with Option only for explicit partial execution.', 'These exact ranges, Borel and Option pullback instances, and full Matrix.orthogonalGroup occur. Fin d index i.val=0,...,d-1 gives theta=(i.val+1/2)pi/d.', 'equivalent', 'T:22-27,41-50. Reindexing source i=1,...,d gives the identical grid; full matrix multiplication preserves all rotated cross terms. No determinant-component, query-span or C.1 dimensional threshold is introduced.'),
    'quantifiers': slot('The declared application fixes the common seed law and measurable program data before every fuel and every full orthogonal O, and preserves each pair for every seed.', 'd and kappa and their bounds; arbitrary S,Omega and sigma algebras; mu and next/updateFO/updateMV/initial; measurability; then all fuel,O; then all omega in each equality.', 'same', 'T:22-41,60,66 and the anonymous reconstruction. No conditional O-dependent seed distribution or hidden random-O law is asserted. Class representation is still outside the target.'),
    'assumptions': slot('Only the concrete dimension/range, carrier, probability and program measurability conditions are application premises. Genuine oracle correctness and measurability must be produced inside the proof.', 'Exactly these premises occur. mv continuity, the actual true-gradient identity, decoder continuity, fo measurability and the two exact commutations are internal proof facts.', 'same', 'T:35-40,88-112. hactual is not a public hgradient premise; count integrability and whole-run measurability are also supplied by P. The condition 2q+1<d and a successful-output premise are absent, as this finite-fuel statement does not need or claim them.'),
    'conclusion': slot('Both actual exact conversions preserve each program-specific finite execution, tagged result, actual cost, measurable execution law and ordinary expectation bounded by fuel.', 'Both eight-part groups give measurable compared maps, all-seed complete record equality/count cap, equal pushforwards/probability, real count integrability and equal ordinary expectations <= fuel.', 'equivalent', 'T:59-70,102-116. The forward and reverse uses are exact instantiations of P; updateFO is never equated to updateMV. These are derived application claims, not a printed full-class sampling theorem.'),
    'scopes': slot('Pointwise in every actual orthogonal precision; finite-fuel partial execution under common mu; the printed reply conversions are used, while Haar-joint law, target sampling/TV and class-uniform complexity remain excluded.', 'The statements are exactly under fixed O and common mu and use the reused interpreter with some/none outcomes and actual natural count. fo really uses gradient f.', 'same', 'T:10-17,41-70 and all six lesson assumptions/step 5. The full-Haar family as a set is retained, but no Haar measure or joint measurability in O is present or needed for the declared pointwise result.'),
    'constant_dependencies': slot('The concrete spectrum depends on d and kappa; every natural fuel bounds its own actual count, with both count integrals under the same seed law.', 'theta,lambda,A are the literal d,kappa,O formulas. Each direction has its own identical paired count and <=fuel bound, for every fuel including zero.', 'same', 'T:41-70. There is no epsilon, target covariance/normalizer, hidden n,k,T threshold, extra lower-bound constant or expected-query-budget substitution.')
}

result_shas = {}
for label, slots in [('P', p_slots), ('T', t_slots)]:
    packet = packets[label]
    result = {
        'semantic_slots': slots,
        'deltas': [],
        'verdict': 'equivalent-after-elaboration',
        'repairs': [],
        'reviewer': reviewer,
        'independent_from_formalizer': True,
        'independent_from_decoder': True,
        'review_evidence': 'Independent source-first receipt retained unchanged; exact fresh canonical packet and anonymous reconstruction; all embedded P170/T118 lines; registered run and genuine-gradient meaning context; five exact adjacent spans and proof/source correspondences checked. Verdict is only for the declared author-derived finite-fuel contract and its private actual application, not for full source-class representation or Q_G equivalence.',
        'review_run_sha256': run_sha,
        'reviewer_packet_sha256': packet['packet_sha256'],
        'reviewer_packet_file_sha256': initial['inputs'][label]['file_sha256'],
        'publication_binding_sha256': packet['publication_binding_sha256'],
        'lean_declaration': packet['lean']['declaration'],
        'lean_statement_sha256': packet['lean']['statement_sha256'],
        'reconstruction_sha256': packet['blind_reconstruction']['text_sha256'],
        'source_text_sha256': packet['source']['text_sha256'],
        'raw_source_sha256': initial['source_sha256'],
        'phase1_source_receipt_sha256': initial['phase1_receipt_sha256'],
        'canonical_contract_result': 'accepted-within-explicit-author-derived-scope',
        'source_statement_status': 'The packet source text is an umbrella attributed restatement that expressly distinguishes printed source facts from the derived bridge. P is the generic bridge; T is its associated private actual-oracle consumer. Neither is certified here as a formalization of the paper\'s entire algorithm class or Q_G equivalence.',
        'whole_module_review_sha256': whole_sha,
        'source_to_lean_correspondence_sha256': correspondence_sha,
        'blocking_delta_count': 0,
        'required_unproved_boundaries': ['Universal source Borel-algorithm representation in this interpreter', 'Successful Euclidean output at the source cap and extraction of rho_A^Alg', 'A joint random-O/Haar execution law', 'Gaussian target/TV accuracy and class-uniform Q_G equivalence', 'Main lower bounds and approximate-oracle claims'],
        'scope_note': 'The review is of exact packet-bound mathematics and reader text. Native-browser layout, aggregate Lean gates, kernel/value dependency certification, Git freshness and canonical admission remain separate.'
    }
    result_shas[label] = write(label + '.canonical-contract-review.json', result)

capsule = {
    'schema_version': 1,
    'run_id': run['run_id'],
    'reviewer': reviewer,
    'phase1_source_receipt_sha256': initial['phase1_receipt_sha256'],
    'review_run_sha256': run_sha,
    'publication_binding_sha256': packets['P']['publication_binding_sha256'],
    'results': {
        label: {'canonical_contract_result': 'accepted-within-explicit-author-derived-scope', 'verdict': 'equivalent-after-elaboration', 'blocking_deltas': 0, 'reviewer_packet_sha256': packets[label]['packet_sha256'], 'result_sha256': result_shas[label]}
        for label in ['P', 'T']
    },
    'whole_module_and_reader_result': 'All embedded P170 and T118 lines reviewed. Private helper coverage is complete. Five lesson spans and source attributions match their declared mathematical roles and exact code.',
    'whole_module_review_sha256': whole_sha,
    'source_to_lean_correspondence_sha256': correspondence_sha,
    'critical_boundary': 'Author-derived finite-fuel execution/law/cost preservation is accepted. Universal source-policy representation, successful sampling, Haar-joint law, TV/Q_G and main lower bounds are not established by P/T and were not granted.',
    'repairs_proposed': [],
    'additional_definition_inputs': extra,
    'unauthorized_material_seen': False,
    'writes_limited_to': str(OUT),
    'noncircular_hash_order': 'Input registers and span check -> review-run -> source correspondence / whole module report -> P/T results -> capsule -> manifest. No earlier file contains a later file hash.'
}
capsule_sha = write('capsule.json', capsule)
manifest = {
    'schema_version': 1,
    'run_id': run['run_id'],
    'review_run_sha256': run_sha,
    'files': {p.name: {'sha256': sha(p.read_bytes()), 'bytes': p.stat().st_size} for p in sorted(OUT.iterdir()) if p.is_file() and p.name != 'manifest.json'},
    'scope': 'Only this independent review directory; manifest intentionally omits its own hash.',
    'acyclicity': 'The capsule hashes only earlier evidence/results. This manifest hashes the capsule; the capsule does not contain a manifest hash.'
}
manifest_sha = write('manifest.json', manifest)
print(json.dumps({'review_run_sha256': run_sha, 'P_result_sha256': result_shas['P'], 'T_result_sha256': result_shas['T'], 'capsule_sha256': capsule_sha, 'manifest_sha256': manifest_sha}, indent=2))
