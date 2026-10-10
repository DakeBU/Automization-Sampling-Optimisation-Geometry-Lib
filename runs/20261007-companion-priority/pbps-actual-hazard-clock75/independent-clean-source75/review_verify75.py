import hashlib
import json
import os
import pathlib
import re
import subprocess
import time
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[4]
OWN = pathlib.Path(__file__).resolve().parent
R75 = OWN.parent


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode('utf-8')


def write_json(name, value):
    (OWN / name).write_bytes((json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))


def main():
    freeze = json.loads((R75 / 'source-review.clean.freeze75.json').read_text(encoding='utf-8'))
    receipts = []
    listed = freeze['inputs'] + [{'path': (R75 / 'source-review.clean.freeze75.json').relative_to(ROOT).as_posix()}]
    for i, item in enumerate(listed, 1):
        path = ROOT / item['path']
        raw = path.read_bytes()
        lf = raw.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
        for key, actual in [('RAW_bytes', len(raw)), ('RAW_sha256', sha(raw)), ('LF_sha256', sha(lf))]:
            if key in item:
                assert item[key] == actual, (path, key)
        snapshot = OWN / 'clean-inputs' / f'{i:02d}.{path.name}.RAW'
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        snapshot.write_bytes(raw)
        receipts.append({'path': item['path'], 'snapshot': snapshot.relative_to(ROOT).as_posix(),
                         'RAW_bytes': len(raw), 'RAW_sha256': sha(raw), 'LF_sha256': sha(lf)})
    packet = json.loads((R75 / 'source-review.clean.packet.json').read_text(encoding='utf-8'))
    packet_no_hash = {k: v for k, v in packet.items() if k != 'packet_sha256'}
    assert sha(canonical(packet_no_hash)) == packet['packet_sha256']
    assert sha(packet['lean']['statement'].encode('utf-8')) == packet['lean']['statement_sha256']
    assert sha(packet['source']['original_text'].encode('utf-8')) == packet['source']['text_sha256']
    assert sha(packet['blind_reconstruction']['text'].encode('utf-8')) == packet['blind_reconstruction']['text_sha256']
    lean = ROOT / packet['lean']['file']
    module = lean.read_bytes()
    assert module.decode('utf-8') == packet['candidate_publication_context']['current_lean_module']
    assert sha(module) == packet['candidate_publication_context']['file']
    lines = module.splitlines(keepends=True)
    assert len(lines) == 396
    lesson_steps = packet['candidate_publication_context']['lesson']['steps']
    assert len(lesson_steps) == 9
    regions = []
    for step in lesson_steps:
        region = step['lean_source_region']
        exact = b''.join(lines[region['start_line'] - 1:region['end_line']])
        assert sha(exact) == region['exact_code_raw_sha256']
        assert exact.decode('utf-8') == step['lean']
        regions.append({'title': step['title'], **region, 'full_exact_body_slice_verified': True})
    imap = json.loads((R75 / 'implementation-source-map75.json').read_text(encoding='utf-8'))
    baseline = json.loads((ROOT / 'runs/20261007-companion-priority/pbps-clock-preproof75/independent-source-baseline75/source-proof-graph75.json').read_text(encoding='utf-8'))
    assert {n['source_node'] for n in imap['nodes']} == {n['id'] for n in baseline['nodes']}
    assert len(imap['source_gap_ids']) == 13
    for node in imap['nodes']:
        for region in node['BODY_regions']:
            exact = b''.join(lines[region['start_line'] - 1:region['end_line']])
            assert sha(exact) == region['exact_code_raw_sha256']
    scan_patterns = [r'\bsorry\b', r'\badmit\b', r'(?m)^\s*(?:private\s+)?axiom\s', r'Prop\s*:=\s*True', r':=\s*trivial\b']
    fake_closures = [pat for pat in scan_patterns if re.search(pat, module.decode('utf-8'))]
    assert not fake_closures
    check = OWN / 'full-module-axiom-check75.lean'
    check.write_bytes(module + b'\n#print axioms AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHazardClock.actual_integrated_hazard_clock_laws\n')
    command = ['lake', 'env', 'lean', check.relative_to(ROOT).as_posix()]
    started = datetime.now(timezone.utc).isoformat()
    with (OWN / 'focused-lean75.stdout.RAW.txt').open('wb') as out, (OWN / 'focused-lean75.stderr.RAW.txt').open('wb') as err:
        proc = subprocess.Popen(command, cwd=str(ROOT), stdout=out, stderr=err)
        print(json.dumps({'foreground_lean_PID': proc.pid, 'runner_PID': os.getpid(), 'command': command}), flush=True)
        code = proc.wait()
    terminal = {'command': command, 'actual_PID': proc.pid, 'actual_EXIT': code,
                'parent_PID': os.getpid(), 'started_utc': started,
                'finished_utc': datetime.now(timezone.utc).isoformat(),
                'stdout_path': (OWN / 'focused-lean75.stdout.RAW.txt').relative_to(ROOT).as_posix(),
                'stderr_path': (OWN / 'focused-lean75.stderr.RAW.txt').relative_to(ROOT).as_posix(),
                'source_equivalence': 'Exact pinned whole module bytes plus a final print-axioms command; no source proof modification.'}
    report = {'schema': 'pbps75-clean-source-review-mechanical-verification/v1',
              'actor': '/root/independent_clean_source75', 'runner_PID': os.getpid(),
              'inputs': receipts, 'canonical_packet_sha256': packet['packet_sha256'],
              'publication_binding_sha256': packet['publication_binding_sha256'],
              'full_module_lines': len(lines), 'six_callers': ['hα', 'hαβ', 'hV', 'hH', 'hη', 'hβη'],
              'literal_let_definitions': ['c', 'Φ', 'rate', 'H', 'C', 'Λ', 'τ', 'W'],
              'conclusion_groups': 10, 'lesson_BODY_steps': regions,
              'source_nodes_mapped': 32, 'source_gap_ids': imap['source_gap_ids'],
              'all_map_BODY_hashes_verified': True, 'fake_closure_scan_patterns': scan_patterns,
              'fake_closure_matches': fake_closures, 'terminal': terminal,
              'semantic_verdict_inferred_from_compilation': False}
    write_json('mechanical-verification75.json', report)
    print(json.dumps({k: v for k, v in report.items() if k not in ['inputs', 'lesson_BODY_steps']}, ensure_ascii=False, indent=2))
    print((OWN / 'focused-lean75.stdout.RAW.txt').read_text(encoding='utf-8'))
    print((OWN / 'focused-lean75.stderr.RAW.txt').read_text(encoding='utf-8'))
    if code:
        raise SystemExit(code)


if __name__ == '__main__':
    main()
