"""Exactly one normal transition call; full original event/evidence retained.

Project mutations allowed: the normal API append, then only own C.status and
own C.evidence.integration_boundary after API success. No retries or recovery
mutation. Private foreign snapshots never enter this portable directory.
"""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import base64
import copy
import json
import os
import stat
import subprocess
import sys

sys.dont_write_bytecode=True
REPO=Path.cwd().resolve()
sys.path.insert(0,str(REPO))
from tools import astis_advance as adv
ROOT=Path(__file__).resolve().parent
OWN=ROOT.parent
PRIVATE=OWN/'PRIVATE-normal-sourceV-baseline'
AID='ASTIS-SA-20261110-GaussianComplexityFixedSpectrumTargetLaw'
ACTOR='/root/targetlaw_fresh_source_9c7d21'
PROOF_OWNER='huanjian_gc_20261110_fixed_spectrum_target_law'
CARRIER='56dbffcda73fa78539777059f26a964d9b53fa0c'
MATH='8ee639d3aced826aa5b4e39fa6f8bedd3b830327'
CP=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-target-law.json')
LEDGER=Path('runs/substantive_advances.jsonl')
h=lambda b:sha256(b).hexdigest()
base=json.loads((PRIVATE/'baseline.private.json').read_bytes())
prefix=(PRIVATE/'ledger-prefix.raw.jsonl').read_bytes()
assert h(prefix)==base['ledger_prefix_sha256']
assert not (ROOT/'normal-api-attempt-started.json').exists(), 'Never replay this attempt'

def save(name,value):
    (ROOT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

def record_file(path):
    path=Path(path)
    if path.is_symlink():return {'kind':'symlink','target':os.readlink(path)}
    if path.is_file():
        value=path.read_bytes()
        return {'kind':'regular','bytes':len(value),'sha256':h(value),'mode':stat.S_IMODE(path.stat().st_mode)}
    return {'kind':'missing'}

def records_states(raw):
    assert raw.endswith(b'\n')
    records=[json.loads(line) for line in raw.splitlines() if line.strip()]
    return records,adv._replay_advances(records)

def preserve_guard(stage,after=False):
    issues=[]
    raw=LEDGER.read_bytes()
    if raw[:len(prefix)]!=prefix:issues.append('ledger raw prefix changed')
    if not after and raw!=prefix:issues.append('ledger changed before normal API')
    records,states=records_states(raw)
    if {k:v for k,v in states.items() if k!=AID}!=base['all_foreign_states']:
        issues.append('foreign state/nested evidence changed')
    old_v=[x for x in records[:len(prefix.splitlines())] if x.get('event')=='transition' and x.get('to_state')=='VERIFIED']
    if old_v!=base['all_historical_VERIFIED_events_full_original_evidence']:
        issues.append('historical V original event/evidence changed')
    for key,value in base['all_current_VERIFIED_states_full_original_evidence'].items():
        if states.get(key)!=value:issues.append('existing current V full value changed: '+key)
    for path,expected in base['protected_tracked_files'].items():
        if record_file(path)!=expected:issues.append('protected tracked changed: '+path)
    for path,expected in base['all_foreign_frontiers'].items():
        p=Path(path)
        if not p.is_file() or h(p.read_bytes())!=expected['sha256'] or json.loads(p.read_bytes())!=expected['value']:
            issues.append('foreign frontier changed: '+path)
    qraw=subprocess.run(['git','ls-files','--others','--exclude-standard','-z'],capture_output=True,check=True).stdout
    ownprefix=str(OWN.relative_to(REPO))+'/'
    qnames={x.decode() for x in qraw.split(b'\0') if x and not x.decode().startswith(ownprefix)}
    for path,expected in base['foreign_untracked_files'].items():
        if path not in qnames or record_file(path)!=expected:
            issues.append('existing foreign queue file changed/deleted: '+path)
    additions=sorted(qnames-set(base['foreign_untracked_files']))
    added_frontiers=sorted(str(p) for p in Path('research-wiki/frontier-cells').rglob('*.json')
                           if str(p)!=str(CP) and str(p) not in base['all_foreign_frontiers'])
    private={'PRIVATE_DO_NOT_PUBLISH':True,'stage':stage,'issues':issues,
             'new_foreign_queue_paths_allowed':additions,'new_foreign_frontier_paths_allowed':added_frontiers}
    pp=PRIVATE/(stage+'.guards.private.json')
    pp.write_text(json.dumps(private,ensure_ascii=False,indent=2)+'\n');pp.chmod(0o444)
    summary={'stage':stage,'issues':len(issues),'ledger_raw_prefix_unchanged':raw[:len(prefix)]==prefix,
             'all296_foreign_states_and_all_nested_values_unchanged':not any('foreign state' in x for x in issues),
             'all313_historical_V_events_full_evidence_preserved':old_v==base['all_historical_VERIFIED_events_full_original_evidence'],
             'all172_existing_current_V_full_values_preserved':all(states.get(k)==v for k,v in base['all_current_VERIFIED_states_full_original_evidence'].items()),
             'all455_foreign_frontiers_preserved':not any('foreign frontier' in x for x in issues),
             'all128348_protected_tracked_files_preserved':not any('protected tracked' in x for x in issues),
             'all86_existing_foreign_untracked_files_preserved':not any('queue file' in x for x in issues),
             'nonconflicting_new_foreign_untracked_count':len(additions),
             'nonconflicting_new_foreign_frontier_count':len(added_frontiers),
             'private_raw_foreign_data_published':False}
    save(stage+'.guards.json',summary)
    if issues:raise RuntimeError(stage+': preservation failed; private diagnostics retained; do not replay')
    return raw,records,states

assert subprocess.run(['git','rev-parse','HEAD'],capture_output=True,check=True).stdout.decode().strip()==CARRIER
preflight=json.loads((ROOT/'preflight-report.json').read_bytes())
assert preflight['state']=='NORMAL_SOURCEV_PREFLIGHT_PASS'
frozen=json.loads((ROOT/'preflight-freeze-receipt.json').read_bytes())
assert h((ROOT/'preflight-manifest.json').read_bytes())==frozen['manifest_sha256']
for item in json.loads((ROOT/'preflight-manifest.json').read_bytes())['files']:
    assert h((ROOT/item['path']).read_bytes())==item['sha256']
evidence_raw=(ROOT/'planned-original-V-evidence.json').read_bytes()
authorization=json.loads((ROOT/'single-API-input-freeze.json').read_bytes())
assert h(evidence_raw)==authorization['evidence_sha256']
evidence=json.loads(evidence_raw)
assert evidence['verifier_id']==ACTOR and evidence['verified_commit']==CARRIER
adv._validate_transition_evidence('VERIFIED',evidence,schema_version=4)
before_raw,before_records,before_states=preserve_guard('before-normal-API')
assert before_states[AID]==base['own_state']
assert before_states[AID]['state']=='PROVED_LOCAL' and before_states[AID]['owner_id']==PROOF_OWNER
assert CP.read_bytes()==base64.b64decode(base['own_frontier_raw_base64'])
assert 'integration_boundary' not in base['own_frontier_value']['evidence']
marker={'actual_actor':ACTOR,'advance_id':AID,'intended_from':'PROVED_LOCAL','intended_to':'VERIFIED',
        'evidence_sha256':h(evidence_raw),'created_utc':datetime.now(timezone.utc).isoformat(),
        'instruction':'Exactly one actual normal API invocation; never replay after this marker.'}
with (ROOT/'normal-api-attempt-started.json').open('x') as out:
    json.dump(marker,out,ensure_ascii=False,indent=2);out.write('\n')
api_returned=False
api_error=None
try:
    adv.transition_advance(AID,'VERIFIED',worker_id=ACTOR,
                           modes=['independent-source-verification'],evidence=evidence)
    api_returned=True
except BaseException as exc:
    api_error=type(exc).__name__+': '+str(exc)

after_raw=LEDGER.read_bytes()
suffix=after_raw[len(prefix):] if after_raw.startswith(prefix) else b''
lines=suffix.splitlines(keepends=True)
matching=[line for line in lines if (lambda obj:obj.get('advance_id')==AID and obj.get('to_state')=='VERIFIED'
          and obj.get('worker_id')==ACTOR)(json.loads(line))]
if suffix and (len(lines)!=1 or len(matching)!=1):
    pp=PRIVATE/'unexpected-post-API-ledger-suffix.private.jsonl';pp.write_bytes(suffix);pp.chmod(0o444)
result={'api_invocations':1,'api_returned_success':api_returned,'api_error':api_error,
        'matching_actual_events':len(matching),'suffix_lines':len(lines),'C_projected':False}
if len(matching)==1:
    actual=matching[0]
    (ROOT/'actual-normal-VERIFIED-append.exact.jsonl').write_bytes(actual)
    event=json.loads(actual)
    assert event['evidence']==evidence
    save('actual-original-V-evidence.all-keys.json',event['evidence'])
    # Preserve the exact lexical JSON value of the top-level evidence field too.
    text=actual.decode('utf-8');dec=json.JSONDecoder();pos=text.index('{')+1
    while True:
        while text[pos].isspace() or text[pos]==',':pos+=1
        key,end=dec.raw_decode(text,pos);pos=end
        while text[pos].isspace():pos+=1
        assert text[pos]==':';pos+=1
        while text[pos].isspace():pos+=1
        value_start=pos;value,end=dec.raw_decode(text,pos)
        if key=='evidence':
            (ROOT/'actual-original-V-evidence.exact.json').write_bytes(text[value_start:end].encode('utf-8'))
            break
        pos=end
    result['actual_event_sha256']=h(actual)
    result['original_evidence_all_top_level_keys']=list(event['evidence'])
    result['original_evidence_all_nested_values_preserved']=True
    save('actual-normal-API-event.full-object.json',event)
save('normal-API-result.json',result)
if not api_returned or len(lines)!=1 or len(matching)!=1:
    raise RuntimeError('Normal API did not satisfy exact single-event success; retain evidence and do not replay')
_,after_states=records_states(after_raw)
assert {k:v for k,v in after_states.items() if k!=AID}==base['all_foreign_states']
assert after_states[AID]['state']=='VERIFIED' and after_states[AID]['owner_id']==PROOF_OWNER
assert after_states[AID]['last_actor']==ACTOR and after_states[AID]['latest_evidence']==evidence

before_cell_raw=CP.read_bytes()
assert before_cell_raw==base64.b64decode(base['own_frontier_raw_base64'])
before_cell=json.loads(before_cell_raw)
cell=copy.deepcopy(before_cell)
boundary={'kind':'normal-independent-sourceV-only','advance_id':AID,'state':'VERIFIED',
          'verifier_id':ACTOR,'proof_owner':PROOF_OWNER,'checked_metadata_commit':CARRIER,
          'native_mathematical_candidate':MATH,'metadata_carrier_is_not_new_native':True,
          'original_normal_API_event_sha256':h(matching[0]),
          'original_V_evidence_all_top_level_keys_and_nested_values_retained':True,
          'source_review_run_sha256':'f5f3b8e590c824241e7a4691208946a4da26ed51e290c35022eff09de20d7c30',
          'native_judgement_sha256':'de2714b49f2501d815428f1a6e6e22913284328463da37078c2150a2e2d0a8ad',
          'preflight_manifest_sha256':frozen['manifest_sha256'],
          'remaining':'No STAB/global integration/source-index/Registry/site/browser/push/PURIFIED or Goal-completion credit. Only this original verifier may later add post_integration without changing original V evidence.'}
cell['status']='independently_verified'
cell['evidence']['integration_boundary']=boundary
comparison=copy.deepcopy(cell);comparison['status']=before_cell['status'];del comparison['evidence']['integration_boundary']
assert comparison==before_cell and cell['owner_id']==PROOF_OWNER
(ROOT/'frontier.before.exact.json').write_bytes(before_cell_raw)
new_cell_raw=(json.dumps(cell,ensure_ascii=False,indent=2)+'\n').encode()
CP.write_bytes(new_cell_raw)
(ROOT/'frontier.after.exact.json').write_bytes(new_cell_raw)
save('frontier.two-field-closeout.json',{'status':'independently_verified','evidence.integration_boundary':boundary})
assert json.loads(CP.read_bytes())==cell and LEDGER.read_bytes()==after_raw
result['C_projected']=True
result['C_only_status_and_new_integration_boundary_changed']=True
save('normal-API-result.json',result)
preserve_guard('after-normal-API-and-two-field-closeout',after=True)
result['all_preservation_guards_passed']=True
result['state']='SUCCESS_SINGLE_NORMAL_VERIFIED_APPEND_AND_TWO_FIELD_CLOSEOUT'
result['metadata_checked_commit']=CARRIER
result['native_mathematical_candidate']=MATH
result['proof_owner_preserved']=PROOF_OWNER
result['actual_verifier']=ACTOR
result['no_global_STAB_or_completion_credit']=True
save('normal-API-result.json',result)
print(json.dumps({key:result[key] for key in ['state','api_invocations','api_returned_success',
                  'C_projected','all_preservation_guards_passed','actual_event_sha256',
                  'metadata_checked_commit','native_mathematical_candidate','proof_owner_preserved','actual_verifier']},indent=2))
