"""Standalone read-only whole-owned verifier; never writes or imports local modules."""
import argparse, collections, ctypes, hashlib, json, os, sys
from pathlib import Path
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path('E:/Samplinglib')
OWN=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(o):return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def check(r):
    p=ROOT/r['path'];b=p.read_bytes();assert len(b)==r['RAW_bytes'] and sha(b)==r['RAW_sha256'],r['path']
    assert sha(b.replace(b'\r\n',b'\n').replace(b'\r',b'\n'))==r['LF_sha256'],r['path']
def alive(pid):
    if os.name=='nt':
        k=ctypes.windll.kernel32;k.OpenProcess.restype=ctypes.c_void_p
        h=k.OpenProcess(0x1000,False,pid)
        if not h:return False
        c=ctypes.c_ulong();ok=k.GetExitCodeProcess(ctypes.c_void_p(h),ctypes.byref(c));k.CloseHandle(ctypes.c_void_p(h))
        return bool(ok and c.value==259)
    try:os.kill(pid,0);return True
    except ProcessLookupError:return False
def main():
    args=argparse.ArgumentParser();args.add_argument('--observed-close-exit',type=int,required=True);a=args.parse_args()
    assert a.observed_close_exit==0,'the caller must supply the actual completed exec_command EXIT'
    lpath=OWN/'lease.final.json';lease=load(lpath)
    assert lease['status']=='CLOSED_LAST' and lease['prohibit_further_writes']
    assert sha(canon({k:v for k,v in lease.items() if k!='lease_sha256'}))==lease['lease_sha256']
    actual={p.relative_to(ROOT).as_posix() for p in OWN.rglob('*') if p.is_file() and p!=lpath}
    bound={r['path'] for r in lease['files']};assert actual==bound and len(bound)==lease['file_count']
    for r in lease['files']:check(r)
    assert all(lpath.stat().st_mtime_ns >= (ROOT/r['path']).stat().st_mtime_ns for r in lease['files'])
    manifest=load(ROOT/lease['whole_owned_manifest']['path'])
    assert sha(canon({k:v for k,v in manifest.items() if k!='manifest_sha256'}))==manifest['manifest_sha256']
    assert {r['path'] for r in manifest['files']}==actual-{lease['whole_owned_manifest']['path']}
    assert manifest['file_count']==len(manifest['files'])
    for r in manifest['files']:check(r)
    run=load(OWN/'source.0.run.json');assert sha(canon({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==lease['native_source_run_sha256']
    assert run['actual_EXIT']==0 and not run['source_admission_ready']
    payload=load(OWN/'complete-named-review-decision-input-payload.json')
    assert sha(canon({k:v for k,v in payload.items() if k!='whole_logical_run_sha256'}))==payload['whole_logical_run_sha256']==lease['whole_logical_run_sha256']
    names={'source.0.run.json','source.0.decision.json','source.0.review.json','source.0.input-manifest.json','source.0.admission-fields.json'}
    assert set(payload['named_complete_RAW_payloads'])==names and payload['named_complete_RAW_payload_count']==5
    for name,p in payload['named_complete_RAW_payloads'].items():
        b=p['complete_RAW_UTF8'].encode();assert b==(OWN/name).read_bytes();assert sha(b)==p['RAW']['RAW_sha256'] and len(b)==p['RAW']['RAW_bytes']
    for mf in ['source.0.input-manifest.json','overlay75.input-manifest.json']:
        v=load(OWN/mf)
        for r in v['inputs']:
            check(r['RAW_snapshot']);check(r['LF_snapshot'])
            raw=(ROOT/r['RAW_snapshot']['path']).read_bytes();lf=(ROOT/r['LF_snapshot']['path']).read_bytes()
            assert raw.replace(b'\r\n',b'\n').replace(b'\r',b'\n')==lf
            assert r['origin']['RAW_sha256']==r['RAW_snapshot']['RAW_sha256']
    review=load(OWN/'source.0.review.json');decision=load(OWN/'source.0.decision.json');admission=load(OWN/'source.0.admission-fields.json')
    assert review['status']==decision['status']==admission['status']=='SUPPLEMENTAL_SOURCE_REVIEW_NOT_ANTI_ANCHORED'
    assert admission['audit_fields'] is None and admission['cell_source_proof_coverage'] is None and admission['publication_source_proof_coverage'] is None
    assert len(review['source_items'])==137 and len(review['source_nodes'])==32 and len(review['source_edges'])==67
    assert collections.Counter(x['source_item']['classification'] for x in review['source_items'])=={'NODE':77,'EXCLUDED':60}
    assert len(review['semantic_slots'])==7 and len(review['definition_audit'])==8 and len(review['conclusion_groups'])==10 and len(review['formula_BODY_blocks'])==9
    assert review['repairs']==[] and review['counts']['mathematical_blocking_deltas']==0
    assert decision['review_run_sha256']==run['run_sha256'] and decision['reviewer_packet_sha256']==run['official_packet_sha256']
    overlay=load(OWN/'overlay75.decision.json');orun=load(OWN/'overlay75.run.json')
    assert sha(canon({k:v for k,v in overlay.items() if k!='decision_sha256'}))==overlay['decision_sha256']
    assert sha(canon({k:v for k,v in orun.items() if k!='run_sha256'}))==orun['run_sha256']
    assert overlay['status']=='ACCEPTED_EXACT_THREE_FIELD_METADATA_OVERLAY_ONLY' and overlay['field_count']==3 and overlay['files']==2
    assert not overlay['canonical_applied_by_reviewer'] and not overlay['source_admission_granted']
    dead=[lease['final_writer_PID']]+[r['PID'] for r in lease['observed_completed_writers']]
    assert all(not alive(p) for p in dead),'review or closure writer still alive'
    for writer in lease['observed_completed_writers']:
        assert writer['EXIT']==0
        check(writer['terminal'])
    # Purely read-only PASS goes to stdout. The CLOSED directory is never reopened.
    print(json.dumps({'status':'READONLY_PASS','verifier_PID':os.getpid(),'observed_final_writer_PID':lease['final_writer_PID'],'observed_final_writer_EXIT':a.observed_close_exit,'all_writer_PIDs_terminated':dead,'whole_owned_file_count_including_lease':len(actual)+1,'lease_RAW_sha256':sha(lpath.read_bytes()),'native_run_sha256':run['run_sha256'],'source_run_RAW_sha256':sha((OWN/'source.0.run.json').read_bytes()),'complete_payload_RAW_sha256':sha((OWN/'complete-named-review-decision-input-payload.json').read_bytes()),'whole_logical_run_sha256':payload['whole_logical_run_sha256'],'overlay_decision_RAW_sha256':sha((OWN/'overlay75.decision.json').read_bytes()),'source_status':review['status'],'source_admission_ready':False,'overlay_ready_for_exact_adoption':True,'writes_performed':0},ensure_ascii=False))
if __name__=='__main__':main()
