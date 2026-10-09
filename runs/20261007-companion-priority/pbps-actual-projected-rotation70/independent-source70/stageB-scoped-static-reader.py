import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os,re
from html.parser import HTMLParser
O=pathlib.Path(__file__).resolve().parent; ROOT=pathlib.Path('E:/Samplinglib')
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'website/scripts')]
import astis_site as base,inline_lean,declaration_lessons
paths=[ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS'/n for n in ('ActualProjectedRotation.lean','ReflectionIntertwining.lean','GaussianReflection.lean')]
snaps=['current70.source_body.exactraw.lean','parent69.ReflectionIntertwining.exactraw.lean','parent.GaussianReflection.exactraw.lean']
assert all(p.read_bytes()==(O/s).read_bytes() for p,s in zip(paths,snaps))
for p,s in [('tools/astis_site.py','reader.astis_site.exactraw.py'),('website/scripts/declaration_lessons.py','reader.declaration_lessons.exactraw.py'),('website/scripts/inline_lean.py','current70.inline_lean.exactraw.py')]:
 assert (ROOT/p).read_bytes()==(O/s).read_bytes()
base.project_lean_paths=lambda:paths
base._ACTIVE_GIT=base.GitContext('','','','',False,False,set())
mods,decls=base.scan_project_sources(); base._SOURCE_BY_NAME={d.full_name:d for d in decls}; inline_lean.declarations.cache_clear()
u=json.loads((O/'current70.lesson.exactraw.json').read_bytes())['units'][0]
name=u['declaration']; helper=u['helpers'][0]
assert helper==name.rsplit('.',1)[0]+'.actual_projected_rotation_statement'
assert base._SOURCE_BY_NAME[helper].kind=='def'
literal=base._SOURCE_BY_NAME[helper].source_text
expected='\n'.join((O/'current70.source_body.exactraw.lean').read_text(encoding='utf-8').splitlines()[17:134]).rstrip()
assert literal==expected
html=declaration_lessons.render_unit(u,'lessons/scoped-source70.html')
(O/'stageB.scoped-static-reader.html').write_text(html,encoding='utf-8',newline='\n')
class P(HTMLParser):
 def __init__(self):super().__init__();self.panels=[];self.details=[];self.steps=0
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='details':
   self.details.append(a)
   if 'data-inline-lean' in a:self.panels.append(a['data-inline-lean'])
  if t=='div' and a.get('class')=='proof-reader-step':self.steps+=1
p=P();p.feed(html)
assert p.panels==[name,name,helper]
assert all('open' not in x for x in p.details)
assert p.steps==8 and html.count('<summary>Corresponding Lean step</summary>')==8
assert base.code_html(literal) in html
assert all(base.code_html(s['lean']) in html for s in u['steps'])
assert 'Full Lean proposition (definition)' in html
assert 'It supplies no mathematical proof or additional hypothesis' in html
assert all('\\\\' not in s['formula'] for s in u['steps'])
result={'schema':'independent-source70-scoped-static-reader-v1','actual_pid':os.getpid(),'scope':'Only three exact current modules, one current lesson, and current renderer/scanner functions; no site build, full repository scan, browser, visual/live or Exposition Seal credit. Git context explicitly blank local-preview mock; no Git calls.','modules':[str(p.relative_to(ROOT)) for p in paths],'scanner_full_private_identity':helper,'literal_kind':'def','literal_exact_lines':[18,133],'literal_complete_exact':True,'inline_panel_identities':p.panels,'all_details_initially_closed':True,'eight_exact_adjacent_BODY_panels':True,'literal_adjacent_nested_with_public_proof':True,'literal_nonprovider_label_and_explanation':True,'all_eight_formulas_single_TeX_backslashes':True,'artifact':'stageB.scoped-static-reader.html','artifact_RAW_sha256':hashlib.sha256(html.encode()).hexdigest(),'full_browser_check_run':False,'canonical_writes':False}
(O/'stageB.scoped-static-reader.checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(result,ensure_ascii=False))
