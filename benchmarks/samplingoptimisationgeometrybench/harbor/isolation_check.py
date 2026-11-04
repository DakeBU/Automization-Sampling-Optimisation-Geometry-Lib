"""Runtime smoke of the declared Docker/cgroup-v2 limits, not a security proof."""
import json
from pathlib import Path


def probe():
    interfaces = sorted(p.name for p in Path('/sys/class/net').iterdir())
    memory = Path('/sys/fs/cgroup/memory.max').read_text().strip()
    cpu = Path('/sys/fs/cgroup/cpu.max').read_text().split()
    if interfaces != ['lo'] or memory == 'max' or not 0 < int(memory) <= 256 * 1024 * 1024:
        raise RuntimeError('Expected loopback-only network and at most 256 MiB cgroup memory')
    if cpu[0] == 'max' or not 0 < int(cpu[0]) <= int(cpu[1]):
        raise RuntimeError('Expected at most one CPU of cgroup quota')
    return {'network_interfaces': interfaces, 'memory_max': memory, 'cpu_max': cpu,
            'scope': 'observed Docker limits only; no arbitrary Lean verifier or escape-resistance certificate'}


if __name__ == '__main__':
    print(json.dumps(probe()))
