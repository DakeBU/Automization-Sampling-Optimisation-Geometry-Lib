"""Bounded exact renderer relocation audit; no site build/canonical writes."""
from pathlib import Path
from html.parser import HTMLParser
import ast,copy,datetime,hashlib,json,re,sys,types
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;B=O.parent/'reader-adjacency-repair86'
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(b),bytes=len(b))
def put(n,j):
 p=O/n;assert not p.exists(),n;p.write_bytes((json.dumps(j,ensure_ascii=False,indent=2)+'\n').encode());return pin(p)
proposal=B/'proposal.json';assert pin(proposal)['raw_sha256']=='07374a3f4cbcc4a1e075be66d1cc87fe3f84aba3390dec4a3435a9fc82e0fcda'
p=json.loads(proposal.read_bytes());before=R/p['before']['path'];after=R/p['after']['path'];diff=R/p['diff']['path']
for q,k in [(before,'before'),(after,'after'),(diff,'diff')]:assert pin(q)['raw_sha256']==p[k]['RAW_sha256'] and pin(q)['bytes']==p[k]['bytes']
canonical=R/'website/scripts/declaration_lessons.py';assert canonical.read_bytes()==before.read_bytes()
ab=ast.parse(before.read_bytes());aa=ast.parse(after.read_bytes())
def topnodes(tree):return {getattr(n,'name',f'node{k}'):ast.dump(n,include_attributes=False) for k,n in enumerate(tree.body)}
nb,na=topnodes(ab),topnodes(aa);assert nb.keys()==na.keys();changed=[k for k in nb if nb[k]!=na[k]];assert changed==['render_unit']
compile(before.read_bytes(),str(before),'exec');compile(after.read_bytes(),str(after),'exec')
sys.dont_write_bytecode=True;sys.path[:0]=[str(R/'tools'),str(R/'website/scripts')]
import astis_site as base
import inline_lean
candidate=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteFirstEventLaw.lean'
lesson=R/'website/content/declaration_lessons/pbps-actual-finite-first-event-law.json'
publication=R/'website/content/publications/pbps-actual-finite-first-event-law.json'
unit=json.loads(lesson.read_bytes())['units'][0]
# Exercise the real source scanner, bounded to one candidate module. No project-wide scan.
base.project_lean_paths=lambda:[candidate]
mods,decls=base.scan_project_sources();assert len(mods)==1
base._SOURCE_BY_NAME={d.full_name:d for d in decls}
# Dependencies are link-only fixture metadata; their source/proof bodies are not read.
for name in unit.get('astis_dependencies',[]):
 module,short=name.rsplit('.',1)
 base._SOURCE_BY_NAME[name]=base.SourceDeclaration(name,short,'theorem',module,module.replace('.','/')+'.lean',1,'','',short,False,[])
base._ACTIVE_GIT=types.SimpleNamespace(web_root='',commit='',commit_published=False,public_source_links=False,dirty_files=set())
inline_lean.declarations.cache_clear()
def load(source,name):
 m=types.ModuleType(name);m.__file__=str(canonical);exec(compile(source,str(canonical),'exec'),m.__dict__);return m
old=load(before.read_bytes(),'repair_before86');new=load(after.read_bytes(),'repair_proposed86')
oldhtml=old.render_unit(unit,'lessons/repair86-sample.html');newhtml=new.render_unit(unit,'lessons/repair86-sample.html')
class Node:
 def __init__(self,t,a,start,parent=None):self.tag=t;self.attrs=dict(a);self.start=start;self.end=None;self.parent=parent;self.children=[];self.parts=[]
 def cls(self,c):return c in self.attrs.get('class','').split()
class DOM(HTMLParser):
 def __init__(self,text):super().__init__(convert_charrefs=True);self.text=text;self.nodes=[];self.stack=[];self.offsets=[0];self.offsets.extend(m.end() for m in re.finditer('\n',text));self.feed(text)
 def pos(self):a,b=self.getpos();return self.offsets[a-1]+b
 def handle_starttag(self,t,a):
  n=Node(t,a,self.pos(),self.stack[-1] if self.stack else None);self.nodes.append(n)
  if n.parent:n.parent.children.append(n)
  if t not in {'br','hr','img','input','meta','link'}:self.stack.append(n)
 def handle_endtag(self,t):
  for k in range(len(self.stack)-1,-1,-1):
   if self.stack[k].tag==t:
    n=self.stack[k];n.end=self.text.find('>',self.pos())+1;self.stack=self.stack[:k];break
 def handle_data(self,d):
  for n in self.stack:n.parts.append(d)
 def byclass(self,c):return [n for n in self.nodes if n.cls(c)]
 def raw(self,n):return self.text[n.start:n.end]
 def code(self,n):return ''.join(next(q for q in self.nodes if q.tag=='code' and q.parent and q.parent.parent==n).parts)
d0,d1=DOM(oldhtml),DOM(newhtml)
stmt0=d0.byclass('inline-lean-statement');stmt1=d1.byclass('inline-lean-statement');assert len(stmt0)==len(stmt1)==1
assert d0.raw(stmt0[0])==d1.raw(stmt1[0])
section=next(n for n in d1.nodes if n.cls('reader-first-pass'));equation=next(n for n in section.children if n.cls('reader-main-equation'))
idx=section.children.index(equation);assert section.children[idx+1]==stmt1[0]
assert section.children[idx+2].tag=='h3' and ''.join(section.children[idx+2].parts)=='Proof roadmap'
assert section.children[idx+3].cls('proof-roadmap')
assert len(d0.byclass('proof-reader-step'))==len(d1.byclass('proof-reader-step'))==11
assert [d0.raw(n) for n in d0.byclass('proof-reader-step')]==[d1.raw(n) for n in d1.byclass('proof-reader-step')]
proof0=d0.byclass('inline-lean-proof');proof1=d1.byclass('inline-lean-proof');assert len(proof0)==len(proof1)==7
assert [d0.raw(n) for n in proof0]==[d1.raw(n) for n in proof1]
assert all('open' not in n.attrs for n in d1.nodes if n.tag=='details')
keys=[(n.attrs.get('data-inline-lean'),n.attrs.get('class')) for n in stmt1+proof1];assert len(keys)==len(set(keys))
main_decl=base._SOURCE_BY_NAME[unit['declaration']]
exact=inline_lean.display_source(main_decl.source_text);sig,body=inline_lean.split_statement(exact)
def code_under(dom,n):
 return ''.join(q.parts for q in []) if False else ''.join(next(q for q in dom.nodes if q.tag=='code' and q.start>n.start and q.end is not None and q.end<n.end).parts)
assert code_under(d1,stmt1[0])==sig
assert code_under(d1,proof1[0])==exact
assert body and ':= by' in body
mal=copy.deepcopy(unit);probe='<script id="repair-injection">window.BAD=1</script>'
for key in ['title','statement','formula','lean_statement','lean_proof']:mal[key]+=probe
mal['steps'][0]['text']+=probe;mal['steps'][0]['lean']+=probe
injected=new.render_unit(mal,'lessons/repair86-injection.html');assert probe not in injected
assert '&lt;script' in injected and not DOM(injected).byclass('repair-injection')
assert len([n for n in DOM(injected).nodes if n.tag=='script'])==0
pub=json.loads(publication.read_bytes());assert pub['items'][0]['statement']==unit['statement']
local_imports=[]
for m in list(sys.modules.values()):
 f=getattr(m,'__file__',None)
 if f:
  q=Path(f)
  try:rel=q.relative_to(R)
  except ValueError:continue
  if q.is_file() and q.suffix=='.py':local_imports.append(q)
local_imports=list(dict.fromkeys(local_imports))
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
checks={'before_after_syntax_compile_in_memory':'PASS','AST_changed_top_level_functions':changed,'same_exact_statement_disclosure_relocated':True,'statement_directly_after_math_formula_before_roadmap':True,'all_details_initially_closed':True,'proof_steps_unchanged':11,'full_proof_disclosures_unchanged':7,'no_duplicate_role_name_disclosures':True,'statement_code_matches_actual_scanner_signature':True,'full_proof_code_matches_actual_scanner_source':True,'injection_probe_escaped':True,'no_Lean_or_lesson_or_publication_edit':True,'bounded_scan_modules':1}
e=put('reader-adjacency.run-evidence86.json',{
 'schema':'astis.distinct-exact-renderer-repair-run86.v1','status':'closed','created_utc':now,'reviewer':'/root/fresh_source78','proposer':'/root','proposal':pin(proposal),'checks':checks,
 'timeline':['Exact proposal/three snapshot pins checked, before/after source and inline_lean/publication_reader inspected.','AST and in-memory syntax compilation found only render_unit semantic change.','Actual source scanner restricted in memory to candidate86 module; dependency names used only as link fixture metadata.','Before/proposed modules loaded separately in memory, same exact current candidate lesson rendered; DOM order, code, proof panels and injection escaping asserted.','Closed owned evidence; no canonical renderer/lesson/Lean/site write.'],
 'line_endings':{'before_CRLF':before.read_bytes().count(b'\r\n'),'before_LF':before.read_bytes().count(b'\n'),'after_CRLF':after.read_bytes().count(b'\r\n'),'after_LF':after.read_bytes().count(b'\n'),'assessment':'19 existing LF-only lines normalized to CRLF; no AST/content difference outside render_unit.'},
 'rendered_sample_hashes':{'before_html_sha256':sha(oldhtml.encode()),'proposed_html_sha256':sha(newhtml.encode()),'exact_statement_signature_sha256':sha(sig.encode()),'exact_full_public_proof_source_sha256':sha(exact.encode())},
 'input_metadata':{'candidate':pin(candidate),'lesson':pin(lesson),'publication':pin(publication)},
 'no_final_source86_verdict_or_semantic_state_read':True,'no_project_scan_site_build_or_compilation_of_Lean':True,'no_source_or_binder_change':True,'no_private_primary_bulk_content':True})
d=put('reader-adjacency.decision86.json',{
 'schema':'astis.distinct-exact-renderer-repair-decision86.v1','status':'closed','created_utc':now,'verdict':'ACCEPT_EXACT_RENDERER_RELOCATION_EXPOSITION_ONLY','proposal_raw_sha256':pin(proposal)['raw_sha256'],'review_run_sha256':e['raw_sha256'],
 'per_change':[{'change':p['changes'][0],'decision':'ACCEPT','evidence':'Identical statement disclosure HTML now is direct sibling immediately after the math statement formula and immediately before roadmap; one statement disclosure remains.'},{'change':p['changes'][1],'decision':'ACCEPT','evidence':'All11 proof step blocks and all7 full proof/helper disclosures byte-identical, closed; complete main theorem proof and complete private Prop helper retained.'},{'change':p['changes'][2],'decision':'ACCEPT','evidence':'Only proof remains at Lean verification after mathematical proof; explanation now states this exact placement.'}],
 'incidental_byte_change':'19 LF-only lines normalized to CRLF; source citation functions and all other top-level ASTs exactly unchanged.',
 'precise_extraction_boundary':'Statement panel retains the existing exact public theorem signature; referenced literal private proposition remains complete in the unchanged full-proposition helper disclosure. No claim that renderer elaborates or substitutes the proposition. Source splitting/sanitizing/escaping unchanged.',
 'checks':checks,'required_additional_repairs':[],
 'truth_boundary':'Distinct exact renderer/exposition repair accepted only. No mathematical/source-fidelity verdict, no proof/VERIFIED/Seal/state credit, no whole-site or live-page validation. Root alone may materialize the exact reviewed renderer.'})
inputs=[proposal,before,after,diff,canonical,R/'website/scripts/inline_lean.py',R/'website/scripts/publication_reader.py',candidate,lesson,publication]+local_imports
m=put('reader-adjacency.run-manifest86.json',{'schema':'astis.exact-renderer-repair-raw-manifest86.v1','status':'closed','created_utc':now,'raw_inputs':[pin(q) for q in dict.fromkeys(inputs)],'raw_outputs':[pin(q) for q in sorted(O.iterdir()) if q.is_file() and q.name!='reader-adjacency.run-manifest86.json'],'manifest_self_hash_omitted':True,'noncircular':'Evidence binds inputs and observed checks; decision binds evidence RAW; manifest binds all outputs except itself.','owned_only_outputs':True,'private_source_bulk_output_files':[]})
for q in [O/'reader-adjacency.decision86.json',O/'reader-adjacency.run-evidence86.json',O/'reader-adjacency.run-manifest86.json']:print(json.dumps(pin(q)))
