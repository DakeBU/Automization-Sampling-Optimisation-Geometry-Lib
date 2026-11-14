#!/usr/bin/env python3
"""Freeze the source-versus-blind comparison before implementation exposure."""
from pathlib import Path
import datetime
import gzip
import hashlib
import json
import os

BASE = Path('/Users/zhouhuanjian/ASTIS-GC/research-wiki/paper-contributions/GaussianComplexity/tv-amplification-semantic-evidence')
PACKET = BASE / 'staged-source-versus-blind-input.json'
OUT = Path(__file__).resolve().parent
PHASE1 = BASE / 'fresh-source-v2/phase1/source-expectations.json'
PHASE1_SHA = '9200b0c66a9339f3b8198b3128fffac25032c593080e956bf08356c0311d637c'
PACKET_SHA = 'd4df7075f2037d57bff90c2f8782e1ec87639cd592a8df40468b2155eb210709'


def sha(value):
    return hashlib.sha256(value).hexdigest()


def jbytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode('utf-8')


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        assert key not in result, 'Duplicate JSON key: ' + key
        result[key] = value
    return result


def write_json(name, value):
    (OUT / name).write_bytes(jbytes(value))


def write_gzip(name, payload):
    (OUT / name).write_bytes(gzip.compress(payload, mtime=0))


raw = PACKET.read_bytes()
assert sha(raw) == PACKET_SHA
packet = json.loads(raw, object_pairs_hook=unique_object)
phase1_raw = PHASE1.read_bytes()
assert sha(phase1_raw) == PHASE1_SHA
phase1 = json.loads(phase1_raw, object_pairs_hook=unique_object)
assert packet['original_source_snapshot_sha256'] == phase1['source_identity']['raw_sha256']
statement = packet['lean']['statement'].encode('utf-8')
blind = packet['blind_reconstruction']['text'].encode('utf-8')
assert sha(statement) == packet['lean']['statement_sha256']
assert sha(blind) == packet['blind_reconstruction']['text_sha256']
context = jbytes(packet['approved_definition_context'])

write_gzip('selective-input.raw.json.gz', raw)
write_gzip('literal-statement.txt.gz', statement)
write_gzip('blind-reconstruction.txt.gz', blind)
write_gzip('approved-definition-context.json.gz', context)

obligations = [
    {
        'id': 'O1',
        'kind': 'constructor/probability',
        'required_meaning': 'The normalized whole-group Haar μ has mass 1; det=±1 are measurable equal-half components; νpos=2•μ.restrict(det=1) and νneg=2•μ.restrict(det=-1) are exactly the source conditioned Haar probabilities.',
        'why_needed': 'The explicit factor 2 represents conditioning only after equal component masses are established. The approved constructor meaning alone states the normalization of μ, not the half-mass theorem.',
        'later_evidence_needed': 'Component measurability/half-mass and probability/conditioning identities, or an equally strong established theorem applicable in the stated n≥3 domain.',
        'status': 'not-audited; no proof/module exposed',
    },
    {
        'id': 'O2',
        'kind': 'constructor/covariance',
        'required_meaning': 'For every orthogonal block tuple in the construction, Bκ(O) and its assembled/reindexed precision A are real symmetric positive definite with I≼A≼κI; the matrix inverse is the genuine positive-definite inverse; γ(A) is N(0,A⁻¹).',
        'why_needed': 'Matrix inverse and multivariateGaussian are total constructors. The source only uses admissible nonsingular precision matrices. Merely writing γ with covariance argument A⁻¹ does not establish the source Gaussian interpretation.',
        'later_evidence_needed': 'Orthogonality-to-spectral/positive-definite proof, preservation by finite blocks and reindexing, inverse positivity, and correct Gaussian covariance/mean bridge on the actual support.',
        'status': 'not-audited; source includes regularity proof but implementation has not been read',
    },
    {
        'id': 'O3',
        'kind': 'constructor/mixture',
        'required_meaning': 'Dpos/Dneg are measurable pushforwards of the independent sign-conditioned block products; Mpos/Mneg bind the intended measurable Gaussian family and are the source averaged target laws barπ_±1.',
        'why_needed': 'Source mixtures are actual probability laws. Total map/bind expressions need their measurability and probability identities, including support sufficient for O2, connected to the source objects.',
        'later_evidence_needed': 'Measurability of tuple-to-precision and relevant Gaussian kernels, product/pushforward/bind probability facts, and the actual-law identification.',
        'status': 'not-audited; no implementation claim is inferred from compilation',
    },
    {
        'id': 'O4',
        'kind': 'constructor/TV',
        'required_meaning': 'Mpos and Mneg are finite probability measures. Consequently toReal on all event masses has its ordinary real meaning and δ is exactly sup over Borel E of |Mpos(E)-Mneg(E)|, the source TV convention.',
        'why_needed': 'ENNReal.toReal sends infinity to zero and real sSup is totalized. The literal expression alone does not assert probability normalization or boundedness. Nonemptiness is elementary: E=∅ supplies value 0, even before probability normalization. Probability gives the defining set a bound of 1.',
        'later_evidence_needed': 'Actual mixture probability instances/lemmas and finite-event bridge; identification of the displayed supremum with the source TV and, if used, half-L1 or overlap identities.',
        'status': 'not-audited; required hypotheses are mathematically implied by the intended construction but code discharge is unknown',
    },
    {
        'id': 'O5',
        'kind': 'analytic/separation',
        'required_meaning': 'The actual single-block P_±1 satisfy the quantitative gap δ₁=(1/2)exp(-5n/sqrtκ), and this implies affinity a≤exp{-(1/8)exp(-10n/sqrtκ)}; an independently justified alternative proof of the same actual-law bound could also suffice.',
        'why_needed': 'The final literal statement contains neither the B.7 gap nor an affinity premise, so the final theorem must supply genuine actual-law separation in its proof rather than simply assume the desired scalar input. Compilation does not expose that analytic coverage.',
        'later_evidence_needed': 'Actual-mixture density/radial-test argument and its determinant cancellation, Poisson/Fubini/integrability boundaries, or a rigorously sufficient alternative; then normalized TV–affinity conversion with the exact constants.',
        'status': 'not-audited; this is an unresolved proof-coverage obligation, not a missing theorem hypothesis',
    },
    {
        'id': 'O6',
        'kind': 'analytic/product-and-residual',
        'required_meaning': 'The actual M_b laws identify with P_b^⊗q times the same standard Gaussian residual of dimension r=d%n, in the given coordinate order. Their affinity is a^q, and TV≥1-affinity.',
        'why_needed': 'The source final proof uses actual density products and Tonelli, not an arbitrary scalar power. The common residual must contribute mass/affinity 1. When r=0, the formal trivial residual must correspond to the source omitted-factor convention.',
        'later_evidence_needed': 'Gaussian and mixture product laws, coordinate transport, normalized densities/integrability/Tonelli or an equivalent measure proof, and the zero-dimensional unit-factor case.',
        'status': 'not-audited; no product-density or affinity proof exposed',
    },
    {
        'id': 'O7',
        'kind': 'arithmetic',
        'required_meaning': 'The natural division/remainder coordinate equation uses d=q*n+r, q≥1, 0≤r<n. All real coercions preserve the exact final expression, and raising the affinity upper bound to natural q yields the stated exponential.',
        'why_needed': 'These connect the explicit coordinate realization and nonnegative natural-power estimate to the source k-block statement.',
        'later_evidence_needed': 'Applicable natural arithmetic/coercion lemmas and the final affinity-to-bound step; n≥3 and κ≥4 already suffice mathematically.',
        'status': 'not-audited; small constructor/arithmetic discharge, not a domain repair',
    },
]

slot_rows = [
    {
        'slot': 'objects',
        'source_expectation': phase1['seven_slots']['objects'],
        'blind_reading': 'The blind reading names the full O(n), normalized whole-group Haar, twice-restricted sign measures, independent q-fold products, actual block precision pushforwards, Gaussian bind mixtures, and the event-mass supremum. It explicitly retains total inverse/Gaussian/sSup meanings.',
        'literal_check': 'B is exactly the source A_O formula. νpos/νneg are the explicit conditional-Haar representation, subject to O1. Dpos/Dneg map independent orthogonal tuples to the exact source block precision, subject to O2/O3. γ(A) is the source centered target on the positive-definite support, subject to O2; Mpos/Mneg are the source averaged targets subject to O3.',
        'source_vs_blind_relation': 'explicit-elaboration',
        'source_vs_literal_relation': 'explicit-elaboration',
        'exactness_limit': 'Actual-law equivalence requires O1–O4; these are not treated as proved. No object mismatch is visible in the literal construction.',
        'obligations': ['O1', 'O2', 'O3', 'O4'],
    },
    {
        'slot': 'domains',
        'source_expectation': phase1['seven_slots']['domains'],
        'blind_reading': 'd,n are natural with 3≤n≤d; κ is real with κ≥4; q=floor(d/n), r=d mod n. Carriers are finite real matrices, the full real orthogonal group, and real Euclidean spaces with Borel structures.',
        'literal_check': '∀ {d n:ℕ} (hn:3≤n) (hnd:n≤d) {κ:ℝ} (hκ:4≤κ) is the source domain. Natural division and remainder exactly realize k and m. No oddness, algorithm budget, or ε restriction is added.',
        'source_vs_blind_relation': 'same',
        'source_vs_literal_relation': 'same',
        'exactness_limit': 'The total definition γ on every real matrix extends notation beyond source admissible inputs; it does not change the support used by the intended mixtures if O2/O3 hold.',
        'obligations': ['O2', 'O3', 'O7'],
    },
    {
        'slot': 'quantifiers',
        'source_expectation': phase1['seven_slots']['quantifiers'],
        'blind_reading': 'For every permissible d,n,κ the displayed constructed positive- and negative-sign mixtures satisfy the bound. Each sign selects its own q-fold product; no random common-sign mixture is formed.',
        'literal_check': 'The universals match. The sign pair is instantiated as pos/neg instead of a bound sign variable, with the same two-prior result. Natural block indices use 0,…,q-1 rather than source 1,…,k. No free scalar/measure premise stands in for the source distributions.',
        'source_vs_blind_relation': 'equivalent',
        'source_vs_literal_relation': 'equivalent',
        'exactness_limit': 'Zero-based indexing and implicit Lean binders are notation elaborations; the construction’s prior-specific independence must still be justified where used.',
        'obligations': ['O1', 'O3'],
    },
    {
        'slot': 'assumptions',
        'source_expectation': phase1['seven_slots']['assumptions'],
        'blind_reading': 'Only 3≤n≤d and κ≥4 are theorem premises. The reconstruction explicitly warns that the total Gaussian, toReal and supremum constructors do not by themselves establish covariance validity, normalization, or boundedness.',
        'literal_check': 'There are no strengthened theorem hypotheses requiring a single-block gap, an affinity bound, an abstract product identity, Gaussian covariance validity, or mixture probability as externally supplied premises. The actual source construction mathematically supplies these properties, but their proof coverage is invisible at this stage.',
        'source_vs_blind_relation': 'explicit-elaboration',
        'source_vs_literal_relation': 'explicit-elaboration',
        'exactness_limit': 'The constructor safeguards expose source-implicit obligations. They are neither demonstrated code facts nor evidence of domain mismatch. Analytic O5/O6 are proof dependencies, not necessarily statement assumptions to add.',
        'obligations': ['O1', 'O2', 'O3', 'O4', 'O5', 'O6', 'O7'],
    },
    {
        'slot': 'conclusion',
        'source_expectation': phase1['seven_slots']['conclusion'],
        'blind_reading': '1-exp(-(q/8)exp(-10n/sqrtκ))≤Δ, with Δ literally the event-mass toReal supremum of Mpos and Mneg, and no silent replacement by TV.',
        'literal_check': 'The final scalar expression is algebraically exact, with the source ≥ direction expressed as lower-bound ≤δ. After O1–O4 identify Mpos/Mneg and δ, it is exactly TV(barπ_+,barπ_-)≥1-exp{-(k/8)exp(-10n/sqrtκ)}.',
        'source_vs_blind_relation': 'equivalent',
        'source_vs_literal_relation': 'equivalent',
        'exactness_limit': 'This is conditional semantic equivalence after constructor elaboration, not an unconditional claim that the totalized δ has already been proved to be source TV. The intermediate Ex72 chain does not appear in the final literal statement; its proof or a sufficient alternative remains O5/O6.',
        'obligations': ['O1', 'O2', 'O3', 'O4', 'O5', 'O6', 'O7'],
    },
    {
        'slot': 'senses',
        'contract_alias': 'scopes',
        'source_expectation': phase1['seven_slots']['senses'],
        'blind_reading': 'The blind reconstruction preserves Borel events, real arithmetic, total measure conversions, the covariance caveat, and the zero-dimensional standard Gaussian point mass. It gives the exact global order j*n+a and q*n+b.',
        'literal_check': 'The e map first swaps (a,j) to (j,a), then finProdFinEquiv maps it to j*n+a; the sum concatenation places residual b at q*n+b. The identity block has size d%n, including zero. Under O2/O3, its zero-dimensional Gaussian unit factor corresponds to omitting the source residual. Under O4 the event supremum is precisely source TV; no half-L1 factor mismatch is visible.',
        'source_vs_blind_relation': 'explicit-elaboration',
        'source_vs_literal_relation': 'explicit-elaboration',
        'exactness_limit': 'No affinity or density symbol occurs in the final literal statement. If the source proof route is implemented, its unsquared affinity convention, normalized Lebesgue densities, and residual factor 1 require O5/O6.',
        'obligations': ['O2', 'O3', 'O4', 'O5', 'O6', 'O7'],
    },
    {
        'slot': 'constants',
        'contract_alias': 'constant_dependencies',
        'source_expectation': phase1['seven_slots']['constants'],
        'blind_reading': 'The reconstruction has q/8, exponent -10n/sqrtκ, outer complement 1, and natural q=floor(d/n).',
        'literal_check': 'Real.exp(-(((d/n:ℕ):ℝ)/8)*Real.exp(-(10*(n:ℝ))/Real.sqrt κ)) is exactly exp{-(k/8)exp(-10n/sqrtκ)}. There is no extra universal constant, asymptotic substitution, or omitted factor.',
        'source_vs_blind_relation': 'same',
        'source_vs_literal_relation': 'same',
        'exactness_limit': 'The constants’ analytic justification—single-block 1/2 and 5, then squared 1/4 and 10, then root/log factor 1/2 giving 1/8—is not supplied by the final statement alone and remains O5/O6/O7.',
        'obligations': ['O5', 'O6', 'O7'],
    },
]

comparison = {
    'document_kind': 'Independent phase2 original-source versus source-blind reconstruction and exact literal statement comparison',
    'phase': '2-frozen-before-full-packet-or-implementation',
    'phase1_expectation_sha256': PHASE1_SHA,
    'raw_source_sha256': phase1['source_identity']['raw_sha256'],
    'selective_input_raw_sha256': PACKET_SHA,
    'literal_statement_sha256': sha(statement),
    'blind_reconstruction_sha256': sha(blind),
    'approved_context_snapshot_sha256': sha(context),
    'parent_full_packet_hashes_as_reported_by_selective_packet_not_independently_verified': {
        'raw': packet['parent_full_packet_raw_sha256'],
        'canonical': packet['parent_full_packet_canonical_sha256'],
    },
    'comparison_scope': 'Compare frozen phase1 source expectations to the actual blind text and literal anonymous statement, using only the approved meaning context exported in the selective input. The full parent packet, proof, module, lesson, source graph and prior verdicts remain unexposed.',
    'pre_code_finding': {
        'primary_classification': 'implicit-assumption-exposed',
        'conditional_meaning_classification': 'equivalent-after-elaboration',
        'meaning': 'No visible domain, quantifier, construction-formula, block-order, inequality-direction, or numerical-constant mismatch. Once the enumerated constructor obligations identify the totalized measures and supremum with the source probability targets/TV, the literal conclusion matches the source. The selective packet alone does not establish those obligations or analytic separation coverage.',
        'not_claimed': 'No unconditional implementation equivalence, proof completion, publication acceptance, source-error verdict, or canonical audit result is made.',
        'repairs': 'No theorem domain/quantifier/conclusion repair is presently indicated. Obligations should be reviewed before proposing assumption additions; adding the desired gap as a premise would change the source-specific theorem unless presented separately as an abstract helper.',
    },
    'slot_name_mapping': {'objects':'objects','domains':'domains','quantifiers':'quantifiers','assumptions':'assumptions','conclusion':'conclusion','senses':'scopes','constants':'constant_dependencies'},
    'slot_comparisons': slot_rows,
    'blind_fidelity_to_literal': {
        'finding': 'The blind text faithfully reconstructs the visible literal construction and bound under the approved context. It exposes the totalized operations and correctly avoids asserting source TV without probability/finite-measure discharge.',
        'coordinate_check': 'prodComm(a,j)=(j,a), finProdFinEquiv(j,a)=j*n+a, residual concatenation=q*n+b. This agrees with source contiguous blocks.',
        'zero_residual_check': 'The formal zero-dimensional identity block and standard Gaussian point mass are a unit-factor elaboration of the source omitted-factor convention. The needed law/transport proof is O6.',
        'sSup_nonempty_nuance': 'The blind text warns in general that a total supremum does not establish nonemptiness or boundedness. For this particular defining set, nonemptiness follows immediately from the empty Borel event; boundedness and TV interpretation still require finite probability measures. This is a proof-obligation refinement, not a reconstruction error.',
        'compiled_flag_limit': 'The selective input says compiled=true. No compiler log or proof term was exposed, so this receipt records that claim without treating it as evidence of analytic or constructor coverage.',
    },
    'unresolved_obligations_for_later_code_review': obligations,
    'phase1_questions_status': {
        'Q1': 'Literal construction is visibly source-specific; actual-law constructor identification awaits O1–O4.',
        'Q2': 'Visible domains and natural k/m arithmetic match; implementation discharge awaits O7.',
        'Q3': 'Actual B.7 analytic coverage remains unexposed: O5.',
        'Q4': 'Final event-sup convention is compatible conditional on O4; proof-level TV/affinity constants remain O5/O6.',
        'Q5': 'Literal coordinate and residual dimensions match; actual product/zero-residual law remains O6.',
        'Q6': 'Final scalar bound/direction match. Full proof chain remains unexposed: O5/O6/O7.',
        'Q7': 'No abstract surrogate hypotheses appear in the final statement; helper specialization/coverage can only be reviewed later.',
        'Q8': 'No T, ε, odd-n or algorithm premise is added.',
        'Q9': 'Selective packet provides no new raw-source correction or conflicting source wording; phase1 editorial observations remain unchanged.',
        'Q10': 'All implementation analytic/constructor coverage remains unreviewed, with O1–O7 specifying the later questions.',
    },
    'stop_boundary': 'This comparison is frozen before any full exact canonical reviewer packet, source graph, audit, module/proof, lesson, candidate publication context, or previous verdict exposure.',
}
write_json('source-versus-blind-comparison.json', comparison)

receipt = {
    'reviewer': '/root/ex72_fresh_source_v2',
    'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'phase1_expectation_sha256_verified_before_comparison': PHASE1_SHA,
    'actual_additional_mathematical_input': {'path': str(PACKET), 'raw_bytes': len(raw), 'raw_sha256': PACKET_SHA, 'archive': 'selective-input.raw.json.gz'},
    'actual_additional_fields_seen': list(packet),
    'actual_compiled_statement_seen': {'anonymous': True, 'sha256': sha(statement), 'compiled_flag_as_reported': packet['lean']['compiled'], 'compiler_or_proof_evidence_seen': False},
    'actual_blind_reconstruction_seen': {
        'sha256': sha(blind),
        'decoder_as_reported': packet['blind_reconstruction']['decoder'],
        'decoder_packet_sha256_as_reported': packet['blind_reconstruction']['decoder_packet_sha256'],
        'decoder_run_sha256_as_reported': packet['blind_reconstruction']['decoder_run_sha256'],
        'source_text_visible_to_decoder_as_reported': packet['blind_reconstruction']['source_text_visible'],
    },
    'approved_definition_context': {'items': len(packet['approved_definition_context']), 'snapshot_sha256': sha(context), 'archive': 'approved-definition-context.json.gz'},
    'reported_withheld_fields': packet['withheld_fields'],
    'actual_exposure_statement': 'Only the one selective additional file was opened as new evidence. My own frozen phase1 expectations were read to verify their hash and populate comparisons. No parent full packet, module/proof, lesson, source graph, canonical audit, old verdict or candidate publication context was opened.',
    'parent_hash_limit': 'Parent full-packet raw/canonical hashes and decoder metadata are receipt fields only; their underlying unseen artifacts were not opened or recomputed.',
    'source_snapshot_limit': 'The selective file reports the same source raw SHA as phase1; my source expectations remain the pre-exposure immutable record and were not edited.',
    'operations': [
        'Read the exact selective file bytes; verify prescribed raw SHA256; parse JSON; print its entire actual contents for review.',
        'Compare actual anonymous literal statement, approved context and blind reconstruction against the already-frozen original-source expectations. No search or repository inventory occurred.',
        'Run this source-versus-blind freeze script, which reads only the selective file and own phase1 expectation file as evidence, verifies raw/text hashes and rejects duplicate JSON keys.',
        'Archive the exact selective bytes and exact statement/blind payload bytes with deterministic lossless gzip; archive the approved context as a deterministic JSON snapshot.',
        'Write the seven-slot comparison and actual exposure receipt, manifest payload hashes, and make phase2 files read-only. Stop before full packet/code exposure.',
    ],
    'whitespace_policy': 'No raw byte stripping, trailing-whitespace cleanup or line-ending rewrite. Exact raw input and text payloads are gzip-compressed with mtime=0; the manifest records compressed and decompressed byte counts/hashes.',
}
write_json('actual-exposure-and-input-receipt.json', receipt)
write_gzip('freeze-operation.log.txt.gz', ('Phase1 expectation SHA verified: '+PHASE1_SHA+'\nSelective input raw SHA verified: '+PACKET_SHA+'\nLiteral and blind text SHA fields verified.\nPhase2 source-versus-blind comparison frozen before code/full-context exposure.\n').encode('utf-8'))

entries = {}
for path in sorted(OUT.iterdir()):
    if not path.is_file() or path.name in {'manifest.json', 'FREEZE.sha256'}:
        continue
    data = path.read_bytes()
    entry = {'bytes': len(data), 'sha256': sha(data)}
    if path.suffix == '.gz':
        payload = gzip.decompress(data)
        entry.update({'decompressed_bytes':len(payload),'decompressed_sha256':sha(payload),'compression':'gzip,mtime=0'})
    entries[path.name] = entry
comparison_sha = entries['source-versus-blind-comparison.json']['sha256']
receipt_sha = entries['actual-exposure-and-input-receipt.json']['sha256']
write_json('manifest.json', {
    'phase':'2-frozen-before-full-packet-or-implementation',
    'comparison_sha256':comparison_sha,
    'actual_exposure_receipt_sha256':receipt_sha,
    'phase1_expectation_sha256':PHASE1_SHA,
    'selective_input_raw_sha256':PACKET_SHA,
    'files':entries,
    'freeze_note':'Every phase2 regular file is made mode 0444. No later code review may edit this phase2 snapshot.',
})
manifest_sha = sha((OUT/'manifest.json').read_bytes())
(OUT/'FREEZE.sha256').write_bytes((comparison_sha+'  source-versus-blind-comparison.json\n'+receipt_sha+'  actual-exposure-and-input-receipt.json\n'+manifest_sha+'  manifest.json\n').encode('ascii'))
for path in OUT.iterdir():
    if path.is_file():
        os.chmod(path, 0o444)
print(json.dumps({'comparison_sha256':comparison_sha,'actual_exposure_receipt_sha256':receipt_sha,'manifest_sha256':manifest_sha,'phase1_expectation_sha256':PHASE1_SHA,'phase2_directory':str(OUT),'constructor_and_analytic_obligations':len(obligations),'full_packet_or_code_seen':False},indent=2))
