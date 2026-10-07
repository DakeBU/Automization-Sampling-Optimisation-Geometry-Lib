import json,hashlib,subprocess,datetime,sys
from pathlib import Path
r=Path('E:/Samplinglib');run=r/'runs/20261007-companion-priority/pbps-macroscopic-energy';out=run/'repository-seal50-repaired';old=run/'repository-seal50';overlay=run/'integration-cell-overlay50';commit='161c2337f23807bfd01d99be95cdd18442a58fee';parent='6b6877482d1c4316b9a8009ebc8d0b0cff6e10cf';cell='research-wiki/frontier-cells/ASTIS-SW-PBPS-macroscopic-energy.json';notespath=(run/'integration.notes.json').relative_to(r).as_posix()
H=lambda b:hashlib.sha256(b).hexdigest();LF=lambda b:b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def read(p):return json.loads(Path(p).read_text('utf-8'))
def encode(d):return (json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode()
def dump(p,d):Path(p).write_bytes(encode(d))
def bind(p):
 p=Path(p);b=p.read_bytes();return {'path':p.relative_to(r).as_posix(),'bytes':len(b),'raw_sha256':H(b),'lf_sha256':H(LF(b))}
def git(*a):return subprocess.check_output(['git',*a],cwd=r)
def diff(a,b,p=''):
 if type(a)!=type(b):return[p]
 if isinstance(a,dict):return sum([diff(a.get(k),b.get(k),p+'/'+k)for k in a.keys()|b.keys()],[])
 if isinstance(a,list):return[p]if len(a)!=len(b)else sum([diff(x,y,p+'/'+str(i))for i,(x,y)in enumerate(zip(a,b))],[])
 return[p]if a!=b else[]
assert git('rev-parse','HEAD').decode().strip()==commit and git('rev-parse',commit+'^').decode().strip()==parent
lease=read(out/'reviewer.seal.lease.json');assert lease['status']=='OPEN'and lease['compiler']=='NOT_STARTED_CLOSED'
original=read(old/'bindings.json');oldseal=read(old/'ProofSeal50.json');assert oldseal['status']=='TYPED_BOUNDARY_EXACT_REPOSITORY_ADMIN_INPUT_BLOCKED';assert H((old/'ProofSeal50.json').read_bytes())=='e17343882a5a2eff2de65551e6e99bbc0b6a8b56a40d43be86908582ed4b0f10';assert H((old/'reviewer.seal.lease.json').read_bytes())=='710565d9325794f30e38c1213883952c2016c183b4242f7ccd59144334675daf'and read(old/'reviewer.seal.lease.json')['status']=='CLOSED'
reused=[]
for x in read(old/'run.json')['outputs']:
 d=bind(r/x['path']);assert all(d[k]==x[k]for k in ['bytes','raw_sha256','lf_sha256']);reused.append(d)
er=read(run/'exposition-seal50/run.json');assert H(json.dumps(er['run_payload'],ensure_ascii=False,sort_keys=False,separators=(',',':')).encode())==er['review_run_sha256']
for x in er['run_payload']['inputs']+er['run_payload']['outputs']+[er['run_payload']['expected_final_closed_lease']]:
 d=bind(r/x['path']);assert all(d[k]==x[k]for k in ['bytes','raw_sha256','lf_sha256'])
assert read(run/'exposition-seal50/lease.json')['status']=='CLOSED';assert H((run/'exposition-seal50/receipt.json').read_bytes())=='64e49476d508fa0f53f5e0da89801c14aae120fd5c7e21547f1ea3fe2d00b4a6'
op=read(overlay/'operations.json');assert op['original_commit']==parent
for key in ['before_notes','after_notes','before_cell','after_cell']:
 x=op[key];d=bind(r/x['path']);assert all(d[k]==x[k]for k in ['bytes','raw_sha256','lf_sha256'])
assert LF((overlay/'cell.before.6b.raw.snapshot.json').read_bytes())==LF(git('show',parent+':'+cell));assert LF((overlay/'notes.before.6b.raw.snapshot.json').read_bytes())==LF(git('show',parent+':'+notespath))
assert (overlay/'cell.after.working.raw.snapshot.json').read_bytes()==(r/cell).read_bytes()==(old/'cell.current.working.raw.snapshot.json').read_bytes();assert git('show',commit+':'+cell)in((r/cell).read_bytes(),LF((r/cell).read_bytes()))
c=read(r/cell);assert c['status']=='independently_verified';sg=c['evidence']['serialized_shared_gate'];assert (sg['root_jobs'],sg['test_jobs'],sg['registry_count'])==(9153,9435,491) and sg['status']=='PASS'and sg['proof_commit']=='864ff305b78030d9e1c840938e82fefcf4185515'
before=read(overlay/'notes.before.6b.raw.snapshot.json');after=read(run/'integration.notes.json');delta=diff(before,after);assert set(delta)=={'/shared_files/6/path','/shared_files/6/bytes','/shared_files/6/raw_sha256','/shared_files/6/lf_sha256','/integration_metadata_repair'};assert after['shared_files'][6]==bind(r/cell)
assert after['integration_metadata_repair']['original_negative_proofseal']==bind(old/'ProofSeal50.json') and after['integration_metadata_repair']['original_exposition_receipt']==bind(run/'exposition-seal50/receipt.json')
paths=git('diff','--name-only',parent,commit).decode().splitlines();allowed=[cell,notespath];canonical=[p for p in paths if not p.startswith(tuple((run/name).relative_to(r).as_posix()+'/'for name in ['repository-seal50','exposition-seal50','integration-cell-overlay50']))];assert set(canonical)==set(allowed)
# Science/source/compiled gates and current static pixels/graph all unchanged from the original negative review.
for x in original['exact50_outputs_reused']+original['root12_actual_status_log_rawLF']+original['visual_artifacts_currentGit']+[original['root_actual_closed_lease'],original['current_official_graph'],original['static_original_companion']]+original['static_complete_source_Test_pages']:
 d=bind(r/x['path']);assert all(d[k]==x[k]for k in ['bytes','raw_sha256','lf_sha256']);reused.append(d)
for x in original['prior1239_Git_current_rawLF']:
 p=r/x['path'];d=bind(p);assert all(d[k]==x[k]for k in ['bytes','raw_sha256','lf_sha256']);blob=git('show',commit+':'+x['path']);assert blob in(p.read_bytes(),LF(p.read_bytes()))
# Bind the exact complete input classes of the official digest to currentcommit; avoid any global proof/whitespace replay.
inputpaths=git('ls-files','--','AutoSamplingTheory','Tests','AutoSamplingTheory.lean','Tests.lean','website/content/publications','research-wiki/frontier-cells').decode().splitlines();inputpaths=[p for p in inputpaths if p.endswith('.lean')or p.endswith('.json')];data=subprocess.check_output(['git','cat-file','--batch'],input=''.join(commit+':'+p+'\n'for p in inputpaths).encode(),cwd=r);pos=0;graphpins=[]
for p in inputpaths:
 end=data.index(b'\n',pos);size=int(data[pos:end].split()[-1]);blob=data[end+1:end+1+size];pos=end+size+2;b=(r/p).read_bytes();assert blob in(b,LF(b)),('GRAPH_INPUT_GIT_DRIFT',p);graphpins.append({**bind(r/p),'Git_blob_sha256':H(blob)})
sys.path[:0]=[str(r),str(r/'tools'),str(r/'website/scripts')];import publication_reader
from tools import astis_advance
digest=publication_reader.graph_input_digest();assert digest==original['current_WORKING_publication_digest']==read(r/'_site/data/underlying-lean-graph.json')['publication_inputs_sha256']
states=astis_advance.current_advances();assert states['ASTIS-SA-20261007-PBPSMacroscopicEnergy']['state']=='VERIFIED';assert {k:v.get('owner_id')for k,v in states.items()if v.get('state')=='STABILIZING'}==read(run/'verified.json')['sole_STABILIZING']
commands=[[sys.executable,'tools/astis_publication.py','check','--base','origin/main'],[sys.executable,'tools/astis_frontier_cells.py','check'],[sys.executable,'tools/astis_publication.py','graph-check','--cell','ASTIS-SW-PBPS-macroscopic-energy','--output','_site'],['git','-c','core.whitespace=cr-at-eol','diff','--check',parent,commit]];checks=[]
for i,command in enumerate(commands):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.run(command,cwd=r,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=out/f'check.{i}.log';log.write_bytes(p.stdout);x={'command':command,'exit_code':p.returncode,'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'log':bind(log)};dump(out/f'check.{i}.status.json',x);checks.append(x);print('freshrepair',i,p.returncode,flush=True)
assert all(x['exit_code']==0 for x in checks)
bindings={'checked_commit':commit,'original_negative_commit':parent,'science_commit_reused':'864ff305b78030d9e1c840938e82fefcf4185515','original_negative_proofseal':bind(old/'ProofSeal50.json'),'original_CLOSED_prooflease':bind(old/'reviewer.seal.lease.json'),'original_negative_exposition':bind(run/'exposition-seal50/receipt.json'),'original_CLOSED_expositionlease':bind(run/'exposition-seal50/lease.json'),'exact_overlay':bind(overlay/'operations.json'),'two_canonical_paths':canonical,'notes_actual_JSON_delta':delta,'cell_current_exact_Git_rawLF':bind(r/cell),'cell_equals_original_working_bytes':True,'root12_gates_unchanged_reused':original['root12_actual_status_log_rawLF'],'root12_9153_9435_Registry491_reused':True,'rootlease_scope_erratum_preserved':original['runtime_lease_template_erratum'],'strict_unchanged_prior_bindings':reused,'exact_official_graph_input_bindings':graphpins,'exact_official_graph_input_digest':digest,'graph_unchanged':original['current_official_graph'],'affected_branch_reused':original['actual50_module_declaration_edges'],'source_gate_reused':'Independent exact864 VERIFIED/source1/nativeblind/wholeproof unchanged. Source0metadata negative and originalordered schemas remain immutable.','fake_closure_reused':original['fake_closure'],'fresh_noncompiler_checks':checks,'whitespace_reuse':original['new_whitespace'],'static_actualdesktop_reuse':original['visual_observations'],'no_new_Lean_compiler_or_VERIFIED':True,'remaining':'Remote161notpushedCIpending; fullreader/ExpositionSeal/main/live/PURIFIED/roughH1/Gamma/halfturn/mains/errors/caps/cost/composition/wholefourGoal OPEN.'};dump(out/'bindings.json',bindings)
print(json.dumps({'checked':commit,'status':'ACCEPT_SCOPED_REPAIR','graphinputs':len(graphpins),'fresh':[x['exit_code']for x in checks],'digest':digest,'canonical':canonical}))
