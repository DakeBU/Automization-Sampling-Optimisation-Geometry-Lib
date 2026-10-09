from pathlib import Path
import ctypes
import hashlib
import json
import os
import sys

OWN = Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-b4-perturbation-preproof72/independent-header-math72')
def sha(raw):
    return hashlib.sha256(raw).hexdigest()
def load(name):
    return json.loads((OWN / name).read_bytes().decode('utf-8'))

closed = load('CLOSED_LAST.json')
manifest = load('owned-manifest72.json')
assert closed['status'] == 'CLOSED'
assert sha((OWN / 'owned-manifest72.json').read_bytes()) == closed['manifest_raw_sha256']
assert sorted(p.name for p in OWN.iterdir() if p.is_file()) == manifest['closed_directory_exact_file_set']
for item in manifest['files']:
    raw = (OWN / item['path']).read_bytes()
    assert len(raw) == item['bytes'] and sha(raw) == item['raw_sha256'], item['path']
    raw.decode('utf-8')
run = load('run72.json')
recorded = run.pop('run_sha256')
logical_raw = json.dumps(run, ensure_ascii=False, sort_keys=True,
                         separators=(',', ':'), allow_nan=False).encode('utf-8')
assert sha(logical_raw) == recorded == closed['run_sha256']
assert run['writer_pid'] == closed['writer_pid'] == manifest['writer_pid']
source_checks = []
for item in load('inputs72.json')['inputs']:
    raw = (OWN / item['snapshot']).read_bytes()
    assert sha(raw) == item['raw_sha256']
    assert sha(raw.replace(b'\r\n', b'\n')) == item['crlf_to_lf_only_sha256']
    assert Path(item['source_absolute_path']).read_bytes() == raw, item['source_absolute_path']
    source_checks.append(item['role'])
kernel = ctypes.WinDLL('kernel32', use_last_error=True)
kernel.OpenProcess.argtypes = [ctypes.c_uint32, ctypes.c_int, ctypes.c_uint32]
kernel.OpenProcess.restype = ctypes.c_void_p
handle = kernel.OpenProcess(0x1000, False, closed['writer_pid'])
writer_terminated = handle is None
if handle:
    exit_code = ctypes.c_uint32()
    kernel.GetExitCodeProcess.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint32)]
    kernel.GetExitCodeProcess.restype = ctypes.c_int
    assert kernel.GetExitCodeProcess(handle, ctypes.byref(exit_code))
    kernel.CloseHandle.argtypes = [ctypes.c_void_p]
    kernel.CloseHandle(handle)
    writer_terminated = exit_code.value != 259
assert writer_terminated, 'writer still active'
close_mtime = (OWN / 'CLOSED_LAST.json').stat().st_mtime_ns
assert all(p.stat().st_mtime_ns <= close_mtime for p in OWN.iterdir() if p.is_file())
sys.stdout.reconfigure(encoding='utf-8')
print(json.dumps({'readonly_verifier_pid': os.getpid(), 'writer_pid': closed['writer_pid'],
                  'writer_terminated': True, 'wholelogical_remove_only_top_run_sha256': True,
                  'owned_manifest_and_last_write_valid': True, 'exact_raw_and_lf_only_inputs': source_checks,
                  'run_sha256': recorded, 'verification': 'PASS', 'exit_contract': 0}, ensure_ascii=True))
sys.exit(0)
