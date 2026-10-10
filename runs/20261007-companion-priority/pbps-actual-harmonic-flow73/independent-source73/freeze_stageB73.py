from pathlib import Path
from html.parser import HTMLParser
import copy, hashlib, json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path('E:/Samplinglib')
BASE=ROOT/'runs/20261007-companion-priority/pbps-actual-harmonic-flow73'
OWN=BASE/'independent-source73'
OLD=ROOT/'runs/20261007-companion-priority/pbps-harmonic-flow-preproof73/independent-header-source73'
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_sha256':sha(b.replace(b'\r\n',b'\n')),'LF_recipe':'CRLF byte pairs -> LF only; preserve every other byte'}
def write(n,x):
 p=OWN/n;assert not p.exists();p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
assert not(OWN/'lease.final.json').exists()
freeze=load(BASE/'source-review.freeze73.json');assert len(freeze['inputs'])==7
inputs=[]
for i,r in enumerate(freeze['inputs']+[freeze['native_reconstruction']]):
 p=Path(r['path']);b=p.read_bytes();assert len(b)==r['RAW_bytes'] and sha(b)==r['RAW_sha256'];assert sha(b.replace(b'\r\n',b'\n'))==r['LF_sha256']
 d=OWN/'current-inputs';d.mkdir(exist_ok=True)
 (d/f'{i}.exactraw.snapshot').write_bytes(b);(d/f'{i}.LF.snapshot').write_bytes(b.replace(b'\r\n',b'\n'))
 inputs.append({**pin(p),'RAW_snapshot':f'current-inputs/{i}.exactraw.snapshot','LF_snapshot':f'current-inputs/{i}.LF.snapshot'})
packet=load(BASE/'source-review.packet.json');core=copy.deepcopy(packet);packet_hash=core.pop('packet_sha256');assert sha(canon(core))==packet_hash
audit=load(ROOT/inputs[1]['path'])
sys.path.insert(0,str(ROOT/'tools'));import astis_semantic_roundtrip_core as semantic
assert semantic.semantic_reviewer_packet(audit)==packet
module=(ROOT/packet['lean']['file']).read_bytes();assert sha(module)=='506c1d57b3c9133db1cfc0515dccbd8759aaec3e1dbf4a128f6a73d3aeb73c8c'
lines=module.splitlines(keepends=True);assert len(lines)==178
pub=load(ROOT/inputs[4]['path'])['items'][0];lesson=load(ROOT/inputs[5]['path'])['units'][0];binding=pub['bindings'][0]
payload={
 'file':sha(module),'current_lean_module':module.decode(),
 'toolchain':sha((ROOT/'lean-toolchain').read_bytes().decode().replace('\r\n','\n').encode()),
 'dependencies':sha((ROOT/'lake-manifest.json').read_bytes().decode().replace('\r\n','\n').encode()),
 'source':pub['source'],'statement':pub['statement'],'formulae':pub['formulae'],'assumptions':pub['assumptions'],
 'obligations':pub['obligations'],'lesson':lesson,
 'binding':{k:v for k,v in binding.items() if k not in {'audit_id','legacy_audit_debt'}}}
assert sha(canon(payload))==packet['publication_binding_sha256']==audit['publication_binding_sha256']
context=copy.deepcopy(payload);context['binding']={k:context['binding'][k] for k in ('declaration','role','supports')};context['lesson']={k:v for k,v in context['lesson'].items() if k not in {'boundary','source_history_boundary'}};context['candidate_assumptions']=[{k:r[k] for k in ('source','lean')} for r in binding['assumption_deltas']]
assert context==packet['candidate_publication_context']==audit['publication_context']
spans=[]
for i,s in enumerate(lesson['steps']):
 r=s['lean_source_region'];code=b''.join(lines[r['start_line']-1:r['end_line']]);assert sha(code)==r['exact_code_raw_sha256'];assert code.decode()==s['lean'];assert r['source_raw_sha256']==sha(module)
 spans.append({'index':i,'title':s['title'],'start_line':r['start_line'],'end_line':r['end_line'],'RAW_sha256':sha(code),'LF_sha256':sha(code.replace(b'\r\n',b'\n')),'formula':s['formula'],'exact_code_matches':True})
assert len(spans)==6 and [r['start_line'] for r in spans]==[98,111,128,146,149,166]
write('StageB.exact-six-BODY-spans73.json',{'module':pin(ROOT/packet['lean']['file']),'spans':spans,'count':6,'full_context_also_read':True})
primary=ROOT/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html';raw=primary.read_bytes();assert sha(raw)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
anchor_rows=[]
for anchor in ['A1','A1.SS1','alg1','S3.E4','S3.E6','S3.E7','S4.E5']:
 a=raw.index(('id="'+anchor+'"').encode());b=a+min(800,len(raw)-a);fragment=raw[a:b]
 anchor_rows.append({'id':anchor,'RAW_start':a,'RAW_end_exclusive':b,'RAW_sha256':sha(fragment),'exact_RAW_utf8':fragment.decode()})
write('StageB.source-URL-anchor-accuracy73.json',{'primary':pin(primary),'publication_URL':pub['source']['url'],'lesson_URLs':[r['url'] for r in lesson['sources']],'anchor_exists':True,'A1_title':'Appendix A Conditional half-turn process: construction, invariance, and implementation','A1_SS1_title':'A.1 The fixed-reference phase space process','decision':'#A1 is an accurate broad parent anchor containing A.1 and the exact flow/energy source. More specific #A1.SS1 is optional; no correction required. Source also explicitly cites Algorithm1 and Section3.','network_refetch':False,'fragments':anchor_rows})
extra=[BASE/'source-review.freeze73.json',ROOT/'tools/astis_semantic_roundtrip_core.py',ROOT/'tools/astis_publication.py',ROOT/'lean-toolchain',ROOT/'lake-manifest.json']
write('StageB.finite-current-inputs73.json',{'current_frozen_inputs':inputs,'current_count':8,'protocol_and_freeze_inputs':[pin(p) for p in extra],'old_source_contract_refs':pin(OWN/'preparation.source-contract-inputs73.json'),'primary_reference':pin(primary),'canonical_packet_sha256':packet_hash,'packet_RAW_sha256':inputs[0]['RAW_sha256'],'publication_binding_sha256':packet['publication_binding_sha256'],'review_context_sha256':sha(canon(context)),'canonical_semantic_reviewer_packet_regeneration_equal':True,'publication_binding_and_context_verified':True,'coverage_metadata_outside_binding_payload_by_current_tools_lines82_117':True,'audit_previous_slots_deltas_verdict_not_used_as_judgment':True,'LF_recipe':'CRLF byte pairs -> LF only; preserve every other byte'})
write('StageB.freeze-current.terminal.json',{'actual_pid':os.getpid(),'exit_code':0,'background':False,'argv':sys.argv})
print(json.dumps({'actual_pid':os.getpid(),'exit_code':0,'current_inputs':8,'module_lines':178,'six_BODY_spans_exact':True,'canonical_packet_sha256':packet_hash,'publication_binding_sha256':packet['publication_binding_sha256'],'context_sha256':sha(canon(context)),'frozen_input_manifest':pin(OWN/'StageB.finite-current-inputs73.json')},indent=2))
