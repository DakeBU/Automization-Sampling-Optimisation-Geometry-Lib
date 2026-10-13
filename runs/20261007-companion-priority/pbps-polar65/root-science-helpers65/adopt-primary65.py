from pathlib import Path
import hashlib,json,html,re,os
r=Path('runs/20261007-companion-priority/pbps-polar-preproof65');d=r/'independent-primary65'
load=lambda n:json.loads((d/n).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
run,lease,manifest=load('review-run.json'),load('lease.final.json'),load('owned-manifest.json')
assert lease['status']=='CLOSED_LAST' and lease['final_owned_file_count']==49
assert sha((d/'lease.final.json').read_bytes())=='484c7e4eb3ce900d957de8a35590399d2593158344f7d5b2565901e53232abbf'
assert sha((d/'owned-manifest.json').read_bytes())==lease['owned_manifest_raw_sha256']=='af1e768364b0e57d1b3b0e8e2b4e49dfa853e4b286dbdb938e0b9b67b14e66f3'
owned=manifest['all_preclosure_owned_files']
for q in owned:
 b=(d/q['filename']).read_bytes();assert len(b)==q['raw_bytes'] and sha(b)==q['raw_sha256']
 assert sha(b.replace(b'\r\n',b'\n').replace(b'\r',b'\n'))==q['lf_sha256']
assert {q['filename'] for q in owned}|{'owned-manifest.json','lease.final.json'}=={p.name for p in d.iterdir() if p.is_file()}
logical=sha(json.dumps({k:v for k,v in run.items() if k!='run_sha256'},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
assert logical==run['run_sha256']==lease['run_sha256']=='4f84380f62a0f178f11dbe1442fc8ec9049f755612c9bd116b1ec12a6673fde9'
assert sha((d/'review-run.json').read_bytes())==lease['complete_RAW_REVIEW_sha256']=='3751bec3cee128e9068ba3a2cbd7c8de3c01df502929c77faca91e3b135fba7f'
assert run['full_source_planning_contents']=={n:load(n) for n in run['full_source_planning_contents']}
i,c,g,h,n=[load(x) for x in ['source-inputs.json','source-coverage-inventory.json','source-proof-graph.json','residual-next-header.json','negative-boundaries.json']]
raw=Path('runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html').read_bytes()
assert sha(raw)==i['primary_raw_sha256']=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
assert len(i['regions'])==6 and c['math_count']==len(c['math_items'])==280
assert c['missing_alttext_count']==c['missing_annotation_count']==c['annotation_mismatch_count']==0
for q in i['regions']:
 a,b=q['source_raw_byte_range'];s=raw[a:b];assert s==(d/(q['name']+'.raw.html')).read_bytes() and sha(s)==q['raw_sha256']
 assert sha(s.replace(b'\r\n',b'\n').replace(b'\r',b'\n'))==q['lf_sha256']
for m in c['math_items']:
 s=raw[m['raw_byte_start']:m['raw_byte_end_exclusive']];assert sha(s)==m['raw_math_sha256']
 assert html.unescape(re.search(rb'\balttext="([^"]*)"',s).group(1).decode())==m['alttext'] and m['annotation_exactly_matches_alttext'] and m['classification']
assert not g['future65_candidate_or_header_or_Lean_seen'] and h['public_extra_premises']==[] and h['no_new_H1_B13_B14_floor_premise']
assert n['candidate_verdict'] is None and not n['SAU_claim'] and not n['whole_paper']
out=r/'root.primary65.adoption.json';assert not out.exists()
out.write_text(json.dumps(dict(status='CLOSED_INDEPENDENT_PRIMARY65_SOURCE_PLANNING_ADOPTED',actual_reader_pid=os.getpid(),native_owned_files=49,native_run_sha256=logical,native_complete_RAW_review_sha256=sha((d/'review-run.json').read_bytes()),source_regions=6,classified_math_items=280,source_graph_sha256=sha((d/'source-proof-graph.json').read_bytes()),residual_header_sha256=sha((d/'residual-next-header.json').read_bytes()),native_lease_RAW_sha256=sha((d/'lease.final.json').read_bytes()),source_only=True,Statement_Seal=False,proof_search=False,SAU_claim=False,remaining_boundary=h),ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS source-only65 CLOSED_LAST readback:49 owned files,6 exact regions,280 classified math items; no statement seal/proof/SAU.')
