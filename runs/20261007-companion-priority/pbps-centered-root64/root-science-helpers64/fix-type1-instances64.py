from pathlib import Path
import hashlib, json

r = Path('runs/20261007-companion-priority/pbps-centered-root-preproof64')
out = r / 'type-instance-repair64'; out.mkdir(exist_ok=False)
paths = [r / 'header1.lean', r / 'type-only1.lean', r / 'header-candidate64.json']
sha = lambda b: hashlib.sha256(b).hexdigest()
before = []
for i, p in enumerate(paths):
    b = p.read_bytes(); snap = out / (str(i) + '.exactraw.snapshot')
    snap.write_bytes(b); before.append(dict(path=p.as_posix(), raw_sha256=sha(b), snapshot=snap.as_posix()))
anchor = '                let HP0 := (innerSL ℝ qP).ker\n'
extra = '''                letI : NormedAddCommGroup HP0 := HP0.normedAddCommGroup
                letI : InnerProductSpace ℝ HP0 := HP0.innerProductSpace
'''
for p in paths[:2]:
    s = p.read_text(encoding='utf-8'); assert s.count(anchor) == 1
    p.write_text(s.replace(anchor, anchor + extra), encoding='utf-8', newline='\n')
q = json.loads(paths[2].read_bytes())
for row in q['headers']:
    p = Path(row['path']); b = p.read_bytes()
    row.update(bytes=len(b), raw_sha256=sha(b), lf_sha256=sha(b))
q['type_diagnosis'] = 'Initial nested HP0 CLM subtraction positivity exposed incoherent inferred subtype norm/module instances; select the derived HP0 normed/inner-product instances internally. No public mathematical premise or gamma/domain/conclusion changed.'
paths[2].write_text(json.dumps(q, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
(out / 'diagnosis.json').write_text(json.dumps(dict(
    status='TYPE_INSTANCE_ALIGNMENT_ONLY_NO_PROOF_SEARCH_NO_SEAL', before=before,
    exact_inserted_derived_instances=extra, public_mathematical_binders_unchanged=True,
    original_failure='named-type1-v1 actual36476 EXIT1; HP0 subtraction .IsPositive type mismatch',
    parent63_production_or_native_artifacts_mutated=False), ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
print('Prepared coherent derived HP0 instances only; retained exact negative TYPE1/header evidence. Candidate remains unproved/unsealed.')
