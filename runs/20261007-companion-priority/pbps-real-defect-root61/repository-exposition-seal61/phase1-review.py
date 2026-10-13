from common import *
import html,re
from html.parser import HTMLParser
from urllib.parse import unquote,urlparse
class Node:
 def __init__(self,tag,attrs=None): self.tag=tag; self.attrs=dict(attrs or []); self.children=[]
 def text(self): return ''.join(x if isinstance(x,str) else x.text() for x in self.children)
 def all(self):
  yield self
  for x in self.children:
   if isinstance(x,Node): yield from x.all()
class Parser(HTMLParser):
 def __init__(self): super().__init__(convert_charrefs=True); self.root=Node('ROOT'); self.stack=[self.root]
 def handle_starttag(self,tag,attrs):
  n=Node(tag,attrs); self.stack[-1].children.append(n)
  if tag not in ['area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr']: self.stack.append(n)
 def handle_endtag(self,tag):
  for i in range(len(self.stack)-1,0,-1):
   if self.stack[i].tag==tag: self.stack=self.stack[:i]; break
 def handle_data(self,data): self.stack[-1].children.append(data)
phase=J(P/'phase1.inputs.json'); pairs=phase['qualified_original_snapshot_pairs']; frozen={r['original']['path']:r['exact_raw_snapshot']['path'] for r in pairs}
def read(p): return path(frozen[path(p).as_posix()]).read_text(encoding='utf8')
for row in pairs: matches(row['original'],row['exact_raw_snapshot']['path']); matches(row['exact_raw_snapshot'])
page=ROOT/'_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html'; parser=Parser(); parser.feed(read(page)); tree=parser.root
plan=J(R/'publication-plan.json'); results=[]; additional=[]
for i,decl in enumerate(plan['mathematical_declarations']):
 article=next(n for n in tree.all() if n.tag=='article' and n.attrs.get('data-authored-declaration')==decl)
 lesson=json.loads(read(ROOT/f"website/content/declaration_lessons/{plan['slugs'][i]}.json"))['units'][0]
 assert lesson['declaration']==decl and len(lesson['steps'])==[6,3][i]
 code_source=read(path(J(R/'math-freeze.json')['inputs'][i]['path'])).replace('\r\n','\n'); short=decl.rsplit('.',1)[1]; start=code_source.index('theorem '+short); end=code_source.index('\n\nend',start); exact_decl=code_source[start:end].strip(); statement=exact_decl.split(':= by')[0].strip()
 details=[n for n in article.all() if n.tag=='details']; code_checks=[]
 for kind,expected in [('statement',statement),('proof',code_source[start:].strip())]:
  d=next(n for n in details if 'inline-lean-'+kind in n.attrs.get('class','').split())
  assert 'open' not in d.attrs
  code=next(n for n in d.all() if n.tag=='code' and n.attrs.get('class')=='language-lean').text().replace('\r\n','\n').strip()
  if code!=expected and not (P/'phase1-code-equality.negative.json').exists():
   import difflib
   W(P/'phase1-code-equality.negative.json',dict(status='EXACT_DISPLAY_CODE_COMPARISON_NEGATIVE',declaration=decl,kind=kind,expected=expected,actual=code,diff=list(difflib.unified_diff(expected.splitlines(),code.splitlines()))))
  assert code==expected,(i,kind,code[:100],expected[:100])
  buttons=[n for n in d.all() if n.tag=='button' and 'data-lean-copy' in n.attrs]; assert len(buttons)==1
  links=[n.attrs['href'] for n in d.all() if n.tag=='a' and n.attrs.get('href')]
  dl=next(x for x in links if '/downloads/lean/' in x); module=next(x for x in links if '/modules/' in x)
  for link in [dl,module]:
   target=(page.parent/unquote(urlparse(link).path)).resolve(); assert target.is_relative_to(ROOT/'_site') and target.exists(); additional.append(snap(target,100+len(additional)))
  downloaded=(page.parent/unquote(urlparse(dl).path)).resolve().read_bytes().replace(b'\r\n',b'\n'); assert downloaded==code_source.encode()
  if kind=='proof': assert code.startswith(exact_decl)
  code_checks.append(dict(kind=kind,closed_by_default=True,complete_exact_LF_code_sha256=H(code.encode()),exact_declaration_body_preserved=True,source_tail_context='Proof display includes original namespace end and #print controls; exact source suffix, not a standalone declaration-only copy' if kind=='proof' else 'Exact complete sealed theorem type',copy_button=True,download_link=dl,module_context_link=module,download_exact_LF_source=True))
 stepdetails=[n for n in details if any(isinstance(x,Node) and x.tag=='summary' and x.text().strip()=='Corresponding Lean step' for x in n.children)]
 if len(stepdetails)!=[6,3][i] and not (P/'phase1-step-reader.negative.json').exists():
  W(P/'phase1-step-reader.negative.json',dict(declaration=decl,details_attributes=[n.attrs for n in details],failure='Reader step class selector mismatch'))
 assert len(stepdetails)==[6,3][i] and all('open' not in n.attrs for n in stepdetails)
 assert lesson['statement'] in article.text() and lesson['boundary'] in article.text()
 results.append(dict(declaration=decl,formula_step_count=len(lesson['steps']),full_statement_present=True,complete_typed_conditions_present=True,source_scope_boundary_present=True,exact_statement_and_declaration_proof=code_checks,all_corresponding_step_Lean_closed=True,formula_steps=[dict(title=s.get('title'),formula=s.get('formula')) for s in lesson['steps']]))
js=read(ROOT/'_site/assets/site.js'); assert 'data-lean-copy' in js and 'clipboard' in js
captures=json.loads(read(ROOT/'.astis/pbps-real-defect-root61/visual61-cdp/capture.json')); assert len(captures['records'])==8 and captures['ownedBrowserExit']['code']==0
observations=[]
for r in captures['records']:
 inspect=json.loads(read(ROOT/'.astis/pbps-real-defect-root61/visual61-cdp'/ (r['label']+'.inspect.json'))); assert inspect['url']==r['url'] and inspect['bodyVisibility']=='visible' and inspect['bodyDisplay']=='block'
 if r['label'].startswith('branch-'): note='Actual declaration card and focused branch visible; tall/dense global layout, long labels. Solid module/import ownership separate from dashed incomplete name-reference scans; consumer scanner LogConcaveOn.prod is not credited as a compiled proof dependency.'
 else: note='Actual source statement/formulas and explanatory proof visible; corresponding and full statement/proof Lean details begin folded. Inline prose math and repeated statement/assumption metadata remain dense reader debt; displayed formulas readable in actual capture.'
 observations.append(dict(label=r['label'],PNG_viewed_independently=True,DOM_frozen_and_verified=True,observation=note))
W(P/'phase1.additional-links.json',dict(count=len(additional),qualified_original_snapshot_pairs=additional,scope='Exact displayed download/module links only; no whole-site scan'))
W(P/'phase1.exposition.json',dict(status='PHASE1_SCOPED_EXPOSITION_CHECKS_PASS_PENDING_FINAL_COMMIT',actual_reviewer_PID=os.getpid(),science_commit=SCI,input_manifest=pin(P/'phase1.inputs.json'),additional_links=pin(P/'phase1.additional-links.json'),declarations=results,captures=observations,total_viewed_PNG=8,total_formula_steps=9,copy_actions='Static actual copy control/code association and site.js clipboard wiring checked; no new browser or interactive clipboard operation',debts=['Full statements repeated in publication assumptions and lesson; dense plain inline math persists.', 'Graph scene tall/dense with long wrapped declaration labels and incomplete dashed references; no exhaustive proof-implication export.', 'No whole chapter/paper Exposition Seal, PURIFIED/main/live/Goal admission.'],remaining='Exact integration/admin inputs/gates/current graph digest/module inventory PHASE2 pending; mathematical acceptance already independent exact-science61 unchanged',no_compiler_or_generator=True))
print('PHASE1_EXPOSITION_PASS','8 actualPNG','6+3 formula steps','complete exact code/download equality',len(additional),'qualified link snapshots')
