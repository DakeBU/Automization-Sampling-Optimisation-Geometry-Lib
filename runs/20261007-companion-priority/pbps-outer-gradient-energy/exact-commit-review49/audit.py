import json,hashlib,subprocess,re,gzip,datetime,sys,os
from pathlib import Path
r=Path('E:/Samplinglib');run=r/'runs/20261007-companion-priority/pbps-outer-gradient-energy';out=run/'exact-commit-review49';commit='5ba91a1c9a553b13a38d48f02f0725a69af146a4';parent='8cacef16fb16b9a1258c365f5c2024f58392326d';decl='AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalGradientEnergy.reflected_conditional_gradient_energy'
os.environ['PYTHONUTF8']='1'
def H(b):return hashlib.sha256(b).hexdigest()
def LF(b):return b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def read(p):return json.loads(Path(p).read_text('utf-8'))
def compact(d,ordered=False):return json.dumps(d,ensure_ascii=False,sort_keys=not ordered,separators=(',',':'),allow_nan=False).encode()
def bind(p):
 p=Path(p);b=p.read_bytes();return {'path':str(p.relative_to(r)).replace('\\','/'),'bytes':len(b),'raw_sha256':H(b),'lf_sha256':H(LF(b))}
def dump(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n','utf-8')
def git(*a):return subprocess.check_output(['git',*a],cwd=r)
assert git('rev-parse','HEAD').decode().strip()==commit
source=read(run/'source.0.review.json');assert source['verdict']=='equivalent-after-elaboration' and not source['blocking'] and not source['deltas'] and not source['repairs'] and not source['source_excess'];assert len(source['semantic_slots'])==7
assert H(compact({k:v for k,v in source.items()if k!='review_run_sha256'}))==source['review_run_sha256']=='b9b0928c8b20cc7b3c98aee31a21503c8992a3bc2e8677d1faea835b8d0f4801'
# Preserve exact producer schemas and current/immutable historical byte mapping.
containers=[('math-freeze.json',read(run/'math-freeze.json')['inputs']),('source.0.review.json inputs',source['input_artifacts']),('source additional',source['additional_source_api_artifacts']),('source.review.lease.json',read(run/'source.review.lease.json')['input_artifacts']),('wholeproof inputs',read(run/'whole-proof-review49/input-bindings.json'))]
snapshots=[p for p in run.rglob('*')if p.is_file() and 'exact-commit-review49' not in str(p) and ('snapshot' in p.name or p.suffix in ['.raw','.lf'])];byhash={}
for p in snapshots:byhash.setdefault(H(p.read_bytes()),[]).append(p)
pins=[];hist=[]
for owner,array in containers:
 for x in array:
  p=r/x['path'];actual=p
  if not p.exists() or H(p.read_bytes())!=x['raw_sha256']:
   candidates=byhash.get(x['raw_sha256'],[])
   assert candidates,('UNRESOLVED_OR_DRIFT',owner,x['path'],x['raw_sha256'])
   actual=candidates[0];allowed=(x['path'].startswith('research-wiki/semantic-roundtrip/audits/') or x['path'].startswith('research-wiki/frontier-cells/') or 'lease' in x['path'])
   assert allowed,('UNEXPECTED_SCIENTIFIC_DRIFT',x['path'],str(actual))
   hist.append({'owner':owner,'original_path':x['path'],'original_pin':x,'exact_snapshot':bind(actual),'current_rawLF':bind(p) if p.exists() else None,'type':'Historical decoder OPEN-to-CLOSED lease or source admission administrative audit/cell successor; explicit immutable historical bytes retained, no science repair.'})
  d=bind(actual);assert all(d[k]==x[k]for k in ['raw_sha256','lf_sha256']) and d['bytes']==x['bytes'];pins.append({'owner':owner,'original_path':x['path'],'actual_binding':d,'status':'PASS_HISTORICAL_TYPED_SNAPSHOT' if actual!=p else 'PASS_STRICT_CURRENT'})
print('pins',len(pins),'historical',len(hist),flush=True)
# Bind every relevant new science/review/statement/topology artifact to actual commit blob; no historical replay.
paths=git('diff','--name-only',parent,commit).decode().splitlines();assert all(p.startswith('runs/20261007-companion-priority/')or p in ['AutoSamplingTheory/ExampleCases/ProximalBPS/ConditionalGradientEnergy.lean','Tests/ProximalBPSConditionalGradientEnergy.lean','website/content/declaration_lessons/pbps-conditional-gradient-energy.json','website/content/publications/pbps-conditional-gradient-energy.json','research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261007-PBPSConditionalGradientEnergy.json','research-wiki/frontier-cells/ASTIS-SW-PBPS-conditional-gradient-energy.json','runs/substantive_advances.jsonl'] for p in paths)
data=subprocess.check_output(['git','cat-file','--batch'],input=''.join(commit+':'+p+'\n'for p in paths).encode(),cwd=r);pos=0;gitrows=[]
for p in paths:
 end=data.index(b'\n',pos);size=int(data[pos:end].decode().split()[-1]);blob=data[end+1:end+1+size];pos=end+size+2;b=(r/p).read_bytes();assert blob in (b,LF(b)),('CURRENT_GIT_DRIFT',p);gitrows.append({**bind(r/p),'Git_blob_raw_sha256':H(blob)})
# Wholeproof rawrun, own relative output recipe, final closed lease and all live API spans.
whole=run/'whole-proof-review49';wr=read(whole/'run.json');assert wr['status']=='CLOSED_ACCEPT_SCOPED_NO_MATHEMATICAL_BLOCKER' and wr['source_topology_self_admission'] is False and not wr['reviewer_compiler_used']
for name,x in wr['output_files'].items():
 d=bind(whole/name);assert d['raw_sha256']==x['raw_sha256'] and d['lf_sha256']==x['lf_sha256'] and d['bytes']==x['raw_bytes'],name
assert H((whole/'lease.json').read_bytes())==wr['expected_actual_closed_lease_raw_sha256'];assert read(whole/'lease.json')['status']=='CLOSED'
apis=[]
for name in ['mathlib-api-bindings.json','extra-api-bindings.json']:
 for x in read(whole/name):
  p=Path(x['path']);b=p.read_bytes();assert H(b)==x['whole_raw_sha256'] and H(LF(b))==x['whole_lf_sha256']
  fragments=x.get('selected_fragments',[x])
  for f in fragments:
   if 'byte_interval0' in f:a,z=f['byte_interval0'];fragment=b[a:z]
   else:a,z=f['physical_lines1'];fragment=b''.join(b.splitlines(keepends=True)[a-1:z])
   assert H(fragment)==f.get('fragment_raw_sha256',f.get('raw_sha256')) and H(LF(fragment))==f.get('fragment_lf_sha256',f.get('lf_sha256'))
   assert (whole/f['raw_snapshot']).read_bytes()==fragment and (whole/f['lf_snapshot']).read_bytes()==LF(fragment)
   apis.append({'live_whole':bind(p),'span':f.get('physical_lines1'),'snapshot':bind(whole/f['raw_snapshot'])})
# Source reviewer anti-anchored packet, actual publication/wholemodule payload and ordered native decoder recipes.
packet=read(run/'source.0.reviewer-packet.json');assert H(compact({k:v for k,v in packet.items()if k!='packet_sha256'}))==packet['packet_sha256']==source['reviewer_packet_sha256']
prod=r/packet['lean']['file'];text=prod.read_text('utf-8');statement=text.split('theorem reflected_conditional_gradient_energy',1)[1].split(' := by',1)[0];assert statement==packet['lean']['statement'] and H(statement.encode())==packet['lean']['statement_sha256']
assert H(packet['source']['original_text'].encode())==packet['source']['text_sha256']==source['source_text_sha256']
item=read(r/'website/content/publications/pbps-conditional-gradient-energy.json')['items'][0];unit=read(r/'website/content/declaration_lessons/pbps-conditional-gradient-energy.json')['units'][0];binding=item['bindings'][0]
fd=lambda p:H((r/p).read_text('utf-8').encode())
payload={'file':fd(packet['lean']['file']),'current_lean_module':text,'toolchain':fd('lean-toolchain'),'dependencies':fd('lake-manifest.json'),'source':item['source'],'statement':item['statement'],'formulae':item['formulae'],'assumptions':item['assumptions'],'obligations':item['obligations'],'lesson':unit,'binding':{k:v for k,v in binding.items()if k not in {'audit_id','legacy_audit_debt'}}};assert H(compact(payload))==packet['publication_binding_sha256']==source['publication_binding_sha256']
assert source['review_started_utc']<source['review_completed_utc']<read(run/'reviewer.source.lease.json')['closed_utc'];primary=read(run/'source.review.primary-first.lease.json');assert primary['closed_utc']<source['review_started_utc']
for name in ['reviewer.source.lease.json','source.review.lease.json','source.review.primary-first.lease.json']:
 d=read(run/name);assert d['status']=='CLOSED';assert H(compact({k:v for k,v in d.items()if k!='lease_run_sha256'}))==d['lease_run_sha256']
dec=run/'anonymous-decoder';dr=read(dec/'run.json');res=read(dec/'result0.json');anon=read(dec/'packet0.json');assert isinstance(res['decoder'],dict) and not dr['source_text_visible'] and not dr['compiler_started'] and dr['status']=='CLOSED'
assert H(compact(dr['digest_payload'],True))==dr['decoder_run_sha256']==source['decoder_run_sha256']==res['decoder_run_sha256'];assert H(compact({k:v for k,v in res.items()if k!='decoder_run_sha256'},True))==dr['digest_payload']['result_projection_sha256'];assert H(compact({k:v for k,v in anon.items()if k!='packet_sha256'}))==anon['packet_sha256']==source['decoder_packet_sha256'];assert anon['lean']['statement']==statement and len(anon['lean']['approved_definition_context'])==9
assert res['reconstructed_theorem_text']==packet['blind_reconstruction']['text'];assert H(res['reconstructed_theorem_text'].encode())==source['reconstruction_text_sha256'];assert dr['decoder_identity']==res['decoder']['identity'] and dr['decoder_identity']!=source['reviewer']
for name in ['packet0.json','result0.json','run.json','lease.json']:
 assert (dec/name).read_bytes()==(r/'.astis/decoder-49'/name).read_bytes()
for x in dr['input_artifacts']+dr['result_artifacts']+[dr['expected_final_closed_lease']]:
 d=bind(r/x['path']);assert all(d[k]==x[k]for k in ['raw_sha256','lf_sha256','bytes'])
# New private helper/direct ASTIS calls are real, invoked once with internal domains; metadata includes Pvar definition.
direct=['AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalGradientVariance.reflected_conditional_gradient_variance','AutoSamplingTheory.ExampleCases.ProximalBPS.GibbsAugmentation.normalized_augmentation_density','AutoSamplingTheory.ExampleCases.ProximalBPS.GaussianReflection.reflection_preserves_augmentation','AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance']
assert unit['astis_dependencies']==direct and text.count('reflected_second_moment')==2 and len(re.findall(r'^private theorem ',text,re.M))==1 and len(re.findall(r'^theorem ',text,re.M))==1
assert len(unit['steps'])==8 and all('\\\\'not in x for x in [unit['formula']]+[s['formula']for s in unit['steps']]);assert not re.search(r'\b(sorry|admit|axiom)\b|Prop\s*:=\s*True|:=\s*trivial',text)
# Exact429/197 immutable whitespace exception audit, including closed creator scripts EOF-only.
w=read(run/'whitespace-diagnosis49/diagnosis.json');assert len(w['findings'])==429 and len(w['immutable_raw_artifacts'])==197
packed=(r/w['gzip']['path']).read_bytes();raw=gzip.decompress(packed);assert H(packed)==w['gzip']['raw_sha256'] and H(raw)==w['full_negative_raw_sha256'] and len(raw)==w['full_negative_raw_bytes'];assert int.from_bytes(packed[4:8],'little')==0 and not packed[3]&8
parsed=[{'path':m.group(1),'line':int(m.group(2)),'diagnosis':m.group(3)}for m in re.finditer(r'^(.+):(\d+): (trailing whitespace\.|new blank line at EOF\.)$',LF(raw).decode(),re.M)];assert parsed==w['findings']
exclusions=[x['path']for x in w['immutable_raw_artifacts']];assert set(exclusions)==set(x['path']for x in w['findings'])
for x in w['immutable_raw_artifacts']:
 p=r/x['path'];d=bind(p);assert all(d[k]==x[k]for k in ['raw_sha256','lf_sha256','bytes']);assert x['path'].startswith('runs/20261007-companion-priority/') and ('49/'in x['path'] or '/pbps-outer-gradient-energy/'in x['path']);lines=p.read_bytes().splitlines()
 for f in [z for z in w['findings']if z['path']==x['path']]:
  if f['diagnosis']=='trailing whitespace.':assert lines[f['line']-1].endswith((b' ',b'\t'))
  else:assert f['line']==len(lines) and lines[-1].strip()==b''
for name in w['immutable_execution_scripts']:
 findings=[x for x in w['findings']if x['path']==name];assert len(findings)==1 and findings[0]['diagnosis']=='new blank line at EOF.';lease=read((r/name).parent/'lease.json');assert lease['status']=='CLOSED'
assert w['authored_check_command']==['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check','--','.']+[':(exclude)'+p for p in exclusions]
# Fresh gates (compiler already CLOSED). Full bounded commit diff negative retained separately, never called fulldiffPASS.
sys.path[:0]=[str(r),str(r/'tools')];from tools import astis,astis_publication
commands=[[sys.executable,'tools/astis_publication.py','check','--base','origin/main'],[sys.executable,'tools/astis_semantic_roundtrip.py','check'],[sys.executable,'tools/astis_frontier_cells.py','check'],[sys.executable,'tools/astis_contributor_contract.py','check','--base','origin/main'],['git','-c','core.whitespace=cr-at-eol','diff','--check',parent,commit,'--','.']+[':(exclude)'+p for p in exclusions]];checks=[]
for i,c in enumerate(commands):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.run(c,cwd=r,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=out/f'check.{i}.log';log.write_bytes(p.stdout);s={'command':c,'exit_code':p.returncode,'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'log':bind(log)};dump(out/f'check.{i}.status.json',s);checks.append(s);print('fresh',i,p.returncode,flush=True)
c=['git','-c','core.whitespace=cr-at-eol','diff','--check',parent,commit];p=subprocess.run(c,cwd=r,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);full=p.stdout;(out/'fresh.full-whitespace.negative.log.gz').write_bytes(gzip.compress(full,mtime=0));fullparsed=[{'path':m.group(1),'line':int(m.group(2)),'diagnosis':m.group(3)}for m in re.finditer(r'^(.+):(\d+): (trailing whitespace\.|new blank line at EOF\.)$',LF(full).decode(),re.M)];assert p.returncode==2 and fullparsed==w['findings']
fake=astis.lean_diagnostics();assert fake['totals']['forbidden_hits']==0;astis_publication.check_advance([decl],reviewed=True)
compiled=(out/'focused.log').read_text('utf-8');sets=re.findall(r'depends on axioms: \[(.*?)\]',compiled,re.S);assert len(sets)==3 and all(set(re.findall(r'[\w.]+',x))=={'propext','Classical.choice','Quot.sound'}for x in sets);assert 'Build completed successfully (3888 jobs).'in compiled
summary={'checked_commit':commit,'source_review':bind(run/'source.0.review.json'),'source_review_run_sha256':source['review_run_sha256'],'source_verdict':source['verdict'],'all_original_pin_checks':pins,'historical_exact_metadata_mappings':hist,'current_Git_rawLF_bindings':gitrows,'wholeproof_run_raw':bind(whole/'run.json'),'wholeproof_all_outputs_verified':True,'wholeproof_actual_API_fragment_checks':apis,'wholeproof_scope':'Own sourcegraphcreator role disclosed; source topology admission false, no freshblind/publication verdict or compiler by mathreviewer; reused as mathematical body review only.','decoder_native_ordered_recipe':{'original_native_decoder_dict':True,'digest_payload_ordered_hash':dr['decoder_run_sha256'],'actualrun_raw':bind(dec/'run.json'),'seven_strings_verbatim':True,'source_text_visible':False,'ignored_and_portable_bytes_equal':True},'private_helper_audit':{'sole_helper':'reflected_second_moment','direct_call_count':1,'public_premises_added':False,'contracts_discharged_in_public_body':'Actualprobabilities/Markov/disintegration from genuine Gibbs/48; compact smoothf bound supplies L2/Fubini; same jointreflection gives actual outer second-moment marginal.'},'actual_direct_ASTIS_math_calls_and_definition':direct,'statement1795_LF_sha256':read(out/'precompiler.json')['header1795_LF_sha256'],'fresh_compiler':read(out/'focused.status.json'),'compiled_standard3_sets':sets,'fresh_checks':checks,'fake_closure':fake['totals'],'source_reviewed_publication_admission':'PASS','whitespace_diagnosis':{'root':bind(run/'whitespace-diagnosis49/diagnosis.json'),'finding_count':429,'immutable_paths':197,'closed_creator_scripts_EOF_only':w['immutable_execution_scripts'],'full_commit_diff_exit':2,'freshfull_raw_sha256':H(full),'freshfull_LF_sha256':H(LF(full)),'freshfull_lossless_gzip':bind(out/'fresh.full-whitespace.negative.log.gz'),'authored_exact_exclusions_exit':checks[4]['exit_code'],'no_Lean_Test_source_or_publication_excluded':True},'remaining':'49 sharedRegistry490/imports/rootmandatory/graph/site/staticactualdesktopreader, literalB13 roughouterH1/operators/C3/halfturn/fullsamplers/main/cost/composition/fourpapers/PURIFIED OPEN.'}
dump(out/'bindings.json',summary);assert all(x['exit_code']==0 for x in checks);print(json.dumps({'commit':commit,'pins':len(pins),'hist':len(hist),'Git':len(gitrows),'APIspans':len(apis),'fresh':[x['exit_code']for x in checks],'fake':fake['totals'],'source':'PASS','fullwhitespace':2,'authored':checks[4]['exit_code']}))
