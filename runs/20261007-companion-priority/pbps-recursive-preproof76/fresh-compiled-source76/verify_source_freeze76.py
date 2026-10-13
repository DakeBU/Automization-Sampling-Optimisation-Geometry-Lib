from pathlib import Path
import datetime, hashlib, json, os

out=Path(__file__).resolve().parent
def sha(b): return hashlib.sha256(b).hexdigest()
freeze_path=out/'source-only.freeze76.json'
freeze=json.loads(freeze_path.read_text(encoding='utf-8'))
receipt=json.loads((out/'write_source_freeze76.foreground-exit.json').read_text(encoding='utf-8'))
assert sha(freeze_path.read_bytes())==receipt['completed_freeze_sha256']
assert receipt['exit_code']==0 and freeze['foreground_writer']['exit_code']==0
assert receipt['writer_pid']==freeze['foreground_writer']['writer_pid']
assert all(v is False for k,v in freeze['anti_anchoring'].items() if k!='source_first_extraction')
raw=(out/'primary-pbps.exactraw.snapshot.html').read_bytes()
m=freeze['primary_source']['raw_manifest']
assert len(raw)==m['source_raw_bytes']==1482128
assert sha(raw)==m['source_raw_sha256']=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
assert sha(raw.replace(b'\r\n',b'\n'))==m['crlf_to_lf_only_sha256']
for fragment in m['fragments']:
    data=(out/fragment['file']).read_bytes()
    assert data==raw[fragment['raw_byte_start']:fragment['raw_byte_end_exclusive']]
    assert sha(data)==fragment['raw_sha256']
    assert sha(data.replace(b'\r\n',b'\n'))==fragment['crlf_to_lf_only_sha256']
for artifact in freeze['own_artifacts']:
    data=(out/artifact['file']).read_bytes()
    assert len(data)==artifact['bytes'] and sha(data)==artifact['sha256']
slots=json.loads((out/'source-seven-slots76.json').read_text(encoding='utf-8'))['slots']
assert set(slots)=={'objects','domains','quantifiers','assumptions','conclusion','scopes_senses','constant_dependencies'}
coverage=json.loads((out/'source-coverage76.json').read_text(encoding='utf-8'))
index=json.loads((out/'source-dom-index76.json').read_text(encoding='utf-8'))
assert {x['id'] for x in coverage['inventory']}=={x['id'] for x in index}
assert all(x['disposition'] in {'NODE','EXCLUDED'} and x['reason'].strip() for x in coverage['inventory']+coverage['subclaim_inventory']+coverage['external_citation_inventory'])
assert all(any(x['id']==sid for x in coverage['inventory']) for sid in ['A1.E1','A1.E2','A1.Ex4','A1.Ex5','A1.Ex6','A1.Ex7','A1.Ex8','bib.bib16'])
graph=json.loads((out/'source-proof-graph76.json').read_text(encoding='utf-8'))
node_ids={x['id'] for x in graph['nodes']}
assert all(e['consumer'] in node_ids and all(p in node_ids for p in e['parents']) for e in graph['hyperedges'])
result={'status':'PASS_SOURCE_ONLY_ARTIFACT_INTEGRITY','pid':os.getpid(),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'freeze_sha256':sha(freeze_path.read_bytes()),'foreground_source_writer_pid':receipt['writer_pid'],'foreground_source_writer_actual_exit':receipt['exit_code'],'coverage_counts':coverage['counts'],'seven_slots_present':True,'source_fragments_exact':True,'candidate_or_old_verdict_seen':False,'mathematical_admission':'OPEN; integrity checks are not independent topology certification or Lean/source equivalence.'}
(out/'source-only-integrity76.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
