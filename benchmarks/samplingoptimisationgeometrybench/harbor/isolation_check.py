"""Runtime smoke of the declared Docker/cgroup-v2 limits, not a security proof."""
import json
import argparse
import errno
import os
from pathlib import Path
import socket


def probe():
    interfaces = sorted(p.name for p in Path('/sys/class/net').iterdir())
    memory = Path('/sys/fs/cgroup/memory.max').read_text().strip()
    cpu = Path('/sys/fs/cgroup/cpu.max').read_text().split()
    observations = {'network_interfaces': interfaces, 'memory_max': memory, 'cpu_max': cpu}
    print(json.dumps(observations), flush=True)
    if memory == 'max' or not 0 < int(memory) <= 256 * 1024 * 1024:
        raise RuntimeError('Expected at most 256 MiB cgroup memory')
    if cpu[0] == 'max' or not 0 < int(cpu[0]) <= int(cpu[1]):
        raise RuntimeError('Expected at most one CPU of cgroup quota')
    # Harbor 0.25 implements no-network with a deny-all egress sidecar, not
    # necessarily Docker's network_mode:none. An eth0 interface is not a leak.
    denied = []
    for address in [('1.1.1.1', 443), ('8.8.8.8', 53)]:
        try:
            with socket.create_connection(address, timeout=1):
                raise RuntimeError('Unexpected external TCP connection')
        except OSError as exc:
            if not isinstance(exc, TimeoutError) and exc.errno not in {
                    errno.ENETUNREACH, errno.EHOSTUNREACH, errno.EACCES, errno.EPERM, errno.ETIMEDOUT}:
                raise RuntimeError('Inconclusive network observation') from exc
            denied.append({'destination': list(address), 'observation': type(exc).__name__})
    return {**observations, 'external_tcp_denials': denied,
            'scope': 'sampled external TCP denials plus configured Harbor deny-all; not exhaustive network or escape verification'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--uid', type=int, required=True)
    args = parser.parse_args()
    if os.geteuid() != args.uid:
        raise RuntimeError('Execution user differs from the declared role')
    print(json.dumps({**probe(), 'effective_uid': os.geteuid()}))
