"""Distinct V4 exact renderer partition/adjacency audit. No canonical writes."""
from pathlib import Path
from html.parser import HTMLParser
import ast,copy,datetime,difflib,hashlib,json,re,sys,types
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;B=O.parent.parent/'reader-adjacency-repair86'
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(b),bytes=len(b))
def put(n,j):
 p=O/n;assert not p.exists(),n;p.write_bytes((json.dumps(j,ensure_ascii=False,indent=2)+'\n').encode());return pin(p)
proposal=B/'proposal.v4.json';assert pin(proposal)['raw_sha256']=='31b67a3c8d2d59685fc8ef594e2e7588508ea0bc6527055c16750a4ffd3c3892'
p=json.loads(proposal.read_bytes());before=R/p['before']['path'];after=R/p['after']['path'];diff=R/p['diff']['path']
for q,k in [(before,'before'),(after,'after'),(diff,'diff')]:assert pin(q)['raw_sha256']==p[k]['RAW_sha256'] and pin(q)['bytes']==p[k]['bytes']
canonical=R/'website/scripts/declaration_lessons.py';assert canonical.read_bytes()==before.read_bytes()
ab,aa=ast.parse(before.read_bytes()),ast.parse(after.read_bytes())
def topnodes(t):return {getattr(n,'name',f'node{k}'):ast.dump(n,include_attributes=False) for k,n in enumerate(t.body)}
nb,na=topnodes(ab),topnodes(aa);assert nb.keys()==na.keys();assert [k for k in nb if nb[k]!=na[k]]==['render_unit']
ops=[q for q in difflib.SequenceMatcher(a=before.read_bytes().splitlines(keepends=True),b=after.read_bytes().splitlines(keepends=True),autojunk=False).get_opcodes() if q[0]!='equal']
assert all(149<=q[1] and q[2]<=210 for q in ops)
compile(before.read_bytes(),str(before),'exec');compile(after.read_bytes(),str(after),'exec')
sys.dont_write_bytecode=True;sys.path[:0]=[str(R/'tools'),str(R/'website/scripts')]
import astis_site as base
import inline_lean
candidate=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteFirstEventLaw.lean'
lesson=R/'website/content/declaration_lessons/pbps-actual-finite-first-event-law.json'
publication=R/'website/content/publications/pbps-actual-finite-first-event-law.json'
unit=json.loads(lesson.read_bytes())['units'][0]
base.project_lean_paths=lambda:[candidate];mods,decls=base.scan_project_sources();assert len(mods)==1
base._SOURCE_BY_NAME={d.full_name:d for d in decls}
for name in unit.get('astis_dependencies',[]):
 module,short=name.rsplit('.',1);base._SOURCE_BY_NAME[name]=base.SourceDeclaration(name,short,'theorem',module,module.replace('.','/')+'.lean',1,'','',short,False,[])
base._ACTIVE_GIT=types.SimpleNamespace(web_root='',commit='',commit_published=False,public_source_links=False,dirty_files=set())
inline_lean.declarations.cache_clear()
def load(raw,name):
 m=types.ModuleType(name);m.__file__=str(canonical);exec(compile(raw,str(canonical),'exec'),m.__dict__);return m
old,new=load(before.read_bytes(),'before_v4_86'),load(after.read_bytes(),'proposed_v4_86')
parser_source=O.parent/'review_renderer86.py';t=ast.parse(parser_source.read_text(encoding='utf8'))
exec(compile(ast.Module(body=[n for n in t.body if isinstance(n,ast.ClassDef) and n.name in ['Node','DOM']],type_ignores=[]),str(parser_source),'exec'),globals())
h0=old.render_unit(unit,'lessons/repair86.html');h1=new.render_unit(unit,'lessons/repair86.html');d0,d1=DOM(h0),DOM(h1)
def panel_map(d):return {(n.attrs['data-inline-lean'],'statement' if n.cls('inline-lean-statement') else 'proof'):n for n in d.nodes if 'data-inline-lean' in n.attrs}
panels0,panels1=panel_map(d0),panel_map(d1);assert panels0.keys()==panels1.keys() and len(panels1)==8
def own_code(d,n):
 return ''.join(next(q for q in d.nodes if q.tag=='code' and q.parent and q.parent.tag=='pre' and q.parent.parent==n).parts)
def ancestor(n,a):
 while n.parent:
  if n.parent is a:return True
  n=n.parent
 return False
main=unit['declaration'];statement=panels1[(main,'statement')];fullproof=panels1[(main,'proof')]
section=next(n for n in d1.nodes if n.cls('reader-first-pass'));eq=next(n for n in section.children if n.cls('reader-main-equation'));idx=section.children.index(eq)
assert section.children[idx+1] is statement and ''.join(section.children[idx+3].parts)=='Proof roadmap'
expected_prop=[];expected_proofs=[];partition=[]
for name in unit['helpers']:
 item=base._SOURCE_BY_NAME[name];sig,_=inline_lean.split_statement(inline_lean.display_source(item.source_text))
 is_prop=item.kind=='def' and item.short_name.endswith('_statement') and re.search(r':\s*Prop\s*$',base.sanitize_lean(sig)) is not None
 (expected_prop if is_prop else expected_proofs).append(name)
 panel=panels1[(name,'proof')];assert (panel.parent is statement.parent) if is_prop else ancestor(panel,fullproof)
 assert not ancestor(panel,fullproof) if is_prop else not ancestor(panel,statement)
 assert d0.raw(panels0[(name,'proof')])==d1.raw(panel)
 assert own_code(d1,panel)==inline_lean.display_source(item.source_text)
 partition.append({'helper':name,'kind':item.kind,'literal_Prop_classifier':is_prop,'placement':'immediately adjacent sibling full-proposition fold' if is_prop else 'inside complete proof fold','exact_code_and_disclosure_preserved':True})
assert len(expected_prop)==1 and len(expected_proofs)==5
prop_panel=panels1[(expected_prop[0],'proof')];prop_code=own_code(d1,prop_panel)
assert all(x in prop_code for x in ['(hα :','(hαβ :','(hV :','(hH :','(hη :','(hβη :','let P :','let ε :','let c :','let Φ :','let S :','let rate :','let Λ :','let τ :','let U :','let F :','let A :','let d :','let ρ :','let J :','Integrable h','IsFiniteMeasure'])
assert 'Full Lean proposition (definition)' in d1.raw(prop_panel)
assert section.children[idx+2] is prop_panel
# Reproduce current browser proof-summary traversal: ancestors must already be open.
def click_sequence_visible(dom):
 opened=set()
 for panel in dom.byclass('inline-lean-proof'):
  parent=panel.parent
  while parent:
   if parent.tag=='details' and id(parent) not in opened:return False,parent.attrs
   parent=parent.parent
  opened.add(id(panel))
 return len(opened)==len(dom.byclass('inline-lean-proof')),None
assert click_sequence_visible(d1)==(True,None)
v3snapshot=B/'renderer.proposed.v3.exactraw.snapshot'
v3module=load(v3snapshot.read_bytes(),'retained_v3_compatibility_probe')
v3dom=DOM(v3module.render_unit(unit,'lessons/repair86.html'))
v3_visibility,v3_blocker=click_sequence_visible(v3dom)
assert not v3_visibility and 'inline-lean-statement' in v3_blocker.get('class','')
for key in [(main,'statement'),(main,'proof')]:assert own_code(d0,panels0[key])==own_code(d1,panels1[key])
assert len(d0.byclass('proof-reader-step'))==len(d1.byclass('proof-reader-step'))==11
assert [d0.raw(n) for n in d0.byclass('proof-reader-step')]==[d1.raw(n) for n in d1.byclass('proof-reader-step')]
assert all('open' not in n.attrs for n in d1.nodes if n.tag=='details')
assert sum('data-inline-lean' in n.attrs for n in d1.nodes)==len(panels1)
# Ordinary no-helper declaration fixture: exercises renderer behavior, not a Lean theorem certificate.
fname='ReaderFixture.plain';fsrc='theorem plain (x : ℝ) : x = x := by\n  rfl'
base._SOURCE_BY_NAME[fname]=base.SourceDeclaration(fname,'plain','theorem','ReaderFixture','ReaderFixture.lean',1,fsrc,'','fixture',False,[])
plain=copy.deepcopy(unit);plain['declaration']=fname;plain.pop('helpers');plain['sources']=[];plain['astis_dependencies']=[]
ordinary=DOM(new.render_unit(plain,'lessons/plain.html'));ordinary_panels=panel_map(ordinary)
assert len(ordinary_panels)==2 and set(ordinary_panels)=={(fname,'statement'),(fname,'proof')}
assert own_code(ordinary,ordinary_panels[(fname,'statement')])==inline_lean.split_statement(fsrc)[0]
assert own_code(ordinary,ordinary_panels[(fname,'proof')])==fsrc
assert all('open' not in n.attrs for n in ordinary.nodes if n.tag=='details')
mal=copy.deepcopy(unit);probe='<script id="repair-inject">BAD()</script>'
for k in ['title','statement','formula','lean_statement','lean_proof']:mal[k]+=probe
mal['steps'][0]['text']+=probe;mal['steps'][0]['lean']+=probe
injected=new.render_unit(mal,'lessons/injection.html');assert probe not in injected and '&lt;script' in injected
assert not [n for n in DOM(injected).nodes if n.tag=='script']
pub=json.loads(publication.read_bytes());assert pub['items'][0]['statement']==unit['statement']
local_imports=[]
for m in list(sys.modules.values()):
 f=getattr(m,'__file__',None)
 if f:
  q=Path(f)
  try:q.relative_to(R)
  except ValueError:continue
  if q.is_file() and q.suffix=='.py':local_imports.append(q)
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
checks={'syntax_compile_in_memory':'PASS','only_AST_render_unit_changed':True,'all_unchanged_line_bytes_preserved_outside_render_changes':True,'same_public_signature_and_full_theorem_proof_code':True,'expanded_private_literal_Prop_now_immediately_adjacent_sibling_after_signature':True,'browser_proof_summary_click_traversal_visible':True,'retained_V3_nested_statement_parent_regression_reproduced':True,'six_source_binders_and14definitions_and_all_outputs_in_sibling_specification':True,'statement_immediately_after_math_formula_before_roadmap':True,'five_genuine_proof_helpers_retained_under_proof':True,'literal_Prop_disclosure_not_duplicated_under_proof':True,'all11_step_blocks_byte_identical':True,'all_disclosures_closed':True,'all8_role_name_panels_exactly_once':True,'ordinary_no_helper_fixture_PASS':True,'injection_probe_escaped':True,'bounded_source_scan_one_module':True}
e=put('reader-adjacency.run-evidence86.json',{'schema':'astis.distinct-exact-reader-v4-run86.v1','status':'closed','created_utc':now,'reviewer':'/root/fresh_source78','proposer':'/root','proposal':pin(proposal),'checks':checks,'partition':partition,'byte_edit_opcodes':ops,'timeline':['Exact V4 proposal/before/after/diff hashes verified; V4 partition logic independently compared with inline_lean literal_statement classification.','Before and V4 modules syntax-compiled and loaded separately in memory. Real scanner bounded to candidate86 only; parent links fixture metadata, no parent BODY read.','Exact current candidate lesson rendered in both versions; sibling statement, expanded literal specification, five proof helper disclosures, main proof code, all11 authored steps and closed DOM hierarchy checked.','Ordinary no-helper source-syntax fixture and HTML injection probe checked. No site build or canonical writes.'],'render_hashes':{'before':sha(h0.encode()),'V4':sha(h1.encode()),'expanded_literal_Prop_code':sha(prop_code.encode())},'prior_versions':'V1/V2/V3 observations immutable. V3 DOM/content acceptance did not check current browser click traversal; its nested statement-parent blocker is independently reproduced here. V4 is authoritative sibling-adjacency repair.', 'browser_compatibility':{'checker':pin(R/'website/scripts/check_cross_domain_browser.py'),'checked_lines':'237-258','V3_blocker':v3_blocker,'V4_selector_count':'1 statement +7 proof-role panels for public theorem and6helpers','V4_all_proof_summaries_visible_in_existing_document_order':True},'no_final_source_verdict_or_shared_state':True})
d=put('reader-adjacency.decision86.json',{'schema':'astis.distinct-exact-reader-v4-decision86.v1','status':'closed','created_utc':now,'verdict':'ACCEPT_EXACT_V4_RENDERER_ADJACENCY_AND_LITERAL_PROP_PARTITION_EXPOSITION_ONLY','proposal_raw_sha256':pin(proposal)['raw_sha256'],'renderer_after_raw_sha256':pin(after)['raw_sha256'],'review_run_sha256':e['raw_sha256'],'per_change':[{'change':q,'decision':'ACCEPT_EXACT_V4_OPERATION'} for q in p['changes']],'checks':checks,'helper_partition':partition,'minimality':'Only render_unit changes semantically: classify existing literal-Prop helpers by same kind/name/sanitized-signature predicate, place those exact disclosures as siblings beside the adjacent signature fold, remove them from proof helper list, preserve all five proof helpers and11 authored steps, update placement sentence. No source/Lean/lesson/binder/proof alteration.','source_extraction':'Complete literal private Prop, with original six hypotheses,14 definitions and all measure/integrability outputs, is now accessible in an initially closed sibling fold immediately after signature before roadmap. Public signature, private proposition source and all theorem/helper proof source remain exact scanner-extracted code, not generated/elaborated substitutes.','required_repairs':[],'V1_V2_V3_retained':True,'V3_not_safe_for_current_browser_checker':True,'scope_wording':'Proposal change4 statement disclosure is interpreted as adjacent statement area, concretely sibling layout specified by change5 and exact V4 code; never nested under the closed signature parent.','truth_boundary':'Accept exact V4 renderer exposition only; no final source86 semantic verdict, mathematical proof credit, VERIFIED, site/live completeness, or canonical mutation.'})
inputs=[v3snapshot,R/'website/scripts/check_cross_domain_browser.py',proposal,before,after,diff,canonical,R/'website/scripts/inline_lean.py',R/'website/scripts/publication_reader.py',candidate,lesson,publication,parser_source,O.parent/'reader-adjacency.decision86.json',O.parent/'v2/reader-adjacency.decision86.json']+local_imports
m=put('reader-adjacency.run-manifest86.json',{'schema':'astis.raw-distinct-reader-v4-manifest86.v1','status':'closed','created_utc':now,'raw_inputs':[pin(q) for q in dict.fromkeys(inputs)],'raw_outputs':[pin(q) for q in sorted(O.iterdir()) if q.is_file() and q.name!='reader-adjacency.run-manifest86.json'],'manifest_self_hash_omitted':True,'noncircular':'Evidence binds input payload/checks, decision binds evidence RAW, manifest binds all outputs except itself. Prior V1/v2 outputs unchanged.','owned_only_outputs':True,'private_primary_bulk_outputs':[]})
for q in [O/'reader-adjacency.decision86.json',O/'reader-adjacency.run-evidence86.json',O/'reader-adjacency.run-manifest86.json']:print(json.dumps(pin(q)))
