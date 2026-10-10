from pathlib import Path
import datetime, hashlib, json, os, subprocess

root = Path.cwd()
pre = Path('runs/20261007-companion-priority/pbps-harmonic-flow-preproof73')
out = pre / 'header-typecheck73'
assert not out.exists()
out.mkdir()
header = pre / 'header73.proposed.lean'
b = header.read_bytes()
split = b.index(b'\ntheorem actual_harmonic_flow_laws')
probe_bytes = b[:split] + b'\n#check @actual_harmonic_flow_statement\nend\nend AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow\n'
probe = root / '.astis/pbps-harmonic73/header73-probe.lean'
assert not probe.exists()
probe.write_bytes(probe_bytes)
(out / 'executed-probe.exactraw.txt').write_bytes(probe_bytes)
(out / 'header.exactraw.txt').write_bytes(b)
env = dict(os.environ, PYTHONUTF8='1')
env.pop('ELAN_TOOLCHAIN', None)
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
try:
    with (out / 'stdout.log').open('wb') as stdout, (out / 'stderr.log').open('wb') as stderr:
        child = subprocess.Popen(['lake', 'env', 'lean', str(probe)], cwd=root, env=env, stdout=stdout, stderr=stderr)
        print(json.dumps(dict(status='RUNNING_SIGNATURE_ELABORATION_ONLY', actual_PID=child.pid)), flush=True)
        code = child.wait()
finally:
    assert probe.read_bytes() == probe_bytes
    probe.unlink()
assert header.read_bytes() == b
record = dict(status='HEADER_TYPECHECK_ONLY' if code == 0 else 'HEADER_ELABORATION_FAILED_NO_PROOF_SEARCH', actual_root_PID=os.getpid(), actual_foreground_PID=child.pid, started_utc=started, terminal_closed=True, exit_code=code, header_RAW_sha256=hashlib.sha256(b).hexdigest(), temporary_probe_removed=True, private_Prop_is_target_specification_not_proof=True, production_writes=False, statement_sealed=False, theorem_proved=False, source_graph_admitted=False, Goal_complete=False)
(out / 'receipt.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf8', newline='\n')
print(json.dumps(record))
print((out / 'stdout.log').read_text(encoding='utf8')[-4500:])
print((out / 'stderr.log').read_text(encoding='utf8')[-1000:])
raise SystemExit(code)
