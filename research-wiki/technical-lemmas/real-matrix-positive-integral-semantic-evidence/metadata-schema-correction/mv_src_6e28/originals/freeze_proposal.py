from pathlib import Path
import json,hashlib
from datetime import datetime,timezone
R=Path('/Users/zhouhuanjian/ASTIS-GC');B=R/'.astis/semantic-neutral-20261112/mv_src_6e28/metadata-schema-correction';CELL=R/'research-wiki/frontier-cells/ASTIS-SHARED-REAL-MATRIX-POSITIVE-INTEGRAL.json';DEST='research-wiki/technical-lemmas/real-matrix-positive-integral-semantic-evidence/metadata-schema-correction/mv_src_6e28/originals'
def rec(p):
 a=p.read_bytes();return {'path':str(p.relative_to(R)),'bytes':len(a),'sha256':hashlib.sha256(a).hexdigest()}
def wr(n,d):
 with (B/n).open('x') as f:f.write(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
assert CELL.read_bytes()==(B/'inputs/C23.original.exact.json').read_bytes()
assert json.loads((B/'isolated-schema-validation.json').read_bytes())['proposed_errors']==[]
wr('originals-manifest.json',{'phase':'S independent verifier metadata serialization correction proposal only','files':[rec(p) for p in sorted(q for q in B.rglob('*') if q.is_file())],'self_hash_external':True,'no_shared_apply_or_V_replay':True})
wr('PROPOSAL-FROZEN.json',{'schema_version':1,'phase':'S_METADATA_SCHEMA_CORRECTION_PROPOSAL_FROZEN_NOT_APPLIED','frozen_utc':datetime.now(timezone.utc).isoformat(),'reviewer':'/root/mv_fresh_source_6e28','shared_cell':str(CELL.relative_to(R)),'original':rec(B/'inputs/C23.original.exact.json'),'proposed_full_bytes':rec(B/'C23.proposed.exact.json'),'unified_diff':rec(B/'C23.proposed.unified.diff'),'json_pointer_diff':rec(B/'proposed-json-pointer-diff.json'),'independent_no_replay_decision':rec(B/'independent-correction-decision.json'),'isolated_actual_schema_check':rec(B/'isolated-schema-validation.json'),'originals_manifest':rec(B/'originals-manifest.json'),'only_delta':'requiredstring evidence.independent_verification plus exactold dict under independent_verification_details','status_owner_source_math_unchanged':True,'new_normal_API_calls':0,'new_V_or_ledger_events':0,'shared_C23_ledger_git_applied_by_this_role':False,'original_V_payload_and_append_unmodified':True,'carrier_rule':'Only after separate authorization, carry exact proposed C23 bytes and these original records; never replay original V or edit prior evidence. No other C/source/state authorized.','self_hash_external':True})
rr=[]
for p in sorted(q for q in B.rglob('*') if q.is_file()):
 x=rec(p);rr.append({'source_path':x['path'],'destination_path':DEST+'/'+str(p.relative_to(B)),'bytes':x['bytes'],'sha256':x['sha256'],'copy_rule':'Exact original metadata proposal/evidence only; proposed full C23 is not automatically applied by this archive.'})
wr('portable-originals-manifest.json',{'records':rr,'files':len(rr),'bytes':sum(x['bytes'] for x in rr),'self_hash_external':True,'postseal_envelope':'Later freeze receipt/stdoutstderr and postseal-output-index separately externalhash bound','no_V_replay':True,'no_shared_apply':True})
for p in [B/'C23.proposed.exact.json',B/'C23.proposed.unified.diff',B/'independent-correction-decision.json',B/'originals-manifest.json',B/'PROPOSAL-FROZEN.json',B/'portable-originals-manifest.json']:print(json.dumps(rec(p)))
