from pathlib import Path
import hashlib, json
W = Path(__file__).parent
sha = lambda b: hashlib.sha256(b).hexdigest()
records = []
for n in ['StatementFormation.lean', 'producer-signature.draft.txt', 'consumer-signature.draft.txt']:
    p = W/n
    old = p.read_bytes()
    out = W/(n+'.attempt1.raw.txt')
    with out.open('xb') as f:
        f.write(old)
    new = old.decode().replace('λ', 'eigenvalue').encode()
    assert new != old
    p.write_bytes(new)
    records.append({'file': n, 'original_sha256': sha(old), 'corrected_sha256': sha(new)})
diag = {'failure_class': 'PARSER_OR_COMPILER',
        'reason': 'Unsealed temporary Prop formation used reserved Lean lambda token λ as a local identifier. Actual Lean exit1 is retained; its subsequent #check output does not establish valid formation.',
        'repair': 'Alpha-rename only that unsealed local eigenvalue identifier; preserve mathematical objects, hypotheses and conclusions. Both actual original drafts and probe retained before mutation.',
        'mathematical_refutation_or_added_assumption': False, 'normal_API_calls': 0, 'files': records}
(W/'statement-formation-reserved-identifier-diagnostic.json').write_text(json.dumps(diag, indent=2)+'\n')
print(json.dumps(diag))
