from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,subprocess
r=Path(__file__).parent;out=r/'retrieval85';out.mkdir(exist_ok=False)
queries=[
 ('local-law',['rg','-n','lawMapEqOfAEEq|lawMapIntegral|Kernel.id|Kernel.const|hHlaw|IsMarkovKernel','AutoSamplingTheory/Probability.lean','AutoSamplingTheory/TechnicalLemmas/Probability/LawMap.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/IdealHalfTurnKernel.lean']),
 ('local-duplicate',['rg','-n','actual_.*(phase|transition).*kernel|actual.*physical.*kernel','AutoSamplingTheory','-g','*.lean']),
 ('mathlib-kernel',['rg','-n','theorem map_apply|instance.*map|theorem.*map|prod_apply|const_apply|id_apply','@M/Probability/Kernel/Composition/MapComap.lean','@M/Probability/Kernel/Composition/Prod.lean','@M/Probability/Kernel/Basic.lean']),
 ('mathlib-integral',['rg','-n','theorem integral_map|integrable_map_measure|integrable_of_bound|map_congr|map_const|dirac_prod','@M/MeasureTheory/Integral/Bochner/Basic.lean','@M/MeasureTheory/Function/L1Space/Integrable.lean','@M/MeasureTheory/Measure/Map.lean','@M/MeasureTheory/Measure/Prod.lean']),
 ('shared-cells',['rg','-l','kernel.*transport|actual.*phase.*kernel|physical.*measur|law.*map','research-wiki/frontier-cells','Libraries/shared-foundations.yml']),
 ('upstream-index',['rg','-l','probability kernel|pushforward|Markov|law.*map','research-wiki/external-lean-libraries','research-wiki/openai-math-2026-intake.json'])]
queries=[(k,[s.replace('@M','.lake/packages/mathlib/Mathlib') for s in args]) for k,args in queries]
def search(item):
 label,args=item;q=subprocess.run(args,capture_output=True)
 assert q.returncode in (0,1),(args,q.stderr)
 p=out/(label+'.txt');p.write_bytes(q.stdout)
 return dict(command=args,exit_code=q.returncode,output=p.as_posix(),RAW_sha256=hashlib.sha256(q.stdout).hexdigest(),lines=len(q.stdout.splitlines()))
with ThreadPoolExecutor(max_workers=6) as pool:checks=list(pool.map(search,queries))
prior=json.loads((r.parent/'pbps-outer-bounded-l2-preread84/retrieval84-v2/reuse-decision84.json').read_bytes())['protocol_and_interface_pins']
for p,h in prior.items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h,p
cards=['research-wiki/sampling-sde-library/cards/AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeMeasurability.md','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.ExampleCases.ProximalBPS.IdealHalfTurnKernel.md','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.Probability.md','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.TechnicalLemmas.Probability.LawMap.md','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.TechnicalLemmas.Probability.KernelTransport.md','AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhysicalTimeMeasurability.lean','AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean']
readings={p:Path(p).read_text(encoding='utf8') for p in cards}
(out/'parent-interfaces.read.json').write_text(json.dumps(readings,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
execution=json.loads(Path('website/content/samplewiki_companion_frontiers.json').read_bytes())['execution']
z=dict(classification='adapt',decision='adapt_existing',canonical_declaration='Prospective actual_phase_transition_kernel, not sealed yet',queries=checks,protocol_and_interface_pins=prior,protocol_reuse='All preceding mandatory protocol RAWs unchanged and verified; reads reused.',parent_interface_pins={p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in cards},execution=execution,reused_declarations=['ActualPhysicalTimeMeasurability.actual_physical_time_measurable_phase','UnitExponentialProduct.unit_exponential_product_laws','ProbabilityTheory.Kernel.map','ProbabilityTheory.Kernel.prod','ProbabilityTheory.Kernel.const','ProbabilityTheory.Kernel.id','MeasureTheory.integral_map','MeasureTheory.Measure.map_congr','MeasureTheory.Integrable.of_bound'],consumer='PBPS AppendixA.1 actual transition law and bounded Borel transition tests: export literal-clock fiber laws and zero-time initialization, integrate source test identities without substituting an ideal sampler.',reason='Generic kernel construction APIs already exist in fixed Mathlib. Existing81 is ideal random-reference/momentum position law at pi, not this full-phase arbitrary-time law. Use actual80 directly; no reproof of actual84 outer convergence and no generic duplicate wrapper. Generic semigroup contracts include unproved Chapman-Kolmogorov and cannot be used as actual producers.',external_port_used=False,upstream_search_scope='Bounded registered compatibility/source indexes only; no upstream result is imported or credited.',no_BODY_before_StatementSeal=True,proof_ingredients_not_source_binders=True,sole_writer='companion_root_20261005')
(out/'reuse-decision85.json').write_text(json.dumps(z,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('Six searches and current parent/core cards recorded; fixed Mathlib reuse, no port or duplicate generic wrapper')
