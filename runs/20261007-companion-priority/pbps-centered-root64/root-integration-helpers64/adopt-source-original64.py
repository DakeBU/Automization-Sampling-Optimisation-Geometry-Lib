from pathlib import Path
import hashlib,json,os,subprocess,sys
root=Path.cwd();sys.path.insert(0,str(root/'tools'));import astis_publication as pub,astis_semantic_roundtrip as rt
r=root/'runs/20261007-companion-priority/pbps-centered-root64';d=r/'independent-source64';load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def pin(p):
 b=p.read_bytes();return dict(path=p.resolve().as_posix(),raw_bytes=len(b),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')))
def write_new(p,x):
 assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
lease=load(d/'lease.final.json');run=load(d/'review-run.json');assert lease['state']=='CLOSED_LAST'
assert sha((d/'lease.final.json').read_bytes())=='c086af55caf52e5322f87d9e47a6ae311997fb002b8c2b3620a9cbae205dd3e2'
assert sha(can({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==lease['logical_run_sha256']=='9acbe7fd557f9fe4355d54f26ee5f2b7d2819d96c0deabd3eaba27aaf45f814d'
raw_review=sha((d/'review-run.json').read_bytes());assert raw_review=='8831289c9ae73ad92bb138016808ccf7e69e64f98c1779b0ea6f7a36ed8db4c3'
manifest=load(d/'full-owned-manifest.json');assert sha((d/'full-owned-manifest.json').read_bytes())=='6330602cfc97f005fc433528f96786a325dae73df35c067912694541fc416ab0'
listed={x['relative_path'] for x in manifest['files']};actual={p.relative_to(d).as_posix() for p in d.rglob('*') if p.is_file()};assert actual==listed|{'full-owned-manifest.json'} and len(actual)==97
for x in manifest['files']:
 b=(d/x['relative_path']).read_bytes();assert len(b)==x['raw_bytes'] and sha(b)==x['raw_sha256']
checks=load(d/'candidate-input-binding-and-span-checks.json');assert len(checks['records'])==21 and len(checks['all12_literal_spans'])==12
maps=[]
for x in checks['records']:
 b=Path(x['source_path']).read_bytes();sp=d/x['raw_snapshot'];assert b==sp.read_bytes() and sha(b)==x['raw_sha256'] and len(b)==x['raw_bytes']
 lf=b.replace(b'\r\n',b'\n').replace(b'\r',b'\n');assert lf==(d/x['lf_snapshot']).read_bytes() and sha(lf)==x['lf_sha256']
 maps.append(dict(original=pin(Path(x['source_path'])),explicit_exact_raw_snapshot=pin(sp)))
for x in checks['all12_literal_spans']:
 b=(root/x['path']).read_bytes();region=b''.join(b.splitlines(keepends=True)[x['start_line']-1:x['end_line']]);assert region==(d/x['raw_excerpt_artifact']).read_bytes() and sha(region)==x['declared_excerpt_sha256']
 assert all(x[k] for k in ['source_raw_hash_match','literal_code_equals_raw_region','literal_code_hash_match','inside_actual_proof_body'])
plan=load(r/'publication-plan.json');pub.inputs.cache_clear();pub.load.cache_clear();data=pub.inputs();decisions=[]
for i,aid in enumerate(plan['audit_ids']):
 q=load(d/f'decision.{i}.json');a=load(root/'research-wiki/semantic-roundtrip/audits'/f'{aid}.json');packet=load(r/f'source.{i}.reviewer-packet.json')
 assert a['state']=='blind-reconstructed' and rt.semantic_reviewer_packet(a)==packet and packet['packet_sha256']==q['reviewer_packet_sha256']
 item=next(x for x in pub.load() if x['id']==plan['slugs'][i]);assert pub.binding_digest(item,item['bindings'][0],data)==a['publication_binding_sha256']==q['publication_binding_sha256']
 assert q['verdict']=='equivalent-after-elaboration' and q['source_admission']['decision']=='SCOPED_ACCEPT' and set(q['semantic_slots'])==set(rt.SEMANTIC_SLOTS)
 assert not q['deltas'] and not q['repairs'] and q['independent_from_formalizer'] and q['independent_from_decoder']
 assert {k:v for k,v in q.items() if k!='review_run_sha256'}==run['native_decisions'][i]
 decisions.append(pin(d/f'decision.{i}.json'))
stage=load(d/'primary-first-stage-seal.json');assert not stage['candidate_visible'];assert stage['sealed_at_utc']<run['candidate_read_process']['first_candidate_read_utc']
assert not run['source_to_candidate_coverage']['unclassified'] and len(run['source_to_candidate_coverage']['items'])==321
for name,pid in [('foreground-finalizer.receipt.json',37048),('foreground-readback.receipt.json',12204)]:
 x=load(d/name);assert x['exit_code']==0 and x['terminal_closed'] and x['actual_foreground_pid']==pid
proc=subprocess.Popen([sys.executable,'-X','utf8',str(d/'native-finalizer64.py'),'postclose'],stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=proc.communicate();assert proc.returncode==0,err.decode(errors='replace')
terminal=json.loads(out);assert terminal['lease_state']=='CLOSED_LAST' and terminal['no_postclose_writes']
write_new(r/'root.source64.original-adoption.json',dict(status='ORIGINAL_TWO_SCOPED_SOURCE64_DECISIONS_ADOPTED_METADATA_DEBT_RETAINED',actual_adopter_pid=os.getpid(),native_logical_run_sha256=run['run_sha256'],native_complete_named_RAW_REVIEW_sha256=raw_review,separate_named_RAW_INPUT_sha256=checks['complete_named_raw_payload']['raw_sha256'],native_owned_files=97,decisions=decisions,finite_input_maps=maps,actual_root_postclose_readback_pid=proc.pid,actual_root_postclose_exit_code=proc.returncode,root_postclose_terminal=terminal,original_close_pid=None,canonical_audits_not_mutated=True,full_ExpositionSeal=False,VERIFIED_transition=False))
print('PASS original CLOSED source64:97 native files,21 RAW/LF pairs,321 source items,12 exact spans,2 scoped decisions. Metadata debt retained; canonical audits untouched.')
