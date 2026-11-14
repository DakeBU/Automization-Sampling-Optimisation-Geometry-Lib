"""Independent selective comparison; never opens surrounding candidate artifacts."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json

ROOT = Path('/Users/zhouhuanjian/ASTIS-GC')
BASE = ROOT / 'research-wiki/paper-contributions/GaussianComplexity/first-order-query-semantic-evidence'
OUT = Path(__file__).resolve().parent
P1 = BASE / 'fresh-source-reader-570298/phase1'
SELECTIVE = BASE / 'phase2-selective-input.json'
PINS = {
    'manifest.json': 'bc44863244c183b086f3c14f1f43a7e6fa5efc3e221a392fb5006ba2e8d985e6',
    'source-semantic-slots.json': 'db5727afd1ad6000cd0980b460d875f127def17f8ab2b8a34cf2701aa3a9fda8',
}
INPUT_SHA = 'ab7f2b914f279787274562f09f21647cbd211114512de8f803b39471302b96f1'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dump(name, value):
    data = (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()
    (OUT / name).write_bytes(data)


assert not (OUT / 'manifest.json').exists(), 'Already frozen: do not overwrite.'
phase1_records = []
for name, expected in PINS.items():
    b = (P1 / name).read_bytes()
    assert sha(b) == expected, name
    phase1_records.append({'path': str((P1 / name).relative_to(ROOT)), 'bytes': len(b), 'sha256': sha(b)})
baseline = json.loads((P1 / 'source-semantic-slots.json').read_bytes())
raw = SELECTIVE.read_bytes()
assert sha(raw) == INPUT_SHA
supplied = json.loads(raw)
packet = supplied['anonymous_decoder_packet']
lean = packet['lean']
decoder = supplied['blind_reconstruction']
statement = lean['statement'].encode()
reconstruction = decoder['reconstructed_theorem_text'].encode()
assert sha(statement) == lean['statement_sha256']
assert sha(reconstruction) == decoder['reconstructed_text_sha256']
assert set(baseline['slots']) == {'objects', 'domains', 'quantifiers', 'assumptions', 'conclusion', 'scopes', 'constant_dependencies'}
(OUT / 'phase2-selective-input.raw.json').write_bytes(raw)
(OUT / 'anonymous-statement.exact.txt').write_bytes(statement)
(OUT / 'blind-reconstruction.exact.txt').write_bytes(reconstruction)
dump('approved-definition-context.json', lean['approved_definition_context'])

def comparison(source, candidate, reconstruction_assessment, status, references):
    return {
        'frozen_source_expectation': source,
        'independent_reading_of_expanded_statement': candidate,
        'blind_reconstruction_check': reconstruction_assessment,
        'assessment': status,
        'source_ids': references,
    }

slots = {
    'objects': comparison(
        'The actual centered quadratic potential f_A, actual E4/E5 block diagonal precision, primitive forward/transpose products, and assembled gradient/value; the residual precision is identity.',
        'Every meaning-carrying object is expanded in the statement: B_j=((κ+1)/2)I-((κ-1)/4)(O_j+O_jᵀ); A is a reindexed fromBlocks(blockDiagonal B,0,0,I_r); f=x·(Ax)/2; query is O_j v for false and O_jᵀv for true; g assembles the prescribed block expression and copies residual coordinates. The outer predicate is the genuine HasGradientAt and the actual gradient operation, not equality between two arbitrary response aliases.',
        'The decoder correctly reconstructs the same matrices, quadratic, primitive oracle, coordinate extraction, and g. Its inverse-selector interpretation matches the displayed conditional. No object substitution or invented response occurs.',
        'Equivalent for the selected pointwise objects, subject to later verification that approved library meanings and expanded signature match the actual module.',
        ['S2.SS0.SSS0.Px1', 'S3.E4', 'S3.E5', 'A2.Ex32', 'A2.Ex33', 'A2.Ex34', 'A2.Ex35']),
    'domains': comparison(
        'κ≥4, 3≤n≤d, k=floor(d/n), O_j∈O(n), x∈R^d, x_j∈R^n, residual z∈R^(d-kn), including residual dimension zero.',
        'hn:3≤n, hnd:n≤d, hκ:4≤κ and Os:Fin(d/n)→orthogonalGroup(Fin n)ℝ reproduce this regime. EuclideanSpace ℝ (Fin d) and WithLp coordinate transport preserve ordinary Euclidean entries and inner product. Let q=d/n and r=d%n; Nat.div_add_mod gives q*n+r=d. Hence r=d-q*n, and the residual dimension is exactly the source dimension. Fin 0 is empty, so the residual branch disappears when n divides d.',
        'The decoder explicitly allows an empty Fin r and both determinant signs, gives ordinary real Euclidean domains, and identifies q and r correctly.',
        'Equivalent after finite-coordinate and remainder identifications. Source d≥1 follows from 3≤n≤d, so no source-admissible parameter is lost.',
        ['S2.p1', 'S2.p2', 'S3.SS1.p1', 'S3.E5', 'S3.SS1.p3', 'A2.Ex32', 'A2.Ex34']),
    'quantifiers': comparison(
        'Universally fix source-admissible dimensions and κ, then all tuples of orthogonal blocks, then every query point; primitive outputs are determined by those choices.',
        'The expanded quantifier order is ∀d,n with hn,hnd, ∀κ with hκ, ∀Os, followed by deterministic let definitions and ∀x. There is no existential or theorem-shaped premise supplying differentiability, a correct gradient, a correct response, or the reconstruction conclusion. The proof used by finCongr is a cardinality equality from natural division, not an extra mathematical binder.',
        'The decoder preserves this order and correctly treats all definitions as fixed before x. Its derivative representation quantifies over increments as the meaning of HasGradientAt, not an additional source assumption.',
        'Equivalent for the selected universal pointwise assertion.',
        ['S3.SS1.p1', 'A2.Ex32', 'A2.Ex33', 'A2.Ex34', 'A2.Ex35']),
    'assumptions': comparison(
        'Only source parameter restrictions and orthogonal-block typing identify this family. Actual exact responses are definitions. No nonzero point, positive residual dimension, determinant-sign, Haar-randomness or gradient-correctness premise belongs to this algebraic reconstruction.',
        'All displayed hypotheses are hn,hnd,hκ and the orthogonalGroup domain. Both query branches are exact matrix-vector definitions. HasGradientAt is in the conclusion. There is no auxiliary symmetry/regularity/consistency witness supplied as a premise. The source ambient 2T<n is absent because no T, algorithm or adaptive assertion is present.',
        'The decoder explicitly identifies the numerical restrictions and orthogonality and correctly says differentiability and gradient correctness are conclusions. It introduces no extra premise.',
        'No excess binder or omitted premise required by the selected source algebra is visible. Absence of 2T<n is the already-frozen pointwise scope distinction, not a source repair.',
        ['S3.SS1.p1', 'A2.SS1.p1', 'A2.Ex32', 'A2.Ex33', 'A2.Ex34', 'A2.Ex35']),
    'conclusion': comparison(
        'Each reconstructed block is A_Oj x_j; the actual full gradient is their assembly with z; the actual value is one half of its inner product with x. Together these are the exact source first-order response (value,gradient).',
        'For every x, HasGradientAt f (g x) x is proved in the proposition, and (f x,gradient f x)=(inner ℝ x (g x)/2,g x). Given the displayed f,A,g, this asserts both real gradient correctness and actual quadratic value reconstruction. Dividing by 2 matches multiplication by 1/2 over ℝ. The source block identity is embodied by B_j and the formula for gb; the theorem states the assembled derivative/response rather than a separately named block equality.',
        'The decoder reconstructs both conjoined conclusions for the same x and g, including that HasGradientAt is a conclusion. Its derivative h↦〈g,h〉 agrees with the approved real-gradient meaning.',
        'Equivalent for the selected Ex33–35 first-order reconstruction, with an explicit differentiability certification supporting the source gradient sense. No discrepancy in value/gradient order or numerical factor.',
        ['S2.SS0.SSS0.Px1', 'A2.Ex33', 'A2.Ex34', 'A2.Ex35']),
    'scopes': comparison(
        'Deterministic exact equality at every point for the actual E4/E5 potential, two primitive responses per unknown block, residual omission when empty. Adaptive transcript simulation and lower bounds are excluded.',
        'All equalities are ordinary exact equalities and HasGradientAt is pointwise everywhere. The coordinate equivalence sends (i,j) through prodComm to (j,i), so approved finProdFinEquiv gives global j*n+i; the residual coordinate is q*n+i. Thus the matrix reindex and gradient assembly use the same consecutive block layout. The local gb formula uses one false and one true primitive expression for each block at the same xb. There is no explicit cost, Borel algorithm, transcript law or resource-cap proposition in the theorem.',
        'The decoder correctly reconstructs coordinate order and unchanged remainder and expressly disclaims a separate query-complexity assertion. Its pointwise reading matches the statement.',
        'Equivalent on pointwise reconstruction. The formula demonstrates that two mathematical primitive responses per block suffice, but no formal query-cost or adaptive simulation theorem is supplied by this proposition.',
        ['S3.E5', 'S3.SS1.p3', 'A2.Ex33', 'A2.Ex34', 'A2.Ex35', 'A2.SS1.SSS0.Px1.p1.3']),
    'constant_dependencies': comparison(
        'Exact coefficients c=(κ+1)/2 and a=(κ-1)/4; value factor 1/2. Two primitive responses per block per point; no hidden constants, tolerances, random events or T-dependent coefficients.',
        'The B and gb formulas use exactly those shared κ coefficients; f and reconstructed value divide by 2. The number of full blocks and residual cardinality are functions only of d,n. Query depends on Os and its inputs, and not κ. No unspecified constant, ε, asymptotic factor, random variable or T appears.',
        'The decoder identifies all numerical factors and parameter dependencies correctly. Its expanded dependency inventory is compatible with the frozen baseline.',
        'Equivalent; no coefficient or constant-scope drift.',
        ['S3.E4', 'S3.E5', 'A2.Ex33', 'A2.Ex35', 'A2.SS1.SSS0.Px1.p1.3']),
}

differences = [
    {'id': 'D1', 'classification': 'same-under-index-equivalence', 'blocking': False, 'source': 'Blocks numbered 1,...,k and local real Euclidean coordinates.', 'candidate': 'Blocks Fin(d/n), numbered 0,...,q-1; e(inl(i,j))=j*n+i.', 'reason': 'Renaming the block index by j_source=j_Fin+1 preserves block order and all pointwise formulas.'},
    {'id': 'D2', 'classification': 'same-under-natural-division-identity', 'blocking': False, 'source': 'Residual identity I_(d-kn).', 'candidate': 'Residual identity indexed by Fin(d%n).', 'reason': 'k=d/n, and Nat.div_add_mod gives d=k*n+(d%n). Zero residual is included, not ruled out.'},
    {'id': 'D3', 'classification': 'same-under-tag-renaming', 'blocking': False, 'source': 'Forward f and inverse i.', 'candidate': 'false=forward and true=transpose/inverse.', 'reason': 'The conditional and gb use the correct two branches. The full orthogonal group makes transpose the inverse and includes both determinant signs.'},
    {'id': 'D4', 'classification': 'source-implicit-made-explicit-conclusion', 'blocking': False, 'source': 'Uses ∇f of a concrete symmetric quadratic.', 'candidate': 'HasGradientAt is an additional explicit conclusion alongside the gradient/value equality.', 'reason': 'This establishes the genuine derivative sense needed by the source, rather than assuming it. It prevents totalized gradient fallback from proving a false semantic reconstruction.'},
    {'id': 'D5', 'classification': 'selected-boundary-omission', 'blocking': False, 'source': 'The surrounding Oracle reduction prose also counts at most 2T primitive queries per block and reduces adaptive transcript indistinguishability.', 'candidate': 'A pointwise derivative and first-order response theorem, with the two primitive expressions in gb but no resource semantics or algorithm.', 'reason': 'This is within the task-selected pointwise boundary. Formal budget accounting and adaptive reduction remain unproved by this theorem and cannot receive source completion credit from it.'},
    {'id': 'D6', 'classification': 'selected-boundary-omission', 'blocking': False, 'source': 'Appendix B.1 ambient 2T<n; main application later selects n=2T+1.', 'candidate': 'No T binder or 2T<n premise.', 'reason': 'The frozen phase1 baseline already identified these as downstream application restrictions unused by Ex33–35. The candidate preserves all actual family-domain conditions.'},
]

traps = [
    {'id': 'T1', 'risk': 'An arbitrary oracle/response alias could make the theorem tautological.', 'result': 'Not present in supplied statement: actual matrices, quadratic, primitive products and Euclidean gradient are fully expanded.'},
    {'id': 'T2', 'risk': 'A totalized gradient could return zero outside differentiability.', 'result': 'Resolved at statement level by conjoined HasGradientAt conclusion for the same f,x,g. Actual proof still requires module review.'},
    {'id': 'T3', 'risk': 'Block/local coordinate order could be interleaved instead of the source E5 layout.', 'result': 'Not present under approved context: prodComm then finProdFinEquiv gives j*n+i, and reindex/assembly share e.'},
    {'id': 'T4', 'risk': 'Bool true/false could reverse forward and inverse semantics.', 'result': 'Not present: true chooses transpose, false chooses O_j, matching decoder and frozen source after tag renaming.'},
    {'id': 'T5', 'risk': 'Finite remainder could require a nonempty residual or leave an extra unknown block.', 'result': 'Not present: no positivity premise for d%n, identity residual is copied directly, and Fin 0 is empty.'},
    {'id': 'T6', 'risk': 'Two calls per block could be overclaimed as two calls for all blocks, or as a proved adaptive query budget.', 'result': 'Expanded gb has two primitive expressions for each j. The proposition itself has no cost or adaptive semantics; those stronger claims remain excluded.'},
    {'id': 'T7', 'risk': 'Correctness/differentiability/spectral estimates could be inserted as assumptions.', 'result': 'Not present in expanded binders. Source family typing and numerical restrictions are the only logical inputs.'},
    {'id': 'T8', 'risk': 'Approved context could differ from actual imported/project definitions.', 'result': 'Still pending exact-module/full-context verification. Phase2 is conditional on the six supplied approved definition meanings.'},
]

pending = [
    {'id': 'P1', 'kind': 'review-evidence', 'required_for_final_source_review': True, 'obligation': 'Bind this selective comparison to the actual canonical reviewer packet, publication context and reviewer run after phase2 freeze. No final canonical verdict has been issued.'},
    {'id': 'P2', 'kind': 'module-context', 'required_for_final_source_review': True, 'obligation': 'Check the exact candidate module, imports, namespace/scoped parameters, definition implementations and elaborated signature match this expanded statement and approved context, including coordinate indexing and gradient conventions.'},
    {'id': 'P3', 'kind': 'proof-and-compiler-evidence', 'required_for_final_source_review': True, 'obligation': 'Inspect the actual proof and focused compilation/axiom/fake-closure evidence for HasGradientAt and the pair equality. The selective compiled=true field is supplied metadata; this reviewer has not opened compiler receipts or the proof.'},
    {'id': 'P4', 'kind': 'publication-scope', 'required_for_final_source_review': True, 'obligation': 'Check full source-facing statement and authored lesson preserve actual E4/E5 precision, genuine gradient, empty residual convention and the selected pointwise boundary, without granting adaptive or full lower-bound credit.'},
    {'id': 'P5', 'kind': 'outside-selected-mathematical-boundary', 'required_for_final_source_review': False, 'obligation': 'A formal primitive-query cost model and 2T-per-block resource accounting are not part of the present proposition. They need separate evidence if claimed.'},
    {'id': 'P6', 'kind': 'outside-selected-mathematical-boundary', 'required_for_final_source_review': False, 'obligation': 'Adaptive Borel simulation, stopping/query-cap preservation, transcript law equality, determinant-sign indistinguishability, Haar conditional arguments, TV separation and the full lower bound remain outside this selected review.'},
]

comparison_record = {
    'schema': 1, 'stage': 'PHASE2_FROZEN_SELECTIVE_COMPARISON',
    'reviewer_identity': '/root/reader_570298',
    'phase1_pins': PINS,
    'source_raw_sha256': baseline['source']['raw_sha256'],
    'selective_input_raw_sha256': INPUT_SHA,
    'anonymous_statement_sha256': sha(statement),
    'reconstructed_text_sha256': sha(reconstruction),
    'supplied_decoder_identity': decoder['decoder'],
    'supplied_decoder_packet_sha256': packet['packet_sha256'],
    'scope': baseline['selected_scope'],
    'method': 'Read the phase2 selective expanded statement directly against the previously frozen raw-source expectations, then independently compare the actual blind reconstruction. No earlier verdict, module, proof, lesson, audit, registry, seal, or canonical reviewer context was read.',
    'slots': slots,
    'differences': differences,
    'definition_sense_traps': traps,
    'pending_obligations': pending,
    'statement_level_result': 'All seven slots agree with the selected pointwise source reconstruction after explicit indexing/representation identifications. No blocking source discrepancy is visible in the selective statement or blind reconstruction.',
    'final_canonical_fidelity_verdict': 'PENDING: exact module/proof/publication and canonical packet binding are intentionally unseen until after this freeze.',
    'source_repair_proposed': False,
    'source_invalid_claim': False,
    'source_V_or_lifecycle_transition': False,
    'stop_rule': 'STOP before full canonical reviewer packet, candidate module/proof, authored lesson, audit/Registry or surrounding new packet artifacts are opened.',
}
dump('seven-slot-comparison.json', comparison_record)

dump('input-manifest.json', {
    'phase1_inputs': phase1_records,
    'selective_input': {'path': str(SELECTIVE.relative_to(ROOT)), 'snapshot': 'phase2-selective-input.raw.json', 'bytes': len(raw), 'raw_sha256': INPUT_SHA},
    'exact_extracted_strings': [
        {'field': 'anonymous_decoder_packet.lean.statement', 'path': 'anonymous-statement.exact.txt', 'bytes': len(statement), 'sha256': sha(statement), 'embedded_hash_verified': True},
        {'field': 'blind_reconstruction.reconstructed_theorem_text', 'path': 'blind-reconstruction.exact.txt', 'bytes': len(reconstruction), 'sha256': sha(reconstruction), 'embedded_hash_verified': True},
    ],
    'approved_context_count': len(lean['approved_definition_context']),
    'supplied_provenance': supplied['provenance'],
    'supplied_compilation_claim': lean['compiled'],
    'independently_opened_compiler_evidence': False,
    'packet_hash_validation_limit': 'Selective raw input, statement text, and reconstruction text digests were independently recomputed. Canonical packet/run hashes are supplied provenance labels; their original raw artifacts/hash algorithm were intentionally not opened in phase2.',
})

dump('exposure-log.json', {
    'reviewer_identity': '/root/reader_570298',
    'starts_from_frozen_phase1_manifest_sha256': PINS['manifest.json'],
    'chronological_phase2_exposures': [
        {'order': 1, 'kind': 'parent-instruction', 'detail': 'Authorized only the exact selective file and own phase1 baseline; instructed freeze phase2 before full context. Packaging-only gzip note was received, but no packaging artifact was opened and no mathematical conclusion was supplied by it.'},
        {'order': 2, 'kind': 'own-frozen-phase1', 'detail': 'Read/recomputed exact manifest and semantic-baseline pins; no phase1 content was modified.'},
        {'order': 3, 'kind': 'selective-candidate-and-decoder', 'path': str(SELECTIVE.relative_to(ROOT)), 'sha256': INPUT_SHA, 'detail': 'Read only the supplied JSON containing expanded anonymous statement, six approved context strings, independent blind reconstruction and provenance labels.'},
        {'order': 4, 'kind': 'selective-digest-check', 'detail': 'Recomputed the exact UTF-8 statement and reconstruction string SHA-256; both match their embedded pins.'},
        {'order': 5, 'kind': 'self-authored-comparison', 'detail': 'Wrote all seven comparisons, explicit source/representation differences, definition-sense traps and pending review boundaries in own phase2 directory.'},
    ],
    'full_canonical_reviewer_packet_seen': False,
    'candidate_module_or_proof_seen': False,
    'authored_lesson_seen': False,
    'publication_payload_seen': False,
    'audit_or_registry_seen': False,
    'statement_seal_seen': False,
    'prior_verdict_content_seen': False,
    'surrounding_new_packet_artifacts_or_capsule_seen': False,
    'source_V_or_ledger_or_shared_writes': False,
    'write_scope': str(OUT.relative_to(ROOT)),
    'state': 'PHASE2_FROZEN_STOP_BEFORE_FULL_CONTEXT',
})

(OUT / 'comparison-summary.md').write_text('''# Phase 2 selective comparison

All seven semantic slots agree with the independently frozen raw-source
baseline on the selected pointwise first-order reconstruction. The statement
uses the actual E4/E5 precision and its quadratic, reconstructs each unknown
block from the actual forward and transpose responses, copies the identity
residual, and proves the real derivative and value/gradient equality.

Finite indexing and remainder are equivalent encodings: block coordinate i in
block j maps to j*n+i; r=d mod n equals d-floor(d/n)*n. A zero-dimensional
residual is retained as an empty type, so the source omission convention holds.
The explicit HasGradientAt conclusion resolves the totalized-gradient concern.
The blind reconstruction preserves these meanings and every quantifier and
coefficient.

The gb formula uses two mathematical primitive responses per block. The theorem
has no formal query-cost or adaptive simulation assertion. Its absence of T and
2T<n matches the pointwise boundary already frozen in phase1. No source repair
or blocking statement-level source discrepancy was identified.

This is not a final canonical fidelity verdict. Exact module/import/definition
and proof checks, compilation/axiom evidence, publication scope, and canonical
reviewer-packet/run binding remain pending. No full module, proof, lesson,
publication, audit, registry, seal or full reviewer context has been opened.
Stop after freezing this phase; the detailed record is seven-slot-comparison.json.
''', encoding='utf-8')

files = []
for p in sorted(OUT.rglob('*')):
    if p.is_file() and p.name != 'manifest.json':
        b = p.read_bytes()
        files.append({'path': str(p.relative_to(OUT)), 'bytes': len(b), 'sha256': sha(b)})
dump('manifest.json', {
    'schema': 1, 'phase': 'phase2-frozen-selective-comparison',
    'reviewer_identity': '/root/reader_570298',
    'frozen_at_utc': datetime.now(timezone.utc).isoformat(),
    'phase1_manifest_sha256': PINS['manifest.json'],
    'phase1_semantic_baseline_sha256': PINS['source-semantic-slots.json'],
    'selective_input_raw_sha256': INPUT_SHA,
    'files': files,
    'manifest_hash_convention': 'Manifest byte count and SHA-256 are reported separately; manifest does not hash itself.',
    'phase2_complete': True,
    'canonical_context_seen_before_freeze': False,
    'next_action': 'STOP. Wait for parent to supply full exact module/context only after phase2 frozen hash is delivered.',
})
for name in ['seven-slot-comparison.json', 'input-manifest.json', 'exposure-log.json', 'manifest.json']:
    b = (OUT / name).read_bytes()
    print(name, len(b), sha(b))
print('STOP: phase2 frozen; no full canonical context opened.')
