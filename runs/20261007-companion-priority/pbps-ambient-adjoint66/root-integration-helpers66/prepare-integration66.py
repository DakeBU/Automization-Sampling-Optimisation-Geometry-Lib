from pathlib import Path
import json,re
old=Path('.astis/pbps-polar65');out=Path('.astis/pbps-ambient-adjoint66')
def write(name,s):
 p=out/name;assert not p.exists(),p;p.write_text(s,encoding='utf-8',newline='\n')
def common(s):
 return s.replace('pbps-polar65','pbps-ambient-adjoint66').replace('integration65','integration66').replace('visual65','visual66').replace('mandatory65','mandatory66').replace('cache65','cache66')
s=common((old/'integration-gate65.py').read_text())
s=s.replace('PolarIsometry.lean','AmbientAdjointCorrector.lean').replace('ProximalBPSPolarIsometry.lean','ProximalBPSAmbientAdjointCorrector.lean')
s=s.replace('ASTIS-SW-PBPS-actual-polar-isometry','ASTIS-SW-PBPS-ambient-adjoint-corrector').replace('pbps-actual-polar-isometry.json','pbps-ambient-adjoint-corrector.json').replace('ASTIS-RT-20261009-PBPSActualPolarIsometry','ASTIS-RT-20261009-PBPSAmbientAdjointCorrector')
write('integration-gate66.py',s)
s=common((old/'cache-generated-cards65.py').read_text()).replace('kept_one_enriched65_card','kept_one_enriched66_card');write('cache-generated-cards66.py',s)
s=common((old/'preserve-generated-context65.py').read_text())
start=s.index('for module,layer,summary in [');end=s.index(']:\n item=',start)
s=s[:start]+"for module,layer,summary in [('AutoSamplingTheory.ExampleCases.ProximalBPS.AmbientAdjointCorrector','SampleWiki paper route','Original C2/two Hessians/positive capped eta produce SAME actual laws/operators/centered root/inverse and polar isometry. Canonical R:L2(J)->kerP, all-vector ambient adjoint identity and actual globally centered input decomposition; genuine corrector norm budget. Two literal private Prop representations add no premise/provider. No full B20/B21,dynamics/main/cost/composition,full Exposition/PURIFIED or whole-paper claim.')"+s[end:]
s=s.replace('Independent exact-science65','Independent exact-science66').replace('Bounded typed polar isometry and adjoint corrector only','Bounded ambient adjoint and globally centered corrector input geometry only').replace('one independently verified65 module card','one independently verified66 module card')
write('preserve-generated-context66.py',s)
slug='pbps-ambient-adjoint-corrector';decl='AutoSamplingTheory.ExampleCases.ProximalBPS.AmbientAdjointCorrector.actual_ambient_adjoint_centered_decomposition';rel='example-cases/samplewiki/companions/proximal-bouncy-particle.html';sel=f"document.getElementById('{slug}')"
for filename,target,copyprobe in [('inspect-cdp65.mjs','inspect-cdp66.mjs',False),('inspect-copy65.mjs','inspect-copy66.mjs',True)]:
 s=common((old/filename).read_text());start=s.index(' const pages=');end=s.index(';\n for(const [label,rel,selector]',start)
 if copyprobe:pages=[['actual-copy-and-download',rel,sel]]
 else:pages=[['actual-statement',rel,sel]]+[[f'actual-proof-{i+1}',rel,sel+f'.querySelectorAll(".proof-reader-step")[{i}]'] for i in range(6)]+[['branch-consumer','lean-foundations.html?view=lean&focus=decl%3A'+decl,"document.querySelector('[data-underlying-lean-graph]')"]]
 s=s[:start]+' const pages='+json.dumps(pages)+s[end:]
 s=re.sub(r'  const name=.+?;\n','  const name='+json.dumps(decl)+';\n',s,count=1)
 write(target,s)
print('Prepared foreground66 integration helpers and eight bounded render probes; no canonical writes or gates executed.')
