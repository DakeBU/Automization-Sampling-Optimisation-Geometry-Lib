from __future__ import annotations
from pathlib import Path
import ast, hashlib, html, json, re, types, datetime
ROOT=Path('E:/Samplinglib');OUT=Path(__file__).resolve().parent
R=ROOT/'runs/20261007-companion-priority/pbps-actual-finite-first-event-law86/reader-adjacency-repair86'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
proposal=R/'proposal.v4.json';renderer=R/'renderer.proposed.v4.exactraw.snapshot'
assert sha(proposal)=='31b67a3c8d2d59685fc8ef594e2e7588508ea0bc6527055c16750a4ffd3c3892'
assert sha(renderer)=='671dc0d177856b9c0f91f8acc6922f1e0e0cf57de5656b44cf8dbdea51cb9cdc'
unit=json.loads((ROOT/'website/content/declaration_lessons/pbps-actual-finite-first-event-law.json').read_text(encoding='utf-8'))['units'][0]
item=json.loads((ROOT/'website/content/publications/pbps-actual-finite-first-event-law.json').read_text(encoding='utf-8'))['items'][0]
module=(ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteFirstEventLaw.lean').read_text(encoding='utf-8')
ns='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteFirstEventLaw.'
starts=list(re.finditer(r'(?m)^(?:private )?(def|theorem) ([A-Za-z_][A-Za-z_0-9]*)',module))
known={}
for i,m in enumerate(starts):
 end=starts[i+1].start() if i+1<len(starts) else module.index('\nend AutoSamplingTheory',m.start())
 source=module[m.start():end].rstrip()
 # Remove the next main theorem's preceding set_option from previous helper.
 source=re.sub(r'\nset_option maxHeartbeats 1000000 in\s*$','',source)
 known[ns+m[2]]=types.SimpleNamespace(kind=m[1],short_name=m[2],source_text=source,source_file='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteFirstEventLaw.lean')
for n in unit['astis_dependencies']:
 known.setdefault(n,types.SimpleNamespace(kind='theorem',short_name=n.rsplit('.',1)[-1],source_text='',source_file=''))
def code_html(s):return '<pre><code>'+html.escape(s)+'</code></pre>'
def list_html(xs,empty=''):
 return '<ul>'+''.join('<li>'+html.escape(str(x))+'</li>' for x in xs)+'</ul>' if xs else empty
base=types.SimpleNamespace(esc=html.escape,sanitize_lean=lambda s:re.sub(r'/\*[\s\S]*?\*/|--[^\n]*','',s),source_href=lambda d,from_path:('module.html',None),lean_source_actions=lambda *a,**k:'',code_html=code_html,relative_prefix=lambda p:'../',declaration_path=lambda d:'module.html#'+d.short_name,list_html=list_html)
def extract_functions(path,names,env):
 tree=ast.parse(path.read_text(encoding='utf-8'))
 selected=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name in names]
 for n in selected:n.decorator_list=[]
 exec(compile(ast.Module(body=selected,type_ignores=[]),str(path),'exec'),env)
 return env
inline_env={'re':re,'base':base,'declarations':lambda:known}
extract_functions(ROOT/'website/scripts/inline_lean.py',{'split_statement','display_source','disclosure'},inline_env)
inline=types.SimpleNamespace(**inline_env)
env={'re':re,'inline_lean':inline,'base':base,'inline_text':html.escape,'source_citation':lambda s,p:'<li>source attribution</li>'}
extract_functions(renderer,{'render_unit'},env)
render=env['render_unit']
generic=render(unit,'lessons/candidate86.html')
# Exercise the real source_card composition without loading project aggregation
# or audit/registry files. Only unrelated badge/provenance helpers are stubbed.
dl=types.SimpleNamespace(render_unit=render,source_citation_anchor=lambda s,p:html.escape(s['label']))
pub=types.SimpleNamespace(inputs=lambda:{'audits':{},'lessons':{unit['declaration']:unit}},verified_binding=lambda *a:False)
pe={'publication':pub,'escape':html.escape,'declaration_lessons':dl,'astis_site':base,'re':re}
extract_functions(ROOT/'website/scripts/publication_reader.py',{'semantic_details','source_card'},pe)
companion=pe['source_card'](item,item['chapter_path'])
results=[]
for name,s in [('generic',generic),('companion',companion)]:
 p=OUT/('candidate-renderer-v4-'+name+'.html');p.write_text(s,encoding='utf-8')
 pos={k:s.index(v) for k,v in {'human_statement':'class="reader-claim"','formula':'reader-main-equation','statement_fold':'inline-lean-statement','roadmap':'Proof roadmap','proof_steps':'class="proof-reader-step"','full_proof':'class="lean-verification"'}.items()}
 assert list(pos.values())==sorted(pos.values()),pos
 statement=s[pos['statement_fold']:pos['roadmap']]
 proof=s[pos['full_proof']:]
 fullprop=ns+'actual_finite_first_event_law_statement'
 assert statement.count('data-inline-lean="'+fullprop+'"')==1
 assert 'let P : Measure' in html.unescape(statement)
 assert 'let J : E' in html.unescape(statement)
 assert '∀ M : ℝ' in html.unescape(statement)
 assert 'data-inline-lean="'+fullprop+'"' not in proof
 assert statement.index('</details>') < statement.index('data-inline-lean="'+fullprop+'"')
 for h in unit['helpers'][1:]:
  assert statement.count('data-inline-lean="'+h+'"')==0
  assert proof.count('data-inline-lean="'+h+'"')==1
 # Every detail is initially closed and all eleven step source texts survive.
 assert not re.search(r'<details[^>]*\bopen(?:\s|=|>)',s)
 assert s.count('<summary>Corresponding Lean step</summary>')==11
 for step in unit['steps']:assert html.escape(step['lean']) in s
 results.append({'surface':name,'html':str(p.relative_to(ROOT)),'raw_sha256':sha(p),'positions':pos,'adjacent_complete_statement_before_roadmap':True,'expanded_literal_Prop_once_as_adjacent_sibling_in_statement_group':True,'genuine_proof_helpers_once_inside_later_proof_fold':True,'all11_exact_adjacent_step_folds':True,'all_details_initially_closed':True})
report={'schema':'astis.independent-source86.renderer-v4-candidate-inspection.v1','reviewer':'independent-primary-source-reviewer86','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'proposal':{'path':str(proposal.relative_to(ROOT)),'raw_sha256':sha(proposal)},'renderer':{'path':str(renderer.relative_to(ROOT)),'raw_sha256':sha(renderer)},'results':results,'method':'Executed exact AST-extracted proposed render_unit, inline_lean split/display/disclosure and publication_reader source_card functions using exact current authorized module source and lesson/publication. Presentation-only code/list/link helpers and no-audit TODO badge input supplied locally; project scans and aggregation/registry reads avoided.','candidate_layout_verdict':'ACCEPTED_AS_PROPOSED_FOR_THIS_DECLARATION','limitations':['Not a separate proposal repair reviewer verdict','Canonical renderer not mutated','Full site generation, actual applied renderer output, browser rendering and live publication unverified','V3 candidate source review retained as superseded layout evidence; V4 sibling avoids hidden enclosing signature fold','All original source-first/provisional observations retained']}
p=OUT/'renderer-v4-candidate-inspection86.json';p.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'path':str(p.relative_to(ROOT)),'raw_sha256':sha(p),'results':results},indent=2))
