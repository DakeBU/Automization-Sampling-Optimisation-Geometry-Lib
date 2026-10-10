from pathlib import Path
import json,hashlib,datetime,sys
sys.stdout.reconfigure(encoding='utf-8');O=Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-source-mean-gradient-domain-sourcegraph54')
def H(b):return hashlib.sha256(b).hexdigest()
def LF(b):return b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def info(p):b=p.read_bytes();return dict(path=str(p),raw_bytes=len(b),lf_bytes=len(LF(b)),raw_sha256=H(b),lf_sha256=H(LF(b)))
def write(n,x):b=(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8');(O/n).write_bytes(b);return b
bindings=json.loads((O/'input-bindings.json').read_text(encoding='utf-8'));checks=[]
for x in bindings:
 z=x['whole'];p=Path(z['path']);b=p.read_bytes();ok=H(b)==z['raw_sha256'] and H(LF(b))==z['lf_sha256'];assert ok
 if 'selected_fragment' in x:
  f=x['selected_fragment'];v=b[f['start_utf8_byte0']:f['end_utf8_byte0_exclusive']];assert H(v)==f['fragment_raw_sha256'] and H(LF(v))==f['fragment_lf_sha256']
 checks.append(dict(path=str(p),raw_LF_exact=ok))
write('final-current-input-checks.json',{'scope':'byte bookkeeping only, not topology/theorem admission','all127_exact':True,'checks':checks,'own_compiler':'NOT_STARTED_CLOSED'})
old=(O/'lease.json').read_bytes();(O/'lease.open.snapshot.json').write_bytes(old)
cl=json.loads(old.decode('utf-8-sig'));cl.update(read='CLOSED',write='CLOSED',python='CLOSED',compiler='NOT_STARTED_CLOSED',phase='SOURCE_RECONSTRUCTION_CLOSED_AWAITING_DISTINCT_TOPOLOGY',pending=[],closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),closure='Actual lease write is final filesystem operation. Accepted root1448 StatementSeal and CLOSED independent53 verification pins bound; no implementation, compiler, claim, SAU/canonical edit or self-admission.')
cb=(json.dumps(cl,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
outputs=[info(p) for p in sorted(O.rglob('*')) if p.is_file() and p.name not in ['run.json','lease.json']]
# References to historical native runs/leases are deliberately not converted into live leases.
run={'schema':'astis-source-proof-graph-native-run54/v1','owner':'/root/gaussian_noncompact_preread_42','scope':str(O),'status':'SOURCE_GRAPH_CREATOR_CLOSED_NOT_TOPOLOGY_ADMITTED','source_first':info(O/'primary-reconstruction.before-candidate.json'),'primary_graph_before_candidate':info(O/'source-graph.primary-draft.before-candidate.json'),'graph':info(O/'source-proof-graph.json'),'contract':info(O/'source-contract.json'),'hypothesis_contract':info(O/'hypothesis-contract.json'),'candidate_LF_sha256':'19de42336148aa900917e6c77753325145d6010dfd1718c1625b2b9a8f7ce595','counts':json.loads((O/'counts.json').read_text(encoding='utf-8')),'inputs':info(O/'input-bindings.json'),'outputs':outputs,'actual_creator_closed_lease':{'path':str(O/'lease.json'),'raw_sha256':H(cb),'lf_sha256':H(LF(cb)),'read':'CLOSED','write':'CLOSED','python':'CLOSED','compiler':'NOT_STARTED_CLOSED'},'historical_source_only_receipts':info(O/'historical-source-only-receipt-bindings.json'),'root_typed_and_parent_status_only':info(O/'admission.status-only.pending-to-closed.json'),'recipes':{'raw':'SHA256 exact filebytes','LF':'CRLF->LF, then remainingCR->LF, SHA256','logical':'SHA256 of UTF8 sorted compact ensure_ascii=False JSON of whole run excluding run_sha256'},'no_compiler_proof_implementation_claim_SAU_canonical_edit':True,'creator_cannot_admit_topology':True}
logical=H(json.dumps(run,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8'));run['run_sha256']=logical;rb=write('run.json',run)
summary=dict(graph_rawLF=run['graph']['raw_sha256'],contract_rawLF=run['contract']['raw_sha256'],hypothesis_rawLF=run['hypothesis_contract']['raw_sha256'],run_rawLF=H(rb),run_logical=logical,actual_closed_lease_rawLF=H(cb),counts=run['counts'],all127_input_rawLF_exact=True,outputs=len(outputs),scope=str(O))
# LAST filesystem operation. No read/write/stat/glob/subprocess afterwards.
(O/'lease.json').write_bytes(cb)
print(json.dumps(summary,ensure_ascii=False,indent=2))
