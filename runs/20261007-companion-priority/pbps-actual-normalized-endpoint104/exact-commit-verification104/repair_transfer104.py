from context104_repaired import *
import os,time
OLD='403c6ea6bc44847ee50b0225c2da166c37e2b279'
assert head()==C and git('rev-parse',C+'^').decode().strip()==OLD
helper=rel(B/'check104.py');repair=rel(B/'metadata-repair104/repair104.json')
changed=set(git('diff','--name-only',OLD,C).decode().splitlines());assert changed=={CELL,helper,repair}
oldcell=json.loads(git('show',OLD+':'+CELL));newcell=load(CELL);expected=copy.deepcopy(oldcell)
oldtext='Actual93/97/102/103 and fixed Mathlib density-product, sigma-finiteness, lintegral/map and measure extensionality APIs; compatible upstream searched in retrieval.'
newtext='Samplinglib actual93/97/102/103 and fixed Mathlib density-product, sigma-finiteness, lintegral/map and measure extensionality APIs; compatible upstream searched in retrieval.'
for a,b in [('shared_floor_audit','searched'),('reuse_plan','searched_existing')]:assert expected[a][b][2]==oldtext;expected[a][b][2]=newtext
assert newcell==expected and git('show',C+':'+CELL)==(R/CELL).read_bytes()
hb=git('show',OLD+':'+helper);ha=git('show',C+':'+helper)
before=b"'graph':['tools/astis_publication.py','graph-check','--cell','ASTIS-SW-PBPS-actual-phase-normalization']"
after=b"'graph':['tools/astis_publication.py','graph-check','--cell','ASTIS-SW-PBPS-actual-normalized-endpoint-sector']"
assert hb.count(before)==1 and hb.replace(before,after)==ha==(R/helper).read_bytes()
rr=load(repair);assert rr['original_science_commit']==OLD
e=rr['search_evidence'];assert info(e['path'])['raw_sha256']==e['raw_sha256'];retr=load(e['path']);assert len(retr['actual_producers'])==4
for x in retr['actual_producers'].values():assert info(x['artifact']['path'])['raw_sha256']==x['artifact']['raw_sha256']
freeze=load(O/'input-freeze104.json');assert freeze['status']=='PASS' and freeze['verified_commit']==OLD
for x in freeze['exact_commit_matches']+freeze['local_pinned_or_excluded_inputs']+freeze['preserved_collaborator_inputs']:
 if x['path'] not in [CELL,helper]:assert info(x['path'])['raw_sha256']==x['raw_sha256'],x['path']
save('narrow-repair-transfer104.native.json',dict(status='PASS',verified_commit=C,original_science=OLD,changed_paths=sorted(changed),two_label_changes_only=True,helper_never_used_as104graph_evidence=True,helper_correct_cell_only=True,existing_four_producer_search_evidence=info(e['path']),all_science_proof_source_decoder_lesson_publication_ledger_unchanged=True,original_failed_trial=info(O/'original-trial104.native.json')))
newfreeze=copy.deepcopy(freeze);newfreeze['verified_commit']=C;newfreeze['original_input_freeze']=info(O/'input-freeze104.json');newfreeze['narrow_repair']=info(O/'narrow-repair-transfer104.native.json')
for x in newfreeze['exact_commit_matches']:
 if x['path'] in [CELL,helper]:
  p=x['path'];x.clear();x.update(info(p));x.update(binding='exact repaired Git blob',git_blob=git('rev-parse',C+':'+p).decode().strip())
newfreeze['exact_commit_matches'].append(dict(**info(repair),binding='exact repaired Git blob',git_blob=git('rev-parse',C+':'+repair).decode().strip()))
save('input-freeze104-repaired.json',newfreeze)
for name in ['source-acceptance104.native.json','metadata-transfer104.json','primary-scope104.native.json','science-scope104.json','kernel-transfer104.json']:
 x=load(O/name);assert x['status']=='PASS' and x['verified_commit']==OLD
 save(name.replace('104','104-repaired'),dict(status='PASS',verified_commit=C,unchanged_evidence=info(O/name),narrow_repair=info(O/'narrow-repair-transfer104.native.json'),reason='Exact diff restricted to two cell retrieval labels and unused graph-helper target plus repair receipt; no mathematical/source/decoder/publication change.'))
env=os.environ.copy();env.pop('ELAN_TOOLCHAIN',None);env['PYTHONUTF8']='1';env['LEAN_NUM_THREADS']='2';env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
checks=[('frontier',[sys.executable,'-X','utf8','tools/astis_frontier_cells.py','check']),('contributor',[sys.executable,'-X','utf8','tools/astis_contributor_contract.py','check','--base',BASE]),('publication',[sys.executable,'-X','utf8','tools/astis_publication.py','check','--base',BASE]),('semantic',[sys.executable,'-X','utf8','tools/astis_semantic_roundtrip.py','check']),('committed-diff',['git','diff','--check',BASE,C])]
receipts=[]
for name,cmd in checks:
 assert head()==C;t=time.time();q=subprocess.run(cmd,cwd=R,env=env,capture_output=True)
 (O/(name+'-repaired.stdout.log')).write_bytes(q.stdout);(O/(name+'-repaired.stderr.log')).write_bytes(q.stderr)
 save(name+'-repaired.receipt.json',dict(command=cmd,verified_commit=C,exit_code=q.returncode,terminal_closed=True,seconds=time.time()-t));receipts.append(name+'-repaired.receipt.json');print(name,q.returncode,flush=True);assert q.returncode==0
sys.path[:0]=[str(R),str(R/'tools')]
from tools import astis_publication as pub
from tools import astis
pub.check_advance([D],reviewed=True);hits=astis.forbidden_pattern_hits();assert not hits
save('fake-closure104-repaired.json',dict(status='PASS',verified_commit=C,hits=hits))
save('checks-complete104-repaired.json',dict(status='PASS',verified_commit=C,receipts=receipts,focused_module_transferred_from_original=info(O/'focused-module.receipt.json'),original_kernel_and_axioms=info(O/'kernel-transfer104.json'),reviewed_publication=True,fake_closure_hits=0))
print('READY_FOR_ADMISSION',C)
