#!/usr/bin/env python3
"""DESIGN ONLY until separate real-facts preflight and execution root grants.
Only one future normal API callsite. Never copy latest STAB evidence.
"""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,copy,datetime,gzip,hashlib,json,os,subprocess,time
ROOT=Path('/Users/zhouhuanjian/ASTIS-GC');HERE=Path(__file__).resolve().parent
CFG=json.loads((HERE/'design-configuration.json').read_text())
ADV=ROOT/'runs/substantive_advances.jsonl';DISC=ROOT/'runs/substantive_discoveries.jsonl'
ENV=dict(os.environ);ENV['PYTHONDONTWRITEBYTECODE']='1';ENV['GIT_OPTIONAL_LOCKS']='0'
os.environ.update(PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0')
def sha(b):return hashlib.sha256(b).hexdigest()
def j(p):return json.loads(p.read_text())
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def emit(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,env=ENV)
def descriptor(path):return {'path':str(path.relative_to(ROOT)),'sha256':sha(path.read_bytes())}
def artifact(d):
    p=(ROOT/d['path']).resolve();assert p.is_relative_to(ROOT) and p.is_file();b=p.read_bytes();assert sha(b)==d['sha256'];return p,b

def seal():
    p=HERE/'design-manifest.json';raw=p.read_bytes();digest=sha(raw);assert digest==(HERE/'design-manifest.sha256').read_text().split()[0]
    for f in json.loads(raw)['files']:
        p=(HERE/f['path']).resolve();assert p.is_relative_to(HERE);b=p.read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256']
    return digest

def strict_current_raw():
    # FIRST: raw complete ledgers, before importing any recovering-loader code.
    ab=ADV.read_bytes();db=DISC.read_bytes();assert sha(ab)==CFG['expected_current_ledger_sha256'] and sha(db)==CFG['expected_discovery_ledger_sha256']
    assert ab.endswith(b'\n') and db.endswith(b'\n');ar=[json.loads(x) for x in ab.splitlines()];dr=[json.loads(x) for x in db.splitlines()];assert all(isinstance(x,dict) for x in ar+dr)
    assert sha(ab.splitlines(keepends=True)[-2])==CFG['original_actual_V_sha256'] and sha(ab.splitlines(keepends=True)[-1])==CFG['expected_STAB_sha256']
    return ab,db,ar,dr

def original_evidence():
    public=(ROOT/CFG['original_actual_V_path']).read_bytes();assert sha(public)==CFG['original_actual_V_sha256'];assert public==(HERE/'original-actual-V-event.raw.json').read_bytes()
    v=json.loads(public);e=copy.deepcopy(v['evidence']);assert len(e)==CFG['original_evidence_key_count_derived']
    assert sha(canon(e))==CFG['original_evidence_canonical_sha256'];assert e['verified_commit']==CFG['source_verified_commit'] and e['verifier_id']==CFG['actor']
    assert 'post_integration_normalpark' not in e
    return e

def pointer(document,p):
    assert isinstance(p,str) and p.startswith('/')
    for token in p.split('/')[1:]:document=document[int(token)] if isinstance(document,list) else document[token.replace('~1','/').replace('~0','~')]
    return document

def assertion(document,spec,required=None):
    value=pointer(document,spec['pointer']);assert value==spec['equals']
    if required is not None:assert value==required
    return value

def accepted(document,spec):
    value=assertion(document,spec)
    assert value is True or isinstance(value,str) and value.lower() in {'accepted','accept','pass','passed','accepted-local','accepted-for-local-reader','accepted_local_reader','accepted_for_local_delivery','accepted_scoped_local_integration','eligible_for_separate_exact_normalpark_review_only'}

def required_real_facts(binding_path):
    f=j(binding_path);assert f['immutable_core']==CFG['immutable_integration_core']
    head=git('rev-parse','HEAD').decode().strip();assert f['execution_HEAD']==head
    assert subprocess.run(['git','merge-base','--is-ancestor',CFG['immutable_integration_core'],head],cwd=ROOT,env=ENV).returncode==0
    dpath,db=artifact(f['delivery_manifest']);delivery=json.loads(db);assert delivery['immutable_core']==CFG['immutable_integration_core']
    assert delivery['actual_eight_same_core_checks']==CFG['expected_eight_gate_descriptors']
    for name,row in delivery['actual_eight_same_core_checks'].items():
        p,b=artifact({'path':row['public_receipt'],'sha256':row['original_receipt']['sha256']});receipt=json.loads(b)
        assert receipt['exit_code']==0 and receipt['head_before']==receipt['head_after']==CFG['immutable_integration_core']
        ob=(ROOT/row['original_receipt']['path']).read_bytes();assert ob==b
        assert sha(gzip.decompress((ROOT/row['public_log_gzip']).read_bytes()))==row['raw_log_sha256']==receipt['log_sha256']
    bp=ROOT/CFG['expected_browser_report_path'];bb=bp.read_bytes();assert sha(bb)==CFG['expected_browser_report_sha256'];browser=json.loads(bb)
    assert browser['head']==browser['site_commit']==browser['actual_gate_commit']==CFG['immutable_integration_core'] and browser['status']=='passed' and browser['errors']==[]
    assert browser['publication_binding_sha256']==CFG['publication_binding_sha256']
    br=j(ROOT/CFG['expected_browser_receipt_path']);assert br['exit_code']==0 and br['head_before']==br['head_after']==CFG['immutable_integration_core']
    images=browser['screenshots'];assert len(images)==44
    for row in images:assert sha((bp.parent/row['file']).read_bytes())==row['sha256']
    # A script PASS/root8 report cannot stand in for the actual independent44 review.
    px=f['all44_review'];pp,pb=artifact(px['artifact']);assert sha(pb)==CFG['root_reported_actual_all44_review_sha256'];pr=json.loads(pb)
    reviewer=assertion(pr,px['reviewer']);assert reviewer not in {CFG['actor'],CFG['proof_owner'],'root','/root'}
    assertion(pr,px['immutable_core'],CFG['immutable_integration_core']);accepted(pr,px['accepted']);assertion(pr,px['opened_count'],44);assertion(pr,px['method'])
    jp,jb=artifact(px['actual_originals_journal']);rows=json.loads(jb);assert all(x['actually_viewed'] is True and x['detail']=='original' and x['contact_sheet_crop_transform_or_browser_rerun'] is False for x in rows)
    pairs={(Path(x[px['file_key']]).name,x[px['sha256_key']]) for x in rows};assert len(rows)==44 and pairs=={(x['file'],x['sha256']) for x in images}
    local=f['local_acceptance'];lp,lb=artifact(local['artifact']);lr=json.loads(lb);accepted(lr,local['accepted']);assertion(lr,local['immutable_core'],CFG['immutable_integration_core']);assertion(lr,local['all44_review_sha256'],sha(pb))
    elig=f['normalpark_eligibility'];ep,eb=artifact(elig['artifact']);er=json.loads(eb);accepted(er,elig['eligible']);assertion(er,elig['immutable_core'],CFG['immutable_integration_core']);assertion(er,elig['local_acceptance_sha256'],sha(lb))
    assert er['must_preserve']['original_V_evidence_fields_exact']==original_evidence() and er['must_preserve']['original_V_evidence_canonical_sha256']==CFG['original_evidence_canonical_sha256']
    assert er['normal_API_calls_authorized_by_this_artifact']==0 and er['eligibility_is_API_or_execution_authorization'] is False and lr['API_or_normalpark_execution_authorized'] is False
    assert er['accepted_reader_limits_preserved_verbatim']==lr['actual_reader_scope']['pixel_limits_preserved_verbatim']
    for key in ('independent_application_readback','approved_browser44_report','independent_all44_original_pixel_acceptance','root_representative8_original_acceptance'):artifact(lr['actual_acceptance_evidence'][key])
    assert len({str(pp),str(lp),str(ep)})==3 and len({sha(pb),sha(lb),sha(eb)})==3
    for rel,digest in CFG['proof_and_source_pins'].items():assert sha((ROOT/rel).read_bytes())==digest,rel
    return f,{'all44_review':px['artifact'],'local_acceptance':local['artifact'],'normalpark_eligibility':elig['artifact'],'delivery_manifest':f['delivery_manifest'],'independent_pixel_reviewer':reviewer,'actual_original_count':44,'actual_originals_journal':px['actual_originals_journal'],'accepted_reader_limits_preserved_verbatim':er['accepted_reader_limits_preserved_verbatim']}

def grant(path,kind,facts_path,preflight_sha=None):
    a=j(path);assert a['issuer']=='/root' and a['action']==kind and a['actor']==CFG['actor']
    assert a['design_manifest_sha256']==seal() and a['helper_sha256']==sha(Path(__file__).read_bytes()) and a['facts_binding_sha256']==sha(facts_path.read_bytes())
    assert a['source_verified_commit']==CFG['source_verified_commit'] and a['immutable_core']==CFG['immutable_integration_core'] and a['original_actual_V_sha256']==CFG['original_actual_V_sha256']
    assert a['normal_API_calls_allowed']==(1 if kind=='execute-normalpark-once' else 0)
    if preflight_sha is not None:assert a['bound_preflight_receipt_sha256']==preflight_sha
    return descriptor(path)

def api_imports():
    sys.path.insert(0,str(ROOT));from tools import astis_advance as advance;from tools import astis_publication as pub
    return advance,pub

def raw_track_snapshot():
    result={}
    for row in git('ls-files','--stage','-z').split(b'\0'):
        if not row:continue
        left,rel=row.split(b'\t',1);mode,blob,stage=left.decode().split();assert stage=='0';path=rel.decode();p=ROOT/path;assert not p.is_symlink()
        result[path]={'sha256':sha(p.read_bytes()),'mode':mode,'index_blob':blob}
    return result

def require_tracks(old,ledger_sha=None):
    now=raw_track_snapshot();expected=copy.deepcopy(old)
    if ledger_sha is not None:expected['runs/substantive_advances.jsonl']['sha256']=ledger_sha
    assert now==expected,'Non-ledger raw tracked/index input changed';return len(now)

def real_bound_preflight(facts_path,authorization_path):
    # Deliberately not run during design preparation; real future files/grant mandatory.
    ab,db,ar,dr=strict_current_raw();grant_desc=grant(authorization_path,'authorize-normalpark-bound-preflight',facts_path);facts,refs=required_real_facts(facts_path);original_evidence()
    advance,pub=api_imports();states=advance._replay_advances(ar);own=states[CFG['advance_id']];assert own['state']=='STABILIZING' and own['owner_id']==CFG['proof_owner'];assert own['publication_declarations']==original_evidence()['publication_declarations']
    pub.check_advance(original_evidence()['publication_declarations'],reviewed=True)
    tracks=raw_track_snapshot();assert ADV.read_bytes()==ab and DISC.read_bytes()==db
    baseline={'HEAD':facts['execution_HEAD'],'tracks':tracks,'foreign_states':{k:v for k,v in states.items() if k!=CFG['advance_id']},'own_state':own,'discovery_states':advance._replay_discoveries(dr),'all_frontier_raw_hashes':{str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in (ROOT/'research-wiki/frontier-cells').rglob('*.json')}}
    out=HERE/'bound-preflight';out.mkdir(exist_ok=False)
    (out/'ledger.before.raw.jsonl.gz').write_bytes(gzip.compress(ab,mtime=0));(out/'discovery.before.raw.jsonl.gz').write_bytes(gzip.compress(db,mtime=0));(out/'baseline.json.raw.gz').write_bytes(gzip.compress(json.dumps(baseline,ensure_ascii=False).encode(),mtime=0));(out/'actual-facts-binding.raw.json').write_bytes(facts_path.read_bytes());(out/'root-preflight-grant.raw.json').write_bytes(authorization_path.read_bytes())
    receipt={'stage':'ACTUAL_BOUND_NORMALPARK_PREFLIGHT_ONLY','actor':CFG['actor'],'normal_API_calls_actual':0,'created_utc_actual':datetime.datetime.now(datetime.timezone.utc).isoformat(),'facts_binding_sha256':sha(facts_path.read_bytes()),'root_preflight_grant':grant_desc,'actual_fact_refs':refs,'expected_HEAD':facts['execution_HEAD'],'ledger_before_sha256':sha(ab),'discovery_sha256':sha(db),'tracked_count':len(tracks),'baseline_archive_sha256':sha((out/'baseline.json.raw.gz').read_bytes()),'original_evidence_keys_preserved':CFG['original_evidence_keys_derived'],'separate_execution_authorization_required':True};emit(out/'preflight-receipt.json',receipt);return receipt

def execute_once(facts_path,authorization_path):
    # No execute route is enabled by a design-only grant or a preflight grant.
    pf=HERE/'bound-preflight';pb=(pf/'preflight-receipt.json').read_bytes();receipt=json.loads(pb);assert receipt['normal_API_calls_actual']==0 and receipt['stage']=='ACTUAL_BOUND_NORMALPARK_PREFLIGHT_ONLY'
    exec_grant=grant(authorization_path,'execute-normalpark-once',facts_path,sha(pb));ab,db,ar,dr=strict_current_raw();facts,refs=required_real_facts(facts_path);assert sha(facts_path.read_bytes())==receipt['facts_binding_sha256']
    assert git('rev-parse','HEAD').decode().strip()==receipt['expected_HEAD'];gz=(pf/'baseline.json.raw.gz').read_bytes();assert sha(gz)==receipt['baseline_archive_sha256'];base=json.loads(gzip.decompress(gz));require_tracks(base['tracks'])
    advance,pub=api_imports();states=advance._replay_advances(ar);assert states[CFG['advance_id']]==base['own_state'] and states[CFG['advance_id']]['state']=='STABILIZING';assert {k:v for k,v in states.items() if k!=CFG['advance_id']}==base['foreign_states'];assert advance._replay_discoveries(dr)==base['discovery_states'];pub.check_advance(original_evidence()['publication_declarations'],reviewed=True)
    evidence=copy.deepcopy(original_evidence());post={'purpose':'Release existing source VERIFIED status after separately accepted local integration; no new source fidelity judgment.','original_actual_V':{'path':CFG['original_actual_V_path'],'sha256':CFG['original_actual_V_sha256'],'preserved_original_evidence_key_count':len(evidence)},'immutable_integration_core':CFG['immutable_integration_core'],'actual_local_acceptance':refs['local_acceptance'],'actual_separate_normalpark_eligibility':refs['normalpark_eligibility'],'actual_independent_all44_original_review':refs['all44_review'],'root_exact_execution_grant':exec_grant,'actual_bound_preflight_receipt':descriptor(pf/'preflight-receipt.json'),'root_exact_preflight_grant':receipt['root_preflight_grant'],'actual_eight_same_core_gates':CFG['expected_eight_gate_descriptors'],'actual_browser_receipt':descriptor(ROOT/CFG['expected_browser_receipt_path']),'actual_browser_report':{'path':CFG['expected_browser_report_path'],'sha256':CFG['expected_browser_report_sha256']},'actual_delivery_manifest':refs['delivery_manifest'],'actual_originals_journal':refs['actual_originals_journal'],'accepted_reader_limits_preserved_verbatim':refs['accepted_reader_limits_preserved_verbatim'],'source_verified_commit_remains':CFG['source_verified_commit'],'remaining_boundary':'No new source statement/proof/audit; no remote acceptance, purification/Exposition Seal, main lower bounds or Goal completion.'}
    evidence['post_integration_normalpark']=post
    assert {k:v for k,v in evidence.items() if k!='post_integration_normalpark'}==original_evidence() and len(evidence)==len(original_evidence())+1
    out=HERE/'execution';out.mkdir(exist_ok=False);emit(out/'actual-call-evidence.json',evidence);(out/'root-execution-grant.raw.json').write_bytes(authorization_path.read_bytes());clock=time.perf_counter();calls=0;error=None
    try:
        # SOLE NORMAL API CALLSITE. No manual ledger append exists in this helper.
        calls+=1
        advance.transition_advance(CFG['advance_id'],'VERIFIED',worker_id=CFG['actor'],modes=['post-integration-normalpark-existing-V-release'],evidence=evidence)
    except BaseException as exc:error=repr(exc)
    after=ADV.read_bytes();append=after[len(ab):] if after.startswith(ab) else b'';(out/'actual-normalpark-append.raw.jsonl').write_bytes(append);(out/'ledger.after-observed.raw.jsonl.gz').write_bytes(gzip.compress(after,mtime=0))
    observation={'actor':CFG['actor'],'normal_API_calls_actual':calls,'returned_success':error is None,'error':error,'elapsed_seconds_actual':time.perf_counter()-clock,'before_ledger_sha256':sha(ab),'after_ledger_sha256':sha(after),'observed_append_sha256':sha(append)};emit(out/'actual-API-receipt.json',observation)
    if error is not None:raise RuntimeError('STOP: real normal API failed, actual bytes preserved; no retry. '+error)
    assert calls==1 and after.startswith(ab) and append.endswith(b'\n') and len(append.splitlines())==1;event=json.loads(append)
    assert event['event']=='transition' and event['advance_id']==CFG['advance_id'] and event['from_state']=='STABILIZING' and event['to_state']=='VERIFIED' and event['worker_id']==CFG['actor'] and event['evidence']==evidence
    assert event['evidence']['verified_commit']==CFG['source_verified_commit'];assert {k:v for k,v in event['evidence'].items() if k!='post_integration_normalpark'}==original_evidence();datetime.datetime.fromisoformat(event['created_at'])
    assert DISC.read_bytes()==db;count=require_tracks(base['tracks'],sha(after));assert {str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in (ROOT/'research-wiki/frontier-cells').rglob('*.json')}==base['all_frontier_raw_hashes'];new=advance._replay_advances([json.loads(x) for x in after.splitlines()]);assert {k:v for k,v in new.items() if k!=CFG['advance_id']}==base['foreign_states'];assert new[CFG['advance_id']]['owner_id']==CFG['proof_owner']
    emit(out/'actual-normalpark-append.parsed.json',event);result={'actor':CFG['actor'],'normal_API_calls':1,'exact_append_path':str((out/'actual-normalpark-append.raw.jsonl').relative_to(ROOT)),'exact_append_sha256':sha(append),'actual_created_at_from_API':event['created_at'],'before_ledger_sha256':sha(ab),'after_ledger_sha256':sha(after),'verified_commit':CFG['source_verified_commit'],'immutable_integration_core':CFG['immutable_integration_core'],'original_actual_V_sha256':CFG['original_actual_V_sha256'],'original_evidence_key_count':len(original_evidence()),'original_evidence_canonical_sha256':CFG['original_evidence_canonical_sha256'],'only_added_evidence_key':'post_integration_normalpark','all_original_evidence_values_preserved':True,'accepted_audit_sha256':CFG['accepted_audit_sha256'],'publication_binding_sha256':CFG['publication_binding_sha256'],'source_review_run_sha256':CFG['source_review_run_sha256'],'proof_owner_preserved':CFG['proof_owner'],'raw_old_ledger_prefix_preserved':True,'all_nonledger_tracked_bytes_index_source_audit_cell_README_models_queues_unchanged':True,'tracked_count':count,'all_foreign_SAU_states_unchanged':True,'discovery_ledger_unchanged':True,'real_facts':refs,'root_exact_execution_grant':exec_grant,'preflight_receipt_sha256':sha(pb),'API_receipt':descriptor(out/'actual-API-receipt.json'),'source_fidelity_reissued':False};emit(out/'execution-manifest.json',result);return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['describe','preflight','execute']);p.add_argument('--facts-binding',type=Path);p.add_argument('--authorization',type=Path);args=p.parse_args()
    if args.mode=='describe':result={'stage':CFG['stage'],'normal_API_calls_actual':0,'requires_real_facts_and_separate_root_grants':True,'preflight_run_by_describe':False}
    else:
        assert args.facts_binding is not None and args.authorization is not None,'Actual complete facts and the separate exact root grant are mandatory; design-only permission never suffices.'
        result=real_bound_preflight(args.facts_binding,args.authorization) if args.mode=='preflight' else execute_once(args.facts_binding,args.authorization)
    print(json.dumps(result,indent=2,ensure_ascii=False))
