import json,hashlib,subprocess,re,gzip,datetime,sys,os
from pathlib import Path
r=Path('E:/Samplinglib');run=r/'runs/20261007-companion-priority/pbps-macroscopic-energy';out=run/'exact-commit-review50';commit='864ff305b78030d9e1c840938e82fefcf4185515';parent='88f47590725f6a771d9aa3284c0578e02caea5d2';decl='AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicEnergy.actual_macroscopic_gradient_energy_blocks'
H=lambda b:hashlib.sha256(b).hexdigest()
LF=lambda b:b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def read(p):return json.loads(Path(p).read_text('utf-8'))
def compact(d,ordered=False):return json.dumps(d,ensure_ascii=False,sort_keys=not ordered,separators=(',',':'),allow_nan=False).encode()
def dump(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n','utf-8')
def bind(p):
 p=Path(p);b=p.read_bytes();return {'path':p.relative_to(r).as_posix(),'bytes':len(b),'raw_sha256':H(b),'lf_sha256':H(LF(b))}
def git(*a):return subprocess.check_output(['git',*a],cwd=r)
def diff(a,b,p=''):
 if type(a)!=type(b):return[p]
 if isinstance(a,dict):return sum([diff(a.get(k),b.get(k),p+'/'+k)for k in a.keys()|b.keys()],[])
 if isinstance(a,list):return[p]if len(a)!=len(b)else sum([diff(x,y,p+'/'+str(i))for i,(x,y)in enumerate(zip(a,b))],[])
 return[p]if a!=b else[]
assert git('rev-parse','HEAD').decode().strip()==commit and git('rev-parse',commit+'^').decode().strip()==parent
assert read(out/'reviewer.exact.lease.json')['compiler']=='CLOSED'
source=read(run/'source.1.review.json');assert source['verdict']=='equivalent-after-elaboration' and not source['blocking'] and len(source['semantic_slots'])==7 and not source['deltas'] and not source['repairs'] and not source['source_excess']
assert H(compact({k:v for k,v in source.items()if k!='review_run_sha256'}))==source['review_run_sha256']=='160b2f0320acb0c5e00f4eb7e80780be0e31c3f90725b8809edfa8d82251f307'
assert H((run/'source.1.review.json').read_bytes())=='10fbdd1261d5edfe9ad5525e1f525c541597d208c65b33274ddf7df648e0efea'
whole=run/'whole-proof-review50';wr=read(whole/'run.json');assert H(compact({k:v for k,v in wr.items()if k!='run_sha256'}))==wr['run_sha256']=='745912c96629789da0a704cfa622c19ed8552da623103833a9477e17a4fb73c6'
assert wr['status']=='CLOSED_ACCEPT_SCOPED_NO_MATHEMATICAL_BLOCKER' and not wr['compiler_used'] and not wr['source_topology_self_admission']
for name,x in wr['outputs'].items():
 d=bind(whole/name);assert d['raw_sha256']==x['raw_sha256'] and d['lf_sha256']==x['lf_sha256'] and d['bytes']==x['raw_bytes'],name
assert H((whole/'lease.json').read_bytes())==wr['actual_own_closed_lease_expected_raw_sha256'] and read(whole/'lease.json')['status']=='CLOSED'
receipt=read(whole/'receipt.json');assert receipt['status']=='ACCEPT_SCOPED_NO_MATHEMATICAL_BLOCKER' and not receipt['mathematical_blockers']
# Every source/math original pin is exact current, or an explicit chronological administrative snapshot.
snapshots=[p for p in run.rglob('*')if p.is_file() and out not in p.parents and ('snapshot' in p.name or p.suffix in ['.raw','.lf'] or p.name.endswith('.before.json'))];byhash={}
for p in snapshots:byhash.setdefault(H(p.read_bytes()),[]).append(p)
containers=[('math-freeze',read(run/'math-freeze.json')['inputs']),('source1',source['input_artifacts']),('source1lease',read(run/'source.1.review.lease.json')['input_artifacts']),('source0',read(run/'source.0.review.json')['input_artifacts']),('wholefreeze',wr['freeze_inputs']),('localclosure',read(whole/'reachable-local-import-closure.json')['local_modules'])]
pins=[];hist=[]
for owner,array in containers:
 for x in array:
  p=Path(x['path']);p=p if p.is_absolute()else r/p;actual=p
  if H(p.read_bytes())!=x['raw_sha256']:
   candidates=byhash.get(x['raw_sha256'],[]);assert candidates,('UNRESOLVED',owner,x['path'])
   actual=candidates[0];rel=p.relative_to(r).as_posix();assert rel.startswith(('research-wiki/semantic-roundtrip/audits/','research-wiki/frontier-cells/','website/content/declaration_lessons/')) or 'lease' in rel,('SCIENCE_DRIFT',rel)
   changes=diff(read(actual),read(p)) if p.suffix=='.json' else []
   if rel.startswith('website/content/declaration_lessons/'):assert changes==['/units/0/mathlib_dependencies/5']
   if rel.startswith('research-wiki/frontier-cells/'):assert all(z.startswith(('/status','/evidence/'))for z in changes)
   if rel.startswith('research-wiki/semantic-roundtrip/audits/'):assert all(z.startswith(('/publication_binding_sha256','/publication_context/lesson/mathlib_dependencies/5','/source_review','/verdict','/semantic_slots','/deltas','/state'))for z in changes),changes
   hist.append({'owner':owner,'original_path':rel,'original_snapshot':bind(actual),'current':bind(p),'changed_JSON_paths':changes,'type':'Explicit metadata-only direct API label or later source-admission/lease administrative successor; mathematical/source bytes not waived.'})
  d=bind(actual);assert d['raw_sha256']==x['raw_sha256'] and d['lf_sha256']==x['lf_sha256'] and d['bytes']==x.get('bytes',x.get('raw_bytes'))
  pins.append({'owner':owner,'original_path':str(x['path']),'binding':d,'typed_historical':actual!=p})
print('strict pins',len(pins),'typed historical',len(hist),flush=True)
# Bind all 1239 changed science packets to actual commit blobs/current raw or explicit Git LF conversion.
paths=git('diff','--name-only',parent,commit).decode().splitlines();batch=git('cat-file','--batch') if False else subprocess.check_output(['git','cat-file','--batch'],input=''.join(commit+':'+p+'\n'for p in paths).encode(),cwd=r);pos=0;gitrows=[]
for p in paths:
 end=batch.index(b'\n',pos);size=int(batch[pos:end].split()[-1]);blob=batch[end+1:end+1+size];pos=end+size+2;b=(r/p).read_bytes();assert blob in (b,LF(b)),('GIT_DRIFT',p);gitrows.append({**bind(r/p),'Git_blob_sha256':H(blob),'Git_projection':'raw'if blob==b else 'CRLF/loneCR-to-LF'})
print('Git paths',len(gitrows),flush=True)
# Primitive fragments bind both live file and original byte slice, without re-expanding unchanged proof.
apis=[]
for x in read(whole/'selected-api-bindings.json'):
 p=Path(x['path']);b=p.read_bytes();assert H(b)==x['raw_sha256'] and H(LF(b))==x['lf_sha256'];fragment=b[x['start_utf8_byte0']:x['end_utf8_byte0_exclusive']];assert H(fragment)==x['fragment_raw_sha256'] and H(LF(fragment))==x['fragment_lf_sha256'];apis.append(x)
# Native five-file decoder and ordered recipe; original OPEN snapshot stays a historical input.
dec=run/'anonymous-decoder';dr=read(dec/'run.json');res=read(dec/'result0.json');anon=read(dec/'packet0.json');dp=dr['digest_payload'];assert H(compact(dp,True))==dr['decoder_run_sha256']=='42ed953d61197c87c06ba038bb1d696db462759fd971f417dac580b111e8c146';assert res['decoder']==dp['identity']=='/root/fresh_blind_decoder50'
assert H(compact({k:v for k,v in res.items()if k!='decoder_run_sha256'},True))==dp['result_projection_sha256'];assert H(compact({k:v for k,v in anon.items()if k!='packet_sha256'}))==anon['packet_sha256']
for p in dec.iterdir():
 if p.is_file() and (r/'.astis/decoder-50'/p.name).exists():assert p.read_bytes()==(r/'.astis/decoder-50'/p.name).read_bytes(),p.name
for x in dp['actual_inputs']:
 p=Path(x['path']);b=p.read_bytes()
 if H(b)!=x['raw_sha256']:
  assert p.name=='lease.json';b=dp['initial_lease_snapshot_utf8'].encode()
 assert H(b)==x['raw_sha256'] and H(LF(b))==x['lf_sha256'] and len(b)==x['bytes']
assert read(dec/'lease.json')['status']=='CLOSED' and not dp.get('source_text_visible',False) and not dp.get('compiler_started',False)
packet=read(run/'source.1.reviewer-packet.json');assert H(compact({k:v for k,v in packet.items()if k!='packet_sha256'}))==packet['packet_sha256']==source['reviewer_packet_sha256']
text=(r/'AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicEnergy.lean').read_text('utf-8');statement=text.split('theorem actual_macroscopic_gradient_energy_blocks',1)[1].split(' := by',1)[0];header='theorem actual_macroscopic_gradient_energy_blocks'+statement.rstrip()+'\n';assert len(header.encode())==2907 and H(header.encode())=='478a899effcc46585270420c4db9c42052a5fcfe3adfd8098ea9548d26c61170';assert statement==packet['lean']['statement'];assert res['reconstructed_theorem_text']==packet['blind_reconstruction']['text']
item=read(r/'website/content/publications/pbps-macroscopic-energy.json')['items'][0];unit=read(r/'website/content/declaration_lessons/pbps-macroscopic-energy.json')['units'][0];binding=item['bindings'][0];fd=lambda p:H((r/p).read_text('utf-8').encode())
payload={'file':fd(packet['lean']['file']),'current_lean_module':text,'toolchain':fd('lean-toolchain'),'dependencies':fd('lake-manifest.json'),'source':item['source'],'statement':item['statement'],'formulae':item['formulae'],'assumptions':item['assumptions'],'obligations':item['obligations'],'lesson':unit,'binding':{k:v for k,v in binding.items()if k not in {'audit_id','legacy_audit_debt'}}};assert H(compact(payload))==source['publication_binding_sha256']==packet['publication_binding_sha256']
overlay=run/'publication-metadata-overlay50';op=read(overlay/'operations.json');before=(overlay/'lesson.before.json').read_bytes();after=(r/'website/content/declaration_lessons/pbps-macroscopic-energy.json').read_bytes();assert before.replace(b'MeasureTheory.Measure.IsCondKernel.disintegrate',b'MeasureTheory.Measure.disintegrate')==after
assert (overlay/'publication.before.json').read_bytes()==(r/'website/content/publications/pbps-macroscopic-energy.json').read_bytes();assert (overlay/'source0.review.json').read_bytes()==(run/'source.0.review.json').read_bytes();assert H((run/'source.0.review.json').read_bytes())=='8cbc4247d849f04af454fbdc5ee1cc6f2b3ab6bb490ac98f573160255e5f6828'
leases=[]
for p in sorted(run.rglob('*lease*.json')):
 if out in p.parents or 'opening' in p.name or 'snapshot' in p.name:continue
 d=read(p)
 if 'status'in d:assert d['status']=='CLOSED',(p,d['status'])
 leases.append(bind(p))
for name in ['source.1.review.run.json','source.1.review.lease.json']:
 d=read(run/name);key='lease_run_sha256'if 'lease_run_sha256'in d else 'run_sha256';assert H(compact({k:v for k,v in d.items()if k!=key}))==d[key]
assert source['completed_utc']<read(run/'source.1.review.lease.json')['closed_utc']
direct=receipt['direct_ASTIS_dependencies'];assert unit['astis_dependencies']==direct and len(direct)==4 and len(unit['steps'])==8 and not re.search(r'^private (theorem|def)|\b(sorry|admit|axiom)\b|Prop\s*:=\s*True|:=\s*trivial',text,re.M);assert text.count('norm_snd')==3
# Full whitespace negative replay is bounded new commit only, precise immutable files; no blanket exclusion.
w=read(run/'whitespace-diagnosis50/diagnosis.json');assert w['findings']==672 and len(w['immutable_raw_artifacts'])==87
packed=(r/w['gzip']['path']).read_bytes();raw=gzip.decompress(packed);assert H(packed)==w['gzip']['raw_sha256'] and H(raw)==w['full_negative_raw_sha256'];assert int.from_bytes(packed[4:8],'little')==0 and not packed[3]&8
parsed=[{'path':m.group(1),'line':int(m.group(2)),'kind':m.group(3).removesuffix('.')}for m in re.finditer(r'^(.+):(\d+): (trailing whitespace\.|new blank line at EOF\.)$',LF(raw).decode(),re.M)]
findings=[f for x in w['immutable_raw_artifacts']for f in x['findings']];assert len(parsed)==672 and sorted(parsed,key=str)==sorted(findings,key=str)
exclusions=[x['path']for x in w['immutable_raw_artifacts']];assert set(exclusions)==set(x['path']for x in parsed)
for x in w['immutable_raw_artifacts']:
 p=r/x['path'];b=p.read_bytes();assert H(b)==x['raw_sha256'] and H(b.replace(b'\r\n',b'\n'))==x['lf_sha256'];assert x['path'].startswith('runs/20261007-companion-priority/') and ('50'in x['path'] or '/pbps-macroscopic-energy/'in x['path']);lines=b.replace(b'\r\n',b'\n').split(b'\n')
 for f in x['findings']:
  assert lines[f['line']-1].endswith((b' ',b'\t',b'\r')) if f['kind']=='trailing whitespace' else lines[-1].strip()==b''
sys.path[:0]=[str(r),str(r/'tools')];from tools import astis,astis_publication,astis_advance
states=astis_advance.current_advances();aid='ASTIS-SA-20261007-PBPSMacroscopicEnergy';assert states[aid]['state']=='PROVED_LOCAL';stabilizing={k:v.get('owner_id')for k,v in states.items()if v.get('state')=='STABILIZING'};assert len(stabilizing)==1 and 'PhaseKernel'in next(iter(stabilizing))
commands=[[sys.executable,'tools/astis_publication.py','check','--base','origin/main'],[sys.executable,'tools/astis_semantic_roundtrip.py','check'],[sys.executable,'tools/astis_frontier_cells.py','check'],[sys.executable,'tools/astis_contributor_contract.py','check','--base','origin/main'],['git','-c','core.whitespace=cr-at-eol','diff','--check',parent,commit,'--','.']+[':(exclude)'+p for p in exclusions]];checks=[]
for i,c in enumerate(commands):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.run(c,cwd=r,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=out/f'check.{i}.log';log.write_bytes(p.stdout);s={'command':c,'exit_code':p.returncode,'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'log':bind(log)};dump(out/f'check.{i}.status.json',s);checks.append(s);print('fresh',i,p.returncode,flush=True)
fake=astis.lean_diagnostics();assert fake['totals']['forbidden_hits']==0;astis_publication.check_advance([decl],reviewed=True)
compiled=(out/'focused.log').read_text('utf-8');sets=re.findall(r'depends on axioms: \[(.*?)\]',compiled,re.S);assert len(sets)==3 and all(set(re.findall(r'[\w.]+',x))=={'propext','Classical.choice','Quot.sound'}for x in sets);assert 'Build completed successfully (3891 jobs).'in compiled
summary={'checked_commit':commit,'parent':parent,'all_original_pin_checks':pins,'historical_exact_metadata_mappings':hist,'current_Git_rawLF_bindings':gitrows,'source_review':bind(run/'source.1.review.json'),'source_review_run_sha256':source['review_run_sha256'],'source_original_negative':bind(run/'source.0.review.json'),'source_reviewed_publication_admission':'PASS','source_overlay':'Exact one direct primitive label plus two derived bindings; immutable negative retained.','wholeproof_run':bind(whole/'run.json'),'wholeproof_run_sha256':wr['run_sha256'],'wholeproof_scope':'Mathematical body only; sourcegraph creator exposure disclosed, no self topology admission.','actual_Mathlib_API_fragments':apis,'native_blind':{'original_native_result_dict_and_identity_string_schema':True,'ordered_digest_payload_sha256':dr['decoder_run_sha256'],'run':bind(dec/'run.json'),'original_five_files_equal':True},'statement2907_LF_sha256':H(header.encode()),'direct_ASTIS_dependencies':direct,'local_adapter':'norm_snd actual fixed J and nu, consumed twice; no private theorem or new standalone primitive.','actual_CLOSED_leases':leases,'fresh_compiler':read(out/'focused.status.json'),'compiler_cache':'Actual3891 foregroundPASS with Test replay; no new root aggregate.','compiled_standard3_sets':sets,'fresh_checks':checks,'fake_closure':fake['totals'],'sole_STABILIZING':stabilizing,'whitespace_diagnosis':{'root':bind(run/'whitespace-diagnosis50/diagnosis.json'),'full_exit':2,'findings':672,'exact_immutable_paths':87,'gzip_lossless_mtime0':True,'authored_exit':checks[4]['exit_code'],'no_blanket_exclusion':True},'remaining':'Shared Registry491/imports/rootmandatory/graph/site/reader/main/live/PURIFIED and roughH1/Gamma/full fourpapers/cost/composition OPEN.'}
dump(out/'bindings.json',summary);assert all(x['exit_code']==0 for x in checks);print(json.dumps({'pins':len(pins),'historical':len(hist),'Git':len(gitrows),'APIs':len(apis),'fresh':[x['exit_code']for x in checks],'fake':fake['totals'],'source':'PASS'}))
