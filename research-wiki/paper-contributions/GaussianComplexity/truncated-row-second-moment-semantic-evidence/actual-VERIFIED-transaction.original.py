from pathlib import Path
import copy
import datetime
import hashlib
import json
import os
import stat
import subprocess
import sys
import tempfile
import time

ROOT=Path('/Users/zhouhuanjian/ASTIS-GC')
HERE=Path(__file__).resolve().parent
E=ROOT/'research-wiki/paper-contributions/GaussianComplexity/truncated-row-second-moment-semantic-evidence'
LEDGER=ROOT/'runs/substantive_advances.jsonl'
CELL=ROOT/'research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-truncated-row-second-moment.json'
FRONTIERS=ROOT/'research-wiki/frontier-cells'
ADVANCE='ASTIS-SA-20261111-GaussianComplexityTruncatedRowMoment'
OWNER='huanjian_gc_20261111_truncated_row_moment'
VERIFIER='/root/radial_cov_fresh_source_42df'
HEAD='b71212eaa20fac05c23286bfd01da31f343a5d09'
CANDIDATE='86c9bb627c61955f2a47f492c59a044230536739'
PLOCAL_CARRIER='0175bc3092572c0c092346e5aa79ea3bb30b361c'
PREFLIGHT_SHA='fae6423e7875098a27e6d08da1a0e8196a356c3452642b05d1c407b51ca38e45'
DECL='AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTruncatedRowMoment.actual_truncated_row_second_moment'
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tools'))
from tools import astis_advance as advance

def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def newbytes(path,data):
    with path.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
def newjson(path,obj):newbytes(path,(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode())
def relative(path):return str(path.relative_to(ROOT))
def git(*args):
    r=subprocess.run(['git',*args],cwd=ROOT,capture_output=True)
    assert r.returncode==0,(args,r.stderr)
    return r.stdout

def frontier_hashes():
    return {relative(p):sha(p.read_bytes()) for p in sorted(FRONTIERS.rglob('*')) if stat.S_ISREG(p.lstat().st_mode)}
def replay(raw):return advance._replay_advances([json.loads(x) for x in raw.splitlines() if x.strip()])
def recursive_diff(a,b,prefix=''):
    if isinstance(a,dict) and isinstance(b,dict):
        out=[]
        for k in sorted(set(a)|set(b)):
            here=prefix+'.'+k if prefix else k
            if k not in a or k not in b:out.append(here)
            else:out.extend(recursive_diff(a[k],b[k],here))
        return out
    return [] if a==b else [prefix]

assert git('rev-parse','HEAD').decode().strip()==HEAD
assert git('status','--porcelain=v1','--untracked-files=no')==b''
pre_raw=(HERE/'immutable-preflight-original.json').read_bytes();assert sha(pre_raw)==PREFLIGHT_SHA
pre=json.loads(pre_raw);assert pre['metadata_HEAD']==HEAD and pre['normal_V_calls_performed']==0
for item in pre['source_runtime_file_checks']:assert sha((ROOT/item['path']).read_bytes())==item['sha256']
for item in pre['review_and_PLOCAL_checks']:assert sha((ROOT/item['path']).read_bytes())==item['sha256']

before_ledger=LEDGER.read_bytes();assert before_ledger==git('show',HEAD+':runs/substantive_advances.jsonl')
assert before_ledger==git('show',PLOCAL_CARRIER+':runs/substantive_advances.jsonl')
before_records=[json.loads(x) for x in before_ledger.splitlines() if x.strip()]
before_states=advance._replay_advances(before_records)
assert len(before_states)==303 and before_states[ADVANCE]['state']=='PROVED_LOCAL'
assert before_states[ADVANCE]['owner_id']==OWNER and VERIFIER!=OWNER
plocal=[x for x in before_records if x.get('advance_id')==ADVANCE and x.get('to_state')=='PROVED_LOCAL']
assert len(plocal)==1
plocal=plocal[0]
assert plocal['evidence']==json.loads((E/'actual-PROVED_LOCAL-evidence.full.json').read_bytes())
assert json.loads((E/'actual-PROVED_LOCAL-append.exact.jsonl').read_bytes())==plocal
assert before_states[ADVANCE]['latest_evidence']==plocal['evidence']
assert not [x for x in before_records if x.get('advance_id')==ADVANCE and x.get('to_state')=='VERIFIED']
foreign_before={k:sha(canon(v)) for k,v in before_states.items() if k!=ADVANCE}
assert len(foreign_before)==302
frontier_before=frontier_hashes();assert len(frontier_before)==463
older_before={k:v for k,v in frontier_before.items() if k!=relative(CELL)};assert len(older_before)==462
cell_raw=CELL.read_bytes();cell=json.loads(cell_raw)
assert cell['status']=='proved_locally' and cell['evidence']['independent_verification']==''
assert cell['owner_id']==OWNER and cell['advance_id']==ADVANCE
assert CELL.read_bytes()==git('show',HEAD+':'+relative(CELL))

# Preserve evidence already stored by the original PROVED_LOCAL append, without rewriting it.
plocal_preserved={relative(p):sha(p.read_bytes()) for p in E.glob('actual-PROVED_LOCAL-*') if p.is_file()}
assert len(plocal_preserved)>=4
newbytes(E/'actual-VERIFIED-preflight-original.json',pre_raw)
newbytes(E/'actual-VERIFIED-transaction.original.py',Path(__file__).read_bytes())

source_audit={
 'path':relative(E/'independent-source-review-original.json'),
 'sha256':'86207f4e0ddacfd449765baa82e5b2e5364eb9cf42a81b4705d707dd4ce3c74f',
 'overlay_path':relative(E/'independent-source-review-overlay.json'),
 'overlay_sha256':'a969787e220eeeb60c8476b8e35369ca63a498235e559c2af925726f88b6d82c',
 'reviewer_packet_sha256':'c7580b10335851b283623638ef1b70e025547a4ee134c481acd75c5deae81b8b',
 'publication_binding_sha256':'cc869c78be53c6197a600c399d0c9822665e9125b4c3db9a7437283903d94382',
 'verdict':'equivalent-after-elaboration',
 'scope':'Canonical Gaussian single-row Ex108 and actual deterministic single-row p12.m5 only; no original-family row transport or concentration credit.'}
native={
 'path':relative(E/'independent-native-and-static-review-original.json'),
 'sha256':'a79b9abdfed36545610d63055f3901b4a226c70ace089ee091277510ea73ca6c',
 'candidate':CANDIDATE,'manifest_sha256':'3f40392a5e737857ad07438e4a9f1f1fa41be96dfc70479a315aa03a42b63280',
 'archive_sha256':'c22c86e7ba52b7e6c00467eb1ff7629f1548628060bdd6e6cf03034661028b71',
 'native_originals_rehashed':73,'scope':'Actual isolated three-module native closure, literal certificates, standard axioms and bounded static structure. No browser/integrated-site acceptance.'}
decision={
 'kind':'Independent decision warranting one actual normal PROVED_LOCAL to VERIFIED',
 'reviewer':VERIFIER,'owner':OWNER,'advance_id':ADVANCE,
 'metadata_verified_commit':HEAD,'mathematical_native_candidate':CANDIDATE,'original_PROVED_LOCAL_carrier':PLOCAL_CARRIER,
 'source_audit':source_audit,'native_and_static_review':native,
 'final_gate_checks':pre['final_real_gate_receipts'],
 'live_reviewed_advance_gate':'Passed independently before this normal transaction; the normal API runs the real reviewed gate again.',
 'preflight':{'path':relative(E/'actual-VERIFIED-preflight-original.json'),'sha256':PREFLIGHT_SHA},
 'formalizer_API_pristine':False,'chronology_pristineness_certified':False,
 'decision':'VERIFIED is warranted for the bounded canonical-row result. Actual transition outcome is recorded separately by the normal API append and execution receipt.',
 'HOLD':pre['HOLD'],
 'independent_from_proving_worker':True,
 'no_snapshot_exports':True,'no_global_integration':True}
newjson(E/'actual-VERIFIED-independent-decision.json',decision)

payload={
 'proved_local_evidence':copy.deepcopy(plocal['evidence']),
 'proved_local_original_append':{'path':relative(E/'actual-PROVED_LOCAL-append.exact.jsonl'),'sha256':sha((E/'actual-PROVED_LOCAL-append.exact.jsonl').read_bytes()),'carrier':PLOCAL_CARRIER},
 'publication_declarations':copy.deepcopy(plocal['evidence']['publication_declarations']),
 'verifier_id':VERIFIER,'verified_commit':HEAD,'mathematical_candidate':CANDIDATE,
 'gate':{'final_real_gate_receipts':pre['final_real_gate_receipts'],'independent_native_and_static_review':native,'preflight':{'path':relative(E/'actual-VERIFIED-preflight-original.json'),'sha256':PREFLIGHT_SHA}},
 'source_audit':source_audit,
 'semantic_roundtrip_audit':{'audit_id':'ASTIS-RT-20261111-HuanjianGaussianTruncatedRowMoment','state':'source-reviewed','verdict':'equivalent-after-elaboration','source_review':'accepted','publication_binding_sha256':source_audit['publication_binding_sha256'],'reviewer_packet_sha256':source_audit['reviewer_packet_sha256']},
 'fake_closure_scan':{'source_scan':pre['source_fake_closure_scan'],'native_owned_axioms':pre['actual_owned_axioms'],'certificate_receipts':pre['native_receipts'],'allowed_axioms':['propext','Classical.choice','Quot.sound'],'actual_owned_module_index_count':3},
 'independent_decision':relative(E/'actual-VERIFIED-independent-decision.json'),
 'formalizer_API_pristine':False,'chronology_pristineness_certified':False,
 'truth_boundary':'Normal verification covers the exact canonical standard-row retained second moment and private deterministic cosine-row mean, with both matrix integrabilities, q=0, real Euclidean operator norm and standard axioms. Original joint-family transport, real desktop/mobile/public-index/graph/copy/download integration, stabilization, full-paper/full-Goal acceptance and purification remain HOLD.'}
assert payload['proved_local_evidence']==plocal['evidence']
newjson(E/'actual-VERIFIED-evidence.full.json',payload)
newjson(E/'actual-VERIFIED-hash-only-preservation-baseline.json',{
 'kind':'Hash-only preservation inventory; no own or foreign state snapshot export',
 'metadata_HEAD':HEAD,'ledger_before_sha256':sha(before_ledger),'ledger_before_bytes':len(before_ledger),
 'foreign_full_replayed_state_count':302,'foreign_full_replayed_state_sha256':foreign_before,
 'older_frontier_regular_file_count':462,'older_frontier_file_sha256':older_before,
 'original_PLOCAL_artifacts':plocal_preserved})

# O_EXCL establishes one actual attempted API call; no retries are made by this script.
newjson(E/'actual-VERIFIED-attempted.once.json',{
 'advance_id':ADVANCE,'from_state':'PROVED_LOCAL','to_state':'VERIFIED','verifier_id':VERIFIER,
 'metadata_HEAD':HEAD,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'normal_API':'tools.astis_advance.transition_advance','normal_API_call_count':1,
 'payload_sha256':sha((E/'actual-VERIFIED-evidence.full.json').read_bytes())})
assert LEDGER.read_bytes()==before_ledger and CELL.read_bytes()==cell_raw
print('NORMAL_API_CALL_BEGIN',flush=True)
start=time.monotonic()
advance.transition_advance(ADVANCE,'VERIFIED',worker_id=VERIFIER,modes=['independent-verification'],evidence=payload)
print('NORMAL_API_CALL_RETURNED',flush=True)
api_elapsed=time.monotonic()-start

after_ledger=LEDGER.read_bytes()
assert after_ledger.startswith(before_ledger)
append=after_ledger[len(before_ledger):]
assert len(append.splitlines())==1 and append.endswith(b'\n')
event=json.loads(append)
assert event['event']=='transition' and event['advance_id']==ADVANCE and event['from_state']=='PROVED_LOCAL' and event['to_state']=='VERIFIED'
assert event['worker_id']==VERIFIER and event['evidence']==payload
assert event['evidence']['proved_local_evidence']==plocal['evidence']
newbytes(E/'actual-VERIFIED-append.exact.jsonl',append)

# Change only the two pre-existing cell fields authorized for normal independent verification.
new_cell=copy.deepcopy(cell);new_cell['status']='independently_verified'
new_cell['evidence']['independent_verification']=relative(E/'actual-VERIFIED-independent-decision.json')
assert recursive_diff(cell,new_cell)==['evidence.independent_verification','status']
assert cell_raw.count(b'"status": "proved_locally"')==1
assert cell_raw.count(b'"independent_verification": ""')==1
new_raw=cell_raw.replace(b'"status": "proved_locally"',b'"status": "independently_verified"',1)
new_raw=new_raw.replace(b'"independent_verification": ""',b'"independent_verification": '+json.dumps(new_cell['evidence']['independent_verification']).encode(),1)
assert json.loads(new_raw)==new_cell
fd,tempname=tempfile.mkstemp(prefix='.normal-verification-',suffix='.tmp',dir=CELL.parent)
with os.fdopen(fd,'wb') as f:f.write(new_raw);f.flush();os.fsync(f.fileno())
os.chmod(tempname,stat.S_IMODE(CELL.stat().st_mode));os.replace(tempname,CELL)

frontier_command=[sys.executable,'-B','tools/astis_frontier_cells.py','check']
started=datetime.datetime.now(datetime.timezone.utc).isoformat();r=subprocess.run(frontier_command,cwd=ROOT,capture_output=True)
ended=datetime.datetime.now(datetime.timezone.utc).isoformat()
newbytes(E/'actual-VERIFIED-whole-frontier.stdout.log',r.stdout)
newbytes(E/'actual-VERIFIED-whole-frontier.stderr.log',r.stderr)
newjson(E/'actual-VERIFIED-whole-frontier.receipt.json',{'command':frontier_command,'cwd':str(ROOT),'started_utc':started,'ended_utc':ended,'head_before':HEAD,'head_after':git('rev-parse','HEAD').decode().strip(),'exit_code':r.returncode,'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr),'actual_registered_cell_scope':'whole live frontier directory'})

after_states=replay(after_ledger)
foreign_after={k:sha(canon(v)) for k,v in after_states.items() if k!=ADVANCE}
frontier_after=frontier_hashes();older_after={k:v for k,v in frontier_after.items() if k!=relative(CELL)}
changed_foreign=[k for k in sorted(set(foreign_before)|set(foreign_after)) if foreign_before.get(k)!=foreign_after.get(k)]
changed_older=[k for k in sorted(set(older_before)|set(older_after)) if older_before.get(k)!=older_after.get(k)]
changed_PLOCAL=[k for k,v in plocal_preserved.items() if sha((ROOT/k).read_bytes())!=v]
changed_own_fields=recursive_diff(before_states[ADVANCE],after_states[ADVANCE])
expected_own={'state','last_actor','modes','latest_evidence','updated_at'}
# Nested latest_evidence keys expand in recursive_diff; all must stay in the normal lifecycle field.
assert all(k in expected_own or k.startswith('latest_evidence.') for k in changed_own_fields)
status=git('status','--porcelain=v1','--untracked-files=no').decode()
tracked_paths=set(git('diff','--name-only').decode().splitlines())
preservation={
 'kind':'Actual normal VERIFIED transaction preservation report',
 'metadata_HEAD':HEAD,'mathematical_native_candidate':CANDIDATE,'original_PROVED_LOCAL_carrier':PLOCAL_CARRIER,
 'advance_id':ADVANCE,'verifier_id':VERIFIER,'actual_normal_API_call_count':1,'normal_API_elapsed_seconds':api_elapsed,
 'ledger':{'before_bytes':len(before_ledger),'before_sha256':sha(before_ledger),'after_bytes':len(after_ledger),'after_sha256':sha(after_ledger),'original_prefix_byte_exact':after_ledger.startswith(before_ledger),'new_append_lines':1,'new_append_sha256':sha(append),'from_state':event['from_state'],'to_state':event['to_state']},
 'original_PLOCAL_nested_evidence_equal':event['evidence']['proved_local_evidence']==plocal['evidence'],
 'original_PLOCAL_artifacts_unchanged':not changed_PLOCAL,'changed_original_PLOCAL_artifacts':changed_PLOCAL,
 'foreign_full_states':{'count_before':len(foreign_before),'count_after':len(foreign_after),'all_302_full_state_hashes_equal':foreign_before==foreign_after,'changed_ids':changed_foreign,'aggregate_before_sha256':sha(canon(foreign_before)),'aggregate_after_sha256':sha(canon(foreign_after))},
 'older_frontier_regular_files':{'count_before':len(older_before),'count_after':len(older_after),'all_462_byte_hashes_equal':older_before==older_after,'changed_paths':changed_older,'aggregate_before_sha256':sha(canon(older_before)),'aggregate_after_sha256':sha(canon(older_after))},
 'own_cell':{'path':relative(CELL),'before_sha256':sha(cell_raw),'after_sha256':sha(CELL.read_bytes()),'only_changed_fields':recursive_diff(cell,json.loads(CELL.read_bytes())),'status_after':json.loads(CELL.read_bytes())['status'],'independent_verification_after':new_cell['evidence']['independent_verification']},
 'own_advance':{'owner_unchanged':after_states[ADVANCE]['owner_id']==OWNER,'state_after':after_states[ADVANCE]['state'],'actual_verified_event_count':len([x for x in [json.loads(s) for s in after_ledger.splitlines()] if x.get('advance_id')==ADVANCE and x.get('to_state')=='VERIFIED'])},
 'tracked_diff_paths':sorted(tracked_paths),'tracked_status':status,
 'whole_frontier_check_exit_code':r.returncode,
 'snapshot_exports_performed':False,'foreign_state_content_exported':False,'global_integration_performed':False,
 'formalizer_API_pristine':False,'chronology_pristineness_certified':False,'remaining_HOLD':pre['HOLD']}
newjson(E/'actual-VERIFIED-preservation-report.json',preservation)
assert not changed_foreign and not changed_older and not changed_PLOCAL
assert foreign_before==foreign_after and older_before==older_after
assert len(frontier_after)==463 and after_states[ADVANCE]['state']=='VERIFIED'
assert after_states[ADVANCE]['owner_id']==OWNER and preservation['own_advance']['actual_verified_event_count']==1
assert tracked_paths=={'runs/substantive_advances.jsonl',relative(CELL)}
assert preservation['own_cell']['only_changed_fields']==['evidence.independent_verification','status']
assert git('rev-parse','HEAD').decode().strip()==HEAD
assert r.returncode==0,(r.stdout,r.stderr)
print(json.dumps({'actual_normal_transition':'PROVED_LOCAL -> VERIFIED','advance_id':ADVANCE,'verifier_id':VERIFIER,'metadata_HEAD':HEAD,'mathematical_candidate':CANDIDATE,'actual_normal_API_calls':1,'foreign_full_states_preserved':302,'older_frontier_regular_files_preserved':462,'own_cell_only_changed_fields':preservation['own_cell']['only_changed_fields'],'actual_whole_frontier_exit_code':r.returncode,'preservation_report_sha256':sha((E/'actual-VERIFIED-preservation-report.json').read_bytes())},indent=2),flush=True)
