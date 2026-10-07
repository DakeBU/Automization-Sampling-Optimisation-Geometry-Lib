import json,hashlib,subprocess,datetime,sys,os,re,gzip,html
from pathlib import Path
r=Path('E:/Samplinglib');run=r/'runs/20261007-companion-priority/pbps-outer-gradient-energy';out=run/'repository-seal49';prior=run/'exact-commit-review49';commit='39d72437b565e21c65364187a810501754a38c4b';science='5ba91a1c9a553b13a38d48f02f0725a69af146a4';decl='AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalGradientEnergy.reflected_conditional_gradient_energy';os.environ['PYTHONUTF8']='1'
def H(b):return hashlib.sha256(b).hexdigest()
def LF(b):return b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def read(p):return json.loads(Path(p).read_text('utf-8'))
def dump(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n','utf-8')
def bind(p):
 p=Path(p);b=p.read_bytes();return {'path':str(p.relative_to(r)).replace('\\','/'),'bytes':len(b),'raw_sha256':H(b),'lf_sha256':H(LF(b))}
def git(*a):return subprocess.check_output(['git',*a],cwd=r)
def diffjson(a,b,p=''):
 if type(a)!=type(b):return[p]
 if isinstance(a,dict):return sum([diffjson(a.get(k),b.get(k),p+'/'+k)for k in a.keys()|b.keys()],[])
 if isinstance(a,list):return[p]if len(a)!=len(b)else sum([diffjson(x,y,p+'/'+str(i))for i,(x,y)in enumerate(zip(a,b))],[])
 return[p]if a!=b else[]
assert read(out/'reviewer.seal.lease.json')['status']=='OPEN';assert git('rev-parse','HEAD').decode().strip()==commit;assert git('rev-parse',commit+'^').decode().strip()==science
verified=read(run/'verified.json');assert verified['verified_commit']==science;assert H((run/'verified.json').read_bytes())=='69172d53a705643aff24f7d910aa01daa92a03ef11e522fe6e46b10c3c4c4266';assert read(prior/'reviewer.exact.lease.json')['status']=='CLOSED'
priorrun=read(prior/'run.json');reused=[]
for x in priorrun['outputs']:
 d=bind(r/x['path']);assert all(d[k]==x[k]for k in ['bytes','raw_sha256','lf_sha256']);reused.append(d)
old=read(prior/'bindings.json');changed=[];oldrows=[];paths=[x['path']for x in old['current_Git_rawLF_bindings']];raw=subprocess.check_output(['git','cat-file','--batch'],input=''.join(commit+':'+p+'\n'for p in paths).encode(),cwd=r);pos=0
for x in old['current_Git_rawLF_bindings']:
 end=raw.index(b'\n',pos);size=int(raw[pos:end].decode().split()[-1]);blob=raw[end+1:end+1+size];pos=end+size+2;p=r/x['path'];b=p.read_bytes();assert blob in (b,LF(b));d=bind(p)
 if H(blob)!=x['Git_blob_raw_sha256']:changed.append(x['path'])
 else:assert all(d[k]==x[k]for k in ['bytes','raw_sha256','lf_sha256'])
 oldrows.append({**d,'Git_blob_raw_sha256':H(blob),'prior_blob_unchanged':H(blob)==x['Git_blob_raw_sha256']})
cell='research-wiki/frontier-cells/ASTIS-SW-PBPS-conditional-gradient-energy.json';assert set(changed)=={cell,'runs/substantive_advances.jsonl'}
pre=read(prior/'precompiler.json')
for x in pre['freeze45']+pre['local_imports65']:
 d=bind(r/x['path']);assert all(d[k]==x[k]for k in ['bytes','raw_sha256','lf_sha256'])
# The only two prior-path successors are verified/shared administration; mathematical/source/pub/test fields remain exact.
before=json.loads(git('show',science+':'+cell));after=read(r/cell);celldelta=diffjson(before,after);assert all(p in ['/status','/blocked/reason']or p.startswith('/evidence/')or p.startswith('/purification/')for p in celldelta);assert after['status']=='independently_verified'and 'serialized_shared_gate'in after['evidence']
notes=read(run/'integration.notes.json');assert notes['proof_commit']==science and notes['registry_count']==490 and notes['root_jobs']==9152 and notes['test_jobs']==9433
rootlease=read(run/'root.integration.lease.json');assert rootlease['status']==rootlease['compiler']==rootlease['Python']==rootlease['read']==rootlease['write']=='CLOSED'and rootlease['exit_code']==0
statusrows=[];gatebindings=[]
for x in notes['checks']:
 d=bind(r/x['path']);assert all(d[k]==x[k]for k in ['bytes','raw_sha256','lf_sha256']);gatebindings.append(d)
 if x['path'].endswith('.status.json'):
  s=read(r/x['path']);assert s['exit_code']==0 and s['proof_commit']==science and rootlease['opened_utc']<=s['started_utc']<s['finished_utc']<=rootlease['closed_utc'];p=r/x['path'].replace('.status.json','.log');assert H(p.read_bytes())==s['log_raw_sha256'];statusrows.append(s)
assert len(statusrows)==12
mandatory=(run/'integration.mandatory.log').read_text('utf-8');tests=(run/'integration.tests.log').read_text('utf-8');assert '9152'in mandatory and '9433'in mandatory and '9433'in tests and 'ASTIS check passed'in mandatory
shared=[]
for x in notes['shared_files']:
 p=r/x['path'];d=bind(p);assert all(d[k]==x[k]for k in ['bytes','raw_sha256','lf_sha256']);assert git('show',commit+':'+x['path'])in(p.read_bytes(),LF(p.read_bytes()));shared.append(d)
for p,imp in [('AutoSamplingTheory/ExampleCases.lean','import AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalGradientEnergy'),('Tests.lean','import Tests.ProximalBPSConditionalGradientEnergy')]:
 text=(r/p).read_text('utf-8');oldtext=git('show',science+':'+p).decode().replace('\r\n','\n');assert text.replace(imp+'\n','',1)==oldtext and text.count(imp+'\n')==1
assert (r/'Tests/Basic.lean').read_text('utf-8').replace('formalizedTechnicalLemmaCount = 490','formalizedTechnicalLemmaCount = 489')==git('show',science+':Tests/Basic.lean').decode().replace('\r\n','\n')
regp='research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl';oldreg=git('show',science+':'+regp).decode().replace('\r\n','\n');newreg=(r/regp).read_text('utf-8');assert newreg.startswith(oldreg);added=[json.loads(x)for x in newreg[len(oldreg):].splitlines()if x.strip()];assert len(added)==1 and added[0]['local_decl']==decl and added[0]['verified_commit']==science and 'rough'in added[0]['next_action'] and 'remain separate'in added[0]['next_action']
# New151 immutable emitted-output findings only; previous429/197 packet unchanged.
w=read(run/'integration-whitespace49/diagnosis.json');assert len(w['findings'])==151 and len(w['immutable_raw_artifacts'])==3
expected=[str((run/p).relative_to(r)).replace('\\','/')for p in ['exact-commit-review49/focused.log','integration.mandatory.log','integration.tests.log']];assert [x['path']for x in w['immutable_raw_artifacts']]==expected;packed=(r/w['gzip']['path']).read_bytes();raw=gzip.decompress(packed);assert H(packed)==w['gzip']['raw_sha256']and H(raw)==w['full_negative_raw_sha256']and len(raw)==w['full_negative_raw_bytes'];assert int.from_bytes(packed[4:8],'little')==0 and not packed[3]&8
parsed=[{'path':m.group(1),'line':int(m.group(2)),'diagnosis':m.group(3)}for m in re.finditer(r'^(.+):(\d+): (trailing whitespace\.|new blank line at EOF\.)$',LF(raw).decode(),re.M)];assert parsed==w['findings'];assert set(expected)==set(x['path']for x in parsed)
for x in w['immutable_raw_artifacts']:
 p=r/x['path'];d=bind(p);assert all(d[k]==x[k]for k in ['bytes','raw_sha256','lf_sha256']);lines=p.read_bytes().splitlines()
 for f in [z for z in w['findings']if z['path']==x['path']]:assert f['diagnosis']=='trailing whitespace.'and lines[f['line']-1].endswith((b' ',b'\t'))
assert w['authored_command']==['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check','--','.']+[':(exclude)'+p for p in expected]
# Science/source admission gates reused exactly; fresh bounded metadata/graph validations no Lean/compiler.
sys.path[:0]=[str(r),str(r/'tools'),str(r/'website/scripts')];from tools import astis,astis_advance,astis_publication
import publication_reader
states=astis_advance.current_advances();assert states['ASTIS-SA-20261007-PBPSConditionalGradientEnergy']['state']=='VERIFIED';assert {k:v.get('owner_id')for k,v in states.items()if v.get('state')=='STABILIZING'}==pre['sole_STABILIZING']
commands=[[sys.executable,'tools/astis_publication.py','check','--base','origin/main'],[sys.executable,'tools/astis_semantic_roundtrip.py','check'],[sys.executable,'tools/astis_frontier_cells.py','check'],[sys.executable,'tools/astis_contributor_contract.py','check','--base','origin/main'],[sys.executable,'tools/astis_publication.py','graph-check','--cell','ASTIS-SW-PBPS-conditional-gradient-energy','--output','_site'],['git','-c','core.whitespace=cr-at-eol','diff','--check',science,commit,'--','.']+[':(exclude)'+p for p in expected]];fresh=[]
for i,c in enumerate(commands):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.run(c,cwd=r,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=out/f'check.{i}.log';log.write_bytes(p.stdout);s={'command':c,'exit_code':p.returncode,'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'log':bind(log)};dump(out/f'check.{i}.status.json',s);fresh.append(s);print('fresh',i,p.returncode,flush=True)
p=subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--check',science,commit],cwd=r,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);full=p.stdout;assert p.returncode==2;fullparsed=[{'path':m.group(1),'line':int(m.group(2)),'diagnosis':m.group(3)}for m in re.finditer(r'^(.+):(\d+): (trailing whitespace\.|new blank line at EOF\.)$',LF(full).decode(),re.M)];assert fullparsed==w['findings'];(out/'fresh.full-whitespace.negative.log.gz').write_bytes(gzip.compress(full,mtime=0))
astis_publication.check_advance([decl],reviewed=True);fake=astis.lean_diagnostics();assert fake['totals']['forbidden_hits']==0
# Official generated graph freshness and actualformal module/import ownership separated from incomplete scanner relations.
graphpath=r/'_site/data/underlying-lean-graph.json';graph=read(graphpath);digest=publication_reader.graph_input_digest();assert graph['publication_inputs_sha256']==digest;node=next(n for n in graph['nodes']if n['id']=='decl:'+decl);assert node['status']=='compiled';module=decl.rsplit('.',1)[0];edges=[e for e in graph['edges']if e.get('source')in['module:'+module,'decl:'+decl]or e.get('target')in['module:'+module,'decl:'+decl]]
for parentmodule in ['ConditionalGradientVariance','GibbsAugmentation','GaussianReflection']:assert any(e['relation']=='imports'and e['source']=='module:AutoSamplingTheory.ExampleCases.ProximalBPS.'+parentmodule and e['target']=='module:'+module for e in edges)
assert any(e['relation']=='imports'and e['source']=='module:'+module and e['target']=='module:Tests.ProximalBPSConditionalGradientEnergy'for e in edges)
# Portable/root capture artifacts currentGit exactbytes. Existing original companion/fullmodule source traceability, scope-only actual pixels.
visual=read(run/'visual.inspection.json');visualpins=[]
for x in visual['artifacts']:
 p=r/x['portable_path'];d=bind(p);assert d['bytes']==x['bytes']and d['raw_sha256']==x['raw_sha256'];assert p.read_bytes()==(r/x['original_path']).read_bytes();assert git('show',commit+':'+x['portable_path'])in(p.read_bytes(),LF(p.read_bytes()));visualpins.append(d)
cdp=read(run/'visual-inspection49/cdp.capture.json');pbps=next(x for x in cdp['records']if x['label']=='pbps');assert pbps['closedLeanDetails']==13 and pbps['mathContainers']==10;assert cdp['ownedBrowserExit']['code']==0 and read(run/'visual-inspection49/proof.capture.json')['ownedBrowserExit']['code']==0
page=r/'_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html';text=page.read_text('utf-8');a=text.index('data-authored-declaration="'+decl+'"');z=text.index('</article>',a);article=html.unescape(text[a:z]);lesson=read(r/'website/content/declaration_lessons/pbps-conditional-gradient-energy.json')['units'][0];assert len(lesson['steps'])==8 and all(x['formula']in article for x in lesson['steps']);assert lesson['formula']in article
codeblocks=[html.unescape(re.sub('<[^>]+>','',x))for x in re.findall(r'<pre[^>]*>\s*<code[^>]*>(.*?)</code>\s*</pre>',text[a:z],re.S)];prod=(r/'AutoSamplingTheory/ExampleCases/ProximalBPS/ConditionalGradientEnergy.lean').read_text('utf-8');publicbody=prod[prod.index('theorem reflected_conditional_gradient_energy'):].strip();assert any(publicbody in c for c in codeblocks)
standalone=[]
for path in ['AutoSamplingTheory/ExampleCases/ProximalBPS/ConditionalGradientEnergy.lean','Tests/ProximalBPSConditionalGradientEnergy.lean']:
 h=r/'_site/modules'/('-'.join(path[:-5].lower().split('/'))+'.html');txt=h.read_text('utf-8');codes=[html.unescape(re.sub('<[^>]+>','',x))for x in re.findall(r'<pre[^>]*>\s*<code[^>]*>(.*?)</code>\s*</pre>',txt,re.S)];assert any((r/path).read_text('utf-8').strip()in c for c in codes);standalone.append(bind(h))
# Historical48CI snapshot only; exact39 remoteCI remains pending, no new remote polling.
cipath=r/'runs/20261007-companion-priority/pbps-conditional-gradient-variance/site-ci-cardinality-repair48/remote.8cacef16.ci.success.json';ci=read(cipath);assert len(ci)==4 and all(x['headSha']=='8cacef16fb16b9a1258c365f5c2024f58392326d'and x['status']=='completed'and x['conclusion']=='success'for x in ci)
result={'checked_commit':commit,'scientific_verified_commit_reused':science,'verified_receipt':bind(run/'verified.json'),'exact5ba_closed_lease':bind(prior/'reviewer.exact.lease.json'),'exact5ba_outputs_reused':reused,'strict_originalGit_paths':oldrows,'only_original_paths_changed_administration':changed,'cell_administrative_JSON_delta':celldelta,'strict_math_freeze45_import65_reuse':bind(prior/'precompiler.json'),'source_native_blind_wholeproof_recipes_reuse':'Exact5ba original source0/decoder/wholeproof receipts unchanged by strict currentGit/raw bindings; no repeated unchanged primary/proof transcript review.','source_1795_statement_reuse':verified['statement_seal'],'root12_actual_status_log_rawLF':gatebindings,'root12_statuses':statusrows,'root_actual_closed_lease':bind(run/'root.integration.lease.json'),'shared_currentGit_rawLF':shared,'registry_true_single_leaf':added[0],'fresh_noncompiler_checks':fresh,'fake_closure':fake['totals'],'source_reviewed_publication_admission':'PASS','current_official_graph':bind(graphpath),'current_publication_input_digest':digest,'actual49_compiled_node':node,'actual49_module_declaration_edges':edges,'graph_truth_boundary':'3 genuine producer module imports/root/Testconsumer/ownership verified; scanner source-reference edges are incomplete lexical hints, including LogConcaveOn.const_mul/prod false substring matches; no exhaustive elaborated proof dependency graph claimed.','visual_artifacts_currentGit':visualpins,'scoped_actual_viewed_images':['cdp.pbps.png','cdp.branch.png','proof.proof.png','proof.proof-late.png'],'visual_observations':'Four actual desktop captures independently viewed: full conditions, sharp coefficient/defect and eight rendered formulas/closed adjacent Lean visible. 901inventory/190selected-viewnodes/517edges/7highlightedrelations are counts only. Dense graph/wrappedsource names, repeated statement, long page/ASCII compressed prose remain presentation debt; no complete ExpositionSeal/fullreader/PURIFIED credit.','static_original_companion':bind(page),'static_complete_source_Test_pages':standalone,'new_whitespace':{'original':bind(run/'integration-whitespace49/diagnosis.json'),'full_exit':2,'findings':151,'exact_immutable_paths':expected,'root_gzip_lossless_mtime0':True,'freshfull_raw_sha256':H(full),'freshfull_lf_sha256':H(LF(full)),'freshfull_lossless_gzip':bind(out/'fresh.full-whitespace.negative.log.gz'),'authored_only_exact3_exclusions_exit':fresh[5]['exit_code'],'original5ba429_197_packet_unchanged':True},'previous48_remoteCI':{'receipt':bind(cipath),'runs':ci,'credit':'PREVIOUS8c_ONLY_NOT39'},'exact39_remoteCI':'PENDING_UNCHECKED_NOT_PUSHED_AT_DISPATCH','compiler_this_seal':'NOT_STARTED_CLOSED','no_newVERIFIED_or_science_shared_site_mutations':True,'remaining':'LiteraljointL2 block norm/Gamma, roughH1 closure/halfturn/main/error/querycost/composition/full4paperGoal/fullreader/ExpositionSeal/main/live/PURIFIED OPEN.'}
dump(out/'bindings.json',result);assert all(x['exit_code']==0 for x in fresh);print(json.dumps({'commit':commit,'oldGitpaths':len(oldrows),'changed':changed,'rootgates':12,'fresh':[x['exit_code']for x in fresh],'fake':fake['totals'],'digest':digest,'whitespace':[2,151,3],'standalone':len(standalone),'visualpins':len(visualpins)}))
