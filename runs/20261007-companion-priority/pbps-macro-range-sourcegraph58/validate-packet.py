from pathlib import Path
import json, hashlib, os, sys, datetime, time, ctypes
BASE=Path('E:/Samplinglib'); OUT=BASE/'runs/20261007-companion-priority/pbps-macro-range-sourcegraph58'; reads=[]; started=time.time()
def sha(b): return hashlib.sha256(b).hexdigest()
def pin(p,b):
    lf=b.replace(b'\r\n',b'\n'); return dict(path=str(p).replace('\\','/'),bytes=len(b),raw_sha256=sha(b),lf_bytes=len(lf),lf_sha256=sha(lf))
def read(p):
    b=p.read_bytes(); reads.append(pin(p,b)); return b
def load(p): return json.loads(read(p).decode('utf-8-sig'))
def native(d):
    s=dict(d); expected=s.pop('content_self_sha256'); actual=sha(json.dumps(s,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()); assert actual==expected; return actual
checked=[]
for p in sorted(OUT.glob('*.json')):
    if p.name.startswith('inherited57.') or p.name in ['run.json','complete.json','lease.json','lease.open.json','validator.json','output-manifest.json']: continue
    d=load(p); checked.append(dict(path=str(p),native_complete_self_digest=native(d)))
strict=[]
for item in load(OUT/'pin-validation.json')['checks']:
    if item['status']=='historical-control-not-live-rechecked': continue
    expected=item.get('expected') if item['status']=='strict-pin-pass' else item['immutable_snapshot']
    actual=pin(Path(expected['path']),read(Path(expected['path']))); assert actual==expected,(expected,actual); strict.append(actual)
# Verify exact input/output receipts recorded by own creation stages. No process/tool gate or math conclusion inferred.
for name in ['source-first-run.json','finish-io.json','source-supplement-io.json','signature-index-io.json','consumer-signature-index-io.json']:
    d=load(OUT/name)
    for key in ['reads','writes']:
        for expected in d[key]:
            actual=pin(Path(expected['path']),read(Path(expected['path']))); assert actual==expected,(name,key,expected,actual)
for name in ['signature-indexed-binder-overlay.json','signature-indexed-test-consumer-overlay.json']:
    d=load(OUT/name)
    for key in (['signature_pin','generic_signature_pin','proposal_pin'] if name.startswith('signature-indexed-binder') else ['signature','proposal']):
        expected=d[key]; actual=pin(Path(expected['path']),read(Path(expected['path']))); assert actual==expected
# All inherited606 rows have byte-faithful correspondence with fixed raw primary; exclusions remain untouched.
inherited=load(OUT/'inherited-source606-inventory.json'); primary=read(BASE/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html')
for row in inherited['coverage']+inherited['citation_coverage']:
    piece=primary[row['primary_start_utf8_byte']:row['primary_end_utf8_byte_exclusive']]
    assert sha(piece)==row['raw_sha256']; assert sha(piece.replace(b'\r\n',b'\n'))==row['lf_sha256']
for row in load(OUT/'source-coverage.json')['regions']:
    p=OUT/'inputs'/(row['source_file']+'.exactraw.snapshot'); b=read(p); piece=b[row['source_span_byte_start']:row['source_span_byte_end']]; assert sha(piece)==row['source_span_raw_sha256']
resource=dict(pid=os.getpid(),cpu_user_seconds=os.times().user,cpu_system_seconds=os.times().system,wall_seconds=time.time()-started,read_operations=len(reads),read_bytes=sum(x['bytes'] for x in reads),peak_working_set_bytes=None)
if os.name=='nt':
    class PMC(ctypes.Structure):
        _fields_=[('cb',ctypes.c_ulong),('PageFaultCount',ctypes.c_ulong),('PeakWorkingSetSize',ctypes.c_size_t),('WorkingSetSize',ctypes.c_size_t),('QuotaPeakPagedPoolUsage',ctypes.c_size_t),('QuotaPagedPoolUsage',ctypes.c_size_t),('QuotaPeakNonPagedPoolUsage',ctypes.c_size_t),('QuotaNonPagedPoolUsage',ctypes.c_size_t),('PagefileUsage',ctypes.c_size_t),('PeakPagefileUsage',ctypes.c_size_t)]
    pmc=PMC(); pmc.cb=ctypes.sizeof(PMC); kernel=ctypes.WinDLL('kernel32'); kernel.GetCurrentProcess.restype=ctypes.c_void_p
    psapi=ctypes.WinDLL('psapi'); psapi.GetProcessMemoryInfo.argtypes=[ctypes.c_void_p,ctypes.POINTER(PMC),ctypes.c_ulong]
    ok=psapi.GetProcessMemoryInfo(kernel.GetCurrentProcess(),ctypes.byref(pmc),pmc.cb)
    resource['memory_query_actual_success']=bool(ok)
    if ok: resource['peak_working_set_bytes']=pmc.PeakWorkingSetSize; resource['working_set_bytes']=pmc.WorkingSetSize
d=dict(actor='/root/source_graph58',status='BOOKKEEPING_AND_SOURCE_SPAN_PIN_VALIDATION_PASS',independent_source_topology_review=False,math_or_Lean_validation=False,compiler='NOT_STARTED_CLOSED',native_complete_digest_rule='Whole object excluding exactly top-level content_self_sha256; no other field/payload elision.',native_json_checks=checked,actual_rechecked_source58_strict_and_temporal_pins=len(strict),inherited606_raw_span_checks=606,own365_source_span_checks=365,reads=reads,resource=resource,finished_utc=datetime.datetime.utcnow().isoformat()+'Z')
d['content_self_sha256']=sha(json.dumps(d,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()); p=OUT/'validator.json'; p.write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps(dict(status=d['status'],native_json=len(checked),strict_pin_checks=len(strict),raw_source_span_checks=606+365,pid=os.getpid(),compiler='NOT_STARTED_CLOSED')))
