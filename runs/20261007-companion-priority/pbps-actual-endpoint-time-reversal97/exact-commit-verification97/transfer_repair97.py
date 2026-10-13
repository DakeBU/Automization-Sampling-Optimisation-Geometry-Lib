from verify97 import *
import os,time
OLD=C;C='7089dfb0698c50d3ffd0180fb58d06bb32e5d7dd'
assert head()==C and git('rev-parse',C+'^').decode().strip()==OLD
repair=rel(B/'samplinglib-search-label-repair97.json');changed=git('diff','--name-only',OLD,C).decode().splitlines();assert set(changed)=={CELL,repair}
def blob(commit,p):return git('show',commit+':'+rel(p))
before=blob(OLD,CELL);after=blob(C,CELL);a=json.loads(before);b=json.loads(after)
for parent,key in [('shared_floor_audit','searched'),('reuse_plan','searched_existing')]:
 old=a[parent][key][0];assert old.startswith('Source-first exact local and pinned Mathlib reuse search: ')
 a[parent][key][0]=old.replace('exact local and pinned','exact Samplinglib and pinned',1)
assert a==b and after==(R/CELL).read_bytes()
rr=load(repair);assert blob(C,repair)==(R/repair).read_bytes()
assert rr['original_commit']==OLD and rr['before_raw_sha256']==sha(before) and rr['after_raw_sha256']==sha(after)
search=rr['existing_search_evidence'];assert blob(OLD,search)==blob(C,search)
search_binding=next(x for x in load(O/'input-freeze97.json')['exact_commit_matches'] if x['path']==search)
assert sha((R/search).read_bytes())==rr['existing_search_raw_sha256']==search_binding['raw_sha256']
assert blob(OLD,search_binding['archive'])==blob(C,search_binding['archive'])
assert gzip.decompress(blob(C,search_binding['archive']))==(R/search).read_bytes()
srch=load(search);assert len(srch['local_results'])==5 and not rr['new_search_claim']
for x in srch['local_results']:
 raw=(R/x['file']).read_text(encoding='utf8');assert re.search(r'\btheorem\s+'+re.escape(x['declaration'].rsplit('.',1)[-1])+r'\b',raw)
freeze=load(O/'input-freeze97.json');assert freeze['status']=='PASS' and freeze['verified_commit']==OLD
for x in freeze['exact_commit_matches']+freeze['local_pinned_or_excluded_inputs']+freeze['preserved_collaborator_inputs']:
 if x['path']!=CELL:assert info(x['path'])['raw_sha256']==x['raw_sha256'],x['path']
for x in load(B/'independent-whole-math97/whole-math-decision97.native.json')['inputs']:assert info(x['path'])['raw_sha256']==x['raw_sha256'],x['path']
trial=load(O/'trialb0dafee/closed-trial-RAW-manifest97.json')
for x in trial['files']:assert info(x['path'])['raw_sha256']==x['raw_sha256']
save('metadata-transfer97.json',dict(status='PASS',verified_commit=C,original_commit=OLD,exact_changed_paths=changed,changed_fields=rr['exact_changed_fields'],existing_search=info(search),existing_local_producer_count=5,repair_receipt=info(repair),all_other_git_blobs_identical=True,all_prior_math_kernel_source_decoder_lesson_publication_inputs_RAW_identical=True,original_failed_trial=info(O/'trialb0dafee/closed-trial-RAW-manifest97.json'),new_search_claim=False))
freeze['verified_commit']=C;freeze['metadata_transfer']='metadata-transfer97.json'
for i,x in enumerate(freeze['exact_commit_matches']):
 if x['path']==CELL:freeze['exact_commit_matches'][i]=dict(**info(CELL),binding='exact repaired Git blob',git_blob=git('rev-parse',C+':'+CELL).decode().strip())
freeze['exact_commit_matches'].append(dict(**info(repair),binding='exact Git repair receipt',git_blob=git('rev-parse',C+':'+repair).decode().strip()))
save('current-input-freeze97.json',freeze)
source=load(O/'source-acceptance97.native.json');source['verified_commit']=C;source['unchanged_science_transfer']='metadata-transfer97.json';save('current-source-acceptance97.native.json',source)
scope=load(O/'science-scope97.json');scope['verified_commit']=C;scope['metadata_transfer']='metadata-transfer97.json';scope['changed_files']+= [repair]
for x in scope['scoped_git_blobs']:
 if x['path']==CELL:x['git_blob']=git('rev-parse',C+':'+CELL).decode().strip();x['git_raw_sha256']=sha(after)
scope['scoped_git_blobs'].append(dict(path=repair,git_blob=git('rev-parse',C+':'+repair).decode().strip(),git_raw_sha256=sha(blob(C,repair))))
save('current-science-scope97.json',scope)
kt=load(O/'kernel-transfer97.json');kt['verified_commit']=C;kt['narrow_metadata_transfer']='metadata-transfer97.json';save('current-kernel-transfer97.json',kt)
env=os.environ.copy();env.pop('ELAN_TOOLCHAIN',None);env['PYTHONUTF8']='1';env['LEAN_NUM_THREADS']='2';env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
PY=[sys.executable,'-X','utf8'];receipts=[]
for name,args in [('current-frontier',PY+['tools/astis_frontier_cells.py','check']),('current-contributor',PY+['tools/astis_contributor_contract.py','check','--base',BASE]),('current-committed-diff',['git','diff','--check',BASE,C])]:
 assert head()==C;start=time.time();p=subprocess.run(args,cwd=R,capture_output=True,env=env)
 (O/(name+'.stdout.log')).write_bytes(p.stdout);(O/(name+'.stderr.log')).write_bytes(p.stderr);save(name+'.receipt.json',dict(command=args,verified_commit=C,exit_code=p.returncode,seconds=time.time()-start,terminal_closed=True));receipts.append(info(O/(name+'.receipt.json')));print(name,p.returncode,flush=True);assert p.returncode==0,name
sys.path[:0]=[str(R),str(R/'tools')]
from tools import astis_publication as pub,astis
pub.check_advance([D],reviewed=True);save('current-publication-reviewed97.json',dict(status='PASS',verified_commit=C,declaration=D))
hits=astis.forbidden_pattern_hits();assert not hits;save('current-fake-closure97.json',dict(status='PASS',verified_commit=C,hits=hits))
reused=[]
for name in ['focused-module','publication','semantic']:
 q=O/'trialb0dafee'/(name+'.receipt.json');r=load(q);assert r['exit_code']==0 and r['verified_commit']==OLD;reused.append(dict(name=name,receipt=info(q),stdout=info(q.with_name(name+'.stdout.log')),stderr=info(q.with_name(name+'.stderr.log')),transfer='metadata-transfer97.json'))
save('current-checks-complete97.json',dict(status='PASS',verified_commit=C,fresh_receipts=receipts,reused_successful_unchanged_gates=reused,source=info(O/'current-source-acceptance97.native.json'),kernel_transfer=info(O/'current-kernel-transfer97.json'),reviewed_publication=info(O/'current-publication-reviewed97.json'),fake_closure_scan=info(O/'current-fake-closure97.json'),axiom_scan=info(O/'axiom-scan97.json'),metadata_transfer=info(O/'metadata-transfer97.json')))
assert head()==C
print('PASS exact repaired commit; all required science admission gates accepted')
