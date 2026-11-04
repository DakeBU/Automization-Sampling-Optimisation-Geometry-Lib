"""Separate-container graph verifier: parse data only; reuse the canonical scorer."""
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sog_bench_curriculum import grade_graph

MAX_BYTES = 65536


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON key')
        result[key] = value
    return result


def invalid_constant(value):
    raise ValueError('Non-finite JSON number')


def read_answer(path):
    if Path(path).is_symlink():
        raise ValueError('Symlink answers are not accepted')
    fd = os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0))
    with os.fdopen(fd, 'rb') as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_BYTES:
            raise ValueError('Expected a regular JSON file of at most 65536 bytes')
        raw = stream.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError('Answer exceeds byte limit')
    row = json.loads(raw.decode('utf-8'), object_pairs_hook=unique_object, parse_constant=invalid_constant)
    if not isinstance(row, dict) or set(row) != {'id', 'binding_sha256', 'attempt', 'answer'}:
        raise ValueError('Expected the exact response envelope')
    if not isinstance(row['id'], str) or not isinstance(row['binding_sha256'], str) or type(row['attempt']) is not int:
        raise ValueError('Invalid response identity, binding or attempt type')
    return row, hashlib.sha256(raw).hexdigest()


def assess(question, path):
    """Malformed/missing answers score zero; unexpected grader bugs propagate."""
    try:
        row, digest = read_answer(path)
        result = grade_graph([question], [row])
        return {'reward': result['points'], 'response_sha256': digest, 'result': result}
    except (ValueError, OSError, UnicodeError, RecursionError) as exc:
        return {'reward': 0, 'answer_error': type(exc).__name__,
                'scope': 'rejected graph response; not a Lean or mathematical judgment'}


def main():
    question = json.loads(Path('/tests/question.json').read_text(encoding='utf-8'))
    report = assess(question, Path('/output/answer.json'))
    logs = Path('/logs/verifier')
    logs.mkdir(parents=True, exist_ok=True)
    (logs / 'assessment.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    (logs / 'reward.txt').write_text(str(report['reward']) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
