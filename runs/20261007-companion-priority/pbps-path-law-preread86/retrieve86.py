from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,subprocess,datetime
R=Path('E:/Samplinglib'); D=R/'runs/20261007-companion-priority/pbps-path-law-preread86'; O=D/'root-retrieval86'; O.mkdir(exist_ok=False)
def pin(p): return {'path':str(p.relative_to(R)).replace('\\','/'),'raw_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
queries=[
 ('local-density',['rg','-n','first.*(event|wait)|hazard.*density|density.*hazard|withDensity.*exp|ext_of_Iic','AutoSamplingTheory','-g','*.lean']),
 ('mathlib-cdf',['rg','-n','theorem.*(ext_of_Iic|integral_eq_sub_of_hasDerivAt|integral_hasDerivAt_right|integral_ofReal|integral_withDensity|integrable_withDensity|lintegral_ofReal|measureReal_def)','@M/MeasureTheory','-g','*.lean']),
 ('shared-frontiers',['rg','-l','first.event|hazard.*density|integrated.hazard|inverse.hazard','research-wiki/frontier-cells','Libraries']),
 ('upstream-compatibility',['rg','-n','first.event|hazard|exponential.*(density|distribution)','research-wiki/external-lean-libraries','research-wiki/openai-math-2026-intake.json']),
 ('mathlib-maps',['rg','-n','theorem.*(map_restrict|restrict_map|map_map|integrable_map_measure|integral_map|restrict_apply|measureReal_eq_measureReal_iff)','@M/MeasureTheory/Measure/Map.lean','@M/MeasureTheory/Integral/Bochner/Basic.lean','@M/MeasureTheory/Integral/Bochner/ContinuousLinearMap.lean','@M/MeasureTheory/Function/L1Space/Integrable.lean'])]
def search(q):
 name,args=q;args=[x.replace('@M','.lake/packages/mathlib/Mathlib') for x in args]
 p=subprocess.run(args,cwd=R,capture_output=True); assert p.returncode in (0,1),(args,p.stderr)
 f=O/(name+'.txt');f.write_bytes(p.stdout)
 return {'command':args,'exit_code':p.returncode,'output':pin(f),'lines':len(p.stdout.splitlines())}
with ThreadPoolExecutor(max_workers=5) as pool: checks=list(pool.map(search,queries))
prior=json.loads((R/'runs/20261007-companion-priority/pbps-transition-kernel-preread85/retrieval85/reuse-decision85.json').read_bytes())['protocol_and_interface_pins']
for p,h in prior.items(): assert hashlib.sha256((R/p).read_bytes()).hexdigest()==h,p
cards=['AutoSamplingTheory.Probability','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHazardClock','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBounceRate','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow','AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct']
reads=[]
for module in cards:
 p=R/'research-wiki/sampling-sde-library/cards'/(module+'.md'); p.read_text(encoding='utf-8'); reads.append(pin(p))
post={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),'origin_main':subprocess.check_output(['git','rev-parse','origin/main'],cwd=R).decode().strip(),'working_branch_updated':False,'reason':'Existing branch retains pushed scientific lineage and original21 tracked collaborator modifications; fetched main unchanged.'}
(D/'post-fetch86.json').write_text(json.dumps(post,indent=2)+'\n',encoding='utf-8')
z={'status':'statement-interface-and-reuse-search-only-before-seal','checks':checks,'module_cards_read':reads,'unchanged_protocol_pins_reused':prior,'source_inputs':pin(D/'statement-api-retrieval86.json'),'no_proof_search':True,'no_external_port':True,'no_shared_changes':True,'decision':'Candidate actual density is strictly beyond actual75 tail/CDF. Generic fixed Mathlib FTC, finite-measure interval extensionality, withDensity and map APIs should be adapted internally. Do not duplicate CDF wrapper or add density/regularity hypotheses to source anchor; independent topology review still pending.'}
(O/'retrieval86.json').write_text(json.dumps(z,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'queries':[{'lines':x['lines'],'exit':x['exit_code']} for x in checks],'cards':len(reads),'protocol_pins':len(prior),'post_fetch':post}))
