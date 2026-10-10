from pathlib import Path
import subprocess,json,hashlib,datetime
r=Path(__file__).parent;rows=[];sha=lambda b:hashlib.sha256(b).hexdigest()
queries=[
 ('local',['rg','-n','conditional.*survival|survival.*conditional|next_wait_survival','AutoSamplingTheory/ExampleCases/ProximalBPS','AutoSamplingTheory/TechnicalLemmas/Probability','-g','*.lean']),
 ('frontiers',['rg','-l','conditional.*survival|history.*tail','research-wiki/frontier-cells','-g','*.json']),
 ('fixed-mathlib',['rg','-n','theorem (prod_apply|prod_apply_symm|lintegral_map|lintegral_prod)|map_prod_map|ofReal_measureReal|measureReal_def','.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Prod.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Lebesgue/Map.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Real.lean']),
 ('upstream',['rg','-n','conditional.*survival|random.hazard|next.wait|head.tail','research-wiki/external-lean-libraries','-g','*.md']),
 ('process-memory',['rg','-l','conditional.*survival|random.hazard|physical.time.*clock','runs/substantive_discoveries.jsonl']),
]
for label,argv in queries:
 q=subprocess.run(argv,capture_output=True);assert q.returncode in [0,1],q.stderr.decode(errors='replace')
 pins={}
 for kind,b in [('stdout',q.stdout),('stderr',q.stderr)]:
  p=r/(label+'.retrieval.'+kind+'.log');assert not p.exists();p.write_bytes(b);pins[kind]=dict(path=p.as_posix(),raw_sha256=sha(b),bytes=len(b))
 rows.append(dict(label=label,argv=argv,exit_code=q.returncode,**pins))
parents=['AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryTailLaw.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHazardClock.lean','AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean']
data=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),checks=rows,actual_compiled_parent_files=[dict(path=p,raw_sha256=sha(Path(p).read_bytes())) for p in parents],decision='adapt_existing: use actual87 joint history/tail law and actual75 joint measurable clock/deterministic survival. Fixed Mathlib supplies generic map/product integration. No new generic wrapper, duplicate independent-tail lemma or external port.',shared_floor_classification='adapt',canonical_shared_substrate='Fixed Mathlib Measure.prod_apply/lintegral_map; actual77 UnitExponentialProduct is unchanged canonical clock substrate.',new_shared_declarations=[],known_compiled_consumers=[],planned_consumers=['S87-I5/G86-13 finite-event law iteration','G86-14 final no-event survival factor'],compatibility='Lean4.33.0, Mathlib db584cd6d46c92f209a44c0f1c829460d327499d Apache2.0; reviewed SLT remains Lean4.32.0 and cannot be added as dependency. No upstream theorem/route imported.',scope='Retrieval only; no sealed new statement/proof/closure yet.')
p=r/'retrieval88.json';assert not p.exists();p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf8',newline='\n');print('Saved reuse queries and exact compiled parent RAWs; no closure credit.')
