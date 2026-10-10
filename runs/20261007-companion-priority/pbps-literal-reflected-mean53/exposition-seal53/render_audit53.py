import sys,json,re,html,hashlib
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.dont_write_bytecode=True
root=Path(r'E:\Samplinglib');role=root/'runs/20261007-companion-priority/pbps-literal-reflected-mean53/exposition-seal53'
sys.path.insert(0,str(root/'tools'));sys.path.insert(0,str(root/'website/scripts'))
import inline_lean
name='AutoSamplingTheory.ExampleCases.ProximalBPS.LiteralReflectedMean.reflected_gibbs_mean_c1'
p=root/'_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html';s=p.read_text(encoding='utf-8');decl=inline_lean.declarations()[name]
exact=inline_lean.display_source(decl.source_text);signature,_=inline_lean.split_statement(exact)
rows=[]
for role_name,expected in [('statement',signature),('proof',exact)]:
 pattern=r'<details class="inline-lean inline-lean-'+role_name+r'" data-inline-lean="'+re.escape(name)+r'"[^>]*>(.*?)</details>'
 m=re.search(pattern,s,re.S);assert m
 code=re.search(r'<pre[^>]*>(.*?)</pre>',m[1],re.S);assert code
 actual=html.unescape(re.sub(r'<[^>]*>','',code[1]));assert actual.strip()==expected.strip()
 hrefs=re.findall(r'href="([^"]+)"',m[1]); rows.append({'role':role_name,'initially_folded':True,'exact_current_extracted_lean_equals_rendered':True,'source_utf8_sha256':hashlib.sha256(expected.strip().encode()).hexdigest(),'rendered_utf8_sha256':hashlib.sha256(actual.strip().encode()).hexdigest(),'source_line':decl.source_line,'code_lines':len(expected.splitlines()),'context_hrefs':hrefs})
start=s.index('<section id="pbps-literal-reflected-mean"');article=s[start:];article=article[:article.index('</article>')+len('</article>')]
metadata={'page':p.relative_to(root).as_posix(),'inline_lean':rows,'six_formula_step_count':article.count('class="proof-reader-step"'),'rendered_initially_closed_details':len(re.findall(r'<details\b(?![^>]*\bopen\b)',article)),'source_attribution_present':'ASTIS-authored source-specific analytic integration' in article,'source_comparison_present':'data-source-comparison="'+name+'"' in article,'scope_exclusions_present':all(t in article for t in ['Actual Tf','rough B.13','expected query costs']),'source_citation_hrefs':sorted(set(html.unescape(h) for h in re.findall(r'href="([^"]+)"',article) if '2609.06905' in h)),'download_or_context_entry_hrefs':rows[0]['context_hrefs'],'helper_source':{'path':'website/scripts/inline_lean.py','raw_sha256':hashlib.sha256((root/'website/scripts/inline_lean.py').read_bytes()).hexdigest()},'boundary':'Local metadata/exact-fold inspection only; links were not downloaded or externally opened; no physical-device/mobile/live/full-reader/PURIFIED conclusion.'}
assert metadata['six_formula_step_count']==6
(role/'render-binding53.json').write_bytes((json.dumps(metadata,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+'\n').encode())
print(json.dumps(metadata,ensure_ascii=False,indent=2))