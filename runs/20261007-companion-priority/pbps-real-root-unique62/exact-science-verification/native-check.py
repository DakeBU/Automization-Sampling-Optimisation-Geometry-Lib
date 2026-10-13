from common import *
from tools import astis_publication
plan=J(R/'publication-plan.json');objects=[];maps=[]
for folder in ['independent-math62','source-review62']:
 run=J(R/folder/'run.json');lease=J(R/folder/'lease.json');assert H(C({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256'];matches(run['named_payload']);assert pin(run['named_payload']['path'])['raw_sha256']==run.get('named_mathematics_payload_sha256',run.get('named_source_payload_sha256'));assert lease['status']=='CLOSED' and lease['closed_last'] and all(x==0 for x in lease['actual_foreground_readback_exit_codes'])
 payload=J(path(run['named_payload']['path']));objects.extend([run,lease,payload,J(path(lease['output_manifest']['path'])),J(path(lease['native_receipt']['path']))])
 if folder=='source-review62':assert run['excess_count']==0 and not run['repairs'];source=run
 def find_pairs(x):
  if isinstance(x,dict):
   if isinstance(x.get('original'),dict) and isinstance(x.get('raw_snapshot'),dict):maps.append(dict(original=x['original'],exact_raw_snapshot=x['raw_snapshot'],authority='Exact native qualified original/raw_snapshot pair'))
   for v in x.values():find_pairs(v)
  elif isinstance(x,list):
   for v in x:find_pairs(v)
 find_pairs(run)
da=J(R/'root.decoder62.adoption.json');dr=pin(R/'anonymous-decoder/native-decoder-run.raw.txt');dp=pin(R/'anonymous-decoder/decoder62.statements.payload.raw.json');assert dr['raw_sha256']==da['native_run_sha256'] and dp['raw_sha256']==da['named_decoder_payload_sha256'];dl=J(R/'anonymous-decoder/lease.CLOSEDLAST.native.json');assert dl['status']=='CLOSED' and dl['closed_last'] and dl['source_text_visible'] is False and dl['source_identity_visible'] is False
objects.extend([dl,J(R/'anonymous-decoder/native-receipt.json'),da])
for m in da['historical_lease_resolution']+da['raw_snapshot_mappings']:
 orig=m['original'].copy();orig['path']=orig.get('path',orig.get('qualified_input'));maps.append(dict(original=orig,exact_raw_snapshot=m['exact_raw_snapshot'],authority='Explicit native decoder original identity mapping, exact raw+LF'))
# Extract only actual pinned rows from these complete native objects; do not recurse into prior transcript/artifact trees.
pins={}
def walk(x):
 if isinstance(x,dict):
  if isinstance(x.get('path'),str) and isinstance(x.get('raw_sha256',x.get('sha256')),str):
   n=x.copy();n['raw_sha256']=n.get('raw_sha256',n.get('sha256'));pins[(path(n['path']).as_posix(),n['raw_sha256'],n.get('lf_sha256'))]=n
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
for obj in objects:walk(obj)
actual=[];used=[]
for row in pins.values():
 try:a=matches(row);mapping=None
 except (AssertionError,FileNotFoundError):
  mapping=next((m for m in maps if path(m['original']['path'])==path(row['path']) and m['original'].get('raw_sha256')==row['raw_sha256'] and (row.get('lf_sha256') is None or m['original'].get('lf_sha256')==row['lf_sha256'])),None)
  assert mapping is not None,('UNMAPPED_NATIVE_PIN',row)
  matches(mapping['exact_raw_snapshot']);a=matches(row,mapping['exact_raw_snapshot']['path'])
  if mapping not in used:used.append(mapping)
 actual.append(dict(original=row,actual=a,historical_mapping=mapping))
audits=[]
for i,aid in enumerate(plan['audit_ids']):
 a=J(ROOT/('research-wiki/semantic-roundtrip/audits/'+aid+'.json'));n=J(R/f'source-review62/source.{i}.review.json');assert a['state']=='accepted' and a['source_review']['state']=='accepted';assert n['verdict']=='equivalent-after-elaboration' and not n['repairs'] and n['excess_count']==0 and not n['blocking_issues'];assert len(n['semantic_slots'])==7
 assert a['publication_binding_sha256']==n['publication_binding_sha256'];assert a['source_review']['review_run_sha256']==source['run_sha256'];assert a['source_review']['run_artifact']==(R/f'source-review62/source.{i}.review.json').relative_to(ROOT).as_posix()
 for k,v in n['semantic_slots'].items():
  expected=v.copy()
  if isinstance(expected.get('reconstructed'),list):expected['reconstructed']='\n'.join(expected['reconstructed'])
  assert a['semantic_slots'][k]==expected,(k,a['semantic_slots'][k],expected)
 audits.append(dict(audit=pin(ROOT/('research-wiki/semantic-roundtrip/audits/'+aid+'.json')),source_native=pin(R/f'source-review62/source.{i}.review.json'),binding=a['publication_binding_sha256'],accepted_seven_slots=True,native_administrative_slot_join_only=True))
W(P/'native.review.json',dict(status='PASS',actual_PID=os.getpid(),checked_commit=SCI,qualified_native_pin_count=len(actual),verified_pins=actual,finite_history_mappings=used,whole_math_run_sha256=J(R/'independent-math62/run.json')['run_sha256'],whole_math_named_raw_payload_sha256=J(R/'independent-math62/run.json')['named_mathematics_payload_sha256'],source_run_sha256=source['run_sha256'],source_named_raw_payload_sha256=source['named_source_payload_sha256'],decoder_whole_raw_sha256=dr['raw_sha256'],decoder_named_raw_sha256=dp['raw_sha256'],native_recipes=dict(math_source_whole='Entire native run sorted compact UTF8 excluding ONLY run_sha256',math_source_named='Exact complete named payload RAW file bytes; not canonical object hash',decoder_whole=da['run_hash_recipe'],decoder_named=da['payload_hash_recipe']),source_audits=audits,mathematical_reason='Complexified positive A/B share squares on arbitrary g by actual public real/imag formula, complex-linearity and canonical embedding intertwining; complex positive-root uniqueness identifies lifts; real embedding isometry gives injectivity. Actual61 constructs SAME literalS/T/D/root internally; actual62 adds all-positive-root uniqueness without alternative energy premise. Genuine original-input Test transfers actual energy/contractivity after equality. Full scalar domain, arbitrary measure generic, rank0/alphaeta1 retained; no jointGammaP.',seven_steps=plan['formula_proof_steps'],private_providers=0,source_identity_separation=dict(decoder_source_text_visible=False,decoder_source_identity_visible=False,source_reviewer_source_exposed=True,math_decoder_read_before_decision=False),remaining=plan['remaining_boundary']))
print('NATIVE62_PASS',len(actual),'qualified pins',len(used),'finite exact mappings')
