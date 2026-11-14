from pathlib import Path
import hashlib, json
W = Path(__file__).parent
sha = lambda b: hashlib.sha256(b).hexdigest()
for n in ['StatementFormation.lean', 'consumer-signature.draft.txt']:
    p = W/n
    old = p.read_bytes()
    with (W/(n+'.coordinate-energy-v2.raw.txt')).open('xb') as f:
        f.write(old)
    text = old.decode()
    norm_old = '(∑ i : Fin d, (v i) ^ 2) ='
    norm_new = '‖(WithLp.toLp 2 v : EuclideanSpace ℝ (Fin d))‖ ^ 2 ='
    energy_old = '(∑ i : Fin d, Real.cos (((2 * q + 1 : ℕ) : ℝ) * θ i) * (v i) ^ 2) ='
    energy_new = '''(inner ℝ (WithLp.toLp 2 v : EuclideanSpace ℝ (Fin d))
        (WithLp.toLp 2 (D.mulVec v) : EuclideanSpace ℝ (Fin d))) ='''
    assert text.count(norm_old) == text.count(energy_old) == 1
    text = text.replace(norm_old, norm_new).replace(energy_old, energy_new)
    p.write_text(text)
diag = {'state': 'UNSEALED_LITERAL_METRIC_ELABORATION',
        'reason': 'Express the genuine private consumer using the actual EuclideanSpace norm and inner product, with WithLp.toLp explicit, rather than only a coordinate-sum variant. This prevents accidental use of the raw-function supremum norm. The source Euclidean energy correspondence must be proved internally.',
        'source_assumptions_or_public_producer_changed': False,
        'draft_coordinate_variant_and_actual_formation_retained': True,
        'normal_API_calls': 0, 'target_mathematical_proof_begun': False,
        'producer_signature_sha256': sha((W/'producer-signature.draft.txt').read_bytes()),
        'consumer_signature_sha256': sha((W/'consumer-signature.draft.txt').read_bytes())}
(W/'unsealed-actual-Euclidean-consumer-elaboration.json').write_text(json.dumps(diag, indent=2)+'\n')
print(json.dumps(diag))
