from pathlib import Path
import json,hashlib
ROOT=Path('E:/Samplinglib');R=ROOT/'runs/20261007-companion-priority/pbps-rough-mean-gradient56';O=R/'source-review56'
def canon(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n'))}
def put(name,v):
 v['content_self_sha256']=sha(canon(v));p=O/name;p.write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode());assert json.loads(p.read_bytes())==v;return pin(p)
opening=json.loads((O/'initial-source-lease.raw.snapshot.json').read_bytes())
assert (R/'source.review.lease.json').read_bytes()==(O/'initial-source-lease.raw.snapshot.json').read_bytes()
for p in opening['input_artifacts']:
 a=pin(ROOT/p['path']);assert all(a[k]==p[k] for k in ['bytes','raw_sha256','lf_sha256'])
packet=json.loads((R/'source.0.reviewer-packet.json').read_bytes());result=json.loads((O/'result0.json').read_bytes());run=json.loads((O/'reviewer.source.run.json').read_bytes())
assert set(result)==set(packet['output_contract'])
assert result['reviewer']=='/root/next_primary56' and result['reviewer_packet_sha256']==packet['packet_sha256']
assert result['independent_from_formalizer'] and result['independent_from_decoder']
assert set(result['semantic_slots'])==set(packet['review_contract']['semantic_slots'])
for value in result['semantic_slots'].values():
 assert set(value)=={'original','reconstructed','relation','evidence'} and value['relation'] in packet['review_contract']['slot_relations'] and all(value.values())
assert result['verdict'] in packet['review_contract']['verdicts']
assert result['review_run_sha256']==run['run_sha256']==sha(canon({k:v for k,v in run.items() if k!='run_sha256'}))
for p in [O/'source.review.json',O/'decoder-locator-review56/review.json',O/'decoder-locator-review56/reviewer.operational.run.json',O/'decoder-locator-review56/lease.open.json',O/'decoder-locator-review56/lease.json']:
 j=json.loads(p.read_bytes());assert sha(canon({k:v for k,v in j.items() if k!='content_self_sha256'}))==j['content_self_sha256']
put('verification-history.json',{'schema_version':1,'status':'ALL_FINAL_CHECKS_PASS','original_open_scope_preserved':True,'diagnostic_history':[{'chunk_id':'63cb8c','exit_code':1,'reason':'gbk stdout encoding for Unicode packet; corrected by explicit UTF8 stdout. Final-stage packet whole-module exposure on successful followup e28044 is recorded.'},{'chunk_id':'a1a0c2','exit_code':1,'reason':'Byte equality check found physical terminal space before :=by versus sealed final LF. Exact normalized header verified, physical prefix preserved; no statement mutation.'},{'chunk_id':'e38368','exit_code':1,'reason':'Verifier expected result.packet_sha256 but native decoder standard result does not contain it; use actual bound packet and reviewer blind_reconstruction.decoder_packet_sha256, no decoder schema rewrite.'},{'chunk_id':'d316b6','exit_code':1,'reason':'Verifier mistakenly included root-added binding-receipt among native decoder originals. Native five originals checked separately; no missing native artifact.'},{'chunk_id':'f5b995','exit_code':1,'reason':'Review script copied primary raw hash with one wrong character; actual primary and432 pins unchanged, checked hash corrected before outputs.'},{'chunk_id':'2d754f','exit_code':0,'reason':'Final all432 exactraw/LF input check and6 locator checks passed.'},{'chunk_id':'299d8d','exit_code':0,'reason':'Independent locator review CLOSED LAST.'},{'chunk_id':'4b614d','exit_code':0,'reason':'Source standard result/native run/report emitted and actual readbacks passed.'}],'compiler_started':False,'canonical_files_written':False})
files=sorted(p for p in O.rglob('*') if p.is_file() and p.name not in ['manifest.json','complete.json'])
pins=[pin(p) for p in files]
manifest=put('manifest.json',{'schema_version':1,'actor':'/root/next_primary56','status':'COMPLETE_EXACT_OUTPUT_READBACK_MANIFEST','input_count':432,'output_count':len(pins),'outputs':pins,'excludes':['manifest.json','complete.json','root source.review.lease.json final closure'],'hash_recipe':'Complete object minus only content_self_sha256. Every listed receipt is physical bytes and physical CRLF-to-LF bytes; snapshots are actual readbacks.'})
complete=put('complete.json',{'schema_version':1,'actor':'/root/next_primary56','status':'COMPLETE','semantic_verdict':result['verdict'],'reviewer_packet_sha256':packet['packet_sha256'],'publication_binding_sha256':packet['publication_binding_sha256'],'manifest':manifest,'standard_result':pin(O/'result0.json'),'native_run':pin(O/'reviewer.source.run.json'),'native_run_complete_minus_run_sha256':run['run_sha256'],'source_report':pin(O/'source.review.json'),'operational_repair':pin(O/'decoder-locator-review56/review.json'),'operational_repair_closed_lease':pin(O/'decoder-locator-review56/lease.json'),'all432_inputs_rechecked':True,'all_output_readbacks_checked':True,'named_payload_hashes':'None in this reviewer native run/report/manifest/complete. Creator sourcegraph self_digest payload_bytes/payload_hash terminology refers to COMPLETE object minus self_digest, as prior separate review established; not a selected component or raw file.','compiler':'NOT_STARTED_CLOSED','source_boundaries':'WeakH1/fullB13/Gamma/halfturn/main/errors/cost/composition open; no Lean/math/aggregate gate admission.','final_root_lease':'Still OPEN; distinct next synchronous finalizer performs rechecks and writes it CLOSED LAST after this process actual EXIT0.'})
for p in [O/'manifest.json',O/'complete.json']:
 j=json.loads(p.read_bytes());assert sha(canon({k:v for k,v in j.items() if k!='content_self_sha256'}))==j['content_self_sha256']
print(json.dumps({'status':'SEALED_READY_FOR_FINAL_CLOSURE','outputs':len(pins),'manifest':manifest,'complete':complete}))
