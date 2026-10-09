import hashlib,json,os,pathlib,sys
sys.dont_write_bytecode=True
from snapshot_named_inputs import snapshot
out=pathlib.Path(__file__).resolve().parent
source=out.parent/'final-reader-repository-packet69.json'
packet_sha='8bd48315996481ca610699deecaf5add6ccee521fbd003923b466785e5aedd67'
packet_raw=source.read_bytes();assert hashlib.sha256(packet_raw).hexdigest()==packet_sha
packet=json.loads(packet_raw);assert len(packet['inputs'])==108
assert packet['actual_root_pid']==39720 and packet['checked_science_commit']=='2d286c283a6fb5dfc13180204bb0da54531a5c67'
inputs=[snapshot(out,source,'final-reader-repository-packet69.RAW.json','frozen final root packet',packet_sha)]
for i,e in enumerate(packet['inputs']):
    path=pathlib.Path(e['path']);raw=path.read_bytes()
    assert len(raw)==e['RAW_bytes'] and hashlib.sha256(raw).hexdigest()==e['RAW_sha256'],str(path)
    assert hashlib.sha256(raw.replace(b'\r\n',b'\n')).hexdigest()==e['LF_sha256'],str(path)
    binary=path.suffix.lower() in {'.png','.jpg','.jpeg','.gif','.webp','.pdf'}
    entry=snapshot(out,path,'current.%03d.%s'%(i,path.name),'final packet named current input',e['RAW_sha256'],binary)
    entry['packet_declared_LF_sha256']=e['LF_sha256']
    entry['packet_declared_LF_recipe']='CRLF-to-LF only, recorded literally from root packet; binary image remains RAW in this reviewer payload'
    inputs.append(entry)
previous=json.loads((out/'input-manifest.json').read_text(encoding='utf-8'))
manifest=dict(schema='repository-reader69-complete-finite-current-input-manifest-v1',
    count=len(previous['inputs'])+len(inputs),prior_frozen_inputs=previous['inputs'],final_current_inputs=inputs,
    final_packet_received=True,final_root_input_count=108,final_root_packet_RAW_sha256=packet_sha,
    text_LF_recipe='only CRLF-to-LF; lone CR preserved',binary_policy='RAW only; no LF transformation')
(out/'final-input-manifest.json').write_text(json.dumps(manifest,sort_keys=True,indent=2)+'\n',encoding='utf-8')
(out/'final-input-ingest.json').write_text(json.dumps(dict(actual_pid=os.getpid(),all_108_RAW_hashes_sizes_and_declared_LF_hashes_verified=True,
    complete_named_inputs=manifest['count'],all_binary_screenshots_preserved_RAW=True,root_packet_RAW_sha256=packet_sha),sort_keys=True,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(actual_pid=os.getpid(),final_root_inputs=108,complete_named_inputs=manifest['count'],packet_RAW_sha256=packet_sha),sort_keys=True))
