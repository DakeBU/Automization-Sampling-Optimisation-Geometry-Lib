from pathlib import Path
import hashlib, json, os
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]
PRIMARY = BASE.parent / 'independent-primary64'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(n): return json.loads((BASE / n).read_text(encoding='utf-8'))
def dump(n, v): (BASE / n).write_text(json.dumps(v, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
def pin(n):
    p = BASE / n
    return {'name': n, 'bytes': p.stat().st_size, 'raw_sha256': sha(p)}

headers = read('exact-header-input-pins.json')
reread = read('primary-before-header-reread-receipt.json')
support = read('bounded-diagnostic-support-inputs.json')
source_process = read('source-reread.process-receipt.json')
graph = json.loads((PRIMARY / 'source-proof-graph.json').read_text(encoding='utf-8'))
excluded_outputs = ['owned-lease.json', 'independent-header64.review.json', 'independent-header64.review.md',
    'review-digests.json', 'terminal-finalizer.json', 'terminal-readback.json',
    'finalizer.stdout.txt', 'finalizer.stderr.txt', 'finalizer.process-receipt.json',
    'readback.stdout.txt', 'readback.stderr.txt', 'readback.process-receipt.json']

payload = {
 'schema': 1,
 'role': 'independent-source-first-PREPROOF-exact-header-review64',
 'event': 'BOUNDED_STATEMENT_HEADER_REVIEW_ONLY',
 'reviewer_actual_pid': os.getpid(),
 'review_utc': datetime.now(timezone.utc).isoformat(),
 'owned_prefix': str(BASE),
 'inspected_science_commit': '4d02622332d02d0bd6c977d3cee48fd535ebf203',
 'science_commit_title': 'Prove actual PBPS unique positive macroscopic defect root',
 'scope_limits': {
    'source_review_of_science63': False, 'Lean_authored': False, 'Lean_compiled': False,
    'proof_search': False, 'Statement_Seal_granted': False, 'theorem_truth_or_science_admission': False,
    'Goal_admission': False, 'canonical_or_ledger_or_Git_or_site_mutation': False,
    'parent_existing_science_acceptance': 'Parent reported SCI63 VERIFIED/CLOSED_LAST; this review inspects its exact commit/interface only and does not reverify that result.'},
 'verdict': {
    'header0': 'ACCEPT_FOR_ROOT_PREPROOF_STATEMENT_SEAL_CONSIDERATION',
    'header1': 'ACCEPT_FOR_ROOT_PREPROOF_STATEMENT_SEAL_CONSIDERATION',
    'blocking_semantic_deltas': [], 'mathematical_repair_overlay_required': False,
    'qualification': 'Acceptance concerns these exact scoped statements and source alignment. Proof implementation, Lean gates, independent proof review and final source/reader admission remain required.'},
 'exact_header_inputs': headers,
 'primary_first_causality': {
    'source_raw_sha256': reread['primary_source_raw_sha256'],
    'source_graph_sha256': reread['graph_sha256'],
    'source_coverage_sha256': reread['coverage_sha256'],
    'primary_before_header_reread_receipt': pin('primary-before-header-reread-receipt.json'),
    'pre_header_source_seal': pin('pre-header-source-seal.json'),
    'actual_source_reread_process': source_process,
    'exact_headers_received_or_read_at_source_reread': reread['exact_header0_or_header1_received_or_read'],
    'immutable_primary64_files': reread['primary64_immutable_outputs'],
    'literal_raw_LF_regions': reread['regions'],
    'coverage_items_rechecked': reread['coverage_items_rechecked'],
    'classification': 'Independent graph and original assumptions reread/sealed before exact candidate header reads; current header inputs record later first-read timestamps.'},
 'seven_semantic_slots': {
  'header0_positive_square_order': {
   'objects': 'Two bounded real-linear operators A,B on the SAME real Lp(2,mu); (B*B-A*A) is composition difference and (B-A) is the operator difference.',
   'domains': 'Arbitrary measurable type Omega and arbitrary Measure mu. Lp equivalence classes and bounded real operators are fixed; no probability, finite measure, sigma-finiteness, finite-L2-dimensionality or Nontrivial premise.',
   'quantifiers': 'For every Omega/measurable structure/mu/A/B, positivity of A, B and B^2-A^2 entails positivity of B-A. All three hypotheses refer to the same space and operator tuple.',
   'assumptions': 'hA,hB,hSquareOrder are the generic background lemma assumptions, exactly the positive-root order adapter domain. Header1 does not expose any of them as new paper binders.',
   'conclusion': '(B-A).IsPositive is real quadratic-form/Loewner operator order, including self-adjointness. A norm lower bound alone cannot satisfy this conclusion.',
   'scopes_senses': 'IsPositive is bounded positive self-adjoint order in the real Hilbert L2 space. No pointwise order, commutativity premise or caller CFC instance/certificate is substituted.',
   'constant_dependencies': 'No scalar constant or loss appears. Canonical complex lifts and square-root monotonicity are internal proof dependencies, not public assumptions.'},
  'header1_actual_centered_root_order_inverse': {
   'objects': 'Original Gibbs mu, Gaussian augmented J, marginal nu, reflection pair Lambda, literal F, exact conditional macro space HP/P, canonical marginal pullback M/e, actual U/T/A/B, positive root Gamma and its SAME e-transport GammaP, constant q/qP and exact centered HP0, actual restriction GammaP0 and bounded Inv.',
   'domains': 'Finite-dimensional real inner-product E with its Borel measurable structure. Lp(2,J), Lp(2,nu), HP and HP0 are Hilbert quotient/subspaces. FiniteDimensional concerns E only; rank-zero E and zero centered subspace are legal, with no Nontrivial or finite-dimensional L2 binder.',
   'quantifiers': 'Original E,V,alpha,beta,eta and source hypotheses precede the conclusion. One coherent S,e,U,T,Gamma,q,GammaP0,Inv tuple is existentially chosen before universal action identities. GammaP=e.conjStarAlgEquiv Gamma and qP=e q are lexical lets; GammaP0 has pointwise equality with that same GammaP restriction.',
   'assumptions': '0<alpha<=beta, C2 V, global two-sided Hessian bounds, eta>0 and beta*eta<=1. The typeclass binders describe the Euclidean model; the two HP0 letI clauses inherit existing subtype norm/inner product and are internal typing facts. No gap/root/onto/unit/public positivity or root certificate.',
   'conclusion': 'Probability laws, actual macro/projection/reflection/conditional action coherence and B10/B11 positive-square/Gram identities; exact centered mean-kernel equivalence, GammaP qP=0, gamma>0, same positive restriction with (GammaP0-gamma I).IsPositive, IsUnit GammaP0, and one Inv with both composition cancellations and norm <=1/gamma.',
   'scopes_senses': 'B15 is operator order on exact HP0, not a lower norm bound. GammaP is still the full macro root and kills constants; inverse/unit/cancellations concern HP0 exclusively. Kernel formula is every-y literal tilted density; conditional operator/pullback formulas are AE representatives. e is fixed by equality to the measure-preserving M inclusion.',
   'constant_dependencies': 'gamma=2*sqrt(alpha*eta)/(1+alpha*eta), exactly B12/B15. hAlphaBeta and beta*eta<=1 imply alpha*eta<=1 internally; alpha*eta=1 is legal. rho=(1-alpha*eta)/(1+alpha*eta), delta=4*alpha*eta/(1+alpha*eta)^2 are derived proof constants, not extra binders. Inverse norm <=1/gamma is a quantitative derived consequence of B15, not a separate printed formula or caller assumption.'}},
 'recursive_binder_audit': {
  'header0': [
   {'binders': ['Omega', 'MeasurableSpace Omega', 'mu', 'A', 'B'], 'classification': 'STANDING_GENERIC_DOMAIN'},
   {'binders': ['hA', 'hB', 'hSquareOrder'], 'classification': 'SOURCE_BACKED_GENERIC_BACKGROUND_DOMAIN', 'paper_public_binders': False}],
  'header1': [
   {'binders': ['E', 'NormedAddCommGroup E', 'InnerProductSpace R E', 'FiniteDimensional R E', 'MeasurableSpace E', 'BorelSpace E'], 'classification': 'STANDING_EUCLIDEAN_MODEL', 'disclosure': 'Coordinate-free finite-dimensional Euclidean presentation includes rank zero.'},
   {'binders': ['V', 'alpha', 'beta', 'eta', 'hAlpha', 'hAlphaBeta', 'hV', 'hH', 'hEta', 'hBetaEta'], 'classification': 'SOURCE', 'anchors': ['S1.E1', 'S2.E6', 'S2.E7']},
   {'binders': ['mY<=product Fact', 'MeasurableSpace product', 'hp', 'HP0 inherited NormedAddCommGroup', 'HP0 inherited InnerProductSpace'], 'classification': 'TYPING_OR_RULED_INTERNAL_DEFINITION', 'new_public_math_premise': False},
   {'binders': ['S', 'e', 'U', 'T', 'Gamma', 'q', 'GammaP0', 'Inv'], 'classification': 'CONCLUSION_WITNESS', 'caller_certificate': False}],
  'EXCESS_binders': [],
  'forbidden_public_certificate_binders_absent': ['CFC', 'finite-L2', 'Nontrivial', 'hGap', 'hRoot', 'hOnto', 'hUnit']},
 'definition_audit': [
  {'definitions': ['mu', 'J', 'nu', 'Lambda', 'F'], 'judgment': 'Exact tilted Gibbs, independent Gaussian product augmentation, marginal and deterministic reflection definitions; normalization/probability is concluded from original inputs.'},
  {'definitions': ['mY', 'HP', 'P'], 'judgment': 'Exact Y-measurable lpMeas and condExpL2 inclusion; HP=range(P) and P|HP=id are concluded, not assumed.'},
  {'definitions': ['hp', 'M', 'e'], 'judgment': 'snd pushforward is measure-preserving; e agrees under inclusion with canonical pullback M for every u. This identifies marginal and actual macro space, rather than allowing an unrelated isometry.'},
  {'definitions': ['S', 'U', 'T'], 'judgment': 'Every-y S formula and Lambda.IsCondKernel give actual conditional law; U is AE pullback by literal F; T is AE conditional integral, self-adjoint, norm-contracting, mean-preserving.'},
  {'definitions': ['A', 'B'], 'judgment': 'Actual macro compression HP.orthogonalProjectionOnto U subtype; leakage ((I-P)*U*P) subtype. B maps into ker(P). Gram identity lives on HP.'},
  {'definitions': ['Gamma', 'GammaP'], 'judgment': 'Positive square equals I-T*T; D1 unique positive square root identifies B10. GammaP is the same root transported by the same e, with actual leakage Gram. No new root premise.'},
  {'definitions': ['q', 'qP', 'HP0'], 'judgment': 'q is AE 1 with inner(q,u)=integral(u); qP=e q. Exact inner-kernel membership is equivalent to marginal mean zero by e.symm. Canonical e/M identifies it with joint macro mean zero. GammaP qP=0 prevents whole-macro inverse.'},
  {'definitions': ['GammaP0', 'Inv'], 'judgment': 'For every f:HP0 its inclusion equals GammaP(f). Positivity/order, unit and both-sided bounded inverse are conclusions on this exact restriction. No fullspace inverse or onto leakage target.'}],
 'source_coverage': [
  {'anchors': ['S1.E1', 'S2.E6', 'S2.E7', 'A2.E1', 'A2.E2', 'A2.E3', 'A2.E4', 'A2.E5', 'A4.E1', 'A4.E2', 'A4.E3'], 'disposition': 'STANDING_AND_EXACT_MODEL_PRODUCER', 'boundary': 'Original assumptions, real L2/order and actual conditional projection/reflection/compression/leakage.'},
  {'anchors': ['A2.E10', 'A2.E11', 'A4.SS1.p2'], 'disposition': 'B10_B11_CONTEXT_CONCLUSIONS', 'boundary': 'Same actual positive square root and leakage Gram; uniqueness is the D1 background identification, not a new caller certificate.'},
  {'anchors': ['A2.E12'], 'disposition': 'EXACT_B12_CONSTANT', 'boundary': 'Printed gamma included; rho/delta internally derived.'},
  {'anchors': ['A3.E1', 'A3.EGx25', 'A3.E3', 'A3.E4', 'A3.SS1.p1', 'A3.SS1.p2', 'A3.SS1.p3', 'A3.SS1.p4', 'A4.E6', 'A4.E10'], 'disposition': 'REQUIRED_PROOF_INGREDIENT_DEPENDENCIES', 'boundary': 'Normalized score, conditional Hessian/PI, rough compact gradient closure, marginal PI and centered C4 sharp contraction. Not public hypotheses and not certified by this review.'},
  {'anchors': ['A2.E9', 'A3.SS1.p5', 'A3.Ex13', 'A3.SS1.p6'], 'disposition': 'INTERNAL_CENTER_AND_SQUARE_GAP_PRODUCERS', 'boundary': 'Constant kernel, exact center invariance, same-root restriction and square gap from C4.'},
  {'anchors': ['A2.E15'], 'disposition': 'EXACT_B15_OPERATOR_ORDER_TARGET', 'boundary': 'GammaP0 >= 2 sqrt(alpha eta)/(1+alpha eta) I, in positive operator order.'},
  {'anchors': ['A2.SS2.p5', 'A2.E16'], 'disposition': 'CENTERED_INVERSE_PRODUCER_FOR_B16', 'boundary': 'Bounded invertibility included; explicit inverse norm is a derived quantitative consequence. B16 polar identity itself is future work.'}],
 'remaining_source_exclusions': [
  {'anchors': ['A2.E13'], 'reason': 'No full B13 weighted H1 theorem or global Sobolev identification is concluded. The necessary compact-gradient graph ingredient must still be assembled for C4.'},
  {'anchors': ['A2.E14', 'A3.E6', 'A3.E7'], 'reason': 'No full B14 spectral interval or independent uniform -1/2 lower spectral branch is concluded; the C4 sharp norm dependency is required internally for B15.'},
  {'anchors': ['A2.E16'], 'reason': 'No B16 normalized leakage V=L GammaP0^-1, polar factorization L=V GammaP0 or V*V=I is concluded. The present exact B11 Gram plus bounded inverse are its real future parents; onto Hperp is not a source claim.'},
  {'anchors': ['A2.E17', 'A3.SS2', 'A3.SS3', 'A4.SS3'], 'reason': 'B17, half-turn affine/interpolation estimates and D4/D5 comparison are downstream branches, not B15 assumptions. Their stricter eta caps cannot be imported into this header.'},
  {'anchors': ['whole PBPS dynamics/mixing', 'SPHMC composition', 'Gaussian Cloud', 'midpoint'], 'reason': 'Paper/whole-Goal completion, dynamic semigroups, mixing/cost/error/initialization claims and other papers are outside this bounded header.'}],
 'required_internal_production_debt': [
  {'edge': 'generic positive real-L2 square order', 'requirement': 'Derive three canonical positive complex lifts Ac,Bc,Dc for A,B,D=B^2-A^2. Use their all-complex-input Re/Im action to prove Dc=Bc^2-Ac^2; positivity of separate lifts alone does not establish subtraction identity.'},
  {'edge': 'positive-root monotonicity', 'requirement': 'Use fixed CFC.sqrt_le_sqrt / CFC.monotone_sqrt on complex bounded operators, positive-root uniqueness and real restriction to derive B-A positivity. This is internal background proof, without public CFC or commutativity certificates.'},
  {'edge': 'full-marginal constant projection', 'requirement': 'HP0 is not literally an Lp space. Internally form centered projection on full marginal L2 using the actual q; derive Gamma q=0 and Gamma^2>=gamma^2 Pi0; apply header0 to gamma Pi0 and SAME Gamma, then transport/restrict by SAME e to HP0.'},
  {'edge': 'C4 production assembly', 'requirement': 'Join production RoughMeanGradient.actual_rough_mean_gradient and GaussianMarginalPoincare.actual_gaussian_marginal_centered_poincare, identifying their exact compact-gradient graphs/closures and SAME T by its reflected conditional AE action. Existing Test contraction/gap/unit consumers are retrieval evidence only; never import Tests into production.'},
  {'edge': 'internally produced unit and inverse', 'requirement': 'From exact positive lower order derive coercivity, complete closed-range/self-adjoint onto or fixed positive-operator IsUnit API; construct actual inverse, both cancellations and operator norm <=1/gamma on HP0, including zero space. No hOnto/hUnit premise.'}],
 'type_only_evidence': {
   'bounded_diagnostic_support_inputs': pin('bounded-diagnostic-support-inputs.json'),
   'observations': support['diagnostic_runs'],
   'type1_correction': 'Original TYPE1(v1) failed inherited HP0 norm/inner-product instance synthesis. TYPE1(v2) inserts only letI inherited NormedAddCommGroup/InnerProductSpace HP0. Public mathematical binders and target conclusions are unchanged; this is a typing correction, not a mathematical repair overlay.',
   'current_type0_actual_pid': 13232, 'current_type1_actual_pid': 33448,
   'current_type0_and_type1_exit': 1,
   'current_only_error': 'noProof64_TYPE_ONLY_INTENTIONALLY_UNDEFINED',
   'theorem_proved_by_TYPE_checks': False,
   'reviewer_runs_Lean': False},
 'conceptual_mirror_audit': {
   'status': 'none-found', 'new_discovery_or_graph_admission': False,
   'mechanism_observed': 'Positive square gap -> positive root lower order -> centered bounded inverse recurs, and real/complex lift is an exact change-of-scalars adapter.',
   'reason': 'For this bounded header, canonical lifts and exact centered restriction are required formal dependency adapters, not weaker cross-model conceptual bridges. Existing family:l2-coercivity is useful navigation but its reversible decay map is not square-root inversion. No second source-backed domain/hypothesis/conclusion map is established here, so no new mirror or transport is proposed or validated.'},
 'fixed_support_input_pins': support['fixed_support_inputs'],
 'process_and_hash_contract': {
   'logical_run_digest': 'SHA256 of canonical UTF-8 JSON (sort_keys=True, ensure_ascii=False, compact separators), removing ONLY the top-level run_sha256. Every other payload field remains.',
   'full_named_RAW_payload_digest': 'SHA256 of the complete literal independent-header64.review.json bytes, including run_sha256 and final newline; separately stored in review-digests.json and terminal/lease layers.',
   'terminal_receipts': 'Actual foreground finalizer/readback child PIDs, exits and closed-process stdout/stderr are recorded after process completion by foreground runner. Their own post-exit receipt cannot be self-hashed; the later CLOSED_LAST lease binds each.',
   'owned_outputs_base_manifest': [pin(p.relative_to(BASE).as_posix()) for p in sorted(BASE.rglob('*')) if p.is_file() and p.relative_to(BASE).as_posix() not in excluded_outputs],
   'base_manifest_self_layer_exclusions': excluded_outputs,
   'pycache_policy': 'Recursive inventories include every owned file, including any pycache. No pycache or hidden-output blanket exclusion. CLOSED_LAST lease excludes only itself; its literal raw hash is reported by actual terminal readback.',
   'terminal_closure_not_yet_claimed_by_this_payload': True,
   'write_boundary': 'CLOSED_LAST lease is the final owned write. Subsequent native terminal readback is read-only.'},
 'run_sha256': None
}
logical = dict(payload)
logical.pop('run_sha256')
payload['run_sha256'] = hashlib.sha256(json.dumps(logical, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()
dump('independent-header64.review.json', payload)

md = '''The exact header0 and corrected header1 are accepted for the root's preproof Statement Seal consideration. This is independent statement/source review only; it grants no Statement Seal, theorem/science credit or whole-Goal admission.

Header0 states the required generic positive square-order implication on arbitrary real Lp(2,mu). Its three positivity premises belong to that background lemma. Header1 has only the original C2/Hessian/Gibbs/Gaussian assumptions and eta cap; it concludes the same actual positive root on the exact centered mean kernel, printed B15 operator order, unit, and one bounded inverse with both cancellation identities. Gamma and GammaP still kill constants, so the inverse is confined to HP0. Rank zero and alpha*eta=1 remain legal.

The seven slots (objects, domains, quantifiers, assumptions, conclusion, scopes/senses, constant dependencies), recursive binder audit, exact definition/AE representative audit, source coverage and exclusions are recorded in the named JSON payload. All existential witnesses are fixed before their universal action statements. Canonical e agrees with M, GammaP is defined from the same Gamma/e, qP=e q, and GammaP0 equals the literal restriction. These equalities prevent substituting unrelated roots or centers.

The explicit bound norm(Inv)<=1/gamma is a quantitative consequence of B15 rather than a separately printed source formula. B16 normalized leakage/polar isometry is future work: it needs this exact centered inverse and B11 Gram; onto Hperp is not asserted. Full B13 Sobolev identification, B14's independent -1/2 branch, B17/half-turn estimates, dynamics/mixing and other papers remain excluded.

Required internal proof debt is explicit: three canonical complex lifts and their subtraction identity; positive-root monotonicity; full-marginal constant projection to apply the real-Lp leaf; exact C4 production assembly joining rough mean gradient and Gaussian marginal Poincare with the same compact-gradient graph and actual conditional T; and derivation of unit/inverse/norm. No Test import into production and no new public gap/root/onto/unit certificate is authorized by this review. No proof search was performed.

The corrected TYPE1 differs only by two inherited HP0 norm/inner-product letI instances. The parent-owned TYPE0 and corrected TYPE1 terminal checks each exit1 solely at the intentional undefined proof-body identifier; they are type diagnostics, not completed theorems. This reviewer did not run Lean. The inspected science interface is commit 4d02622332d02d0bd6c977d3cee48fd535ebf203, not a new source re-review of SCI63.

The source graph and original assumptions were reread/sealed before exact header reads, with actual foreground source-reread child PID50080/exit0 and literal raw/LF region maps. Primary64 artifacts stay untouched. This review has no blocking semantic delta and requires no mathematical repair overlay. No new conceptual mirror is proposed: canonical lifts and centered restriction are exact dependency adapters rather than a separately supported cross-model bridge.

Finalizer/readback process receipts and CLOSED_LAST lease provide the native terminal closure layer. The logical payload digest removes only run_sha256; the full named RAW digest includes it. Self-referencing layers are excluded only from their own inventory and bound by later layers. Every owned file, including any pycache, is bound by the final lease except the lease itself, whose raw digest is checked and reported by the read-only terminal readback.
'''
(BASE / 'independent-header64.review.md').write_text(md, encoding='utf-8', newline='\n')
dump('review-digests.json', {'schema': 1, 'named_payload': 'independent-header64.review.json',
    'run_sha256': payload['run_sha256'], 'full_named_RAW_payload_sha256': sha(BASE / 'independent-header64.review.json'),
    'payload_bytes': (BASE / 'independent-header64.review.json').stat().st_size,
    'report_raw_sha256': sha(BASE / 'independent-header64.review.md'),
    'distinction': 'Logical whole-payload canonical digest removes ONLY run_sha256; full literal RAW named payload includes that field.'})
print(json.dumps({'event': 'REVIEW_WRITTEN', 'actual_pid': os.getpid(), **read('review-digests.json')}))
