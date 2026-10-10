from pathlib import Path
import json,hashlib,datetime,subprocess,sys
r=Path('E:/Samplinglib');prefix='runs/20261007-companion-priority/standardized-rgo-kl-dimension';base=r/prefix;parent=base/'repository-seal45';expo=base/'exposition-seal45';out=parent/'graph-repair-review45';target='114d5412a0127d31809a9d55431cf89cdc378bc7'
sha=lambda b:hashlib.sha256(b).hexdigest();lf=lambda b:b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def enc(j):return (json.dumps(j,ensure_ascii=False,indent=2)+'\n').encode()
def put(p,j):p.write_bytes(enc(j))
def bind(p):
 b=p.read_bytes();return {'path':p.relative_to(r).as_posix(),'bytes':len(b),'raw_sha256':sha(b),'lf_sha256':sha(lf(b))}
def checkbinding(x):
 a=bind(r/x['path']);assert all(a[k]==x[k] for k in ['raw_sha256','lf_sha256','bytes']),x['path'];return a
assert json.loads((out/'reviewer.graph.lease.json').read_text())['status']=='OPEN'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=r).decode().strip()==target
prior=[]
for p,h in [(parent/'ProofSeal45.json','fedea4d355fa271310c8ff368bf9ed9541c50f8378a93c5419103326ee49b59e'),(expo/'ExpositionSeal45.json','68f468cb59d22c2c30c2bf1c5f6c8eb3f5a0d2ca2d2d38768d3e0c4a2a690606'),(parent/'reviewer.seal.lease.json','1a6b764a76ab7f81e76121cdd56fa92f7b010866cacd8fbd862637f1a75602b4'),(expo/'reviewer.seal.lease.json','cdddb768b7963a30488dbce659d95d37b566b47119b586a2c10ae4c349ce28e8')]:
 assert sha(p.read_bytes())==h,p;prior.append(bind(p))
pb=json.loads((parent/'reviewer.seal.bindings.json').read_text());pe=json.loads((expo/'reviewer.seal.bindings.json').read_text());proofseal=json.loads((parent/'ProofSeal45.json').read_text())
assert checkbinding(proofseal['bindings'])==bind(parent/'reviewer.seal.bindings.json')
assert checkbinding(json.loads((expo/'ExpositionSeal45.json').read_text())['binding'])==bind(expo/'reviewer.seal.bindings.json')
# Exact current bytes bind inherited source/compiler/fake seals without replaying transcripts or Lean.
science=[checkbinding(x) for x in pb['current_Lean_toolchain_bindings']]
for x in pb['closed_actual_leases']:
 checkbinding(x);assert json.loads((r/x['path']).read_text())['status']=='CLOSED'
for key in ['companion','lesson','publication','article_snapshot']:checkbinding(pe[key])
for x in pe['standalone_modules']:checkbinding(x['source']);checkbinding(x['standalone_render'])
for x in pb['fresh_metadata_checks']:checkbinding(x)
assert (parent/'reviewer.seal.graph-failed.original.log').read_bytes()==(r/pb['fresh_metadata_checks'][-1]['path']).read_bytes()
diagnosis=checkbinding(proofseal['graph_diagnosis'])

rootlease=json.loads((base/'root.post-admin-graph.lease.json').read_text());assert rootlease['status']=='CLOSED' and rootlease['compiler']=='NOT_STARTED_CLOSED' and rootlease['checked_commit']==target
roots=[]
for i,name in enumerate(['official-graph','graph','site-check']):
 p=base/f'post-admin.{name}.status.json';j=json.loads(p.read_text());b=(base/f'post-admin.{name}.log').read_bytes()
 assert j==rootlease['checks'][i] and j['exit_code']==0 and j['checked_commit']==target and sha(b)==j['log_raw_sha256']
 assert rootlease['opened_utc']<=j['started_utc']<j['finished_utc']<=rootlease['closed_utc']
 roots.append({'status':bind(p),'log':bind(base/f'post-admin.{name}.log'),'execution':j})

sys.path.insert(0,str(r/'tools'));sys.path.insert(0,str(r/'website/scripts'))
import publication_reader,astis_publication,astis_advance
graph=json.loads((r/'_site/data/underlying-lean-graph.json').read_text());actualdigest=publication_reader.graph_input_digest()
assert actualdigest==graph['publication_inputs_sha256']=='2c19b58d58dc66e92df76c481752b77b5038cefa21c3a2b4a1478faefb90fd94'
module='AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGOKLDimension';decl=module+'.standardized_rgo_unique_prox_and_kl_le_dimension';branch=[e for e in graph['edges'] if module in json.dumps(e) or 'Tests.StandardizedRGOKLDimension' in json.dumps(e)]
assert branch==pb['actual_graph_branch']==pe['actual_graph_branch']
nodes={x['id']:x for x in graph['nodes']};assert nodes['module:'+module]['status']=='compiled' and nodes['module:Tests.StandardizedRGOKLDimension']['status']=='compiled'
for p in ['AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGOKLFisher','AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGOPositionFisher']:
 assert {'source':'module:'+p,'target':'module:'+module,'relation':'imports'} in branch
assert {'source':'module:'+module,'target':'decl:'+decl,'relation':'declares'} in branch
assert graph['reference_contract']=='Name-scanned references are incomplete signals, not elaborated proof dependencies.'
for name in pe['actual_three_tests']:
 assert name in (r/pe['standalone_modules'][1]['source']['path']).read_text() and name in (r/pe['standalone_modules'][1]['standalone_render']['path']).read_text()
cmd=[sys.executable,'tools/astis_publication.py','graph-check','--cell','ASTIS-SW-SPHMC-standardized-rgo-kl-dimension','--output','_site'];started=datetime.datetime.now(datetime.timezone.utc).isoformat();res=subprocess.run(cmd,cwd=r,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(out/'reviewer.graph.check.log').write_bytes(res.stdout);finished=datetime.datetime.now(datetime.timezone.utc).isoformat();assert res.returncode==0
report=json.loads(res.stdout);assert report['status']=='graph coverage checked'
state=astis_advance.current_advances();assert state['ASTIS-SA-20261007-StandardizedRGOKLDimension']['state']=='VERIFIED';assert [k for k,j in state.items() if j.get('state')=='STABILIZING']==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
receipts={'checked_commit':target,'prior_seals_and_actual_closed_leases':prior,'inherited_current_science_source_Test_toolchain_exact_count':len(science),'current_science_source_Test_toolchain_exact_bindings':science,'root_closed_lease':bind(base/'root.post-admin-graph.lease.json'),'root_three_actual_status_logs':roots,'generated_graph':bind(r/'_site/data/underlying-lean-graph.json'),'actual_publication_input_digest':actualdigest,'exact_unchanged_graph_branch':branch,'inherited_original_failed_diagnosis':diagnosis,'inherited_original_failed_log':bind(parent/'reviewer.seal.graph-failed.original.log'),'independent_current_graph_check':{'command':cmd,'exit_code':res.returncode,'started_utc':started,'finished_utc':finished,'log':bind(out/'reviewer.graph.check.log')},'compiler':'NOT_STARTED_CLOSED'}
put(out/'reviewer.graph.bindings.json',receipts)
overlay={'schema_version':1,'seal':'ProofSeal45-current-graph-freshness-overlay','actor':'picard_commit_verifier_43','role':'independent bounded freshness repair reviewer','checked_commit':target,'status':'ACCEPTED_SCOPED_CURRENT_GRAPH_FRESHNESS_REPAIR','resolved_typed_boundary':'CURRENT_GENERATED_GRAPH_FRESHNESS_OPEN at original ProofSeal45; root officialgraph regenerated current administrative inputs, then graph/site checks passed; independent current cell graph-check now EXIT0','actual_generated_digest':actualdigest,'parent_repository_science_source_aggregate_scope':'exact reuse; actual1100Lean/Test/toolchain bytes unchanged, original763 VERIFICATION/root9150Tests9429/Registry488/focused3827direct3/reachability286/52modules/fake0 reused; no new compiler or semantic proof claim','parent_static_exposition_scope':'exact original sixformula/foldedpublicLean and standalone completeimports/all3Test snapshots reused, actualbranch identical','source_overlays':'source correspondence, audit and incomplete scanner references retain original nonformal relation labels; 43+31 are actual production module imports','original_negative_evidence':'ProofSeal45 and original failedgraph log/digest diagnosis preserved byte-exact; overlay resolves freshness only without rewriting historical FAILED or current114 original scope','root_evidence':roots,'bindings':bind(out/'reviewer.graph.bindings.json'),'compiler':'NOT_STARTED_CLOSED','no_canonical_writes_or_VERIFIED_transition':True,'sole_STABILIZING':'ASTIS-SA-20261005-SPHMCImplementedPhaseKernel unchanged','excluded_credit':['full companion inline imports/Tests/directTestlink/copy/download/bundle delivery','browser/mobile/visual checks','main merge/deployedlive/fullreader/PURIFIED','GaussianT2/W2/FIRST/fullpaper mains/sampler/error/work/cost/composition','source-only future48'], 'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
put(out/'ProofSeal45.graph-freshness-overlay.json',overlay)
outputs=[bind(p) for p in sorted(out.iterdir()) if p.is_file() and p.name not in ['reviewer.graph.run.json','reviewer.graph.lease.json','reviewer.graph.lease.closed.json']]
run={'actor':'picard_commit_verifier_43','checked_commit':target,'scope':'graph freshness repair only','outputs':outputs,'compiler':'NOT_STARTED_CLOSED','completed_utc':overlay['completed_utc']};run['run_hash']=sha(json.dumps(run,sort_keys=True,separators=(',',':')).encode());put(out/'reviewer.graph.run.json',run)
lease=json.loads((out/'reviewer.graph.lease.json').read_text());lease.update(status='CLOSED',read='CLOSED',python='CLOSED',write='CLOSED',compiler='NOT_STARTED_CLOSED',closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),overlay=bind(out/'ProofSeal45.graph-freshness-overlay.json'),run=bind(out/'reviewer.graph.run.json'),final_operation='Actual aggregate lease closure is final filesystem operation; no canonical mutation.')
result={'overlay':bind(out/'ProofSeal45.graph-freshness-overlay.json'),'run_hash':run['run_hash'],'closed_actual_lease_raw_sha256':sha(enc(lease)),'generated_digest':actualdigest,'independent_graph_check_exit':0}
put(out/'reviewer.graph.lease.closed.json',lease)
# Final filesystem operation.
put(out/'reviewer.graph.lease.json',lease)
print(json.dumps(result))
