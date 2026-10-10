from pathlib import Path
import json,hashlib,subprocess,sys,datetime,concurrent.futures
r=Path('E:/Samplinglib');prefix='runs/20261007-companion-priority/pbps-conditional-gradient-variance';run=r/prefix;oldcommit='53f65a50263c13823aef5da7d9a3279de3514243';commit='8d950c37e41bd5d816c4132c6a5cdde0e30dcbee';cellpath='research-wiki/frontier-cells/ASTIS-SW-PBPS-conditional-gradient-variance.json';parent='AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance_nonneg'
sha=lambda b:hashlib.sha256(b).hexdigest();lf=lambda b:b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def put(p,j):p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def load(p):return json.loads((r/p).read_text(encoding='utf-8-sig'))
def bind(p):
 b=p.read_bytes();return {'path':p.relative_to(r).as_posix(),'bytes':len(b),'raw_sha256':sha(b),'lf_sha256':sha(lf(b))}
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=r).decode().strip()==commit
assert subprocess.check_output(['git','rev-parse','HEAD^'],cwd=r).decode().strip()==oldcommit
assert sha((run/'reviewer.exact.blocker.json').read_bytes())=='c9cdedc8c9f248526a790a9e789a8d57f2dbbf444637a30ba5b622d843ba2271'
assert sha((run/'reviewer.exact.lease.json').read_bytes())=='bc77f93c1aac1a5771d9c57eed3c06f639c393633b6ed74b1f65dfb7e6a21158'
old=load(prefix+'/reviewer.exact.bindings.json');negative=load(prefix+'/reviewer.exact.blocker.json');assert bind(run/'reviewer.exact.bindings.json')==negative['bindings']
assert load(prefix+'/reviewer.exact.lease.json')['status']=='CLOSED'
assert load(prefix+'/reviewer.exact1.lease.json')['status']=='OPEN'
change_paths=subprocess.check_output(['git','diff-tree','--no-commit-id','--name-only','-r',oldcommit,commit],cwd=r).decode().splitlines();overlaypaths=[prefix+'/contributor-cell-overlay48/cell.before.raw.snapshot.json',prefix+'/contributor-cell-overlay48/repair.json'];canonical=[p for p in change_paths if not p.startswith(prefix+'/reviewer.exact.') and p not in overlaypaths]
assert canonical==[cellpath],canonical
oldcell=json.loads(subprocess.check_output(['git','show',oldcommit+':'+cellpath],cwd=r));expected=json.loads(json.dumps(oldcell));expected['reuse_plan']['reused_declarations'].append(parent);cell=load(cellpath);assert cell==expected
assert cell['reuse_plan']['reused_declarations'].count(parent)==1
assert all(p.startswith(prefix+'/reviewer.exact.') or p==cellpath or p in overlaypaths for p in change_paths)
proposal=load(prefix+'/contributor-cell-overlay48/repair.json');before_raw=(run/'contributor-cell-overlay48/cell.before.raw.snapshot.json').read_bytes();assert json.loads(before_raw)==oldcell and sha(before_raw)==proposal['before_raw_sha256'];assert sha((r/cellpath).read_bytes())==proposal['after_raw_sha256'] and proposal['base_commit']==oldcommit and proposal['added_existing_direct_parent']==parent and proposal['exact_fields']==['/reuse_plan/reused_declarations']

# All prior actual/snapshot raw/LF bytes remain exact; new cell is a separate process-only projection.
pinrows=[]
for x in old['pins']:
 p=r/x['actual_path'];b=p.read_bytes();assert all(sha(lf(b) if 'lf' in k else b)==v for k,v in x['hashes'].items()),(x['owner'],x['path'])
 if x['bytes'] is not None:assert len(b)==x['bytes']
 pinrows.append({'owner':x['owner'],'slot':x['slot'],'original_path':x['path'],'exact_original_or_snapshot_path':x['actual_path'],'status':'PASS_UNCHANGED_ORIGINAL_BYTES'})
for x in old['actual_closed_parent_leases']:
 assert bind(r/x['binding']['path'])==x['binding'];j=load(x['binding']['path']);assert j.get('status',j.get('state'))=='CLOSED'
assert bind(run/'source.0.review.json')==old['source0_raw'] and bind(run/'source.1.review.json')==old['source1_raw'] and bind(run/'source.review.overlay1.checks.json')==old['source_overlay_raw']
assert negative['historical_administrative_mapping']==bind(run/'reviewer.exact.administrative-reconciliation.json')
pre=load(prefix+'/reviewer.exact.precompiler.json')
for x in pre['freeze36']+pre['recursive_local_imports63']:
 b=(r/x['path']).read_bytes();assert sha(b)==x['raw_sha256'] and sha(lf(b))==x['lf_sha256']
for x in old['Mathlib_API_fragments']:
 b=Path(x['path']).read_bytes();a,z=x['span'];fragment=b''.join(b.splitlines(keepends=True)[a-1:z]);assert sha(b)==x['whole_raw_sha256'] and sha(lf(b))==x['whole_lf_sha256'] and sha(fragment)==x['fragment_raw_sha256'] and sha(lf(fragment))==x['fragment_lf_sha256']
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=r/'.lake/packages/mathlib').decode().strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
tree={x.split('\t',1)[1]:x.split()[2] for x in subprocess.check_output(['git','ls-tree','-r',commit],cwd=r).decode().splitlines()};paths=[x['path'] for x in old['Git_blobs']];batch=subprocess.run(['git','cat-file','--batch'],cwd=r,input=('\n'.join(tree[p] for p in paths)+'\n').encode(),stdout=subprocess.PIPE,check=True).stdout;pos=0;gitrows=[]
for x,p in zip(old['Git_blobs'],paths):
 end=batch.index(b'\n',pos);size=int(batch[pos:end].split()[2]);pos=end+1;blob=batch[pos:pos+size];pos+=size+1;b=(r/p).read_bytes();assert lf(b)==lf(blob),p
 if p!=cellpath:assert sha(blob)==x['Git_blob_raw_sha256'] and sha(b)==x['working_raw_sha256'],p
 gitrows.append({'path':p,'working_raw_sha256':sha(b),'working_lf_sha256':sha(lf(b)),'Git_blob_raw_sha256':sha(blob),'status':'PASS_MINIMAL_CELL_REPAIR' if p==cellpath else 'PASS_UNCHANGED_EXACT_GIT_AND_RAW'})
compiler=load(prefix+'/reviewer.exact.focused.status.json');assert compiler['exit_code']==0 and compiler['checked_commit']==oldcommit and compiler['compiler_runs_by_this_verifier']==1
assert sha((run/'reviewer.exact.focused.log').read_bytes())==compiler['log_raw_sha256'] and compiler==negative['positive_gates']['actual_focused']
assert bind(run/'reviewer.exact.foreground-session.json') in load(prefix+'/reviewer.exact.run.json')['outputs']
sys.path.insert(0,str(r));sys.path.insert(0,str(r/'tools'));from tools import astis,astis_advance,astis_publication
cs=[['tools/astis_publication.py','check','--base','origin/main'],['tools/astis_semantic_roundtrip.py','check'],['tools/astis_frontier_cells.py','check'],['tools/astis_contributor_contract.py','check','--base','origin/main'],['git','-c','core.whitespace=cr-at-eol','diff','--check',oldcommit,commit,'--',cellpath]]
def check(z):
 i,c=z;cmd=c if c[0]=='git' else [sys.executable,*c];start=datetime.datetime.now(datetime.timezone.utc).isoformat();res=subprocess.run(cmd,cwd=r,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);p=run/f'reviewer.exact1.check.{i}.log';p.write_bytes(res.stdout);return {'command':cmd,'exit_code':res.returncode,'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),**bind(p),'tail':res.stdout.decode('utf-8',errors='replace')[-400:]}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:checks=list(pool.map(check,enumerate(cs)))
fake=astis.lean_diagnostics();assert fake['totals']['forbidden_hits']==0 and all(x['exit_code']==0 for x in checks)
decl='AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalGradientVariance.reflected_conditional_gradient_variance';astis_publication.check_advance([decl],reviewed=True)
state=astis_advance.current_advances();assert state['ASTIS-SA-20261007-PBPSConditionalGradientVariance']['state']=='PROVED_LOCAL';assert [k for k,j in state.items() if j.get('state')=='STABILIZING']==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel'];put(run/'reviewer.exact1.state.before.json',{'advance':state['ASTIS-SA-20261007-PBPSConditionalGradientVariance'],'sole_STABILIZING':state['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']})
out={'checked_commit':commit,'prior_exact_commit':oldcommit,'canonical_diff_paths':canonical,'actual_cell_repair':'only reuse_plan.reused_declarations appends exact existing Poincare.variance_nonneg once','cell_raw_LF':bind(r/cellpath),'original_negative':bind(run/'reviewer.exact.blocker.json'),'original_negative_lease':bind(run/'reviewer.exact.lease.json'),'original_rawLF_pin_checks':pinrows,'Git_rawLF_checks':gitrows,'source0_original_negative':old['source0_raw'],'source1_accepted_original':old['source1_raw'],'source_overlay_original':old['source_overlay_raw'],'historical_admin_reconciliation':bind(run/'reviewer.exact.administrative-reconciliation.json'),'math_freeze36_local_imports63_current_strict':bind(run/'reviewer.exact.precompiler.json'),'original53_actual_focused_reused':compiler,'original_foreground_session':bind(run/'reviewer.exact.foreground-session.json'),'compiled_standard3_sets':old['compiled_standard_axiom_sets'],'wholemath_and8actualMathlibAPI_spans_reused':True,'fresh_checks':checks,'source_reviewed_publication_admission_gate':'PASS','fresh_fake_closure':fake['totals'],'compiler_this_stage':'NOT_STARTED_CLOSED'}
put(run/'reviewer.exact1.bindings.json',out)
print(json.dumps({'checked_commit':commit,'pinchecks':len(pinrows),'Gitchecks':len(gitrows),'new_compiler_runs':0,'prior_actual_focused_jobs':3886,'fresh_checks':[x['exit_code'] for x in checks],'fake':fake['totals'],'reviewed_admission':'PASS'}))
