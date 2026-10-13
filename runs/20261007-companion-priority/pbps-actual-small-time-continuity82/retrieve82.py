from pathlib import Path
import hashlib,json,subprocess,sys
r=Path(__file__).parent;out=r/'retrieval82';out.mkdir(exist_ok=False)
def save(name,x):(out/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def search(label,args):
 p=subprocess.run(['rg',*args],capture_output=True);assert p.returncode in [0,1]
 (out/(label+'.stdout.snapshot')).write_bytes(p.stdout);(out/(label+'.stderr.log')).write_bytes(p.stderr)
 return dict(search=label,command=['rg',*args],exit_code=p.returncode,matching_lines=len(p.stdout.splitlines()),RAW_sha256=hashlib.sha256(p.stdout).hexdigest())
queries=[]
queries.append(search('local-duplicates',['-n','stochastic.*contin|small.time|first.*defect|first.*jump.*prob','AutoSamplingTheory/ExampleCases/ProximalBPS','AutoSamplingTheory/TechnicalLemmas','research-wiki/frontier-cells','-g','*.lean','-g','*.json']))
queries.append(search('mathlib-probability-floor',['-n','measureReal_mono|measureReal_compl|map_map|map_apply',' .lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Real.lean'.strip(),'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Map.lean']))
queries.append(search('mathlib-limits',['-n','theorem tendsto_of_tendsto_of_tendsto_of_le_of_le|theorem squeeze_zero|theorem squeeze_zero\x27|cdf_expMeasure_eq','.lake/packages/mathlib/Mathlib/Topology','.lake/packages/mathlib/Mathlib/Probability/Distributions/Exponential.lean']))
queries.append(search('compatible-pinned-upstream',['-n','PDMP|stochastic.continu|piecewise.deterministic|first.jump','research-wiki/openai-math-2026-intake.json','research-wiki/openai-math-textbook-coverage.json','research-wiki/external-lean-libraries','-g','*.json','-g','*.md']))
queries.append(search('process-memory',['-n','ActualWaitCompositionElaboration|DependentPropStatementStaging','runs/substantive_discoveries.jsonl']))
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_advance as adv
parents=[('ASTIS-SA-20261010-PBPSActualPhysicalTimeMeasurability','AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhysicalTimeMeasurability.lean'),('ASTIS-SA-20261010-PBPSActualFiniteJumpRecursion','AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean')]
states=adv.current_advances()
# Exact event identities are read from current cell evidence, never guessed from dates.
cells=[]
for cid in ['ASTIS-SW-PBPS-actual-physical-time-measurability','ASTIS-SW-PBPS-actual-finite-jump-recursion','ASTIS-SW-PBPS-actual-hazard-clock','ASTIS-SW-PBPS-actual-harmonic-flow','ASTIS-SHARED-unit-exponential-product']:
 p=Path('research-wiki/frontier-cells')/(cid+'.json')
 if p.exists():
  c=json.loads(p.read_bytes());aid=c.get('evidence',{}).get('substantive_advance');s=states.get(aid,{})
  cells.append(dict(cell_id=cid,status=c['status'],advance_id=aid,advance_state=s.get('state'),parents=c.get('parents',[]),RAW_sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
save('current-cells82.json',cells)
modules=['ActualPhysicalTimeMeasurability','ActualFiniteJumpRecursion','ActualHazardClock','ActualHarmonicFlow']
files=['AutoSamplingTheory/ExampleCases/ProximalBPS/'+m+'.lean' for m in modules]+['AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean']
rows=[]
for p in files:
 b=Path(p).read_bytes();rows.append(dict(path=p,RAW_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b)))
packet=subprocess.run([sys.executable,'-X','utf8','tools/astis_publication.py','packet','--cell','ASTIS-SW-PBPS-actual-physical-time-measurability'],capture_output=True)
(out/'actual80.packet.snapshot.json').write_bytes(packet.stdout);(out/'actual80.packet.stderr.log').write_bytes(packet.stderr);assert packet.returncode==0
save('reuse-decision82.json',dict(status='RETRIEVAL_NO_PROOF_CREDIT',queries=queries,current_cells=cells,exact_parent_modules=rows,decision='adapt_existing',new_canonical_shared_declarations=[],reason='Construct source-specific actual small-time probability consumer. Generic probability monotonicity/complement, pushforward, continuity and squeeze are existing pinned Mathlib floors; no new shared copy or assumed coupling certificate.',consumer='arXiv2609.06905v1 A1.Ex22 actual strong-continuity ingredient; global invariance/L2 semigroup remain OPEN',process_memory_ids=['ASTIS-DISC-20261010-ActualWaitCompositionElaboration','ASTIS-DISC-20261009-DependentPropStatementStaging'],standing_instruction=False,control_plane_math_authority=False,statement_seal='Pending independent exact header reviews',proof_started=False))
print(json.dumps(dict(queries=queries,current_cells=cells),ensure_ascii=False,indent=2))
