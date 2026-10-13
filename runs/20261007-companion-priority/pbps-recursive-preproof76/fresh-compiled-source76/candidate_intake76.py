from pathlib import Path
import hashlib, json, os, datetime
out=Path(__file__).resolve().parent
freeze_path=Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-actual-finite-jump-recursion76/source-review.freeze76.json')
freeze_raw=freeze_path.read_bytes()
freeze=json.loads(freeze_raw.decode('utf-8'))
assert freeze['input_count']==15 and len(freeze['inputs'])==15
copies=[]
for i,pin in enumerate(freeze['inputs'],1):
    data=Path(pin['path']).read_bytes()
    assert len(data)==pin['RAW_bytes']
    assert hashlib.sha256(data).hexdigest()==pin['RAW_sha256']
    assert hashlib.sha256(data.replace(b'\r\n',b'\n')).hexdigest()==pin['LF_sha256']
    name='candidate-input'+str(i).zfill(2)+'.raw'
    assert not (out/name).exists()
    (out/name).write_bytes(data)
    copies.append({**pin,'own_raw_copy':name})
hash_only=[]
for pin in freeze['hash_only_coordinator_pins']:
    data=Path(pin['path']).read_bytes()
    assert len(data)==pin['RAW_bytes']
    assert hashlib.sha256(data).hexdigest()==pin['RAW_sha256']
    assert hashlib.sha256(data.replace(b'\r\n',b'\n')).hexdigest()==pin['LF_sha256']
    hash_only.append({**pin,'content_decoded':False,'content_inspected':False,'read_operation':'bytes for digest only; no copy retained'})
(out/'candidate-dispatch.freeze76.raw.json').write_bytes(freeze_raw)
packet=json.loads((out/'candidate-input01.raw').read_text(encoding='utf-8'))
result={'status':'PINNED_15_INPUTS_MATCH','pid':os.getpid(),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_only_freeze_sha256':freeze['source_only_freeze_before_candidate']['RAW_sha256'],'freeze_raw_sha256':hashlib.sha256(freeze_raw).hexdigest(),'canonical_reviewer_packet_sha256':freeze['canonical_reviewer_packet_sha256'],'publication_binding_sha256':freeze['publication_binding_sha256'],'readable_inputs':copies,'hash_only_inputs':hash_only,'packet_top_level_keys':list(packet)}
(out/'candidate-intake76.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['readable_inputs','hash_only_inputs']},ensure_ascii=False,indent=2))
