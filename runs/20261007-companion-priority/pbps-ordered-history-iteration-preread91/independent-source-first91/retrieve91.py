from pathlib import Path
import subprocess,json,hashlib,datetime
ROOT=Path('E:/Samplinglib');OUT=ROOT/'runs/20261007-companion-priority/pbps-ordered-history-iteration-preread91/independent-source-first91'
def desc(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def write(n,x):
 p=OUT/n;assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8');return desc(p)
queries=[
 ('local-pbps-coordinates',['rg','-n','-i','ordered|absolute.time|simplex|cumulative|translation','AutoSamplingTheory/ExampleCases/ProximalBPS','--glob','*.lean']),
 ('local-shared-coordinates',['rg','-n','-i','shear|translation|translate|lintegral_add|map_add_left','AutoSamplingTheory/TechnicalLemmas','AutoSamplingTheory/Probability.lean','AutoSamplingTheory/SDE.lean','--glob','*.lean']),
 ('mathlib-translation',['rg','-n','map_mul_left_eq_self|measurePreserving_mul_left|skew_product|lintegral_map|lintegral_withDensity_eq_lintegral_mul|measurable_lintegral_prod_right','--glob','*.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Group/Measure.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Prod.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/WithDensity.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Lebesgue/Map.lean']),
 ('upstream-metadata',['rg','-n','-i','pbps|point.process|poisson|exponential|translation|lebesgue|conditional','research-wiki/openai-math-2026-intake.json','research-wiki/external-lean-libraries'])]
receipts=[]
for name,cmd in queries:
 p=subprocess.run(cmd,cwd=ROOT,capture_output=True,encoding='utf8');receipts.append(write('retrieval91.'+name+'.native.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':cmd,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'interpretation':'Read-only retrieval; matches are candidates, not local theorem certificates. Exit1 means no matches.'}))
paths=[
 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryExtension.lean',
 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualConditionalNextWaitDensity.lean',
 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualConditionalNextWaitSurvival.lean',
 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryTailLaw.lean',
 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualNonaccumulation.lean',
 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhysicalTimeCover.lean',
 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean',
 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean',
 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBounceRate.lean',
 '.lake/packages/mathlib/Mathlib/MeasureTheory/Group/Measure.lean',
 '.lake/packages/mathlib/Mathlib/MeasureTheory/Group/Prod.lean',
 '.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Prod.lean',
 '.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/WithDensity.lean',
 'AutoSamplingTheory/Probability.lean','AutoSamplingTheory/SDE.lean',
 'research-wiki/technical-lemmas/README.md','docs/openai-math-assimilation-protocol.md',
 'research-wiki/openai-math-2026-intake.json','research-wiki/external-lean-libraries/README.md',
 'research-wiki/external-lean-libraries/mathlib.md','research-wiki/external-lean-libraries/lean-stat-learning-theory.md',
 'lean-toolchain','lake-manifest.json',
 'runs/20261007-companion-priority/pbps-next-history-extension-preread90/source-proof-graph90.accepted-successor.json',
 'runs/20261007-companion-priority/pbps-actual-finite-first-event-law86/topology-repair-review86/source-proof-graph86.single-edge-proposed-successor.json',
 'runs/20261007-companion-priority/pbps-actual-finite-first-event-law86/independent-source86/source-inventory86.exhaustive-successor.json']
interfaces=[]
for rel in paths:
 p=ROOT/rel
 if p.suffix=='.lean' and 'ExampleCases' in rel:
  s=p.read_bytes();stop=s.find(b':= by',s.find(b'\ntheorem '));assert stop>=0
  dest=OUT/('interface91.'+p.stem+'.exactraw.lean');assert not dest.exists();dest.write_bytes(s[:stop]+b'\n')
  interfaces.append({'module':desc(p),'snapshot_header_only':desc(dest),'cut':'Before first public theorem proof; whole private Prop and public binders retained. No91 candidate/Lean exists.'})
cells=[]
for p in sorted((ROOT/'research-wiki/frontier-cells').glob('*.json')):
 j=json.loads(p.read_text(encoding='utf8'));s=json.dumps(j).lower()
 if (p.name.startswith('ASTIS-SW-PBPS-actual-') and any(x in p.name for x in ['history','hazard','finite-first','nonaccum','physical-time','event-time','jump-recursion'])) or (p.name.startswith('ASTIS-SHARED-') and any(x in p.name for x in ['mixture','kernel-invariant','markov-kernel'])):
  cells.append({'input':desc(p),'state':j.get('status',j.get('state')),'delta':j.get('theorem_delta',j.get('boundary','')),'goal':j.get('goal','')})
  paths.append(p.relative_to(ROOT).as_posix())
snapshots=[]
for rel in paths+['docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json']:
 p=ROOT/rel
 if rel.startswith('.lake/') or '/runs/' in p.as_posix():continue
 dest=OUT/'input-snapshots91'/rel;dest.parent.mkdir(parents=True,exist_ok=True);assert not dest.exists();dest.write_bytes(p.read_bytes());snapshots.append({'original_at_read':desc(p),'immutable_snapshot':desc(dest)})
out=write('retrieval91.native.json',{'schema':'astis-source-retrieval91-v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'primary_first_predecessor':desc(OUT/'primary-first91.freeze.native.json'),'queries':receipts,'inputs':[desc(ROOT/p) for p in paths],'interfaces':interfaces,'mutable_input_snapshots':snapshots,'shared_frontier_results':cells,'fixed_toolchain':'leanprover/lean4:v4.33.0','fixed_mathlib_rev':'db584cd6d46c92f209a44c0f1c829460d327499d','reuse_findings':[
 {'library':'Samplinglib','classification':'adapt-existing','result':'Actual90 complete-history relative-wait extension is the main stochastic parent. Actual89 provides the jointly Borel finite density and all-history fiber finite bound; direct89 use is optional if these facts are rederived internally, but its density is genuinely consumed transitively by90. No existing actual absolute-time density law located by these queries.'},
 {'library':'Samplinglib adjacent','classification':'reuse-existing-later','result':'Actual88 d-parametric survival is consumed only at final survival assembly. ActualNonaccumulation and ActualPhysicalTimeCover already give actual-input event-time finiteness/unique half-open interval coverage; they do not by themselves identify A7 strict-horizon count/path density.'},
 {'library':'fixed Mathlib','classification':'reuse','declarations':['MeasureTheory.map_add_left_eq_self','MeasureTheory.measurePreserving_add_left','MeasureTheory.MeasurePreserving.skew_product','MeasureTheory.MeasurePreserving.lintegral_comp','MeasureTheory.lintegral_withDensity_eq_lintegral_mul'],'result':'History-dependent additive shear follows by jointly Borel translation and fiber Lebesgue translation invariance. Additive names generated by to_additive; no compilation claim for a91 application.'},
 {'library':'shared Frontier Cells','classification':'no-duplicate-target-found','result':'Existing finite-kernel mixture/Markov transport cells do not provide actual iid stopped PBPS absolute event-time density. Existing history/density/extension/survival and nonaccumulation/cover cells should be reused, not reproved as new advances.'},
 {'library':'compatible upstream','classification':'provenance-only-not-used','result':'Reviewed OpenAI intake pinned adc7f1241b42e322a6451854ab7e4b4c146bf78a/Apache2 and external library catalog searched. No matching source-specific next-event adapter located; no material imported, no upstream theorem assumed compiled locally. Fixed Mathlib plus ASTIS suffices, so no new upstream assimilation is proposed.'}],
 'search_limit':'Bounded text/index search, not exhaustive theorem nonexistence proof. An initial guessed ActualEventTimeNonaccumulation filename was absent; rg --files found ActualNonaccumulation and its actual signature was inspected. This was a retrieval correction, not failed mathematics.',
 'no_implementation':True,'creator_self_approval':False})
print(json.dumps({'retrieval':out,'queries':receipts,'interface_count':len(interfaces),'cells':len(cells),'snapshots':len(snapshots)},indent=2))
