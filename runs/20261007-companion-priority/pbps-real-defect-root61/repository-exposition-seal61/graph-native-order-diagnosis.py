from common import *
q=J(P/'graph.freshness.negative.json'); p=J(P/'graph.after-native-adapter.input.payload.json'); rows=q['source_rows']; names=[path(x['path']).relative_to(ROOT).as_posix() for x in rows]
new=['AutoSamplingTheory.lean']+[x.relative_to(ROOT).as_posix() for x in sorted(ROOT/n for n in names if n.startswith('AutoSamplingTheory/'))]+['Tests.lean']+[x.relative_to(ROOT).as_posix() for x in sorted(ROOT/n for n in names if n.startswith('Tests/'))]+['lakefile.lean','lean-toolchain','lake-manifest.json']
assert set(new)==set(names) and len(new)==len(names)==931
h=hashlib.sha256()
for n in new:
 row=next(x for x in rows if x['path']==path(n).as_posix()); matches(row); h.update(n.encode()); h.update(b'\0'); h.update(path(n).read_bytes()); h.update(b'\0')
p['lean']=h.hexdigest(); observed=H(C(p)); expected=q['official_frozen_header']; differences=[dict(position=i,old=a,native=b) for i,(a,b) in enumerate(zip(names,new)) if a!=b]
W(P/'graph.native-WindowsPath-order.payload.json',p)
W(P/'graph.native-WindowsPath-order.diagnosis.json',dict(status='PASS_NATIVE_ORDER_EXPLAINS_READER_NEGATIVE' if observed==expected else 'NEGATIVE',actual_PID=os.getpid(),observed=observed,official=expected,native_raw_source_digest=h.hexdigest(),source_rows_count=len(new),ordering_differences=differences,exact_native_order=new,payload=pin(P/'graph.native-WindowsPath-order.payload.json'),scope='Same931 exact integration sources/raw bytes and complete226 items277 native cells; native sorted WindowsPath ordering only; no source/current graph change'))
assert observed==expected,(observed,expected)
print('NATIVE_WINDOWS_PATH_ORDER_PASS',observed,'differences',len(differences))
