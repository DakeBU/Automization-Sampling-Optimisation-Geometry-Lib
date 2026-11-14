"""Freeze this independent reviewer's raw-source-only phase 1 evidence.

Run only before exposure to any candidate statement, decoder, or implementation.
All outputs are confined to this script's phase1 directory.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
from bs4 import BeautifulSoup

ROOT = Path('/Users/zhouhuanjian/ASTIS-GC')
OUT = Path(__file__).resolve().parent
SOURCE = ROOT / '.astis/huanjian-resume-20261103/2610.20492v1.html'
EXPECTED = '6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write_json(name, obj):
    (OUT / name).write_bytes((json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode())


def exact_element(raw, ident):
    marker = b'id="' + ident.encode() + b'"'
    assert raw.count(marker) == 1, ident
    at = raw.index(marker)
    start = raw.rfind(b'<', 0, at)
    opening = re.match(rb'<([A-Za-z][A-Za-z0-9:_-]*)\b[^>]*>', raw[start:])
    assert opening is not None, ident
    tag = opening.group(1)
    token = re.compile(rb'<(/?)' + re.escape(tag) + rb'\b[^>]*>')
    depth = 0
    for m in token.finditer(raw, start):
        if m.group(1):
            depth -= 1
        elif not m.group(0).rstrip().endswith(b'/>'):
            depth += 1
        if depth == 0:
            end = m.end()
            excerpt = raw[start:end]
            parsed = BeautifulSoup(excerpt, 'html.parser')
            assert parsed.find(id=ident) is not None, ident
            return start, end, excerpt
    raise ValueError(ident)


raw = SOURCE.read_bytes()
assert sha(raw) == EXPECTED
assert not (OUT / 'manifest.json').exists(), 'Already frozen: do not overwrite phase 1.'
(OUT / 'source-excerpts').mkdir(exist_ok=True)
(OUT / 'instruction-snapshots').mkdir(exist_ok=True)

controls = [
    'AGENTS.md',
    'docs/proof-digestion-protocol.md',
    'docs/evidence-routed-memory-protocol.md',
    'docs/theorem-publication-protocol.md',
    '.agents/skills/astis-semantic-roundtrip/SKILL.md',
]
control_records = []
for i, path in enumerate(controls, 1):
    data = (ROOT / path).read_bytes()
    name = f'instruction-snapshots/{i:02d}-{Path(path).name}.raw'
    (OUT / name).write_bytes(data)
    control_records.append({'source_path': path, 'snapshot': name, 'bytes': len(data), 'sha256': sha(data)})

anchors = [
    'S2.p1', 'S2.p2', 'S2.SS0.SSS0.Px1', 'S2.SS0.SSS0.Px2',
    'S2.SS0.SSS0.Px4', 'S3.SS1.p1', 'S3.E4', 'S3.E5',
    'S3.SS1.p3', 'A2.SS1.p1', 'A2.SS1.SSS0.Px1.p1',
    'A2.Ex32', 'A2.Ex33', 'A2.Ex34', 'A2.Ex35',
    'A2.SS1.SSS0.Px1.p1.2', 'A2.SS1.SSS0.Px1.p1.3',
]
excerpts = []
for ident in anchors:
    start, end, data = exact_element(raw, ident)
    name = f'source-excerpts/{ident}.raw.html'
    (OUT / name).write_bytes(data)
    s = BeautifulSoup(data, 'html.parser')
    for m in s.find_all('math'):
        m.replace_with(m.get('alttext', ''))
    display = s.get_text(' ', strip=True) + '\n'
    derived_name = f'source-excerpts/{ident}.readable.txt'
    (OUT / derived_name).write_bytes(display.encode())
    excerpts.append({
        'source_id': ident, 'path': name, 'source_byte_start_inclusive': start,
        'source_byte_end_exclusive': end, 'bytes': len(data), 'sha256': sha(data),
        'readable_derivative': derived_name,
        'derivative_rule': 'BeautifulSoup html.parser; replace every math with its literal alttext; get_text(separator=" ", strip=True); append LF. Raw excerpt is authoritative.'
    })
write_json('source-excerpt-index.json', {
    'source_path': str(SOURCE.relative_to(ROOT)), 'source_bytes': len(raw),
    'source_raw_sha256': EXPECTED,
    'exact_excerpt_convention': 'Each .raw.html is an unmodified contiguous byte slice of the pinned raw HTML, including opening and closing element tags. Offsets are zero based.',
    'excerpts': excerpts,
})

def slot(text, *evidence):
    return {'statement': text, 'source_ids': list(evidence)}

semantic = {
    'phase': 1,
    'reviewer_identity': '/root/reader_570298',
    'source': {'title': 'On Complexity of Gaussian Sampling', 'revision': 'arXiv:2610.20492v1', 'raw_sha256': EXPECTED},
    'selected_scope': 'Only exact pointwise reconstruction of one first-order query, Appendix B.1 primitive definition and Ex33–35, interpreted using the actual Section 2 quadratic oracle and Section 3 E4/E5 precision. No adaptive transcript or full lower-bound certification.',
    'slots': {
        'objects': [
            slot('Euclidean real vectors and real matrices; O(n) consists of n by n real matrices O with transpose(O) O = I_n.', 'S2.p1', 'S2.p2'),
            slot('A_O = ((κ+1)/2) I_n - ((κ-1)/4)(O+transpose(O)); the actual full precision is A_boldO = diag(A_O1,...,A_Ok,I_(d-kn)). These are concrete matrices, not arbitrary block operators supplied by a query evaluator.', 'S3.E4', 'S3.E5'),
            slot('The potential is f_A(x) = (1/2) x^T A x, and exact FO_A(x) is the ordered value-and-gradient pair ((1/2)x^T A x, A x). The source target is the centered Gaussian N(0,A^{-1}), but no distributional conclusion is selected here.', 'S2.SS0.SSS0.Px1'),
            slot('Primitive oracle O_boldO(j,v,f) = O_j v; O_boldO(j,v,i) = transpose(O_j) v. Inverse means transpose of this orthogonal block.', 'A2.Ex32', 'A2.SS1.SSS0.Px1.p1.2'),
            slot('Query x=(x_1,...,x_k,z); each unknown block contributes g_j=((κ+1)/2)x_j-((κ-1)/4)(F_j+I_j), where F_j and I_j are the actual forward and inverse responses at the same input x_j.', 'A2.Ex33', 'A2.Ex34'),
        ],
        'domains': [
            slot('The Section 2 model has integer d≥1, real κ≥1, and A symmetric with I_d ⪯ A ⪯ κ I_d; x ranges over all R^d.', 'S2.SS0.SSS0.Px1'),
            slot('The selected hard-family construction stands at κ≥4, integer block dimension 3≤n≤d, k=floor(d/n), and tuple (O_1,...,O_k) in O(n)^k. Consequently d-kn is a nonnegative integer.', 'S3.SS1.p1'),
            slot('j ranges over {1,...,k}; primitive v and every x_j lie in R^n; z lies in R^(d-kn); τ has the two meaningful tags forward f and inverse i.', 'A2.Ex32', 'S3.E5', 'A2.Ex34'),
            slot('When kn=d, the identity block is omitted. The pointwise formula then has no residual coordinates; equivalently a zero-dimensional residual contributes the unique empty vector and zero inner-product term.', 'S3.SS1.p3', 'S3.E5', 'A2.Ex34', 'A2.Ex35'),
        ],
        'quantifiers': [
            slot('For every source-admissible κ,d,n and associated k, for every tuple of orthogonal blocks, for every point x=(x_1,...,x_k,z), and for each j=1,...,k, the displayed reconstruction equalities hold exactly. The oracle responses are fixed by those blocks and inputs; they are not independently chosen witnesses.', 'S3.SS1.p1', 'A2.Ex32', 'A2.Ex33', 'A2.Ex34', 'A2.Ex35'),
            slot('The pointwise equalities do not quantify over algorithms, seeds, transcripts, priors, stopping times, or target samples. Repeating a pointwise evaluator at T queries explains the local resource count, but adaptive law equality is a further argument outside this selection.', 'A2.SS1.SSS0.Px1.p1.3'),
        ],
        'assumptions': [
            slot('SOURCE/STANDING: the actual hard-family precision uses exactly E4/E5 and orthogonal blocks in the source parameter regime. TYPING: real finite Euclidean coordinates, their dimensions, ordinary inner product, transpose and matrix multiplication.', 'S2.p1', 'S2.p2', 'S3.SS1.p1', 'S3.E4', 'S3.E5'),
            slot('Exact oracle access: responses are precisely O_j x_j and transpose(O_j) x_j; no error, randomness, approximation tolerance, or noisy observations appear in the selected identities.', 'A2.Ex32', 'A2.Ex33', 'S2.SS0.SSS0.Px1'),
            slot('Appendix B.1 has the ambient condition 2T<n. It is used by the ensuing indistinguishability proof, not by the algebraic reconstruction equations Ex33–35. Likewise k=floor(d/n), n≥3, κ≥4 and orthogonality specify the source family, though the displayed matrix algebra extends beyond several of those restrictions. Such an extension should be identified as an algebraic generalization, not as a source repair.', 'A2.SS1.p1', 'S3.SS1.p1', 'A2.Ex33', 'A2.Ex34', 'A2.Ex35'),
            slot('No extra nonzero-vector, positive residual dimension, sign-specific determinant, Haar-randomness, Borelness, probability independence, spectral-bound witness, or pre-assumed reconstruction conclusion is required to establish these pointwise algebraic identities. The broader algorithm model has Borel requirements, but these are not additional premises of this selected pointwise result.', 'S2.SS0.SSS0.Px2', 'A2.Ex32', 'A2.Ex33', 'A2.Ex34', 'A2.Ex35'),
        ],
        'conclusion': [
            slot('For each block, A_Oj x_j = ((κ+1)/2)x_j - ((κ-1)/4)(O_boldO(j,x_j,f)+O_boldO(j,x_j,i)).', 'A2.Ex33'),
            slot('The actual gradient of f_(A_boldO) is (A_O1 x_1,...,A_Ok x_k,z), which is reconstructed as (g_1,...,g_k,z). The identity residual passes through unchanged.', 'A2.Ex34', 'S2.SS0.SSS0.Px1', 'S3.E5'),
            slot('The actual function value is (1/2)〈x,∇f_(A_boldO)(x)〉; hence the evaluator returns exactly the source FO ordered pair (value,gradient). In block coordinates the value is (1/2)(sum_j〈x_j,g_j〉+〈z,z〉). The expanded block expression is a consequence, not an extra source quotation.', 'A2.Ex35', 'A2.Ex34', 'S2.SS0.SSS0.Px1'),
            slot('One point needs at most two primitive queries per block: the forward and inverse responses at x_j. This is 2k primitive queries across all k blocks, with no primitive query on the identity residual and no further oracle query for the value.', 'A2.Ex32', 'A2.Ex33', 'A2.Ex34', 'A2.Ex35', 'A2.SS1.SSS0.Px1.p1.3'),
        ],
        'scopes': [
            slot('Equality is deterministic, pointwise and exact on the whole source query domain, not almost everywhere, in probability, in expectation, or only on nonzero vectors.', 'A2.Ex33', 'A2.Ex34', 'A2.Ex35'),
            slot('The pair has the Section 2 meaning: actual quadratic value and actual gradient/matrix-vector product for E4/E5. Equality to a separately invented response function without this connection would leave an unproved semantic bridge.', 'S2.SS0.SSS0.Px1', 'S3.E4', 'S3.E5', 'A2.Ex34', 'A2.Ex35'),
            slot('The resource phrase is per block. Two calls total for all k unknown blocks is not the selected source assertion.', 'A2.SS1.SSS0.Px1.p1.3'),
            slot('The last sentence of the Oracle reduction paragraph also claims sufficiency of adaptive primitive transcript indistinguishability when 2T<n. This phase does not certify that adaptive reduction, its measurability, conditional Haar laws, Lemma 3.2, or the Gaussian sampling lower bound.', 'A2.SS1.SSS0.Px1.p1.3', 'S2.SS0.SSS0.Px2'),
            slot('The zero-residual convention is literal omission or its zero-dimensional Euclidean encoding; the z entry is not an extra unknown hard block.', 'S3.SS1.p3', 'S3.E5', 'A2.Ex34'),
        ],
        'constant_dependencies': [
            slot('The reconstruction coefficients are exactly c=(κ+1)/2 and a=(κ-1)/4, shared by all blocks; gradient uses c x_j - a(F_j+I_j), and value uses the exact scalar 1/2. They depend only on κ.', 'S3.E4', 'A2.Ex33', 'A2.Ex35'),
            slot('The resource bound is the absolute count two per block per point, hence at most 2T per block over T points. k enters only the total count 2k per point and number of coordinates; d-kn fixes residual dimension. There are no hidden constants or dependence on x,O_j,determinant sign,ε,or a probability event.', 'A2.Ex32', 'A2.Ex33', 'A2.SS1.SSS0.Px1.p1.3', 'S3.E5'),
            slot('n=2T+1 and 2T<n belong to the later lower-bound/indistinguishability application; they are not coefficient constraints or denominator conditions in Ex33–35.', 'S3.SS1.p1', 'A2.SS1.p1', 'A2.Ex33', 'A2.Ex35'),
        ],
    },
    'candidate_information_visible_before_freeze': False,
    'verdict': 'No candidate verdict in phase 1. This is an independently frozen source baseline.',
}
write_json('source-semantic-slots.json', semantic)

write_json('source-only-topology.json', {
    'scope': semantic['selected_scope'],
    'nodes': [
        {'id': 'model', 'kind': 'source-definition', 'source_ids': ['S2.SS0.SSS0.Px1'], 'meaning': 'Actual centered quadratic potential and exact value/gradient oracle.'},
        {'id': 'block-precision', 'kind': 'source-definition', 'source_ids': ['S3.E4'], 'meaning': 'Affine symmetric part of the orthogonal block.'},
        {'id': 'full-precision', 'kind': 'source-definition', 'source_ids': ['S3.E5', 'S3.SS1.p3'], 'meaning': 'Actual block diagonal precision and omission of zero residual.'},
        {'id': 'primitive', 'kind': 'source-definition', 'source_ids': ['A2.Ex32', 'A2.SS1.SSS0.Px1.p1.2'], 'meaning': 'Forward and transpose multiplication.'},
        {'id': 'block-reconstruction', 'kind': 'reused-display', 'source_ids': ['A2.Ex33'], 'meaning': 'Expand E4 on x_j and substitute the two primitive outputs.'},
        {'id': 'gradient', 'kind': 'reused-display', 'source_ids': ['A2.Ex34'], 'meaning': 'Apply actual block diagonal precision; identity residual stays z.'},
        {'id': 'value', 'kind': 'reused-display', 'source_ids': ['A2.Ex35'], 'meaning': 'Use actual quadratic oracle value as half inner product with gradient.'},
        {'id': 'local-resource', 'kind': 'substantive-proof-paragraph-selection', 'source_ids': ['A2.SS1.SSS0.Px1.p1.3'], 'meaning': 'Two primitive observations suffice per point per block; repetition gives at most 2T per block, algebraic accounting only.'},
    ],
    'edges': [
        {'parents': ['block-precision', 'primitive'], 'consumer': 'block-reconstruction', 'use_site': 'A2.Ex33', 'discharge': 'Definition substitution, distributivity of multiplication.'},
        {'parents': ['model', 'full-precision', 'block-reconstruction'], 'consumer': 'gradient', 'use_site': 'A2.Ex34', 'discharge': 'Symmetric quadratic gradient is matrix-vector product; block diagonal multiplication.'},
        {'parents': ['model', 'gradient'], 'consumer': 'value', 'use_site': 'A2.Ex35', 'discharge': 'Substitute Ax=gradient in (1/2)x^TAx.'},
        {'parents': ['primitive', 'block-reconstruction', 'gradient', 'value'], 'consumer': 'local-resource', 'use_site': 'A2.SS1.SSS0.Px1.p1.3', 'discharge': 'Only forward and inverse observations for each x_j are used; residual and inner product are direct arithmetic.'},
    ],
    'explicit_exclusions': [
        {'source_ids': ['S2.SS0.SSS0.Px2', 'S2.SS0.SSS0.Px4'], 'reason': 'Read as model context. Borel adaptive algorithms, stopping decisions, output laws, and deterministic cap semantics are outside pointwise reconstruction.'},
        {'source_ids': ['A2.SS1.p1'], 'reason': 'Ambient 2T<n read and retained as surrounding application context; not a premise used by the pointwise algebra.'},
        {'source_ids': ['S3.SS1.p3'], 'reason': 'Only its explicit zero-residual omission convention is selected. Averaged Gaussian law and tensor product law are excluded.'},
        {'source_ids': ['A2.SS1.SSS0.Px1.p1.3'], 'reason': 'Adaptive transcript sufficiency assertion is excluded; only deterministic local query count is selected.'},
        {'source_ids': ['S3'], 'reason': 'Whole S3 source text was displayed on initial raw-source read. All lower-bound, TV separation, indistinguishability, regularity proof and theorem-completion claims remain outside this selected review.'},
    ],
    'source_gaps_within_selected_pointwise_algebra': [],
    'remaining_boundary': 'No adaptive simulation construction, Borel response-map proof, transcript law equality, source-wide regularity proof or lower bound has been reviewed.',
})

write_json('exposure-log.json', {
    'reviewer': '/root/reader_570298',
    'input_message': 'Parent supplied only source identity/raw digest, exact source anchors, selected pointwise scope, phase separation, prohibited targets, and owned output directory.',
    'chronological_exposures': [
        {'order': 1, 'kind': 'metadata-only-inventory', 'detail': 'pwd and rg --files for AGENTS/protocol filenames across ASTIS-GC and .agents. Returned unrelated protocol snapshot names; no file contents.'},
        {'order': 2, 'kind': 'instruction-content', 'paths': ['AGENTS.md']},
        {'order': 3, 'kind': 'instruction-content', 'paths': ['docs/proof-digestion-protocol.md', 'docs/evidence-routed-memory-protocol.md', 'docs/theorem-publication-protocol.md'], 'detail': 'Combined output partly truncated; publication and evidence-routed protocol were subsequently read separately.'},
        {'order': 4, 'kind': 'metadata-only-inventory', 'detail': 'rg --files for AGENTS/semantic filenames under .agents, docs, GaussianComplexity and source-cache directory. Returned filenames of older unrelated semantic/review artifacts; their contents were not opened. No first-order candidate statement, audit, seal, implementation or decoder contents exposed.'},
        {'order': 5, 'kind': 'instruction-content', 'paths': ['.agents/skills/astis-semantic-roundtrip/SKILL.md']},
        {'order': 6, 'kind': 'raw-source-content', 'path': str(SOURCE.relative_to(ROOT)), 'raw_sha256': EXPECTED, 'detail': 'Verified whole-file digest; displayed selected primitive paragraph including Ex32–35, S2 text, E4/E5, and entire S3 text. No candidate files were accessed.'},
        {'order': 7, 'kind': 'instruction-path-check', 'detail': 'Checked exact ancestor and output/source-subtree AGENTS.md paths; none existed beyond already-read repository AGENTS.md.'},
        {'order': 8, 'kind': 'raw-source-content', 'detail': 'Read title and direct child source text for S2, S3.SS1, A2.SS1; then selected S2 oracle/algorithm/budget paragraphs with formula alttext rendering.'},
        {'order': 9, 'kind': 'instruction-content', 'paths': ['docs/theorem-publication-protocol.md', 'docs/evidence-routed-memory-protocol.md'], 'detail': 'Complete separate reads.'},
        {'order': 10, 'kind': 'self-authored-source-only-record', 'detail': 'Created phase 1 exact excerpt extraction and independent semantic/topology/exposure records. No external candidate interpretation used.'},
    ],
    'candidate_statement_seen': False,
    'approved_candidate_definition_context_seen': False,
    'decoder_output_seen': False,
    'target_module_or_tests_seen': False,
    'statement_seal_seen': False,
    'publication_or_assumption_delta_payload_seen': False,
    'prior_verdict_or_review_content_seen': False,
    'canonical_reviewer_packet_seen': False,
    'write_scope': str(OUT.relative_to(ROOT)),
    'shared_source_V_or_ledger_writes': False,
    'browsers_or_security_workarounds_used': False,
    'detached_or_background_processes_used': False,
    'phase1_boundary': 'Freeze manifest before any selective candidate statement, approved definition context or blind reconstruction is delivered; stop at phase 1 until parent authorizes phase 2.',
})

(OUT / 'source-reconstruction.md').write_text('''# Independent raw-source reconstruction, phase 1

The exact source is arXiv:2610.20492v1, raw SHA-256
`6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`.
This baseline was written before seeing any candidate statement, code, decoder,
seal, publication payload, prior verdict, or canonical reviewer packet.

For the source hard family, fix κ≥4, 3≤n≤d and k=floor(d/n), and choose
O_j∈O(n). Let r=d-kn. The actual precision is the block diagonal matrix with
blocks A_j=((κ+1)/2)I-((κ-1)/4)(O_j+O_jᵀ), followed by I_r.
For any x=(x_1,…,x_k,z), obtain F_j=O_j x_j and I_j=O_jᵀ x_j from two
primitive calls per block. Then

    g_j=((κ+1)/2)x_j-((κ-1)/4)(F_j+I_j)=A_j x_j,
    g=(g_1,…,g_k,z)=A_boldO x=∇f_(A_boldO)(x),
    v=(1/2)〈x,g〉=f_(A_boldO)(x).

Thus (v,g) is exactly the Section 2 first-order response for the actual
Section 3 E4/E5 quadratic. The residual requires no primitive call. If r=0,
the source omits that block; its zero-dimensional encoding has zero contribution.
The pointwise count is at most two calls per block, hence 2k across all blocks.

The coefficients and value factor are exact. No probability statement or
nonzero-vector restriction occurs. The source parameter restrictions and
orthogonality identify the family, but the algebraic identities extend beyond
some of those restrictions. The source's ambient 2T<n is needed downstream;
it is not used in the pointwise equalities. This review does not establish
adaptive transcript simulation, Borel measurability, indistinguishability,
TV separation, or any full lower bound.

The authoritative detailed baseline is `source-semantic-slots.json`.
Exact source byte slices and offsets are in `source-excerpt-index.json`.
Readable text derivatives are provided only for inspection, not as raw evidence.
''', encoding='utf-8')

records = []
for p in sorted(OUT.rglob('*')):
    if p.is_file() and p.name != 'manifest.json':
        data = p.read_bytes()
        records.append({'path': str(p.relative_to(OUT)), 'bytes': len(data), 'sha256': sha(data)})
manifest = {
    'schema': 1,
    'phase': 'phase1-frozen-source-only',
    'reviewer_identity': '/root/reader_570298',
    'frozen_at_utc': datetime.now(timezone.utc).isoformat(),
    'source_path': str(SOURCE.relative_to(ROOT)), 'source_raw_bytes': len(raw), 'source_raw_sha256': EXPECTED,
    'scope': semantic['selected_scope'],
    'instruction_snapshots': control_records,
    'files': records,
    'manifest_hash_convention': 'SHA-256 and byte count of manifest.json are reported separately; manifest does not contain its own hash.',
    'write_scope': str(OUT.relative_to(ROOT)),
    'phase1_complete': True,
    'candidate_exposure_before_freeze': False,
    'next_action': 'STOP. Await selective statement, approved context and blind reconstruction; freeze phase 2 before any full canonical reviewer packet/code access.',
}
write_json('manifest.json', manifest)
data = (OUT / 'manifest.json').read_bytes()
print(json.dumps({'phase1_manifest': str((OUT/'manifest.json').relative_to(ROOT)), 'manifest_bytes': len(data), 'manifest_sha256': sha(data), 'source_sha256': EXPECTED, 'frozen_files': len(records)}, indent=2))
