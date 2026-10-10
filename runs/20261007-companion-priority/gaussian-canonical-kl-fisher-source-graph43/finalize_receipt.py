from pathlib import Path
import json,hashlib,datetime
D=Path(__file__).resolve().parent
def dump(o):return (json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def sha(b):return hashlib.sha256(b).hexdigest()
old=(D/'sourcegraph-run.json').read_bytes()
(D/'sourcegraph-run.initial-receipt.raw.snapshot.json').write_bytes(old)
lease=json.loads((D/'lease.open.json').read_text(encoding='utf-8-sig'))
lease['all_read_write_python_operations_within_open_lease']=False
lease['chronology_clarification']='All source/API reads and graph authoring occurred OPEN. First receipt routine closed this lease before reading output hashes/writing final receipt. Those finalization operations are disclosed; finalization.lease.json now separately covers corrected receipt and closes as last filesystem operation.'
(D/'lease.open.json').write_bytes(dump(lease))
finpath=D/'finalization.lease.json'
finraw=finpath.read_bytes()
(D/'finalization.lease.initial.raw.snapshot.json').write_bytes(finraw)
fin=json.loads(finraw.decode('utf-8-sig'));assert fin['state']=='OPEN'
fin.update(state='CLOSED',closed_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_close_is_final_filesystem_operation=True)
finalbytes=dump(fin)
(D/'leases.closed.json').write_bytes(dump({'status':'ALL_REAL_LEASES_CLOSED','lease_files':['lease.open.json','finalization.lease.json'],'chronology':'Source lease closes after mathematical authoring. Separate finalization lease covers receipt correction; predicted CLOSED bytes are hashed and its actual closure is the final filesystem operation.'}))
outputs=[]
for p in sorted(D.iterdir()):
    if p.is_file() and p.name!='sourcegraph-run.json':
        raw=finalbytes if p.name=='finalization.lease.json' else p.read_bytes()
        outputs.append({'path':p.name,'raw_sha256':sha(raw),'lf_sha256':sha(raw.replace(b'\r\n',b'\n')),'bytes':len(raw)})
run=json.loads(old.decode('utf-8'));run['output_binding']=outputs
run['lease_chronology']='Corrected two actual CLOSED leases; source authoring OPEN, receipt finalization separately OPEN and actual final close after receipt serialization. Initial receipt snapshot preserved.'
run['run_closed_at_utc']=fin['closed_at_utc']
runbytes=dump(run)
(D/'sourcegraph-run.json').write_bytes(runbytes)
print('sourcegraph-run.json '+sha(runbytes))
finpath.write_bytes(finalbytes)
