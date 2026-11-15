"""Copy exact sealed scripts into fresh namespace; only invocation adapts to absolute authorization paths."""
import datetime as dt,hashlib,json,os,stat,sys,time,traceback
from pathlib import Path
OWN=Path(__file__).resolve().parent;REPO=OWN.parents[2];OLD=OWN.parent/'matrix_domain_normal_verification_61e4'
PINS={'verification_common.py':'5ecb1959ce2bd002ae3eaaadd5eb67d4852deb61693aee7ee17bd64bf9649822','verify_once.py':'342079d11a4458c1d8b27f483c195dcfb1e608f090865dcb5666602c924a6f76','project_cell_once.py':'c02bb4b16caa622c14f1f5e2e6cc68a0aae9e7c74e0519f41b55db4ddb347ecc'}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):
    with Path(p).open('x') as f:f.write(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def main():
    checks=[]
    def check(n,ok):
        checks.append({'name':n,'pass':bool(ok)})
        if not ok:raise AssertionError(n)
    for n,h in PINS.items():
        check('sealed-original-script-pin:'+n,sha(OLD/n)==h)
        with (OWN/n).open('xb') as f:f.write((OLD/n).read_bytes())
        check('new-script-direct-byte-equality:'+n,(OWN/n).read_bytes()==(OLD/n).read_bytes() and sha(OWN/n)==h)
    for n in ['PROVED_LOCAL-original25.exact.json','authorization.schema.json']:
        with (OWN/n).open('xb') as f:f.write((OLD/n).read_bytes())
    check('PL25-exact',sha(OWN/'PROVED_LOCAL-original25.exact.json')=='4e1ae70212a5c951239de161597d0ebf816632c70762305d8c22a7841ea1e520' and len(json.loads((OWN/'PROVED_LOCAL-original25.exact.json').read_text()))==25)
    d=OWN/'local-private-guards';d.mkdir(mode=0o700,exist_ok=False);os.chmod(d,0o700)
    check('new-private-guard-namespace-empty0700',stat.S_IMODE(d.stat().st_mode)==0o700 and not list(d.iterdir()))
    proof=OLD/'window1-failure-review-v1/postfailure-preservation.outcome.json'
    check('actual-failure-preservation-reused-without-reexecution',sha(proof)=='5d566503ae8e3d5d5c73b13cb50c1f78c3504dcdc777f873612746c60c974605')
    frozen=json.loads((OLD/'window1.contract.draft.json').read_text());auth=OWN/'window1.ROOT-authorization.v1.json'
    check('absolute-auth-path-contract',auth.is_absolute() and auth.relative_to(REPO).as_posix().endswith('/window1.ROOT-authorization.v1.json'))
    frozen['runtime_invocation_contract']={'all_authorization_arguments_must_be_absolute':True,'new_namespace_only':True,'old_failed_namespace_must_not_be_rerun':True,'actual_window1_authorization_file':str(auth),'scripts_copied_byte_exact':True,'no_source_code_fix_or_new_math_source_reader_gate_run':True}
    write(OWN/'window1.contract.draft.json',frozen)
    second=json.loads((OLD/'window2.contract.template.json').read_text());second['projection_candidate']['file']=str((OWN/'target-cell-proposal.exact.json').relative_to(REPO));second['runtime_invocation_contract']={'all_authorization_arguments_must_be_absolute':True,'new_namespace_only':True}
    write(OWN/'window2.contract.template.json',second)
    command=['python3','-B',str(OWN/'verify_once.py'),'--authorization',str(auth),'--authorization-sha256','ROOT_ACTUAL_NEW_AUTHORIZATION_SHA256']
    report={'schema':'R17-byte-identical-absolute-authorization-successor-preparation-v1','status':'PREPARED_ONLY_NO_ACTION','checks':checks,'scripts':PINS,'old_implementation_failure_exit1_API0_PL1_V0_preserved':True,'original_failure_preservation_report_sha256':sha(proof),'only_operational_change':'Fresh OWN output/guard namespace and ABSOLUTE authorization argument at actual invocation. Three action/guard scripts retain identical original bytes/SHA; no source patch applied.','carrier_and_evidence_pins_inherited_exact_from_prepared_draft_not_reaudited':frozen['carrier_commit'],'six_real_gate_summary_sha256':frozen['gate_summary']['sha256'],'new_API_cell_ledger_Git_mutations':0,'native_source_reader_Lean_gate_reruns':0,'full_guard_snapshot_runs':0,'normal_API_actual_before_this_preparation':0,'root_must_review_and_separately_authorize_new_window':True,'window1_draft_sha256':sha(OWN/'window1.contract.draft.json'),'window2_template_sha256':sha(OWN/'window2.contract.template.json'),'concrete_ABSOLUTE_path_invocation':command}
    write(OWN/'preparation-result.json',report)
    print(json.dumps({'status':report['status'],'scripts':PINS,'checks':len(checks),'window1_draft_sha256':report['window1_draft_sha256'],'window2_template_sha256':report['window2_template_sha256'],'preparation_result_sha256':sha(OWN/'preparation-result.json'),'concrete_invocation':command}))
if __name__=='__main__':
    p=OWN/'preparation-process';p.mkdir(exist_ok=False)
    for fd,n in [(1,'stdout.raw'),(2,'stderr.raw')]:
        f=(p/n).open('xb',buffering=0);os.dup2(f.fileno(),fd);f.close()
    utc=dt.datetime.now(dt.timezone.utc).isoformat();start=time.monotonic();code=0
    try:main()
    except BaseException:traceback.print_exc();code=1
    sys.stdout.flush();sys.stderr.flush()
    write(p/'receipt.json',{'schema':'R17-actual-byte-copy-absolute-invocation-preparation-OS-receipt-v1','argv':[sys.executable,*sys.argv],'cwd':str(Path.cwd()),'pid':os.getpid(),'started_utc':utc,'ended_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-start,'actual_exit_code':code,'script_sha256':sha(__file__),'stdout_sha256':sha(p/'stdout.raw'),'stderr_sha256':sha(p/'stderr.raw'),'scope':'Only own exact script/PL/schema byte copies and draft invocation adaptation; no native/source/reader/gate/full snapshot/API/cell/ledger/index/Git action.'});sys.exit(code)
