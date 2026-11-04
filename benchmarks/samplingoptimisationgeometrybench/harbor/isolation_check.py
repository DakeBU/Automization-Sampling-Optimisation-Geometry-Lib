"""Runtime smoke of the declared Docker/cgroup-v2 limits, not a security proof."""
import json
import argparse
import os
from pathlib import Path


def probe():
    interfaces = sorted(p.name for p in Path('/sys/class/net').iterdir())
    memory = Path('/sys/fs/cgroup/memory.max').read_text().strip()
    cpu = Path('/sys/fs/cgroup/cpu.max').read_text().split()
    pids = Path('/sys/fs/cgroup/pids.max').read_text().strip()
    observations = {'network_interfaces': interfaces, 'memory_max': memory, 'cpu_max': cpu, 'pids_max': pids}
    print(json.dumps(observations), flush=True)
    if memory == 'max' or not 0 < int(memory) <= 256 * 1024 * 1024:
        raise RuntimeError('Expected at most 256 MiB cgroup memory')
    if cpu[0] == 'max' or not 0 < int(cpu[0]) <= int(cpu[1]):
        raise RuntimeError('Expected at most one CPU of cgroup quota')
    if interfaces != ['lo'] or pids == 'max' or not 0 < int(pids) <= 128:
        raise RuntimeError('Expected Docker network_mode:none and at most 128 processes')
    return {**observations, 'scope': 'observed Docker isolation limits; not an arbitrary Lean verifier or escape-resistance certificate'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--uid', type=int, required=True)
    args = parser.parse_args()
    if os.geteuid() != args.uid:
        raise RuntimeError('Execution user differs from the declared role')
    print(json.dumps({**probe(), 'effective_uid': os.geteuid()}))
