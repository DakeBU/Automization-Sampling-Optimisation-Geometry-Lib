import json,hashlib,re,subprocess,sys,datetime
from pathlib import Path
r=Path('E:/Samplinglib');run=r/'runs/20261007-companion-priority/pbps-gaussian-marginal-gradient';out=run/'whole-proof-review51';freeze=run/'math-freeze.json';H=lambda b:hashlib.sha256(b).hexdigest();LF=lambda b:b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def read(p):return json.loads(Path(p).read_text('utf-8'))
def encode(d):return (json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode()
def dump(n,d):(out/n).write_bytes(encode(d))
def pin(p):
 p=Path(p);b=p.read_bytes();return {'path':p.relative_to(r).as_posix(),'raw_sha256':H(b),'lf_sha256':H(LF(b)),'raw_bytes':len(b),'lf_bytes':len(LF(b))}
assert read(out/'lease.json')['status']=='OPEN'and not read(out/'lease.json')['compiler_started'];m=read(freeze);assert len(m['inputs'])==53
rows=[]
for x in m['inputs']:
 p=r/x['path'];b=p.read_bytes();assert H(b)==x['raw_sha256']and H(LF(b))==x['lf_sha256']and len(b)==x['bytes'];rows.append(pin(p))
dump('freeze-bindings.json',rows)
prod=r/'AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/GaussianMarginalGradient.lean';test=r/'Tests/ProximalBPSGaussianMarginalGradient.lean';b=prod.read_bytes();a=b.index(b'theorem gaussian_marginal_gradient_closable');z=b.index(b':= by',a);header=LF(b[a:z]).rstrip()+b'\n';assert len(header)==697 and H(header)=='d7273526caa94ec518b790626edb6b289bdabfdd1104a196cd2e8eb110211e81';assert header==LF((r/'runs/20261007-companion-priority/pbps-gaussian-marginal-gradient-preproof51/prospective-statement.txt').read_bytes());(out/'actual-public-header.lf').write_bytes(header)
text=prod.read_text('utf-8');tt=test.read_text('utf-8');assert len(re.findall(r'^theorem ',text,re.M))==1 and len(re.findall(r'^theorem ',tt,re.M))==2 and not re.search(r'^private (theorem|def|instance)',text,re.M)
assert text.count('gaussian_convolution_potential_c2')==1 and text.count('WeightedGradient.compact_gradient_closable')==1
assert text.index('have hI : Integrable')<text.index('have hnorm')<text.index('have htilt')<text.index('rw [← htilt]')<text.index('exact WeightedGradient.compact_gradient_closable')
assert 'let : IsProbabilityMeasure J' in text and 'let : IsProbabilityMeasure ν'in text and 'Measure.map_map measurable_snd hpair'in text
assert '(μ : Measure E) [IsProbabilityMeasure μ] {η : ℝ} (hη : 0 < η)'in header.decode() and 'ContDiff ℝ ∞ f'in header.decode()
# All exact source/API provider fragments, no implementation-directed source topology rewrite.
providers=read(r/'runs/20261007-companion-priority/pbps-gaussian-marginal-gradient-topology-overlay51/selected-providers.json');apiout=[];d=out/'selected-apis';d.mkdir(exist_ok=True)
for i,x in enumerate(providers):
 p=Path(x['path']);b=p.read_bytes();assert H(b)==x['whole_raw_sha256']and H(LF(b))==x['whole_lf_sha256'];fragment=b[x['start_utf8_byte0']:x['end_utf8_byte0_exclusive']];assert H(fragment)==x['fragment_raw_sha256']and H(LF(fragment))==x['fragment_lf_sha256'];name=f'{i:02d}';(d/(name+'.raw')).write_bytes(fragment);(d/(name+'.lf')).write_bytes(LF(fragment));apiout.append({**x,'own_raw_snapshot':pin(d/(name+'.raw')),'own_LF_snapshot':pin(d/(name+'.lf'))})
dump('source-api-fragment-bindings.json',apiout)
# Additional actual body/domain primitives exercised in normalization/closure/Test; bind bounded exact raw slices.
extras=[('LinearPMap.IsClosed/IsClosable and closure real conditional choice','Mathlib/Topology/Algebra/Module/LinearPMap.lean',63,71),('LinearPMap.closure chooses actual closed graph only under provenclosability','Mathlib/Topology/Algebra/Module/LinearPMap.lean',94,109),('Continuous.memLp_of_hasCompactSupport implicit finitecompacts contract','Mathlib/MeasureTheory/Function/LpSpace/Indicator.lean',23,33),('Continuous.memLp_of_hasCompactSupport','Mathlib/MeasureTheory/Function/LpSpace/Indicator.lean',82,87),('fderiv vanishes offsupport','Mathlib/Analysis/Calculus/FDeriv/Const.lean',374,377)]
extra=[]
for i,(label,path,start,end)in enumerate(extras):
 p=r/'.lake/packages/mathlib'/path;b=p.read_bytes();fragment=b''.join(b.splitlines(keepends=True)[start-1:end]);name='extra'+str(i);(d/(name+'.raw')).write_bytes(fragment);(d/(name+'.lf')).write_bytes(LF(fragment));extra.append({'id':label,'whole':pin(p),'physical_lines1':[start,end],'fragment_raw_sha256':H(fragment),'fragment_lf_sha256':H(LF(fragment)),'snapshot_raw':pin(d/(name+'.raw')),'snapshot_LF':pin(d/(name+'.lf'))})
gp=r/'AutoSamplingTheory/TechnicalLemmas/Analysis/Calculus/Gradient.lean';b=gp.read_bytes();fragment=b''.join(b.splitlines(keepends=True)[113:119]);(d/'canonical-continuous-gradient.raw').write_bytes(fragment);extra.append({'id':'canonical continuous_gradient_of_contDiff_one Test helper, C1/CompleteSpace follows finiteHilbert','whole':pin(gp),'fragment':pin(d/'canonical-continuous-gradient.raw')});dump('extra-api-bindings.json',extra)
# Complete project-local recursive import reachability; admitted parent internals retained opaque in semantic review.
sys.path[:0]=[str(r),str(r/'tools')];from tools import astis,astis_advance
todo=['AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianMarginalGradient','Tests.ProximalBPSGaussianMarginalGradient'];seen={};edges=[];external=set();hits=[];rawmarkers=[]
while todo:
 module=todo.pop()
 if module in seen:continue
 p=r/(module.replace('.','/')+'.lean');b=p.read_bytes();t=b.decode('utf-8');seen[module]=pin(p);clean=astis.strip_lean_comments_and_strings(t)
 for lineno,line in enumerate(clean.splitlines(),1):
  if astis.FORBIDDEN_REGEX.search(line):hits.append({'module':module,'line':lineno,'text':line.strip()})
 for lineno,line in enumerate(t.splitlines(),1):
  if astis.FORBIDDEN_REGEX.search(line):rawmarkers.append({'module':module,'line':lineno,'scope':'raw doc/string marker only unless also executable hit'})
 for imported in re.findall(r'^import\s+(\S+)',clean,re.M):
  if imported.startswith(('AutoSamplingTheory.','Tests.')):edges.append({'prerequisite':imported,'consumer':module});todo.append(imported)
  else:external.add(imported)
assert not hits;dump('reachable-local-import-closure.json',{'modules':seen,'edges':edges,'external_imports':sorted(external),'scope':'Complete local import closure binding/lexicalscan, not complete elaborated constant graph or fullMathlibbody audit.'});dump('fake-closure-scan.json',{'local_modules':len(seen),'executable_fake_closure_hits':hits,'raw_nonclosure_markers':rawmarkers,'three_kernel_prints_checked_separately':True})
control=read(run/'current-control.json');states=astis_advance.current_advances();stabilizing={k:v.get('owner_id')for k,v in states.items()if v.get('state')=='STABILIZING'};assert list(stabilizing)==control['sole_stabilization_owner'];parentchecks=[]
for decl,admissions in control['parent_admissions'].items():
 for a in admissions:assert states[a['id']]['state']==a['state']
 p=r/(decl.rsplit('.',1)[0].replace('.','/')+'.lean');raw=p.read_bytes();committed=subprocess.check_output(['git','show',m['checked_base_commit']+':'+p.relative_to(r).as_posix()],cwd=r);assert committed in(raw,LF(raw));parentchecks.append({'declaration':decl,'admitted_state':admissions,'current':pin(p),'Git_base_blob_sha256':H(committed),'semantic_review':'Existing admitted theorem header/contracts opaque; no re-review of unchanged parentinternals claimed.'})
# Actual50 accepted producer is reused only for same-law inputprobability at this Test consumer.
p50=r/'AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicEnergy.lean';assert H(p50.read_bytes())=='4cd87c85f195774c4182894629e2f24efb3c1c1955447833d686d6826b5bab3a';assert 'MacroscopicEnergy.actual_macroscopic_gradient_energy_blocks'in tt and 'letI : IsProbabilityMeasure μ := hactual.1'in tt
assert 'hf2.toLp f,hg2.toLp (gradient f),hf2.coeFn_toLp,hg2.coeFn_toLp'in tt and 'hgrad.memLp_of_hasCompactSupport hgc'in tt;assert 'rank_zero_noncentered_graph'in tt and 'hmean' in tt and 'simpa only [hv0] using hgraph'in tt
compiler=[]
for label in ['production.2','tests.0']:
 s=read(run/(label+'.status.json'));l=read(run/(label+'.compiler.lease.json'));p=r/l['source'];assert s['exit_code']==l['exit_code']==0 and l['status']==l['compiler']==l['Python']=='CLOSED'and l['opened_utc']<=s['finished_utc']<=l['closed_utc']<read(out/'lease.json')['opened_utc'];assert H((run/(label+'.log')).read_bytes())==s['log_raw_sha256']and H(p.read_bytes())==s['source_raw_sha256'];assert p.read_bytes()==(run/(label+'.source.raw.snapshot.lean')).read_bytes();compiler.append({'status':pin(run/(label+'.status.json')),'log':pin(run/(label+'.log')),'lease':pin(run/(label+'.compiler.lease.json')),'reused_only':True})
log=(run/'tests.0.log').read_text('utf-8');sets=re.findall(r"'([^']+)' depends on axioms: \[(.*?)\]",log,re.S);assert len(sets)==3 and all(set(re.findall(r'[\w.]+',s))=={'propext','Classical.choice','Quot.sound'}for _,s in sets)and 'Build completed successfully (3893 jobs).'in log
for name in ['production.0.compiler.lease.json','production.1.compiler.lease.json','production.2.compiler.lease.json','tests.0.compiler.lease.json']:assert read(run/name)['status']=='CLOSED'
top=read(r/'runs/20261007-companion-priority/pbps-gaussian-marginal-gradient-topology-review51/source-topology-review.repaired.json');seal=read(r/'runs/20261007-companion-priority/pbps-gaussian-marginal-gradient-preproof-review51/statement.typed-admission.review.json');assert not top['blocking']and not seal['blocking']and seal['signature_lf_sha256']==H(header)
dump('checked-mathematics.json',{'frozen_base_commit':m['checked_base_commit'],'freeze_inputs':53,'public_header_LF_bytes':697,'public_header_LF_sha256':H(header),'production':pin(prod),'tests':pin(test),'parent_contract_reuse':parentchecks,'actual50_same_law_probability_consumer':pin(p50),'selected_source_API_fragments':len(apiout),'additional_domain_API_fragments':len(extra),'recursive_ASTIS_modules':len(seen),'fake_hits':0,'compiler_reuse':compiler,'three_standard_axiom_sets':[{'declaration':d,'axioms':re.findall(r'[\w.]+',s)}for d,s in sets],'sole_STABILIZING':stabilizing,'no_new_private_or_public_provider':'One exactpublic697 theorem; no private/helper declaration. All normalization bridges local have/let, actualtwo admitted parent calls. Tests2consumer proofs reviewed complete.','source_topology_reuse':'Accepted repaired selected-source/API graph used only as contract, no self/finalsource admission or wholepaper coverage.','mathematical_blockers':[],'remaining':m['remaining_boundary'],'compiler_used_by_reviewer':False,'exact_commit_VERIFIED':False,'future_anonymous_decoder_source_review_publication_not_read':True})
print(json.dumps({'header':H(header),'freeze':53,'source_API':len(apiout),'extra_API':len(extra),'recursive_modules':len(seen),'fake':0,'axiom_sets':3,'whole_math':'ACCEPT_SCOPED_NO_MATHEMATICAL_BLOCKER','compiler':'NOT_STARTED_CLOSED'}))
