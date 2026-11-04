"""Trusted root hook: bound declared answer bytes BEFORE Harbor transfers them."""
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bench_bounded_io import InputRejected, MAX_BYTES, MAX_RECEIPT_BYTES, read_bounded

POLICY = 'bounded-answer-before-transfer-v1'
REJECTIONS = {'symlink', 'not-regular', 'too-large', 'changed-during-read', 'missing', 'input-io-error'}


def capture(path):
    reason = None
    try:
        raw = read_bounded(path)
    except InputRejected as exc:
        raw, reason = b'', str(exc)
    except FileNotFoundError:
        raw, reason = b'', 'missing'
    except OSError:
        raw, reason = b'', 'input-io-error'
    receipt = {'schema_version': 1, 'policy': POLICY,
               'status': 'captured' if reason is None else 'rejected',
               'reason': reason, 'raw_bytes': len(raw),
               'raw_sha256': hashlib.sha256(raw).hexdigest()}
    encoded = (json.dumps(receipt, sort_keys=True) + '\n').encode('utf-8')
    if len(raw) > MAX_BYTES or len(encoded) > MAX_RECEIPT_BYTES:
        raise RuntimeError('Collector output exceeded its own fixed bounds')
    return raw, encoded


def main():
    if os.name != 'posix' or os.geteuid() != 0 or not hasattr(os, 'O_NOFOLLOW'):
        raise RuntimeError('Trusted collection requires the Linux root role and no-follow semantics')
    target = Path('/handoff')
    info = target.lstat()
    if not stat.S_ISDIR(info.st_mode) or info.st_uid != 0 or stat.S_IMODE(info.st_mode) != 0o700:
        raise RuntimeError('Handoff directory must be root-owned mode 0700')
    raw, receipt = capture(Path('/output/answer.json'))
    # Only the trusted hook can write this root-owned directory. A failed hook
    # leaves a missing/inconsistent receipt, which is an infrastructure failure.
    for name, content in [('answer.bin', raw), ('collection.json', receipt)]:
        destination = target / name
        with destination.open('xb') as stream:
            stream.write(content)
        destination.chmod(0o600)
    print(json.dumps({'collector_uid': os.geteuid(), 'answer_bytes': len(raw),
                      'receipt_bytes': len(receipt), 'scope': 'declared answer channel only'}))


if __name__ == '__main__':
    main()
