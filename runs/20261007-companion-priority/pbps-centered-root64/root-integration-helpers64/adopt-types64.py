from pathlib import Path
import hashlib, json, os

r = Path('runs/20261007-companion-priority/pbps-centered-root-preproof64')
load = lambda p: json.loads(Path(p).read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
rows = []
for i, label, pid in [(0, 'named-type0-v1', 13232), (1, 'named-type1-v2', 33448)]:
    d = r / label; rec = load(d / 'receipt.json')
    assert rec['actual_foreground_pid'] == pid and rec['terminal_closed'] and rec['exit_code'] == 1
    for key in ['stdout', 'stderr']:
        q = rec[key]; b = Path(q['path']).read_bytes()
        assert sha(b) == q['raw_sha256'] and len(b) == q['bytes']
    messages = [json.loads(s) for s in (d / 'stdout.log').read_text(encoding='utf-8').splitlines() if s.strip()]
    errors = [x for x in messages if x.get('severity') == 'error']
    assert len(errors) == 1 and errors[0]['data'] == 'Unknown identifier `noProof64_TYPE_ONLY_INTENTIONALLY_UNDEFINED`'
    assert errors[0]['kind'] == 'lean.unknownIdentifier._namedError'
    assert (d / 'stderr.log').read_bytes() == b''
    for name in ['header'+str(i)+'.lean', 'type-only'+str(i)+'.lean']:
        p = (r / name).resolve(); q = next(q for q in rec['inputs'] if Path(q['path']).resolve() == p)
        assert sha(p.read_bytes()) == q['raw_sha256'], name
    rows.append(dict(header=(r / ('header'+str(i)+'.lean')).as_posix(),
        header_RAW_sha256=sha((r / ('header'+str(i)+'.lean')).read_bytes()),
        actual_type_diagnostic_receipt=(d / 'receipt.json').as_posix(),
        actual_pid=pid, expected_exit_code=1, only_error=errors[0], theorem_proved=False))
negative = load(r / 'named-type1-v1/receipt.json')
assert negative['actual_foreground_pid'] == 36476 and negative['exit_code'] == 1
assert load(r / 'type-instance-repair64/diagnosis.json')['public_mathematical_binders_unchanged']
out = r / 'root.named-types64.adoption.json'; assert not out.exists()
out.write_text(json.dumps(dict(
    status='TWO_FULL_NAMED64_TYPES_ELABORATED_NO_PROOF_NO_STATEMENT_SEAL',
    actual_adopter_pid=os.getpid(), rows=rows,
    original_TYPE1_inferred_instance_failure=(r / 'named-type1-v1/receipt.json').as_posix(),
    internal_derived_HP0_instances_only=True, no_public_math_premise_added=True,
    no_production_Lean_or_closed_native_artifact_changed=True,
    no_Lean_proof_or_science_credit=True, independent_header_review_pending=True,
    proof_search_started=False, Statement_Seal=False, SAU_claim=False),
    ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
print('PASS both full named64 types elaborate; exactly intentional undefined-body errors (not proofs). Original HP0 instance failure retained; no Statement Seal/SAU/proof credit.')
