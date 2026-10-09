from pathlib import Path
import hashlib,json,html,re,os
r=Path('runs/20261007-companion-priority/pbps-ambient-adjoint-preproof66');d=r/'independent-primary66'
load=lambda n:json.loads((d/n).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
run,lease,manifest,index=[load(n) for n in ['review-run.json','lease.final.json','owned-manifest.json','closure-index.json']]
assert lease['status']=='CLOSED_LAST' and lease['last_owned_write'] and lease['owned_file_count']==51
assert sha((d/'lease.final.json').read_bytes())=='db59cca284da19d3de1065ade795574f0b6a2e2c06c6f010f3bf0817ee820b0c'
assert sha((d/'owned-manifest.json').read_bytes())==lease['manifest_RAW_sha256']=='0ba5a703a971aef1020e84bc9c00aa328ea132e94dd95c428b6fd7ad0c9cc790'
assert set(manifest['all_owned_file_names'])=={p.name for p in d.iterdir() if p.is_file()}
for x in manifest['files']:
 b=(d/x['name']).read_bytes();assert len(b)==x['RAW_bytes'] and sha(b)==x['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n').replace(b'\r',b'\n'))==x['LF_sha256']
logical=sha(json.dumps({k:v for k,v in run.items() if k!='run_sha256'},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
assert logical==run['run_sha256']==lease['whole_logical_run_sha256']=='d34639601263352d2f241188d6a85a993757ab79743ca7ec6effe7ea430fb4e6'
for k in ['COMPLETE_RAW_DECISION','COMPLETE_RAW_REVIEW','SEPARATE_COMPLETE_RAW_INPUT']:
 x=index[k];assert sha((d/x['name']).read_bytes())==x['RAW_sha256'] and len((d/x['name']).read_bytes())==x['RAW_bytes']
i,c,g,h=[load(n) for n in ['source-input-regions.json','source-coverage-inventory.json','source-proof-graph.json','residual-next-header.json']]
raw=Path(i['primary_full_path']).read_bytes();assert sha(raw)==i['primary_full_RAW_sha256']=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
assert len(i['regions'])==6 and c['count']==len(c['math_items'])==310
assert c['missing_alttext']==c['missing_annotation']==c['annotation_mismatch']==0
for x in i['regions']:
 a,b=x['source_RAW_range_end_exclusive'];s=raw[a:b];assert s==(d/(x['name']+'.raw.html')).read_bytes() and sha(s)==x['RAW_sha256']
for x in c['math_items']:
 a,b=x['RAW_byte_range'];s=raw[a:b];assert sha(s)==x['raw_math_sha256']
 assert html.unescape(re.search(rb'\balttext="([^"]*)"',s).group(1).decode())==x['alttext'] and x['annotation_matches']
assert not i['candidate_header_or_Lean_seen'] and not g['candidate_header_Lean_seen']
decision=load('primary-source-decision.json');assert decision['candidate_verdict'] is None and not decision['SAU_claim']
out=r/'root.primary66.adoption.json';assert not out.exists()
out.write_text(json.dumps(dict(status='CLOSED_PRIMARY66_SOURCE_PLANNING_ADOPTED',actual_root_pid=os.getpid(),native_owned_files=51,native_run_sha256=logical,native_complete_RAW_review_sha256=index['COMPLETE_RAW_REVIEW']['RAW_sha256'],source_regions=6,classified_math_items=310,source_graph_sha256=index['source_graph']['RAW_sha256'],native_lease_RAW_sha256=sha((d/'lease.final.json').read_bytes()),source_only=True,Statement_Seal=False,proof_search=False,SAU_claim=False,remaining_boundary=h),ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS primary66 CLOSED51:6 exact primary regions,310/310 literal math items; intrinsic block adjoint vs canonical ambient extension kept distinct; no candidate/proof/claim.')
