from pathlib import Path
import json,hashlib,gzip,subprocess
root=Path.cwd(); r=root/'runs/20261007-companion-priority/pbps-centered-defect59';d=r/'repository-exposition-seal59'
load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def path(s):
 p=Path(str(s).replace('\\','/'));return p if p.is_absolute() else root/p
def check(q):
 b=path(q['path']).read_bytes();z=b.replace(b'\r\n',b'\n')
 assert sha(b)==q['raw_sha256'] and sha(z)==q['lf_sha256'],q['path']
 assert len(b)==q['bytes'] and ('lf_bytes' not in q or len(z)==q['lf_bytes']),q['path']
 return q
def pin(p):
 b=p.read_bytes();z=b.replace(b'\r\n',b'\n');return dict(path=p.relative_to(root).as_posix(),bytes=len(b),lf_bytes=len(z),raw_sha256=sha(b),lf_sha256=sha(z))
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert head=='47a28adfa36bfa67ce201f9b3ff9823c85fc3b45'
run,lease,receipt,inputs,outputs,readback=[load(d/f) for f in ['run.json','lease.json','receipt.json','input.manifest.json','outputs.final.json','readback.json']]
assert lease['status']=='CLOSEDLAST' and lease['compiler']==run['compiler']=='NOT_STARTED_CLOSED'
assert sha(can({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==lease['run_sha256']=='fab3d629c324bc7e5d09fb4fbebc215601957bca1dceb345588b9e2572d4954c'
assert sha(can(run['named_repository_exposition_payload']))==run['named_repository_exposition_payload_sha256']==lease['named_repository_exposition_payload_sha256']=='664870093c5ae1a723db232221e4b57139f44b3439933e6b4a4e1d97a18eaf5c'
assert sha(can({k:v for k,v in lease.items() if k!='lease_sha256'}))==lease['lease_sha256']=='4cd977334f894bea5b0156e6bdc32a8308430414462370528761e5a98005686c'
assert sha(can({k:v for k,v in outputs.items() if k!='outputs_sha256'}))==outputs['outputs_sha256']
assert pin(d/'lease.json')['raw_sha256']=='e9b613171d9891b3f0bfaaeb6059966b70fd573a5dd77259699a233d3c7c629b'
assert pin(d/'receipt.json')['raw_sha256']=='6d2d4fe8e61fdf64c08f4af45a911f8ead7a87dc9b92932914d0d45c34488d9f'
assert receipt['checked_integration_commit']==run['checked_integration_commit']==head
assert receipt['verdict']=='ACCEPT_SCOPED_REPOSITORY_AND_EXPOSITION_NO_MATHEMATICAL_OR_SOURCE_BLOCKER'
assert inputs['count']==len(inputs['artifacts'])==readback['input_count']==914
assert outputs['count']==len(outputs['artifacts'])==lease['output_count']==28
for q in inputs['artifacts']+outputs['artifacts']:check(q)
for k in ['run','receipt','payload','outputs','readback']:check(lease[k])
for p in lease['foreground_child_processes']:
 assert p['exit_code']==0 and p['terminal_closed'];check(p['stdout']);check(p['stderr'])
mapping_record=load(d/'historical-mappings.json');maps=mapping_record['mappings']
assert len(maps)==mapping_record['count']==10
native_checks=load(d/'native-checks.json');assert native_checks['used_historical_map_count']==6
for m in maps:
 q=check(m['snapshot']);assert all(m['original'][k]==q[k] for k in ['bytes','raw_sha256','lf_sha256'])
gm=load(d/'graph-successor.json')['old_negative_mapping'];check(gm['exact_gzip_snapshot'])
b=gzip.decompress(path(gm['exact_gzip_snapshot']['path']).read_bytes());o=gm['original']
assert len(b)==o['bytes'] and sha(b)==o['raw_sha256'] and sha(b.replace(b'\r\n',b'\n'))==o['lf_sha256']
assert load(d/'graph-successor.json')['only_generated_graph_changed_fields']==['publication_inputs_sha256']
out=dict(status='INDEPENDENT_SCOPED_REPOSITORY_EXPOSITION59_ACCEPTED',integration_commit=head,science_commit=run['checked_science_commit'],native_actor=run['actor'],native_run=pin(d/'run.json'),native_lease=pin(d/'lease.json'),native_receipt=pin(d/'receipt.json'),native_run_sha256=run['run_sha256'],native_named_payload_sha256=run['named_repository_exposition_payload_sha256'],input_pins_read_back=914,outputs_read_back=28,historical_maps=maps,exact_graph_negative_map=gm,counts=receipt['counts'],scope=receipt['scope'],presentation_debts=receipt['presentation_debts'],canonical_math_mutations=False,new_verified_transition=False,main_live_purified=False)
(r/'root.repository-exposition59.adoption.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Accepted native CLOSEDLAST complete run/payload/lease hashes,914 exact inputs,28 outputs,10 available/6 used qualified historical maps and exact original stale-graph gzip. No math or status mutation.')
