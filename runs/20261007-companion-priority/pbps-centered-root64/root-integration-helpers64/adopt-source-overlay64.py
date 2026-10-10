from pathlib import Path
import hashlib,json,os,subprocess,sys
root=Path.cwd();sys.path.insert(0,str(root/'tools'));import astis_publication as pub,astis_semantic_roundtrip as rt
r=root/'runs/20261007-companion-priority/pbps-centered-root64';d=r/'independent-auxiliary-overlay64';load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
lease=load(d/'lease.final.json');run=load(d/'review-run.json');decision=load(d/'decision.0.json');checks=load(d/'finite-diff-checks.json');manifest=load(d/'full-owned-manifest.json')
assert lease['state']=='CLOSED_LAST' and sha((d/'lease.final.json').read_bytes())=='ffb94ac50e17b293278fb9c3866cb447f24334a41569d951df681ae00b557a49'
assert sha(can({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==lease['logical_run_sha256']==decision['review_run_sha256']=='c6b32a97745075cbc6bf286cdd763af1bcd4bf1cae69b937c19737c815a42d53'
named=sha((d/'review-run.json').read_bytes());assert named==lease['complete_named_RAW_REVIEW']['raw_sha256']=='afa5bf100c9d91435c76deb8ca9fe45bcc212453a4e1f71ee0ef1bd4f138d91c' and lease['complete_named_RAW_REVIEW']['deletion']=='NONE'
assert sha((d/'full-owned-manifest.json').read_bytes())=='edceb9563899f6ef141e8f2a63b67eb5e4c8c7f667c8130939b4bdb0f6aaf450'
actual={p.relative_to(d).as_posix() for p in d.rglob('*') if p.is_file()};assert actual=={x['relative_path'] for x in manifest['files']}|{'full-owned-manifest.json'} and len(actual)==54
for x in manifest['files']:
 b=(d/x['relative_path']).read_bytes();assert len(b)==x['raw_bytes'] and sha(b)==x['raw_sha256']
assert {k:v for k,v in decision.items() if k!='review_run_sha256'}==run['native_decision']==load(d/'decision.0.frozen.json')
assert decision['verdict']=='equivalent-after-elaboration' and decision['metadata_overlay_review']['status']=='ACCEPTED_METADATA_ONLY' and not decision['source_statement_mathematical_repair'] and not decision['source_assumptions_changed']
assert decision['independent_from_formalizer'] and decision['independent_from_decoder'] and decision['independent_from_overlay_preparer'] and decision['original_decision1_remains_applicable']
assert not decision['repairs'] and not decision['deltas'] and set(decision['semantic_slots'])==set(rt.SEMANTIC_SLOTS)
assert len(checks['input_maps'])==18 and len(checks['all12_literal_body_region_checks'])==12
for x in checks['input_maps']:
 b=Path(x['source_path']).read_bytes();assert b==(d/x['raw_snapshot']).read_bytes() and sha(b)==x['raw_sha256']
 lf=b.replace(b'\r\n',b'\n').replace(b'\r',b'\n');assert lf==(d/x['lf_snapshot']).read_bytes() and sha(lf)==x['lf_sha256']
for k in ['historical_before_pins_match_adoption','fresh_packet_hash_match','publication_binding_match','candidate_context_match_current','mathematical_source_statement_unchanged','lean_statement_unchanged','blind_reconstruction_and_decoder_packet_unchanged','generic_statement_formulae_assumptions_unchanged','all_three_generic_steps_unchanged','all_nine_actual_steps_unchanged','three_lean_hashes_match_original','peer_packet1_raw_unchanged','peer_publication_binding_unchanged','source_attribution_now_exact_background_not_printed_auxiliary','only_two_actual_mathlib_dependencies_remain']:assert checks[k],k
aid='ASTIS-RT-20261009-RealL2PositiveSquareOrder';a=load(root/'research-wiki/semantic-roundtrip/audits'/f'{aid}.json');packet=load(r/'auxiliary-metadata-overlay64/fresh-reviewer-packet.json');assert rt.semantic_reviewer_packet(a)==packet and packet['packet_sha256']==decision['reviewer_packet_sha256']
pub.inputs.cache_clear();pub.load.cache_clear();data=pub.inputs();item=next(x for x in pub.load() if x['id']=='real-l2-positive-square-order');assert pub.binding_digest(item,item['bindings'][0],data)==a['publication_binding_sha256']==decision['publication_binding_sha256']
for n,pid in [('foreground-finalizer.receipt.json',25164),('foreground-readback.receipt.json',18412)]:
 x=load(d/n);assert x['exit_code']==0 and x['terminal_closed'] and x['actual_foreground_pid']==pid
command=load(d/'foreground-finalizer.receipt.json')['command'];proc=subprocess.Popen(command[:-1]+['postclose'],stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=proc.communicate();assert proc.returncode==0,err.decode(errors='replace');terminal=json.loads(out)
p=r/'root.source64.overlay-adoption.json';assert not p.exists();p.write_text(json.dumps(dict(accepted=True,status='SEPARATE_INDEPENDENT_METADATA_OVERLAY64_ACCEPTED',actual_adopter_pid=os.getpid(),decision_path=(d/'decision.0.json').as_posix(),native_run_sha256=run['run_sha256'],native_complete_RAW_review_sha256=named,native_owned_files=54,actual_root_readback_pid=proc.pid,actual_root_readback_exit_code=0,terminal_readback=terminal,source_statement_mathematical_repair=False,all12_original_body_excerpts_unchanged=True,all_original_Lean_and_decoder_unchanged=True,original_actual_decision1_remains_applicable=True,full_ExpositionSeal=False,VERIFIED_transition=False),ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS separate CLOSED overlay64:54 native files,18 RAW/LF pairs,current seven-slot decision,12 unchanged excerpts. No mathematical repair or full Exposition claim.')
