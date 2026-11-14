#!/usr/bin/env python3
"""Data-custody assembler only: no Git, normal APIs, proof checks, or state writes."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
N = ROOT / '.astis/semantic-neutral-20261114/bernstein_exp_native_72c4'
F = ROOT / '.astis/semantic-neutral-20261114/bernstein_exp_fresh_61a9'
E = ROOT / 'research-wiki/technical-lemmas/matrix-bernstein-exponential-semantic-evidence'
MATH = '0ff1e2227b8e5a45a6a73906582ef042bd0d73ff'
READER = '9a8b163f4753a1329dbc0435c1e7f810f729c349'
REVIEWER = '/root/bernstein_exp_fresh_61a9'
P_SHA = '7fc1996495b439c1b0aa53a3e69b6b4547952a42ee5f721834b6a1092430f6cc'
T_SHA = '66bcf7750e8a70f6d69cea4bb08513f78364c3c3583862c119ffe4ff9cc9d883'


def require(ok, message):
    if not ok:
        raise ValueError(message)


class Custody:
    def __init__(self):
        self.frozen = {}

    def path(self, path, base=ROOT):
        p = Path(path)
        require(not any('.private.' in part for part in p.parts), 'private artifact forbidden')
        if not p.is_absolute():
            p = (ROOT if p.parts and p.parts[0] in {
                '.astis', 'research-wiki', 'AutoSamplingTheory', 'Tests', 'website'
            } else base) / p
        p = p.resolve()
        require(p.is_relative_to(ROOT), 'artifact escaped repository: ' + str(p))
        require(not any('.private.' in part for part in p.parts), 'private target forbidden')
        return p

    def ref(self, path, expected=None, base=ROOT):
        p = self.path(path, base)
        raw = p.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        require(expected is None or expected == digest, 'SHA256 mismatch: ' + str(p))
        key = str(p.relative_to(ROOT))
        require(key not in self.frozen or self.frozen[key] == digest, 'conflicting frozen path')
        self.frozen[key] = digest
        return {'path': key, 'sha256': digest}

    def load(self, path, expected=None, base=ROOT):
        ref = self.ref(path, expected, base)
        return ref, json.loads((ROOT / ref['path']).read_bytes())

    def cited(self, obj, base=ROOT):
        """Freeze explicit file+hash citations, never infer a verdict from them."""
        refs = []
        if isinstance(obj, dict):
            for key, value in obj.items():
                digest = obj.get('sha256') if key in ('path', 'file') else None
                for suffix in ('_path', '_file', '_artifact'):
                    if key.endswith(suffix):
                        digest = obj.get(key[:-len(suffix)] + '_sha256', digest)
                if isinstance(value, str) and isinstance(digest, str) and re.fullmatch('[0-9a-f]{64}', digest):
                    # Installed browser provenance stays inside its genuine
                    # receipt; do not reopen external executable/app files.
                    p = Path(value)
                    if not p.is_absolute() or p.is_relative_to(ROOT):
                        refs.append(self.ref(value, digest, base))
                refs.extend(self.cited(value, base))
        elif isinstance(obj, list):
            for value in obj:
                refs.extend(self.cited(value, base))
        return refs

    def browser(self, report_path, receipt_path, contract_path, wrapper_path,
                status, exit_code, png_count=None, expected_report=None, graph_only=False):
        rr, report = self.load(report_path, expected_report, N)
        pr, receipt = self.load(receipt_path, base=N)
        cr, contract = self.load(contract_path, base=N)
        wr = self.ref(wrapper_path, base=N)
        require(report['status'] == receipt['actual_checks']['status'] == status, 'browser status mismatch')
        require(receipt['exit_code'] == exit_code and receipt['exception'] is None, 'process exit/exception mismatch')
        require(report['browser_started'] is True, 'browser never started')
        require(report['reader_commit'] == contract['reader_commit'] == READER, 'reader commit mismatch')
        require(report['mathematical_candidate'] == contract['mathematical_candidate'] == MATH, 'math candidate mismatch')
        require(report['contract_sha256'] == receipt['contract_sha256'] == cr['sha256'], 'contract binding mismatch')
        require(report['wrapper_sha256'] == receipt['wrapper_sha256'] == contract['wrapper_sha256'] == wr['sha256'], 'wrapper binding mismatch')
        require(self.ref(receipt['actual_checks']['path'], receipt['actual_checks']['sha256'], N) == rr, 'actual report binding mismatch')
        require(receipt['actual_chrome']['runtime_browser_version'], 'missing actual browser version')
        streams = {}
        for name in ('stdout', 'stderr'):
            s = receipt[name]
            streams[name] = self.ref(s['path'], s['sha256'], N)
            require((ROOT / streams[name]['path']).stat().st_size == s['bytes'], 'raw stream byte count mismatch')
        pngs = [self.ref(x['path'], x['sha256'], N) for x in report['screenshots']]
        require(pngs and len({x['path'] for x in pngs}) == len(pngs), 'missing/duplicate screenshots')
        require(png_count is None or len(pngs) == png_count, 'screenshot count mismatch')
        require(receipt['actual_checks']['screenshot_count'] == len(pngs), 'receipt screenshot count mismatch')
        if graph_only:
            require(report['schema'] == 'root-primary-graph-zoom-result-v1', 'unexpected graph report schema')
            require(contract['schema'] == 'root-primary-graph-only-real-zoom-contract-v1', 'unexpected graph contract schema')
            require(report['scope'] == 'GRAPH_ONLY; no full P/T reader rerun; no data/CSS/layout mutation', 'graph scope mismatch')
            require(report['real_UI_actions'] and contract['prohibited_mutations'], 'missing graph UI/mutation contract')
        else:
            require(report['production_changes_applied'] is False, 'production change reported')
        if status == 'PASS':
            require(all(x['pass'] for x in report['checks']), 'failed actual check')
            if not graph_only:
                require(not report['javascript_errors'] and not report['blocked_external_requests'], 'browser errors/blocked requests')
        self.cited(contract.get('owned_inputs', []), N)
        return {'actual_checks': rr, 'process_receipt': pr, 'contract': cr, 'wrapper': wr,
                'checker_exit': exit_code, 'raw_streams': streams, 'screenshots': pngs}


def assemble(args):
    c = Custody()
    native, _ = c.load(N / 'native-mathematics-report.v1.json', 'b65ea8f10740af2fad395ef448c9d0e87f92dc5646a1b3a313e5efdda356bc69')
    parents, _ = c.load(N / 'actual-canonical-parent-supplement.v1.json', 'ce0c6fc6de645fec235b3b69a66a59baa58433d7c195a76f516f024ba2bef624')
    original = c.browser('root-primary-browser-output-v3/original/actual-checks.json',
        'root-primary-browser-process-v3/original/process-receipt.json', 'root-primary-browser-contract.v3.json',
        'primary_browser_wrapper_v3.py', 'FAIL', 1, 38, '2c59e330141418ae36b6377b6e7aa21fc431b1e4cd8af7cea8793188656f4ee5')
    candidate = c.browser('root-primary-browser-output-v5/candidate/actual-checks.json',
        'root-primary-browser-process-v5/candidate/process-receipt.json', 'root-primary-browser-contract.v5.json',
        'primary_browser_wrapper_v5.py', 'PASS', 0, 50, '22c4b9b5435891139431095aa1b3e997b44954f7fa3bccb6fb22de6f01b786b7')
    prior_candidate = c.browser('root-primary-browser-output-v3/candidate/actual-checks.json',
        'root-primary-browser-process-v3/candidate/process-receipt.json', 'root-primary-browser-contract.v3.json',
        'primary_browser_wrapper_v3.py', 'FAIL', 1, 38, 'f36c3d9a4917682160d70c7c6e70fb980f98454c52dc664349a7bdd3fcedb3db')
    env_ref, env = c.load(N / 'root-primary-browser-output-v2/original/actual-checks.json')
    require(env['status'] == 'FAIL' and not env['screenshots'] and env.get('browser_started') is not True,
            'v2 must remain an environment failure without a reader verdict')
    for name in ['browser-v2-ENV_BLOCKED-preservation.json', 'browser-v3-evidence-preservation.json']:
        c.ref(N / name)

    source = {}
    for key, path in {'P_audit': ROOT / 'research-wiki/semantic-roundtrip/audits/huanjian-matrix-bernstein-exponential.json',
                      'T_audit': E / 'private-consumer-audit.source-reviewed.v2.json'}.items():
        source[key], audit = c.load(path)
        require(audit['source_review']['state'] == 'accepted', 'source audit not accepted')
        require(audit['source_review']['reviewer'] == REVIEWER, 'source reviewer identity mismatch')
        c.cited(audit['independent_original_overlay'])
    for key, name in [('P', 'P.audit-overlay.v2.json'), ('T', 'T.audit-overlay.v2.json'),
                      ('run', 'source-reader-review.run.v2.json'), ('manifest', 'source-reader-review.manifest.v2.json'),
                      ('P_freeze', 'P-whole-module-code-freeze.v1.receipt.json'),
                      ('PT_freeze', 'PT-whole-module-code-freeze.v1.receipt.json'),
                      ('PT_judgment', 'PT-whole-module-code-judgment.v1.json'),
                      ('raw_freeze', 'rawfreeze.receipt.json'), ('originals', 'chosen-originals.manifest.v1.json')]:
        source[key], obj = c.load(F / name)
        # Whole-code judgment prose cites background library files. Its exported
        # archive is the bounded custody surface; never traverse library paths.
        if key != 'PT_judgment':
            c.cited(obj, F)
        if key == 'originals':
            for member in obj['members']:
                c.ref(member['original_path'], member['sha256'], F)
        exported = E / 'source-review/bernstein_exp_fresh_61a9' / name
        if exported.is_file():
            c.ref(exported, source[key]['sha256'])
    for key, path, digest in [
        ('exact_P', ROOT / 'AutoSamplingTheory/TechnicalLemmas/Probability/MatrixBernsteinExponential.lean', P_SHA),
        ('exact_T', ROOT / 'Tests/GaussianComplexityBernsteinMgf.lean', T_SHA),
        ('seal', ROOT / 'research-wiki/technical-lemmas/matrix-bernstein-exponential-statement-seal.json', 'c3103a9e8d08fea6c83f35201fce953af4dd93e88a1a3d7d647fc4deaaddeb7a'),
        ('lesson', ROOT / 'website/content/declaration_lessons/huanjian-matrix-bernstein-exponential.json', 'f745771917dc9e69985f03e1616d56a3688f23989b4528b8d4f6a3441bb9e6b8'),
        ('publication', ROOT / 'website/content/publications/huanjian-matrix-bernstein-exponential.json', '71772041637f66f4cae69737a4c65e64422203e8a58ee69212970e8532340903'),
        ('source_map', E / 'source-lean-map.authored-v1.json', '50b95e0bb6b4d4bfac5557e82d1e4f7188c1467d791c9765c0cc6b531ebce15a')]:
        source[key] = c.ref(path, digest)
    c.ref(E / 'local-math-candidate.json')

    review_ref, review = c.load(args.runtime_review)
    review_inputs = c.cited(review)
    graph_args = [args.graph_report, args.graph_receipt, args.graph_contract, args.graph_wrapper]
    require(not any(graph_args) or all(graph_args), 'all four graph artifact arguments are required together')
    graph = None
    if all(graph_args):
        graph = c.browser(*graph_args, 'PASS', 0, 12,
            'c313cbb71ead4e2486deb54957797e5c348170c061fc01c685375124dfb6e89c', graph_only=True)
        require(graph['contract']['sha256'] == 'e2397ec7db5845440235d20120fe978319a9222aedd70aea9b7b6338c4042f26', 'graph contract changed')
        require(graph['wrapper']['sha256'] == '5fc8895cdae381ee61e8db16ca7a58580ca2481cc925c27bd4043fdbbd1859e2', 'graph wrapper changed')
    if args.check_custody_only:
        return {'mode': 'CUSTODY_ONLY_NO_ACCEPTANCE_OR_PL_PAYLOAD', 'frozen_file_count': len(c.frozen),
                'main_screenshot_counts': [38, 50], 'reviewer_accepted': review.get('accepted_isolated_candidate'),
                'graph_supplement_supplied': graph is not None}

    require(review['reviewer'] == REVIEWER, 'must use the original independent runtime reviewer')
    require(review['accepted_isolated_candidate'] is True, 'final original reviewer has not explicitly accepted candidate')
    require(review['immutable_reader_commit'] == READER and review['mathematical_candidate'] == MATH, 'final review commit mismatch')
    require(review['production_changes_applied'] is False, 'final review reports production changes')
    require(not review.get('graph_zoom_pending'), 'final review still has a graph zoom blocker')
    for label, bundle in [('original', original), ('isolated_candidate', candidate)]:
        r = review['actual_report_refs'][label]
        require(c.ref(r['path'], r['sha256']) == bundle['actual_checks'], 'review/main report mismatch')
    # This chain already has a graph-zoom hold: its final closure must bind actual supplemental evidence.
    require(graph is not None, 'actual graph zoom supplement is mandatory for this pending review chain')
    require(any(x['sha256'] == graph['actual_checks']['sha256'] for x in review_inputs),
            'final reviewer did not hash-bind actual graph supplement report')
    reader = {'actual_reader_candidate_commit': READER, 'original': original, 'isolated_candidate': candidate,
        'graph_zoom_supplement': graph, 'independent_runtime_review': {'artifact': review_ref,
        'accepted': review['accepted_isolated_candidate']}, 'production_shared_files_changed': False,
        'exact_full_source_folds': {'P_lines': 148, 'T_lines': 240, 'folds': 7},
        'scope_boundary': 'Original v3 FAIL and isolated C2 v5 PASS plus graph supplement independently accepted; production/shared integration and purification held.',
        'graph_boundary': 'Actual isolated graph runtime and original independent review bound; no production graph admission.',
        'preserved_predecessors': {'candidate_v3_font_FAIL': prior_candidate,
                                  'original_v2_ENV_BLOCKED_without_reader_verdict': env_ref}}
    return {'metadata_commit': args.metadata_commit, 'native_math': native, 'native_actual_parents': parents,
            'source_evidence': source, 'reader': reader,
            'frozen_inputs': [{'path': p, 'sha256': h} for p, h in sorted(c.frozen.items())]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime-review', required=True, help='Actual final original reviewer JSON, never a synthesized acceptance wrapper')
    parser.add_argument('--metadata-commit', required=True, help='Exact supplied metadata commit; no Git call is made')
    defaults = {'report': N / 'root-primary-graph-zoom-output/candidate/actual-checks.json',
                'receipt': N / 'root-primary-graph-zoom-process/candidate/process-receipt.json',
                'contract': N / 'root-primary-graph-zoom-contract.json',
                'wrapper': N / 'primary_graph_zoom_supplement.py'}
    for name, path in defaults.items():
        parser.add_argument('--graph-' + name, default=str(path))
    parser.add_argument('--check-custody-only', action='store_true', help='Read/hash evidence and report counts; never emit normal PL payload')
    parser.add_argument('--output', default=str(OUT / 'normal-PL-inputs.json'))
    args = parser.parse_args()
    require(re.fullmatch('[0-9a-f]{40}', args.metadata_commit), 'metadata_commit must be an exact 40-hex commit')
    output = Path(args.output).resolve()
    require(output.parent == OUT, 'output must stay in the assigned neutral directory')
    result = assemble(args)
    if args.check_custody_only:
        print(json.dumps(result))
        return
    raw = (json.dumps(result, ensure_ascii=False, indent=2) + '\n').encode()
    with output.open('xb') as handle:
        handle.write(raw)
    print(json.dumps({'assembled': str(output.relative_to(ROOT)), 'sha256': hashlib.sha256(raw).hexdigest(),
                      'frozen_file_count': len(result['frozen_inputs'])}))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, OSError) as error:
        print('BLOCKED: ' + str(error), file=sys.stderr)
        sys.exit(2)
