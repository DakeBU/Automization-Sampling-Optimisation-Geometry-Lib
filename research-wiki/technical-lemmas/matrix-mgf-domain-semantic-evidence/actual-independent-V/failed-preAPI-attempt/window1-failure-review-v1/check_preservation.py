"""Read-only post-failure guards. Never invokes the normal transition or either action driver."""
import sys
from pathlib import Path
OUT=Path(__file__).resolve().parent;OWN=OUT.parent
sys.path.insert(0,str(OWN))
from verification_common import *

def main():
    auth=OWN/'window1.ROOT-authorization.v1.json';a=validate_authorization(auth,'a3e7256f834cb1cc540bb89ea1d5ed175506d75572243d0beeab171d8a2c2215','NORMAL_PROOF_V_ONCE')
    d=PRIVATE/'window1-before';araw=(d/'advance-ledger.exact.jsonl').read_bytes();draw=(d/'discovery-ledger.exact.jsonl').read_bytes();ar,dr,adv,disc=replay(araw,draw)
    before={'state':read(d/'full-guard-map.private.json'),'araw':araw,'draw':draw,'records':ar,'adv':adv,'disc':disc,'index':(d/'index.exact').read_bytes()}
    after=snapshot('window1-failure-after',a);guards=postguards(before,after,a,set())
    assert before['araw']==after['araw'] and before['draw']==after['draw']
    suffix=after['araw'][len(araw):];assert suffix==b'';exact(PRIVATE/'window1-failure-actual-suffix.raw',suffix)
    pl=read(OWN/'PROVED_LOCAL-original25.exact.json');inspect_target(after,pl,'PROVED_LOCAL')
    marker=PRIVATE/'normal-V-attempted.once.json';assert not marker.exists() and not (PRIVATE/'window1-API-return.private.json').exists()
    receipt=read(OWN/'window1-OS-receipt.public.json');assert receipt['actual_exit_code']==1
    stderr=(PRIVATE/'window1-OS-process/stderr.raw').read_bytes();assert sha(stderr)==receipt['stderr_sha256'] and b'ident(authpath)' in stderr and b'ValueError:' in stderr
    proposal={'schema':'R17-window1-relative-authorization-path-implementation-fix-proposal-v1','status':'PROPOSAL_ONLY_NOT_APPLIED','classification':'IMPLEMENTATION_FAILED_PRE_API_PATH_NORMALIZATION','old_common_sha256':file_sha(OWN/'verification_common.py'),'old_verify_script_sha256':file_sha(OWN/'verify_once.py'),'function':'ident','exact_old_line':"    p=Path(p);return {'file':str(p.relative_to(REPO)),'bytes':p.stat().st_size,'sha256':file_sha(p)}",'exact_new_line':"    p=Path(p).resolve();return {'file':str(p.relative_to(REPO)),'bytes':p.stat().st_size,'sha256':file_sha(p)}",'reason':'The actual authorized CLI used a repo-relative authorization path. Resolve it before relative_to(REPO); absolute input behavior and all action/guard/target semantics remain unchanged.','new_action_requires_new_successor_output_guard_paths_and_explicit_ROOT_authorization':True,'normal_API_has_not_been_called':True}
    old=(OWN/'verification_common.py').read_text();assert old.count(proposal['exact_old_line'])==1
    import difflib
    fixed=old.replace(proposal['exact_old_line'],proposal['exact_new_line']);ast.parse(fixed)
    diff=''.join(difflib.unified_diff(old.splitlines(True),fixed.splitlines(True),fromfile='preserved-failed-original/verification_common.py',tofile='proposed-only/verification_common.py'))
    exact(OUT/'path-normalization.proposed.exact.diff',diff.encode());proposal['proposal_diff_sha256']=file_sha(OUT/'path-normalization.proposed.exact.diff');proposal['proposed_common_bytes_sha256']=sha(fixed.encode());write(OUT/'path-normalization.proposal.json',proposal)
    outcome={'schema':'R17-window1-actual-pre-API-failure-preservation-outcome-v1','status':'ACTUAL_EXIT1_BEFORE_API_ALL_POSTFAILURE_GUARDS_PASSED','advance_id':ADV,'checked_source_metadata_carrier':a['carrier_commit'],'actual_OS_exit_code':1,'normal_API_calls_actual':0,'actual_target_PL_events':1,'actual_target_VERIFIED_events':0,'normal_V_attempt_marker_present':False,'actual_A_ledger_suffix_bytes':0,'actual_A_ledger_suffix_sha256':sha(suffix),'full_old_A_ledger_prefix_and_bytes_preserved':True,'full_D_ledger_preserved':True,'all_frontiers_including_target_unchanged':True,'all_postfailure_guards_passed':True,'guards':guards,'failure_classification':'IMPLEMENTATION_FAILED: ident() relative authorization path vs absolute REPO, before marker/API/payload write','original_OS_receipt':ident(OWN/'window1-OS-receipt.public.json'),'actual_original_stderr_sha256':sha(stderr),'raw_OS_streams_fullledgers_index_allstate_guardmaps_remain_local_private':True,'normalV_success_or_cell_projection_claimed':False,'automatic_retry_rollback_or_script_rewrite':False,'fix_proposal':ident(OUT/'path-normalization.proposal.json')}
    write(OUT/'postfailure-preservation.outcome.json',outcome)
    print(json.dumps({'status':outcome['status'],'normal_API_calls_actual':0,'PL':1,'V':0,'all_postfailure_guards_passed':True,'outcome_sha256':file_sha(OUT/'postfailure-preservation.outcome.json'),'proposal_sha256':file_sha(OUT/'path-normalization.proposal.json'),'proposal_diff_sha256':proposal['proposal_diff_sha256']}))

if __name__=='__main__':
    os.umask(0o077);p=OUT/'process';p.mkdir(exist_ok=False)
    for fd,n in [(1,'stdout.raw'),(2,'stderr.raw')]:
        f=(p/n).open('xb',buffering=0);os.dup2(f.fileno(),fd);f.close()
    utc=dt.datetime.now(dt.timezone.utc).isoformat();start=time.monotonic();code=0
    try:main()
    except BaseException:traceback.print_exc();code=1
    sys.stdout.flush();sys.stderr.flush()
    write(p/'receipt.json',{'schema':'R17-actual-readonly-postfailure-preservation-OS-receipt-v1','argv':[sys.executable,*sys.argv],'cwd':str(Path.cwd()),'pid':os.getpid(),'started_utc':utc,'ended_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-start,'actual_exit_code':code,'script_sha256':file_sha(__file__),'stdout_sha256':file_sha(p/'stdout.raw'),'stderr_sha256':file_sha(p/'stderr.raw'),'no_API_driver_replay_rollback_cell_or_tracked_mutation':True});sys.exit(code)
