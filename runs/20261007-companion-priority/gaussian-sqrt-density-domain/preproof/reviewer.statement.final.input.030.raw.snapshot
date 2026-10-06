from pathlib import Path
import hashlib, json, re, subprocess

scratch = Path('.astis/gaussian-domain32')
proposal = json.loads((scratch / 'root.statement-proposal.json').read_text(encoding='utf-8'))
checks = []
for target in proposal['targets']:
    signature = target['signature']
    b = Path(signature['path']).read_bytes()
    assert hashlib.sha256(b).hexdigest() == signature['raw_sha256']
    s = b.replace(b'\r\n', b'\n').decode('utf-8')
    assert hashlib.sha256(s.encode()).hexdigest() == signature['lf_sha256']
    body = re.sub(r'^theorem\s+\w+\s*\n', '', s, count=1)
    binders, conclusion = body.rsplit(' :\n', 1)
    checks.append('#check (∀ ' + binders.lstrip() + ',\n' + conclusion.rstrip() + '\n)')
probe = scratch / 'StatementTypeProbe.lean'
assert not probe.exists()
probe.write_text('import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGOPositionFisher\nimport AutoSamplingTheory.TechnicalLemmas.Measure.IsotropicGaussianDensity\nopen MeasureTheory InnerProductSpace ProbabilityTheory\nopen scoped RealInnerProductSpace NNReal\nnoncomputable section\n\n' + '\n\n'.join(checks) + '\n', encoding='utf-8')
log = scratch / 'root.statement-typecheck.0.log'
assert not log.exists()
with log.open('w', encoding='utf-8') as out:
    result = subprocess.run(['lake', 'env', 'lean', str(probe)], stdout=out, stderr=subprocess.STDOUT)
record = {
    'schema_version': 1, 'status': 'type-elaboration-pass' if result.returncode == 0 else 'type-elaboration-failed',
    'exit_code': result.returncode, 'command': ['lake', 'env', 'lean', str(probe)],
    'exact_input_signatures': [t['signature'] for t in proposal['targets']],
    'probe_path': probe.as_posix(), 'probe_raw_sha256': hashlib.sha256(probe.read_bytes()).hexdigest(),
    'log_path': log.as_posix(), 'log_raw_sha256': hashlib.sha256(log.read_bytes()).hexdigest(),
    'transformation': 'Remove only theorem/name header and change final declaration colon to forall comma. No theorem body or placeholder introduced.',
    'theorem_bodies_or_proof_search': False, 'production_edits': False, 'compiler_lease': 'CLOSED',
}
(scratch / 'root.statement-typecheck.0.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(record['status'], flush=True)
raise SystemExit(result.returncode)
