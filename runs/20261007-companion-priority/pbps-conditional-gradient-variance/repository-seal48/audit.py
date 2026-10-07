import os,sys,json,hashlib,subprocess,re,datetime,html,ast
from pathlib import Path
r=Path('E:/Samplinglib');os.chdir(r);os.environ['PYTHONUTF8']='1'
prefix='runs/20261007-companion-priority/pbps-conditional-gradient-variance';run=r/prefix;out=run/'repository-seal48';expo=run/'exposition-seal48'
commit='79efd28ca8827742e690529f8c763a7bce9b054a';prior='8d950c37e41bd5d816c4132c6a5cdde0e30dcbee'
def H(b):return hashlib.sha256(b).hexdigest()
def LF(b):return b.replace(b'\r\n',b'\n')
def bind(p):
 p=Path(p);b=p.read_bytes();return {'path':str(p.relative_to(r)).replace('\\','/'),'bytes':len(b),'raw_sha256':H(b),'lf_sha256':H(LF(b))}
def read(p):return json.loads(Path(p).read_text('utf-8'))
def dump(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n','utf-8')
def git(*args):return subprocess.check_output(['git',*args],cwd=r)
def logical(d,key):return H(json.dumps({k:v for k,v in d.items() if k!=key},ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode())
assert git('rev-parse','HEAD').decode().strip()==commit
assert git('rev-parse',commit+'^').decode().strip()==prior
for folder in [out,expo]:assert read(folder/'reviewer.seal.lease.json')['status']=='OPEN'
old=read(run/'reviewer.exact1.bindings.json');verified=read(run/'verified.json');assert verified['verified_commit']==prior
paths=[x['path'] for x in old['Git_rawLF_checks']]
# Bounded exact blobs; not whole-history diff/diagnostic replay.
blobs=subprocess.check_output(['git','cat-file','--batch'],input=''.join(commit+':'+p+'\n' for p in paths).encode(),cwd=r)
pos=0;rows=[];changed=[]
for pin in old['Git_rawLF_checks']:
 end=blobs.index(b'\n',pos);header=blobs[pos:end].decode();size=int(header.split()[-1]);b=blobs[end+1:end+1+size];pos=end+size+2
 p=r/pin['path'];cur=p.read_bytes();assert b in (cur,LF(cur)),('Git/current',pin['path'])
 same=H(b)==pin['Git_blob_raw_sha256'];rawsame=H(cur)==pin['working_raw_sha256'];
 if not same:changed.append(pin['path'])
 else:assert rawsame,('raw drift',pin['path'])
 rows.append({**bind(p),'Git_blob_sha256':H(b),'prior_blob_unchanged':same,'prior_working_raw_unchanged':rawsame})
expected=['website/content/samplewiki_companion_frontiers.json','website/scripts/samplewiki_companions.py','research-wiki/frontier-cells/ASTIS-SW-PBPS-conditional-gradient-variance.json']
assert set(changed)==set(expected)
pre=read(run/'reviewer.exact.precompiler.json');freeze=read(run/'math-freeze.json')
assert len(freeze['inputs'])==36
for x in freeze['inputs']:
 d=bind(r/x['path']);assert d['raw_sha256']==x['raw_sha256'] and d['lf_sha256']==x['lf_sha256'],x['path']
# Freeze/import/API proof reuse is protected by original exact Git receipts and strict current raw values.
print('precompiler keys',list(pre),flush=True)
notes=read(run/'integration.notes.json');gaterows=[];statuses=[]
for x in notes['checks']:
 p=r/x['path'];d=bind(p);assert all(d[k]==x[k] for k in ['bytes','raw_sha256','lf_sha256']);gaterows.append(d)
 if p.name.endswith('.status.json'):
  s=read(p);assert s['exit_code']==0 and s['proof_commit']==prior
  log=p.with_name(p.name.replace('.status.json','.log'));assert H(log.read_bytes())==s['log_raw_sha256'];assert s['started_utc']<s['finished_utc'];statuses.append(s)
assert len(statuses)==12
lease=read(run/'root.integration.lease.json');assert lease['status']=='CLOSED' and lease['compiler']=='CLOSED';assert all(s['finished_utc']<=lease['closed_utc'] for s in statuses)
mandatory=(run/'integration.mandatory.log').read_text('utf-8');tests=(run/'integration.tests.log').read_text('utf-8');assert '9151' in mandatory and '9431' in mandatory and '9431' in tests and 'ASTIS check passed' in mandatory
shared=[]
for item in notes['shared_files']:
 p=item['path'] if isinstance(item,dict) else item
 cur=(r/p).read_bytes();blob=git('show',commit+':'+p);assert blob in (cur,LF(cur));shared.append(bind(r/p))
prod='AutoSamplingTheory/ExampleCases/ProximalBPS/ConditionalGradientVariance.lean';test='Tests/ProximalBPSConditionalGradientVariance.lean';decl='AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalGradientVariance.reflected_conditional_gradient_variance'
for path in ['AutoSamplingTheory/ExampleCases.lean','Tests.lean']:
 txt=(r/path).read_text('utf-8');assert ('ConditionalGradientVariance' in txt),path
assert 'formalizedTechnicalLemmaCount = 489' in (r/'Tests/Basic.lean').read_text('utf-8')
registry=(r/'research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl').read_text('utf-8');assert decl in registry
# Exact planned-source representation overlay: two constants only, original negative immutable.
plan=run/'four-paper-source-plan-review48';before=(plan/'phase-space-overlay48/candidate.before.raw.snapshot.py').read_bytes();after=(plan/'phase-space-overlay48/candidate.after.raw.snapshot.py').read_bytes();repair=read(plan/'phase-space-overlay48/repair.json');assert H(before)==repair['before_raw_sha256'] and H(after)==repair['after_raw_sha256']
checks=read(plan/'comparison.overlay.checks.json');assert checks['raw_exact_two_string_replacements'] and checks['before_equals_immutable_original_candidate'] and checks['primary_contract_and_original_negative_bytes_unchanged'] and not checks['script_executed'];assert len(checks['two_AST_constant_values_only'])==2
oldast=ast.parse(before.decode('utf-8'));newast=ast.parse(after.decode('utf-8'));delta=[]
def cmp(a,b,path='root'):
 if isinstance(a,ast.AST) and isinstance(b,ast.AST):
  assert type(a)==type(b)
  for f in a._fields:cmp(getattr(a,f),getattr(b,f),path+'.'+f)
 elif isinstance(a,list) and isinstance(b,list):
  assert len(a)==len(b)
  for i,(aa,bb) in enumerate(zip(a,b)):cmp(aa,bb,path+'['+str(i)+']')
 elif a!=b:delta.append({'path':path,'before':a,'after':b})
cmp(oldast,newast);assert delta==checks['two_AST_constant_values_only']
planreceipts=[]
for name in ['comparison.review.json','comparison.overlay.review.json']:
 d=read(plan/name);assert logical(d,'review_run_sha256')==d['review_run_sha256'];planreceipts.append(bind(plan/name))
assert read(plan/'comparison.review.json')['blocking'] and not read(plan/'comparison.overlay.review.json')['blocking']
for name in ['reviewer.primary.lease.json','reviewer.comparison.lease.json','reviewer.comparison.overlay.lease.json']:
 d=read(plan/name);assert d['status']=='CLOSED';assert logical(d,'lease_run_sha256')==d['lease_run_sha256'];planreceipts.append(bind(plan/name))
# Fresh noncompiler validators preserve their raw logs/status even when a check fails.
sys.path.insert(0,str(r));sys.path.insert(0,str(r/'tools'));sys.path.insert(0,str(r/'website/scripts'));from tools import astis,astis_publication
import publication_reader
commands=[[sys.executable,'tools/astis_publication.py','check','--base','origin/main'],[sys.executable,'tools/astis_semantic_roundtrip.py','check'],[sys.executable,'tools/astis_frontier_cells.py','check'],[sys.executable,'tools/astis_contributor_contract.py','check','--base','origin/main'],[sys.executable,'tools/astis_publication.py','graph-check','--cell','ASTIS-SW-PBPS-conditional-gradient-variance','--output','_site'],['git','-c','core.whitespace=cr-at-eol','diff','--check',prior,commit,'--',prod,test,'research-wiki/frontier-cells/ASTIS-SW-PBPS-conditional-gradient-variance.json']]
fresh=[]
for i,c in enumerate(commands):
 t=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.run(c,cwd=r,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=out/f'check.{i}.log';log.write_bytes(p.stdout);s={'command':c,'exit_code':p.returncode,'started_utc':t,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'log':bind(log)};dump(out/f'check.{i}.status.json',s);fresh.append(s);print('fresh',i,p.returncode,flush=True)
fake=astis.lean_diagnostics();assert fake['totals']['forbidden_hits']==0
astis_publication.check_advance([decl],reviewed=True)
graph=read(r/'_site/data/underlying-lean-graph.json');digest=publication_reader.graph_input_digest();assert graph['publication_inputs_sha256']==digest
nodes=graph['nodes'];edges=graph['edges'];target=[n for n in nodes if n.get('id')=='decl:'+decl];assert len(target)==1
module=prod[:-5].replace('/','.');targetedges=[e for e in edges if e.get('source') in ['decl:'+decl,'module:'+module] or e.get('target') in ['decl:'+decl,'module:'+module]]
print('target node',target,'edges',targetedges,flush=True)
# Preserve observed remote CI negative as distinct integration-fixture boundary, without inventing current Lean CI state.
ci=r/'.astis/pbps-gradient48/ci79-site.failed.log';cibind=bind(ci);citxt=ci.read_text('utf-8');assert 'FAILED' in citxt and ('3' in citxt and '4' in citxt)
# Immutable actual screenshots and DOM metrics; no browser started by this reviewer.
visual=read(run/'visual.inspection.json');artifacts=[]
for x in visual['artifacts']:
 p=r/x['portable_path'];d=bind(p);assert d['bytes']==x['bytes'] and d['raw_sha256']==x['raw_sha256'];original=r/x['original_path'];assert p.read_bytes()==original.read_bytes();assert git('show',commit+':'+x['portable_path']) in (p.read_bytes(),LF(p.read_bytes()));artifacts.append(d)
# Original companion contains exact publication statement/body; standalone module pages contain complete source imports/tests.
page=r/'_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html';txt=page.read_text('utf-8');start=txt.index('data-authored-declaration="'+decl+'"');end=txt.index('</article>',start);article=txt[start:end]
codeblocks=[html.unescape(re.sub('<[^>]+>','',x)) for x in re.findall(r'<pre[^>]*>\s*<code[^>]*>(.*?)</code>\s*</pre>',article,re.S)]
science=(r/prod).read_text('utf-8');theorem=science[science.index('theorem reflected_conditional_gradient_variance'):].strip();assert any(theorem in c for c in codeblocks),[len(c) for c in codeblocks]
lesson=read(r/'website/content/declaration_lessons/pbps-conditional-gradient-variance.json')['units'][0];print('lesson unitkeys',list(lesson),flush=True)
standalone=[]
for path in [prod,test]:
 htmlpath=r/'_site/modules'/('-'.join(path[:-5].lower().split('/'))+'.html');mtxt=htmlpath.read_text('utf-8');codes=[html.unescape(re.sub('<[^>]+>','',x)) for x in re.findall(r'<pre[^>]*>\s*<code[^>]*>(.*?)</code>\s*</pre>',mtxt,re.S)];src=(r/path).read_text('utf-8').strip();assert any(src in c for c in codes),(path,[len(c) for c in codes]);standalone.append(bind(htmlpath))
assert 'gaussian_precision_step' in (r/test).read_text('utf-8') and 'rank_zero_actual_kernel' in (r/test).read_text('utf-8')
cdp=read(run/'visual-inspection48/cdp.capture.json');print('CDP keys',list(cdp),flush=True)
result={'checked_commit':commit,'prior_VERIFIED_commit':prior,'Git_rawLF_checks':rows,'exact_science_paths_unchanged':len(rows)-len(changed),'typed_metadata_changed_paths':changed,'strict_math_freeze_count':36,'original63_local_imports_and8_Mathlib_spans_reused':bind(run/'reviewer.exact.precompiler.json'),'verified_receipt':bind(run/'verified.json'),'original_exact1_closed_lease':bind(run/'reviewer.exact1.lease.json'),'original53_focused_gate':bind(run/'reviewer.exact.focused.status.json'),'root12_gate_bindings':gaterows,'root12_statuses':statuses,'root_integration_closed_lease':bind(run/'root.integration.lease.json'),'shared_currentGit_rawLF':shared,'planned_overlay_AST_delta':delta,'planned_source_review_bindings':planreceipts,'fresh_checks':fresh,'fresh_fake_closure':fake['totals'],'reviewed_source_admission':'PASS_REUSED_ORIGINAL_SOURCE1','graph_publication_input_digest':digest,'actual48_graph_node':target,'actual48_graph_edges':targetedges,'current_CI_negative':{'site_run':37657924769,'receipt':cibind,'boundary':'two stale website unittest cardinality expectations 3 versus authorized4 sources; local12 gates remain actualPASS; overall79CI not PASS; Lean run37657924748 was pending per root, no success credit'},'visual_artifacts':artifacts,'original_companion_page':bind(page),'standalone_complete_source_Test_pages':standalone,'compiler_this_stage':'NOT_STARTED_CLOSED','new_VERIFIED_transition':False}
dump(out/'bindings.json',result)
assert all(s['exit_code']==0 for s in fresh)
print(json.dumps({'checked_commit':commit,'science_unchanged':len(rows)-3,'rootgates':len(statuses),'fresh':[s['exit_code'] for s in fresh],'fake':fake['totals'],'graphdigest':digest,'artifacts':len(artifacts)}),flush=True)
