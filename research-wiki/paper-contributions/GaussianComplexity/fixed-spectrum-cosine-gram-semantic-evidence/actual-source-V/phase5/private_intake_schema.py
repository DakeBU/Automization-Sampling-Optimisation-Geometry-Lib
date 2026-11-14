#!/opt/anaconda3/bin/python
import hashlib,json,pathlib,sys
sys.dont_write_bytecode=True
ROOT=pathlib.Path('/Users/zhouhuanjian/ASTIS-GC');BASE=pathlib.Path(__file__).resolve().parent
PRIVATE=BASE.parent/'private-phase5-preservation';PRIVATE.mkdir(exist_ok=True,mode=0o700)
W=ROOT/'.astis/huanjian-gc-fixed-spectrum-cosine-gram-20261110'
schemas=[]
for name in ['intake-baseline.private.json','intake-tracked-private-preservation.json']:
    data=(W/name).read_bytes();(PRIVATE/name).write_bytes(data)
    obj=json.loads(data)
    schemas.append({'input':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
                    'top_schema':{k:{'type':type(v).__name__,'length':len(v) if hasattr(v,'__len__') else None} for k,v in obj.items()}})
ledger=ROOT/'runs/substantive_advances.jsonl';raw=ledger.read_bytes();assert not raw or raw.endswith(b'\n')
(PRIVATE/'ledger-before.raw.jsonl').write_bytes(raw)
records=[json.loads(line) for line in raw.splitlines() if line.strip()]
sys.path.insert(0,str(ROOT));from tools import astis_advance as adv
states=adv._replay_advances(records)
ADV='ASTIS-SA-20261110-GaussianComplexityFixedSpectrumCosineGram'
own=states[ADV];assert own['state']=='PROVED_LOCAL'
assert own['owner_id']=='huanjian_gc_20261110_fixed_spectrum_cosine_gram'
matches=[(line,json.loads(line)) for line in raw.splitlines(keepends=True) if line.strip() and json.loads(line).get('advance_id')==ADV and json.loads(line).get('to_state')=='PROVED_LOCAL']
assert len(matches)==1
pline,plocal=matches[0]
(BASE/'original-PROVED_LOCAL-event.exact.jsonl').write_bytes(pline)
(BASE/'original-PROVED_LOCAL-evidence.json').write_text(json.dumps(plocal['evidence'],ensure_ascii=False,indent=2)+'\n')
(PRIVATE/'full-states-before.json').write_text(json.dumps(states,ensure_ascii=False,indent=2)+'\n')
vs=[r for r in records if r.get('event')=='transition' and r.get('to_state')=='VERIFIED']
frontier=ROOT/'research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-cosine-gram.json'
fbytes=frontier.read_bytes();(BASE/'own-frontier-before.raw.json').write_bytes(fbytes)
summary={'private_guard_inputs_process_schema_only':schemas,'whole_ledger_bytes_before':len(raw),
         'whole_ledger_sha256_before':hashlib.sha256(raw).hexdigest(),'whole_ledger_record_count':len(records),
         'whole_repository_prior_VERIFIED_event_count':len(vs),'local_packet_prior_V_count_is_not_the_whole_ledger_count':True,
         'prior_VERIFIED_distinct_advances':len({r['advance_id'] for r in vs}),
         'all_current_advances':len(states),'foreign_current_advances':len(states)-1,
         'own_state':own['state'],'own_owner':own['owner_id'],
         'original_PLOCAL_event_sha256':hashlib.sha256(pline).hexdigest(),
         'private_snapshot_scope':'Full raw ledger/foreign states/control guard inputs remain private outside portable phase5.'}
(BASE/'private-intake-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
print('OWN_PLOCAL_EVENT',json.dumps(plocal,ensure_ascii=False,indent=2))
print('OWN_FRONTIER',fbytes.decode())
