import json,hashlib,subprocess,re,gzip,datetime,sys
from pathlib import Path
r=Path('E:/Samplinglib');run=r/'runs/20261007-companion-priority/pbps-gaussian-marginal-gradient';o=run/'exact-verification51';commit='19f7e6bed7975fac9b7e1ea0b0b95d0c084083f6';decl='AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianMarginalGradient.gaussian_marginal_gradient_closable';H=lambda b:hashlib.sha256(b).hexdigest();LF=lambda b:b.replace(b'\r\n',b'\n').replace(b'\r',b'\n');now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def read(p):return json.loads(Path(p).read_text('utf-8-sig'))
def compact(d):return json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def dump(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n','utf-8')
def bind(p):
 p=Path(p);b=p.read_bytes();return {'path':p.relative_to(r).as_posix(),'raw_sha256':H(b),'lf_sha256':H(LF(b)),'raw_bytes':len(b),'lf_bytes':len(LF(b))}
def verify(p,x):
 d=bind(p);assert d['raw_sha256']==x['raw_sha256'] and d['lf_sha256']==x['lf_sha256'] and d['raw_bytes']==x.get('bytes',x.get('raw_bytes')),('PIN',str(p));return d

def git(*a):return subprocess.check_output(['git',*a],cwd=r)
def diff(a,b,p=''):
 if type(a)!=type(b):return[p]
 if isinstance(a,dict):return sum([diff(a.get(k),b.get(k),p+'/'+k)for k in a.keys()|b.keys()],[])
 if isinstance(a,list):return[p]if len(a)!=len(b)else sum([diff(x,y,p+'/'+str(i))for i,(x,y)in enumerate(zip(a,b))],[])
 return[p]if a!=b else[]
assert git('rev-parse','HEAD').decode().strip()==commit;parent=git('rev-parse',commit+'^').decode().strip();assert read(o/'reviewer.exact.lease.json')['compiler']=='CLOSED'
s=read(run/'source.1.review.json');assert not s['blocking'] and s['verdict']=='equivalent-after-elaboration' and len(s['semantic_slots'])==7 and not s['deltas'] and not s['repairs'] and not s['source_excess'];assert H(compact({k:v for k,v in s.items()if k!='review_run_sha256'}))==s['review_run_sha256']=='6721d6790b3699f41b788d017875d7a0014e0def4888cfb2643276f93562afdf'
whole=run/'whole-proof-review51';wr=read(whole/'run.json');assert H(compact({k:v for k,v in wr.items()if k!='run_sha256'}))==wr['run_sha256']=='dae85e8915b37569ea50de068f78876d968008c3cd8b732b0d72325a3706a216';assert not wr['compiler_used'] and not wr['source_topology_self_admission']
for n,x in wr['outputs_relative_own_folder'].items():verify(whole/n,x)
assert H((whole/'lease.json').read_bytes())==wr['actual_final_closed_lease_expected_raw_sha256'];assert read(whole/'lease.json')['status']=='CLOSED';receipt=read(whole/'receipt.json');assert receipt['status']=='ACCEPT_SCOPED_NO_MATHEMATICAL_BLOCKER'
# Original snapshots are explicit historical metadata successors, never a waiver of mathematical drift.
byhash={}
for p in run.rglob('*'):
 if p.is_file() and o not in p.parents and ('snapshot' in p.name or p.suffix in ['.raw','.lf']):byhash.setdefault(H(p.read_bytes()),[]).append(p)
closure=read(whole/'reachable-local-import-closure.json')['modules'];containers=[('mathfreeze53',read(run/'math-freeze.json')['inputs']),('wholefinal53',read(whole/'freeze-bindings.final.json')),('closure71',list(closure.values())),('source1',s['input_artifacts']),('source1run',read(run/'source.1.review.run.json')['input_artifacts']),('source1lease',read(run/'source.1.review.lease.json')['input_artifacts'])];pins=[];historical=[]
for owner,arr in containers:
 for x in arr:
  p=Path(x['path']);p=p if p.is_absolute()else r/p;actual=p
  if H(p.read_bytes())!=x['raw_sha256']:
   candidates=byhash.get(x['raw_sha256'],[]);assert candidates,('UNRESOLVED',owner,x['path']);actual=candidates[0];rel=p.relative_to(r).as_posix();assert rel.startswith(('research-wiki/semantic-roundtrip/audits/','research-wiki/frontier-cells/')) or 'lease' in rel,('SCIENCE_DRIFT',rel)
   changes=diff(read(actual),read(p));
   if rel.startswith('research-wiki/frontier-cells/'):assert all(z.startswith(('/status','/evidence/'))for z in changes),changes
   if rel.startswith('research-wiki/semantic-roundtrip/audits/'):assert all(z.startswith(('/source_review','/verdict','/semantic_slots','/deltas','/state','/reconstruction/decoder'))for z in changes),changes
   historical.append({'owner':owner,'original_path':rel,'historical_snapshot':bind(actual),'current':bind(p),'JSON_changes':changes,'mapping':'Explicit historical source admission or closed runtime lease administrative successor; no science drift.'})
  pins.append({'owner':owner,'original_path':str(x['path']),'actual_bound':verify(actual,x),'historical':actual!=p})
print('original pins',len(pins),'historical',len(historical),flush=True)
# Full changed current commit set, with Git raw/LF mapping explicitly recorded.
paths=git('diff','--name-only',parent,commit).decode().splitlines();batch=subprocess.check_output(['git','cat-file','--batch'],input=''.join(commit+':'+p+'\n'for p in paths).encode(),cwd=r);pos=0;gitrows=[]
for p in paths:
 end=batch.index(b'\n',pos);size=int(batch[pos:end].split()[-1]);blob=batch[end+1:end+1+size];pos=end+size+2;b=(r/p).read_bytes();assert blob in (b,LF(b)),('GIT_DRIFT',p);gitrows.append({**bind(r/p),'Git_blob_sha256':H(blob),'projection':'raw'if b==blob else 'CRLF/loneCR-to-LF'})
# Original selected exact primitive fragments and local dependencies still match.
apis=read(whole/'source-api-fragment-bindings.json')
for x in apis:
 b=Path(x['path']).read_bytes();assert H(b)==x['whole_raw_sha256'] and H(LF(b))==x['whole_lf_sha256'];f=b[x['start_utf8_byte0']:x['end_utf8_byte0_exclusive']];assert H(f)==x['fragment_raw_sha256'] and H(LF(f))==x['fragment_lf_sha256']
for x in read(whole/'extra-api-bindings.json'):verify(r/x['whole']['path'],x['whole'])
for mod,x in closure.items():
 b=(r/x['path']).read_bytes();blob=git('show',commit+':'+x['path']);assert blob in (b,LF(b)),('CLOSURE_GIT',mod)
# Native decoder51 has an object identity and canonical-sorted logical recipe, not an invented older schema.
dec=run/'anonymous-decoder';dr=read(dec/'run.json');res=read(dec/'result0.json');anon=read(dec/'packet0.json');dp=dr['run_binding_payload'];assert H(compact(dp))==dr['decoder_run_sha256']=='d0d363b3e8142fd831f447c803bea69ac6a4eda01ea813849be3f3b110a0c789';assert res['decoder']==dp['identity'] and isinstance(res['decoder'],dict);assert H(compact({k:v for k,v in res.items()if k!='logical_digest_sha256'}))==res['logical_digest_sha256'];assert res['decoder_run_sha256']==dr['decoder_run_sha256'];assert H(compact({k:v for k,v in anon.items()if k!='packet_sha256'}))==anon['packet_sha256']
for name,x in [('packet0.json',dp['input_packet']),('initial-lease.raw.snapshot.json',dp['preserved_opening_snapshot']),('lease.json',dr['expected_final_closed_lease']),('result0.json',dr['result_artifact'])]:
 verify(dec/name,x);assert H(compact(read(dec/name)))==x['logical_sha256'];assert (dec/name).read_bytes()==(r/'.astis/decoder-51'/name).read_bytes()
assert (dec/'run.json').read_bytes()==(r/'.astis/decoder-51/run.json').read_bytes();assert read(dec/'lease.json')['status']=='CLOSED';assert not dp['exposure']['source_text_visible'] and dp['exposure']['inherited_general_source_identity_metadata_visible'] and not dp['exposure']['strict_no_source_identity_exposure_claimed']
packet=read(run/'source.1.reviewer-packet.json');assert H(compact({k:v for k,v in packet.items()if k!='packet_sha256'}))==packet['packet_sha256']==s['reviewer_packet_sha256'];assert packet['blind_reconstruction']['text']==res['reconstructed_theorem_text'];assert all(not v for v in packet['anti_anchoring'].values());assert s['reviewer']!=packet['roles']['formalizer'] and s['reviewer']!=packet['roles']['blind_decoder']
text=(r/'AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/GaussianMarginalGradient.lean').read_text('utf-8');statement=text.split('theorem gaussian_marginal_gradient_closable',1)[1].split(' := by',1)[0];header='theorem gaussian_marginal_gradient_closable'+statement.rstrip()+'\n';assert H(header.encode())=='d7273526caa94ec518b790626edb6b289bdabfdd1104a196cd2e8eb110211e81' and len(header.encode())==697;assert statement==packet['lean']['statement']==anon['lean']['statement']
item=read(r/'website/content/publications/gaussian-marginal-gradient.json')['items'][0];unit=read(r/'website/content/declaration_lessons/gaussian-marginal-gradient.json')['units'][0];binding=item['bindings'][0];fd=lambda p:H((r/p).read_text('utf-8').encode());payload={'file':fd(packet['lean']['file']),'current_lean_module':text,'toolchain':fd('lean-toolchain'),'dependencies':fd('lake-manifest.json'),'source':item['source'],'statement':item['statement'],'formulae':item['formulae'],'assumptions':item['assumptions'],'obligations':item['obligations'],'lesson':unit,'binding':{k:v for k,v in binding.items()if k not in {'audit_id','legacy_audit_debt'}}};assert H(compact(payload))==s['publication_binding_sha256']==packet['publication_binding_sha256']
ad=run/'decoder-identity-adapter51';op=read(ad/'operations.json');before=read(ad/'audit.before.raw.snapshot.json');after=read(ad/'audit.after.raw.snapshot.json');assert diff(before,after)==['/reconstruction/decoder'];assert before['reconstruction']['decoder']==res['decoder'];assert after['reconstruction']['decoder']==res['decoder']['agent'];assert not (run/'source.0.review.json').exists();assert op['classification']=='IMPLEMENTATION_FAILED_ADMIN_SCHEMA_ONLY';assert len(unit['steps'])==6
for x in op['evidence']:verify(r/x['path'],x)
leases=[]
for p in sorted(run.rglob('*lease*.json')):
 if o in p.parents or 'snapshot' in p.name:continue
 d=read(p)
 for k in ['status','read','write','Python','read_lease','write_lease','Python_lease','compiler','compiler_lease']:
  if k in d:assert d[k]in ['CLOSED','NOT_STARTED_CLOSED'],('LEASE_OPEN',str(p),k,d[k])
 leases.append(bind(p))
for n,key in [('source.1.review.run.json','run_sha256'),('source.1.review.lease.json','lease_run_sha256'),('reviewer.source.1.lease.json','lease_run_sha256')]:
 d=read(run/n);assert H(compact({k:v for k,v in d.items()if k!=key}))==d[key]
assert s['review_completed_utc']<read(run/'source.1.review.lease.json')['closed_utc'];assert s['review_started_utc']>read(run/'source.review.primary-first.lease.json')['closed_utc']
# New science-only whitespace negative: exact individual immutable exceptions, lossless gzip, no full-diff pass claim.
w=read(run/'whitespace-diagnosis51/diagnosis.json');assert w['findings']==256;packed=(r/w['gzip']['path']).read_bytes();raw=gzip.decompress(packed);assert H(packed)==w['gzip']['raw_sha256'] and H(raw)==w['full_negative_raw_sha256'] and int.from_bytes(packed[4:8],'little')==0
parsed=[{'path':m.group(1),'line':int(m.group(2)),'kind':m.group(3).removesuffix('.')}for m in re.finditer(r'^(.+):(\d+): (trailing whitespace\.|new blank line at EOF\.)$',LF(raw).decode(),re.M)];findings=[f for x in w['immutable_raw_artifacts']for f in x['findings']];assert len(parsed)==256 and sorted(parsed,key=str)==sorted(findings,key=str);exclusions=[x['path']for x in w['immutable_raw_artifacts']];assert set(exclusions)==set(x['path']for x in parsed)
for x in w['immutable_raw_artifacts']:
 b=(r/x['path']).read_bytes();assert H(b)==x['raw_sha256'] and H(b.replace(b'\r\n',b'\n'))==x['lf_sha256'];assert x['path'].startswith('runs/20261007-companion-priority/');lines=b.replace(b'\r\n',b'\n').split(b'\n')
 for f in x['findings']:assert lines[f['line']-1].endswith((b' ',b'\t',b'\r'))if f['kind']=='trailing whitespace'else lines[-1].strip()==b''
sys.path[:0]=[str(r),str(r/'tools')];from tools import astis,astis_publication,astis_advance
states=astis_advance.current_advances();aid='ASTIS-SA-20261007-GaussianMarginalGradient';assert states[aid]['state']=='PROVED_LOCAL';stabilizing={k:v.get('owner_id')for k,v in states.items()if v.get('state')=='STABILIZING'};assert len(stabilizing)==1 and 'PhaseKernel'in next(iter(stabilizing));assert git('-C','.lake/packages/mathlib','rev-parse','HEAD').decode().startswith('db584cd6');assert 'v4.33.0'in (r/'lean-toolchain').read_text('utf-8')
commands=[[sys.executable,'tools/astis_publication.py','check','--base','origin/main'],[sys.executable,'tools/astis_semantic_roundtrip.py','check'],[sys.executable,'tools/astis_frontier_cells.py','check'],[sys.executable,'tools/astis_contributor_contract.py','check','--base','origin/main'],['git','-c','core.whitespace=cr-at-eol','diff','--check',parent,commit,'--','.']+[':(exclude)'+p for p in exclusions]];checks=[]
for i,c in enumerate(commands):
 start=now();p=subprocess.run(c,cwd=r,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=o/f'check.{i}.log';log.write_bytes(p.stdout);d={'command':c,'exit_code':p.returncode,'started_utc':start,'finished_utc':now(),'log':bind(log)};dump(o/f'check.{i}.status.json',d);checks.append(d);print('fresh',i,p.returncode,flush=True)
fake=astis.lean_diagnostics();dump(o/'fake-closure.json',fake);assert fake['totals']['forbidden_hits']==0;astis_publication.check_advance([decl],reviewed=True)
compiled=(o/'focused.log').read_text('utf-8');sets=re.findall(r'depends on axioms: \[(.*?)\]',compiled,re.S);assert len(sets)==3 and all(set(re.findall(r'[\w.]+',x))=={'propext','Classical.choice','Quot.sound'}for x in sets)and 'Build completed successfully (3893 jobs).'in compiled
summary={'checked_commit':commit,'parent':parent,'original_pins':pins,'historical_metadata_mappings':historical,'Git_bindings':gitrows,'source_review':bind(run/'source.1.review.json'),'source_review_run_sha256':s['review_run_sha256'],'source_reviewed_publication_gate':'PASS','undispatched_original_negative':bind(ad/'operations.json'),'native_decoder_schema_object':True,'native_decoder_run_sha256':dr['decoder_run_sha256'],'native_decoder_run':bind(dec/'run.json'),'native_decoder_general_identity_metadata_exposure':dp['exposure'],'identity_adapter_exact_one_field':True,'no_source0_verdict_invented':True,'wholeproof_run':bind(whole/'run.json'),'wholeproof_run_sha256':wr['run_sha256'],'wholeproof_reuse':'Entire unchanged normalization/body/2Tests math; strict53freeze/71localimports/62+6primitive wholefiles; no new mathematical review claim.','actual_CLOSED_leases':leases,'fresh_focused':read(o/'focused.status.json'),'compiler_reuse':'Actual foreground focused3893 PASS, cached replay; not a fresh shared aggregate.','standard3':sets,'fresh_checks':checks,'fake_closure_totals':fake['totals'],'sole_STABILIZING':stabilizing,'whitespace':{'full_exit':2,'findings':256,'individual_immutable_paths':len(exclusions),'gzip_lossless_mtime0':True,'authored_exit':checks[4]['exit_code'],'diagnosis':bind(run/'whitespace-diagnosis51/diagnosis.json')},'remaining':'Shared Registry492/imports/rootmandatory/graph/site/reader/main/live/PURIFIED; literalTf/roughH1/Gamma/fullfourpapers/cost/composition OPEN.'};dump(o/'bindings.json',summary);assert all(x['exit_code']==0 for x in checks);print(json.dumps({'pins':len(pins),'hist':len(historical),'Git':len(gitrows),'closure':len(closure),'APIs':len(apis),'fresh':[x['exit_code']for x in checks],'fake':fake['totals']}))
