#!/usr/bin/env python3
"""Create source-blind reconstruction artifacts from exactly two packet inputs.

The translation notes are a concise record of semantic decisions and coverage,
not a proof, source comparison, or source-facing verdict.
"""
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/Users/zhouhuanjian/ASTIS-GC')
OUT = ROOT / '.astis/semantic-neutral-20261115/blind_decoder_8a39'
DECODER = 'trace_domain_blind_decoder_8a39'
INPUTS = {
    letter: ROOT / f'.astis/huanjian-gc-trace-mgf-domain-20261115/packet-{letter}.anonymous.v1.json'
    for letter in ('a', 'b')
}

TEXT_A = r'''For every universe u and every carrier ι : Type u equipped with a finite enumeration, decidable equality, and at least one element, for every real square matrix A ∈ Matrix ι ι ℝ with Aᵀ = A, and for every real number s, both inequalities hold:

    0 < tr(expₘ(sA)),
    tr(expₘ(sA)) ≤ (card ι : ℝ) · expℝ(|s| · ‖A‖₂→₂).

Here matrix multiplication is the usual matrix multiplication on the entire carrier ι; expₘ is the power-series exponential in that matrix algebra, expₘ(B) = ∑ₙ₌₀^∞ Bⁿ/n!, while expℝ is the scalar real exponential. The trace is the unnormalized sum of all diagonal entries, tr(B) = ∑ᵢ∈ι Bᵢᵢ. The matrix norm ‖A‖₂→₂ is the operator norm induced by the Euclidean norm on real coordinate vectors indexed by ι. The product sA multiplies every entry of A by s, and |s| is real absolute value. Both conclusions concern every s ∈ ℝ, with no sign or magnitude restriction.
'''

TEXT_B = r'''For every pair of natural numbers d,q ∈ ℕ satisfying 2q + 1 < d, make the following definitions, in the displayed order. Write I_d = {0,…,d−1} for Fin d and J = {0,…,q} for Fin(q+1); when an index occurs in a real formula it means its natural-number value coerced to ℝ.

Let D = EuclideanSpace ℝ (Fin d), the real Euclidean space with coordinate carrier I_d, and E = EuclideanSpace ℝ (Fin(q+1)), the real Euclidean space with coordinate carrier J. Let Ω = J → D, so ω ∈ Ω assigns one vector ω_b ∈ D to each b ∈ J. Equip Ω with the unconditional measure

    μ = Measure.pi (b ↦ stdGaussian D),

the displayed finite product of the standard centered Gaussian law on D. Let

    M = Matrix (J × J) (J × J) ℝ,
    r = ((q+1 : ℕ) : ℝ),
    L = 2r + 3 log(1000 · (d : ℝ)),
    α_i = ((i.val : ℝ) + 1 − 1/2) · π / (d : ℝ)             (i ∈ I_d),
    t_i(k) = 1                                            if k.val = 0,
             √2 · cos((k.val : ℝ) · α_i)                  otherwise (k ∈ J).

Here log, cos, π and the square root are the real operations appearing in these definitions. Define the Euclidean row vector

    x_i(ω) = WithLp.toLp 2 (b ↦ ω_b(i)) ∈ E.

WithLp.toLp 2 and WithLp.ofLp change only the representation between coordinate functions and Euclidean vectors, preserving all coordinates. For every i ∈ I_d and every ω ∈ Ω define the real matrix Y_i(ω) ∈ M by the literal inclusive cutoff

    Y_i(ω) = (d : ℝ)⁻¹ · [outer(WithLp.ofLp(x_i(ω)), WithLp.ofLp(x_i(ω)))
                          ⊗ outer(t_i,t_i)]              if ‖x_i(ω)‖₂² ≤ L,
             0_M                                         otherwise.

The multiplication by (d : ℝ)⁻¹ is scalar multiplication of every matrix entry. The symbol outer(a,b) means Matrix.vecMulVec a b, with entry a_j b_k. The symbol ⊗ means Matrix.kronecker, with the first coordinate of each paired index coming from its first matrix factor. Thus the nonzero branch has entry, for b,k,b′,k′ ∈ J,

    Y_i(ω)_((b,k),(b′,k′))
       = (d : ℝ)⁻¹ · ω_b(i) · ω_b′(i) · t_i(k) · t_i(k′).

The other branch is the actual zero matrix, and the norm in the cutoff is the Euclidean norm of the row vector. Define

    mean_i = ∫_Ω Y_i(ω) dμ(ω) ∈ M,
    Z_i(ω) = Y_i(ω) − mean_i,

where the mean is exactly the displayed unconditional matrix-valued Bochner integral under μ. For Boolean values useCos and minus define deterministic weights and one global scalar sign by

    w_useCos(i) = cos((((2q+1 : ℕ) : ℝ)) · α_i)            if useCos = true,
                  1                                      if useCos = false,
    sign_minus = −1                                      if minus = true,
                 1                                       if minus = false,
    S_useCos,minus(ω) = sign_minus · ∑_{i∈I_d} w_useCos(i) · Z_i(ω),
    Rstar = 2r(L+1)/(d : ℝ).

The sum runs over every i ∈ Fin d. Both multiplications involving w_useCos and sign_minus are matrix scalar multiplications; sign_minus multiplies the entire sum. The Boolean choices are universally quantified deterministic selectors, not random signs.

Then for every real s ∈ ℝ and every useCos,minus ∈ Bool, let

    f(ω) = tr(expₘ(s · S_useCos,minus(ω))),
    B = r² · expℝ(|s| · ((d : ℝ) · Rstar)).

All of the following hold simultaneously:

    (1) f is Bochner integrable as a real scalar function on (Ω,μ);
    (2) for every ω ∈ Ω, 0 < f(ω) and f(ω) ≤ B;
    (3) 0 < ∫_Ω f(ω) dμ(ω);
    (4) ∫_Ω f(ω) dμ(ω) ≤ B.

The pointwise bounds hold for every ω, not only almost everywhere. All displayed integrals use exactly μ. There is no sign or magnitude restriction on s. The trace is the ordinary sum of all diagonal entries indexed by J × J, without division by the dimension; M has (q+1)² rows and (q+1)² columns. The matrix exponential expₘ is the power-series exponential ∑ₙ₌₀^∞ Aⁿ/n! in M with ordinary matrix multiplication; expℝ is the scalar real exponential. A norm of a matrix, if used, has the approved Euclidean operator-norm sense; the norm actually present in this proposition is the Euclidean row norm in the cutoff. No integrability premise is added to the definition of mean_i; the asserted integrability conclusion is specifically Integrable f μ.
'''

DETAIL_A = {
    'objects': 'An arbitrary finite nonempty carrier ι : Type u with Fintype, DecidableEq, and Nonempty instances; A : Matrix ι ι ℝ; s : ℝ; ordinary trace; matrix power-series exponential; real scalar exponential; Euclidean induced matrix operator norm.',
    'domains': 'u is the universe level of the arbitrary carrier. The index carrier ι is finite and nonempty, with decidable equality. A ranges over all real square matrices on ι subject to transpose equality; s ranges over all of ℝ. The trace sum uses every diagonal index in ι.',
    'quantifiers': 'For every {ι : Type u} with [Fintype ι] [DecidableEq ι] [Nonempty ι], for every A : Matrix ι ι ℝ, if A.IsHermitian, then for every s : ℝ both stated inequalities hold.',
    'assumptions': 'Exactly finite enumeration, decidable equality, nonemptiness of ι, and A.IsHermitian, which over ℝ means Aᵀ = A. There is no hypothesis on the sign or magnitude of s and no additional hypothesis on A.',
    'conclusion': 'The conjunction 0 < Matrix.trace (NormedSpace.exp (s • A)) and Matrix.trace (NormedSpace.exp (s • A)) ≤ (Fintype.card ι : ℝ) * Real.exp (|s| * ‖A‖).',
    'scopes': 'The matrix A is fixed before the universally quantified scalar s. Both inequalities share exactly the same ι, A, and s. The trace is unnormalized; exp on the left is matrix exponential and exp on the right is scalar real exponential. The displayed norm is Matrix.Norms.L2Operator.',
    'constant_dependencies': 'The prefactor is precisely the real coercion of card ι. The scalar exponent is precisely |s| * ‖A‖. No unspecified or existential constants occur.',
}

DETAIL_B = {
    'objects': 'Natural d,q with 2*q+1<d; D = EuclideanSpace ℝ (Fin d); E = EuclideanSpace ℝ (Fin(q+1)); Ω = Fin(q+1) → D; μ = Measure.pi (fun _ : Fin(q+1) => stdGaussian D); M = Matrix (Fin(q+1) × Fin(q+1)) (Fin(q+1) × Fin(q+1)) ℝ; the real quantities r,L,α,tvec,row,Y,mean,Z,w,sign,S,Rstar,f,B are exactly those defined in reconstructed_theorem_text. M has dimension (q+1)^2, with first paired coordinates from the row outer-product factor in the Kronecker product.',
    'domains': 'd,q ∈ ℕ, including q=0 when the inequality holds. Fin d has natural values 0,…,d−1; Fin(q+1) has values 0,…,q. Both row coordinates and tvec coordinates use Fin(q+1). Each ω is a function assigning a vector of D to each b ∈ Fin(q+1). The integration domain is all Ω with the displayed unconditional μ. s ranges over all ℝ; useCos and minus each range over both Boolean values. The cutoff includes equality, ‖row i ω‖^2 ≤ L; the other branch is the zero matrix. The pointwise conclusions range over every ω ∈ Ω.',
    'quantifiers': 'For all {d q : ℕ} and every proof hq of 2*q+1<d, the displayed let definitions precede ∀ s : ℝ, ∀ useCos minus : Bool. After f and B are defined for these s and selectors, the conclusion is Integrable f μ ∧ (∀ ω, 0 < f ω ∧ f ω ≤ B) ∧ 0 < ∫ ω, f ω ∂μ ∧ (∫ ω, f ω ∂μ) ≤ B. Each i in Y, mean, Z and the finite sum ranges over Fin d; b,k and the paired matrix indices range over Fin(q+1).',
    'assumptions': 'The only numerical hypothesis is 2*q+1<d for natural d,q. The Gaussian measure, matrices, truncation, centering, weights, sign and sums are definitions, not extra hypotheses. No integrability hypothesis is supplied for the displayed definition of mean, and no range restriction is supplied for real s. The conclusion itself asserts Integrable f μ. There are no additional probabilistic assumptions or extra matrix hypotheses.',
    'conclusion': 'For every real s and both values of each Boolean selector, f(ω) = Matrix.trace (NormedSpace.exp (s • S useCos minus ω)) is Bochner integrable under μ, is strictly positive and at most B for every ω, and its scalar Bochner integral under μ is strictly positive and at most B, where B is exactly r^2 * Real.exp (|s| * ((d : ℝ) * Rstar)).',
    'scopes': 'All definitions through Rstar are within the scope of d,q,hq. The μ in mean and in every conclusion is the same unconditional finite Gaussian product measure. mean_i does not depend on the current evaluation ω; Y_i(ω) is centered by that fixed matrix. The two Boolean arguments choose one deterministic weight family and one global scalar sign before f is evaluated at ω. The factor sign minus is outside the complete sum over Fin d. The Kronecker index order is ((row-coordinate, tvec-coordinate), (row-coordinate, tvec-coordinate)). The trace sums diagonal entries on the full paired carrier with no normalization. exp in f is matrix power-series exponential, exp in B is scalar Real.exp; row norms are Euclidean. The final pointwise conjunction is universal, not almost-everywhere.',
    'constant_dependencies': 'r = ((q+1 : ℕ) : ℝ); L = 2*r + 3*Real.log(1000*(d : ℝ)); α_i = ((i.val : ℝ)+1−1/2)*Real.pi/(d : ℝ); tvec uses exactly 1 at k.val=0 and Real.sqrt 2 * Real.cos((k.val : ℝ)*α_i) otherwise. Y uses exactly (d : ℝ)^(-1), the inclusive L cutoff and the two displayed outer products in that order. The cosine weight frequency is exactly ((2*q+1 : ℕ) : ℝ); the other weight is exactly 1. sign true is −1 and sign false is 1. Rstar = 2*r*(L+1)/(d : ℝ); B = r^2 * Real.exp(|s|*((d : ℝ)*Rstar)). Thus B depends only on d,q,s and not on either Boolean selector or ω. There are no unspecified or existential constants; no simplification of Rstar inside B is substituted for the literal definition.',
}

NOTES = {
    'a': '''Translation coverage summary for packet a:
- The arbitrary carrier and all three typeclass requirements are retained.
- The real Hermitian assumption is rendered as transpose equality.
- The output is a conjunction of strict trace positivity and an inclusive upper bound.
- The trace is unnormalized; the two exponentials have different carriers.
- The scalar parameter is every real number and the norm is the approved Euclidean operator norm.
- No source identity, proof comparison, or source-facing verdict is attempted.
Ambiguities: none requiring an added assumption within the supplied statement and approved definitions. The universe parameter is retained rather than selecting one concrete index type.
''',
    'b': '''Translation coverage summary for packet b:
- The natural-number inequality, all finite carriers and their endpoints, and all let definitions are retained.
- The angle retains +1−1/2 literally, and the cosine frequency retains the natural expression 2*q+1 before real coercion.
- The sample carrier is a function to D, with exactly the displayed finite Gaussian product measure.
- Euclidean row norms and matrix/real exponentials are distinguished.
- The cutoff is inclusive, the alternative is the zero matrix, and Kronecker paired-index order is expanded entrywise.
- The matrix mean is the displayed unconditional Bochner integral; no premise of mean integrability is added.
- The Boolean choices select deterministic weights and one global sign; the complete sum stays inside that sign.
- The four logical outputs include integrability, universal pointwise positivity and upper bound, and strict positivity and upper bound of the scalar integral.
- The matrix dimension prefactor r^2, and Rstar and B with all literal constants, are retained.
- No source identity, proof comparison, or source-facing verdict is attempted.
Ambiguities: none requiring an added assumption within the supplied statement and approved definitions. No assertion about any different measure, conditional law, random sign, or alternate cutoff is inferred.
''',
}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def encode_json(obj):
    return (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8')

def new_file(path, data):
    with path.open('xb') as out:
        out.write(data)

def main():
    started = datetime.now(timezone.utc).isoformat()
    OUT.mkdir(parents=True, exist_ok=True)
    script_hash = sha(Path(__file__).read_bytes())
    for letter, theorem, detail in [('a', TEXT_A, DETAIL_A), ('b', TEXT_B, DETAIL_B)]:
        raw_packet = INPUTS[letter].read_bytes()
        packet = json.loads(raw_packet)
        canonical_packet = json.dumps(
            {key: value for key, value in packet.items() if key != 'packet_sha256'},
            sort_keys=True, separators=(',', ':'), ensure_ascii=False,
        ).encode('utf-8')
        assert sha(canonical_packet) == packet['packet_sha256']
        assert sha(packet['lean']['statement'].encode('utf-8')) == packet['lean']['statement_sha256']
        assert packet['input_artifacts'] == ['lean-statement', 'approved-definition-context']
        assert packet['non_disclosure']['source_text_included'] is False
        theorem_path = OUT / f'packet-{letter}.reconstructed-theorem.v1.txt'
        notes_path = OUT / f'packet-{letter}.translation-notes.v1.txt'
        run_path = OUT / f'packet-{letter}.decoder-run.v1.json'
        result_path = OUT / f'packet-{letter}.decoder-result.v1.json'
        theorem_bytes = theorem.encode('utf-8')
        notes_bytes = NOTES[letter].encode('utf-8')
        new_file(theorem_path, theorem_bytes)
        new_file(notes_path, notes_bytes)
        run = {
            'schema_version': 1,
            'decoder': DECODER,
            'run_started_utc': started,
            'packet_processed_utc': datetime.now(timezone.utc).isoformat(),
            'process_id': os.getpid(),
            'input_path': str(INPUTS[letter]),
            'input_artifacts': packet['input_artifacts'],
            'input_file_sha256': sha(raw_packet),
            'packet_sha256': packet['packet_sha256'],
            'packet_hash_definition': 'SHA-256 of UTF-8 JSON excluding packet_sha256, sorted keys, compact separators, ensure_ascii=False',
            'lean_statement_sha256': packet['lean']['statement_sha256'],
            'source_text_visible': False,
            'input_access_scope': 'Only the two named anonymous packet inputs; own newly generated artifacts are also read for hashing. No source, sibling input, context, audit, protocol, Lean file, or repository instruction input was accessed.',
            'translation_method': 'Independent direct reading of Lean quantifiers and literal let definitions using only each packet approved_definition_context. Concise semantic coverage notes are separate; no proof or source comparison is performed.',
            'script_path': str(Path(__file__).resolve()),
            'script_sha256': script_hash,
            'reconstructed_text_path': str(theorem_path),
            'reconstructed_text_sha256': sha(theorem_bytes),
            'translation_notes_path': str(notes_path),
            'translation_notes_sha256': sha(notes_bytes),
            'noncircular_digest': 'This immutable run artifact does not contain its own digest or a hash of a result file. The decoder result hashes this run artifact after creation.',
        }
        run_bytes = encode_json(run)
        new_file(run_path, run_bytes)
        run_path.chmod(0o444)
        result = {
            'reconstructed_theorem_text': theorem,
            'reconstructed_text_sha256': sha(theorem_bytes),
            **detail,
            'decoder': DECODER,
            'decoder_run_sha256': sha(run_bytes),
            'source_text_visible': False,
            'schema_version': 1,
            'packet_id': packet['packet_id'],
            'input_artifacts': packet['input_artifacts'],
            'input_path': str(INPUTS[letter]),
            'input_file_sha256': sha(raw_packet),
            'packet_sha256': packet['packet_sha256'],
            'lean_statement_sha256': packet['lean']['statement_sha256'],
            'decoder_run_artifact': str(run_path),
            'reconstructed_text_artifact': str(theorem_path),
            'translation_notes_artifact': str(notes_path),
            'translation_notes_sha256': sha(notes_bytes),
            'ambiguities': 'No unresolved ambiguity requiring additional assumptions was identified within the supplied Lean statement and approved definition context. No source theorem was inferred.',
        }
        assert set(packet['output_contract']).issubset(result)
        assert result['reconstructed_theorem_text'].encode('utf-8') == theorem_bytes
        new_file(result_path, encode_json(result))
        print(json.dumps({
            'result_path': str(result_path),
            'result_sha256': sha(result_path.read_bytes()),
            'reconstructed_text_sha256': result['reconstructed_text_sha256'],
            'decoder_run_sha256': result['decoder_run_sha256'],
            'translation_notes_sha256': result['translation_notes_sha256'],
            'script_sha256': script_hash,
        }))

if __name__ == '__main__':
    main()
