from pathlib import Path
import json,hashlib,gzip,subprocess,datetime,sys,concurrent.futures
r=Path(r'E:/Samplinglib');run=r/'runs/20261007-companion-priority/gaussian-canonical-kl-fisher';out=run/'repository-seal43';prefix=run.relative_to(r).as_posix();commit='4dff1d75c51c952281242333fc8ec48426a964a3';original='4f3e7bc45ba79e0f53a50064ae49bd1be385d2c9';port='7e5afc8798bb96adcc3e247fec2e943f161e9aea';proof='19b569ae0fe37c97da0f98b4d1f4933ebabc7052';main='c05de12e6a8ca7af8ce2df8608836f8d4e90f617';sha=lambda b:hashlib.sha256(b).hexdigest();lf=lambda b:b.replace(b'\r\n',b'\n').replace(b'\r',b'\n');load=lambda p:json.loads((r/p).read_text(encoding='utf-8-sig'))
sys.path.insert(0,str(r));sys.path.insert(0,str(r/'tools'));from tools import astis
blob=lambda c,p:subprocess.check_output(['git','show',c+':'+p],cwd=r)
def bind(p):
 b=(r/p).read_bytes();return {'path':p,'raw_sha256':sha(b),'lf_sha256':sha(lf(b)),'bytes':len(b)}
def stream_hash(p,compressed=False):
 h=hashlib.sha256();n=0
 with (gzip.open(p,'rb') if compressed else p.open('rb')) as f:
  while data:=f.read(1048576):h.update(data);n+=len(data)
 return {'raw_sha256':h.hexdigest(),'bytes':n}
def write(p,j):(out/p).write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
a=load(prefix+'/reviewer.exact.check.5.archive.json');arc=bind(a['archive_path']);assert arc['raw_sha256']==a['archive_raw_sha256'] and arc['bytes']==a['archive_bytes'];decomp=stream_hash(r/a['archive_path'],True);assert decomp=={'raw_sha256':a['original_raw_sha256'],'bytes':a['original_bytes']};backup=stream_hash(r/a['local_exact_backup']);assert backup==decomp
# Raw original is retained locally but ignored; preserve and confirm bytes without expanding output.
rawlocal=stream_hash(r/a['original_path']);assert rawlocal==decomp
raworiginal=blob(original,a['original_path']);assert sha(raworiginal)==a['original_raw_sha256'] and len(raworiginal)==a['original_bytes'];del raworiginal
assert blob(commit,a['archive_path'])==(r/a['archive_path']).read_bytes()
clean=load(prefix+'/clean-port.json');assert clean['only_storage_delta']==a
storage_delta=subprocess.check_output(['git','diff','--name-status',original,port],cwd=r).decode().splitlines();assert len(storage_delta)==4 and any(x=='D\t'+a['original_path'] for x in storage_delta)
incoming=subprocess.check_output(['git','diff','--name-status',port,commit],cwd=r).decode().splitlines();assert len(incoming)==10 and not any(x.endswith('.lean') for x in incoming)
assert not subprocess.check_output(['git','diff','--name-only',original,commit,'--','*.lean','lean-toolchain','lake-manifest.json','lakefile.lean'],cwd=r)
parents=subprocess.check_output(['git','show','-s','--format=%P',commit],cwd=r).decode().strip().split();assert parents==[port,main]
retained=subprocess.check_output(['git','rev-parse','refs/heads/codex/sphmc-standardized-rgo'],cwd=r).decode().strip();assert retained==original
cleanbindings=[]
for p in clean['exact_unchanged_paths']:
 originalblob=blob(original,p);portblob=blob(port,p);currentblob=blob(commit,p);assert originalblob==portblob==currentblob,p
 working=(r/p).read_bytes();assert lf(working)==lf(currentblob),p
 cleanbindings.append({'path':p,'original_port_current_blob_raw_sha256':sha(currentblob),'current_working':bind(p),'all_three_blobs_identical':True})
# Current science literally remains the independently VERIFIED43 commit, including original reviews/decoder/overlays and51 imported modules.
old=load(prefix+'/reviewer.exact.bindings.json');scipaths={x['path'] for x in old['git_blobs'] if x['path'].endswith('.lean') and x['status']=='PASS'}
scipaths|={prefix+'/'+p for p in ['verified.json','whole-proof-review43/reviewer.math.review.json','whole-proof-review43/reviewer.math.run.json','whole-proof-review43/reviewer.math.checks.json','math-freeze.json','source.0.review.json','source.1.review.json','source.review.repair1.lease.json','source.review.repair1.overlay-review.json','anonymous-decoder/packet0.json','anonymous-decoder/result0.json','anonymous-decoder/run.json','exposition-provenance-overlay/repair.json']}
science=[]
for p in sorted(scipaths):
 baseline=original if p.endswith('/verified.json') else proof; bb=blob(baseline,p);bc=blob(commit,p);working=(r/p).read_bytes();assert bb==bc and lf(working)==lf(bc),p
 science.append({'path':p,'proof_current_Git_blob_raw_sha256':sha(bc),'working':bind(p),'proof_current_blob_identical':True,'baseline_commit':baseline})
# Actual root9149/9427 evidence and post-main gates; logged execution is bracketed by real CLOSED leases.
integration=load(prefix+'/integration.json');rootlease=load(prefix+'/root.integration.lease.json');postlease=load(prefix+'/root.post-main.lease.json');assert rootlease['status']=='CLOSED' and rootlease['exit_code']==0 and postlease['status']=='CLOSED' and postlease['exit_code']==0 and postlease['checked_commit']==commit
assert integration['aggregate_summary']=={'root_build_jobs':9149,'tests_build_jobs':9427,'registry_leaves':487}
agg=(run/'aggregate.log').read_text(encoding='utf8');assert 'Build completed successfully (9149 jobs).' in agg and 'Build completed successfully (9427 jobs).' in agg and 'ASTIS check passed' in agg
assert load(prefix+'/aggregate.status.json')['exit_code']==0
postgates=[]
for tag in ['publication','contributor','site-build','official-graph','graph','site-check']:
 p=prefix+f'/post-main.{tag}.status.json';j=load(p);assert j['exit_code']==0 and j['checked_commit']==commit
 postgates.append({'label':tag,'status':bind(p),'log':bind(prefix+f'/post-main.{tag}.log'),'command':j['command'],'exit_code':0,'checked_commit':commit})
# Fresh narrow source/metadata/static checks, no compiler or site rebuild.
commands=[['tools/astis_publication.py','check','--base','origin/main'],['tools/astis_semantic_roundtrip.py','check'],['tools/astis_frontier_cells.py','check'],['tools/astis_process_memory.py','check'],['tools/astis_contributor_contract.py','check','--base','origin/main'],['tools/astis_publication.py','graph-check','--cell','ASTIS-SW-SPHMC-standardized-rgo-kl-fisher','--output','_site'],['website/scripts/check_site.py']]
def check(item):
 i,c=item;started=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.run([sys.executable]+c,cwd=r,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);fn=f'reviewer.repository.check.{i}.log';(out/fn).write_bytes(p.stdout)
 return {'command':c,'exit_code':p.returncode,'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'log':bind((out/fn).relative_to(r).as_posix()),'tail':p.stdout.decode('utf8',errors='replace')[-500:]}
with concurrent.futures.ThreadPoolExecutor(max_workers=7) as ex:checks=list(ex.map(check,enumerate(commands)))
assert all(x['exit_code']==0 for x in checks)
fake=astis.lean_diagnostics();assert fake['totals']['forbidden_hits']==0
# Snapshot single current-head workflow batch; PR rollup includes a previous-head contributor result, not credited here.
cmd=['gh','run','list','--repo','DakeBU/Automization-Sampling-Optimisation-Geometry-Lib','--commit',commit,'--limit','8','--json','databaseId,headSha,name,status,conclusion,workflowName,url'];observed=datetime.datetime.now(datetime.timezone.utc).isoformat();rr=subprocess.run(cmd,cwd=r,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=35);(out/'reviewer.repository.remote315.head-runs.raw.json').write_bytes(rr.stdout)
remote={'observed_utc':observed,'command':cmd,'exit_code':rr.returncode,'raw':bind((out/'reviewer.repository.remote315.head-runs.raw.json').relative_to(r).as_posix()),'runs':json.loads(rr.stdout) if rr.returncode==0 else [],'scope':'Single bounded snapshot only. No inference from previous-head rollup, old42 CI, or running checks; PR315 remains draft/open; no current43 merge/live credit.'}
if rr.returncode==0:assert all(x['headSha']==commit for x in remote['runs'])
outjson={'checked_commit':commit,'verified_proof_commit':proof,'original_shared_commit':original,'clean_port_commit':port,'merged_main_commit':main,'archive':{'receipt':bind(prefix+'/reviewer.exact.check.5.archive.json'),'compressed':arc,'decompressed':decomp,'local_backup':backup,'retained_local_original':rawlocal,'original_commit_raw_matches':True,'current_commit_archive_matches':True,'storage_delta':storage_delta,'only_failed_diagnostic_storage_changed':True},'clean_port':{'receipt':bind(prefix+'/clean-port.json'),'unchanged_bindings':cleanbindings,'retained_original_branch':retained},'incoming_main':{'parents':parents,'changes':incoming,'all_Lean_and_toolchain_unchanged':True,'scope':'10 protocol/attribution/OpenAI-intake/site changes; this43 proof uses no OpenAI math theorem or source package. No shared proof/assumption or source boundary changed.'},'exact_science_inputs':science,'root_gate':{'reused':True,'working_head_at_execution':proof,'science_and_shared_integrated_tree_preserved_via_original4f_port7e5_current4dff':True,'integration':bind(prefix+'/integration.json'),'root_lease':bind(prefix+'/root.integration.lease.json'),'aggregate':bind(prefix+'/aggregate.log'),'status':bind(prefix+'/aggregate.status.json'),'root_build_jobs':9149,'tests_jobs':9427,'Registry_leaves':487,'compiler_started_by_repository_verifier':False},'root_post_main_gate':{'lease':bind(prefix+'/root.post-main.lease.json'),'gates':postgates},'fresh_independent_checks':checks,'static_fake_closure':{'status':'PASS','files':fake['totals']['files'],'hits':0},'remote':remote,'compiler':'NOT_STARTED_CLOSED'}
write('reviewer.repository.bindings.json',outjson)
print(json.dumps({'archive_decompressed':decomp,'original_retained':retained,'science_inputs':len(science),'clean_port_inputs':len(cleanbindings),'postmain_checks':len(postgates),'independent_checks':[(x['command'][0],x['exit_code'],x['tail']) for x in checks],'fake':outjson['static_fake_closure'],'remote':remote},ensure_ascii=False))

