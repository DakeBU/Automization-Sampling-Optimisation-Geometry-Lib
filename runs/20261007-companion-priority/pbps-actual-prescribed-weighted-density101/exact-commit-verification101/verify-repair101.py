from context101 import *
import os,time
C='4713623d3edbc5d258e563e8521271c316f0dc8c'
OLD='4808820b06e696524a9bd45b8d61f615f592999b'
BASE='1dda6b4bbcdcd3b3131d86a5d90e5f9743e250b3'
assert head()==C and git('rev-parse',C+'^').decode().strip()==OLD
closure=load(O/'closed-trial480-manifest101.native.json')
for x in closure['owned_artifacts']:assert info(x['path'])['raw_sha256']==x['raw_sha256'],x['path']
rp=rel(B/'frontier-search-label-repair101.json');repair=load(rp)
assert set(git('diff','--name-only',OLD,C).decode().splitlines())=={CELL,rp}
oldraw=git('show',OLD+':'+CELL);newraw=git('show',C+':'+CELL)
assert newraw==(R/CELL).read_bytes() and git('show',C+':'+rp)==(R/rp).read_bytes()
assert sha(oldraw)==repair['before_cell_RAW_sha256'] and sha(newraw)==repair['after_cell_RAW_sha256']
oldcell=json.loads(oldraw);cell=load(CELL);expected=copy.deepcopy(oldcell)
for a,k in [('shared_floor_audit','searched'),('reuse_plan','searched_existing')]:expected[a][k].append(repair['added_label'])
assert expected==cell and cell['shared_floor_audit']['searched']==cell['reuse_plan']['searched_existing']
assert repair['existing_retrieval']==load(PRE/'retrieval101.json')
q=repair['existing_retrieval']['queries'][0];assert q['exit_code']==0 and q['command'][-1]=='.lake/packages/mathlib/Mathlib/Data/ENNReal/Real.lean' and '297:theorem ofReal_mul' in q['stdout']
assert 'Samplinglib' in repair['added_label'] and 'Mathlib' in repair['added_label']
f=load(O/'input-freeze101.json');assert f['status']=='PASS' and f['verified_commit']==OLD
for x in f['exact_commit_matches']+f['local_pinned_or_excluded_inputs']+f['preserved_collaborator_inputs']:
 if x['path']!=CELL:assert info(x['path'])['raw_sha256']==x['raw_sha256'],x['path']
for x in load(B/'independent-whole-math101/prepared-inputs101.native.json')['inputs']:assert info(x['path'])['raw_sha256']==x['raw_sha256'],x['path']
assert len(f['preserved_collaborator_inputs'])==21
for n in ['focused-module','contributor','publication','semantic']:
 r=load(O/(n+'.receipt.json'));assert r['verified_commit']==OLD and r['exit_code']==0
save('metadata-repair-admission101.native.json',dict(status='PASS',verified_commit=C,original_commit=OLD,repair=info(rp),original_trial=info(O/'closed-trial480-manifest101.native.json'),exact_two_file_delta=True,only_cell_search_label_appended=True,no_new_search_claim=True,existing_preproof_search=info(PRE/'retrieval101.json'),original_cell_RAW=sha(oldraw),current_cell=info(CELL),old_cell_recovery=OLD+':'+CELL,all_other_Git_blobs_unchanged=True,all21_collaborator_RAWs_unchanged=True,explicit_root_dispatch='Root froze 4713623d3edbc5d258e563e8521271c316f0dc8c and authorized independent admission after this repair and remaining checks.'))
f['verified_commit']=C;f['transfer_from']=info(O/'input-freeze101.json');f['repair_admission']=info(O/'metadata-repair-admission101.native.json')
f['exact_commit_matches']=[dict(**info(CELL),binding='exact Git blob after narrow independent search-label repair',git_blob=git('rev-parse',C+':'+CELL).decode().strip()) if x['path']==CELL else x for x in f['exact_commit_matches']]
f['exact_commit_matches'].append(dict(**info(rp),binding='exact Git blob',git_blob=git('rev-parse',C+':'+rp).decode().strip()))
save('input-freeze101-repaired.json',f)
for name in ['source-acceptance101.native.json','kernel-transfer101.json','metadata-transfer101.json','primary-scope101.native.json','axiom-scan101.json']:
 old=load(O/name);assert old['status']=='PASS' and old['verified_commit']==OLD
 new=copy.deepcopy(old);new['verified_commit']=C;new['unchanged_evidence_transfer']=dict(from_commit=OLD,to_commit=C,original_receipt=info(O/name),justification='Only two-file cell search-label repair; all original science Git blobs and native original RAW evidence unchanged, independently rechecked.')
 save(name.replace('101','101-repaired'),new)
scope=load(O/'science-scope101.json');scope['verified_commit']=C;scope['changed_files']=git('diff','--name-only',BASE,C).decode().splitlines();scope['original_scope_receipt']=info(O/'science-scope101.json')
for x in scope['scoped_git_blobs']:
 if x['path']==CELL:x.update(git_blob=git('rev-parse',C+':'+CELL).decode().strip(),git_raw_sha256=sha(newraw))
scope['scoped_git_blobs'].append(dict(path=rp,git_blob=git('rev-parse',C+':'+rp).decode().strip(),git_raw_sha256=info(rp)['raw_sha256']))
save('science-scope101-repaired.json',scope)
env=os.environ.copy();env['PYTHONUTF8']='1';env.pop('ELAN_TOOLCHAIN',None);env['LEAN_NUM_THREADS']='2';env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
PY=[sys.executable,'-X','utf8']
checks=[('frontier-repaired',PY+['tools/astis_frontier_cells.py','check']),('contributor-repaired',PY+['tools/astis_contributor_contract.py','check','--base',BASE]),('publication-repaired',PY+['tools/astis_publication.py','check','--base',BASE]),('committed-diff',['git','diff','--check',BASE,C])]
receipts=[]
for name,argv in checks:
 assert head()==C;start=time.time()
 with (O/(name+'.stdout.log')).open('xb') as out,(O/(name+'.stderr.log')).open('xb') as err:p=subprocess.run(argv,cwd=R,env=env,stdout=out,stderr=err)
 save(name+'.receipt.json',dict(command=argv,verified_commit=C,exit_code=p.returncode,seconds=time.time()-start,terminal_closed=True));receipts.append(name+'.receipt.json');print(name,p.returncode,flush=True);assert p.returncode==0,name
sys.path[:0]=[str(R),str(R/'tools')]
from tools import astis_publication as pub
from tools import astis
pub.check_advance([D],reviewed=True);save('publication-reviewed101.json',dict(status='PASS',verified_commit=C,declaration=D))
hits=astis.forbidden_pattern_hits();save('fake-closure101.json',dict(status='PASS' if not hits else 'FAIL',verified_commit=C,hits=hits));assert not hits
assert head()==C
save('checks-complete101.json',dict(status='PASS',verified_commit=C,receipts=receipts,unchanged_successful_checks_transferred=[dict(check=n,original_receipt=info(O/(n+'.receipt.json')),original_commit=OLD,verified_commit=C,reason='Unchanged code, kernel inputs, source, decoder and semantic audit; exact narrow metadata delta validated.') for n in ['focused-module','semantic']],reviewed_publication=True,fake_closure_hits=0,axiom_scan='axiom-scan101-repaired.json',kernel_transfer='kernel-transfer101-repaired.json',metadata_repair='metadata-repair-admission101.native.json'))
print('PASS_REPAIRED_EXACT_COMMIT_ALL_GATES',C,flush=True)
