import json,hashlib,os,datetime
from pathlib import Path
R=Path('E:/Samplinglib');T=R/'runs/20261007-companion-priority/pbps-macroscopic-centered-range58';B=T/'source-review58';B.mkdir(parents=True,exist_ok=True)
def h(b):return hashlib.sha256(b).hexdigest()
def rec(p):
    b=Path(p).read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=str(p).replace('\\','/'),raw_bytes=len(b),raw_sha256=h(b),lf_bytes=len(l),lf_sha256=h(l))
def write(n,o):(B/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lease=T/'source.review.lease.json';raw=lease.read_bytes();write('lease.open.json',dict(actor='/root/statement_topology58',status='OPEN',pid=os.getpid(),compiler='NOT_STARTED_CLOSED',time=datetime.datetime.now(datetime.timezone.utc).isoformat()));(B/'source.review.lease.OPEN.exactraw.snapshot.json').write_bytes(raw)
l=json.loads(raw.decode('utf-8'));assert l['status']=='OPEN' and len(l['input_artifacts'])==101
(B/'inputs').mkdir(exist_ok=True);reads=[]
for i,r in enumerate(l['input_artifacts']):
    p=R/r['path'];got=rec(p);assert got['raw_bytes']==r['bytes'] and got['raw_sha256']==r['raw_sha256'] and got['lf_sha256']==r['lf_sha256'],r['path']
    a=B/'inputs'/('%03d.exactraw.snapshot'%i);f=B/'inputs'/('%03d.crlf-to-lf.snapshot'%i);b=p.read_bytes();a.write_bytes(b);f.write_bytes(b.replace(b'\r\n',b'\n'));reads.append(dict(actual_input=got,exactraw_snapshot=rec(a),crlf_to_lf_snapshot=rec(f),content_read_scope='Byte receipt only for old audit/control/preproof seal; no old semantic verdict or whole-math review read.'))
P=R/'runs/20261007-companion-priority/pbps-macro-range-preproof-review58'
supplemental=[]
for p in [P/'independent-source-reconstruction.json',P/'primary.exactraw.snapshot.html',P/'A2.SS1.raw.html',P/'A2.SS2.raw.html',P/'A3.SS1.raw.html',P/'A4.SS1.raw.html',R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Function/FactorsThrough.lean',R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Function/LpSeminorm/Basic.lean',R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Function/ConditionalExpectation/AEMeasurable.lean',R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Function/ConditionalExpectation/CondexpL2.lean',R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Tilted.lean']:
    supplemental.append(rec(p))
assert rec(P/'primary.exactraw.snapshot.html')['raw_sha256']=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
write('input.manifest.json',dict(schema_version=1,actor='/root/statement_topology58',root_lease_snapshot=rec(B/'source.review.lease.OPEN.exactraw.snapshot.json'),inputs=reads,supplemental_readonly_inputs=supplemental,root101_all_actual_raw_lf_match=True,root101_no_recursive_provider_tree_copy=True,process_pid=os.getpid(),created=datetime.datetime.now(datetime.timezone.utc).isoformat()))
print(json.dumps(dict(pid=os.getpid(),root_inputs=len(reads),supplemental_inputs=len(supplemental),manifest=rec(B/'input.manifest.json'))))
