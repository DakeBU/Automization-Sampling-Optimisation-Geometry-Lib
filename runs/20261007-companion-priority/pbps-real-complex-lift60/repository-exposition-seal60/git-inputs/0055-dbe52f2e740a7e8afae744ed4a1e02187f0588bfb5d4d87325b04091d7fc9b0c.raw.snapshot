import pathlib,json,hashlib,os,sys
ROOT=pathlib.Path('E:/Samplinglib');D=ROOT/'runs/20261007-companion-priority/pbps-real-complex-lift60/exact-science-verification';sys.path.insert(0,str(ROOT));os.chdir(ROOT)
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
from tools import astis_advance as advance
before=(D/'ledger.before-VERIFIED.exactraw.snapshot.jsonl').read_bytes();ledger=ROOT/'runs/substantive_advances.jsonl';assert ledger.read_bytes()==before
e=json.loads((D/'verification-evidence.json').read_bytes());identity='/root/whole_math52/exact-science60'
advance.transition_advance('ASTIS-SA-20261008-PBPSPositiveDefectComplexLift','VERIFIED',worker_id=identity,evidence=e)
after=ledger.read_bytes();assert after.startswith(before) and len(after)>len(before);records=[json.loads(x) for x in after[len(before):].splitlines() if x.strip()];assert len(records)==1
record=records[0];assert record['worker_id']==identity and record['to_state']=='VERIFIED' and record['evidence']['verified_commit']=='0a77416f5ec38702c46ec1358966b9dd4846c8d3'
state=advance.current_advances();assert state['ASTIS-SA-20261008-PBPSPositiveDefectComplexLift']['state']=='VERIFIED';assert [k for k,v in state.items() if v.get('state')=='STABILIZING']==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
q=dict(actual_PID=os.getpid(),status='INDEPENDENT_VERIFIED_TRANSITION_READBACK_PASS',record=record,ledger_before=pin(D/'ledger.before-VERIFIED.exactraw.snapshot.jsonl'),ledger_after=pin(ledger),prefix_bytes_preserved=True,append_record_count=1,sole_STABILIZING='ASTIS-SA-20261005-SPHMCImplementedPhaseKernel',canonical_cells_or_proofs_mutated=False)
(D/'transition.json').write_bytes((json.dumps(q,ensure_ascii=False,indent=2)+'\n').encode());print(json.dumps(dict(status='VERIFIED',actual_PID=os.getpid(),checked_commit=e['verified_commit'])),flush=True)
