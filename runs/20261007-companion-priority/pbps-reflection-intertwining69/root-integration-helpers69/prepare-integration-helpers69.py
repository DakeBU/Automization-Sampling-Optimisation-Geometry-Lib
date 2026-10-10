from pathlib import Path
import json,re
h=Path('.astis/pbps-sharp-energy68');newrun='pbps-reflection-intertwining69';slug='pbps-actual-reflection-intertwining';decl='AutoSamplingTheory.ExampleCases.ProximalBPS.ReflectionIntertwining.actual_reflection_intertwining'
for name in ['inspect-cdp68.mjs','inspect-copy68.mjs','preserve-integration-newlines68.py','cache-generated-cards68.py','preserve-generated-context68.py']:
 s=(h/name).read_text(encoding='utf-8')
 for a,b in [('runs/20261007-companion-priority/pbps-sharp-energy68','runs/20261007-companion-priority/'+newrun),('integration68','integration69'),('verification68','verification69'),('visual68','visual69'),('generated-card-cache68','generated-card-cache69'),('kept_two_enriched68_cards','kept_one_enriched69_card'),('Actual mandatory66','Actual mandatory69'),('science68','science69')]:s=s.replace(a,b)
 if name.startswith('inspect-'):
  rel='example-cases/samplewiki/companions/proximal-bouncy-particle.html';selector="document.getElementById('"+slug+"')"
  pages=[['unit0-copy-and-download',rel,selector]] if 'copy' in name else [['unit0-statement',rel,selector]]+[[f'unit0-proof-{j+1}',rel,selector+f'.querySelectorAll(".proof-reader-step")[{j}]'] for j in range(6)]+[['branch-actual-consumer','lean-foundations.html?view=lean&focus=decl%3A'+decl,"document.querySelector('[data-underlying-lean-graph]')"]]
  s=re.sub(r' const pages=\[.*?\];',lambda _: ' const pages='+json.dumps(pages)+';',s,count=1)
  s=re.sub(r'  const name=.*?;',lambda _: '  const name='+json.dumps(decl)+';',s,count=1)
 if name=='preserve-integration-newlines68.py':
  start=s.index('paths=');end=s.index('\nrecords=[]',start)
  s=s[:start]+"paths=['AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json']+['research-wiki/frontier-cells/'+x+'.json' for x in json.loads((r/'publication-plan.json').read_bytes())['active_cells']]"+s[end:]
 if name=='preserve-generated-context68.py':
  start=s.index('owned=');end=s.index('\ngraphpaths=',start)
  s=s[:start]+"owned={'AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl','runs/substantive_advances.jsonl','runs/substantive_discoveries.jsonl'}|{'research-wiki/frontier-cells/'+x+'.json' for x in plan['active_cells']}"+s[end:]
  s=s.replace("owned |= {'website/content/declaration_lessons/hilbert-sharp-quadratic-corrector-bound.json', 'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-HilbertSharpQuadraticCorrectorBound.json'}",'')
  start=s.index('for module,layer,summary in [');end=s.index(':\n item=next',start)
  modules=[('AutoSamplingTheory.ExampleCases.ProximalBPS.ReflectionIntertwining','SampleWiki paper route','Same original six callers and twelve actual witnesses give D=R U inclusion and V0*D=-A0V0* on all kerP. Same U is identified by exact AE pullback actions before consuming the ambient block identity. No ontoV, range restriction, extra regularity or sharp-energy68 dependency. Actual projected rotation/B21 corrector change, B4/H1/dynamics/main/errors/cost/composition remain open.')]
  s=s[:start]+'for module,layer,summary in '+repr(modules)+s[end:]
  s=s.replace('Independent exact-science68 verified','Independent exact-science69 verified').replace('Bounded sharp corrector energy and modified-energy equivalence only','Bounded actual full-micro reflection intertwining only').replace('two independently verified68 module cards','one independently verified69 module card')
 dest=h/name.replace('68','69');assert not dest.exists(),dest;dest.write_text(s,encoding='utf-8',newline='\n')
print('Prepared bounded69 integration/reader helpers only; no canonical mutation or acceptance.')
