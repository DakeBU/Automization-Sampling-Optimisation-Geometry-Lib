from pathlib import Path
import json,hashlib,datetime
R=Path('runs/20261007-companion-priority/gaussian-clt-entropy-preread')
def s(b):return hashlib.sha256(b).hexdigest()
def d(p):
 b=p.read_bytes();return {'path':p.as_posix(),'raw_sha256':s(b),'lf_sha256':s(b.replace(b'\r\n',b'\n')),'bytes':len(b)}
def w(p,x):p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
old=json.loads((R/'run.json').read_text(encoding='utf-8'));drifts=[]
for r in old['evidence_artifacts']:
 now=d(Path(r['path']))
 if now['raw_sha256']!=r['raw_sha256']:drifts.append({'before':r,'after':now})
assert len(drifts)==1 and drifts[0]['before']['path']==(R/'audit.log').as_posix()
w(R/'run-closure-reconciliation.json',{'status':'closed-manifest-reconciled','diagnostic':'Author process inventoried its own redirected log while still empty. Original manifest/lease retained; new closed manifest binds final actual log. No mathematical/source/API input or packet changes.','changed_active_log':drifts,'original_manifest':d(R/'run.json'),'original_lease':d(R/'lease.json'),'source_detail_packet':d(R/'source-detail-packet.json')})
rows=[d(p) for p in sorted(R.iterdir()) if p.is_file() and p.name not in ['run.closed.json','lease.closed.json']]
w(R/'run.closed.json',{'status':'CLOSED','evidence_artifacts':rows,'manifest_sha256':s(json.dumps(rows,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()),'inputs_read_only':True,'compiler_started':False,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
w(R/'lease.closed.json',{'status':'CLOSED','compiler':'NOT_REQUESTED/CLOSED','Python':'CLOSED on final process exit','read':'CLOSED','write':'CLOSED','run':d(R/'run.closed.json'),'packet':d(R/'source-detail-packet.json'),'canonical_edits':False})
print(json.dumps({'run':d(R/'run.closed.json'),'packet':d(R/'source-detail-packet.json'),'lease':d(R/'lease.closed.json'),'all_leases':'CLOSED'}))
