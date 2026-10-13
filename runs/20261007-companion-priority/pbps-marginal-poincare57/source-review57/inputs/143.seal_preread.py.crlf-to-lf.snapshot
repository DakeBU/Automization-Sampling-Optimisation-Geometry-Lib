from pathlib import Path
import json,hashlib
ROOT=Path('E:/Samplinglib');O=Path(__file__).parent
def canon(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n'))}
def put(name,v):
 v['content_self_sha256']=sha(canon(v));p=O/name;p.write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode());assert json.loads(p.read_bytes())==v;return pin(p)
def check_pin(v):
 a=pin(ROOT/v['path']);assert all(a[k]==v[k] for k in ['bytes','raw_sha256','lf_sha256']),v
def scan(v):
 if isinstance(v,dict):
  if {'path','bytes','raw_sha256','lf_sha256'}<=set(v):check_pin(v)
  for x in v.values():scan(x)
 elif isinstance(v,list):
  for x in v:scan(x)
source=json.loads((O/'primary.contract.json').read_bytes());anchors=json.loads((O/'source-anchor-manifest.json').read_bytes())
for f in ['source-anchor-manifest.json','primary.contract.json','public-contracts.complete-receipts.json','source.precision-addendum.json','next-consumer.blueprint.json','reviewer.primary.run.json']:
 v=json.loads((O/f).read_bytes());assert sha(canon({k:x for k,x in v.items() if k!='content_self_sha256'}))==v['content_self_sha256'];scan(v)
raw=(O/'primary-pbps.exactraw.snapshot.html').read_bytes()
for a in anchors['anchors']:
 b=(ROOT/a['exactraw']['path']).read_bytes();assert raw[a['source_start_utf8_byte']:a['source_end_utf8_byte_exclusive']]==b
 assert (ROOT/a['crlf_to_lf']['path']).read_bytes()==b.replace(b'\r\n',b'\n')
assert len(anchors['anchors'])==21
source_inputs=[ROOT/'runs/20261007-companion-priority/phase-pbps-primary-preread56'/f for f in ['primary-pbps.raw.snapshot.html','primary.contract.json','lease.json','A3.SS1.raw.html','A3.SS2.raw.html','A2.SS1.raw.html','A2.SS2.raw.html','A4.SS1.raw.html','A4.SS2.raw.html','S1.p1.raw.html','S1.p2.raw.html','S2.SS2.raw.html']]
source_inputs+=[ROOT/'website/content/samplewiki_companion_frontiers.json',ROOT/'docs/companion-papers-handoff.md',ROOT/'.agents/skills/astis-source-dependency-audit/SKILL.md',ROOT/'tools/astis_advance.py']
records=json.loads((O/'public-contracts.complete-receipts.json').read_bytes())['files'];source_inputs+=[ROOT/r['source_file']['path'] for r in records]
inputpins=[pin(p) for p in source_inputs]
for p in [ROOT/'website/content/samplewiki_companion_frontiers.json',ROOT/'docs/companion-papers-handoff.md']:
 b=p.read_bytes();(O/(p.stem+'.exactraw.snapshot')).write_bytes(b);(O/(p.stem+'.crlf-to-lf.snapshot')).write_bytes(b.replace(b'\r\n',b'\n'))
put('input-manifest.json',{'schema_version':1,'actor':'/root/next_primary56','status':'ALL_INPUT_PINS_READBACK_VERIFIED','input_count':len(inputpins),'inputs':inputpins,'capsule_stdout':pin(O/'capsule.raw.snapshot.json'),'capsule_utf8_process':{'chunk_id':'a6b765','exit_code':0,'subprocess_returncode':0,'compiler_started':False},'source_raw_and21_balanced_anchor_spans_verified':True,'public_contract_extract_count':8,'candidate57_exposure':'NONE'})
schema={'$schema':'https://json-schema.org/draft/2020-12/schema','title':'Independent primary-first PBPS57 native source contract','type':'object','required':['schema_version','actor','status','source','standing_assumptions','objects','exact_formulae','source_dependency_graph','gradient_laplacian_convention','remaining_boundaries','chronology','compiler_started','formal_admission','content_self_sha256'],'properties':{'schema_version':{'const':1},'actor':{'const':'/root/next_primary56'},'status':{'const':'PRIMARY_ONLY_SOURCE_CONTRACT_SEALED'},'compiler_started':{'const':False},'formal_admission':{'const':False},'content_self_sha256':{'type':'string','pattern':'^[0-9a-f]{64}$'}}}
(O/'primary.contract.schema.json').write_text(json.dumps(schema,indent=2)+'\n',encoding='utf-8',newline='\n')
assert all(k in source for k in schema['required']) and source['status']=='PRIMARY_ONLY_SOURCE_CONTRACT_SEALED' and not source['compiler_started'] and not source['formal_admission']
outputs=[pin(p) for p in sorted(O.iterdir()) if p.is_file() and p.name not in ['manifest.json','complete.json','lease.json']]
manifest=put('manifest.json',{'schema_version':1,'actor':'/root/next_primary56','status':'COMPLETE_OUTPUT_READBACK_MANIFEST','outputs':outputs,'output_count':len(outputs),'exclusions':['manifest.json','complete.json','lease.json'],'hash_recipe':'Complete native object excluding only content_self_sha256; UTF8 ensure_asciiFalse ordinal sorted keys compact comma/colon, no newline. Raw physical bytes and CRLF->LF receipts distinct. No selected named payload.'})
complete=put('complete.json',{'schema_version':1,'actor':'/root/next_primary56','status':'SOURCE_ONLY_COMPLETE_READY_FOR_CLOSURE','primary_contract':pin(O/'primary.contract.json'),'blueprint':pin(O/'next-consumer.blueprint.json'),'native_run':pin(O/'reviewer.primary.run.json'),'inputs':pin(O/'input-manifest.json'),'manifest':manifest,'balanced_anchor_count':21,'source_only_outcome':'Gamma_P defect-root definition/inverse scope corrected; actual nu Poincare C3 consumer/reuse blueprint, no theorem proof/admission.','candidate57_exposure':'NONE','compiler_lease':'NOT_STARTED_CLOSED','formal_admission':False,'source_weakH1_Gamma_root_inverse_halfturn_residuals_preserved':True,'final_closure':'Separate finalizer after actual seal EXIT0, final lease CLOSED LAST.'})
print(json.dumps({'status':'SOURCE_ONLY_COMPLETE','input_count':len(inputpins),'output_count':len(outputs),'manifest':manifest,'complete':complete}))
