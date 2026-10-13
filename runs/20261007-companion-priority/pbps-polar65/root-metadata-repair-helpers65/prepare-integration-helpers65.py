from pathlib import Path
import json,re
old=Path('.astis/pbps-centered-root64');out=Path('.astis/pbps-polar65')
def write(name,s):
 p=out/name;assert not p.exists(),p;p.write_text(s,encoding='utf-8',newline='\n')
def common(s):return s.replace('pbps-centered-root64','pbps-polar65').replace('integration64','integration65').replace('visual64','visual65').replace('mandatory64','mandatory65')
s=common((old/'integration-gate64.py').read_text());s=s.replace('CenteredRootOrderInverse.lean','PolarIsometry.lean').replace('ProximalBPSCenteredRootOrderInverse.lean','ProximalBPSPolarIsometry.lean')
s=s.replace('ASTIS-SW-PBPS-centered-root-order-inverse','ASTIS-SW-PBPS-actual-polar-isometry').replace('pbps-centered-root-order-inverse.json','pbps-actual-polar-isometry.json').replace('ASTIS-RT-20261009-PBPSCenteredRootOrderInverse','ASTIS-RT-20261009-PBPSActualPolarIsometry')
write('integration-gate65.py',s)
s=common((old/'cache-generated-cards64.py').read_text()).replace('cache64','cache65').replace('kept_two_enriched64_cards','kept_one_enriched65_card');write('cache-generated-cards65.py',s)
s=common((old/'preserve-generated-context64.py').read_text())
s=s.replace("'runs/substantive_advances.jsonl'","'runs/substantive_advances.jsonl','runs/substantive_discoveries.jsonl','research-wiki/frontier-cells/ASTIS-SHARED-l2-real-positive-square-order.json'")
start=s.index("for module,layer,summary in [");end=s.index("]:\n item=",start)
s=s[:start]+"for module,layer,summary in [('AutoSamplingTheory.ExampleCases.ProximalBPS.PolarIsometry','SampleWiki paper route','Original C2/two Hessians/positive capped eta produce SAME actual HP0 root/inverse and B0:HP0->kerP,V0=B0 Inv. B0=V0 Gamma0,V0*V0=I and all-vector norm preservation; genuine typed adjoint corrector/contraction/residual consumer. No onto,ambient-adjoint extraction,full Exposition/PURIFIED or whole-paper claim.')"+s[end:]
s=s.replace('Independent exact-science64','Independent exact-science65').replace('Bounded auxiliary square-order and actual centered root order/inverse only','Bounded typed polar isometry and adjoint corrector only').replace('two independently verified64 module cards','one independently verified65 module card')
write('preserve-generated-context65.py',s)
slug='pbps-actual-polar-isometry';decl='AutoSamplingTheory.ExampleCases.ProximalBPS.PolarIsometry.actual_centered_polar_isometry';rel='example-cases/samplewiki/companions/proximal-bouncy-particle.html';sel=f"document.getElementById('{slug}')"
for filename,target,copyprobe in [('inspect-cdp64.mjs','inspect-cdp65.mjs',False),('inspect-copy64.mjs','inspect-copy65.mjs',True)]:
 s=common((old/filename).read_text());start=s.index(' const pages=');end=s.index(';\n for(const [label,rel,selector]',start)
 if copyprobe:pages=[['actual-copy-and-download',rel,sel]]
 else:pages=[['actual-statement',rel,sel]]+[[f'actual-proof-{i+1}',rel,sel+f'.querySelectorAll(".proof-reader-step")[{i}]'] for i in range(5)]+[['branch-consumer','lean-foundations.html?view=lean&focus=decl%3A'+decl,"document.querySelector('[data-underlying-lean-graph]')"]]
 s=s[:start]+' const pages='+json.dumps(pages)+s[end:]
 s=re.sub(r"  const name=label==='branch-consumer'\?.+?;\n",'  const name='+json.dumps(decl)+';\n',s,count=1)
 write(target,s)
print('Prepared integration65 foreground wrapper,preservation/cache and bounded seven-capture/two-copy/two-download reader probes; not executed.')
