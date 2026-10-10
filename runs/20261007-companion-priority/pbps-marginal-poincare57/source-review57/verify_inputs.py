from pathlib import Path
import json,hashlib,sys,os
sys.stdout.reconfigure(encoding='utf8')
R=Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-marginal-poincare57';O=B/'source-review57'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(j):return json.dumps(j,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf8')
def pin(p):
 p=Path(p);p=p if p.is_absolute() else R/p;b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return {'path':str(p).replace('\\','/'),'bytes':len(b),'raw_sha256':sha(b),'lf_bytes':len(lf),'lf_sha256':sha(lf)}
def write(n,j):
 j['content_self_sha256']=sha(canon(j));p=O/n;p.write_bytes((json.dumps(j,ensure_ascii=False,indent=2)+'\n').encode('utf8'));q=json.loads(p.read_bytes());v=q.pop('content_self_sha256');assert sha(canon(q))==v;return pin(p)
lease=json.loads((O/'initial-source-lease.raw.snapshot.json').read_bytes());assert lease['status']=='OPEN' and lease['compiler_started'] is False
assert (B/'source.review.lease.json').read_bytes()==(O/'initial-source-lease.raw.snapshot.json').read_bytes()
pins=[];(O/'inputs').mkdir(exist_ok=True)
for i,q in enumerate(lease['input_artifacts']):
 assert 'whole-math' not in q['path'] and 'whole_math' not in q['path'],q['path']
 a=pin(q['path']);assert all(a[k]==q[k] for k in ['bytes','raw_sha256','lf_sha256']),q['path'];pins.append(a)
 raw=Path(a['path']).read_bytes();stem=f'{i:03d}.{Path(a["path"]).name}';p=O/'inputs'/(stem+'.exactraw.snapshot');z=O/'inputs'/(stem+'.crlf-to-lf.snapshot')
 if p.exists():assert p.read_bytes()==raw and z.read_bytes()==raw.replace(b'\r\n',b'\n')
 else:p.write_bytes(raw);z.write_bytes(raw.replace(b'\r\n',b'\n'))
 assert p.read_bytes()==raw and z.read_bytes()==raw.replace(b'\r\n',b'\n')
assert len(pins)==614
packet=json.loads((B/'source.0.reviewer-packet.json').read_bytes());q=dict(packet);v=q.pop('packet_sha256');assert sha(canon(q))==v==lease['reviewer_packet_sha256']
assert sha(packet['source']['original_text'].encode())==packet['source']['text_sha256']
assert sha(packet['blind_reconstruction']['text'].encode())==packet['blind_reconstruction']['text_sha256']
assert sha(packet['lean']['statement'].encode())==packet['lean']['statement_sha256']
main=R/packet['lean']['file'];raw=main.read_bytes();text=raw.decode('utf8');start=text.index('theorem actual_gaussian_marginal_centered_poincare');end=text.index(' := by',start);signature=(text[start:end].rstrip()+'\n').encode('utf8');assert len(signature)==1244 and sha(signature)=='e706b4e6c3c07f58a090ee86cb51dd91be2f11afe707db653737e4983c7181e9'
(O/'production.header.seal.normalized.lf.snapshot.lean').write_bytes(signature)
(O/'production.header.physical.raw.snapshot.lean').write_bytes(text[start:end].encode('utf8'))
assert packet['candidate_publication_context']['current_lean_module']==text
pubpath=R/'website/content/publications/gaussian-marginal-poincare.json';lessonpath=R/'website/content/declaration_lessons/gaussian-marginal-poincare.json';pub=json.loads(pubpath.read_bytes())['items'][0];lesson=json.loads(lessonpath.read_bytes())['units'][0];binding=next(b for b in pub['bindings'] if b['declaration']==packet['lean']['declaration']);context=packet['candidate_publication_context']
payload={k:context[k] for k in ['file','current_lean_module','toolchain','dependencies','source','statement','formulae','assumptions','obligations','lesson','binding']};payload['lesson']=lesson;payload['binding']={k:v for k,v in binding.items() if k not in ['audit_id','legacy_audit_debt']}
for k in ['source','statement','formulae','assumptions','obligations']:assert payload[k]==pub[k]
for p,k in [(main,'file'),(R/'lean-toolchain','toolchain'),(R/'lake-manifest.json','dependencies')]:assert sha(p.read_text(encoding='utf8').encode())==payload[k]
digest=sha(canon(payload));assert digest==packet['publication_binding_sha256']=='cd7704313084137b33ef2cff81e754a65cfe0cee0af14f8eddcacef27de8442e'
audit=json.loads((R/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261008-GaussianMarginalPoincare.json').read_bytes());assert audit['publication_binding_sha256']==digest
# Review context is a deliberate projection, not the binding payload itself.
project=dict(payload);project['binding']={k:payload['binding'][k] for k in ['declaration','role','supports']};project['lesson']={k:v for k,v in lesson.items() if k not in ['boundary','source_history_boundary']};project['candidate_assumptions']=[{k:d[k] for k in ['source','lean']} for d in binding['assumption_deltas']];assert project==context
write('publication.binding.payload.json',{'schema_version':1,'payload':payload,'named_payload_sha256':digest,'named_payload_recipe':'SHA256 complete binding payload only; not wrapper complete-object hash. File/toolchain/manifest digests use UTF8 text with universal-newline normalization per existing binding_payload API.','review_context_complete_sha256':sha(canon(context)),'projection_rule':'Context restricts binding to declaration/role/supports, removes lesson boundary/source_history_boundary, adds candidate_assumptions source/lean only. Context full digest therefore intentionally differs from publication binding digest.'})
build=[]
for prefix in ['production.0','tests.4']:
 s=json.loads((B/(prefix+'.status.json')).read_bytes());l=json.loads((B/(prefix+'.compiler.lease.json')).read_bytes());assert s['exit_code']==0 and l['status']=='CLOSED' and l['exit_code']==0;assert sha((B/(prefix+'.log')).read_bytes())==s['log_raw_sha256'];assert sha((B/(prefix+'.source.raw.snapshot.lean')).read_bytes())==s['source_raw_sha256'];build.append({'status':pin(B/(prefix+'.status.json')),'lease':pin(B/(prefix+'.compiler.lease.json')),'actual_pid':s['process_id'],'actual_exit_code':0,'log':pin(B/(prefix+'.log'))})
decoder=json.loads((B/'anonymous-decoder/run.json').read_bytes());q=dict(decoder);rd=q.pop('run_sha256');assert sha(canon(q))==rd==packet['blind_reconstruction']['decoder_run_sha256']
dl=json.loads((B/'anonymous-decoder/lease.json').read_bytes());assert dl['status']=='CLOSED' and decoder['source_text_visible'] is False and dl['source_text_visible'] is False and decoder['identityblind'] is False
dr=json.loads((B/'anonymous-decoder/result0.json').read_bytes());print('decoder-result-schema',list(dr))
assert dr['reconstructed_theorem_text']==packet['blind_reconstruction']['text'] and dr['decoder_run_sha256']==rd and dr['source_text_visible'] is False
checks=[];temporal_checks=[]
def verify_embedded(j,where):
 if isinstance(j,dict):
  if {'path','bytes','raw_sha256'}<=set(j):
   a=pin(j['path'])
   if not all(a[k]==j[k] for k in ['bytes','raw_sha256','lf_sha256'] if k in j):
    assert where in ['decoder-run/actually_read_inputs/1','decoder-lease/initial_lease_artifact'] and j==dl['initial_lease_artifact'],(where,j['path'])
    old=pin(B/'anonymous-decoder/initial-lease.raw.snapshot.json');assert all(old[k]==j[k] for k in ['bytes','raw_sha256','lf_sha256'] if k in j)
    assert json.loads(Path(old['path']).read_bytes())==decoder['initial_lease_snapshot'] and decoder['initial_lease_snapshot']['status']=='OPEN'
    temporal_checks.append({'where':where,'historical_OPEN_input':j,'current_CLOSED_path_pin':a,'preserved_exact_OPEN_snapshot':old,'explicit_native_link':'run.initial_lease_snapshot + lease.initial_lease_artifact + lease.initial_lease_preservation; root portable snapshot exactraw/LF matches. Temporal receipt, not a malformed locator or a source repair.'});a=old
   assert all(a[k]==j[k] for k in ['bytes','raw_sha256','lf_sha256'] if k in j),(where,j['path']);checks.append({'where':where,'pin':a})
  for k,v in j.items():verify_embedded(v,where+'/'+k)
 elif isinstance(j,list):
  for i,v in enumerate(j):verify_embedded(v,where+'/'+str(i))
verify_embedded(decoder,'decoder-run');verify_embedded(dl,'decoder-lease')
freeze=json.loads((B/'math-freeze.json').read_bytes());assert len(freeze['inputs'])==602
for q in freeze['inputs']:
 a=pin(q['path']);assert all(a[k]==q[k] for k in ['bytes','raw_sha256','lf_sha256']),q['path']
write('input-verification.json',{'schema_version':1,'reviewer':'/root/next_primary56','native_input_count':len(pins),'native_inputs':pins,'all_match':True,'math_freeze602_current_unchanged':True,'packet_complete_minus_packet_sha256':packet['packet_sha256'],'packet_actual_raw_lf_pin':pin(B/'source.0.reviewer-packet.json'),'publication_binding_sha256':digest,'publication_binding_payload_recipe':'Named complete payload distinct from wrapper self hash and projected context full digest.','header1244_exact_sha256':sha(signature),'build_evidence':build,'decoder_run_complete_minus_run_sha256':rd,'decoder_native_pin_checks':checks,'decoder_temporal_OPEN_input_checks':temporal_checks,'operational_verification_negative':'0ddcdc EXIT1 after614 successful pins: initially compared historical decoder OPEN lease receipt to current CLOSED path. Original failed script preserved; explicit native opening snapshot link verified, no decoder/source mutation or repair.','decoder_source_text_blind':True,'decoder_identityblind':False,'final_stage_candidate_body_exposure':{'first_actual_packet_read_chunk':'01602f','complete_main_and_Test_display_chunk':'a173b3','strict_final_proof_body_blindness':False,'own_primary_statement_topology_before_this_exposure':True},'whole_math_verdict_read':False,'compiler_started_by_reviewer':False,'source_binding_API_negative_preserved':pin(B/'source-binding.0.diagnosis.json')})
write('input.manifest.json',{'schema_version':1,'reviewer':'/root/next_primary56','source_lease_original_open':pin(O/'initial-source-lease.raw.snapshot.json'),'pins':pins,'count':len(pins),'recipe':'Exact raw bytes; LF replaces onlyCRLF withLF, neverJSON reserialization. Raw/LF snapshots actually read back. Full parent module bytes may be hashed/snapshotted as receipts; source interpretation uses sealed public contracts, no parent proof re-verification. No whole-math artifacts included.'})
print(json.dumps({'status':'SOURCE_INPUTS_VERIFIED','pid':os.getpid(),'pins':len(pins),'math_freeze_pins':602,'decoder_receipt_checks':len(checks),'signature_bytes':len(signature),'packet_sha256':packet['packet_sha256'],'publication_binding_sha256':digest,'strict_final_body_blindness':False,'no_compiler':True},ensure_ascii=False))
