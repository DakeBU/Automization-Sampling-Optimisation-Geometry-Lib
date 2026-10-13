from pathlib import Path
import json, hashlib, subprocess, sys, re, datetime, html
from html.parser import HTMLParser

r=Path('E:/Samplinglib'); prefix='runs/20261007-companion-priority/standardized-rgo-kl-dimension'; run=r/prefix
out=run/'repository-seal45'; expo=run/'exposition-seal45'
target='114d5412a0127d31809a9d55431cf89cdc378bc7'; integration='9244497eaa528168ca570941f29274b9b37ee1a8'; proof='76373366787499ebbc9e778fe568d0332233aef0'
sha=lambda b:hashlib.sha256(b).hexdigest(); lf=lambda b:b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
load=lambda p:json.loads((r/p).read_text(encoding='utf-8-sig'))
blobcache={}
def git(*a):
 if len(a)==2 and a[0]=='show' and a[1] in blobcache:return blobcache[a[1]]
 return subprocess.check_output(['git',*a],cwd=r)
def write(p,j):p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def binding(p):
 b=(r/p).read_bytes();return {'path':p,'bytes':len(b),'raw_sha256':sha(b),'lf_sha256':sha(lf(b))}
def tree(c):
 return {x.split('\t',1)[1]:x.split()[2] for x in git('ls-tree','-r',c).decode().splitlines()}
assert git('rev-parse','HEAD').decode().strip()==target
assert git('rev-parse','origin/main').decode().strip()=='c05de12e6a8ca7af8ce2df8608836f8d4e90f617'
for p in [out,expo]:assert json.loads((p/'reviewer.seal.lease.json').read_text())['status']=='OPEN'
tp,ti,tt=tree(proof),tree(integration),tree(target)
science_paths=[p for p in tt if p.endswith('.lean') or p in ['lean-toolchain','lake-manifest.json','lakefile.lean']]
batch=subprocess.run(['git','cat-file','--batch'],cwd=r,input=('\n'.join(tt[p] for p in science_paths)+'\n').encode(),stdout=subprocess.PIPE,check=True).stdout
pos=0
for p in science_paths:
 end=batch.index(b'\n',pos);header=batch[pos:end].split();size=int(header[2]);pos=end+1;blobcache[target+':'+p]=batch[pos:pos+size];pos+=size+1
follow=git('diff-tree','--no-commit-id','--name-only','-r',integration,target).decode().splitlines()
assert sorted(follow)==sorted([prefix+'/discovery46-publication-reconciliation.json','runs/substantive_discoveries.jsonl'])
assert subprocess.run(['git','merge-base','--is-ancestor',proof,target],cwd=r).returncode==0

# Bind exact mathematical and independent review caches; inspect receipts, not transcripts.
old=load(prefix+'/reviewer.exact.bindings.json'); ver=load(prefix+'/verified.json'); rec=load(prefix+'/reviewer.exact.admission-reconciliation.json')
assert sha((run/'verified.json').read_bytes())=='18b81ef73a94230e07851d5caa28e35d5bfb56d44c9d9b15e9fad4e7e513c733'
assert sha((run/'reviewer.exact.bindings.json').read_bytes())=='aeea9c2aa42172e73c59904c264236cd87b309d5a5b0e612217c14bfb9c568f3'
changes=[]; unchanged=[]
for x in old['Git_blobs']:
 p=x['path']
 if x['status']!='PASS':continue
 if tp[p]!=tt[p]:changes.append(p)
 else:unchanged.append(p)
allowed={'AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','research-wiki/cited-results/SLT_reuse_audit.md','research-wiki/frontier-cells/ASTIS-SW-SPHMC-standardized-rgo-kl-dimension.json','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl','runs/substantive_advances.jsonl','runs/substantive_discoveries.jsonl','website/content/samplewiki_companion_frontiers.json'}
assert set(changes)<=allowed,(changes,set(changes)-allowed)
pinchecks=[]
for x in old['pins']:
 p=x['actual_path']
 if p in changes:continue
 b=(r/p).read_bytes()
 assert all(sha(lf(b) if 'lf' in k.lower() else b)==v for k,v in x['hashes'].items()),(x['owner'],p)
 if x.get('bytes') is not None:assert len(b)==x['bytes']
 pinchecks.append({'owner':x['owner'],'slot':x['slot'],'path':p,'status':'PASS_ORIGINAL_RAW_LF'})
science=[]
for p in tt:
 if p.endswith('.lean') or p in ['lean-toolchain','lake-manifest.json','lakefile.lean']:
  b=(r/p).read_bytes();bc=git('show',target+':'+p);assert lf(b)==lf(bc),p
  if tp.get(p)!=tt[p]:assert p in allowed,p
  science.append({'path':p,'proof_blob_unchanged':tp.get(p)==tt[p],**binding(p),'git_lf_sha256':sha(lf(bc))})
for x in old['Mathlib_pins']:
 p=x['path'];b=(r/p).read_bytes();assert sha(b)==x['working_raw_sha256'];assert x['lf_identical']
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=r/'.lake/packages/mathlib').decode().strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
leases=[]
for x in rec['leases']:
 p=x['path'];assert binding(p)==x['binding'];assert load(p)['status']=='CLOSED';leases.append(binding(p))
for p in [prefix+'/reviewer.exact.lease.json',prefix+'/root.integration.lease.json']:
 j=load(p);assert j['status']=='CLOSED';leases.append(binding(p))
notes=load(prefix+'/integration.notes.json');rootlease=load(prefix+'/root.integration.lease.json')
checks=[]
for x in notes['checks']:
 assert binding(x['path'])==x,x['path']
 assert ti[x['path']]==tt[x['path']]
 b=git('show',target+':'+x['path']);assert sha(lf(b))==x['lf_sha256']
 if x['path'].endswith('.status.json'):
  j=load(x['path']);assert j['exit_code']==0 and j['proof_commit']==proof
  assert rootlease['opened_utc']<=j['started_utc']<j['finished_utc']<=rootlease['closed_utc']
 checks.append(x)
assert len(checks)==18
mandatory=(run/'integration.mandatory.log').read_text();assert '9150 jobs' in mandatory and '9429 jobs' in mandatory and 'ASTIS check passed' in mandatory
for x in notes['shared_files']:
 p=x['path']
 if p=='runs/substantive_discoveries.jsonl':
  assert sha(git('show',integration+':'+p))==x['lf_sha256'] or sha(lf(git('show',integration+':'+p)))==x['lf_sha256']
 else:
  a=binding(p);assert a['raw_sha256']==x['raw_sha256'] and a['lf_sha256']==x['lf_sha256'],p
  assert ti[p]==tt[p]
reg=(r/'AutoSamplingTheory/TechnicalLemmas/Registry.lean').read_text()
assert 'def formalizedTechnicalLemmaCount' in reg
assert re.search(r'formalizedTechnicalLemmaCount\s*=\s*488\s*:=\s*by native_decide',(r/'Tests/Basic.lean').read_text())
module='AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGOKLDimension'; decl=module+'.standardized_rgo_unique_prox_and_kl_le_dimension'
assert 'import '+module in (r/'AutoSamplingTheory/ExampleCases.lean').read_text()
assert 'import Tests.StandardizedRGOKLDimension' in (r/'Tests.lean').read_text()
cell=load('research-wiki/frontier-cells/ASTIS-SW-SPHMC-standardized-rgo-kl-dimension.json');assert cell['status']=='independently_verified'
# Actual current administrative graph projection differs from source-admission snapshots only in recorded fields.
sourceaudit=load('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261007-StandardizedRGOKLDimension.json')
assert not sourceaudit.get('deltas')
correction=load(prefix+'/discovery46-publication-reconciliation.json');assert correction['science_change'] is False
before=git('show',integration+':runs/substantive_discoveries.jsonl');after=git('show',target+':runs/substantive_discoveries.jsonl')
assert after.startswith(before);newlines=after[len(before):].strip().splitlines();assert len(newlines)==1
discovery=json.loads(newlines[0]);assert correction['discovery'] in json.dumps(discovery)
assert 'RAW' in json.dumps(discovery)
packet46=r/'runs/20261007-companion-priority/gaussian-talagrand-next-leaf-preread46';run46=json.loads((packet46/'run.json').read_text())
assert sha((packet46/'run.json').read_bytes())==correction['original46_run_sha256']==discovery['metadata']['run_sha256']
outputs46=[]
for x in run46['output_bindings']:
 b=(packet46/x['path']).read_bytes();assert len(b)==x['raw_bytes'] and sha(b)==x['raw_sha256'] and sha(lf(b))==x['lf_sha256'],x['path'];outputs46.append(x)
lease46=(packet46/'lease.json').read_bytes();assert sha(lease46)==run46['actual_final_lease_sha256'] and sha(lf(lease46))==run46['actual_final_lease_lf_sha256'];assert json.loads(lease46)['state']=='CLOSED'
inputs46=[]
for x in json.loads((packet46/'input-bindings.json').read_text())['inputs']:
 b=(r/x['path']).read_bytes();rows=b.splitlines(keepends=True);ranges=x.get('selected_physical_ranges');selected=b if ranges is None else b''.join(b''.join(rows[a-1:z]) for a,z in ranges)
 if 'end_column_exclusive' in x:
  a,z=ranges[0];selected=b''.join(rows[a-1:z-1])+rows[z-1][:x['end_column_exclusive']-1]
 assert sha(selected)==x['raw_sha256'] and sha(lf(selected))==x['lf_sha256'],x['id']
 if 'whole_file_raw_sha256' in x:assert sha(b)==x['whole_file_raw_sha256']
 assert (packet46/(x['id']+'.raw.snapshot.txt')).read_bytes()==selected and (packet46/(x['id']+'.lf.snapshot.txt')).read_bytes()==lf(selected)
 inputs46.append(x['id'])
write(out/'reviewer.seal.RAW46-bindings.json',{'scope':'byte/chronology-only; no mathematical or compiler validation of46','original_run':binding((packet46/'run.json').relative_to(r).as_posix()),'actual_closed_lease':binding((packet46/'lease.json').relative_to(r).as_posix()),'original_input_bindings_checked':inputs46,'original_output_bindings_checked':outputs46,'producer_LF_recipe':'CRLF->LF followed by loneCR->LF','original46_preserved':True,'publication_only_in_commit':target,'prospective924_phrase_corrected_by':binding(prefix+'/discovery46-publication-reconciliation.json')})

# Own bounded metadata checks only; no compiler, site regeneration or historical whitespace replay.
commands=[['tools/astis_publication.py','check','--base','origin/main'],['tools/astis_semantic_roundtrip.py','check'],['tools/astis_frontier_cells.py','check'],['tools/astis_contributor_contract.py','check','--base','origin/main'],['tools/astis_publication.py','graph-check','--cell','ASTIS-SW-SPHMC-standardized-rgo-kl-dimension','--output','_site']]
fresh=[]
if (out/'reviewer.seal.metadata-checks.json').exists():
 fresh=json.loads((out/'reviewer.seal.metadata-checks.json').read_text())
 for x in fresh:
  a=binding(x['path']);assert a['raw_sha256']==x['raw_sha256'] and a['lf_sha256']==x['lf_sha256']
else:
 for i,c in enumerate(commands):
  start=datetime.datetime.now(datetime.timezone.utc).isoformat();res=subprocess.run([sys.executable,*c],cwd=r,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  f=out/f'reviewer.seal.check.{i}.log';f.write_bytes(res.stdout);fresh.append({'command':c,'exit_code':res.returncode,'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),**binding(f.relative_to(r).as_posix())})
 write(out/'reviewer.seal.metadata-checks.json',fresh)
assert [j['exit_code'] for j in fresh]==[0,0,0,0,1]
diagnosis=json.loads((out/'reviewer.seal.graph-freshness-diagnosis.json').read_text());assert diagnosis['matching_exact_old_current_field_projections']==[['/evidence/serialized_shared_gate']]
proofcell=json.loads(git('show',proof+':research-wiki/frontier-cells/ASTIS-SW-SPHMC-standardized-rgo-kl-dimension.json'))
assert all(cell[k]==proofcell[k] for k in ['source_anchor','target_statement','parents','reader_contract','statement_seal','source_proof_coverage','source_detail_audit','proof_digestion','conceptual_mirror_audit'])
sys.path.insert(0,str(r));sys.path.insert(0,str(r/'tools'));from tools import astis,astis_advance
fake=astis.lean_diagnostics();assert fake['totals']['forbidden_hits']==0
state=astis_advance.current_advances();stabilizing=[j for j in state.values() if j.get('state')=='STABILIZING'];assert len(stabilizing)==1 and stabilizing[0]['advance_id']=='ASTIS-SA-20261005-SPHMCImplementedPhaseKernel'
assert state['ASTIS-SA-20261007-StandardizedRGOKLDimension']['state']=='VERIFIED'

graph=load('_site/data/underlying-lean-graph.json');nodes={j['id']:j for j in graph['nodes']};edges=graph['edges'];branch=[e for e in edges if module in json.dumps(e) or 'Tests.StandardizedRGOKLDimension' in json.dumps(e)]
parents=['AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGOKLFisher','AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGOPositionFisher']
for parent in parents:assert {'source':'module:'+parent,'target':'module:'+module,'relation':'imports'} in edges
assert {'source':'module:'+module,'target':'decl:'+decl,'relation':'declares'} in edges
assert {'source':'module:'+module,'target':'module:Tests.StandardizedRGOKLDimension','relation':'imports'} in edges
assert {'source':'module:Tests.StandardizedRGOKLDimension','target':'module:Tests','relation':'imports'} in edges
assert graph['reference_contract']=='Name-scanned references are incomplete signals, not elaborated proof dependencies.'
write(out/'reviewer.seal.bindings.json',{'checked_commit':target,'proof_commit':proof,'integration_commit':integration,'unchanged_prior_Git_paths':unchanged,'changed_prior_Git_paths':changes,'strict_original_pin_checks':pinchecks,'current_Lean_toolchain_bindings':science,'closed_actual_leases':leases,'root_status_log_bindings':checks,'root_lease':rootlease,'RAW46_followup_paths':follow,'RAW46_discovery':discovery,'chronology_correction':correction,'fresh_metadata_checks':fresh,'fake_closure':fake['totals'],'actual_graph_branch':branch,'graph_binding':binding('_site/data/underlying-lean-graph.json'),'sole_STABILIZING':stabilizing[0]})

class Codes(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.pre=False;self.code=False;self.items=[];self.buffer=[]
 def handle_starttag(self,t,a):
  if t=='pre':self.pre=True
  if t=='code' and self.pre:self.code=True;self.buffer=[]
 def handle_endtag(self,t):
  if t=='code' and self.code:self.items.append(''.join(self.buffer));self.code=False
  if t=='pre':self.pre=False
 def handle_data(self,d):
  if self.code:self.buffer.append(d)
companion='_site/example-cases/samplewiki/companions/smoothed-picard-hmc.html';s=(r/companion).read_text();start=s.index('data-authored-declaration="'+decl+'"');stop=s.index('</article>',start);article=s[start:stop]
lesson=load('website/content/declaration_lessons/standardized-rgo-kl-dimension.json')['units'][0]
assert len(lesson['steps'])==6
for step in lesson['steps']:
 assert html.escape(step['title']) in article and step['formula'] in html.unescape(article)
assert article.count('proof-reader-equation')==7
assert '<details open' not in article
assert 'ContDiff' in article and 'hH' in article
public_source=(r/'AutoSamplingTheory/ExampleCases/SmoothedPicardHMC/StandardizedRGOKLDimension.lean').read_text()
begin=public_source.index('theorem standardized_rgo_unique_prox_and_kl_le_dimension');public_block=public_source[begin:].strip();header=public_source[begin:public_source.index(' := by',begin)].strip()
public_codes=[html.unescape(c).strip() for c in re.findall(r'<pre[^>]*><code[^>]*>(.*?)</code></pre>',article,re.S)]
assert header in public_codes and public_block in public_codes
assert 'klDiv' in article and 'toReal' in article and 'finite' in article
assert 'GaussianT2/W2/FIRST4.6' in article
modules=[]
for src,page in [('AutoSamplingTheory/ExampleCases/SmoothedPicardHMC/StandardizedRGOKLDimension.lean','_site/modules/autosamplingtheory-examplecases-smoothedpicardhmc-standardizedrgokldimension.html'),('Tests/StandardizedRGOKLDimension.lean','_site/modules/tests-standardizedrgokldimension.html')]:
 parser=Codes();text=(r/page).read_text();parser.feed(text)
 src_text=lf((r/src).read_bytes()).decode()
 assert any(lf(c.encode()).decode().strip()==src_text.strip() for c in parser.items),(src,'full source absent')
 assert 'complete-module-source' in text
 modules.append({'source':binding(src),'standalone_render':binding(page),'complete_imports_and_source_exact':True})
testnames=['actual_fixed_posterior','actual_variable_step_family','rank_zero_actual_canonical_kl']
for n in testnames:assert n in (r/'Tests/StandardizedRGOKLDimension.lean').read_text() and n in (r/modules[1]['standalone_render']['path']).read_text()
links=re.findall(r'href="([^"]+)"',article)
assert any('standardizedrgoklfisher' in x for x in links) and any('standardizedrgopositionfisher' in x for x in links)
assert any('arxiv.org/html/2609.06906v1#S4.E6' in x for x in links)
(expo/'reviewer.seal.article.raw.snapshot.html').write_text(article,encoding='utf-8')
write(expo/'reviewer.seal.bindings.json',{'checked_commit':target,'companion':binding(companion),'article_snapshot':binding((expo/'reviewer.seal.article.raw.snapshot.html').relative_to(r).as_posix()),'lesson':binding('website/content/declaration_lessons/standardized-rgo-kl-dimension.json'),'publication':binding('website/content/publications/standardized-rgo-kl-dimension.json'),'six_formula_steps':lesson['steps'],'actual_public_folded_Lean':True,'assumptions_preserved':lesson['assumptions'],'standalone_modules':modules,'actual_three_tests':testnames,'source_and_parent_links':links,'actual_graph_branch':branch,'scope':'STATIC_ONLY_NO_BROWSER_OR_DELIVERY_CONTROLS_TESTED','stale_stage_phrase':'Existing immutable lesson/pub says independent/shared admission pending; later exact763 and integration924 receipts supersede stage wording only. No mathematical prose altered.','boundaries':['full inline imports and Tests within companion article','direct Test link from companion article','copy/download controls and bundles','rendered browser/mobile/visual acceptance','main merge and deployed live reader','complete PURIFIED delivery','Gaussian T2/W2/FIRST/full paper mains/work/cost']})
print(json.dumps({'checked_commit':target,'unchanged_prior_Git_paths':len(unchanged),'changed_prior_Git_paths':changes,'original_pin_checks':len(pinchecks),'canonical_Lean_toolchain_files':len(science),'root_nine_checks':9,'root_jobs':9150,'Tests_jobs':9429,'Registry':488,'fake':fake['totals'],'fresh_checks':[j['exit_code'] for j in fresh],'STATIC_six_steps':6,'standalone_complete_modules':2,'actual_tests':3},ensure_ascii=False))
