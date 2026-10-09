from pathlib import Path
import hashlib,json
old=Path('.astis/pbps-corrector71');new=Path('.astis/pbps-perturbation72')
replacements=[('pbps-actual-corrector-change71','pbps-b4-corrector-perturbation72'),('pbps-corrector71','pbps-perturbation72'),('ActualCorrectorChange.actual_corrector_change','ActualCorrectorPerturbation.actual_corrector_perturbation'),('ActualCorrectorChange','ActualCorrectorPerturbation'),('actual-corrector-change','actual-corrector-perturbation'),('foreground-integration71.py','foreground72.py'),('integration71','integration72'),('visual71','visual72'),('mandatory71','mandatory72'),('small71','small72'),('final71','final72')]
rows=[]
for name in ['small-gates71.py','final-gates71.py','inspect-cdp71.mjs','inspect-copy71.mjs','run-browser71.py','python-regression71.py']:
 p=old/name;s=p.read_text(encoding='utf8')
 for a,b in replacements:s=s.replace(a,b)
 if name=='final-gates71.py':
  s=s.replace("('site-check-final'", "('graph-check-generic-final',['tools/astis_publication.py','graph-check','--cell','ASTIS-SW-PBPS-hilbert-corrector-perturbation']),('site-check-final'",1)
 if name in ['inspect-cdp71.mjs','inspect-copy71.mjs']:
  start=s.index(' const pages=');end=s.index(';\n for(const [label,rel,selector] of pages)',start)
  if name=='inspect-cdp71.mjs':
   replacement=''' const plan=JSON.parse(fs.readFileSync('runs/20261007-companion-priority/pbps-b4-corrector-perturbation72/publication-plan.json','utf8'));
 const pages=[];
 for(const [i,slug] of plan.slugs.entries()){
  const unit=JSON.parse(fs.readFileSync(`website/content/declaration_lessons/${slug}.json`,'utf8')).units[0];
  pages.push([`unit${i}-statement`,'example-cases/samplewiki/companions/proximal-bouncy-particle.html',`document.getElementById('${slug}')`]);
  for(let j=0;j<unit.steps.length;j++)pages.push([`unit${i}-proof-${j+1}`,'example-cases/samplewiki/companions/proximal-bouncy-particle.html',`document.getElementById('${slug}').querySelectorAll(".proof-reader-step")[${j}]`]);
 }
 pages.push(['branch-actual-consumer','lean-foundations.html?view=lean&focus=decl%3AAutoSamplingTheory.ExampleCases.ProximalBPS.ActualCorrectorPerturbation.actual_corrector_perturbation',"document.querySelector('[data-underlying-lean-graph]')"])'''
  else:
   replacement=''' const plan=JSON.parse(fs.readFileSync('runs/20261007-companion-priority/pbps-b4-corrector-perturbation72/publication-plan.json','utf8'));
 const pages=plan.slugs.map((slug,i)=>[`unit${i}-copy-and-download`,'example-cases/samplewiki/companions/proximal-bouncy-particle.html',`document.getElementById('${slug}')`])'''
  s=s[:start]+replacement+s[end:]
 dest=new/name.replace('71.','72.');assert not dest.exists(),dest;dest.write_text(s,encoding='utf8',newline='\n')
 rows.append(dict(source=p.as_posix(),source_RAW_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),adapted=dest.as_posix(),adapted_RAW_sha256=hashlib.sha256(dest.read_bytes()).hexdigest()))
dest=new/'integration-helper-adaptations72.json';assert not dest.exists()
dest.write_text(json.dumps(dict(status='TARGET_PATH_ADAPTATIONS_AND_DYNAMIC_TWO_UNIT_READER_LIST_ONLY',files=rows,canonical_scripts_changed=False,source_math_unchanged=True),indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS prepared72 integration helpers; current6+4 steps/two cells dynamic; no gates run or canonical writes.')
