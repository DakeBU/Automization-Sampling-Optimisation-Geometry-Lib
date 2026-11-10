"""Separate-container graph verifier: parse data only; reuse the canonical scorer."""
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sog_bench_curriculum import bind_graph_submissions, grade_graph
from bench_bounded_io import InputRejected, MAX_BYTES, MAX_RECEIPT_BYTES, read_bounded
from collect_answer import POLICY, REJECTIONS


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON key')
        result[key] = value
    return result


def invalid_constant(value):
    raise ValueError('Non-finite JSON number')


def parse_answer(raw):
    row = json.loads(raw.decode('utf-8'), object_pairs_hook=unique_object, parse_constant=invalid_constant)
    if not isinstance(row, dict) or set(row) != {'id', 'prompt_sha256', 'attempt', 'answer'}:
        raise ValueError('Expected the exact response envelope')
    if not isinstance(row['id'], str) or not isinstance(row['prompt_sha256'], str) or type(row['attempt']) is not int:
        raise ValueError('Invalid response identity, binding or attempt type')
    return row, hashlib.sha256(raw).hexdigest()


def read_answer(path):
    return parse_answer(read_bounded(path))


def assess_bytes(question, raw):
    """Grade the exact captured bytes, never a second file read."""
    try:
        row, digest = parse_answer(raw)
        result = grade_graph([question], bind_graph_submissions([question], [row]))
        return {'reward': result['points'], 'response_sha256': digest, 'result': result}
    except (ValueError, UnicodeError, RecursionError) as exc:
        return {'reward': 0, 'answer_error': type(exc).__name__,
                'scope': 'rejected graph response; not a Lean or mathematical judgment'}


def assess(question, path):
    """Local raw-file compatibility API; unknown I/O errors remain unscored."""
    try:
        raw = read_bounded(path)
    except (InputRejected, FileNotFoundError) as exc:
        return {'reward': 0, 'answer_error': type(exc).__name__,
                'scope': 'rejected graph response; not a Lean or mathematical judgment'}
    except OSError as exc:
        raise RuntimeError('Unscored input I/O failure') from exc
    return assess_bytes(question, raw)


def assess_collected(question, raw_path, receipt_path):
    """A missing/corrupt trusted receipt is infrastructure failure, not zero credit."""
    try:
        receipt = json.loads(read_bounded(receipt_path, MAX_RECEIPT_BYTES),
                             object_pairs_hook=unique_object, parse_constant=invalid_constant)
        raw = read_bounded(raw_path)
        expected = {'schema_version', 'policy', 'status', 'reason', 'raw_bytes', 'raw_sha256'}
        if (not isinstance(receipt, dict) or set(receipt) != expected
                or type(receipt['schema_version']) is not int or receipt['schema_version'] != 1
                or receipt['policy'] != POLICY or type(receipt['raw_bytes']) is not int
                or receipt['raw_bytes'] != len(raw) or receipt['raw_sha256'] != hashlib.sha256(raw).hexdigest()):
            raise ValueError('Invalid collection receipt')
        if receipt['status'] == 'rejected':
            if raw != b'' or not isinstance(receipt['reason'], str) or receipt['reason'] not in REJECTIONS:
                raise ValueError('Invalid rejected collection')
            return {'reward': 0, 'collection': receipt,
                    'scope': 'rejected answer artifact; not a mathematical or Lean judgment'}
        if receipt['status'] != 'captured' or receipt['reason'] is not None:
            raise ValueError('Invalid captured collection')
    except (ValueError, OSError, UnicodeError, RecursionError, TypeError) as exc:
        raise RuntimeError('Missing, corrupt or inconsistent trusted collection') from exc
    return {**assess_bytes(question, raw), 'collection': receipt}


def main():
    question = json.loads(Path('/tests/question.json').read_text(encoding='utf-8'))
    report = assess_collected(question, Path('/handoff/answer.bin'), Path('/handoff/collection.json'))
    logs = Path('/logs/verifier')
    logs.mkdir(parents=True, exist_ok=True)
    (logs / 'assessment.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    (logs / 'reward.txt').write_text(str(report['reward']) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
