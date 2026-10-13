# -*- coding: utf-8 -*-
from pathlib import Path
import json,hashlib,datetime,sys
sys.stdout.reconfigure(encoding='utf-8');R=Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/pbps-after-energy-preread50'
def sha(b):return hashlib.sha256(b).hexdigest()
def lf(b):return b.replace(b'\r\n',b'\n')
def dump(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def read(n):return json.loads((O/n).read_text(encoding='utf-8'))
bindings=[]
for name in ['primary-first.bindings.json','api-input-bindings.initial.json','weighted-public-bindings.json','selected-api-bindings.json']:
 for x in read(name):
  x=dict(x,binding_group=name);bindings.append(x)
extra=read('Lp-ext.binding.json');extra.update(id='Lp-ext',raw_snapshot='Lp-ext.raw',lf_snapshot='Lp-ext.lf');bindings.append(extra)
process_ids={'frontier-execution-provider','current-handoff','reflection-cell','representative-cell','weighted-cell','gradient-distribution-cell'}
policy_deltas=[];checks=[]
for x in bindings:
 p=Path(x['path']);b=p.read_bytes();id=x.get('id','primary')
 assert sha((O/x['raw_snapshot']).read_bytes())==x.get('fragment_raw_sha256',x.get('raw_fragment_sha256'))
 assert sha((O/x['lf_snapshot']).read_bytes())==x.get('fragment_lf_sha256',x.get('lf_fragment_sha256'))
 if sha(b)!=x['whole_raw_sha256'] or sha(lf(b))!=x['whole_lf_sha256']:
  assert id in process_ids,id
  policy_deltas.append(dict(id=id,path=str(p),historical_raw_sha256=x['whole_raw_sha256'],current_raw_sha256=sha(b),historical_lf_sha256=x['whole_lf_sha256'],current_lf_sha256=sha(lf(b)),classification='process-only metadata drift, historical snapshot retained, no theorem source premise; current text not semantically reread'))
 else:
  checks.append(dict(id=id,path=str(p),whole_raw_lf_match=True))
 # Ensure raw fragments are actual contiguous bytes except explicitly reconstructed energy terminal newline.
 fragment=(O/x['raw_snapshot']).read_bytes()
 if id!='public-energy49': assert fragment in b,id
 else: assert len((O/x['lf_snapshot']).read_bytes())==1795
(O/'input-bindings.json').write_bytes(dump(bindings));(O/'final-input-checks.json').write_bytes(dump(dict(math_source_api_match=True,checks=checks,process_only_deltas=policy_deltas,exact_contiguous_fragments_checked=True,reconstructed_parent_header_terminal_newline_explicit=True)))
lease=read('lease.json');assert lease['status']=='OPEN' and all(lease[k]=='OPEN' for k in ['read','write','python']) and lease['compiler']=='CLOSED'
closed=dict(lease);closed.update(status='CLOSED',read='CLOSED',write='CLOSED',python='CLOSED',compiler='CLOSED',compiler_used=False,closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),last_filesystem_operation='Close actual source-only read/write/Python leases after all input checks/output hashes; no following filesystem operation')
closedbytes=dump(closed)
outputs={}
for f in sorted(O.iterdir(),key=lambda x:x.name):
 if f.is_file() and f.name not in ['run.json','lease.json']:
  b=f.read_bytes();outputs[f.name]=dict(raw_sha256=sha(b),lf_sha256=sha(lf(b)),raw_bytes=len(b),lf_bytes=len(lf(b)))
run=dict(schema_version='source-api-preread50-run-v1',status='CLOSED_SOURCE_API_RECOMMENDATION_ONLY',selected_candidate='A-actual-macroscopic-energy-blocks',candidate_count=3,input_count=len(bindings),output_files=outputs,actual_closed_lease_sha256=sha(closedbytes),source_before_api_chronology=['Actual lease OPEN','primary-first.py pins/reads exact primary B.9/B.13/C.1 beforepublicheaders','public-first.py reads current public producers/cells/cards and execution','weighted public headers','minimal MacroscopicRepresentative local reflected_disintegration body and exact definitions/API contracts','untyped recommendation authored','final current input check then actual CLOSED lease'],hash_recipe=dict(raw='SHA256 exact bytes',lf='SHA256 after replacing CRLF with LF only; for CRCRLF provider bytes this leaves a residual CR, disclosed separately; semantic normalized view is a separate file',whole_fragment='Every selected binding distinguishes whole provider hashes from exact raw/LF selected fragments; energy header terminal newline reconstruction is explicitly marked',run='SHA256 exact UTF8 LF run.json bytes, without selfhash field',output_scope='Sorted all prepared private output files excluding run.json and lease.json; actual CLOSED lease separately bound'),limits='No compiler/proof/claim/statement seal/Lean declaration/shared canonical edits/admission or sourcegraph created. Current source/API recommendation is not formal truth. No49finalsourceverdict/decoder/publication read; original49 and other frontiers remain untouched.',process_only_delta_count=len(policy_deltas),sourcegraph_creator_and49wholebody_exposure_disclosed=True,self_admission=False,compiler_used=False)
runbytes=dump(run);(O/'run.json').write_bytes(runbytes)
result=dict(status=run['status'],run_sha256=sha(runbytes),capsule_sha256=outputs['capsule.md']['raw_sha256'],sourcecontract_sha256=outputs['sourcecontract.json']['raw_sha256'],closed_lease_sha256=sha(closedbytes),input_count=len(bindings),process_only_deltas=policy_deltas,all_actual_leases='CLOSED')
# FINAL filesystem operation. Only already computed in-memory output follows.
(O/'lease.json').write_bytes(closedbytes)
print(json.dumps(result,ensure_ascii=False,indent=2))
