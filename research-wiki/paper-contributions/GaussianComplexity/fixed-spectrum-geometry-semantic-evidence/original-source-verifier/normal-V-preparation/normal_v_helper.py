#!/usr/bin/env python3
"""No-mutation preflight by default. Execution needs a later exact authorization.
Never call a recovering loader before checking complete raw old ledgers.
"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import argparse,copy,datetime,gzip,hashlib,json,os,stat,subprocess,time
from concurrent.futures import ThreadPoolExecutor
ROOT=Path('/Users/zhouhuanjian/ASTIS-GC');HERE=Path(__file__).resolve().parent
CFG=json.loads((HERE/'configuration.json').read_text())
ADV=ROOT/'runs/substantive_advances.jsonl';DISC=ROOT/'runs/substantive_discoveries.jsonl'
ENV=dict(os.environ);ENV['PYTHONDONTWRITEBYTECODE']='1';ENV['GIT_OPTIONAL_LOCKS']='0'
os.environ['PYTHONDONTWRITEBYTECODE']='1';os.environ['GIT_OPTIONAL_LOCKS']='0'
def sha(b):return hashlib.sha256(b).hexdigest()
def j(path):return json.loads(path.read_text())
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def jsonl(b):
    assert b and b.endswith(b'\n'),'incomplete ledger: no recovering loader allowed'
    rows=[json.loads(x) for x in b.splitlines()]
    assert all(isinstance(x,dict) for x in rows)
    return rows
def original_raw():
    # This must precede every import/call capable of reaching recovering loaders.
    ab=ADV.read_bytes();db=DISC.read_bytes()
    assert sha(ab)==CFG['advance_ledger_before_sha256'];assert sha(db)==CFG['discovery_ledger_before_sha256']
    ar=jsonl(ab);dr=jsonl(db)
    assert ab==gzip.decompress((HERE/'advance-ledger.before.raw.jsonl.gz').read_bytes())
    assert db==gzip.decompress((HERE/'discovery-ledger.before.raw.jsonl.gz').read_bytes())
    return ab,db,ar,dr
def baseline():
    b=(HERE/'protected-baseline.json.raw.gz').read_bytes();assert sha(b)==CFG['protected_baseline_gzip_sha256']
    raw=gzip.decompress(b);assert sha(raw)==CFG['protected_baseline_raw_sha256'];return json.loads(raw)
def verify_seal(required=False):
    p=HERE/'preparation-manifest.json'
    if not p.exists():assert not required;return None
    b=p.read_bytes();digest=sha(b);assert digest==(HERE/'preparation-manifest.sha256').read_text().split()[0]
    for f in json.loads(b)['files']:
        q=(HERE/f['path']).resolve();assert q.is_relative_to(HERE);raw=q.read_bytes();assert len(raw)==f['bytes'] and sha(raw)==f['sha256'],f['path']
    return digest
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,env=ENV)
def tracked_baseline_check(base,overrides=None):
    overrides=overrides or {};assert git('rev-parse','HEAD').decode().strip()==CFG['candidate']
    entries={}
    for item in git('ls-files','--stage','-z').split(b'\0'):
        if not item:continue
        left,path=item.split(b'\t',1);mode,blob,stage=left.decode().split();assert stage=='0';entries[path.decode()]=(mode,blob)
    assert set(entries)==set(base['all_tracked']),'tracked-path set changed'
    def check(item):
        rel,meta=item;p=ROOT/rel;st=p.stat();assert not p.is_symlink() and not meta['symlink'];assert entries[rel]==(meta['mode'],meta['git_index_blob']),rel
        assert bool(st.st_mode & 0o111)==(meta['mode']=='100755'),rel
        digest=hashlib.sha256();size=0
        with p.open('rb') as f:
            while chunk:=f.read(1024*1024):digest.update(chunk);size+=len(chunk)
        expected=overrides.get(rel,meta['sha256']);assert digest.hexdigest()==expected,rel
        if rel not in overrides:assert size==meta['raw_bytes'],rel
        return size
    with ThreadPoolExecutor(max_workers=8) as pool:total=sum(pool.map(check,base['all_tracked'].items(),chunksize=128))
    return {'tracked_files':len(entries),'raw_bytes_checked':total,'all_unallowed_raw_tracked_bytes_preserved':True,'allowed_overrides':overrides}
def import_apis():
    sys.path.insert(0,str(ROOT))
    from tools import astis_advance as advance
    from tools import astis_publication as publication
    return advance,publication
def earlier_evidence_check():
    p3=ROOT/CFG['phase3_private_dir'];public=ROOT/CFG['phase3_public_dir'];mb=(p3/'phase3_manifest.json').read_bytes();assert sha(mb)==CFG['phase3_manifest_sha256'];m=json.loads(mb)
    for f in m['files']:
        a=(p3/f['path']).read_bytes();b=(public/f['path']).read_bytes();assert a==b and len(a)==f['bytes'] and sha(a)==f['sha256'],f['path']
    assert sha((HERE/'accepted-audit.raw.json').read_bytes())==CFG['accepted_audit_sha256']
    assert sha((p3/'reviewer-run.json').read_bytes())==CFG['source_review_run_sha256']
    assert j(p3/'review-result.json')['verdict']=='equivalent-after-elaboration'
    assert not j(p3/'private-successor-schema-check.json')['errors']
    assert len(j(p3/'lean-evidence/fresh-compilation.json')['runs'])==5 and all(x['returncode']==0 for x in j(p3/'lean-evidence/fresh-compilation.json')['runs'])
    assert j(p3/'lean-evidence/kernel-probe-run.json')['returncode']==0
    for rel,digest in CFG['proof_and_publication_pins'].items():assert sha((ROOT/rel).read_bytes())==digest,rel
    return {'phase3_private_and_public_payloads_exact':len(m['files']),'fresh_proof_receipts_preserved':True,'no_new_Lean_or_runtime_claim':True}
def states_check(base,ar,dr,advance,expected_own_state,after_projection=False):
    # Pure replay of strict caller-parsed rows; never current_advances/load_jsonl.
    states=advance._replay_advances(ar);foreign={k:v for k,v in states.items() if k!=CFG['advance_id']};assert foreign==base['foreign_SAU_states']
    own=states[CFG['advance_id']];assert own['state']==expected_own_state and own['owner_id']==CFG['proof_owner'];assert own['publication_declarations']==base['own_SAU_state']['publication_declarations']
    if expected_own_state=='PROVED_LOCAL':assert own==base['own_SAU_state']
    else:
        allowed={'state','last_actor','modes','latest_evidence','updated_at'}
        assert {k:v for k,v in own.items() if k not in allowed}=={k:v for k,v in base['own_SAU_state'].items() if k not in allowed}
        assert own['last_actor']==CFG['actor'] and own['modes']==CFG['modes']
    assert advance._replay_discoveries(dr)==base['all_discovery_states']
    for rel,digest in base['all_frontier_raw_hashes'].items():
        expected=CFG['projection_after_sha256'] if after_projection and rel==CFG['cell_path'] else digest
        assert sha((ROOT/rel).read_bytes())==expected,rel
    for rel,digest in base['all_models_before'].items():assert sha((ROOT/rel).read_bytes())==digest,rel
    return {'foreign_SAU_states':len(foreign),'all_discovery_states':len(base['all_discovery_states']),'frontiers_checked':len(base['all_frontier_raw_hashes']),'models_checked':len(base['all_models_before']),'proof_owner_preserved':True,'own_state':expected_own_state}
def publication_overlay_check(publication):
    # Only an in-memory accepted audit overlay; actual canonical audit stays blind.
    real=publication.roundtrip.load_registry;accepted=j(HERE/'accepted-audit.raw.json')
    def overlay(*args,**kwargs):
        data=copy.deepcopy(real(*args,**kwargs));hits=[i for i,a in enumerate(data['audits']) if a['id']==accepted['id']];assert len(hits)==1;data['audits'][hits[0]]=accepted;return data
    publication.roundtrip.load_registry=overlay
    try:
        publication.check_advance(j(HERE/'planned-normal-api-evidence.json')['publication_declarations'],reviewed=True)
        data=publication.inputs();item=next(i for i in publication.load() if i['id']=='huanjian-fixed-spectrum-geometry');binding=item['bindings'][0]
        assert publication.binding_digest(item,binding,data)==CFG['publication_binding_sha256']
    finally:
        publication.roundtrip.load_registry=real;publication.inputs.cache_clear();publication.load.cache_clear()
    return {'normal_publication_check_with_private_in_memory_successor':'pass','actual_canonical_audit_not_changed':True,'overlay_removed_before_any_future_normal_API':True}
def preflight():
    start=time.perf_counter();ab,db,ar,dr=original_raw();base=baseline();seal=verify_seal()
    tracked=tracked_baseline_check(base);earlier=earlier_evidence_check()
    assert (ROOT/CFG['cell_path']).read_bytes()==(HERE/'own-cell.before.raw.json').read_bytes()
    assert sha((ROOT/CFG['audit_path']).read_bytes())==CFG['original_blind_audit_sha256']
    advance,publication=import_apis();state=states_check(base,ar,dr,advance,'PROVED_LOCAL');evidence=j(HERE/'planned-normal-api-evidence.json')
    advance._validate_transition_evidence('VERIFIED',evidence,schema_version=4)
    assert evidence['verifier_id']==CFG['actor']!=CFG['proof_owner'] and evidence['verified_commit']==CFG['candidate']
    gate=publication_overlay_check(publication)
    # End-to-end no-mutation guard, including every raw tracked baseline byte.
    tracked_after=tracked_baseline_check(base)
    # Recheck complete raw files after all validation; do not repair any tail.
    assert ADV.read_bytes()==ab and DISC.read_bytes()==db
    assert sha((ROOT/CFG['audit_path']).read_bytes())==CFG['original_blind_audit_sha256']
    assert (ROOT/CFG['cell_path']).read_bytes()==(HERE/'own-cell.before.raw.json').read_bytes()
    return {'mode':'PREPARATION_ONLY_NO_MUTATION','actor':CFG['actor'],'normal_API_calls_actual':0,'checked_candidate':CFG['candidate'],'preparation_manifest_sha256':seal,'strict_old_ledger_bytes_checked_before_imports_or_recovering_loaders':True,'advance_records':len(ar),'discovery_records':len(dr),'tracked_preservation':tracked,'tracked_preservation_after_checks':tracked_after,'prior_evidence':earlier,'state_preservation':state,'publication_preflight':gate,'elapsed_seconds_actual':time.perf_counter()-start,'actual_V_event_created':False,'actual_execution_manifest_created':False}
def write_json(path,value):path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def atomic_copy_bytes(data,target,execution):
    # Temporary is private; only exact final bytes replace an authorized target.
    mode=stat.S_IMODE(target.stat().st_mode);tmp=execution/(target.name+'.private-tmp');fd=os.open(tmp,os.O_CREAT|os.O_EXCL|os.O_WRONLY,mode)
    with os.fdopen(fd,'wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
    os.chmod(tmp,mode);os.replace(tmp,target);d=os.open(target.parent,os.O_RDONLY)
    try:os.fsync(d)
    finally:os.close(d)
def execute_later(authorization):
    # Not authorized merely by the existence of this code. Exact later root grant required.
    seal=verify_seal(required=True);auth=j(authorization)
    assert auth=={'action':'execute-exact-prepared-normal-PROVED_LOCAL-to-VERIFIED-once','actor':CFG['actor'],'checked_candidate_commit':CFG['candidate'],'preparation_manifest_sha256':seal,'allow_exact_audit_copy':True,'allow_post_success_exact_own_cell_projection':True}
    report=preflight();execution=HERE/'execution';execution.mkdir(exist_ok=False) # one-shot, including failures
    started=datetime.datetime.now(datetime.timezone.utc).isoformat();clock=time.perf_counter();write_json(execution/'preflight-receipt.json',report);(execution/'authorization.raw.json').write_bytes(authorization.read_bytes())
    ab,db,ar,dr=original_raw();earlier_evidence_check();base=baseline();audit=ROOT/CFG['audit_path'];cell=ROOT/CFG['cell_path'];accepted=(HERE/'accepted-audit.raw.json').read_bytes();oldaudit=audit.read_bytes();assert sha(accepted)==CFG['accepted_audit_sha256']
    write_json(execution/'attempt-started.json',{'actor':CFG['actor'],'started_at_actual':started,'normal_API_calls_actual':0,'no_retry_rule':'This execution directory is exclusive. Any failure stops without retrying or manually fabricating a V append.'})
    atomic_copy_bytes(accepted,audit,execution);advance,_=import_apis();api_calls=0;api_start=time.perf_counter();api_error=None
    try:
        # THE ONLY NORMAL STATE-TRANSITION API CALL IN THIS HELPER.
        api_calls+=1
        advance.transition_advance(CFG['advance_id'],'VERIFIED',worker_id=CFG['actor'],modes=CFG['modes'],evidence=j(HERE/'planned-normal-api-evidence.json'))
    except BaseException as exc:api_error=repr(exc)
    api_elapsed=time.perf_counter()-api_start;after=ADV.read_bytes();append=after[len(ab):] if after.startswith(ab) else b''
    (execution/'ledger.after-observed.raw.jsonl.gz').write_bytes(gzip.compress(after,mtime=0));(execution/'actual-V-append.raw.jsonl').write_bytes(append)
    receipt={'actor':CFG['actor'],'normal_API_calls_actual':api_calls,'normal_API':CFG['normal_api'],'returned_success':api_error is None,'error':api_error,'elapsed_seconds_actual':api_elapsed,'before_ledger_sha256':sha(ab),'after_ledger_sha256':sha(after),'observed_append_sha256':sha(append),'observed_append_bytes':len(append)};write_json(execution/'normal-API-receipt.json',receipt)
    if api_error is not None:
        if after==ab:atomic_copy_bytes(oldaudit,audit,execution) # no event: restore only exact audit bytes
        write_json(execution/'FAILED-NO-RETRY.json',receipt);raise RuntimeError('Normal API failed; preserved actual bytes/receipt. No retry or own-cell projection. '+api_error)
    assert api_calls==1 and after.startswith(ab) and append.endswith(b'\n') and len(append.splitlines())==1
    event=json.loads(append);assert isinstance(event,dict);expected=j(HERE/'planned-normal-api-evidence.json')
    assert {k:event[k] for k in ('event','advance_id','from_state','to_state','worker_id','modes','evidence')}=={'event':'transition','advance_id':CFG['advance_id'],'from_state':'PROVED_LOCAL','to_state':'VERIFIED','worker_id':CFG['actor'],'modes':CFG['modes'],'evidence':expected}
    assert event['schema_version']==4 and isinstance(event['created_at'],str);datetime.datetime.fromisoformat(event['created_at'])
    assert DISC.read_bytes()==db and sha(audit.read_bytes())==CFG['accepted_audit_sha256'] and cell.read_bytes()==(HERE/'own-cell.before.raw.json').read_bytes()
    state=states_check(base,jsonl(after),jsonl(db),advance,'VERIFIED');assert jsonl(after)[-1]==event
    write_json(execution/'actual-V-append.parsed.json',event)
    # This receipt is written only now, from the actual successful API/event bytes.
    manifest={'schema_version':1,'actor':CFG['actor'],'normal_API_calls':1,'normal_API':CFG['normal_api'],'exact_append_sha256':sha(append),'exact_append_path':str((execution/'actual-V-append.raw.jsonl').relative_to(ROOT)),'before_ledger_sha256':sha(ab),'after_ledger_sha256':sha(after),'verified_commit':CFG['candidate'],'publication_binding_sha256':CFG['publication_binding_sha256'],'accepted_audit_sha256':CFG['accepted_audit_sha256'],'source_review_run_sha256':CFG['source_review_run_sha256'],'actual_V_append':{'path':str((execution/'actual-V-append.raw.jsonl').relative_to(ROOT)),'sha256':sha(append),'bytes':len(append),'parsed_path':str((execution/'actual-V-append.parsed.json').relative_to(ROOT)),'created_at_from_actual_API':event['created_at']},'before_ledger':{'path':'runs/substantive_advances.jsonl','sha256':sha(ab),'bytes':len(ab),'lossless_archive':str((HERE/'advance-ledger.before.raw.jsonl.gz').relative_to(ROOT))},'after_ledger':{'path':'runs/substantive_advances.jsonl','sha256':sha(after),'bytes':len(after),'lossless_archive':str((execution/'ledger.after-observed.raw.jsonl.gz').relative_to(ROOT))},'elapsed_seconds':{'API_actual':api_elapsed,'execution_so_far_actual':time.perf_counter()-clock},'receipts':{'preflight':str((execution/'preflight-receipt.json').relative_to(ROOT)),'preflight_sha256':sha((execution/'preflight-receipt.json').read_bytes()),'normal_API':str((execution/'normal-API-receipt.json').relative_to(ROOT)),'normal_API_sha256':sha((execution/'normal-API-receipt.json').read_bytes())},'own_cell_projection':{'path':CFG['cell_path'],'before_sha256':CFG['projection_before_sha256'],'after_sha256':CFG['projection_after_sha256'],'status':'actual V parsed; exact planned projection not yet applied'},'raw_old_ledger_prefix_preserved':True,'discovery_ledger_sha256':sha(db),'proof_owner':CFG['proof_owner'],'foreign_state_preservation':state,'checked_candidate_vs_future_carrying_commit':'Candidate ab8; no future accepted-audit carrying commit created or checked by this helper.'}
    assert set(j(HERE/'execution-manifest.schema.json')['required']) <= set(manifest)
    write_json(execution/'execution-manifest.json',manifest)
    # Only AFTER the real successful V append and its actual receipt exist.
    assert ADV.read_bytes()==after and DISC.read_bytes()==db and cell.read_bytes()==(HERE/'own-cell.before.raw.json').read_bytes()
    projected=(HERE/'own-cell.after.raw.json').read_bytes();assert sha(projected)==CFG['projection_after_sha256'];atomic_copy_bytes(projected,cell,execution)
    state=states_check(base,jsonl(after),jsonl(db),advance,'VERIFIED',after_projection=True)
    overrides={CFG['audit_path']:CFG['accepted_audit_sha256'],'runs/substantive_advances.jsonl':sha(after),CFG['cell_path']:CFG['projection_after_sha256']};preserved=tracked_baseline_check(base,overrides)
    assert ADV.read_bytes()==after and DISC.read_bytes()==db and sha(audit.read_bytes())==CFG['accepted_audit_sha256'] and sha(cell.read_bytes())==CFG['projection_after_sha256']
    manifest['own_cell_projection']['status']='applied exact frozen bytes after successful normal V';manifest['foreign_state_preservation']=state;manifest['tracked_preservation']=preserved;manifest['elapsed_seconds']['execution_total_actual']=time.perf_counter()-clock;write_json(execution/'execution-manifest.json',manifest)
    return manifest
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('mode',choices=['preflight','verify-preparation','execute']);parser.add_argument('--authorization',type=Path);args=parser.parse_args()
    if args.mode=='preflight':result=preflight()
    elif args.mode=='verify-preparation':result={'sealed_preparation_sha256':verify_seal(required=True),'normal_API_calls_actual':0,'mode':'seal-integrity-only'}
    else:assert args.authorization is not None,'later explicit exact authorization file required';result=execute_later(args.authorization)
    print(json.dumps(result,indent=2,ensure_ascii=False))
