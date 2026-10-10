from pathlib import Path
import hashlib,json,os,subprocess,sys
r=Path('runs/20261007-companion-priority/pbps-first-corrector-energy-preproof67');sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda p:json.loads(Path(p).read_bytes())
expected=[('independent-header-math67',55,'b7e810b4a56cb7f233fe772824350fb2ab2de486c50d585b50d9076db4a16c1a','2771f26aabe876a43d20fa69e0dfc13ac588889a5d6e5150847cf89f15fe7a31'),('independent-header-source67',54,'8af44d6dfd0e79e75f2f86accbc728cefa9f3f43b50b07469bba0ec4091596fb','ccc6a84bae39b0daa9c6743a65095cd289f4f13ad2ffb2c0fd2a71ea922ea956')]
records=[]
for sub,count,lh,rh in expected:
 d=r/sub;l=load(d/'lease.final.json');assert l['status']=='CLOSED_LAST' and l['last_owned_write'] and sha((d/'lease.final.json').read_bytes())==lh
 run=load(d/('run.json' if 'math' in sub else 'review-run.json'));h=sha(json.dumps({k:v for k,v in run.items() if k!='run_sha256'},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode());assert h==rh==l['whole_logical_run_sha256']==run['run_sha256']
 before={p.as_posix():(sha(p.read_bytes()),p.stat().st_mtime_ns) for p in d.rglob('*') if p.is_file()};assert len(before)==count
 if 'math' in sub:
  pins=l['all_owned_except_this_final_lease'];assert {Path(q['path']).resolve() for q in pins}|{(d/'lease.final.json').resolve()}=={p.resolve() for p in d.rglob('*') if p.is_file()}
  for q in pins:
   b=Path(q['path']).read_bytes();assert len(b)==q['raw_bytes'] and sha(b)==q['raw_sha256'] and sha(b.replace(b'\r\n',b'\n').replace(b'\r',b'\n'))==q['lf_sha256']
  v=load(d/'mathematical-statement-review.json');assert v['header_count']==3 and not v['proof_search'] and not v['source_mathematical_repair']
 else:
  m=load(d/'owned-manifest.json');assert sha((d/'owned-manifest.json').read_bytes())==l['manifest_RAW_sha256']
  for q in m['regular_file_entries']:
   b=(d/q['name']).read_bytes();assert len(b)==q['RAW_bytes'] and sha(b)==q['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==q['LF_sha256']
  v=load(d/'header-decisions.json');assert len(v['decisions'])==3 and v['all_three_have_full_seven_slots'] and v['source_missing']==0 and v['no_mathematical_repair_required']
  for k in ['COMPLETE_RAW_REVIEW','COMPLETE_RAW_DECISION','SEPARATE_COMPLETE_RAW_INPUT']:
   q=l[k];b=(d/q['name']).read_bytes();assert sha(b)==q['RAW_sha256'] and len(b)==q['RAW_bytes']
 assert before=={p.as_posix():(sha(p.read_bytes()),p.stat().st_mtime_ns) for p in d.rglob('*') if p.is_file()}
 records.append(dict(package=sub,owned_files=count,whole_logical_run_sha256=h,lease_RAW_sha256=lh,postclose_owned_writes=0))
for i,h in enumerate(['91d2c9a38d1db992306cbce8a4c735ea2bfb51d2a48991f1e7ec94eed1b42766','07b2c7e9cb0ee47e654305c13a6c6cb59844fb6d7345e414f0c49e7bc11ac98c','e53aedbe9f4ca7d784e5215085c4fb3c40ff9eea00349bd9893c8ad76526bc83']):assert sha((r/f'header{i}-expanded.lean').read_bytes())==h
out=r/'root.header67.adoption.json';assert not out.exists();out.write_text(json.dumps(dict(status='THREE_DRAFT_HEADERS_ACCEPTED_TYPE_FORMED_NO_PROOF',actual_root_pid=os.getpid(),native_packages=records,source_semantic_slots=21,Statement_Seal=False,SAU_claim=False,proof_search=False,required_final_whole_module_review=True),ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS CLOSED55 math/CLOSED54 source header67 adoption; three exact drafts,21 slots; no proof/SAU/Seal credit.')
