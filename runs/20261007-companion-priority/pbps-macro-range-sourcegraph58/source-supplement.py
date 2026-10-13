from pathlib import Path
import json, hashlib, datetime, os, sys
BASE=Path('E:/Samplinglib/runs/20261007-companion-priority'); OUT=BASE/'pbps-macro-range-sourcegraph58'; P=BASE/'phase-pbps-gamma-preread57'
def sha(b): return hashlib.sha256(b).hexdigest()
def pin(p,b):
    lf=b.replace(b'\r\n',b'\n'); return dict(path=str(p).replace('\\','/'),bytes=len(b),raw_sha256=sha(b),lf_bytes=len(lf),lf_sha256=sha(lf))
reads=[]; writes=[]
def read(p):
    b=p.read_bytes(); reads.append(pin(p,b)); return b
def write(name,obj):
    p=OUT/name
    if isinstance(obj,dict):
        obj=dict(obj); obj['content_self_sha256']=sha(json.dumps(obj,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()); b=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
    else: b=obj
    p.write_bytes(b); receipt=pin(p,b); writes.append(receipt); return receipt
anchors=[]
for n in ['A2.E8','A2.E9']:
    raw=read(P/(n+'.raw.html')); text=read(P/(n+'.text.txt'))
    anchors.append(dict(anchor=n,source=pin(P/(n+'.raw.html'),raw),exact_raw=write(n+'.raw.snapshot.html',raw),lf=write(n+'.lf.snapshot.html',raw.replace(b'\r\n',b'\n')),formula=text.decode(),disposition='NODE',nodes=['S:T-same','S:sharp-C2'] if n=='A2.E9' else ['S:model','S:T-same']))
write('source-anchor-supplement.json',dict(actor='/root/source_graph58',status='SOURCE_ONLY_ANCHOR_PRECISION_AFTER_SEAL_NO_TOPOLOGY_CHANGE',original_graph_pin=pin(OUT/'source-proof-graph.json',read(OUT/'source-proof-graph.json')),anchors=anchors,correction='S:T-same source equation for actual conditional mean is B9; B8 defines Yplus/Yminus. Original S:T-same anchor B8/B2/C1 remains immutable; this additive source-use precision explicitly includes B9.',chronology='Original source graph was sealed from original source-only58 and primary57 source contracts. Exact raw B8/B9 reread added after accepted public headers/Test. No candidate58 existed, no node/edge/statement change, no prior CLOSED source mutation.',claim='Source anchor precision only, creator cannot validate own topology.'))
write('conceptual-mirror-audit.json',dict(actor='/root/source_graph58',status='none-found',scope='Source58 bounded exact range/centered transport/squared defect integration',reason='The mechanism is exact real isometric operator transport plus contraction-to-positive quadratic defect. No new cross-domain correspondence beyond existing source decomposition is discovered; no conceptual bridge is promoted to a formal dependency.',independently_validated=False,source_or_Lean_admission=False))
write('source-supplement-io.json',dict(actor='/root/source_graph58',python_pid=os.getpid(),python_executable=sys.executable,foreground=True,utc=datetime.datetime.utcnow().isoformat()+'Z',reads=reads,writes=writes,compiler='NOT_STARTED_CLOSED',source58_candidate_exposure=False))
print(json.dumps(dict(status='SUPPLEMENT_CLOSED',anchors=len(anchors))))
