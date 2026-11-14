from pathlib import Path
import sys,json,hashlib,subprocess,re,html,shutil,os
from html.parser import HTMLParser
r=Path.cwd();d=Path(__file__).resolve().parent;c='8ee639d3aced826aa5b4e39fa6f8bedd3b830327';sys.path[:0]=[str(r/'tools'),str(r/'website/scripts')]
import astis_site as base, declaration_lessons as lessons, inline_lean,astis_publication as pub,astis
paths=['AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumTargetLaw.lean','Tests/GaussianComplexityFixedSpectrumTargetLaw.lean','AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumAdmissibility.lean','AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumGaussianMoments.lean'];target=paths[0];test=paths[1]
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==c
for p in paths:assert (r/p).read_bytes()==(d/'candidate'/p).read_bytes()
base.project_lean_paths=lambda:[r/p for p in paths]
mods,decls=base.scan_project_sources();known={a.full_name:a for a in decls};base._SOURCE_BY_NAME=known;base._ALL_MODULES=mods
base._ACTIVE_GIT=base.GitContext(c,'immutable-candidate-static-verification','','',False,False,set())
base._ACTIVE_GATE=base.GateEvidence(False,False,c,'','',[],'Bounded independent static fixture; no whole repository gate authority.')
unit=json.loads((d/'candidate/website/content/declaration_lessons/huanjian-fixed-spectrum-target-law.json').read_text())['units'][0];name=unit['declaration'];page=lessons.lesson_path(name);out=d/'static';out.mkdir(exist_ok=True)
# Load only this exact publication, the minimal field needed from its cell, and
# the code/source/exposition binding fields of its draft audit. No prior verdict read.
extra=['website/content/publications/huanjian-fixed-spectrum-target-law.json','research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-target-law.json','research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-target-law.json']
for p in extra:
 b=subprocess.check_output(['git','show',c+':'+p]);assert (r/p).read_bytes()==b;q=d/'candidate'/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
item=json.loads((d/'candidate'/extra[0]).read_text())['items'][0];binding=item['bindings'][0];cell_raw=json.loads((d/'candidate'/extra[1]).read_text());cell={k:cell_raw[k] for k in ['cell_id','shared_floor_audit']};raw_audit=json.loads((d/'candidate'/extra[2]).read_text());audit=raw_audit.get('audits',[raw_audit])[0] if isinstance(raw_audit,dict) else raw_audit[0]
audit={k:audit[k] for k in ['id','lean','publication_binding_sha256','publication_context','state'] if k in audit}
data={'declarations':known,'lessons':{name:unit},'cells':{cell['cell_id']:cell},'audits':{audit['id']:audit}}
errors=pub.validate([item],data,strict_names=None)
publication={'scope':'Only new public producer binding; reviewed=False; no source-review acceptance claimed','reviewed':False,'errors':errors,'binding_sha256':pub.binding_digest(item,binding,data),'audit_binding_sha256':audit.get('publication_binding_sha256')}
(d/'publication.bounded.json').write_text(json.dumps(publication,indent=2)+'\n')
assert not errors,errors
hits=[]
for p in paths[:2]:
 source=(d/'candidate'/p).read_text();clean=astis.strip_lean_comments_and_strings(source)
 for i,line in enumerate(clean.splitlines(),1):
  if astis.FORBIDDEN_REGEX.search(line):hits.append({'file':p,'line':i,'code':line})
(d/'fake-closure.bounded.json').write_text(json.dumps({'scope':paths[:2],'hits':hits},indent=2)+'\n');assert not hits
# Render the unchanged authored lesson renderer with an exact source-assumption
# comparison table, without importing a semantic verdict into this review.
rows=''.join('<tr>'+''.join('<td>'+html.escape(x[k])+'</td>' for k in ['source','lean','classification','reason'])+'</tr>' for x in binding['assumption_deltas'])
comparison='<section data-source-comparison="'+name+'"><h3>Source assumptions versus formal assumptions</h3><table>'+rows+'</table><p>'+html.escape(binding['boundary'])+'</p></section>'
body=lessons.render_unit(unit,page,source_comparison=comparison);rendered=base.page(unit['title'],page,body)
q=out/page;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(rendered)
# Existing page is used solely as a theme fixture by the unchanged source exporter.
fixture=r/'_site/textbook/index.html'
if fixture.exists():
 q=out/'textbook/index.html';q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(fixture.read_bytes());(d/'theme-fixture.json').write_text(json.dumps({'source':str(fixture),'sha256':hashlib.sha256(fixture.read_bytes()).hexdigest(),'scope':'Theme fixture only; no canonical site, graph, browser, desktop, mobile or pixel authority.'},indent=2)+'\n')
lessons.export_sources(out,[unit])
for module in mods:
 if module.source_file==target:
  rel='modules/'+base.slugify(module.name)+'.html';q=out/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(base.render_source_module(module,[]))
for p in paths[:2]:
 q=out/'downloads/lean'/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes((d/'candidate'/p).read_bytes())
class Node:
 def __init__(self,t,a,parent=None):self.tag=t;self.attrs=dict(a);self.parent=parent;self.children=[];self.text=''
 def all(self,t=None):
  ans=[]
  for a in self.children:
   if t is None or a.tag==t:ans.append(a)
   ans+=a.all(t)
  return ans
 def textall(self):return self.text+''.join(x.textall() for x in self.children)
class Parse(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.root=Node('root',[]);self.stack=[self.root]
 def handle_starttag(self,t,a):
  n=Node(t,a,self.stack[-1]);self.stack[-1].children.append(n)
  if t not in ['meta','link','br','hr','img','input']:self.stack.append(n)
 def handle_endtag(self,t):
  for i in range(len(self.stack)-1,0,-1):
   if self.stack[i].tag==t:self.stack=self.stack[:i];break
 def handle_data(self,s):self.stack[-1].text+=s
parser=Parse();parser.feed(rendered);root=parser.root;article=next(n for n in root.all('article') if n.attrs.get('data-authored-declaration')==name)
classes=lambda n:n.attrs.get('class','').split();details=article.all('details');proofsteps=[n for n in details if 'proof-reader-step' in classes(n)];pres=article.all('pre');codes=[n.textall() for n in pres];T=(d/'candidate'/test).read_text();P=(d/'candidate'/target).read_text();statement,_=inline_lean.split_statement(inline_lean.display_source(known[name].source_text));exact=inline_lean.display_source(known[name].source_text)
checks={'concise_claim_exact':any(n.attrs.get('class')=='reader-claim' and n.textall()==unit['statement'] for n in article.all('p')),'six_literal_steps':len(proofsteps)==6,'all_disclosures_initially_closed':all('open' not in n.attrs for n in details),'assumptions_fold_closed':any('assumption-ledger' in classes(n) and 'open' not in n.attrs for n in details),'exact_public_statement_adjacent':any(n.attrs.get('data-inline-lean')==name and 'inline-lean-statement' in classes(n) and statement in [p.textall() for p in n.all('pre')] and n.parent.attrs.get('class')=='reader-first-pass' for n in details),'exact_public_proof':exact in codes,'full3593B_Test_at_step6':unit['steps'][5]['lean'].encode()==(d/'candidate'/test).read_bytes() and T in [x.textall() for x in proofsteps[5].all('pre')],'step_leans_literal':all(s['lean'] in [p.textall() for p in n.all('pre')] for s,n in zip(unit['steps'],proofsteps)),'first4_steps_contained_P':all(s['lean'] in P for s in unit['steps'][:4]),'step5_contained_T':unit['steps'][4]['lean'] in T,'source_context_Link_L16':any(n.attrs.get('href','').endswith('data/lesson-sources/'+test+'.html#L16') for n in article.all('a')),'boundary_exact':any(unit['boundary'] in n.textall() for n in details if 'boundary-ledger' in classes(n)),'actual_ASTIS_parents_present':all(dep in rendered for dep in unit['astis_dependencies']),'download_P_exact':(out/'downloads/lean'/target).read_bytes()==(d/'candidate'/target).read_bytes(),'download_T_exact':(out/'downloads/lean'/test).read_bytes()==(d/'candidate'/test).read_bytes(),'public_context_complete_source':(out/'modules'/ (base.slugify(known[name].module)+'.html')).is_file()}
source=(out/'data/lesson-sources'/(test+'.html')).read_text();ps=Parse();ps.feed(source);spans=[n for n in ps.root.all('span') if re.fullmatch('L[0-9]+',n.attrs.get('id',''))];checks['exported_Test_every_line_exact']=len(spans)==len(T.splitlines()) and all(n.textall()==line for n,line in zip(spans,T.splitlines()));checks['exported_Test_L16_private_statement']=any(n.attrs.get('id')=='L16' and n.textall().startswith('private theorem actual_target_gaussian_norm_mean') for n in spans)
context_path=out/'modules'/(base.slugify(known[name].module)+'.html');context=Parse();context.feed(context_path.read_text());context_section=next(n for n in context.root.all('section') if n.attrs.get('id')=='complete-module-source');checks['public_context_exact_full_P']=P in [n.textall() for n in context_section.all('pre')];checks['public_context_link_exists']=any(n.attrs.get('href','').endswith('modules/'+base.slugify(known[name].module)+'.html#complete-module-source') for n in article.all('a'));checks['step_prose_formula_literal']=all(lessons.inline_text(step['text']) in rendered and html.escape(step['formula']) in rendered for step in unit['steps']);checks['all_assumptions_literal']=all(lessons.inline_text(a) in rendered for a in unit['assumptions'])
report={'candidate':c,'lesson_sha256':hashlib.sha256((d/'candidate/website/content/declaration_lessons/huanjian-fixed-spectrum-target-law.json').read_bytes()).hexdigest(),'rendered_page':str(out/page),'checks':checks,'all_pass':all(checks.values()),'scope':'Independent static DOM/exact-byte evidence only. No browser/OS/desktop/mobile/pixel/global graph/global gate authority; source fidelity independently reviewed elsewhere.'};(d/'reader.static.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'publication':publication,'fake_closure_hits':hits,'reader':report},indent=2));assert report['all_pass'],checks
for p in ['tools/astis_site.py','website/scripts/declaration_lessons.py','website/scripts/inline_lean.py','website/scripts/source_lineage.py','website/scripts/library_shelves.py','website/scripts/formalization_progress.py','tools/astis_publication.py']:
 b=(r/p).read_bytes();assert b==subprocess.check_output(['git','show',c+':'+p]);q=d/'renderer-sources'/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
