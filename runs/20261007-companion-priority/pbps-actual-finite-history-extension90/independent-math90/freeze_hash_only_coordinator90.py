from pathlib import Path
import datetime,hashlib,json
R=Path('E:/Samplinglib');O=Path(__file__).parent
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def put(n,v):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
put('coordinator-historical-hash90.negative.json',{'tool_chunk':'1a0144','exit_code':1,'kind':'HASH_ONLY_COORDINATOR_EVOLUTION_BEFORE_ORIGINAL_SNAPSHOT','expected_historical_draft_audit_raw':'b130806b77fc1b3ec3c4799e36f77fc1cde2c7b275c1465a1db27ed0bd1f93c4','observed_current_audit_raw':'c623aa7dde64d17fa772cec53e70d4aae769b46016100ffa7090df79b17a1427','stopped_before_JSON_semantic_content_read':True,'no_mathematical_or_Lean_failure':True,'original_freeze_not_overwritten':True})
freeze=json.loads((O/'publication-freeze90.original.exactraw.json').read_text('utf8'))
rows=[]
for d in freeze['inputs']:
 if not d['path'].startswith(('research-wiki/semantic-roundtrip/','research-wiki/frontier-cells/')):continue
 p=R/d['path'];b=p.read_bytes();got=hashlib.sha256(b).hexdigest()
 kind='audit' if '/audits/' in d['path'] else 'cell'
 q=O/f'.private.coordinator-{kind}90.observed.exactraw.json'
 with q.open('xb') as out:out.write(b)
 rows.append({'canonical_path':d['path'],'historical_expected_raw':d['raw_sha256'],'observed_hash_only_snapshot':pin(q),'historical_original_matched':got==d['raw_sha256'],'read_mode':'Exact byte hash and lossless snapshot only; JSON content and decoder/source assessments not consulted.'})
put('hash-only-coordinator-input90.snapshot-index.json',{'status':'HASH_ONLY_OBSERVATIONS_WITH_HISTORICAL_EVOLUTION_DISCLOSED','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'records':rows,'not_mathematical_or_source_review_evidence':True,'original_draft_audit_snapshot_resolution_pending_root_pointer':True,'historical_root_freeze_left_immutable':True})
print(json.dumps({'records':[{'kind':x['canonical_path'],'matched':x['historical_original_matched'],'observed':x['observed_hash_only_snapshot']['raw_sha256']} for x in rows]},indent=2))
