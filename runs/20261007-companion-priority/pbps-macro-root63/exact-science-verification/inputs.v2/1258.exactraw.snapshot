import hashlib,json,os
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(r'E:\Samplinglib')
RUN=ROOT/'runs/20261007-companion-priority/pbps-macro-root63'
OUT=RUN/'independent-source63'
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def load(p):return json.loads(p.read_text(encoding='utf-8'))
packet=load(OUT/'candidate-input-00.exactraw.snapshot.json')
expo=load(OUT/'candidate-input-01.exactraw.snapshot.json')
codes=load(OUT/'candidate-input-02.exactraw.snapshot.json')
supp=load(OUT/'candidate-input-03.exactraw.snapshot.json')
overlay=load(OUT/'candidate-input-04.exactraw.snapshot.json')
adoption=load(OUT/'candidate-input-05.exactraw.snapshot.json')
source_manifest=load(OUT/'primary-only.input.manifest.json')
source=ROOT/source_manifest['source_primary']['path']
assert sha(source.read_bytes())==source_manifest['source_primary']['raw_sha256']
checks={'foreground_verifier_pid':os.getpid(),'executed_utc':datetime.now(timezone.utc).isoformat(),'compiler_started':False,'source_primary_verified':True}
for key,field in [('source','original_text'),('lean','statement')]:
 expected=packet[key]['text_sha256' if key=='source' else 'statement_sha256']
 assert sha(packet[key][field].encode('utf-8'))==expected
assert sha(canonical({k:v for k,v in packet.items() if k!='packet_sha256'}))==packet['packet_sha256']
assert sha(packet['blind_reconstruction']['text'].encode('utf-8'))==packet['blind_reconstruction']['text_sha256']
assert packet['anti_anchoring']=={'prior_semantic_slots_included':False,'prior_deltas_included':False,'prior_verdict_included':False,'prior_repairs_included':False}
checks['source_statement_Lean_statement_reconstruction_and_packet_declared_hashes_verified']=True
checks['eight_exact_spans']=[]
steps=expo['units'][0]['steps']
assert len(steps)==8==codes['steps']
for index,(step,region) in enumerate(zip(steps,codes['regions'])):
 assert region==step['lean_source_region']
 p=ROOT/region['path']; raw=p.read_bytes()
 assert sha(raw)==region['source_raw_sha256']
 chunk=b''.join(raw.splitlines(keepends=True)[region['start_line']-1:region['end_line']])
 assert chunk==step['lean'].encode('utf-8')
 assert sha(chunk)==region['exact_code_raw_sha256']
 local=OUT/('actual-main.exactraw.snapshot.lean' if index<7 else 'actual-Test.exactraw.snapshot.lean')
 local.write_bytes(raw)
 checks['eight_exact_spans'].append({'step':index+1,'path':region['path'],'start_line':region['start_line'],'end_line':region['end_line'],'raw_sha256':sha(chunk),'literal_match':True})
assert (ROOT/packet['lean']['file']).read_bytes().decode('utf-8')==packet['candidate_publication_context']['current_lean_module']
assert sha((ROOT/'lean-toolchain').read_text(encoding='utf-8').encode('utf-8'))==packet['candidate_publication_context']['toolchain']
assert sha((ROOT/'lake-manifest.json').read_text(encoding='utf-8').encode('utf-8'))==packet['candidate_publication_context']['dependencies']
for name in ['lean-toolchain','lake-manifest.json']:
 (OUT/(name+'.exactraw.snapshot')).write_bytes((ROOT/name).read_bytes())
unit=load(ROOT/'website/content/declaration_lessons/pbps-unique-positive-macroscopic-defect-root.json')['units'][0]
item=load(ROOT/'website/content/publications/pbps-unique-positive-macroscopic-defect-root.json')['items'][0]
binding=next(x for x in item['bindings'] if x['declaration']==packet['lean']['declaration'])
full_binding={'file':sha((ROOT/packet['lean']['file']).read_text(encoding='utf-8').encode('utf-8')),'current_lean_module':packet['candidate_publication_context']['current_lean_module'],'toolchain':packet['candidate_publication_context']['toolchain'],'dependencies':packet['candidate_publication_context']['dependencies'],'source':item['source'],'statement':item['statement'],'formulae':item['formulae'],'assumptions':item['assumptions'],'obligations':item['obligations'],'lesson':unit,'binding':{k:v for k,v in binding.items() if k not in {'audit_id','legacy_audit_debt'}}}
assert sha(canonical(full_binding))==packet['publication_binding_sha256']
assert {k:v for k,v in unit.items() if k not in {'boundary','source_history_boundary'}}==packet['candidate_publication_context']['lesson']
for field in ['statement','formulae','assumptions','obligations','source']:
 assert item[field]==packet['candidate_publication_context'][field]
checks['fresh_canonical_publication_binding_recomputed_from_main_toolchain_manifest_lesson_and_item']=packet['publication_binding_sha256']
checks['presentation_overlay']={'classification':overlay['classification'],'mathematical_statement_repaired':False,'source_assumption_repaired':False,'main_Test_unchanged':True}
before_expo=load(Path(overlay['raw_snapshot_mappings'][1]['exact_raw_snapshot']['path']))
diffs=[]
def diff(a,b,path=''):
 if type(a)!=type(b):diffs.append(path);return
 if isinstance(a,dict):
  for k in sorted(set(a)|set(b)):
   if k not in a or k not in b:diffs.append(path+'/'+k)
   else:diff(a[k],b[k],path+'/'+k)
 elif isinstance(a,list):
  if len(a)!=len(b):diffs.append(path+'/length')
  for i,(aa,bb) in enumerate(zip(a,b)):diff(aa,bb,path+'/'+str(i))
 elif a!=b:diffs.append(path)
diff(before_expo,expo)
assert set(diffs)=={'/units/0/steps/2/lean','/units/0/steps/2/lean_source_region/start_line','/units/0/steps/2/lean_source_region/exact_code_raw_sha256'}
checks['presentation_overlay']['exact_changed_JSON_leaves']=diffs
before_manifest=load(Path(overlay['raw_snapshot_mappings'][2]['exact_raw_snapshot']['path']))
diffs=[];diff(before_manifest,codes)
assert set(diffs)=={'/regions/2/start_line','/regions/2/exact_code_raw_sha256'}
checks['presentation_overlay']['exact_changed_manifest_leaves']=diffs
for row in overlay['raw_snapshot_mappings']:
 p=Path(row['exact_raw_snapshot']['path']);assert sha(p.read_bytes())==row['original']['raw_sha256']==row['exact_raw_snapshot']['raw_sha256']
checks['presentation_overlay']['all8_before_RAW_snapshots_verified']=True
checks['math_pins_current30']=[]
for row in supp['current30']:
 p=Path(row['path']);b=p.read_bytes();lf=b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
 assert sha(b)==row['raw_sha256'];assert sha(lf)==row['lf_sha256']
 checks['math_pins_current30'].append({'path':row['path'],'raw_sha256':sha(b),'lf_sha256':sha(lf),'verified':True,'read_mode':'bytes-only; no historical verdict parsed'})
for k in ['original_immutable_math_freeze','original_independent_math_run']:
 row=supp[k];assert sha(Path(row['path']).read_bytes())==row['raw_sha256']
 checks[k+'_raw_verified']=row['raw_sha256']
checks['candidate_snapshots_current']=[]
for row in load(OUT/'candidate-input.manifest.json'):
 assert sha(Path(row['origin']).read_bytes())==row['raw_sha256']
 checks['candidate_snapshots_current'].append({'origin':row['origin'],'raw_sha256':row['raw_sha256']})
dp=RUN/'anonymous-decoder'
native=load(dp/'native.run.json');lease=load(dp/'lease.json');decoded=load(dp/'decoded.payload.json')
logical=sha(canonical({k:v for k,v in native.items() if k!='run_sha256'}))
assert logical==native['run_sha256']==adoption['native_run_sha256']==packet['blind_reconstruction']['decoder_run_sha256']
payload_hash=sha((dp/'decoded.payload.json').read_bytes())
assert payload_hash==native['decoded_payload_raw_sha256']==adoption['native_named_RAW_payload_sha256']==lease['decoded_payload_raw_sha256']
assert sha(decoded['reconstructed_theorem_text'].encode('utf-8'))==packet['blind_reconstruction']['text_sha256']
assert decoded['reconstructed_theorem_text']==packet['blind_reconstruction']['text']
assert lease['status']=='CLOSED_LAST' and (dp/'lease.json').read_bytes()==(dp/'proposed-lease.closed.json').read_bytes()
owned=[]
for name,h in lease['owned_artifacts'].items():
 assert sha((dp/name).read_bytes())==h
 owned.append({'name':name,'raw_sha256':h})
assert len(owned)+len(lease['self_hash_exclusions'])==adoption['native_owned_files']
assert sha((dp/'lease.json').read_bytes())==adoption['CLOSED_LAST']['raw_sha256']
assert not native['source_text_visible'] and not native['source_identity_visible'] and not native['compiler_started']
checks['decoder_closure_verified']={'whole_run_sha256':logical,'whole_run_recipe':'sorted compact UTF8 JSON excluding ONLY top-level run_sha256','distinct_full_payload_RAW_sha256':payload_hash,'native_output_manifest':owned,'lease_RAW_sha256':sha((dp/'lease.json').read_bytes()),'lease_CLOSED_LAST':True,'complete_output_count':len(owned)+2,'source_blind':True,'reconstruction_exactly_adopted':True,'context_digest_declared':native['input_digests']['context_declared_sha256'],'context_digest_missing_is_explicit':native['input_digests']['context_declared_sha256'] is None}
checks['all_checks_passed']=True
(OUT/'binding-check.result.json').write_bytes((json.dumps(checks,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps({'all_checks_passed':True,'exact_spans':8,'current30':len(checks['math_pins_current30']),'publication_binding_sha256':packet['publication_binding_sha256'],'decoder_whole_run_sha256':logical,'decoder_payload_RAW_sha256':payload_hash},indent=2))
